export default function App() {
  const pageStyle = {
    fontFamily: "Arial, sans-serif",
    padding: "2rem",
  };

  return (
    <div style={pageStyle}>
      <h1>{{ project_name }}</h1>
      <p>ForgeStack generated frontend is ready.</p>

      <ul>
        {% if has_feature.charts %}
        <li>Charts enabled</li>
        {% endif %}
        {% if has_feature.filters %}
        <li>Filters enabled</li>
        {% endif %}
        {% if has_feature.reporting %}
        <li>Reporting enabled</li>
        {% endif %}
        {% if has_feature.auth %}
        <li>Authentication enabled</li>
        {% endif %}
        {% if has_feature.admin %}
        <li>Admin tools enabled</li>
        {% endif %}
      </ul>
    </div>
  );
}