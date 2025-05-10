# React-Django Framework

A framework for creating modern web applications with React (TanStack Router) and Django.

## Features

- React frontend with TypeScript and TanStack Router
- Django backend with REST framework
- PostgreSQL database
- Docker support
- Development and production configurations
- CLI tool for project management

## Installation

```bash
pip install rdframework
```

## Usage

### Create a New Project

```bash
rdframework create myproject
```

This will create a new project with the following structure:

```
myproject/
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

### Generate a New Component

```bash
rdframework component MyComponent
```

This will create a new React component in the `frontend/app/components` directory.

### Generate a New Django App

```bash
rdframework app myapp
```

This will create a new Django app in the `backend` directory.

### Start Development Servers

```bash
rdframework start
```

This will start both the frontend and backend development servers.

## Development

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 13+
- Docker and Docker Compose (optional)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/rdframework.git
   cd rdframework
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:

   ```bash
   pip install -e .
   ```

4. Run tests:
   ```bash
   python -m pytest
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
