from devscaffold.core.plan import Plan, FileWrite


class MLWorkspacePlugin:

    name = "ml-workspace"
    requires = ["celery", "redis", "fastapi"]

    def plan(self, ctx):

        p = Plan()

        p.folders += [
            "ml",
            "ml/data",
            "ml/models",
            "ml/pipelines",
            "notebooks"
        ]

        p.files.append(
            FileWrite(
                "ml/pipelines/example_pipeline.py",
"""
from celery import shared_task

@shared_task
def train_model():
    print("Training model...")
"""
            )
        )

        p.files.append(
            FileWrite(
                "notebooks/README.md",
"""
# Jupyter Notebooks

Place experimentation notebooks here.
"""
            )
        )

        p.compose = {
            "services": {
                "jupyter": {
                    "image": "jupyter/scipy-notebook",
                    "ports": ["8888:8888"],
                    "volumes": [
                        "./notebooks:/home/jovyan/work",
                        "./ml:/home/jovyan/ml"
                    ]
                }
            }
        }

        return p

    def after_generate(self, ctx):

        ctx.append_file(
            "backend/requirements.txt",
            "scikit-learn\npandas\nnumpy\n"
        )


def plugin():
    return MLWorkspacePlugin()