import argparse
import subprocess
import sys
import os
import shutil
from pathlib import Path
import questionary
from questionary import Style

from . import __version__

# Color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Regular colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

# Enhanced color printing functions
def print_error(message):
    print(f"{Colors.BRIGHT_RED}{EMOJI_ERROR} {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.BRIGHT_YELLOW}{EMOJI_WARNING} {message}{Colors.RESET}")

def print_success(message):
    print(f"{Colors.BRIGHT_GREEN}{EMOJI_SUCCESS} {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.BRIGHT_CYAN}{EMOJI_INFO} {message}{Colors.RESET}")

def print_step(message):
    print(f"{Colors.BRIGHT_BLUE}{EMOJI_GEAR} {message}{Colors.RESET}")

def print_party(message):
    print(f"{Colors.BRIGHT_MAGENTA}{EMOJI_PARTY} {message}{Colors.RESET}")

def print_rocket(message):
    print(f"{Colors.BRIGHT_GREEN}{EMOJI_ROCKET} {message}{Colors.RESET}")

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
EMOJI_PYTHON = "🐍"
EMOJI_NODE = "🟩"
EMOJI_INSTALL = "📦"
EMOJI_NONE = "🔒"
EMOJI_ALL = "🎯"

TEMPLATE_REPO_URL = "https://github.com/Abdullah6346/ReactTangoTemplate.git"

# Custom questionary style
custom_style = Style([
    ('question', 'bold'),
    ('answer', 'fg:#ff9d00 bold'),
    ('pointer', 'fg:#ff9d00 bold'),
    ('highlighted', 'fg:#ff9d00 bold'),
    ('selected', 'fg:#cc5454'),
    ('separator', 'fg:#cc5454'),
    ('instruction', ''),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])

# --- Helper Functions ---
def command_exists(command_name):
    """Checks if a command is available on the system."""
    return shutil.which(command_name) is not None

def is_git_available():
    """Checks if the 'git' command is available on the system."""
    return command_exists("git")

def execute_command(command_list, cwd=None, error_message="Command failed", verbose_output=True, check_return_code=True):
    """
    Executes a command, optionally streaming its output, and handles errors.
    Returns True on success, False on failure if check_return_code is True.
    """
    cmd_str = ' '.join(str(c) for c in command_list)
    print_step(f"Executing: {Colors.CYAN}{cmd_str}{Colors.RESET}" + (f" in {Colors.YELLOW}{cwd}{Colors.RESET}" if cwd else ""))
    try:
        process = subprocess.Popen(
            command_list,
            cwd=cwd,
            stdout=sys.stdout if verbose_output else subprocess.PIPE,
            stderr=sys.stderr if verbose_output else subprocess.PIPE,
            text=True,
            universal_newlines=True # Recommended for text mode
        )
        stdout, stderr = process.communicate() # Wait for command to complete

        if check_return_code and process.returncode != 0:
            print_error(f"{error_message} (Exit code: {process.returncode})")
            if not verbose_output and stderr: # Print stderr if it wasn't already streamed
                print(f"Stderr: {stderr.strip()}")
            return False
        return True
    except FileNotFoundError:
        print_error(f"Command '{command_list[0]}' not found. Please ensure it's installed and in your PATH.")
        return False
    except Exception as e:
        print_error(f"An unexpected error occurred while running command: {cmd_str}\n{e}")
        return False

# --- Python Installation Logic ---
def install_backend_dependencies(project_path: Path, use_venv: bool):
    print(f"\n{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.RESET}")
    print(f"{Colors.BRIGHT_MAGENTA}{EMOJI_PYTHON} BACKEND DEPENDENCY INSTALLATION {EMOJI_PYTHON}{Colors.RESET}")
    print(f"{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.RESET}")
    
    if not command_exists("python3"):
        print_error("Python 3 ('python3') is not installed or not in PATH. Please install Python 3.")
        return False

    pip_command_name = "pip3" if command_exists("pip3") else "pip"
    if not command_exists(pip_command_name):
        print_error(f"pip ('{pip_command_name}') is not installed or not in PATH. Please install pip.")
        return False

    python_executable = "python3"
    requirements_file = project_path / "requirements.txt"
    if not requirements_file.exists():
        print_warning(f"'requirements.txt' not found in {project_path}. Skipping backend dependencies.")
        return True # Not a failure of this function, just nothing to do.

    pip_to_use = pip_command_name
    activate_command = ""

    if use_venv:
        venv_path = project_path / "venv"
        print_step(f"Creating Python virtual environment at '{Colors.YELLOW}{venv_path}{Colors.RESET}'...")
        if not execute_command([python_executable, "-m", "venv", str(venv_path)], cwd=project_path, error_message="Failed to create virtual environment."):
            return False

        if os.name == 'nt': # Windows
            pip_in_venv = venv_path / "Scripts" / f"{pip_command_name}.exe"
            activate_command = f"cd {project_path.name} && .\\venv\\Scripts\\activate" # Simplified for next steps
        else: # macOS/Linux
            pip_in_venv = venv_path / "bin" / pip_command_name
            activate_command = f"cd {project_path.name} && source venv/bin/activate"

        pip_to_use = str(pip_in_venv)
        print_info(f"Virtual environment created. To activate it later: {Colors.CYAN}{activate_command.replace(f'cd {project_path.name} && ', '')}{Colors.RESET}")
    else:
        print_info("Not using a virtual environment for Python dependencies.")

    print_step(f"Installing Python packages from '{Colors.YELLOW}{requirements_file}{Colors.RESET}' using '{Colors.CYAN}{pip_to_use}{Colors.RESET}'...")
    if not execute_command([pip_to_use, "install", "-r", str(requirements_file)], cwd=project_path, error_message="Failed to install Python dependencies."):
        return False

    print_success("Backend dependencies installed successfully! 🎊")
    return True

# --- Node.js Installation Logic ---
def install_frontend_dependencies(project_path: Path):
    print(f"\n{Colors.BRIGHT_GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BRIGHT_GREEN}{EMOJI_NODE} FRONTEND DEPENDENCY INSTALLATION {EMOJI_NODE}{Colors.RESET}")
    print(f"{Colors.BRIGHT_GREEN}{'='*60}{Colors.RESET}")
    
    if not command_exists("node"):
        print_error("Node.js ('node') is not installed or not in PATH. Please install Node.js.")
        return False

    package_json_file = project_path / "package.json"
    if not package_json_file.exists():
        print_warning(f"'package.json' not found in {project_path}. Skipping frontend dependencies.")
        return True # Not a failure, just nothing to do.

    if not command_exists("pnpm"):
        print_info("pnpm not found. Attempting to install pnpm globally using npm...")
        if not command_exists("npm"):
            print_error("npm is not installed or not in PATH. Cannot install pnpm. Please install pnpm or npm manually.")
            return False
        if not execute_command(["npm", "install", "-g", "pnpm"], error_message="Failed to install pnpm globally."):
            return False
        print_success("pnpm installed globally. You might need to open a new terminal for 'pnpm' to be available.")

    print_step("Installing Node.js packages with pnpm...")
    if not execute_command(["pnpm", "install"], cwd=project_path, error_message="Failed to install Node.js dependencies."):
        return False

    print_success("Frontend dependencies installed successfully! 🎊")
    return True

# --- Main Project Setup Orchestrator ---
def run_project_setup(project_path: Path, install_be: bool, install_fe: bool, use_venv_for_be: bool):
    """Runs the full project setup (backend and/or frontend)."""
    print(f"\n{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{EMOJI_INSTALL} STARTING DEPENDENCY INSTALLATIONS {EMOJI_INSTALL}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}")
    
    all_successful = True
    installations_run = 0
    
    if install_be:
        installations_run += 1
        print_info(f"[{installations_run}] Starting backend dependency installation...")
        if not install_backend_dependencies(project_path, use_venv_for_be):
            all_successful = False
            print_error("Backend dependency installation failed.")
        else:
            print_success("Backend installation completed successfully!")
            
    if install_fe:
        installations_run += 1
        print_info(f"[{installations_run}] Starting frontend dependency installation...")
        if not install_frontend_dependencies(project_path):
            all_successful = False
            print_error("Frontend dependency installation failed.")
        else:
            print_success("Frontend installation completed successfully!")

    if all_successful and (install_be or install_fe): # Only show if something was attempted
        print(f"\n{Colors.BRIGHT_GREEN}{'='*70}{Colors.RESET}")
        print_party(f"ALL DEPENDENCY INSTALLATIONS COMPLETED SUCCESSFULLY! {EMOJI_SPARKLES}")
        print(f"{Colors.BRIGHT_GREEN}{'='*70}{Colors.RESET}")
    elif not all_successful:
        print(f"\n{Colors.BRIGHT_YELLOW}{'='*70}{Colors.RESET}")
        print_warning("Dependency installation completed with some issues. Please review the logs above.")
        print(f"{Colors.BRIGHT_YELLOW}{'='*70}{Colors.RESET}")
    
    return all_successful

def handle_create_project(args):
    """Handles the logic for the 'create' subcommand."""
    project_name = args.project_name
    branch_to_clone = args.branch

    target_dir = Path(project_name).resolve()

    if target_dir.exists():
        print_error(f"Directory '{target_dir}' already exists. Please choose a different name or remove the existing directory.")
        sys.exit(1)

    print(f"{Colors.BRIGHT_CYAN}{EMOJI_CLONE} Cloning ReactTangoTemplate into '{Colors.YELLOW}{project_name}{Colors.RESET}{Colors.BRIGHT_CYAN}'...{Colors.RESET}")
    git_clone_command = ["git", "clone"]
    if branch_to_clone:
        git_clone_command.extend(["--branch", branch_to_clone])
    git_clone_command.extend([TEMPLATE_REPO_URL, str(target_dir)])

    if not execute_command(git_clone_command, error_message="Failed to clone template repository."):
        sys.exit(1)
    print_success(f"Template cloned successfully into '{Colors.YELLOW}{target_dir}{Colors.RESET}'.")

    git_dir_path = target_dir / ".git"
    if git_dir_path.exists() and git_dir_path.is_dir():
        print_step("Removing template's .git directory...")
        try:
            shutil.rmtree(git_dir_path)
            print(f"{Colors.BRIGHT_GREEN}{EMOJI_SPARKLES} Template .git directory removed.{Colors.RESET}")
        except OSError as e:
            print_warning(f"Could not remove .git directory: {e}. Please remove it manually.")
    else:
        print_warning("Template .git directory not found after clone. Skipping removal.")

    # --- Git Initialization ---
    should_initialize_git = False
    if is_git_available():
        if args.force_init_git:
            should_initialize_git = True
            print_step("--init-git flag used: Forcing git initialization.")
        elif args.force_no_init_git:
            should_initialize_git = False
            print(f"{Colors.BRIGHT_YELLOW}{EMOJI_SKIP} --no-init-git flag used: Skipping git initialization.{Colors.RESET}")
        else:
            try:
                init_choice = questionary.confirm(
                    f"{EMOJI_PROMPT} Initialize a new git repository in the project?",
                    default=True, 
                    auto_enter=False,
                    style=custom_style
                ).ask()
                if init_choice is None: # User pressed Ctrl+C or Esc
                    print(f"\n{Colors.BRIGHT_RED}{EMOJI_CANCEL} Operation cancelled by user. Exiting.{Colors.RESET}")
                    sys.exit(0)
                should_initialize_git = init_choice
            except Exception as e: # Handle non-interactive environment
                print_warning(f"Could not display interactive git prompt ({e}). Defaulting to no git initialization.")
                print_info("Use --init-git or --no-init-git to explicitly control this.")
                should_initialize_git = False # Safer default
    else:
        if args.force_init_git:
            print_warning("--init-git flag used, but Git command not found. Cannot initialize repository.")
        else:
            print_warning("Git command not found. Skipping git repository initialization.")

    if should_initialize_git:
        print(f"\n{Colors.BRIGHT_BLUE}{EMOJI_GIT} Initializing a new git repository in '{Colors.YELLOW}{target_dir}{Colors.RESET}{Colors.BRIGHT_BLUE}'...{Colors.RESET}")
        if execute_command(["git", "init"], cwd=str(target_dir), error_message="Failed to initialize git repository."):
            print(f"{Colors.BRIGHT_GREEN}{EMOJI_SPARKLES} New git repository initialized.{Colors.RESET}")
            print_step("Adding files to the new repository...")
            if execute_command(["git", "add", "."], cwd=str(target_dir), error_message="Failed to add files to git."):
                print_step("Making initial commit...")
                initial_commit_message = f"Initial commit: Bootstrap '{project_name}' from ReactTangoTemplate"
                if execute_command(["git", "commit", "-m", initial_commit_message], cwd=str(target_dir), error_message="Failed to make initial commit."):
                    print_success(f"Initial commit made: \"{initial_commit_message}\"")

    # --- Enhanced Dependency Installation with More Options ---
    ran_any_installation = False
    install_choices_made = []

    if not args.skip_all_install: # If user didn't explicitly skip all
        package_json_exists = (target_dir / "package.json").exists()
        requirements_txt_exists = (target_dir / "requirements.txt").exists()

        available_install_options = []
        
        # Add "Install All" option if both exist
        if requirements_txt_exists and package_json_exists:
            available_install_options.append(
                questionary.Choice(
                    f"{EMOJI_ALL} Install All Dependencies (Backend + Frontend)", 
                    value="all", 
                    checked=True
                )
            )
        
        # Add individual options
        if requirements_txt_exists:
            available_install_options.append(
                questionary.Choice(
                    f"{EMOJI_PYTHON} Backend Only (Python with venv)", 
                    value="backend", 
                    checked=False if (requirements_txt_exists and package_json_exists) else True
                )
            )
        if package_json_exists:
            available_install_options.append(
                questionary.Choice(
                    f"{EMOJI_NODE} Frontend Only (Node.js with pnpm)", 
                    value="frontend", 
                    checked=False if (requirements_txt_exists and package_json_exists) else True
                )
            )
        
        # Add "Install None" option
        available_install_options.append(
            questionary.Choice(
                f"{EMOJI_NONE} Install None (Skip all installations)", 
                value="none", 
                checked=False
            )
        )

        if available_install_options:
            if args.install_all:
                print_step("--install-all flag used: Proceeding with all available installations.")
                if requirements_txt_exists:
                    install_choices_made.append("backend")
                if package_json_exists:
                    install_choices_made.append("frontend")
            else:
                try:
                    print(f"\n{Colors.BRIGHT_MAGENTA}{'='*70}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_MAGENTA}{EMOJI_INSTALL} DEPENDENCY INSTALLATION OPTIONS {EMOJI_INSTALL}{Colors.RESET}")
                    print(f"{Colors.BRIGHT_MAGENTA}{'='*70}{Colors.RESET}")
                    
                    selected_option = questionary.select(
                        f"{EMOJI_PROMPT} What dependencies would you like to install?",
                        choices=available_install_options,
                        style=custom_style
                    ).ask()

                    if selected_option is None: # User cancelled
                        print(f"\n{Colors.BRIGHT_RED}{EMOJI_CANCEL} Dependency installation cancelled by user.{Colors.RESET}")
                        install_choices_made = [] # Ensure it's an empty list
                    elif selected_option == "all":
                        if requirements_txt_exists:
                            install_choices_made.append("backend")
                        if package_json_exists:
                            install_choices_made.append("frontend")
                        print_info(f"Selected: {Colors.BRIGHT_GREEN}Install All Dependencies{Colors.RESET}")
                    elif selected_option == "none":
                        install_choices_made = []
                        print_info(f"Selected: {Colors.BRIGHT_YELLOW}Skip All Installations{Colors.RESET}")
                    else:
                        install_choices_made = [selected_option]
                        option_name = "Backend" if selected_option == "backend" else "Frontend"
                        print_info(f"Selected: {Colors.BRIGHT_CYAN}{option_name} Only{Colors.RESET}")
                        
                except Exception as e:
                    print_warning(f"Could not display interactive install prompt ({e}). Skipping installations.")
                    print_info("Use --install-all to force or --skip-all-install to suppress this.")
                    install_choices_made = []

            if install_choices_made:
                install_be = "backend" in install_choices_made
                install_fe = "frontend" in install_choices_made
                # For backend, always use venv if installing, unless a --no-venv flag is explicitly passed by user
                # Here, args.with_venv is True by default or set by --with-venv/--no-venv
                use_venv_for_be = args.with_venv if install_be else False

                if run_project_setup(target_dir, install_be, install_fe, use_venv_for_be):
                    ran_any_installation = True # Mark that at least one setup was attempted successfully
            elif not args.install_all : # Only show skip message if not forced by --install-all
                print(f"\n{Colors.BRIGHT_YELLOW}{EMOJI_SKIP} No dependencies selected for installation.{Colors.RESET}")
        else:
            print_info("No dependency manifest files (requirements.txt, package.json) found. Skipping installation phase.")
    else: # --skip-all-install was used
        print(f"\n{Colors.BRIGHT_YELLOW}{EMOJI_SKIP} --skip-all-install flag used. All dependency installations are skipped.{Colors.RESET}")

    # Final success message with enhanced styling
    print(f"\n{Colors.BRIGHT_GREEN}{'='*70}{Colors.RESET}")
    print_party(f"PROJECT '{Colors.BRIGHT_YELLOW}{project_name.upper()}{Colors.RESET}{Colors.BRIGHT_MAGENTA}' CREATED SUCCESSFULLY! {EMOJI_ROCKET}")
    print(f"{Colors.BRIGHT_GREEN}{'='*70}{Colors.RESET}")
    
    print(f"\n{Colors.BRIGHT_BLUE}{EMOJI_NEXT_STEPS} NEXT STEPS:{Colors.RESET}")
    print(f"  {Colors.BRIGHT_CYAN}1.{Colors.RESET} {Colors.YELLOW}cd {project_name}{Colors.RESET}")

    if not ran_any_installation and not args.skip_all_install:
        print(f"  {Colors.BRIGHT_CYAN}2.{Colors.RESET} {Colors.BRIGHT_BLUE}{EMOJI_GEAR} Install dependencies manually if needed:{Colors.RESET}")
        if (target_dir / "requirements.txt").exists() and "backend" not in install_choices_made:
             print(f"     {Colors.BRIGHT_MAGENTA}{EMOJI_PYTHON} Backend:{Colors.RESET} {Colors.CYAN}python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt{Colors.RESET}")
        if (target_dir / "package.json").exists() and "frontend" not in install_choices_made:
             print(f"     {Colors.BRIGHT_GREEN}{EMOJI_NODE} Frontend:{Colors.RESET} {Colors.CYAN}pnpm install{Colors.RESET}")
    elif args.with_venv and "backend" in install_choices_made:
        activate_cmd_rel = f"venv/Scripts/activate" if os.name == 'nt' else "venv/bin/activate"
        print(f"  {Colors.BRIGHT_CYAN}2.{Colors.RESET} {Colors.BRIGHT_MAGENTA}{EMOJI_PYTHON} Activate Python virtual environment:{Colors.RESET} {Colors.CYAN}source {activate_cmd_rel}{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}3.{Colors.RESET} {Colors.BRIGHT_GREEN}{EMOJI_ROCKET} Start development server:{Colors.RESET} {Colors.CYAN}pnpm run dev{Colors.RESET}")
    else:
        print(f"  {Colors.BRIGHT_CYAN}2.{Colors.RESET} {Colors.BRIGHT_GREEN}{EMOJI_ROCKET} Start development server:{Colors.RESET} {Colors.CYAN}pnpm run dev{Colors.RESET}")

    print(f"\n  {Colors.DIM}For more details, check the README.md inside your new project.{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_YELLOW}{EMOJI_SPARKLES} Happy coding! {EMOJI_SPARKLES}{Colors.RESET}")

def main():
    banner = f"""{Colors.BRIGHT_CYAN}
╔═══════════════════════════════════════════════════════╗
║                 {Colors.BRIGHT_YELLOW}React Tango CLI{Colors.BRIGHT_CYAN}                       ║
║        {Colors.BRIGHT_GREEN}TanStack Router + Django Framework{Colors.BRIGHT_CYAN}             ║
║                    {Colors.BRIGHT_MAGENTA}v{__version__}{Colors.BRIGHT_CYAN}                             ║
╚═══════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

    parser = argparse.ArgumentParser(
        description=f"{EMOJI_ROCKET} ReactTango CLI - Create and manage ReactTango projects.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers(dest="command", title="Available commands", help="Run 'reactango <command> --help' for more information.")
    subparsers.required = True

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

    # --- Git Initialization Flags ---
    git_group_create = parser_create.add_mutually_exclusive_group()
    git_group_create.add_argument(
        "--init-git",
        action="store_true",
        help="Force initialization of a new git repository.",
        dest="force_init_git"
    )
    git_group_create.add_argument(
        "--no-init-git",
        action="store_true",
        help="Force skipping git initialization.",
        dest="force_no_init_git"
    )

    # --- Enhanced Dependency Installation Flags ---
    install_group = parser_create.add_mutually_exclusive_group()
    install_group.add_argument(
        "--install-all",
        action="store_true",
        help="Automatically install all available dependencies (backend & frontend).",
    )
    install_group.add_argument(
        "--skip-all-install",
        action="store_true",
        help="Skip all automatic dependency installations and prompts.",
    )
    install_group.add_argument(
        "--install-none",
        action="store_true",
        help="Explicitly skip all dependency installations (same as --skip-all-install).",
        dest="skip_all_install"
    )
    
    # Venv for backend (only relevant if backend is installed)
    # Default is True if backend dependencies are installed.
    parser_create.add_argument(
        "--with-venv",
        action="store_true",
        default=True, # Explicitly set default, though store_true implies False if not present
        help="Use a Python virtual environment for backend (default: True if backend is installed).",
    )
    parser_create.add_argument(
        "--no-venv",
        action="store_false", # This will set args.with_venv to False if used
        dest="with_venv",
        help="Do not use a Python virtual environment for backend.",
    )

    parser_create.set_defaults(func=handle_create_project)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()