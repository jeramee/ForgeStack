from __future__ import annotations

TOOL_BOUNDARIES = {
    "devmake": {
        "active": True,
        "maturity": "active",
        "repo_status": "implemented-in-main-forgestack-repo",
        "role": "active project generation CLI for ForgeStack",
        "owns": [
            "project creation",
            "preset resolution",
            "planning",
            "graphing",
            "apply/generation",
            "plugin discovery",
            "output rendering",
            "stack/app/project/output orchestration",
        ],
        "does_not_own": [
            "standalone data-workbench product lane",
            "standalone operational view/publishing product lane",
        ],
    },
    
    # Minimal placeholders for reserved future lanes
    "devdata": {"active": False, "maturity": "reserved"},
    "devview": {"active": False, "maturity": "reserved"},

    "devdata": {
        "active": False,
        "maturity": "reserved",
        "repo_status": "defined-but-not-split",
        "role": "future data/workflow/workbench lane under ForgeStack",
        "owns": [
            "local workflow state",
            "sqlite-backed operational persistence",
            "notebook workspace",
            "data processing lane",
            "pipeline/workbench patterns",
            "ingestion/staging utilities",
            "structured workflow patterns",
            "semi-connected processing support",
        ],
        "does_not_own": [
            "core planner/executor",
            "generic preset resolution",
            "main project generation lifecycle",
            "all user-facing surfaces by default",
        ],
    },
    "devview": {
        "active": False,
        "maturity": "reserved",
        "repo_status": "defined-but-not-split",
        "role": "future operational surfaces and published views lane under ForgeStack",
        "owns": [
            "operator surfaces",
            "technician panels",
            "queue/status views",
            "dashboard/view publishing",
            "notebook-backed published views",
            "mobile-responsive operational web surfaces",
            "browser-facing workflow presentation",
        ],
        "does_not_own": [
            "core planner/executor",
            "generic preset resolution",
            "notebook authoring workflows",
            "processing/state semantics by default",
        ],
    },
}


def get_tool_boundary(tool_name: str) -> dict:
    return TOOL_BOUNDARIES[tool_name]


def is_active_tool(tool_name: str) -> bool:
    return bool(TOOL_BOUNDARIES[tool_name]["active"])


def list_reserved_tools() -> list[str]:
    return [
        name
        for name, meta in TOOL_BOUNDARIES.items()
        if not meta.get("active", False)
    ]