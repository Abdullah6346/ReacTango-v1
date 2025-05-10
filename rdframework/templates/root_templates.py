from .base_templates import BaseTemplates

class RootTemplates(BaseTemplates):
    """Templates for root-level project files"""

    def get_readme_content(self, project_name):
        """Get content for README.md"""
        return f"""# {project_name}

A modern web application built with React (TanStack Router) and Django.

## Features

- React frontend with TypeScript and TanStack Router
- Django backend with REST framework
- PostgreSQL database
- Docker support
- Development and production configurations

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 13+
- Docker and Docker Compose (optional)

### Development Setup

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

4. Open your browser and visit:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Docker Setup

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Open your browser and visit:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Project Structure

```
{project_name}/
├── backend/           # Django backend
│   ├── api/          # API app
│   ├── manage.py     # Django management script
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── app/         # Application code
│   ├── public/      # Static files
│   └── package.json
├── .env             # Environment variables
├── .env.example     # Example environment variables
├── docker-compose.yml
└── README.md
```

## Development

### Backend

- Create a new Django app:
  ```bash
  python manage.py startapp <app_name>
  ```

- Run migrations:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### Frontend

- Create a new component:
  ```bash
  npm run component <component_name>
  ```

- Create a new route:
  ```bash
  npm run route <route_name>
  ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
""" 