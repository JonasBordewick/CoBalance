using System;
using CoBalance.Logger;
using UnityEngine;

namespace CoBalance
{
    public sealed class BalanceLogSource : MonoBehaviour
    {
        private GameStatLogger _logger;

        private void OnEnable()
        {
            _logger = FindFirstObjectByType<GameStatLogger>();
            if (_logger == null)
            {
                CoBalanceLogger.LogError("No GameStatLogger found in the scene. BalanceLogSource will not function.");
                return;
            }
            _logger.RegisterLogSource(this);
        }
        
        private void OnDisable()
        {
            if (_logger != null)
            {
                _logger.DeregisterLogSource(this);
            }
        }
    }
}