import os
import subprocess
from ..utils.path_finder import PathFinder
from ..templates.django_templates import DjangoTemplates

class AppGenerator:
    def __init__(self):
        self.path_finder = PathFinder()
        self.templates = DjangoTemplates()

    def generate_app(self, name):
        """Generate a new Django app"""
        # Find the backend directory
        backend_dir = self.path_finder.find_backend_dir(os.getcwd())
        if not backend_dir:
            print("Error: Could not find backend directory")
            return False

        # Create the app using Django's startapp command
        try:
            subprocess.run(
                ["python", "manage.py", "startapp", name],
                cwd=backend_dir,
                check=True
            )
        except subprocess.CalledProcessError:
            print(f"Error: Failed to create Django app '{name}'")
            return False

        # Create app structure
        app_dir = os.path.join(backend_dir, name)
        
        # Create serializers.py
        with open(os.path.join(app_dir, "serializers.py"), "w") as f:
            f.write(self.templates.get_serializers_content(name))

        # Create urls.py
        with open(os.path.join(app_dir, "urls.py"), "w") as f:
            f.write(self.templates.get_app_urls_content(name))

        # Update views.py
        with open(os.path.join(app_dir, "views.py"), "w") as f:
            f.write(self.templates.get_app_views_content(name))

        # Create migrations directory if it doesn't exist
        migrations_dir = os.path.join(app_dir, "migrations")
        os.makedirs(migrations_dir, exist_ok=True)
        with open(os.path.join(migrations_dir, "__init__.py"), "w") as f:
            f.write("")

        print(f"Generated Django app: {name}")
        return True 