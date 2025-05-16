import argparse
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

        # --- THIS IS THE MISSING PART ---
        # Create backend (Django) structure
        self._create_django_structure(project_dir, name)
        # ---------------------------------

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
        print(f"  5. Install frontend dependencies: cd frontend && npm install") # or pnpm install / yarn install
        print(f"  6. Start backend: cd backend && python manage.py runserver")
        print(f"  7. Start frontend: cd frontend && npm run dev") # or pnpm dev / yarn dev

    def _create_django_structure(self, project_dir, project_name):
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
            f.write(self._get_django_settings_content(project_snake_case))

        # Create urls.py
        with open(os.path.join(django_project_dir, "urls.py"), "w") as f:
            f.write(self._get_django_urls_content(project_snake_case)) # Pass name needed? Check method

        # Create wsgi.py
        with open(os.path.join(django_project_dir, "wsgi.py"), "w") as f:
            f.write(self._get_django_wsgi_content(project_snake_case))

        # Create asgi.py
        with open(os.path.join(django_project_dir, "asgi.py"), "w") as f:
            f.write(self._get_django_asgi_content(project_snake_case))

        # Create manage.py
        with open(os.path.join(backend_dir, "manage.py"), "w") as f:
            f.write(self._get_django_manage_content(project_snake_case))
        # Make manage.py executable (optional, good practice on Linux/Mac)
        try:
            os.chmod(os.path.join(backend_dir, "manage.py"), 0o755)
        except OSError:
            pass # Ignore if chmod fails (e.g., Windows)

        # Create requirements.txt
        with open(os.path.join(backend_dir, "requirements.txt"), "w") as f:
            f.write(self._get_requirements_content())

        # Create api app
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
            f.write("from rest_framework import serializers\n\n# Define your serializers here\n") # Added placeholder comment

        # Create api/views.py
        with open(os.path.join(api_dir, "views.py"), "w") as f:
            f.write(self._get_api_views_content()) # Use helper for content

        # Create api/urls.py
        with open(os.path.join(api_dir, "urls.py"), "w") as f:
            f.write(self._get_api_urls_content()) # Use helper for content

        # Create api/migrations folder
        migrations_dir = os.path.join(api_dir, "migrations")
        os.makedirs(migrations_dir, exist_ok=True)
        with open(os.path.join(migrations_dir, "__init__.py"), "w") as f:
            f.write("")

    # =============================================
    # === React Frontend Structure Creation ===
    # =============================================
    def _create_react_structure(self, project_dir, project_name):
        """Create React project structure based on the user-provided template"""
        print("Creating React frontend structure (user template)...")
        frontend_dir = os.path.join(project_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)

        # Root frontend files, based on user's provided structure
        with open(os.path.join(frontend_dir, ".dockerignore"), "w") as f:
            f.write(self._get_frontend_dockerignore_content()) # New placeholder
        with open(os.path.join(frontend_dir, ".gitignore"), "w") as f: # Frontend specific .gitignore
            f.write(self._get_frontend_gitignore_content()) # User needs to update content of this method
        with open(os.path.join(frontend_dir, "Dockerfile"), "w") as f: # Frontend specific Dockerfile
            f.write(self._get_frontend_dockerfile_content()) # New placeholder
        with open(os.path.join(frontend_dir, "README.md"), "w", encoding="utf-8") as f: # Frontend specific README
            f.write(self._get_frontend_readme_md_content()) # New placeholder
        with open(os.path.join(frontend_dir, "package.json"), "w") as f:
            f.write(self._get_package_json_content(project_name)) # User needs to update content of this method
        # pnpm-lock.yaml is auto-generated, so we don't create it here.
        # with open(os.path.join(frontend_dir, "pnpm-lock.yaml"), "w") as f:
        with open(os.path.join(frontend_dir, "react-router.config.ts"), "w") as f:
            f.write(self._get_react_router_config_ts_content()) # New placeholder
        with open(os.path.join(frontend_dir, "tsconfig.json"), "w") as f:
            f.write(self._get_tsconfig_content()) # User needs to update content of this method
        with open(os.path.join(frontend_dir, "vite.config.ts"), "w") as f:
            f.write(self._get_vite_config_content()) # User needs to update content of this method

        # Create app directory (replaces src)
        app_dir = os.path.join(frontend_dir, "app")
        os.makedirs(app_dir, exist_ok=True)
        # User needs to confirm the internal structure of 'app/' based on their template.
        # The following is a sensible default structure, adapted from src/ to app/.



        with open(os.path.join(app_dir, "root.tsx"), "w") as f:
            f.write(self._get_root_tsx_content())

        with open(os.path.join(app_dir, "routes.ts"), "w") as f:
            f.write(self._get_routes_ts_content())

        # Create App.css (Used by root route, now in app/)
        with open(os.path.join(app_dir, "app.css"), "w") as f:
            f.write(self._get_app_css_content())


        # Create routes directory for TanStack Router (now in app/routes)
        # User to confirm if this file-based routing is still used with react-router.config.ts
        routes_dir = os.path.join(app_dir, "routes")
        os.makedirs(routes_dir, exist_ok=True)
   
     
        with open(os.path.join(routes_dir, "home.tsx"), "w") as f:
            f.write(self._get_home_route_tsx_content())

        # Create welcome directory and welcome.tsx (now in app/welcome)
        welcome_dir = os.path.join(app_dir, "welcome")
        os.makedirs(welcome_dir, exist_ok=True)
        with open(os.path.join(welcome_dir, "welcome.tsx"), "w") as f:
            f.write(self._get_welcome_tsx_content())
            
        # Create logo SVG files
        with open(os.path.join(welcome_dir, "logo-light.svg"), "w") as f:
            f.write(self._get_logo_light_svg_content())
            
        with open(os.path.join(welcome_dir, "logo-dark.svg"), "w") as f:
            f.write(self._get_logo_dark_svg_content())

        # Create api.ts (now in app/)
        with open(os.path.join(app_dir, "api.ts"), "w") as f:
            f.write(self._get_api_ts_content())

        # Create public directory (sibling to app/)
        public_dir = os.path.join(frontend_dir, "public")
        os.makedirs(public_dir, exist_ok=True)
        # User to confirm contents of public/. For now, adding vite.svg as an example.
        with open(os.path.join(public_dir, "vite.svg"), "w") as f:
             f.write('<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100"><rect width="100" height="100" rx="15" fill="#747bff"></rect><path fill="#fff" d="M62.5 12.5h-25v12.5h12.5v50h12.5z"></path><path fill="#fff" d="M37.5 87.5h25v-12.5h-12.5v-50h-12.5z"></path></svg>') # Vite logo

      

    # =============================================
    # === Root Project Files Creation ===
    # =============================================
    def _create_root_files(self, project_dir, project_name):
        """Create root files like README, .gitignore, etc."""
        print("Creating project configuration files...")

        # Create README.md
        with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(self._get_readme_content(project_name)) # Use the updated README

        # Create .gitignore (Root level)
        with open(os.path.join(project_dir, ".gitignore"), "w") as f:
            f.write(self._get_gitignore_content())

        # Create .env.example file (more common than .env)
        with open(os.path.join(project_dir, ".env.example"), "w") as f:
            f.write(self._get_env_content())
        print("Created .env.example - Copy this to .env and fill in your secrets.")

    # =============================================
    # === Generators (Component, App) ===
    # =============================================
    def generate_component(self, name, component_type="functional"):
        """Generate a new React component in frontend/src/components"""
        current_dir = os.getcwd()
        project_root = self._find_project_root(current_dir)

        if not project_root:
             print("Error: Could not find project root (missing frontend/ or backend/). Make sure you are inside the project.")
             return

        components_dir = os.path.join(project_root, "frontend", "src", "components")
        if not os.path.isdir(components_dir):
            print(f"Error: Components directory not found at {components_dir}")
            # Optionally offer to create it
            # os.makedirs(components_dir, exist_ok=True)
            # print(f"Created components directory: {components_dir}")
            return


        # Sanitize and format name (e.g., user-profile -> UserProfile)
        component_name = "".join(word.capitalize() for word in name.split('-'))

        component_path = os.path.join(components_dir, f"{component_name}.tsx")

        if os.path.exists(component_path):
            print(f"Error: Component {component_name} already exists at {component_path}")
            return

        if component_type == "functional":
            content = self._get_functional_component_content(component_name)
        else:
            content = self._get_class_component_content(component_name) # Keep class components if needed

        with open(component_path, "w") as f:
            f.write(content)

        print(f"Component {component_name} created at {component_path}")

    def generate_app(self, name):
        """Generate a new Django app in backend/"""
        current_dir = os.getcwd()
        project_root = self._find_project_root(current_dir)

        if not project_root:
             print("Error: Could not find project root (missing frontend/ or backend/). Make sure you are inside the project.")
             return

        backend_dir = os.path.join(project_root, "backend")
        if not os.path.isdir(backend_dir):
             print(f"Error: Backend directory not found at {backend_dir}")
             return

        # Basic validation for app name
        app_name_clean = name.lower().replace('-', '_').replace(' ', '_')
        if not app_name_clean.isidentifier():
             print(f"Error: '{name}' is not a valid Python identifier for a Django app name.")
             return

        app_dir = os.path.join(backend_dir, app_name_clean)

        if os.path.exists(app_dir):
            print(f"Error: App '{app_name_clean}' already exists at {app_dir}")
            return

        # Use django-admin startapp if available, otherwise create manually
        manage_py_path = os.path.join(backend_dir, "manage.py")
        python_executable = sys.executable # Use the python running the script

        if os.path.exists(manage_py_path) and python_executable:
            print(f"Attempting to create app '{app_name_clean}' using manage.py...")
            try:
                # Run manage.py startapp from the backend directory
                result = subprocess.run(
                    [python_executable, manage_py_path, "startapp", app_name_clean],
                    cwd=backend_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Django app '{app_name_clean}' created successfully using manage.py.")
                print(f"Don't forget to add '{app_name_clean}' to INSTALLED_APPS in your backend/*/settings.py")
                # Add serializers.py and urls.py manually as startapp doesn't create them
                with open(os.path.join(app_dir, "serializers.py"), "w") as f:
                     f.write("from rest_framework import serializers\n\n# Define your serializers here\n")
                with open(os.path.join(app_dir, "urls.py"), "w") as f:
                     f.write("from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    # Add your API URLs here\n]\n")
                return # Success
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"Warning: 'manage.py startapp' failed ({e}). Falling back to manual creation.")
                # Fall through to manual creation if startapp fails

        # Manual creation (fallback or if manage.py not found)
        print(f"Creating app '{app_name_clean}' manually...")
        os.makedirs(app_dir, exist_ok=True)
        # Create standard app files
        files_to_create = {
            "__init__.py": "",
            "admin.py": "from django.contrib import admin\n\n# Register your models here.\n",
            "apps.py": f"from django.apps import AppConfig\n\n\nclass {app_name_clean.capitalize()}Config(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = '{app_name_clean}'\n",
            "models.py": "from django.db import models\n\n# Create your models here.\n",
            "serializers.py": "from rest_framework import serializers\n\n# Define your serializers here\n", # Add serializers
            "tests.py": "from django.test import TestCase\n\n# Create your tests here.\n",
            "views.py": "from django.shortcuts import render\nfrom rest_framework import viewsets # Example import\n\n# Create your views here.\n",
             "urls.py": "from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    # Add your API URLs here\n]\n" # Add urls.py
        }
        for filename, content in files_to_create.items():
            with open(os.path.join(app_dir, filename), "w") as f:
                f.write(content)
        # Create migrations folder
        migrations_dir = os.path.join(app_dir, "migrations")
        os.makedirs(migrations_dir, exist_ok=True)
        with open(os.path.join(migrations_dir, "__init__.py"), "w") as f:
            f.write("")

        print(f"Django app '{app_name_clean}' created manually at {app_dir}")
        print(f"Don't forget to add '{app_name_clean}' to INSTALLED_APPS in your backend/*/settings.py")


    # =============================================
    # === Server Start ===
    # =============================================
    def start_servers(self):
        """Start both frontend and backend servers concurrently"""
        current_dir = os.getcwd()
        project_root = self._find_project_root(current_dir)

        if not project_root:
            print("Error: Could not find project root. Make sure you are in a React-Django project directory.")
            return

        backend_dir = os.path.join(project_root, "backend")
        frontend_dir = os.path.join(project_root, "frontend")

        if not os.path.isdir(backend_dir):
             print(f"Error: Backend directory not found at {backend_dir}")
             return
        if not os.path.isdir(frontend_dir):
             print(f"Error: Frontend directory not found at {frontend_dir}")
             return

        backend_process = None
        frontend_process = None

        try:
            print("Starting backend server (Django)...")
            # Ensure venv is activated or python is correctly pathed
            # This assumes 'python' resolves correctly, might need venv path
            backend_process = subprocess.Popen(
                [sys.executable, "manage.py", "runserver"],
                cwd=backend_dir
            )
            print(f"Backend PID: {backend_process.pid}")

            print("Starting frontend server (Vite)...")
            # Use npm, pnpm, or yarn - check lock file? For now, default to npm
            package_manager = "npm" # Or detect based on lock file
            frontend_process = subprocess.Popen(
                [package_manager, "run", "dev"],
                cwd=frontend_dir,
                # On Windows, shell=True might be needed for npm if not in PATH correctly
                shell=sys.platform == "win32"
            )
            print(f"Frontend PID: {frontend_process.pid}")

            print("\nServers started. Press Ctrl+C to stop.")
            # Wait for processes to complete (they won't unless interrupted)
            if backend_process: backend_process.wait()
            if frontend_process: frontend_process.wait()

        except KeyboardInterrupt:
            print("\nStopping servers...")
        except Exception as e:
            print(f"\nError starting servers: {e}")
        finally:
            if frontend_process and frontend_process.poll() is None:
                print("Terminating frontend process...")
                frontend_process.terminate()
                frontend_process.wait() # Wait for termination
            if backend_process and backend_process.poll() is None:
                print("Terminating backend process...")
                backend_process.terminate()
                backend_process.wait() # Wait for termination
            print("Servers stopped.")


    # =============================================
    # === Helper Methods (Find Dirs) ===
    # =============================================
    # --- Keep _find_project_root ---
    def _find_project_root(self, start_dir):
        """Find the project root directory by looking for frontend/ and backend/ subdirs."""
        current_dir = os.path.abspath(start_dir)
        while True:
            if os.path.exists(os.path.join(current_dir, "frontend")) and \
               os.path.exists(os.path.join(current_dir, "backend")):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # Reached root
                return None
            current_dir = parent_dir

    # --- (_find_components_dir and _find_backend_dir are not used directly by core logic anymore, but kept for reference/potential use) ---
    def _find_components_dir(self, start_dir):
        """Find the components directory (heuristic)."""
        project_root = self._find_project_root(start_dir)
        if (project_root):
            components_dir = os.path.join(project_root, "frontend", "app", "components") # MODIFIED src to app
            if os.path.isdir(components_dir):
                return components_dir
        # Fallback search (less reliable)
        for root, dirs, _ in os.walk(start_dir):
            if "components" in dirs:
                potential_dir = os.path.join(root, "components")
                # Check if it looks like a React app structure nearby (main.tsx in parent of components dir)
                if os.path.exists(os.path.join(os.path.dirname(potential_dir), "main.tsx")):
                     return potential_dir
        return None

    def _find_backend_dir(self, start_dir):
        """Find the backend directory (heuristic)."""
        project_root = self._find_project_root(start_dir)
        if project_root:
            backend_dir = os.path.join(project_root, "backend")
            if os.path.isdir(backend_dir) and os.path.exists(os.path.join(backend_dir, "manage.py")):
                return backend_dir
        # Fallback: check current dir
        if os.path.exists(os.path.join(start_dir, "manage.py")):
             # Check if it's inside a likely project root
             parent = os.path.dirname(start_dir)
             if os.path.exists(os.path.join(parent, "frontend")):
                 return start_dir
        return None


    # =============================================
    # === Template Content Methods (DJANGO) ===
    # =============================================
    def _get_django_settings_content(self, project_name_snake):
        # Basic Django settings, including CORS and DRF/SimpleJWT placeholders
        return rf'''"""
Django settings for {project_name_snake} project.
"""
import os
from pathlib import Path
from datetime import timedelta
import environ # Use django-environ for better env var handling

# Initialize environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '..', '.env')) # Read .env from project root

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable, fallback for local dev if not set
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-for-{project_name_snake}')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # Your apps
    'api', # Default API app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name_snake}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # No server-side templates needed typically for SPA
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{project_name_snake}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# Default to SQLite for easy setup, use env vars for PostgreSQL etc.
DATABASES = {{
    'default': env.db('DATABASE_URL', default=f'sqlite:///{{BASE_DIR / "db.sqlite3"}}') # Revert to original f-string
}}
DATABASES['default']['ATOMIC_REQUESTS'] = True # Recommended for DRF


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/
STATIC_URL = 'static/'
# Typically not serving static files from Django in production with SPA
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Add other authentication classes if needed, e.g., SessionAuthentication for browsable API
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Default to requiring authentication
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Optional: Default pagination, throttling, etc.
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}}

# Simple JWT settings
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {{
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60)), # e.g., 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env.int('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7)),    # e.g., 7 days
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # Use Django SECRET_KEY by default
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5), # Default, not typically used with access/refresh pair
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1), # Default
}}

# CORS settings
# https://github.com/adamchainz/django-cors-headers
# Use environment variables for production origins
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:5173', # Default Vite dev port
    'http://127.0.0.1:5173',
    'http://localhost:8000', # Allow backend origin for browsable API etc.
    'http://127.0.0.1:8000',
])
# Or allow all for local development (less secure)
# CORS_ALLOW_ALL_ORIGINS = DEBUG

# Optional: Allow credentials (cookies, authorization headers)
# CORS_ALLOW_CREDENTIALS = True

# Optional: Specify allowed methods and headers if needed
# CORS_ALLOW_METHODS = [...]
# CORS_ALLOW_HEADERS = [...]
'''

    def _get_django_urls_content(self, project_name_snake):
        # Root URL configuration for the Django project
        return rf'''"""
{project_name_snake} URL Configuration
"""
"""
temp URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Redirect root URL to the API
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')), # Include URLs from the 'api' app
    # Add other app URLs here: path('api/app2/', include('app2.urls')),

    # Auth endpoints provided by Simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Optional: Include DRF login/logout urls for browsable API
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

'''

    def _get_django_wsgi_content(self, project_name_snake):
        return rf'''"""
WSGI config for {project_name_snake} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name_snake}.settings')

application = get_wsgi_application()
'''

    def _get_django_asgi_content(self, project_name_snake):
         return rf'''"""
ASGI config for {project_name_snake} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name_snake}.settings')

application = get_asgi_application()
'''

    def _get_django_manage_content(self, project_name_snake):
        return rf'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name_snake}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''

    def _get_requirements_content(self):
        # Core Django + DRF + JWT + CORS + Env Vars + DB driver example
        return r'''Django>=4.2,<5.1 # Specify compatible range
djangorestframework>=3.14,<3.16
djangorestframework-simplejwt>=5.3,<5.5
django-cors-headers>=4.0,<4.5
django-environ>=0.11,<0.12 # For .env handling

# Choose your database driver:
psycopg2-binary>=2.9,<2.10 # For PostgreSQL (recommended for production)
# mysqlclient>=2.1,<2.3    # For MySQL/MariaDB
# Leave blank or comment out if using default SQLite

# Optional for production deployment:
gunicorn>=20.1,<22.0 # WSGI server
# uvicorn[standard]>=0.20,<0.25 # ASGI server (if using async features)

# Optional for development:
# ipython # Enhanced Python shell
'''

    def _get_api_views_content(self):
         # Basic DRF view for the API app
         return r"""from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def example_view(request):
    if request.method == 'GET':
        return Response({"message": "Hello from the API!"})
"""

    def _get_api_urls_content(self):
        # Basic URL configuration for the API app
        return r"""from django.urls import path
from . import views

urlpatterns = [
    # Add your API URLs here
    path('', views.example_view, name='example_view'),
]
"""

    # =============================================
    # === Template Content Methods (REACT) ===
    # =============================================
    def _get_package_json_content(self, project_name):
        # Basic package.json for a React project with TanStack Router
        # USER NEEDS TO PROVIDE CONTENT FOR THIS FROM THEIR TEMPLATE
        return rf'''{{
  "name": "{project_name}",
  "private": true,
  "type": "module",
  "scripts": {{
    "build": "react-router build",
    "dev": "react-router dev",
    "start": "react-router-serve ./build/server/index.js",
    "typecheck": "react-router typegen && tsc"
  }},
  "dependencies": {{
    "@react-router/node": "^7.5.3",
    "@react-router/serve": "^7.5.3",
    "isbot": "^5.1.27",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "react-router": "^7.5.3"
  }},
  "devDependencies": {{
    "@react-router/dev": "^7.5.3",
    "@tailwindcss/vite": "^4.1.4",
    "@types/node": "^20",
    "@types/react": "^19.1.2",
    "@types/react-dom": "^19.1.2",
    "tailwindcss": "^4.1.4",
    "typescript": "^5.8.3",
    "vite": "^6.3.3",
    "vite-tsconfig-paths": "^5.1.4"
  }}
}}
'''

    def _get_vite_config_content(self):
        # Basic Vite config for a React project with TanStack Router
        # USER NEEDS TO PROVIDE CONTENT FOR THIS FROM THEIR TEMPLATE
        return r'''import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tailwindcss(), reactRouter(), tsconfigPaths()],
});
'''

    def _get_tsconfig_content(self):
        # Basic tsconfig.json for a React project with TanStack Router
        # USER NEEDS TO PROVIDE CONTENT FOR THIS FROM THEIR TEMPLATE. This is a placeholder.
        return r'''{
  "include": [
    "**/*",
    "**/.server/**/*",
    "**/.client/**/*",
    ".react-router/types/**/*"
  ],
  "compilerOptions": {
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "types": ["node", "vite/client"],
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "rootDirs": [".", "./.react-router/types"],
    "baseUrl": ".",
    "paths": {
      "~/*": ["./app/*"]
    },
    "esModuleInterop": true,
    "verbatimModuleSyntax": true,
    "noEmit": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "strict": true
  }
}

'''

   


    def _get_app_css_content(self):
        # Basic layout and styling used in __root.tsx. Assumes this is app/App.css
        # User should replace with their template's content.
        return r'''@import "tailwindcss";

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif,
    "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}

html,
body {
  @apply bg-white dark:bg-gray-950;

  @media (prefers-color-scheme: dark) {
    color-scheme: dark;
  }
}
'''


    def _get_api_ts_content(self):
        # Axios instance with interceptors for JWT auth and refresh. Assumes this is app/api.ts
        # User should replace with their template's content or verify this one.
        return r'''import axios from 'axios';
// import {{ jwtDecode }} from 'jwt-decode'; // Use named import if needed

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({{
  baseURL: API_BASE_URL,
  headers: {{
    'Content-Type': 'application/json',
  }},
}});

// Example: Request interceptor (add if needed, e.g., for JWT)
/*
api.interceptors.request.use(
  (config) => {{
    const token = localStorage.getItem('accessToken');
    if (token) {{
      config.headers.Authorization = `Bearer ${{token}}`;
    }}
    return config;
  }},
  (error) => {{
    return Promise.reject(error);
  }}
);
*/

export default api;
'''

    def _get_frontend_gitignore_content(self):
        # User should update with their frontend/.gitignore content.
        return r'''# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons (https://nodejs.org/api/addons.html)
build/Release

# Dependency directories
node_modules/
jspm_packages/

# Snowpack dependency directory (https://snowpack.dev/)
web_modules/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.*.local
.env.local

# Parcel cache files
.cache
.parcel-cache

# Next.js build outputs
.next/
out/

# Nuxt.js build outputs
.nuxt/
dist/

# Remix build outputs
.cache/
build/
public/build/

# Docusaurus build outputs
.docusaurus/

# Gatsby build outputs
.cache/
public

# vuepress build outputs
.vuepress/dist

# Serverless directories
.serverless/

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS configuration file
.tern-project

# Vitest cache directory
.vitest_cache/

# Vite build output directory
dist
dist-ssr

# Sass cache folder
.sass-cache/

# Stylelint cache file
.stylelintcache

# Storybook build outputs
storybook-static

# TanStack Router generated file (re-generated on changes)
# User to verify if routeTree.gen.ts is still applicable with react-router.config.ts
app/routeTree.gen.ts # MODIFIED from src/ to app/

# VSCode specific settings/cache
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.history/

# JetBrains IDE specific settings/cache
.idea/

# macOS specific files
.DS_Store
'''





    def _get_readme_content(self, project_name):
        project_name_snake = project_name.lower().replace('-', '_').replace(' ', '_')
        return rf'''# {project_name}

A full-stack web application starter template built with React (TanStack Router, Vite, TypeScript) and Django (DRF, SimpleJWT).

## Project Structure

```
.
{{project_name}}/
├── backend/ # Django project
│ ├── api/ # Default Django REST Framework API app
│ │ ├── {project_name_snake}/ # Django project settings/config app
│ │ ├── venv/ # Python virtual environment (if created here)
│ │ ├── manage.py
│ │ └── requirements.txt
│ ├── frontend/ # React project (Vite + TanStack Router)
│ │ ├── app/  # Main application code (replaces src/)
│ │ │ ├── components/ # Reusable UI components
│ │ │ ├── routes/ # TanStack Router File-Based Routes (if still used)
│ │ │ │ ├── __root.tsx
│ │ │ │ ├── index.tsx
│ │ │ │ └── about.tsx
│ │ │ ├── api.ts # Configured Axios instance
│ │ │ ├── App.css # Styles for __root layout
│ │ │ ├── index.css # Global base styles
│ │ │ └── main.tsx # React entry point, Router setup
│ │ ├── public/ # Static assets
│ │ ├── .dockerignore # Frontend specific
│ │ ├── .gitignore # Frontend specific
│ │ ├── Dockerfile # Frontend specific
│ │ ├── README.md # Frontend-specific README
│ │ ├── package.json
│ │ ├── pnpm-lock.yaml
│ │ ├── react-router.config.ts
│ │ ├── tsconfig.json
│ │ ├── vite.config.ts
├── .env.example # Example environment variables (copy to .env)
├── .gitignore # Root gitignore
└── README.md # This file (Root README)
```
# ... existing code ...
# `VITE_API_URL`: Base URL for API calls from the *client* code (defaults to `/api` to use the proxy). Set to the full backend URL (e.g., `https://api.yourdomain.com`) if not using the proxy or in production builds.

## License

This project template is licensed under the MIT License.
''' # Ensure closing triple quotes are present and correctly placed

    def _get_gitignore_content(self):
        # Comprehensive root .gitignore covering Python/Django and Node/React
        return r'''# =========================================
# Python / Django
# =========================================

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
# Usually these files are created by pyinstaller, if you are using pyinstaller
# builds is most likely harmless to keep this in your gitignore
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal # SQLite journal file
media/ # Optional: Ignore media files if large/generated

# Environments
.env
.env.* # Allow specific .env files like .env.example if needed
!.env.example
.venv
venv/
env/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# =========================================
# Node / React / Vite
# =========================================

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons (https://nodejs.org/api/addons.html)
build/Release

# Dependency directories
node_modules/
jspm_packages/

# Snowpack dependency directory (https://snowpack.dev/)
web_modules/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.*.local
.env.local

# Parcel cache files
.cache
.parcel-cache

# Next.js build outputs
.next/
out/

# Nuxt.js build outputs
.nuxt/
dist/

# Remix build outputs
.cache/
build/
public/build/

# Docusaurus build outputs
.docusaurus/

# Gatsby build outputs
.cache/
public

# vuepress build outputs
.vuepress/dist

# Serverless directories
.serverless/

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS configuration file
.tern-project

# Vitest cache directory
.vitest_cache/

# Vite build output directory
dist
dist-ssr

# Sass cache folder
.sass-cache/

# Stylelint cache file
.stylelintcache

# Storybook build outputs
storybook-static

# TanStack Router generated file (re-generated on changes)
# User to verify if routeTree.gen.ts is still applicable with react-router.config.ts
app/routeTree.gen.ts # MODIFIED from src/ to app/

# VSCode specific settings/cache
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
.history/

# JetBrains IDE specific settings/cache
.idea/

# macOS specific files
.DS_Store
'''
  
    def _get_env_content(self):
        # Basic .env.example content
        return r'''# Django Backend Configuration
# -----------------------------
# SECURITY WARNING: Don't commit your actual .env file with secrets!
# Generate a strong, unique secret key for production.
# You can generate one using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=your_django_secret_key_here

# Set to True for development, False for production
DEBUG=True

# Allowed hosts for Django (comma-separated if multiple)
# For development, localhost and 127.0.0.1 are usually fine.
# For production, set this to your domain(s).
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database URL (Example for PostgreSQL, adjust as needed)
# Format: db_type://USER:PASSWORD@HOST:PORT/NAME
# For SQLite (default in settings.py if DATABASE_URL is not set):
# DATABASE_URL=sqlite:///./backend/db.sqlite3
DATABASE_URL=postgres://user:password@localhost:5432/mydatabase

# CORS Allowed Origins for Django (comma-separated)
# These are the frontend URLs that are allowed to make requests to the backend.
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT Token Lifetimes (in minutes/days as configured in settings.py)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7


# React Frontend Configuration
# ----------------------------
# Vite specific environment variables should be prefixed with VITE_
# Base URL for API calls from the client-side React app.
# If your Django backend is running on a different port or domain during development (without proxy),
# set this to the full backend URL (e.g., http://localhost:8000/api).
# If using Vite's proxy (common setup), /api should work.
VITE_API_URL=/api

# Other frontend-specific environment variables can go here
# VITE_SOME_OTHER_KEY=some_value
'''

    def _get_frontend_dockerfile_content(self):
        return r"""FROM node:20-alpine AS development-dependencies-env
COPY . /app
WORKDIR /app
RUN npm ci

FROM node:20-alpine AS production-dependencies-env
COPY ./package.json package-lock.json /app/
WORKDIR /app
RUN npm ci --omit=dev

FROM node:20-alpine AS build-env
COPY . /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
WORKDIR /app
RUN npm run build

FROM node:20-alpine
COPY ./package.json package-lock.json /app/
COPY --from=production-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
WORKDIR /app
CMD ["npm", "run", "start"]"""

    def _get_frontend_readme_md_content(self): # Differentiated from root readme
        return rf'''# Welcome to React Router!

A modern, production-ready template for building full-stack React applications using React Router.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/remix-run/react-router-templates/tree/main/default)

## Features

- 🚀 Server-side rendering
- ⚡️ Hot Module Replacement (HMR)
- 📦 Asset bundling and optimization
- 🔄 Data loading and mutations
- 🔒 TypeScript by default
- 🎉 TailwindCSS for styling
- 📖 [React Router docs](https://reactrouter.com/)

## Getting Started

### Installation

Install the dependencies:

```bash
npm install
```

### Development

Start the development server with HMR:

```bash
npm run dev
```

Your application will be available at `http://localhost:5173`.

## Building for Production

Create a production build:

```bash
npm run build
```

## Deployment

### Docker Deployment

To build and run using Docker:

```bash
docker build -t my-app .

# Run the container
docker run -p 3000:3000 my-app
```

The containerized application can be deployed to any platform that supports Docker, including:

- AWS ECS
- Google Cloud Run
- Azure Container Apps
- Digital Ocean App Platform
- Fly.io
- Railway

### DIY Deployment

If you're familiar with deploying Node applications, the built-in app server is production-ready.

Make sure to deploy the output of `npm run build`

```
├── package.json
├── package-lock.json (or pnpm-lock.yaml, or bun.lockb)
├── build/
│   ├── client/    # Static assets
│   └── server/    # Server-side code
```

## Styling

This template comes with [Tailwind CSS](https://tailwindcss.com/) already configured for a simple default starting experience. You can use whatever CSS framework you prefer.

---

Built with ❤️ using React Router.
'''

    def _get_frontend_dockerignore_content(self):
        return r""".react-router
build
node_modules
README.md"""

    def _get_react_router_config_ts_content(self):
        return r'''import type { Config } from "@react-router/dev/config";

export default {
  // Config options...
  // Server-side render by default, to enable SPA mode set this to `false`
  ssr: true,
} satisfies Config;
'''

    def _get_root_tsx_content(self):
        return r'''import {{
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "react-router";

import type { Route } from "./+types/root";
import "./app.css";

export const links: Route.LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}

export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) {
  let message = "Oops!";
  let details = "An unexpected error occurred.";
  let stack: string | undefined;

  if (isRouteErrorResponse(error)) {
    message = error.status === 404 ? "404" : "Error";
    details =
      error.status === 404
        ? "The requested page could not be found."
        : error.statusText || details;
  } else if (import.meta.env.DEV && error && error instanceof Error) {
    details = error.message;
    stack = error.stack;
  }

  return (
    <main className="pt-16 p-4 container mx-auto">
      <h1>{message}</h1>
      <p>{details}</p>
      {stack && (
        <pre className="w-full p-4 overflow-x-auto">
          <code>{stack}</code>
        </pre>
      )}
    </main>
  );
}
'''

    def _get_routes_ts_content(self):
        return r'''import { type RouteConfig, index } from "@react-router/dev/routes";

export default [index("routes/home.tsx")] satisfies RouteConfig;
'''

    def _get_home_route_tsx_content(self):
        return r'''import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <Welcome />;
}
'''

    def _get_welcome_tsx_content(self):
        return r'''import logoDark from "./logo-dark.svg";
import logoLight from "./logo-light.svg";

export function Welcome() {
  return (
    <main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        <header className="flex flex-col items-center gap-9">
          <div className="w-[500px] max-w-[100vw] p-4">
            <img
              src={logoLight}
              alt="React Router"
              className="block w-full dark:hidden"
            />
            <img
              src={logoDark}
              alt="React Router"
              className="hidden w-full dark:block"
            />
          </div>
        </header>
        <div className="max-w-[300px] w-full space-y-6 px-4">
          <nav className="rounded-3xl border border-gray-200 p-6 dark:border-gray-700 space-y-4">
            <p className="leading-6 text-gray-700 dark:text-gray-200 text-center">
              What\'s next?
            </p>
            <ul>
              {resources.map(({ href, text, icon }) => (
                <li key={href}>
                  <a
                    className="group flex items-center gap-3 self-stretch p-3 leading-normal text-blue-700 hover:underline dark:text-blue-500"
                    href={href}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {icon}
                    {text}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </main>
  );
}

const resources = [
  {
    href: "https://reactrouter.com/docs",
    text: "React Router Docs",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        className="stroke-gray-600 group-hover:stroke-current dark:stroke-gray-300"
      >
        <path
          d="M9.99981 10.0751V9.99992M17.4688 17.4688C15.889 19.0485 11.2645 16.9853 7.13958 12.8604C3.01467 8.73546 0.951405 4.11091 2.53116 2.53116C4.11091 0.951405 8.73546 3.01467 12.8604 7.13958C16.9853 11.2645 19.0485 15.889 17.4688 17.4688ZM2.53132 17.4688C0.951566 15.8891 3.01483 11.2645 7.13974 7.13963C11.2647 3.01471 15.8892 0.951453 17.469 2.53121C19.0487 4.11096 16.9854 8.73551 12.8605 12.8604C8.73562 16.9853 4.11107 19.0486 2.53132 17.4688Z"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      </svg>
    ),
  },
  {
    href: "https://rmx.as/discord",
    text: "Join Discord",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="20"
        viewBox="0 0 24 20"
        fill="none"
        className="stroke-gray-600 group-hover:stroke-current dark:stroke-gray-300"
      >
        <path
          d="M15.0686 1.25995L14.5477 1.17423L14.2913 1.63578C14.1754 1.84439 14.0545 2.08275 13.9422 2.31963C12.6461 2.16488 11.3406 2.16505 10.0445 2.32014C9.92822 2.08178 9.80478 1.84975 9.67412 1.62413L9.41449 1.17584L8.90333 1.25995C7.33547 1.51794 5.80717 1.99419 4.37748 2.66939L4.19 2.75793L4.07461 2.93019C1.23864 7.16437 0.46302 11.3053 0.838165 15.3924L0.868838 15.7266L1.13844 15.9264C2.81818 17.1714 4.68053 18.1233 6.68582 18.719L7.18892 18.8684L7.50166 18.4469C7.96179 17.8268 8.36504 17.1824 8.709 16.4944L8.71099 16.4904C10.8645 17.0471 13.128 17.0485 15.2821 16.4947C15.6261 17.1826 16.0293 17.8269 16.4892 18.4469L16.805 18.8725L17.3116 18.717C19.3056 18.105 21.1876 17.1751 22.8559 15.9238L23.1224 15.724L23.1528 15.3923C23.5873 10.6524 22.3579 6.53306 19.8947 2.90714L19.7759 2.73227L19.5833 2.64518C18.1437 1.99439 16.6386 1.51826 15.0686 1.25995ZM16.6074 10.7755L16.6074 10.7756C16.5934 11.6409 16.0212 12.1444 15.4783 12.1444C14.9297 12.1444 14.3493 11.6173 14.3493 10.7877C14.3493 9.94885 14.9378 9.41192 15.4783 9.41192C16.0471 9.41192 16.6209 9.93851 16.6074 10.7755ZM8.49373 12.1444C7.94513 12.1444 7.36471 11.6173 7.36471 10.7877C7.36471 9.94885 7.95323 9.41192 8.49373 9.41192C9.06038 9.41192 9.63892 9.93712 9.6417 10.7815C9.62517 11.6239 9.05462 12.1444 8.49373 12.1444Z"
          strokeWidth="1.5"
        />
      </svg>
    ),
  },
];
'''

    def _get_logo_light_svg_content(self):
        # User should update with their logo-light.svg content
        return r'''<svg width="1080" height="174" viewBox="0 0 1080 174" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M231.527 86.9999C231.527 94.9642 228.297 102.173 223.067 107.387C217.837 112.606 210.614 115.835 202.634 115.835C194.654 115.835 187.43 119.059 182.206 124.278C176.977 129.498 173.741 136.707 173.741 144.671C173.741 152.635 170.51 159.844 165.281 165.058C160.051 170.277 152.828 173.507 144.847 173.507C136.867 173.507 129.644 170.277 124.42 165.058C119.19 159.844 115.954 152.635 115.954 144.671C115.954 136.707 119.19 129.498 124.42 124.278C129.644 119.059 136.867 115.835 144.847 115.835C152.828 115.835 160.051 112.606 165.281 107.387C170.51 102.173 173.741 94.9642 173.741 86.9999C173.741 71.0711 160.808 58.1643 144.847 58.1643C136.867 58.1643 129.644 54.9347 124.42 49.7155C119.19 44.502 115.954 37.2931 115.954 29.3287C115.954 21.3643 119.19 14.1555 124.42 8.93622C129.644 3.71698 136.867 0.493164 144.847 0.493164C160.808 0.493164 173.741 13.4 173.741 29.3287C173.741 37.2931 176.977 44.502 182.206 49.7155C187.43 54.9347 194.654 58.1643 202.634 58.1643C218.594 58.1643 231.527 71.0711 231.527 86.9999Z" fill="#F44250"/>
<path d="M115.954 86.9996C115.954 71.0742 103.018 58.1641 87.061 58.1641C71.1037 58.1641 58.1677 71.0742 58.1677 86.9996C58.1677 102.925 71.1037 115.835 87.061 115.835C103.018 115.835 115.954 102.925 115.954 86.9996Z" fill="#121212"/>
<path d="M58.1676 144.671C58.1676 128.745 45.2316 115.835 29.2743 115.835C13.317 115.835 0.381104 128.745 0.381104 144.671C0.381104 160.596 13.317 173.506 29.2743 173.506C45.2316 173.506 58.1676 160.596 58.1676 144.671Z" fill="#121212"/>
<path d="M289.313 144.671C289.313 128.745 276.378 115.835 260.42 115.835C244.463 115.835 231.527 128.745 231.527 144.671C231.527 160.596 244.463 173.506 260.42 173.506C276.378 173.506 289.313 160.596 289.313 144.671Z" fill="#121212"/>
<g clip-path="url(#clip0_171_1761)">
<path d="M562.482 173.247C524.388 173.247 498.363 147.49 498.363 110.468C498.363 73.4455 524.388 47.6885 562.482 47.6885C600.576 47.6885 626.869 73.7135 626.869 110.468C626.869 147.222 600.576 173.247 562.482 173.247ZM562.482 144.007C579.386 144.007 587.703 130.319 587.703 110.468C587.703 90.6168 579.386 76.9289 562.482 76.9289C545.579 76.9289 537.529 90.6168 537.529 110.468C537.529 130.319 545.311 144.007 562.482 144.007Z" fill="#121212"/>
<path d="M833.64 141.116C824.217 141.116 819.237 136.684 819.237 126.156V74.8983H851.928V47.7792H819.237V1.15527H791.75L786.1 26.1978C783.343 36.4805 780.82 42.822 773.897 46.0821C773.105 46.4506 771.129 46.9976 769.409 47.3884C768.014 47.701 766.596 47.8573 765.167 47.8573H752.338V47.9243H734.832C723.578 47.9243 714.445 57.0459 714.445 68.3111V111.552C714.445 130.599 707.199 142.668 692.719 142.668C678.238 142.668 672.868 133.279 672.868 116.375V47.9243H634.249V125.765C634.249 151.254 644.442 173.248 676.63 173.248C691.915 173.248 703.895 167.231 711.096 157.182C712.145 155.72 714.445 156.49 714.445 158.276V170.022H753.332V83.8412C753.332 78.8953 757.34 74.8871 762.286 74.8871H779.882V136.952C779.882 164.663 797.89 173.248 817.842 173.248C833.908 173.248 844.436 169.374 853.58 162.441V136.126C846.1 139.453 839.725 141.116 833.629 141.116H833.64Z" fill="#121212"/>
<path d="M981.561 130.865C975.387 157.962 954.197 173.258 923.07 173.258C885.243 173.258 858.415 150.18 858.415 112.354C858.415 74.5281 885.779 47.6992 922.266 47.6992C961.699 47.6992 982.365 74.796 982.365 107.263V113.884H896.509C894.555 135.711 909.382 144.017 924.409 144.017C937.829 144.017 946.136 138.915 950.434 127.918L981.561 130.865ZM945.075 94.9372C944.271 83.1361 936.757 75.8567 921.998 75.8567C906.434 75.8567 899.188 82.321 897.045 94.9372H945.064H945.075Z" fill="#121212"/>
<path d="M1076.24 85.7486C1070.06 82.2652 1064.17 80.9142 1055.85 80.9142C1039.75 80.9142 1029.02 90.0358 1029.02 110.691V170.02H990.393V47.9225H1029.02V64.3235C1029.02 65.4623 1030.54 65.8195 1031.05 64.8035C1036.68 53.5718 1047.91 44.707 1062.03 44.707C1069.27 44.707 1075.45 46.8507 1078.66 49.5414L1076.25 85.7597L1076.24 85.7486Z" fill="#121212"/>
<path d="M547.321 31.5345V23.9983H522.457V31.5345H515.378V2.23828H542.14C553.562 2.23828 554.366 2.95282 554.366 13.1239C554.366 17.4111 553.472 18.5611 551.329 19.6553L549.408 20.6378L551.318 21.6426C553.595 22.8372 554.366 23.2391 554.366 30.0273V31.5345H547.332H547.321ZM522.457 18.3601H547.321V7.88763H522.457V18.349V18.3601Z" fill="#121212"/>
<path d="M578.493 2.23828H610.826V7.90996H580.067V14.5083H610.011V19.2868H580.067V25.8963H610.837V31.501L578.504 31.5345C575.344 31.5345 572.787 28.9778 572.787 25.8293V7.95462C572.787 4.80617 575.344 2.24945 578.493 2.24945V2.23828Z" fill="#121212"/>
<path d="M655.562 31.5345L653.151 26.3429H633.747L631.335 31.5345H624.58L637.007 4.75034C637.71 3.22078 639.262 2.23828 640.937 2.23828H645.927C647.613 2.23828 649.154 3.22078 649.857 4.75034L662.284 31.5345H655.529H655.562ZM643.46 8.06627C642.712 8.06627 642.053 8.49053 641.729 9.17158L635.968 21.5756H650.94L645.19 9.17158C644.878 8.49053 644.208 8.06627 643.46 8.06627Z" fill="#121212"/>
<path d="M694.862 32.4153C676.05 32.4153 675.313 32.4153 675.313 16.8852C675.313 1.35505 676.05 1.36621 694.862 1.36621C711.721 1.36621 713.764 2.06959 714.244 10.5325H707.333V7.01556H682.168V26.766H707.333V23.2714H714.244C713.775 31.7119 711.721 32.4153 694.862 32.4153Z" fill="#121212"/>
<path d="M745.282 31.5345V7.02795H729.16V2.23828H768.148V7.02795H752.026V31.5345H745.282Z" fill="#121212"/>
<path d="M454.419 169.819C450.935 165.264 448.792 154.814 447.452 137.397C446.112 118.104 437.806 113.817 422.532 113.817H392.254V169.83H347.494V0.986328H432.715C476.391 0.986328 498.106 21.6187 498.106 54.5882C498.106 79.2399 482.833 95.3171 462.201 98.0078C479.618 101.491 489.8 111.405 491.676 130.966C494.087 156.154 494.891 163.656 500.518 169.819H454.419ZM424.676 78.704C443.969 78.704 453.615 73.8808 453.615 58.3395C453.615 44.6739 443.969 37.4392 424.676 37.4392H392.254V78.7152H424.676V78.704Z" fill="#121212"/>
</g>
<defs>
<clipPath id="clip0_171_1761">
<rect width="731.156" height="172.261" fill="white" transform="translate(347.494 0.986328)"/>
</clipPath>
</defs>
</svg>
'''

    def _get_logo_dark_svg_content(self):
        # User should update with their logo-dark.svg content
        return r'''<svg width="1080" height="174" viewBox="0 0 1080 174" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M231.527 86.9999C231.527 94.9642 228.297 102.173 223.067 107.387C217.837 112.606 210.614 115.835 202.634 115.835C194.654 115.835 187.43 119.059 182.206 124.278C176.977 129.498 173.741 136.707 173.741 144.671C173.741 152.635 170.51 159.844 165.281 165.058C160.051 170.277 152.828 173.507 144.847 173.507C136.867 173.507 129.644 170.277 124.42 165.058C119.19 159.844 115.954 152.635 115.954 144.671C115.954 136.707 119.19 129.498 124.42 124.278C129.644 119.059 136.867 115.835 144.847 115.835C152.828 115.835 160.051 112.606 165.281 107.387C170.51 102.173 173.741 94.9642 173.741 86.9999C173.741 71.0711 160.808 58.1643 144.847 58.1643C136.867 58.1643 129.644 54.9347 124.42 49.7155C119.19 44.502 115.954 37.2931 115.954 29.3287C115.954 21.3643 119.19 14.1555 124.42 8.93622C129.644 3.71698 136.867 0.493164 144.847 0.493164C160.808 0.493164 173.741 13.4 173.741 29.3287C173.741 37.2931 176.977 44.502 182.206 49.7155C187.43 54.9347 194.654 58.1643 202.634 58.1643C218.594 58.1643 231.527 71.0711 231.527 86.9999Z" fill="#F44250"/>
<path d="M115.954 86.9996C115.954 71.0742 103.018 58.1641 87.0608 58.1641C71.1035 58.1641 58.1676 71.0742 58.1676 86.9996C58.1676 102.925 71.1035 115.835 87.0608 115.835C103.018 115.835 115.954 102.925 115.954 86.9996Z" fill="#121212"/>
<path d="M58.1676 144.671C58.1676 128.745 45.2316 115.835 29.2743 115.835C13.317 115.835 0.381104 128.745 0.381104 144.671C0.381104 160.596 13.317 173.506 29.2743 173.506C45.2316 173.506 58.1676 160.596 58.1676 144.671Z" fill="#121212"/>
<path d="M289.313 144.671C289.313 128.745 276.378 115.835 260.42 115.835C244.463 115.835 231.527 128.745 231.527 144.671C231.527 160.596 244.463 173.506 260.42 173.506C276.378 173.506 289.313 160.596 289.313 144.671Z" fill="#121212"/>
<g clip-path="url(#clip0_171_1761)">
<path d="M562.482 173.247C524.388 173.247 498.363 147.49 498.363 110.468C498.363 73.4455 524.388 47.6885 562.482 47.6885C600.576 47.6885 626.869 73.7135 626.869 110.468C626.869 147.222 600.576 173.247 562.482 173.247ZM562.482 144.007C579.386 144.007 587.703 130.319 587.703 110.468C587.703 90.6168 579.386 76.9289 562.482 76.9289C545.579 76.9289 537.529 90.6168 537.529 110.468C537.529 130.319 545.311 144.007 562.482 144.007Z" fill="#121212"/>
<path d="M833.64 141.116C824.217 141.116 819.237 136.684 819.237 126.156V74.8983H851.928V47.7792H819.237V1.15527H791.75L786.1 26.1978C783.343 36.4805 780.82 42.822 773.897 46.0821C773.105 46.4506 771.129 46.9976 769.409 47.3884C768.014 47.701 766.596 47.8573 765.167 47.8573H752.338V47.9243H734.832C723.578 47.9243 714.445 57.0459 714.445 68.3111V111.552C714.445 130.599 707.199 142.668 692.719 142.668C678.238 142.668 672.868 133.279 672.868 116.375V47.9243H634.249V125.765C634.249 151.254 644.442 173.248 676.63 173.248C691.915 173.248 703.895 167.231 711.096 157.182C712.145 155.72 714.445 156.49 714.445 158.276V170.022H753.332V83.8412C753.332 78.8953 757.34 74.8871 762.286 74.8871H779.882V136.952C779.882 164.663 797.89 173.248 817.842 173.248C833.908 173.248 844.436 169.374 853.58 162.441V136.126C846.1 139.453 839.725 141.116 833.629 141.116H833.64Z" fill="#121212"/>
<path d="M981.561 130.865C975.387 157.962 954.197 173.258 923.07 173.258C885.243 173.258 858.415 150.18 858.415 112.354C858.415 74.5281 885.779 47.6992 922.266 47.6992C961.699 47.6992 982.365 74.796 982.365 107.263V113.884H896.509C894.555 135.711 909.382 144.017 924.409 144.017C937.829 144.017 946.136 138.915 950.434 127.918L981.561 130.865ZM945.075 94.9372C944.271 83.1361 936.757 75.8567 921.998 75.8567C906.434 75.8567 899.188 82.321 897.045 94.9372H945.064H945.075Z" fill="#121212"/>
<path d="M1076.24 85.7486C1070.06 82.2652 1064.17 80.9142 1055.85 80.9142C1039.75 80.9142 1029.02 90.0358 1029.02 110.691V170.02H990.393V47.9225H1029.02V64.3235C1029.02 65.4623 1030.54 65.8195 1031.05 64.8035C1036.68 53.5718 1047.91 44.707 1062.03 44.707C1069.27 44.707 1075.45 46.8507 1078.66 49.5414L1076.25 85.7597L1076.24 85.7486Z" fill="#121212"/>
<path d="M547.321 31.5345V23.9983H522.457V31.5345H515.378V2.23828H542.14C553.562 2.23828 554.366 2.95282 554.366 13.1239C554.366 17.4111 553.472 18.5611 551.329 19.6553L549.408 20.6378L551.318 21.6426C553.595 22.8372 554.366 23.2391 554.366 30.0273V31.5345H547.332H547.321ZM522.457 18.3601H547.321V7.88763H522.457V18.349V18.3601Z" fill="#121212"/>
<path d="M578.493 2.23828H610.826V7.90996H580.067V14.5083H610.011V19.2868H580.067V25.8963H610.837V31.501L578.504 31.5345C575.344 31.5345 572.787 28.9778 572.787 25.8293V7.95462C572.787 4.80617 575.344 2.24945 578.493 2.24945V2.23828Z" fill="#121212"/>
<path d="M655.562 31.5345L653.151 26.3429H633.747L631.335 31.5345H624.58L637.007 4.75034C637.71 3.22078 639.262 2.23828 640.937 2.23828H645.927C647.613 2.23828 649.154 3.22078 649.857 4.75034L662.284 31.5345H655.529H655.562ZM643.46 8.06627C642.712 8.06627 642.053 8.49053 641.729 9.17158L635.968 21.5756H650.94L645.19 9.17158C644.878 8.49053 644.208 8.06627 643.46 8.06627Z" fill="#121212"/>
<path d="M694.862 32.4153C676.05 32.4153 675.313 32.4153 675.313 16.8852C675.313 1.35505 676.05 1.36621 694.862 1.36621C711.721 1.36621 713.764 2.06959 714.244 10.5325H707.333V7.01556H682.168V26.766H707.333V23.2714H714.244C713.775 31.7119 711.721 32.4153 694.862 32.4153Z" fill="#121212"/>
<path d="M745.282 31.5345V7.02795H729.16V2.23828H768.148V7.02795H752.026V31.5345H745.282Z" fill="#121212"/>
<path d="M454.419 169.819C450.935 165.264 448.792 154.814 447.452 137.397C446.112 118.104 437.806 113.817 422.532 113.817H392.254V169.83H347.494V0.986328H432.715C476.391 0.986328 498.106 21.6187 498.106 54.5882C498.106 79.2399 482.833 95.3171 462.201 98.0078C479.618 101.491 489.8 111.405 491.676 130.966C494.087 156.154 494.891 163.656 500.518 169.819H454.419ZM424.676 78.704C443.969 78.704 453.615 73.8808 453.615 58.3395C453.615 44.6739 443.969 37.4392 424.676 37.4392H392.254V78.7152H424.676V78.704Z" fill="#121212"/>
</g>
<defs>
<clipPath id="clip0_171_1761">
<rect width="731.156" height="172.261" fill="white" transform="translate(347.494 0.986328)"/>
</clipPath>
</defs>
</svg>
'''

    def _get_env_content(self):
        # Basic .env.example content
        return r'''# Django Backend Configuration
# -----------------------------
# SECURITY WARNING: Don't commit your actual .env file with secrets!
# Generate a strong, unique secret key for production.
# You can generate one using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=your_django_secret_key_here

# Set to True for development, False for production
DEBUG=True

# Allowed hosts for Django (comma-separated if multiple)
# For development, localhost and 127.0.0.1 are usually fine.
# For production, set this to your domain(s).
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database URL (Example for PostgreSQL, adjust as needed)
# Format: db_type://USER:PASSWORD@HOST:PORT/NAME
# For SQLite (default in settings.py if DATABASE_URL is not set):
# DATABASE_URL=sqlite:///./backend/db.sqlite3
DATABASE_URL=postgres://user:password@localhost:5432/mydatabase

# CORS Allowed Origins for Django (comma-separated)
# These are the frontend URLs that are allowed to make requests to the backend.
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT Token Lifetimes (in minutes/days as configured in settings.py)
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7


# React Frontend Configuration
# ----------------------------
# Vite specific environment variables should be prefixed with VITE_
# Base URL for API calls from the client-side React app.
# If your Django backend is running on a different port or domain during development (without proxy),
# set this to the full backend URL (e.g., http://localhost:8000/api).
# If using Vite's proxy (common setup), /api should work.
VITE_API_URL=/api

# Other frontend-specific environment variables can go here
# VITE_SOME_OTHER_KEY=some_value
'''

    def _get_frontend_dockerfile_content(self):
        return r"""FROM node:20-alpine AS development-dependencies-env
COPY . /app
WORKDIR /app
RUN npm ci

FROM node:20-alpine AS production-dependencies-env
COPY ./package.json package-lock.json /app/
WORKDIR /app
RUN npm ci --omit=dev

FROM node:20-alpine AS build-env
COPY . /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
WORKDIR /app
RUN npm run build

FROM node:20-alpine
COPY ./package.json package-lock.json /app/
COPY --from=production-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
WORKDIR /app
CMD ["npm", "run", "start"]"""

    def _get_frontend_readme_md_content(self): # Differentiated from root readme
        return rf'''# Welcome to React Router!

A modern, production-ready template for building full-stack React applications using React Router.

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/remix-run/react-router-templates/tree/main/default)

## Features

- 🚀 Server-side rendering
- ⚡️ Hot Module Replacement (HMR)
- 📦 Asset bundling and optimization
- 🔄 Data loading and mutations
- 🔒 TypeScript by default
- 🎉 TailwindCSS for styling
- 📖 [React Router docs](https://reactrouter.com/)

## Getting Started

### Installation

Install the dependencies:

```bash
npm install
```

### Development

Start the development server with HMR:

```bash
npm run dev
```

Your application will be available at `http://localhost:5173`.

## Building for Production

Create a production build:

```bash
npm run build
```

## Deployment

### Docker Deployment

To build and run using Docker:

```bash
docker build -t my-app .

# Run the container
docker run -p 3000:3000 my-app
```

The containerized application can be deployed to any platform that supports Docker, including:

- AWS ECS
- Google Cloud Run
- Azure Container Apps
- Digital Ocean App Platform
- Fly.io
- Railway

### DIY Deployment

If you're familiar with deploying Node applications, the built-in app server is production-ready.

Make sure to deploy the output of `npm run build`

```
├── package.json
├── package-lock.json (or pnpm-lock.yaml, or bun.lockb)
├── build/
│   ├── client/    # Static assets
│   └── server/    # Server-side code
```

## Styling

This template comes with [Tailwind CSS](https://tailwindcss.com/) already configured for a simple default starting experience. You can use whatever CSS framework you prefer.

---

Built with ❤️ using React Router.
'''

    def _get_frontend_dockerignore_content(self):
        return r""".react-router
build
node_modules
README.md"""

    def _get_react_router_config_ts_content(self):
        return r'''import type { Config } from "@react-router/dev/config";

export default {
  // Config options...
  // Server-side render by default, to enable SPA mode set this to `false`
  ssr: true,
} satisfies Config;
'''

    def _get_root_tsx_content(self):
        return r'''import {
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "react-router";

import type { Route } from "./+types/root";
import "./app.css";

export const links: Route.LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}

export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) {
  let message = "Oops!";
  let details = "An unexpected error occurred.";
  let stack: string | undefined;

  if (isRouteErrorResponse(error)) {
    message = error.status === 404 ? "404" : "Error";
    details =
      error.status === 404
        ? "The requested page could not be found."
        : error.statusText || details;
  } else if (import.meta.env.DEV && error && error instanceof Error) {
    details = error.message;
    stack = error.stack;
  }

  return (
    <main className="pt-16 p-4 container mx-auto">
      <h1>{message}</h1>
      <p>{details}</p>
      {stack && (
        <pre className="w-full p-4 overflow-x-auto">
          <code>{stack}</code>
        </pre>
      )}
    </main>
  );
}
'''

    def _get_routes_ts_content(self):
        return r'''import { type RouteConfig, index } from "@react-router/dev/routes";

export default [index("routes/home.tsx")] satisfies RouteConfig;
'''

    def _get_home_route_tsx_content(self):
        return r'''import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <Welcome />;
}
'''

    def _get_welcome_tsx_content(self):
        return r'''import logoDark from "./logo-dark.svg";
import logoLight from "./logo-light.svg";

export function Welcome() {
  return (
    <main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        <header className="flex flex-col items-center gap-9">
          <div className="w-[500px] max-w-[100vw] p-4">
            <img
              src={logoLight}
              alt="React Router"
              className="block w-full dark:hidden"
            />
            <img
              src={logoDark}
              alt="React Router"
              className="hidden w-full dark:block"
            />
          </div>
        </header>
        <div className="max-w-[300px] w-full space-y-6 px-4">
          <nav className="rounded-3xl border border-gray-200 p-6 dark:border-gray-700 space-y-4">
            <p className="leading-6 text-gray-700 dark:text-gray-200 text-center">
              What\'s next?
            </p>
            <ul>
              {resources.map(({ href, text, icon }) => (
                <li key={href}>
                  <a
                    className="group flex items-center gap-3 self-stretch p-3 leading-normal text-blue-700 hover:underline dark:text-blue-500"
                    href={href}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {icon}
                    {text}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </main>
  );
}

const resources = [
  {
    href: "https://reactrouter.com/docs",
    text: "React Router Docs",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        className="stroke-gray-600 group-hover:stroke-current dark:stroke-gray-300"
      >
        <path
          d="M9.99981 10.0751V9.99992M17.4688 17.4688C15.889 19.0485 11.2645 16.9853 7.13958 12.8604C3.01467 8.73546 0.951405 4.11091 2.53116 2.53116C4.11091 0.951405 8.73546 3.01467 12.8604 7.13958C16.9853 11.2645 19.0485 15.889 17.4688 17.4688ZM2.53132 17.4688C0.951566 15.8891 3.01483 11.2645 7.13974 7.13963C11.2647 3.01471 15.8892 0.951453 17.469 2.53121C19.0487 4.11096 16.9854 8.73551 12.8605 12.8604C8.73562 16.9853 4.11107 19.0486 2.53132 17.4688Z"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      </svg>
    ),
  },
  {
    href: "https://rmx.as/discord",
    text: "Join Discord",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="20"
        viewBox="0 0 24 20"
        fill="none"
        className="stroke-gray-600 group-hover:stroke-current dark:stroke-gray-300"
      >
        <path
          d="M15.0686 1.25995L14.5477 1.17423L14.2913 1.63578C14.1754 1.84439 14.0545 2.08275 13.9422 2.31963C12.6461 2.16488 11.3406 2.16505 10.0445 2.32014C9.92822 2.08178 9.80478 1.84975 9.67412 1.62413L9.41449 1.17584L8.90333 1.25995C7.33547 1.51794 5.80717 1.99419 4.37748 2.66939L4.19 2.75793L4.07461 2.93019C1.23864 7.16437 0.46302 11.3053 0.838165 15.3924L0.868838 15.7266L1.13844 15.9264C2.81818 17.1714 4.68053 18.1233 6.68582 18.719L7.18892 18.8684L7.50166 18.4469C7.96179 17.8268 8.36504 17.1824 8.709 16.4944L8.71099 16.4904C10.8645 17.0471 13.128 17.0485 15.2821 16.4947C15.6261 17.1826 16.0293 17.8269 16.4892 18.4469L16.805 18.8725L17.3116 18.717C19.3056 18.105 21.1876 17.1751 22.8559 15.9238L23.1224 15.724L23.1528 15.3923C23.5873 10.6524 22.3579 6.53306 19.8947 2.90714L19.7759 2.73227L19.5833 2.64518C18.1437 1.99439 16.6386 1.51826 15.0686 1.25995ZM16.6074 10.7755L16.6074 10.7756C16.5934 11.6409 16.0212 12.1444 15.4783 12.1444C14.9297 12.1444 14.3493 11.6173 14.3493 10.7877C14.3493 9.94885 14.9378 9.41192 15.4783 9.41192C16.0471 9.41192 16.6209 9.93851 16.6074 10.7755ZM8.49373 12.1444C7.94513 12.1444 7.36471 11.6173 7.36471 10.7877C7.36471 9.94885 7.95323 9.41192 8.49373 9.41192C9.06038 9.41192 9.63892 9.93851 9.6417 10.7815C9.62517 11.6239 9.05462 12.1444 8.49373 12.1444Z"
          strokeWidth="1.5"
        />
      </svg>
    ),
  },
];
'''

    def _get_logo_light_svg_content(self):
        # User should update with their logo-light.svg content
        return r'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100"><rect width="100" height="100" rx="15" fill="#747bff"></rect><path fill="#fff" d="M62.5 12.5h-25v12.5h12.5v50h12.5z"></path><path fill="#fff" d="M37.5 87.5h25v-12.5h-12.5v-50h-12.5z"></path></svg>'''

    def _get_logo_dark_svg_content(self):
        # User should update with their logo-dark.svg content
        return r'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 100 100"><rect width="100" height="100" rx="15" fill="#747bff"></rect><path fill="#fff" d="M62.5 12.5h-25v12.5h12.5v50h12.5z"></path><path fill="#fff" d="M37.5 87.5h25v-12.5h-12.5v-50h-12.5z"></path></svg>'''

    # =============================================
    # === Main Execution Logic ===
    # =============================================
def main():
        parser = argparse.ArgumentParser(
            description="CLI tool for creating and managing React (TanStack Router) + Django projects.",
            formatter_class=argparse.RawTextHelpFormatter # Preserve formatting in help text
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands:", required=True) # Make command required

        # --- Create project command ---
        create_parser = subparsers.add_parser(
            "create",
            help="Create a new React+Django project structure.",
            description="Creates a new project directory with separate 'frontend' (React/Vite/TanStack) and 'backend' (Django/DRF) folders."
        )
        create_parser.add_argument("name", help="Name of the project directory to create.")
        # --template argument kept for future expansion, but not currently used.
        # create_parser.add_argument("--template", default="default", help="Project template to use (currently only 'default').")

        # --- Generate component command ---
        component_parser = subparsers.add_parser(
            "component",
            help="Generate a React component.",
            description="Generates a React component file (.tsx) inside the 'frontend/src/components/' directory of the current project."
                      "\\nRun this command from within the project directory."
        )
        component_parser.add_argument("name", help="Name of the component (e.g., UserProfile, user-profile).")
        component_parser.add_argument("--type", choices=["functional", "class"], default="functional",
                                     help="Type of component (default: functional).")

        # --- Generate app command ---
        app_parser = subparsers.add_parser(
            "app",
            help="Generate a Django app.",
            description="Generates a new Django app directory inside the 'backend/' directory of the current project."
                      "\\nRuns 'python manage.py startapp <name>' if possible, otherwise creates files manually."
                      "\\nRun this command from within the project directory."
        )
        app_parser.add_argument("name", help="Name of the Django app (e.g., products, user_profiles).")

        # --- Start servers command ---
        start_parser = subparsers.add_parser( # Assign to variable for potential future args
            "start",
            help="Start development servers.",
            description="Starts both the frontend (Vite) and backend (Django) development servers concurrently."
                      "\\nRun this command from the project's root directory."
        )

        args = parser.parse_args()
        framework = ReactDjangoFramework()

        if args.command == "create":
            framework.create_project(args.name) 
        elif args.command == "component":
            framework.generate_component(args.name, args.type)
        elif args.command == "app":
            framework.generate_app(args.name)
        elif args.command == "start":
            framework.start_servers()
        else:
            parser.print_help()
            sys.exit(1)

if __name__ == "__main__":
        main()