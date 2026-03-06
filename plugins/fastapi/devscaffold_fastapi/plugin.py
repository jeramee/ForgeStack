from devscaffold.core.plan import Plan, FileWrite


class FastAPIPlugin:

    name = "fastapi"

    def plan(self, ctx):
        p = Plan()

        p.folders.append("backend/app")

        p.files.append(
            FileWrite(
                "backend/app/main.py",
                """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello"}
"""
            )
        )

        p.files.append(
            FileWrite(
                "backend/requirements.txt",
                "fastapi\nuvicorn[standard]\n"
            )
        )

        p.files.append(
            FileWrite(
                "backend/Dockerfile",
                """
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
"""
            )
        )

        p.compose = {
            "services": {
                "backend": {
                    "build": "./backend",
                    "volumes": ["./backend:/app"],
                    "ports": ["8000:8000"]
                }
            }
        }

        return p


def plugin():
    return FastAPIPlugin()