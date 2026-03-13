from forgestack.cli.main import _build_render_context


def test_build_render_context_exposes_features_and_has_feature():
    raw_doc = {
        "kind": "project",
        "name": "MyApp",
    }

    effective_doc = {
        "kind": "resolved-project",
        "name": "MyApp",
        "plugins": ["react", "python"],
        "project": {"name": "MyApp"},
        "stack": {"name": "web-stack"},
        "app": {
            "name": "finance-dashboard",
            "features": {
                "charts": True,
                "auth": True,
                "reporting": False,
                "filters": True,
            },
        },
        "values": {},
    }

    ctx = _build_render_context(raw_doc, effective_doc)

    assert ctx["features"] == {
        "charts": True,
        "auth": True,
        "reporting": False,
        "filters": True,
    }

    assert ctx["has_feature"]["charts"] is True
    assert ctx["has_feature"]["auth"] is True
    assert ctx["has_feature"]["reporting"] is False
    assert ctx["has_feature"]["filters"] is True

def test_build_render_context_exposes_pipeline_workbench_features():
    raw_doc = {
        "kind": "project",
        "name": "PipelineWorkbenchApp",
    }

    effective_doc = {
        "kind": "resolved-project",
        "name": "PipelineWorkbenchApp",
        "plugins": ["react", "fastapi", "sqlite", "jupyter", "kedro"],
        "project": {"name": "PipelineWorkbenchApp"},
        "stack": {"name": "structured-workflow-stack"},
        "app": {
            "name": "pipeline-workbench",
            "features": {
                "pipeline_workbench": True,
                "structured_workflow": True,
                "workbench": True,
                "notebooks": True,
                "local_analysis": True,
                "quick_actions": True,
            },
        },
        "values": {},
    }

    ctx = _build_render_context(raw_doc, effective_doc)

    assert ctx["has_feature"]["pipeline_workbench"] is True
    assert ctx["has_feature"]["structured_workflow"] is True
    assert ctx["has_feature"]["workbench"] is True
    assert ctx["has_feature"]["notebooks"] is True
    assert ctx["has_feature"]["local_analysis"] is True
    assert ctx["has_feature"]["quick_actions"] is True