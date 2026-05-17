using System;
using BalancingFramework.Logger;
using UnityEditor;
using UnityEngine;

namespace BalancingFramework.Editor.Windows
{
    public class LogConsoleWindow : EditorWindow
    {
        private Vector2 _scroll;
        private bool _autoScroll = true;

        private bool _showInfo = true;
        private bool _showWarning = true;
        private bool _showError = true;

        private string _search = "";

        [MenuItem("Balancing/Log Console")]
        public static void Open()
        {
            var w = GetWindow<LogConsoleWindow>("Balancing Log Console");
            w.minSize = new Vector2(560, 320);
            w.Show();
        }

        private void OnEnable()
        {
            BalancingFrameworkLogger.OnLogMessageAdded += OnNewLog;
        }

        private void OnDisable()
        {
            BalancingFrameworkLogger.OnLogMessageAdded -= OnNewLog;
        }

        private void OnNewLog(BalancingLogMessage _)
        {
            Repaint();
        }

        private void OnGUI()
        {
            DrawToolbar();

            EditorGUILayout.Space(4);

            _scroll = EditorGUILayout.BeginScrollView(_scroll);

            var entries = BalancingFrameworkLogger.LogMessages;
            for (int i = 0; i < entries.Count; i++)
            {
                var e = entries[i];
                if (!PassFilter(e)) continue;

                using (new EditorGUILayout.HorizontalScope(GUI.skin.box))
                {
                    GUILayout.Label(GetIcon(e.Level), GUILayout.Width(18), GUILayout.Height(18));
                    
                    EditorGUILayout.LabelField($"[{e.Timestamp:HH:mm:ss}] {e.Message}", EditorStyles.wordWrappedLabel);
                }
            }

            EditorGUILayout.EndScrollView();

            if (_autoScroll && Event.current.type == EventType.Repaint)
                _scroll.y = float.MaxValue;
        }

        private void DrawToolbar()
        {
            using (new EditorGUILayout.HorizontalScope(EditorStyles.toolbar))
            {
                if (GUILayout.Button("Clear", EditorStyles.toolbarButton, GUILayout.Width(60)))
                    BalancingFrameworkLogger.Clear();

                GUILayout.Space(8);

                _showInfo = GUILayout.Toggle(_showInfo, "Info", EditorStyles.toolbarButton);
                _showWarning = GUILayout.Toggle(_showWarning, "Warning", EditorStyles.toolbarButton);
                _showError = GUILayout.Toggle(_showError, "Error", EditorStyles.toolbarButton);

                GUILayout.Space(12);
                GUILayout.Label("Search:", GUILayout.Width(48));
                _search = GUILayout.TextField(_search, EditorStyles.toolbarTextField, GUILayout.MinWidth(120));

                GUILayout.FlexibleSpace();
                _autoScroll = GUILayout.Toggle(_autoScroll, "Auto-Scroll", EditorStyles.toolbarButton);
            }
        }

        private bool PassFilter(BalancingLogMessage e)
        {
            if (!string.IsNullOrEmpty(_search))
            {
                var s = _search.Trim();
                if (!e.Message.Contains(s, StringComparison.OrdinalIgnoreCase))
                    return false;
            }

            switch (e.Level)
            {
                case BalancingLogLevel.Info: return _showInfo;
                case BalancingLogLevel.Warning: return _showWarning;
                case BalancingLogLevel.Error: return _showError;
                default: return true;
            }
        }

        private static GUIContent GetIcon(BalancingLogLevel level)
        {
            switch (level)
            {
                case BalancingLogLevel.Warning:
                    return EditorGUIUtility.IconContent("console.warnicon");
                case BalancingLogLevel.Error:
                    return EditorGUIUtility.IconContent("console.erroricon");
                default:
                    return EditorGUIUtility.IconContent("console.infoicon");
            }
        }
    }
}