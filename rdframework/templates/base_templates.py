class BaseTemplates:
    """Base class for all template generators"""
    
    def get_gitignore_content(self):
        """Get content for .gitignore file"""
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
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
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# React
dist/
dist-ssr/
*.local

# Testing
coverage/
.coverage
htmlcov/
.pytest_cache/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover
.hypothesis/
"""

    def get_docker_compose_content(self, project_name):
        """Get content for docker-compose.yml file"""
        return f"""version: '3.8'

services:
  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DJANGO_SETTINGS_MODULE={project_name}.settings
    depends_on:
      - db

  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB={project_name}
      - POSTGRES_USER={project_name}
      - POSTGRES_PASSWORD={project_name}

volumes:
  postgres_data:
"""

    def get_env_content(self):
        """Get content for .env file"""
        return """# Django settings
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Frontend settings
VITE_API_URL=http://localhost:8000
"""

    def get_env_example_content(self):
        """Get content for .env.example file"""
        return """# Django settings
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Frontend settings
VITE_API_URL=http://localhost:8000
""" 