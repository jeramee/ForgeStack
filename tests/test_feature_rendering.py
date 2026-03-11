from forgestack.core.template_loader import render_template_text


def test_react_package_template_includes_feature_dependencies():
    context = {
        "project_name": "MyApp",
        "has_feature": {
            "charts": True,
            "filters": True,
        },
    }

    rendered = render_template_text("react_package", context)

    assert '"name": "myapp-frontend"' in rendered
    assert '"recharts": "^2.12.0"' in rendered
    assert '"@tanstack/react-query": "^5.59.0"' in rendered


def test_react_package_template_omits_feature_dependencies_when_disabled():
    context = {
        "project_name": "MyApp",
        "has_feature": {
            "charts": False,
            "filters": False,
        },
    }

    rendered = render_template_text("react_package", context)

    assert '"name": "myapp-frontend"' in rendered
    assert '"recharts": "^2.12.0"' not in rendered
    assert '"@tanstack/react-query": "^5.59.0"' not in rendered