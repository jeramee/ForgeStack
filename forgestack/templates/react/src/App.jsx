import { useEffect, useMemo, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

function FeatureList({ features }) {
  if (!features.length) {
    return <p>No app features enabled.</p>;
  }

  return (
    <ul>
      {features.map((feature) => (
        <li key={feature}>{feature}</li>
      ))}
    </ul>
  );
}

export default function App() {
  const [health, setHealth] = useState(null);
  const [config, setConfig] = useState(null);
  const [taskResult, setTaskResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [taskLoading, setTaskLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadApplicationData() {
      try {
        setLoading(true);
        setError("");

        const [healthResponse, configResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/health`),
          fetch(`${API_BASE_URL}/config`),
        ]);

        if (!healthResponse.ok) {
          throw new Error(`Health request failed with ${healthResponse.status}`);
        }

        if (!configResponse.ok) {
          throw new Error(`Config request failed with ${configResponse.status}`);
        }

        const healthData = await healthResponse.json();
        const configData = await configResponse.json();

        setHealth(healthData);
        setConfig(configData);
      } catch (err) {
        setError(err.message || "Failed to load generated app data.");
      } finally {
        setLoading(false);
      }
    }

    loadApplicationData();
  }, []);

  async function queuePingTask() {
    try {
      setTaskLoading(true);
      setError("");

      const response = await fetch(`${API_BASE_URL}/tasks/ping`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Task request failed with ${response.status}`);
      }

      const data = await response.json();
      setTaskResult(data);
    } catch (err) {
      setError(err.message || "Failed to queue ping task.");
    } finally {
      setTaskLoading(false);
    }
  }

  const featureNames = useMemo(() => {
    if (!config?.features) {
      return [];
    }

    return Object.entries(config.features)
      .filter(([, enabled]) => Boolean(enabled))
      .map(([name]) => name);
  }, [config]);

  const title = config?.project_name || "{{ project_name }}";

  const pageStyle = {
    fontFamily: "Arial, sans-serif",
    padding: "2rem",
    maxWidth: "900px",
    margin: "0 auto",
  };

  const cardStyle = {
    border: "1px solid #d0d7de",
    borderRadius: "12px",
    padding: "1rem",
    marginBottom: "1rem",
  };

  const codeStyle = {
    backgroundColor: "#f6f8fa",
    padding: "0.75rem",
    borderRadius: "8px",
    overflowX: "auto",
  };

  return (
    <div style={pageStyle}>
      <h1>{title}</h1>
      <p>ForgeStack generated application skeleton.</p>

      {loading && <p>Loading backend health and config...</p>}
      {error && <p>Error: {error}</p>}

      <div style={cardStyle}>
        <h2>Backend Health</h2>
        {health ? (
          <pre style={codeStyle}>{JSON.stringify(health, null, 2)}</pre>
        ) : (
          !loading && <p>No health response loaded yet.</p>
        )}
      </div>

      <div style={cardStyle}>
        <h2>Generated Config</h2>
        {config ? (
          <>
            <p>
              <strong>Project:</strong> {config.project_name}
            </p>
            <p>
              <strong>Stack:</strong> {config.stack_name}
            </p>
            <p>
              <strong>App:</strong> {config.app_name}
            </p>
            <h3>Enabled Features</h3>
            <FeatureList features={featureNames} />
            <pre style={codeStyle}>{JSON.stringify(config, null, 2)}</pre>
          </>
        ) : (
          !loading && <p>No config loaded yet.</p>
        )}
      </div>

      <div style={cardStyle}>
        <h2>Celery Ping Task</h2>
        <button type="button" onClick={queuePingTask} disabled={taskLoading}>
          {taskLoading ? "Queueing..." : "Queue ping task"}
        </button>

        {taskResult && (
          <pre style={codeStyle}>{JSON.stringify(taskResult, null, 2)}</pre>
        )}
      </div>
    </div>
  );
}
