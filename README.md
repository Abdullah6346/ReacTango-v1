# 🚀 React Tango Creator (`reactango`)

<div align="center">

<img src="https://raw.githubusercontent.com/Abdullah6346/ReactTangoTemplate/main/app/welcome/logo.svg" alt="Reactango Logo" width="200"/>


![React Tango Creator Logo](https://img.shields.io/badge/⚡-React%20Tango%20Creator-blue?style=for-the-badge&logo=react)

[![PyPI version](https://img.shields.io/pypi/v/react-tango-creator.svg?style=flat-square)](https://pypi.org/project/react-tango-creator/)
[![Python Version](https://img.shields.io/pypi/pyversions/react-tango-creator.svg?style=flat-square)](https://pypi.org/project/react-tango-creator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/react-tango-creator?style=flat-square)](https://pypi.org/project/react-tango-creator/)

**The fastest way to bootstrap modern full-stack applications with React + Django**

[Quick Start](#-quick-start) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## ✨ What is React Tango Creator?

`reactango` is a powerful command-line tool that instantly scaffolds production-ready full-stack applications using the **ReactTangoTemplate**. It combines the best of modern frontend and backend technologies:

Stop wasting time on boilerplate setup and start building features from day one!

## 🎯 Quick Start

Get your new project running in under 30 seconds:

```bash
# Install reactango globally
pip install reactango

# Create your new project
reactango create my-awesome-project

# Navigate to your project
cd my-awesome-project

```

That's it! Your full-stack application is now ready!

## 🌟 Features

### 🏗️ **Instant Project Scaffolding**

- Creates a complete full-stack project structure in seconds
- No manual setup or configuration required
- Ready-to-use development environment

### 🔄 **Clean Git History**

- Automatically initializes a fresh Git repository
- Removes template history for a clean start
- Makes initial commit with all template files

### ⚙️ **Modern Tech Stack**

- **React 18** with hooks and modern patterns
- **TanStack Router** for type-safe routing
- **Vite** for lightning-fast development
- **Django** with REST Framework for robust APIs
- **TypeScript** for type safety across the stack

### 🐳 **Containerized Development**

- Docker Compose setup included
- Consistent development environment
- Easy deployment and scaling

### 🛠️ **Developer Experience**

- Hot reloading for both frontend and backend
- Pre-configured linting and formatting
- Organized project structure
- Comprehensive documentation

## 📦 Installation

### Install from PyPI (Recommended)

```bash
pip install reactango
```

## 🚀 Usage

### Basic Usage

Create a new project with the default template:

```bash
reactango create my-project-name
```

### Advanced Options

```bash
# Create project with custom branch
reactango create-app my-project --branch feature-branch

# Skip automatic Git initialization
reactango create-app my-project --no-git

# Show help
reactango --help
```

### Command Options

| Option         | Description                            | Default  |
| -------------- | -------------------------------------- | -------- |
| `project_name` | Name of your new project               | Required |
| `--branch`     | Specific branch of the template to use | `main`   |
| `--no-git`     | Skip Git repository initialization     | `False`  |
| `--help`       | Show help message                      | -        |

## 📚 What You Get

After running `reactango create-app`, your project will have:

```
/ (root)
├── api/                  # Django api
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── welcome/
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── __pycache__/
│   │   └── models/
│   │       ├── __init__.py
│   │       └── welcome.py
│   └── __pycache__/
├── app/                  # React app (TanStack Router)
│   ├── app.css
│   ├── root.tsx
│   ├── routes.ts
│   ├── routes/
│   │   └── home.tsx
│   └── welcome/
│       ├── logo-dark.svg
│       ├── logo-light.svg
│       └── welcome.tsx
├── config/               # Django config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __pycache__/
├── public/               # Static assets
│   └── favicon.ico
├── db.sqlite3
├── Dockerfile
├── install.js
├── manage.py
├── package.json
├── pnpm-lock.yaml
├── react-router.config.ts
├── requirements.txt
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🔧 Prerequisites

Before using `reactango`, ensure you have:

- **Python 3.7+** with pip
- **Git** for version control
- **Node.js 16+** (if running frontend outside Docker)

## Getting Started

### Backend (Django)

1. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Frontend (React + TanStack Router)

1. Install Node dependencies:
   ```sh
   pnpm install
   ```

### Install All (Backend + Frontend)

1. Run the installer script (with interactive options):
   ```sh
   node install.js
   ```
   - Use `--backend-only` to install only Django dependencies
   - Use `--frontend-only` to install only frontend dependencies
   - Use `--with-venv` to create and use a Python virtual environment

### Simple RUN

1. Run this:
   ```sh
   pnpm run dev
   ```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `python -m pytest`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/Abdullah6346/ReacTango-v1/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/Abdullah6346/ReacTango-v1/discussions)
- **Documentation**: [Wiki](https://github.com/Abdullah6346/ReacTango-v1/wiki)

## 🙏 Acknowledgments

- Built on top of the powerful [ReactTangoTemplate](https://github.com/Abdullah6346/ReactTangoTemplate)
- Inspired by tools like Create React App and Django startproject
- Thanks to all contributors and the open-source community

---

<div align="center">

**Made with ❤️ for the developer community**

[⭐ Star us on GitHub](https://github.com/Abdullah6346/ReacTango-v1) if this project helped you!

</div>
