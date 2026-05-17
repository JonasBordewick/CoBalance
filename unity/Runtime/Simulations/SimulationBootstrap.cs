using UnityEngine;

namespace BalancingFramework.Simulations
{
    public sealed class SimulationBootstrap : MonoBehaviour
    {
#if UNITY_EDITOR
        private int _tick;
        private int _maxTick;

        private void OnEnable()
        {
            if (!JobContext.IsJobMode)
            {
                Debug.LogError(JobContext.DebugString());
                Destroy(gameObject);
                return;
            }

            SimulationRunTerminator.ResetState();

            Time.timeScale = JobContext.CurrentJobSettings.execution.timeScale;
            Time.fixedDeltaTime = JobContext.CurrentJobSettings.execution.fixedDeltaTime;

            _tick = 0;
            _maxTick = Mathf.CeilToInt(
                JobContext.CurrentJobSettings.execution.maxSimulationTime / Time.fixedDeltaTime
            );
        }

        private void FixedUpdate()
        {
            if (_tick >= _maxTick)
            {
                SimulationRunTerminator.FinishRun("maxSimulationTime");
                return;
            }

            _tick++;
        }
#endif
    }
}