import argparse
import subprocess
import sys
import os
import shutil # For rmtree
from pathlib import Path

# The GitHub repository URL for your template
TEMPLATE_REPO_URL = "https://github.com/Abdullah6346/ReactTangoTemplate.git"

def run_command_verbose(command, cwd=None):
    """Helper function to run a subprocess command and stream its output."""
    try:
        process = subprocess.Popen(command, cwd=cwd, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate() # Wait for command to finish
        if process.returncode != 0:
            # Error message is already printed by the command itself to stderr
            sys.exit(process.returncode)
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Please ensure it's installed and in your PATH.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running command: {' '.join(command)}\n{e}")
        sys.exit(1)

def run_command_quiet(command, cwd=None):
    """Helper function to run a subprocess command quietly, checking for errors."""
    try:
        subprocess.run(
            command,
            cwd=cwd,
            check=True, # Raise CalledProcessError on non-zero exit
            stdout=subprocess.DEVNULL, # Suppress stdout
            stderr=subprocess.PIPE    # Capture stderr to show on error
        )
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Please ensure it's installed and in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        if e.stderr:
            print(f"Stderr: {e.stderr.decode().strip()}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running command: {' '.join(command)}\n{e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Create a new project from the ReactTangoTemplate."
    )
    parser.add_argument(
        "project_name",
        help="The name of the new project (and the directory to be created).",
    )
    parser.add_argument(
        "--branch",
        help="Specify a branch of the template to clone (e.g., 'main', 'develop'). Defaults to the default branch.",
        default=None # Git will use the default branch of the repo
    )
    parser.add_argument(
        "--no-git-init",
        action="store_true",
        help="Do not initialize a new git repository in the created project.",
    )

    args = parser.parse_args()
    project_name = args.project_name
    branch_to_clone = args.branch

    target_dir = Path(project_name).resolve()

    if target_dir.exists():
        print(f"Error: Directory '{target_dir}' already exists. Please choose a different name or remove the existing directory.")
        sys.exit(1)

    print(f"Cloning ReactTangoTemplate into '{project_name}'...")
    git_clone_command = ["git", "clone"]
    if branch_to_clone:
        git_clone_command.extend(["--branch", branch_to_clone])
    git_clone_command.extend([TEMPLATE_REPO_URL, str(target_dir)])

    run_command_verbose(git_clone_command) # Let git clone output directly

    print(f"\nTemplate cloned successfully into '{target_dir}'.")

    # Remove the .git directory from the cloned template
    git_dir_path = target_dir / ".git"
    if git_dir_path.exists() and git_dir_path.is_dir():
        print(f"Removing template's .git directory from '{git_dir_path}'...")
        try:
            shutil.rmtree(git_dir_path)
            print("Template .git directory removed.")
        except OSError as e:
            print(f"Warning: Could not remove .git directory: {e}. Please remove it manually.")
            # Decide if this should be a fatal error or just a warning
    else:
        # This case should ideally not happen if clone was successful
        print("Warning: Template .git directory not found after clone. Skipping removal.")

    if not args.no_git_init:
        print(f"\nInitializing a new git repository in '{target_dir}'...")
        try:
            run_command_quiet(["git", "init"], cwd=str(target_dir))
            print("New git repository initialized.")

            print("Adding files to the new repository...")
            run_command_quiet(["git", "add", "."], cwd=str(target_dir))

            print("Making initial commit...")
            initial_commit_message = f"Initial commit: Bootstrap '{project_name}' from ReactTangoTemplate"
            run_command_quiet(["git", "commit", "-m", initial_commit_message], cwd=str(target_dir))
            print(f"Initial commit made: \"{initial_commit_message}\"")

        except Exception as e: # Catching general exception from run_command_quiet if it exits
            # Error message is already printed by run_command_quiet
            print("Skipping further git operations due to previous error.")
    else:
        print("\nSkipping git repository initialization as requested (--no-git-init).")

    print("\nProject setup complete!")
    print("\nNext steps:")
    print(f"  1. cd {project_name}")
    print("  2. Follow the setup instructions in the project's README.md.")
    print("     Typically, this involves:")
    print("     - Running `node install.js` (or its variants like `--with-venv`)")
    print("     - Or manually installing backend (`pip install -r requirements.txt`)")
    print("     - And frontend (`pnpm install`) dependencies.")
    print("  3. Then run the development server (e.g., `pnpm run dev`).")

if __name__ == "__main__":
    main()