{% raw %}
import React, { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

export default function App() {
  const [config, setConfig] = useState(null);
  const [configError, setConfigError] = useState("");
  const [loadingConfig, setLoadingConfig] = useState(true);

  const [taskId, setTaskId] = useState("");
  const [taskState, setTaskState] = useState("");
  const [taskResult, setTaskResult] = useState(null);
  const [taskError, setTaskError] = useState("");
  const [isPolling, setIsPolling] = useState(false);

  useEffect(() => {
    async function loadConfig() {
      try {
        setLoadingConfig(true);
        setConfigError("");

        const response = await fetch(`${API_BASE}/config`);
        if (!response.ok) {
          throw new Error(`Config request failed: ${response.status}`);
        }

        const data = await response.json();
        setConfig(data);
      } catch (error) {
        setConfigError(error.message || "Failed to load config");
      } finally {
        setLoadingConfig(false);
      }
    }

    loadConfig();
  }, []);

  async function runPingTask() {
    try {
      setTaskError("");
      setTaskResult(null);
      setTaskState("queueing");

      const response = await fetch(`${API_BASE}/tasks/ping`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Task request failed: ${response.status}`);
      }

      const data = await response.json();
      setTaskId(data.task_id);
      setTaskState(data.status || "queued");
      setIsPolling(true);
    } catch (error) {
      setTaskError(error.message || "Failed to queue task");
      setTaskState("failed");
      setIsPolling(false);
    }
  }

  useEffect(() => {
    if (!taskId || !isPolling) return;

    let cancelled = false;

    async function pollTask() {
      try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`);
        if (!response.ok) {
          throw new Error(`Task status request failed: ${response.status}`);
        }

        const data = await response.json();
        if (cancelled) return;

        setTaskState(data.state || "");

        if (data.ready) {
          setIsPolling(false);

          if (data.successful) {
            setTaskResult(data.result ?? null);
          } else {
            setTaskError(data.error || "Task failed");
          }
        }
      } catch (error) {
        if (!cancelled) {
          setTaskError(error.message || "Polling failed");
          setIsPolling(false);
        }
      }
    }

    pollTask();
    const timer = setInterval(pollTask, 1500);

    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [taskId, isPolling]);

  const featureEntries = config?.features ? Object.entries(config.features) : [];

  return (
    <div>
      <h1>ForgeStack Generated App</h1>

      <section style={{ marginBottom: "2rem" }}>
        <h2>Configuration</h2>

        {loadingConfig && <p>Loading config...</p>}
        {configError && <p>{configError}</p>}

        {config && (
          <div>
            <p><strong>Project:</strong> {config.project_name}</p>
            <p><strong>Stack:</strong> {config.stack_name}</p>
            <p><strong>App:</strong> {config.app_name}</p>

            <div>
              <strong>Features:</strong>
              {featureEntries.length === 0 ? (
                <p>None</p>
              ) : (
                <ul>
                  {featureEntries.map(([name, enabled]) => (
                    <li key={name}>
                      {name}: {String(enabled)}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}
      </section>

      <section>
        <h2>Async Task Demo</h2>
        <button onClick={runPingTask}>Run Ping Task</button>

        {taskId && <p><strong>Task ID:</strong> {taskId}</p>}
        {taskState && <p><strong>Task State:</strong> {taskState}</p>}
        {isPolling && <p>Polling for completion...</p>}

        {taskResult && (
          <div>
            <strong>Task Result:</strong>
            <pre>{JSON.stringify(taskResult, null, 2)}</pre>
          </div>
        )}

        {taskError && <p>{taskError}</p>}
      </section>
    </div>
  );
}
{% endraw %}