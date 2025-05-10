import os
from ..templates.root_templates import RootTemplates

class RootGenerator:
    def __init__(self):
        self.templates = RootTemplates()

    def create_root_files(self, project_dir, project_name):
        """Create root-level project files"""
        # Create README.md
        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(self.templates.get_readme_content(project_name))

        # Create .gitignore
        with open(os.path.join(project_dir, ".gitignore"), "w") as f:
            f.write(self.templates.get_gitignore_content())

        # Create docker-compose.yml
        with open(os.path.join(project_dir, "docker-compose.yml"), "w") as f:
            f.write(self.templates.get_docker_compose_content(project_name))

        # Create .env
        with open(os.path.join(project_dir, ".env"), "w") as f:
            f.write(self.templates.get_env_content())

        # Create .env.example
        with open(os.path.join(project_dir, ".env.example"), "w") as f:
            f.write(self.templates.get_env_example_content())

        print("Created root project files") 