from forgestack.core.template_loader import render_template_text


def test_generated_react_app_template_targets_vertical_slice_endpoints():
    rendered = render_template_text(
        "react/src/generated/AppShell.jsx",
        {
            "project_name": "MyApp",
            "features": {"charts": True, "auth": False},
            "has_feature": {"charts": True, "auth": False},
        },
    )

    assert 'const API_BASE = "http://localhost:8000";' in rendered
    assert "/config" in rendered
    assert "/tasks/ping" in rendered
    assert "/tasks/${taskId}" in rendered
    assert "setInterval" in rendered
    assert "setTaskState" in rendered
    assert "setTaskResult" in rendered


def test_generated_react_app_template_displays_project_stack_app_and_features():
    rendered = render_template_text(
        "react/src/generated/AppShell.jsx",
        {
            "project_name": "MyApp",
            "features": {"charts": True, "filters": True},
            "has_feature": {"charts": True, "filters": True},
        },
    )

    assert '<strong>Project:</strong> {config.project_name}' in rendered
    assert '<strong>Stack:</strong> {config.stack_name}' in rendered
    assert '<strong>App:</strong> {config.app_name}' in rendered
    assert '<strong>Features:</strong>' in rendered
    assert "featureEntries.map" in rendered
