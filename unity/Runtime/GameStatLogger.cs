using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using CoBalance.DTO;
using CoBalance.Logger;
using CoBalance.Simulations;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace CoBalance
{
    public class GameStatLogger: MonoBehaviour
    {
        public static GameStatLogger Instance { get; private set; }

         private void OnEnable()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
        }
        
        
        [Header("Logging")]
        [SerializeField] private bool isEnabled = true;
        [SerializeField] private string sessionID = "run";
        [SerializeField] private int flushEveryLines = 50;
        
        private readonly List<LogDescriptor> _descriptors = new List<LogDescriptor>();
        private readonly HashSet<(int, string)> _registeredInstances = new HashSet<(int, string)>();
        private StreamWriter _writer;
        
        private int _tickRate = 100;
        private int _tick;
        private int _linesSinceFlush;
        
        private BalanceFrameworkSettings _settings;


        private void Awake()
        {
            DontDestroyOnLoad(gameObject);
            _settings = BalanceFrameworkSettings.Load();
            
            _openFileInWriter();
            _rescanScene();
            
            _tickRate = _settings.defaultLogTickRate;
            isEnabled = _settings.enableTimeBasedLogging;

            SceneManager.sceneLoaded += OnSceneLoaded;
        }
        
        private void FixedUpdate()
        {
            if (!isEnabled || _writer == null) return;

            _tick++;
            
            var t = Time.fixedTime;

            foreach (var d in _descriptors)
            {
                if (_tick % _tickRate != 0) continue;

                object v;
                try { v = d.Getter(); }
                catch { continue; }

                _writeSample(t, d, v);
            }

            if (_linesSinceFlush >= flushEveryLines)
            {
                _writer.Flush();
                _linesSinceFlush = 0;
            }
        }

        /// <summary>Writes a snapshot of all registered [BalanceLog] fields to the log at the current fixed time.</summary>
        public void LogGameStats()
        {
            var time = Time.fixedTime;

            foreach (var descriptor in _descriptors)
            {
                object value;
                try { value = descriptor.Getter(); }
                catch { continue; }

                _writeSample(time, descriptor, value);
            }
        }

        /// <summary>Writes a single key/value pair to the log at the current fixed time.</summary>
        public void LogGameStat(string key, object value)
        {
            var time = Time.fixedTime;
            var descriptor = new LogDescriptor(key, () => value);
            _writeSample(time, descriptor, value);
        }

        /// <summary>Writes a single key/value pair to the log at the given timestamp.</summary>
        public void LogGameStat(float t, string key, object value)
        {
            var descriptor = new LogDescriptor(key, () => value);
            _writeSample(t, descriptor, value);
        }

        private void OnDestroy()
        {
            SceneManager.sceneLoaded -= OnSceneLoaded;
            _closeFile();
        }

        private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
        {
            _rescanScene();
        }

        private void _openFileInWriter()
        {
            try
            {
                var stamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
                var path = Utilities.GetLogFilePath($"{sessionID}_{stamp}.jsonl");
                
                if (JobContext.IsJobMode)
                {
                    var jobId = JobContext.CurrentJobSettings.jobId;
                    var counter = JobContext.Counter ?? "0";
                    path = Utilities.GetLogFilePath($"{jobId}_{counter}.jsonl");
                }
                
                var dir = Path.GetDirectoryName(path);
                if (!string.IsNullOrEmpty(dir))
                    Directory.CreateDirectory(dir);

                _writer = new StreamWriter(
                    path,
                    append: false,
                    encoding: new System.Text.UTF8Encoding(encoderShouldEmitUTF8Identifier: true)
                );
                _writer.AutoFlush = false;
                
            }
            catch (Exception ex)
            {
                Debug.LogError($"Failed to open log file: {ex.Message}");
                isEnabled = false;
            }
        }
        
        private void _writeSample(float time, LogDescriptor logDescriptor, object obj)
        {
            if (obj == null)
                return;

            var cultureInfo =CultureInfo.InvariantCulture;

            switch (obj)
            {
                case float fv:
                    _writer.WriteLine(
                        $"{{\"t\":{time.ToString("F4", cultureInfo)},\"k\":\"{logDescriptor.Key}\",\"v\":{fv.ToString(cultureInfo)}}}");
                    break;

                case double dv:
                    _writer.WriteLine(
                        $"{{\"t\":{time.ToString("F4", cultureInfo)},\"k\":\"{logDescriptor.Key}\",\"v\":{dv.ToString(cultureInfo)}}}");
                    break;

                case int iv:
                    _writer.WriteLine(
                        $"{{\"t\":{time.ToString("F4", cultureInfo)},\"k\":\"{logDescriptor.Key}\",\"v\":{iv.ToString(cultureInfo)}}}");
                    break;

                case long lv:
                    _writer.WriteLine(
                        $"{{\"t\":{time.ToString("F4", cultureInfo)},\"k\":\"{logDescriptor.Key}\",\"v\":{lv.ToString(cultureInfo)}}}");
                    break;

                default:
                    if (obj is IConvertible)
                    {
                        double num = Convert.ToDouble(obj, cultureInfo);
                        _writer.WriteLine(
                            $"{{\"t\":{time.ToString("F4", cultureInfo)},\"k\":\"{logDescriptor.Key}\",\"v\":{num.ToString(cultureInfo)}}}");
                    }
                    return;
            }

            _linesSinceFlush++;
        }

        private void _closeFile()
        {
            try
            {
                _writer?.Flush();
                _writer?.Dispose();
            }
            catch { }
            finally
            {
                _writer = null;
            }
        }

        private void _rescanScene()
        {
            _descriptors.Clear();
            _registeredInstances.Clear();
            
            var monoBehaviours = FindObjectsByType<MonoBehaviour>(FindObjectsInactive.Include, FindObjectsSortMode.None);
            foreach (var mb in monoBehaviours)
            {
                if (mb == null) continue;
                _collectLogDescriptorsFromObject(mb);
                _collectReferencedScriptableObjects(mb);
            }
        }

        private List<(int, LogDescriptor)> _collectLogDescriptorsFromObject(UnityEngine.Object obj)
        {
            var descriptors = new List<(int, LogDescriptor)>();
            var type = obj.GetType();
            var flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;

            foreach (var fieldInfo in type.GetFields(flags))
            {
                var logAttr = fieldInfo.GetCustomAttribute<BalanceLogAttribute>();
                if (logAttr == null) continue;
                
                var key = string.IsNullOrEmpty(logAttr.Key) ? fieldInfo.Name : logAttr.Key;
                
                var descriptor = new LogDescriptor(key, () => fieldInfo.GetValue(obj));
                descriptors.Add((obj.GetInstanceID(), descriptor));
                
                if (_registeredInstances.Contains((obj.GetInstanceID(), key)))
                {
                    CoBalanceLogger.LogWarning(
                        $"Duplicate log key '{key}' on object '{obj.name}' (instance ID: {obj.GetInstanceID()}). Skipping registration.");
                    continue;
                }
                
                _descriptors.Add(descriptor);
                _registeredInstances.Add((obj.GetInstanceID(), key));
            }

            return descriptors;
        }
        
        private void _collectReferencedScriptableObjects(object source)
        {
            var flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
            var fields = source.GetType().GetFields(flags);

            foreach (var field in fields)
            {
                if (!typeof(ScriptableObject).IsAssignableFrom(field.FieldType))
                    continue;

                var so = field.GetValue(source) as ScriptableObject;
                if (so == null) continue;

                _collectLogDescriptorsFromObject(so);
            }
        }

        public void RegisterLogSource(MonoBehaviour source)
        {
            if (source == null) return;
            var monoBehaviours = source.GetComponents<MonoBehaviour>();
            foreach (var mb in monoBehaviours)
            {
                _collectLogDescriptorsFromObject(mb);
            }
        }
        
        public void DeregisterLogSource(MonoBehaviour source)
        {
            if (source == null) return;
            var descriptorsToRemove = _collectLogDescriptorsFromObject(source);
            foreach (var (instanceID, descriptor) in descriptorsToRemove)
            {
                _registeredInstances.Remove((instanceID, descriptor.Key));
                
                _descriptors.Where(d => d.Key == descriptor.Key)
                    .ToList()
                    .ForEach(d => _descriptors.Remove(d));
            }
        }
        
    }
}