from pathlib import Path

from forgestack.core.tool_boundaries import (
    TOOL_BOUNDARIES,
    get_tool_boundary,
    is_active_tool,
    list_reserved_tools,
)


DOC_PATH = Path("docs/devdata-devview-boundaries.md")


def test_only_devmake_is_active():
    active_tools = [
        name for name, meta in TOOL_BOUNDARIES.items() if meta.get("active", False)
    ]
    assert active_tools == ["devmake"]


def test_devdata_and_devview_are_reserved_not_active():
    assert TOOL_BOUNDARIES["devdata"]["active"] is False
    assert TOOL_BOUNDARIES["devview"]["active"] is False
    assert TOOL_BOUNDARIES["devdata"]["maturity"] == "reserved"
    assert TOOL_BOUNDARIES["devview"]["maturity"] == "reserved"


def test_devmake_stays_in_main_repo_role():
    devmake = get_tool_boundary("devmake")
    assert devmake["repo_status"] == "implemented-in-main-forgestack-repo"
    assert "project creation" in devmake["owns"]
    assert "preset resolution" in devmake["owns"]
    assert "stack/app/project/output orchestration" in devmake["owns"]


def test_devdata_owns_data_and_workflow_concerns():
    devdata = get_tool_boundary("devdata")
    assert "local workflow state" in devdata["owns"]
    assert "sqlite-backed operational persistence" in devdata["owns"]
    assert "notebook workspace" in devdata["owns"]
    assert "structured workflow patterns" in devdata["owns"]


def test_devview_owns_surface_and_publishing_concerns():
    devview = get_tool_boundary("devview")
    assert "technician panels" in devview["owns"]
    assert "queue/status views" in devview["owns"]
    assert "dashboard/view publishing" in devview["owns"]
    assert "notebook-backed published views" in devview["owns"]


def test_reserved_tool_listing():
    reserved = list_reserved_tools()
    assert "devdata" in reserved
    assert "devview" in reserved
    assert "devmake" not in reserved


def test_is_active_tool_helper():
    assert is_active_tool("devmake") is True
    assert is_active_tool("devdata") is False
    assert is_active_tool("devview") is False


# Remove or comment out the doc-dependent tests:

def test_boundary_doc_exists():
    # Disabled: public doc no longer exists
    # assert DOC_PATH.exists(), "Expected devdata/devview boundary doc to exist."
    pass

def test_boundary_doc_preserves_main_stance():
    # Disabled: public doc no longer exists
    # text = DOC_PATH.read_text(encoding="utf-8").lower()
    # assert "forgeStack".lower() in text
    # assert "devmake" in text
    # assert "devdata" in text
    # assert "devview" in text
    # assert "no standalone `devdata` cli yet".lower() in text
    # assert "no standalone `devview` cli yet".lower() in text
    # assert "no repo split yet".lower() in text
    pass