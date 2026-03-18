from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_generated_device_bridge_vertical_slice(tmp_path):
    raw_doc = load_stack_yaml("projects/DeviceOpsConsoleApp.yaml")
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / "DeviceOpsConsoleApp"
    execute_plan(plan, output_root=output_root)

    app_config = (output_root / "backend" / "app_config.py").read_text(encoding="utf-8")
    compose = (output_root / "docker-compose.yml").read_text(encoding="utf-8")
    frontend_shell = (output_root / "frontend" / "src" / "generated" / "AppShell.jsx").read_text(encoding="utf-8")

    device_readme = (output_root / "device" / "README.md").read_text(encoding="utf-8")
    arduino_readme = (output_root / "device" / "arduino" / "README.md").read_text(encoding="utf-8")
    sketch = (output_root / "device" / "arduino" / "sketch.ino").read_text(encoding="utf-8")
    protocol_readme = (output_root / "device" / "protocol" / "README.md").read_text(encoding="utf-8")

    assert '"project_name": "DeviceOpsConsoleApp"' in app_config
    assert '"stack_name": "device-bridge-stack"' in app_config
    assert '"app_name": "device-ops-console"' in app_config

    assert '"device": {' in app_config
    assert '"enabled": True' in app_config
    assert '"bridge": "arduino"' in app_config
    assert '"connection": "serial"' in app_config
    assert '"sketch": "device/arduino/sketch.ino"' in app_config

    assert '"sqlite": {' in app_config
    assert '"database": "app.db"' in app_config

    assert "postgres:" not in compose
    assert "redis:" not in compose
    assert "celery:" not in compose
    assert "jupyter:" not in compose

    assert "Device Ops Console" in frontend_shell
    assert "Device Bridge" in frontend_shell
    assert "Technician Actions" in frontend_shell

    assert "# Device Bridge" in device_readme
    assert "# Arduino Bridge" in arduino_readme
    assert "Serial.begin(9600);" in sketch
    assert 'ForgeStack Arduino bridge scaffold ready' in sketch
    assert "# Device Protocol" in protocol_readme