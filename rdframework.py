#!/usr/bin/env python
import argparse
import os
import shutil
import subprocess
import json
import sys
from pathlib import Path

class ReactDjangoFramework:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        
    def create_project(self, name, template="default"):
        """Create a new project with the given name and template."""
        print(f"Creating new project: {name}")
        
        # Create project directories
        project_dir = os.path.abspath(name)
        os.makedirs(project_dir, exist_ok=True)
        
        # Create backend (Django) structure
        self._create_django_structure(project_dir, name)
        
        # Create frontend (React) structure
        self._create_react_structure(project_dir, name)
                
        # Create README and other root files
        self._create_root_files(project_dir, name)
        
        # Initialize git
        subprocess.run(["git", "init"], cwd=project_dir)
        
        print(f"\nProject '{name}' created successfully!")
        print(f"\nNext steps:")
        print(f"  1. cd {name}")
        print(f"  2. Create a virtual environment: python -m venv venv")
        print(f"  3. Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print(f"  4. Install backend dependencies: pip install -r backend/requirements.txt")
        print(f"  5. Install frontend dependencies: cd frontend && npm install")
        print(f"  6. Start backend: cd backend && python manage.py runserver")
        print(f"  7. Start frontend: cd frontend && npm run dev")

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
            f.write(self._get_django_urls_content())
        
        # Create wsgi.py
        with open(os.path.join(django_project_dir, "wsgi.py"), "w") as f:
            f.write(self._get_django_wsgi_content(project_snake_case))
        
        # Create asgi.py
        with open(os.path.join(django_project_dir, "asgi.py"), "w") as f:
            f.write(self._get_django_asgi_content(project_snake_case))
        
        # Create manage.py
        with open(os.path.join(backend_dir, "manage.py"), "w") as f:
            f.write(self._get_django_manage_content(project_snake_case))
        
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
            f.write("from rest_framework import serializers\n")
        
        # Create api/views.py
        with open(os.path.join(api_dir, "views.py"), "w") as f:
            f.write("from rest_framework.decorators import api_view\nfrom rest_framework.response import Response\n\n@api_view(['GET'])\ndef api_overview(request):\n    api_urls = {\n        'List': '/api/items/',\n        'Detail': '/api/items/<id>/',\n        'Create': '/api/items/create/',\n        'Update': '/api/items/update/<id>/',\n        'Delete': '/api/items/delete/<id>/',\n    }\n    return Response(api_urls)\n")
        
        # Create api/urls.py
        with open(os.path.join(api_dir, "urls.py"), "w") as f:
            f.write("from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.api_overview, name='api-overview'),\n]\n")

        # Create api/migrations folder
        os.makedirs(os.path.join(api_dir, "migrations"), exist_ok=True)
        with open(os.path.join(api_dir, "migrations", "__init__.py"), "w") as f:
            f.write("")
    
    def _create_react_structure(self, project_dir, project_name):
        """Create React project structure"""
        print("Creating React frontend structure...")
        frontend_dir = os.path.join(project_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)
        
        # Create package.json
        with open(os.path.join(frontend_dir, "package.json"), "w") as f:
            f.write(self._get_package_json_content(project_name))
        
        # Create vite.config.ts
        with open(os.path.join(frontend_dir, "vite.config.ts"), "w") as f:
            f.write(self._get_vite_config_content())
        
        # Create tsconfig.json
        with open(os.path.join(frontend_dir, "tsconfig.json"), "w") as f:
            f.write(self._get_tsconfig_content())
        
        # Create .eslintrc.json
        with open(os.path.join(frontend_dir, ".eslintrc.cjs"), "w") as f:
            f.write(self._get_eslint_content())
        
        # Create src directory
        src_dir = os.path.join(frontend_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        
        # Create index.html
        with open(os.path.join(frontend_dir, "index.html"), "w") as f:
            f.write(self._get_index_html_content(project_name))
        
        # Create main.tsx
        with open(os.path.join(src_dir, "main.tsx"), "w") as f:
            f.write(self._get_main_tsx_content())
        
        # Create App.tsx
        with open(os.path.join(src_dir, "App.tsx"), "w") as f:
            f.write(self._get_app_tsx_content())
        
        # Create App.css
        with open(os.path.join(src_dir, "App.css"), "w") as f:
            f.write(self._get_app_css_content())
        
        # Create index.css
        with open(os.path.join(src_dir, "index.css"), "w") as f:
            f.write(self._get_index_css_content())
        
        # Create components directory
        components_dir = os.path.join(src_dir, "components")
        os.makedirs(components_dir, exist_ok=True)
        
        # Create api.ts - for React API service
        with open(os.path.join(src_dir, "api.ts"), "w") as f:
            f.write(self._get_api_ts_content())
        
        # Create .gitignore
        with open(os.path.join(frontend_dir, ".gitignore"), "w") as f:
            f.write(self._get_frontend_gitignore_content())
        
        # Create public directory
        public_dir = os.path.join(frontend_dir, "public")
        os.makedirs(public_dir, exist_ok=True)
        
    
    def _create_root_files(self, project_dir, project_name):
        """Create root files like README, .gitignore, etc."""
        print("Creating project configuration files...")
        
        # Create README.md
        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(self._get_readme_content(project_name))
        
        # Create .gitignore
        with open(os.path.join(project_dir, ".gitignore"), "w") as f:
            f.write(self._get_gitignore_content())
        
        # Create .env file
        with open(os.path.join(project_dir, ".env"), "w") as f:
            f.write(self._get_env_content())
        
        # Create .env.example file
        with open(os.path.join(project_dir, ".env.example"), "w") as f:
            f.write(self._get_env_content())
    
    def generate_component(self, name, component_type="functional"):
        """Generate a new React component"""
        current_dir = os.getcwd()
        
        # Find the components directory
        components_dir = self._find_components_dir(current_dir)
        
        if not components_dir:
            print("Error: Could not find components directory. Make sure you are in a React-Django project.")
            return
        
        component_path = os.path.join(components_dir, f"{name}.tsx")
        
        # Check if component already exists
        if os.path.exists(component_path):
            print(f"Error: Component {name} already exists at {component_path}")
            return
        
        # Create component content based on type
        if component_type == "functional":
            content = self._get_functional_component_content(name)
        else:
            content = self._get_class_component_content(name)
        
        # Write component file
        with open(component_path, "w") as f:
            f.write(content)
        
        print(f"Component {name} created at {component_path}")
    
    def generate_app(self, name):
        """Generate a new Django app"""
        current_dir = os.getcwd()
        
        # Find the backend directory
        backend_dir = self._find_backend_dir(current_dir)
        
        if not backend_dir:
            print("Error: Could not find backend directory. Make sure you are in a React-Django project.")
            return
        
        app_dir = os.path.join(backend_dir, name)
        
        # Check if app already exists
        if os.path.exists(app_dir):
            print(f"Error: App {name} already exists at {app_dir}")
            return
        
        # Create app directory
        os.makedirs(app_dir, exist_ok=True)
        
        # Create __init__.py
        with open(os.path.join(app_dir, "__init__.py"), "w") as f:
            f.write("")
        
        # Create admin.py
        with open(os.path.join(app_dir, "admin.py"), "w") as f:
            f.write("from django.contrib import admin\n\n# Register your models here.\n")
        
        # Create apps.py
        with open(os.path.join(app_dir, "apps.py"), "w") as f:
            f.write(f"from django.apps import AppConfig\n\n\nclass {name.capitalize()}Config(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = '{name}'\n")
        
        # Create models.py
        with open(os.path.join(app_dir, "models.py"), "w") as f:
            f.write("from django.db import models\n\n# Create your models here.\n")
        
        # Create serializers.py
        with open(os.path.join(app_dir, "serializers.py"), "w") as f:
            f.write("from rest_framework import serializers\n")
        
        # Create views.py
        with open(os.path.join(app_dir, "views.py"), "w") as f:
            f.write("from django.shortcuts import render\nfrom rest_framework import viewsets\nfrom rest_framework.response import Response\n\n# Create your views here.\n")
        
        # Create urls.py
        with open(os.path.join(app_dir, "urls.py"), "w") as f:
            f.write("from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    # Add your URLs here\n]\n")
        
        # Create migrations folder
        os.makedirs(os.path.join(app_dir, "migrations"), exist_ok=True)
        with open(os.path.join(app_dir, "migrations", "__init__.py"), "w") as f:
            f.write("")
        
        print(f"Django app {name} created at {app_dir}")
        print(f"Don't forget to add '{name}' to INSTALLED_APPS in your settings.py")
    
    def start_servers(self):
        """Start both frontend and backend servers"""
        current_dir = os.getcwd()
        
        # Find the project root directory
        project_root = self._find_project_root(current_dir)
        
        if not project_root:
            print("Error: Could not find project root. Make sure you are in a React-Django project.")
            return
        
        print("Starting backend server...")
        backend_process = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            cwd=os.path.join(project_root, "backend")
        )
        
        print("Starting frontend server...")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=os.path.join(project_root, "frontend")
        )
        
        try:
            # Wait for both processes
            backend_process.wait()
            frontend_process.wait()
        except KeyboardInterrupt:
            print("Stopping servers...")
            backend_process.terminate()
            frontend_process.terminate()
    
    def _find_components_dir(self, start_dir):
        """Find the components directory"""
        # First, try to find it in the current directory or its children
        for root, dirs, _ in os.walk(start_dir):
            if "components" in dirs:
                components_dir = os.path.join(root, "components")
                if os.path.exists(os.path.join(root, "App.tsx")) or os.path.exists(os.path.join(root, "App.jsx")):
                    return components_dir
        
        # If not found, try to find the project root and then look for components
        project_root = self._find_project_root(start_dir)
        if project_root:
            frontend_dir = os.path.join(project_root, "frontend")
            if os.path.exists(frontend_dir):
                src_dir = os.path.join(frontend_dir, "src")
                if os.path.exists(src_dir):
                    components_dir = os.path.join(src_dir, "components")
                    if os.path.exists(components_dir):
                        return components_dir
        
        return None
    
    def _find_backend_dir(self, start_dir):
        """Find the backend directory"""
        # First, check if the current directory is the backend directory
        if os.path.exists(os.path.join(start_dir, "manage.py")):
            return start_dir
        
        # If not, try to find the project root and then look for backend
        project_root = self._find_project_root(start_dir)
        if project_root:
            backend_dir = os.path.join(project_root, "backend")
            if os.path.exists(backend_dir) and os.path.exists(os.path.join(backend_dir, "manage.py")):
                return backend_dir
        
        return None
    
    def _find_project_root(self, start_dir):
        """Find the project root directory"""
        current_dir = os.path.abspath(start_dir)
        
        # Look for both frontend and backend directories
        while current_dir != os.path.dirname(current_dir):  # Stop at root directory
            if os.path.exists(os.path.join(current_dir, "frontend")) and os.path.exists(os.path.join(current_dir, "backend")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        return None
    
    # Template content methods
    def _get_django_settings_content(self, project_name):
        return f'''"""
Django settings for {project_name} project.
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = '{project_name}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Only for development

# JWT settings
SIMPLE_JWT = {{
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}}
'''
    
    def _get_django_urls_content(self):
        return '''"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
'''
    
    def _get_django_wsgi_content(self, project_name):
        return f'''"""
WSGI config for {project_name} project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_wsgi_application()
'''
    
    def _get_django_asgi_content(self, project_name):
        return f'''"""
ASGI config for {project_name} project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_asgi_application()
'''
    
    def _get_django_manage_content(self, project_name):
        return f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''
    
    def _get_requirements_content(self):
        return '''Django>=4.2.0,<5.0.0
djangorestframework>=3.14.0,<4.0.0
djangorestframework-simplejwt>=5.2.2,<6.0.0
django-cors-headers>=4.0.0,<5.0.0
psycopg2-binary>=2.9.6,<3.0.0
gunicorn>=20.1.0,<21.0.0
'''
    
    def _get_package_json_content(self, project_name):
        # Convert to kebab-case for package name
        package_name = project_name.lower().replace('_', '-').replace(' ', '-')
        
        return f'''{{
  "name": "{package_name}",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "axios": "^1.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.15.0",
    "jwt-decode": "^3.1.2"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.3",
    "eslint": "^8.45.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }}
}}
'''
    
    def _get_vite_config_content(self):
        return '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
'''
    
    def _get_tsconfig_content(self):
        return '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''
    
    def _get_eslint_content(self):
        return '''module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
'''
    
    def _get_index_html_content(self, project_name):
        return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
    
    def _get_main_tsx_content(self):
        return '''import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
'''
    
    def _get_app_tsx_content(self):
        return '''import { useState, useEffect } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import './App.css'
import api from './api'

function App() {
  const [message, setMessage] = useState<string>('Loading...')

  useEffect(() => {
    // Example API call
    api.get('/api/')
      .then(response => {
        setMessage(JSON.stringify(response.data))
      })
      .catch(error => {
        console.error('Error fetching API data:', error)
        setMessage('Error connecting to API')
      })
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>React + Django Framework</h1>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/about">About</Link></li>
          </ul>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={
            <div className="home-page">
              <h2>Welcome to your new application!</h2>
              <p>This is a template for a React + Django application.</p>
              <div className="api-message">
                <h3>API Response:</h3>
                <pre>{message}</pre>
              </div>
            </div>
          } />
          <Route path="/about" element={
            <div className="about-page">
              <h2>About</h2>
              <p>This application was created with the React-Django Framework CLI.</p>
            </div>
          } />
        </Routes>
      </main>

      <footer>
        <p>&copy; {new Date().getFullYear()} React-Django Framework</p>
      </footer>
    </div>
  )
}

export default App
'''
    
    def _get_app_css_content(self):
        return '''
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #282c34;
  padding: 1rem;
  color: white;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.app-header nav ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
}

.app-header nav li {
  margin-right: 1rem;
}

.app-header nav a {
  color: white;
  text-decoration: none;
}

.app-header nav a:hover {
  text-decoration: underline;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.api-message {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.api-message pre {
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

footer {
  background-color: #f5f5f5;
  padding: 1rem;
  text-align: center;
}
'''
    
    def _get_index_css_content(self):
        return '''
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

#root {
  width: 100%;
  min-height: 100vh;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
}
'''
    
    def _get_api_ts_content(self):
        return '''import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the JWT token in headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If the error is 401 and we haven't tried to refresh the token yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        
        const response = await axios.post(`${API_URL}/api/token/refresh/`, {
          refresh: refreshToken,
        });
        
        // Store the new tokens
        localStorage.setItem('token', response.data.access);
        
        // Update the original request with the new token
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        
        // Retry the original request
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails, clear tokens and redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
'''
    
    def _get_frontend_gitignore_content(self):
        return '''# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
'''
    
    
    def _get_readme_content(self, project_name):
        return f'''# {project_name}

A full-stack web application built with React and Django.

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd {project_name}
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm run dev
```

4. Open your browser and navigate to http://localhost:5173

## Features

- React 18 with TypeScript
- Django 4 with Django REST Framework
- JWT Authentication
- API integration

## Development

### Backend

- Create a new Django app:
```bash
python manage.py startapp app_name
```

- Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Frontend

- Create a production build:
```bash
npm run build
```



## License

This project is licensed under the MIT License.
'''
    
    def _get_gitignore_content(self):
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
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
*.egg-info/
.installed.cfg
*.egg
*.manifest
*.spec
pip-log.txt
pip-delete-this-directory.txt
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/
.pytest_cache/
.venv
venv/
ENV/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
.DS_Store
dist
dist-ssr
coverage
*.local

# Database
*.sqlite3
*.db

# Editor directories and files
.idea
.vscode
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs
*.log


'''
    
    def _get_env_content(self):
        return '''# Django settings
DEBUG=True
SECRET_KEY=change-this-in-production
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Database settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Frontend settings
VITE_API_URL=http://localhost:8000
'''
    
    def _get_functional_component_content(self, name):
        return f'''import React from 'react';

interface {name}Props {{
  // Define your props here
}}

const {name}: React.FC<{name}Props> = (props) => {{
  return (
    <div className="{name.toLowerCase()}">
      <h2>{name} Component</h2>
    </div>
  );
}};

export default {name};
'''
    
    def _get_class_component_content(self, name):
        return f'''import React, {{ Component }} from 'react';

interface {name}Props {{
  // Define your props here
}}

interface {name}State {{
  // Define your state here
}}

class {name} extends Component<{name}Props, {name}State> {{
  constructor(props: {name}Props) {{
    super(props);
    this.state = {{
      // Initialize your state here
    }};
  }}

  render() {{
    return (
      <div className="{name.toLowerCase()}">
        <h2>{name} Component</h2>
      </div>
    );
  }}
}}

export default {name};
'''

def main():
    parser = argparse.ArgumentParser(description="CLI tool for React-Django framework")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Create project command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("name", help="Name of the project")
    create_parser.add_argument("--template", default="default", help="Template to use")
    
    # Generate component command
    component_parser = subparsers.add_parser("component", help="Generate a React component")
    component_parser.add_argument("name", help="Name of the component")
    component_parser.add_argument("--type", choices=["functional", "class"], default="functional", 
                                 help="Type of component")
    
    # Generate app command
    app_parser = subparsers.add_parser("app", help="Generate a Django app")
    app_parser.add_argument("name", help="Name of the app")
    
    # Start servers command
    subparsers.add_parser("start", help="Start both frontend and backend servers")
    
    args = parser.parse_args()
    
    framework = ReactDjangoFramework()
    
    if args.command == "create":
        framework.create_project(args.name, args.template)
    elif args.command == "component":
        framework.generate_component(args.name, args.type)
    elif args.command == "app":
        framework.generate_app(args.name)
    elif args.command == "start":
        framework.start_servers()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()