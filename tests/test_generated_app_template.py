from forgestack.core.template_loader import render_template_text


def test_generated_react_app_template_targets_vertical_slice_endpoints():
    rendered = render_template_text(
        "react/src/App.jsx",
        {
            "project_name": "MyApp",
            "features": {"charts": True, "auth": False},
            "has_feature": {"charts": True, "auth": False},
        },
    )

    assert 'const API_BASE_URL = "http://localhost:8000";' in rendered
    assert 'fetch(`${API_BASE_URL}/health`)' in rendered
    assert 'fetch(`${API_BASE_URL}/config`)' in rendered
    assert 'fetch(`${API_BASE_URL}/tasks/ping`' in rendered
    assert 'ForgeStack generated application skeleton.' in rendered
    assert 'const title = config?.project_name || "MyApp";' in rendered


def test_generated_react_app_template_displays_project_stack_app_and_features():
    rendered = render_template_text(
        "react/src/App.jsx",
        {
            "project_name": "MyApp",
            "features": {"charts": True, "filters": True},
            "has_feature": {"charts": True, "filters": True},
        },
    )

    assert '<strong>Project:</strong> {config.project_name}' in rendered
    assert '<strong>Stack:</strong> {config.stack_name}' in rendered
    assert '<strong>App:</strong> {config.app_name}' in rendered
    assert '<h3>Enabled Features</h3>' in rendered
    assert 'Object.entries(config.features)' in rendered
    assert 'Queue ping task' in rendered
