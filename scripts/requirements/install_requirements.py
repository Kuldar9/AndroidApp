import os
import subprocess
import sys
import platform
import shutil

VENV_DIR = "./python_venv"
REQUIREMENTS_FILE = os.path.join(".", "requirements.txt")  # Changeable requirements file path

def run_command(command, shell=True, capture_output=False):
    """Helper function to run a command and capture output."""
    result = subprocess.run(command, shell=shell, text=True, capture_output=capture_output)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        if result.stderr:
            print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip() if capture_output else None

def is_same_requirements(pip_path, requirements_file):
    """Check if installed packages match the requirements.txt."""
    try:
        installed = subprocess.check_output([pip_path, "freeze"], text=True)
        with open(requirements_file, "r") as f:
            required = f.read()
        return installed.strip() == required.strip()
    except Exception as e:
        print("⚠️ Could not compare installed packages with requirements.txt.")
        print(str(e))
        return False

def get_python_executable():
    """Get the Python executable for the current environment."""
    return shutil.which("python3") or shutil.which("python")

def main():
    # Step 1: Create virtual environment if it doesn't exist
    if not os.path.isdir(VENV_DIR):
        print("🛠️ Creating virtual environment...")
        python_exec = get_python_executable()
        if not python_exec:
            print("❌ Could not find a Python executable.")
            sys.exit(1)
        run_command(f'"{python_exec}" -m venv "{VENV_DIR}"')
    else:
        print("✅ Virtual environment already exists. Skipping creation.")

    # Step 2: Set Python executable and pip paths based on OS
    if platform.system() == "Windows":
        python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
        pip_executable = os.path.join(VENV_DIR, "Scripts", "pip.exe")
        activate_command = f'"{VENV_DIR}\\Scripts\\activate.bat"'
        activate_gitbash_command = f"source {VENV_DIR}/Scripts/activate"  # Fix for Git Bash activation
    else:
        python_executable = os.path.join(VENV_DIR, "bin", "python")
        pip_executable = os.path.join(VENV_DIR, "bin", "pip")
        activate_command = f"source {VENV_DIR}/bin/activate"
        activate_gitbash_command = activate_command  # On non-Windows systems, it's the same

    # Step 3: Upgrade pip using python executable from the virtual environment (recommended way)
    print("⬆️ Upgrading pip...")
    run_command(f'"{python_executable}" -m pip install --upgrade pip')

    # Step 4: Install requirements only if needed
    if os.path.isfile(REQUIREMENTS_FILE):
        print("📦 Checking if dependencies are up-to-date...")
        if not is_same_requirements(pip_executable, REQUIREMENTS_FILE):
            print(f"📥 Installing/updating dependencies from {REQUIREMENTS_FILE}...")
            run_command(f'"{pip_executable}" install -r {REQUIREMENTS_FILE}')
        else:
            print("✅ Dependencies are already up-to-date. Skipping installation.")
    else:
        print(f"⚠️ No {REQUIREMENTS_FILE} found in the specified directory. Skipping dependency installation.")

    # Step 5: Show how to activate the environment
    print("\n🎉 Setup complete!")
    print(f"👉 To activate the virtual environment, run:\n\"{activate_command}\"")
    print(f"👉 To activate the virtual environment in Git Bash, run:\n{activate_gitbash_command}")
    sys.exit(0)

if __name__ == "__main__":
    main()