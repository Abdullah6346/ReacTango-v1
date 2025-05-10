import os
import subprocess
import sys
from .path_finder import PathFinder

class ServerManager:
    def __init__(self):
        self.path_finder = PathFinder()

    def start_servers(self):
        """Start both frontend and backend servers concurrently"""
        current_dir = os.getcwd()
        project_root = self.path_finder.find_project_root(current_dir)

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
            backend_process = subprocess.Popen(
                [sys.executable, "manage.py", "runserver"],
                cwd=backend_dir
            )
            print(f"Backend PID: {backend_process.pid}")

            print("Starting frontend server (Vite)...")
            package_manager = "npm"  # Or detect based on lock file
            frontend_process = subprocess.Popen(
                [package_manager, "run", "dev"],
                cwd=frontend_dir,
                shell=sys.platform == "win32"
            )
            print(f"Frontend PID: {frontend_process.pid}")

            print("\nServers started. Press Ctrl+C to stop.")
            if backend_process:
                backend_process.wait()
            if frontend_process:
                frontend_process.wait()

        except KeyboardInterrupt:
            print("\nStopping servers...")
        except Exception as e:
            print(f"\nError starting servers: {e}")
        finally:
            if frontend_process and frontend_process.poll() is None:
                print("Terminating frontend process...")
                frontend_process.terminate()
                frontend_process.wait()
            if backend_process and backend_process.poll() is None:
                print("Terminating backend process...")
                backend_process.terminate()
                backend_process.wait()
            print("Servers stopped.") 