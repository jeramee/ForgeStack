from devscaffold.core.plan import Plan


class PostgresPlugin:

    name = "postgres"

    def plan(self, ctx):

        p = Plan()

        p.compose = {
            "services": {
                "db": {
                    "image": "postgres:16",
                    "environment": {
                        "POSTGRES_DB": "appdb",
                        "POSTGRES_USER": "appuser",
                        "POSTGRES_PASSWORD": "devpass"
                    },
                    "ports": ["5432:5432"],
                    "volumes": ["pgdata:/var/lib/postgresql/data"]
                }
            },
            "volumes": {
                "pgdata": {}
            }
        }

        return p

def after_generate(self, ctx):

    ctx.append_file(
        "backend/.env",
        "DATABASE_URL=postgresql://appuser:devpass@db:5432/appdb\n"
    )
    

def plugin():
    return PostgresPlugin()