import os
import subprocess
import sys
from ..templates.django_templates import DjangoTemplates

class DjangoGenerator:
    def __init__(self):
        self.templates = DjangoTemplates()

    def create_structure(self, project_dir, project_name):
        """Create Django project structure"""
        print("Creating Django backend structure...")
        backend_dir = os.path.join(project_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)

        # Create Django project
        project_snake_case = project_name.lower().replace('-', '_').replace(' ', '_')

        # Create Django project main directory
        django_project_dir = os.path.join(backend_dir, project_snake_case)
        os.makedirs(django_project_dir, exist_ok=True)

        # Create __init__.py
        with open(os.path.join(django_project_dir, "__init__.py"), "w") as f:
            f.write("")

        # Create settings.py
        with open(os.path.join(django_project_dir, "settings.py"), "w") as f:
            f.write(self.templates.get_settings_content(project_snake_case))

        # Create urls.py
        with open(os.path.join(django_project_dir, "urls.py"), "w") as f:
            f.write(self.templates.get_urls_content(project_snake_case))

        # Create wsgi.py
        with open(os.path.join(django_project_dir, "wsgi.py"), "w") as f:
            f.write(self.templates.get_wsgi_content(project_snake_case))

        # Create asgi.py
        with open(os.path.join(django_project_dir, "asgi.py"), "w") as f:
            f.write(self.templates.get_asgi_content(project_snake_case))

        # Create manage.py
        with open(os.path.join(backend_dir, "manage.py"), "w") as f:
            f.write(self.templates.get_manage_content(project_snake_case))
        try:
            os.chmod(os.path.join(backend_dir, "manage.py"), 0o755)
        except OSError:
            pass

        # Create requirements.txt
        with open(os.path.join(backend_dir, "requirements.txt"), "w") as f:
            f.write(self.templates.get_requirements_content())

        # Create api app
        self._create_api_app(backend_dir)

    def _create_api_app(self, backend_dir):
        """Create the default API app"""
        api_dir = os.path.join(backend_dir, "api")
        os.makedirs(api_dir, exist_ok=True)

        # Create api/__init__.py
        with open(os.path.join(api_dir, "__init__.py"), "w") as f:
            f.write("")

        # Create api/admin.py
        with open(os.path.join(api_dir, "admin.py"), "w") as f:
            f.write("from django.contrib import admin\n\n# Register your models here.\n")

        # Create api/apps.py
        with open(os.path.join(api_dir, "apps.py"), "w") as f:
            f.write("from django.apps import AppConfig\n\n\nclass ApiConfig(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = 'api'\n")

        # Create api/models.py
        with open(os.path.join(api_dir, "models.py"), "w") as f:
            f.write("from django.db import models\n\n# Create your models here.\n")

        # Create api/serializers.py
        with open(os.path.join(api_dir, "serializers.py"), "w") as f:
            f.write("from rest_framework import serializers\n\n# Define your serializers here\n")

        # Create api/views.py
        with open(os.path.join(api_dir, "views.py"), "w") as f:
            f.write(self.templates.get_api_views_content())

        # Create api/urls.py
        with open(os.path.join(api_dir, "urls.py"), "w") as f:
            f.write(self.templates.get_api_urls_content())

        # Create api/migrations folder
        migrations_dir = os.path.join(api_dir, "migrations")
        os.makedirs(migrations_dir, exist_ok=True)
        with open(os.path.join(migrations_dir, "__init__.py"), "w") as f:
            f.write("") 