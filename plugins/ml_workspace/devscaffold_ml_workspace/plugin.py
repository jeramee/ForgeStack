from devscaffold.core.plugin_api import Plugin, PluginMetadata


class MLWorkspacePlugin(Plugin):
    metadata = PluginMetadata(
        name="ml-workspace",
        version="1.0.0",
        requires=["celery", "redis", "fastapi"],
        provides=["ml"],
        description="Add an ML workspace and Jupyter service",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        for folder in ["ml", "ml/data", "ml/models", "ml/pipelines", "notebooks"]:
            ctx.create_dir(folder, f"Create {folder}")
        ctx.create_file("ml/pipelines/example_pipeline.py", "from celery import shared_task\n\n@shared_task\ndef train_model():\n    print(\"Training model...\")\n", "Create example ML pipeline")
        ctx.create_file("notebooks/README.md", "# Jupyter Notebooks\n\nPlace experimentation notebooks here.\n", "Create notebooks README")
        ctx.add_service("jupyter", {"image": "jupyter/scipy-notebook", "ports": ["8888:8888"], "volumes": ["./notebooks:/home/jovyan/work", "./ml:/home/jovyan/ml"]}, "Add Jupyter service")
        ctx.append_file("backend/requirements.txt", "scikit-learn\npandas\nnumpy\n", "Append ML dependencies")


def plugin():
    return MLWorkspacePlugin()
