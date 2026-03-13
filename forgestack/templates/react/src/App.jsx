{% raw %}
import React, { useEffect, useMemo, useState } from "react";

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

  const [items, setItems] = useState([]);
  const [itemsLoading, setItemsLoading] = useState(false);
  const [itemsError, setItemsError] = useState("");

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

  const featureEntries = config?.features ? Object.entries(config.features) : [];
  const isTechnicianConsole =
    config?.app_name === "technician-console" || Boolean(config?.features?.technician_console);
  const isDataWorkbench =
    config?.app_name === "data-workbench" || Boolean(config?.features?.workbench);
  const hasSQLite = Boolean(config?.sqlite?.enabled);
  const hasJupyter = Boolean(config?.jupyter?.enabled);

  async function loadItems() {
    try {
      setItemsLoading(true);
      setItemsError("");

      const response = await fetch(`${API_BASE}/items`);
      if (!response.ok) {
        throw new Error(`Items request failed: ${response.status}`);
      }

      const data = await response.json();
      setItems(Array.isArray(data) ? data : []);
    } catch (error) {
      setItemsError(error.message || "Failed to load items");
    } finally {
      setItemsLoading(false);
    }
  }

  async function seedItem() {
    try {
      setItemsError("");

      const response = await fetch(`${API_BASE}/items/seed`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Seed request failed: ${response.status}`);
      }

      await loadItems();
    } catch (error) {
      setItemsError(error.message || "Failed to seed item");
    }
  }

  useEffect(() => {
    if (hasSQLite) {
      loadItems();
    }
  }, [hasSQLite]);

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

  const cardStyle = {
    border: "1px solid #d1d5db",
    borderRadius: "12px",
    padding: "1rem",
    background: "#ffffff",
    marginBottom: "1rem",
  };

  const compactButtonStyle = {
    padding: "0.75rem 1rem",
    borderRadius: "10px",
    border: "1px solid #cbd5e1",
    background: "#f8fafc",
    cursor: "pointer",
    fontWeight: 600,
  };

  const layoutStyle = {
    maxWidth: "900px",
    margin: "0 auto",
    padding: "1rem",
    fontFamily: "Arial, sans-serif",
  };

const itemCountLabel = useMemo(
  () => `${items.length} item${items.length === 1 ? "" : "s"}`,
  [items.length]
);



const isPipelineWorkbench =
  config?.app_name === "pipeline-workbench" ||
  Boolean(config?.features?.pipeline_workbench);

const isNotebookView =
  config?.app_name === "notebook-view" ||
  Boolean(config?.features?.published_view);

const hasWorkflow = Boolean(config?.workflow?.enabled);
const hasVoila = Boolean(config?.voila?.enabled);

const isDeviceOpsConsole =
  config?.app_name === "device-ops-console" ||
  Boolean(config?.features?.device_ops_console);

const hasDeviceBridge = Boolean(config?.device?.enabled);

  return (
    <div style={layoutStyle}>
      <h1>
        {isDeviceOpsConsole
          ? "Device Ops Console"
          : isTechnicianConsole
          ? "Technician Console"
          : isPipelineWorkbench
          ? "Pipeline Workbench"
          : isDataWorkbench
          ? "Data Workbench"
          : isNotebookView
          ? "Notebook View Bridge"
          : "ForgeStack Generated App"}
      </h1>

      <section style={{ ...cardStyle }}>
        <h2 style={{ marginTop: 0 }}>Configuration</h2>

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
                <ul style={{ paddingLeft: "1.25rem" }}>
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

      {hasSQLite && (
        <>
          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>{isTechnicianConsole ? "Queue Summary" : "Items"}</h2>
            <p><strong>Total:</strong> {itemCountLabel}</p>
            <p><strong>Database:</strong> {config?.sqlite?.database || "app.db"}</p>
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Quick Actions</h2>
            <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
              <button style={compactButtonStyle} onClick={loadItems}>Refresh Items</button>
              <button style={compactButtonStyle} onClick={seedItem}>Seed Sample Item</button>
            </div>
            {itemsError && <p style={{ marginTop: "1rem" }}>{itemsError}</p>}
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>{isTechnicianConsole ? "Work Items" : "Items List"}</h2>

            {itemsLoading && <p>Loading items...</p>}

            {!itemsLoading && items.length === 0 && (
              <p>No items available yet.</p>
            )}

            {!itemsLoading && items.length > 0 && (
              <div>
                {items.map((item) => (
                  <div
                    key={item.id}
                    style={{
                      border: "1px solid #e5e7eb",
                      borderRadius: "10px",
                      padding: "0.85rem",
                      marginBottom: "0.75rem",
                      background: "#f8fafc",
                    }}
                  >
                    <p style={{ margin: "0 0 0.35rem 0" }}>
                      <strong>ID:</strong> {item.id}
                    </p>
                    <p style={{ margin: 0 }}>
                      <strong>Name:</strong> {item.name}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </section>
        </>
      )}

      {hasWorkflow && (
        <>
          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Workflow Overview</h2>
            <p><strong>Engine:</strong> {config?.workflow?.engine}</p>
            <p><strong>Pipeline Root:</strong> {config?.workflow?.pipeline_root}</p>
            <p><strong>Config Root:</strong> {config?.workflow?.config_root}</p>
            <p><strong>Data Root:</strong> {config?.workflow?.data_root}</p>
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Pipeline Assets</h2>
            <p><strong>Starter Pipeline:</strong> {config?.workflow?.sample_pipeline}</p>
            <p>Structured workflow scaffolding is available for pipeline-oriented development.</p>
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Pipeline Stages</h2>
            <ul style={{ paddingLeft: "1.25rem", marginBottom: 0 }}>
              {(config?.workflow?.stages || []).map((stage) => (
                <li key={stage}>{stage}</li>
              ))}
            </ul>
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Data Staging</h2>
            <p>Use the generated data and configuration folders as the starting point for local pipeline workflows.</p>
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Future Pipeline Actions</h2>
            <p>Later milestones may add local execution helpers, richer pipeline templates, and workflow launch actions.</p>
          </section>
        </>
      )}

      {hasDeviceBridge && (
        <>
          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Device Bridge</h2>
            <p><strong>Bridge:</strong> {config?.device?.bridge}</p>
            <p><strong>Connection:</strong> {config?.device?.connection}</p>
            <p><strong>Sketch:</strong> {config?.device?.sketch}</p>
          </section>

          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Technician Actions</h2>
            <p>Use this console as a starting point for local device checks, serial workflows, and technician-side bridge operations.</p>
          </section>
        </>
      )}

      {hasJupyter && (
        <section style={{ ...cardStyle }}>
          <h2 style={{ marginTop: 0 }}>Notebook Workspace</h2>
          <p><strong>Status:</strong> Available</p>
          <p><strong>Port:</strong> {config?.jupyter?.port}</p>
          <p>
            <a
              href={`http://localhost:${config?.jupyter?.port || 8888}`}
              target="_blank"
              rel="noreferrer"
            >
              Open Jupyter Workspace
            </a>
          </p>
        </section>
      )}

      {hasVoila && (
          <section style={{ ...cardStyle }}>
            <h2 style={{ marginTop: 0 }}>Notebook View Bridge</h2>
            <p><strong>Status:</strong> Available</p>
            <p><strong>Port:</strong> {config?.voila?.port}</p>
            <p>
              <a
                href={`http://localhost:${config?.voila?.port || 8866}`}
                target="_blank"
                rel="noreferrer"
              >
                Open Voilà View
              </a>
            </p>
          </section>
        )}

      {config?.features?.auth && (
        <section style={{ ...cardStyle }}>
          <h2 style={{ marginTop: 0 }}>Async Task Demo</h2>
          <button style={compactButtonStyle} onClick={runPingTask}>Run Ping Task</button>

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
      )}
    </div>
  );
}
{% endraw %}