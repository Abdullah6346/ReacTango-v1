import os
from ..templates.react_templates import ReactTemplates

class ReactGenerator:
    def __init__(self):
        self.templates = ReactTemplates()

    def create_structure(self, project_dir, project_name):
        """Create React project structure based on the user-provided template"""
        print("Creating React frontend structure...")
        frontend_dir = os.path.join(project_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)

        # Root frontend files
        with open(os.path.join(frontend_dir, ".dockerignore"), "w") as f:
            f.write(self.templates.get_dockerignore_content())
        with open(os.path.join(frontend_dir, ".gitignore"), "w") as f:
            f.write(self.templates.get_gitignore_content())
        with open(os.path.join(frontend_dir, "Dockerfile"), "w") as f:
            f.write(self.templates.get_dockerfile_content())
        with open(os.path.join(frontend_dir, "README.md"), "w") as f:
            f.write(self.templates.get_readme_content())
        with open(os.path.join(frontend_dir, "package.json"), "w") as f:
            f.write(self.templates.get_package_json_content(project_name))
        with open(os.path.join(frontend_dir, "react-router.config.ts"), "w") as f:
            f.write(self.templates.get_router_config_content())
        with open(os.path.join(frontend_dir, "tsconfig.json"), "w") as f:
            f.write(self.templates.get_tsconfig_content())
        with open(os.path.join(frontend_dir, "vite.config.ts"), "w") as f:
            f.write(self.templates.get_vite_config_content())

        # Create app directory
        app_dir = os.path.join(frontend_dir, "app")
        os.makedirs(app_dir, exist_ok=True)

        # Create app files
        with open(os.path.join(app_dir, "root.tsx"), "w") as f:
            f.write(self.templates.get_root_tsx_content())
        with open(os.path.join(app_dir, "routes.ts"), "w") as f:
            f.write(self.templates.get_routes_ts_content())
        with open(os.path.join(app_dir, "app.css"), "w") as f:
            f.write(self.templates.get_app_css_content())
        with open(os.path.join(app_dir, "api.ts"), "w") as f:
            f.write(self.templates.get_api_ts_content())

        # Create routes directory
        routes_dir = os.path.join(app_dir, "routes")
        os.makedirs(routes_dir, exist_ok=True)
        with open(os.path.join(routes_dir, "home.tsx"), "w") as f:
            f.write(self.templates.get_home_route_tsx_content())

        # Create welcome directory and files
        welcome_dir = os.path.join(app_dir, "welcome")
        os.makedirs(welcome_dir, exist_ok=True)
        with open(os.path.join(welcome_dir, "welcome.tsx"), "w") as f:
            f.write(self.templates.get_welcome_tsx_content())
        with open(os.path.join(welcome_dir, "logo-light.svg"), "w") as f:
            f.write(self.templates.get_logo_light_svg_content())
        with open(os.path.join(welcome_dir, "logo-dark.svg"), "w") as f:
            f.write(self.templates.get_logo_dark_svg_content())

        # Create public directory
        public_dir = os.path.join(frontend_dir, "public")
        os.makedirs(public_dir, exist_ok=True)
        with open(os.path.join(public_dir, "vite.svg"), "w") as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100"><rect width="100" height="100" rx="15" fill="#747bff"></rect><path fill="#fff" d="M62.5 12.5h-25v12.5h12.5v50h12.5z"></path><path fill="#fff" d="M37.5 87.5h25v-12.5h-12.5v-50h-12.5z"></path></svg>') 