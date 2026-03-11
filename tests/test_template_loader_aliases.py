from forgestack.core.template_loader import render_template_text


def test_legacy_and_canonical_template_ids_render_same_output():
    context = {
        "project_name": "MyApp",
        "has_feature": {
            "charts": True,
            "filters": True,
        },
    }

    legacy = render_template_text("react_package", context)
    canonical = render_template_text("react/package.json", context)

    assert legacy == canonical