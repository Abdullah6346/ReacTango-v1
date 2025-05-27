#!/usr/bin/env python3
"""
React Tango CLI - A CLI tool to create new projects using ReactTangoTemplate
"""

import argparse
import os
import subprocess
import sys
import shutil
from pathlib import Path
import tempfile

class ReactTangoCLI:
    def __init__(self):
        self.template_repo = "https://github.com/Abdullah6346/ReactTangoTemplate.git"
        self.version = "1.0.0"

    def print_banner(self):
        """Print the React Tango banner"""
        banner = """
╔═══════════════════════════════════════════════════════╗
║                 React Tango CLI                       ║
║        TanStack Router + Django Framework             ║
║                    v{}                             ║
╚═══════════════════════════════════════════════════════╝
        """.format(self.version)
        print(banner)

    def check_git_installed(self):
        """Check if Git is installed on the system"""
        try:
            subprocess.run(['git', '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def check_node_installed(self):
        """Check if Node.js is installed"""
        try:
            subprocess.run(['node', '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def check_python_installed(self):
        """Check if Python is installed"""
        return sys.version_info >= (3, 6)

    def create_project(self, project_name, destination=None):
        """Create a new React Tango project"""
        self.print_banner()
        
        # Validate project name
        if not project_name or not project_name.replace('-', '').replace('_', '').isalnum():
            print("❌ Error: Project name must be alphanumeric (with optional hyphens and underscores)")
            return False

        # Set destination directory
        if destination:
            project_path = Path(destination) / project_name
        else:
            project_path = Path.cwd() / project_name

        # Check if directory already exists
        if project_path.exists():
            print(f"❌ Error: Directory '{project_path}' already exists")
            return False

        # Check prerequisites
        print("🔍 Checking prerequisites...")
        
        if not self.check_git_installed():
            print("❌ Error: Git is not installed. Please install Git first.")
            return False
        print("✅ Git is installed")

        if not self.check_python_installed():
            print("❌ Error: Python 3.6+ is required")
            return False
        print("✅ Python is installed")

        if not self.check_node_installed():
            print("⚠️  Warning: Node.js not found. You'll need it to run the frontend.")
        else:
            print("✅ Node.js is installed")

        # Clone the repository
        print(f"\n📦 Creating project '{project_name}'...")
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir) / "template"
                
                # Clone the repository
                print("🔄 Cloning template repository...")
                subprocess.run([
                    'git', 'clone', '--depth', '1', 
                    self.template_repo, str(temp_path)
                ], check=True, capture_output=True)

                # Remove .git directory
                git_dir = temp_path / '.git'
                if git_dir.exists():
                    shutil.rmtree(git_dir)

                # Copy template to destination
                shutil.copytree(temp_path, project_path)
                
                print(f"✅ Project created successfully at: {project_path}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error cloning repository: {e}")
            return False
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            return False

        # Initialize git repository
        try:
            print("🔄 Initializing Git repository...")
            subprocess.run(['git', 'init'], cwd=project_path, check=True, capture_output=True)
            subprocess.run(['git', 'add', '.'], cwd=project_path, check=True, capture_output=True)
            subprocess.run([
                'git', 'commit', '-m', 'Initial commit from React Tango template'
            ], cwd=project_path, check=True, capture_output=True)
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError:
            print("⚠️  Warning: Could not initialize Git repository")

        # Print success message and next steps
        self.print_success_message(project_name, project_path)
        return True

    def print_success_message(self, project_name, project_path):
        """Print success message with next steps"""
        print(f"""
🎉 Success! Created {project_name} at {project_path}

📋 Next steps:
   cd {project_name}
   
🔧 Install dependencies:
   # Install all dependencies (recommended)
   node install.js
   
   # Or install separately:
   pip install -r requirements.txt  # Backend (Django)
   pnpm install                     # Frontend (React + TanStack Router)

🚀 Start development:
   pnpm run dev

📚 Learn more:
   • Frontend: React with TanStack Router
   • Backend: Django REST API
   • Full Stack: Modern development workflow

Happy coding! 🚀
        """)

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="React Tango CLI - Create full stack apps with TanStack Router + Django",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  react-tango create my-app
  react-tango create my-app --destination /path/to/projects
  react-tango --version
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='React Tango CLI v1.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new React Tango project')
    create_parser.add_argument(
        'project_name', 
        help='Name of the project to create'
    )
    create_parser.add_argument(
        '--destination', '-d',
        help='Destination directory (default: current directory)'
    )

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return

    cli = ReactTangoCLI()
    
    if args.command == 'create':
        success = cli.create_project(args.project_name, args.destination)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()