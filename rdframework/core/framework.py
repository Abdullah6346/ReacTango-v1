import os
import subprocess
import sys
from pathlib import Path

class ReactDjangoFramework:
    def __init__(self):
        pass

    def create_project(self, name, template="default"):
        """Create a new project with the given name and template."""
        print(f"Creating new project: {name}")

        project_dir = os.path.abspath(name)
        os.makedirs(project_dir, exist_ok=True)

        # Create backend (Django) structure
        self._create_django_structure(project_dir, name)

        # Create frontend (React with TanStack Router) structure
        self._create_react_structure(project_dir, name)

        # Create README and other root files
        self._create_root_files(project_dir, name)

        # Initialize git
        try:
            subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
            print("Initialized empty Git repository.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: Could not initialize git repository. Error: {e}")

        print(f"\nProject '{name}' created successfully!")
        print(f"\nNext steps:")
        print(f"  1. cd {name}")
        print(f"  2. Create a virtual environment: python -m venv venv")
        print(f"  3. Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print(f"  4. Install backend dependencies: cd backend && pip install -r requirements.txt")
        print(f"  5. Install frontend dependencies: cd frontend && npm install")
        print(f"  6. Start backend: cd backend && python manage.py runserver")
        print(f"  7. Start frontend: cd frontend && npm run dev")

    def _create_django_structure(self, project_dir, project_name):
        """Create Django project structure"""
        from ..generators.django_generator import DjangoGenerator
        generator = DjangoGenerator()
        generator.create_structure(project_dir, project_name)

    def _create_react_structure(self, project_dir, project_name):
        """Create React project structure"""
        from ..generators.react_generator import ReactGenerator
        generator = ReactGenerator()
        generator.create_structure(project_dir, project_name)

    def _create_root_files(self, project_dir, project_name):
        """Create root files like README, .gitignore, etc."""
        from ..generators.root_generator import RootGenerator
        generator = RootGenerator()
        generator.create_files(project_dir, project_name)

    def generate_component(self, name, component_type="functional"):
        """Generate a new React component"""
        from ..generators.component_generator import ComponentGenerator
        generator = ComponentGenerator()
        generator.generate(name, component_type)

    def generate_app(self, name):
        """Generate a new Django app"""
        from ..generators.app_generator import AppGenerator
        generator = AppGenerator()
        generator.generate(name)

    def start_servers(self):
        """Start both frontend and backend servers concurrently"""
        from ..utils.server_manager import ServerManager
        manager = ServerManager()
        manager.start_servers()

    def _find_project_root(self, start_dir):
        """Find the project root directory by looking for frontend/ and backend/ subdirs."""
        from ..utils.path_finder import PathFinder
        finder = PathFinder()
        return finder.find_project_root(start_dir) 