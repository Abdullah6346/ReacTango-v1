import argparse
import subprocess
import sys
import os
import shutil
from pathlib import Path
import questionary

from . import __version__ 

EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_SUCCESS = "✅"
EMOJI_INFO = "ℹ️"
EMOJI_CLONE = "🌀"
EMOJI_TRASH = "🗑️"
EMOJI_GIT = "🐙"
EMOJI_ROCKET = "🚀"
EMOJI_PARTY = "🎉"
EMOJI_SPARKLES = "✨"
EMOJI_PROMPT = "❓"
EMOJI_CANCEL = "🛑"
EMOJI_SKIP = "🚫"
EMOJI_NEXT_STEPS = "👉"
EMOJI_GEAR = "⚙️"
EMOJI_ADD = "➕"
EMOJI_COMMIT = "📝"


TEMPLATE_REPO_URL = "https://github.com/Abdullah6346/ReactTangoTemplate.git"

# --- Helper functions (is_git_available, run_command_verbose, run_command_quiet) remain the same ---
def is_git_available():
    """Checks if the 'git' command is available on the system."""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def run_command_verbose(command, cwd=None):
    """Helper function to run a subprocess command and stream its output."""
    try:
        process = subprocess.Popen(command, cwd=cwd, stdout=sys.stdout, stderr=sys.stderr)
        process.communicate()
        if process.returncode != 0:
            sys.exit(process.returncode)
    except FileNotFoundError:
        print(f"{EMOJI_ERROR} Error: Command '{command[0]}' not found. Please ensure it's installed and in your PATH.")
        sys.exit(1)
    except Exception as e:
        print(f"{EMOJI_ERROR} An unexpected error occurred while running command: {' '.join(command)}\n{e}")
        sys.exit(1)

def run_command_quiet(command, cwd=None):
    """Helper function to run a subprocess command quietly, checking for errors."""
    try:
        subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
    except FileNotFoundError:
        print(f"{EMOJI_ERROR} Error: Command '{command[0]}' not found. Please ensure it's installed and in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"{EMOJI_ERROR} Error running command: {' '.join(command)}")
        if e.stderr:
            print(f"Stderr: {e.stderr.decode().strip()}")
        sys.exit(1)
    except Exception as e:
        print(f"{EMOJI_ERROR} An unexpected error occurred while running command: {' '.join(command)}\n{e}")
        sys.exit(1)
# --- End of helper functions ---


def handle_create_project(args):
    """Handles the logic for the 'create' subcommand."""
    project_name = args.project_name
    branch_to_clone = args.branch

    target_dir = Path(project_name).resolve()

    if target_dir.exists():
        print(f"{EMOJI_ERROR} Error: Directory '{target_dir}' already exists. Please choose a different name or remove the existing directory.")
        sys.exit(1)

    print(f"{EMOJI_CLONE} Cloning ReactTangoTemplate into '{project_name}'...")
    git_clone_command = ["git", "clone"]
    if branch_to_clone:
        git_clone_command.extend(["--branch", branch_to_clone])
    git_clone_command.extend([TEMPLATE_REPO_URL, str(target_dir)])

    run_command_verbose(git_clone_command)

    print(f"\n{EMOJI_SUCCESS} Template cloned successfully into '{target_dir}'.")

    git_dir_path = target_dir / ".git"
    if git_dir_path.exists() and git_dir_path.is_dir():
        print(f"{EMOJI_TRASH} Removing template's .git directory from '{git_dir_path}'...")
        try:
            shutil.rmtree(git_dir_path)
            print(f"{EMOJI_SPARKLES} Template .git directory removed.")
        except OSError as e:
            print(f"{EMOJI_WARNING} Warning: Could not remove .git directory: {e}. Please remove it manually.")
    else:
        print(f"{EMOJI_WARNING} Warning: Template .git directory not found after clone. Skipping removal.")

    should_initialize_git = False
    git_is_present = is_git_available()

    if args.force_init_git: # These come from the subparser now
        if git_is_present:
            should_initialize_git = True
            print(f"\n{EMOJI_GEAR} --init-git flag used: Forcing git initialization.")
        else:
            print(f"\n{EMOJI_WARNING} Warning: --init-git flag used, but Git command not found. Cannot initialize repository.")
            should_initialize_git = False
    elif args.force_no_init_git: # These come from the subparser now
        should_initialize_git = False
        print(f"\n{EMOJI_SKIP} --no-init-git flag used: Skipping git initialization.")
    else:
        if git_is_present:
            try:
                init_choice = questionary.confirm(
                    f"{EMOJI_PROMPT} Initialize a new git repository in the project?",
                    default=True,
                    auto_enter=False
                ).ask()

                if init_choice is None:
                    print(f"\n{EMOJI_CANCEL} Operation cancelled by user during git initialization prompt.")
                    sys.exit(0)
                should_initialize_git = init_choice
            except Exception as e:
                print(f"\n{EMOJI_WARNING} Warning: Could not display interactive prompt ({e}). Defaulting to initializing git.")
                print(f"{EMOJI_INFO} Use --no-init-git to skip or --init-git to force initialization.")
                should_initialize_git = True
        else:
            print(f"\n{EMOJI_WARNING} Warning: Git command not found. Cannot initialize a git repository.")
            should_initialize_git = False

    if should_initialize_git:
        print(f"\n{EMOJI_GIT} Initializing a new git repository in '{target_dir}'...")
        try:
            run_command_quiet(["git", "init"], cwd=str(target_dir))
            print(f"{EMOJI_SPARKLES} New git repository initialized.")

            print(f"{EMOJI_ADD} Adding files to the new repository...")
            run_command_quiet(["git", "add", "."], cwd=str(target_dir))

            print(f"{EMOJI_COMMIT} Making initial commit...")
            initial_commit_message = f"Initial commit: Bootstrap '{project_name}' from ReactTangoTemplate"
            run_command_quiet(["git", "commit", "-m", initial_commit_message], cwd=str(target_dir))
            print(f"{EMOJI_SUCCESS} Initial commit made: \"{initial_commit_message}\"")
        except Exception:
            print(f"{EMOJI_SKIP} Skipping further git operations due to previous error.")
    elif not args.force_no_init_git: # Only print if not explicitly told not to init
        print(f"\n{EMOJI_SKIP} Skipping git repository initialization.")

    print(f"\n{EMOJI_PARTY} Project '{project_name}' created successfully! {EMOJI_ROCKET}")
    print(f"\n{EMOJI_NEXT_STEPS} Next steps:")
    print(f"  1. cd {project_name}")
    print("  2. Follow the setup instructions in the project's README.md.")
    # ... (rest of the next steps messages)
    print(f"\n{EMOJI_SPARKLES} Happy coding! {EMOJI_SPARKLES}")


def main():
    banner = f"""
╔═══════════════════════════════════════════════════════╗
║                 React Tango CLI                       ║
║        TanStack Router + Django Framework             ║
║                    v{__version__}                             ║
╚═══════════════════════════════════════════════════════╝
"""
    print(banner)

    # Main parser
    parser = argparse.ArgumentParser(
        description=f"{EMOJI_ROCKET} ReactTango CLI - Create and manage ReactTango projects.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", title="Available commands", help="Run 'reactango <command> --help' for more information.")
    subparsers.required = True # Make a subcommand required

    # --- Create 'create' command subparser ---
    parser_create = subparsers.add_parser(
        "create",
        help="Create a new ReactTango project from the template.",
        description="Creates a new project by cloning the ReactTangoTemplate and setting it up for you."
    )
    parser_create.add_argument(
        "project_name",
        help="The name of the new project (and the directory to be created).",
    )
    parser_create.add_argument(
        "--branch",
        help="Specify a branch of the template to clone (e.g., 'main', 'develop'). Defaults to the default branch.",
        default=None
    )
    # Git initialization flags specific to the 'create' command
    git_group_create = parser_create.add_mutually_exclusive_group()
    git_group_create.add_argument(
        "--init-git",
        action="store_true",
        help="Force initialization of a new git repository in the created project.",
        dest="force_init_git"
    )
    git_group_create.add_argument(
        "--no-init-git",
        action="store_true",
        help="Force skipping initialization of a new git repository in the created project.",
        dest="force_no_init_git"
    )
    # Set the function to call when 'create' command is used
    parser_create.set_defaults(func=handle_create_project)

    # --- Add more subparsers here for future commands ---
    # parser_update = subparsers.add_parser("update", help="Update something...")
    # parser_update.set_defaults(func=handle_update_command)

    args = parser.parse_args()

    # Call the function associated with the chosen subparser
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # This should not happen if subparsers.required = True and a default is not set
        parser.print_help()

if __name__ == "__main__":
    main()