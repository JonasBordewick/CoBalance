using System;
using System.Collections.Generic;

namespace CoBalance.Logger
{
    public enum BalancingLogLevel
    {
        Info,
        Warning,
        Error
    }
        
    public readonly struct BalancingLogMessage
    {
        public readonly DateTime Timestamp;
        public readonly BalancingLogLevel Level;
        public readonly string Message;
            
        public BalancingLogMessage(BalancingLogLevel level, string message)
        {
            Timestamp = DateTime.Now;
            Level = level;
            Message = message;
        }
    }

    public static class CoBalanceLogger
    {
        private const string LogTag = "[CoBalance] ";
        
        private const int MaxLogMessages = 1000;
        private static readonly List<BalancingLogMessage> _logMessages = new List<BalancingLogMessage>(MaxLogMessages);
        
        public static event Action<BalancingLogMessage> OnLogMessageAdded;
        public static IReadOnlyList<BalancingLogMessage> LogMessages => _logMessages.AsReadOnly();

        public static void Clear()
        {
            _logMessages.Clear();
        }

        public static void LogInfo(string message) => AddLogMessage(BalancingLogLevel.Info, LogTag + message);
        public static void LogWarning(string message) => AddLogMessage(BalancingLogLevel.Warning, LogTag + message);
        public static void LogError(string message) => AddLogMessage(BalancingLogLevel.Error, LogTag + message);
        
        private static void AddLogMessage(BalancingLogLevel level, string message)
        {
            var logMessage = new BalancingLogMessage(level, message);
            _logMessages.Add(logMessage);
            if (_logMessages.Count > MaxLogMessages)
            {
                _logMessages.RemoveAt(0);
            }
            OnLogMessageAdded?.Invoke(logMessage);
        }
    }
}