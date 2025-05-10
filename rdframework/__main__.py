import argparse
import sys
from .core.framework import ReactDjangoFramework

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for creating and managing React (TanStack Router) + Django projects.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands:", required=True)

    # Create project command
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new React+Django project structure.",
        description="Creates a new project directory with separate 'frontend' (React/Vite/TanStack) and 'backend' (Django/DRF) folders."
    )
    create_parser.add_argument("name", help="Name of the project directory to create.")

    # Generate component command
    component_parser = subparsers.add_parser(
        "component",
        help="Generate a React component.",
        description="Generates a React component file (.tsx) inside the 'frontend/src/components/' directory of the current project."
                  "\nRun this command from within the project directory."
    )
    component_parser.add_argument("name", help="Name of the component (e.g., UserProfile, user-profile).")
    component_parser.add_argument("--type", choices=["functional", "class"], default="functional",
                                 help="Type of component (default: functional).")

    # Generate app command
    app_parser = subparsers.add_parser(
        "app",
        help="Generate a Django app.",
        description="Generates a new Django app directory inside the 'backend/' directory of the current project."
                  "\nRuns 'python manage.py startapp <name>' if possible, otherwise creates files manually."
                  "\nRun this command from within the project directory."
    )
    app_parser.add_argument("name", help="Name of the Django app (e.g., products, user_profiles).")

    # Start servers command
    start_parser = subparsers.add_parser(
        "start",
        help="Start development servers.",
        description="Starts both the frontend (Vite) and backend (Django) development servers concurrently."
                  "\nRun this command from the project's root directory."
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