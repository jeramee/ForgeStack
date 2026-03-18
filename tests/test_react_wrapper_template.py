from forgestack.core.plan_executor import render_template_text


def test_react_wrapper_template_imports_generated_shell():
    rendered = render_template_text("react/src/App.jsx", {})

    assert "import AppShell from './generated/AppShell'" in rendered
    assert "return <AppShell />" in rendered