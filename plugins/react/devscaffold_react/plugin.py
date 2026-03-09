from devscaffold.core.plugin_api import Plugin, PluginMetadata


class ReactPlugin(Plugin):
    metadata = PluginMetadata(
        name="react",
        version="1.0.0",
        requires=[],
        provides=["frontend"],
        description="Generate a Vite React frontend",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        port = ctx.options.get("port", 5173)
        ctx.create_dir("frontend/src", "Create frontend source directory")
        ctx.create_file(
            "frontend/package.json",
            "{\n  \"name\": \"frontend\",\n  \"private\": true,\n  \"version\": \"0.1.0\",\n  \"type\": \"module\",\n  \"scripts\": {\n    \"dev\": \"vite\",\n    \"build\": \"vite build\",\n    \"preview\": \"vite preview\"\n  },\n  \"dependencies\": {\n    \"react\": \"^18.3.1\",\n    \"react-dom\": \"^18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@vitejs/plugin-react\": \"^4.3.1\",\n    \"vite\": \"^5.4.2\"\n  }\n}\n",
            "Create frontend package manifest",
        )
        ctx.create_file("frontend/index.html", "<!doctype html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"UTF-8\" />\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n    <title>ForgeStack App</title>\n  </head>\n  <body>\n    <div id=\"root\"></div>\n    <script type=\"module\" src=\"/src/main.jsx\"></script>\n  </body>\n</html>\n", "Create frontend HTML entrypoint")
        ctx.create_file("frontend/src/main.jsx", "import React from \"react\";\nimport ReactDOM from \"react-dom/client\";\nimport \"./styles.css\";\n\nfunction App() {\n  return (\n    <main>\n      <h1>ForgeStack</h1>\n      <p>Your React frontend is ready.</p>\n    </main>\n  );\n}\n\nReactDOM.createRoot(document.getElementById(\"root\")).render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>\n);\n", "Create frontend application entrypoint")
        ctx.create_file("frontend/src/styles.css", "body {\n  font-family: Inter, Arial, sans-serif;\n  margin: 0;\n  padding: 2rem;\n}\n", "Create frontend stylesheet")
        ctx.create_file("frontend/vite.config.js", f"import {{ defineConfig }} from \"vite\";\nimport react from \"@vitejs/plugin-react\";\n\nexport default defineConfig({{\n  plugins: [react()],\n  server: {{\n    host: \"0.0.0.0\",\n    port: {port}\n  }}\n}});\n", "Create Vite config")
        ctx.add_service("frontend", {"image": "node:20", "working_dir": "/app", "volumes": ["./frontend:/app"], "ports": [f"{port}:{port}"], "command": ["sh", "-lc", "npm install && npm run dev -- --host 0.0.0.0"]}, "Add frontend service")


def plugin():
    return ReactPlugin()
