import argparse
import subprocess
import sys
import os
import shutil # For rmtree
from pathlib import Path
import questionary # Import questionary

# The GitHub repository URL for your template
TEMPLATE_REPO_URL = "https://github.com/Abdullah6346/ReactTangoTemplate.git"

def is_git_available():
    """Checks if the 'git' command is available on the system."""
    try:
        # Try running 'git --version' quietly
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def run_command_verbose(command, cwd=None):
    """Helper function to run a subprocess command and stream its output."""
    try:
        process = subprocess.Popen(command, cwd=cwd, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate() # Wait for command to finish
        if process.returncode != 0:
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
        default=None
    )
    # Flags to explicitly control git initialization, overriding interactive prompt
    git_group = parser.add_mutually_exclusive_group()
    git_group.add_argument(
        "--init-git",
        action="store_true",
        help="Force initialization of a new git repository.",
        dest="force_init_git"
    )
    git_group.add_argument(
        "--no-init-git",
        action="store_true",
        help="Force skipping initialization of a new git repository.",
        dest="force_no_init_git"
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

    run_command_verbose(git_clone_command)

    print(f"\nTemplate cloned successfully into '{target_dir}'.")

    git_dir_path = target_dir / ".git"
    if git_dir_path.exists() and git_dir_path.is_dir():
        print(f"Removing template's .git directory from '{git_dir_path}'...")
        try:
            shutil.rmtree(git_dir_path)
            print("Template .git directory removed.")
        except OSError as e:
            print(f"Warning: Could not remove .git directory: {e}. Please remove it manually.")
    else:
        print("Warning: Template .git directory not found after clone. Skipping removal.")

    # Determine whether to initialize git
    should_initialize_git = False
    git_is_present = is_git_available()

    if args.force_init_git:
        if git_is_present:
            should_initialize_git = True
            print("\n--init-git flag used: Forcing git initialization.")
        else:
            print("\nWarning: --init-git flag used, but Git command not found. Cannot initialize repository.")
            should_initialize_git = False
    elif args.force_no_init_git:
        should_initialize_git = False
        print("\n--no-init-git flag used: Skipping git initialization.")
    else:
        # No explicit flags, so ask interactively if git is available
        if git_is_present:
            try:
                init_choice = questionary.confirm(
                    "Initialize a new git repository in the project?",
                    default=True, # Default to 'Yes'
                    auto_enter=False # User must explicitly press Enter
                ).ask()

                if init_choice is None: # User pressed Ctrl+C or Esc
                    print("\nOperation cancelled by user during git initialization prompt.")
                    sys.exit(0)
                should_initialize_git = init_choice
            except Exception as e: # Catch potential errors from questionary (e.g. if not a TTY)
                print(f"\nCould not display interactive prompt ({e}). Defaulting to initializing git.")
                print("Use --no-init-git to skip or --init-git to force initialization.")
                should_initialize_git = True # Fallback if prompt fails
        else:
            print("\nGit command not found. Cannot initialize a git repository.")
            should_initialize_git = False


    if should_initialize_git:
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
        except Exception:
            # Error already printed by run_command_quiet
            print("Skipping further git operations due to previous error.")
    elif not args.force_no_init_git: # Only print this if not explicitly told not to init
        print("\nSkipping git repository initialization.")


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