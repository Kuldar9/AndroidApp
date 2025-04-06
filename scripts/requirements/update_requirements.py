import subprocess
import sys
import os
import shutil

VENV_DIR = "./python_venv"
REQUIREMENTS_FILE = 'requirements.txt'  # Default name for the requirements file

def get_python_executable():
    """Get the Python executable for the virtual environment."""
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def get_pip_executable():
    """Get the pip executable for the virtual environment."""
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "pip")

def update_requirements(requirements_file=REQUIREMENTS_FILE):
    """Update the requirements.txt with the current environment's installed packages."""
    
    # Ensure we're in a virtual environment by checking the Python executable path
    python_exec = get_python_executable()
    pip_exec = get_pip_executable()

    if not os.path.isfile(python_exec):
        print("❌ Virtual environment not found. Please ensure python_venv exists.")
        sys.exit(1)

    print(f"Using Python executable from virtual environment: {python_exec}")
    print(f"Using pip executable from virtual environment: {pip_exec}")

    # Run pip freeze using the virtual environment's pip
    try:
        print("Running pip freeze...")
        result = subprocess.run([pip_exec, 'freeze'], check=True, stdout=subprocess.PIPE, text=True)
        print("pip freeze output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Failed to run pip freeze.")
        print(e)
        sys.exit(1)

    # Check if requirements file exists, if not, create it
    if not os.path.isfile(requirements_file):
        print(f"⚠️ {requirements_file} not found. It will be created.")

    # Write the output of pip freeze to the requirements.txt
    try:
        with open(requirements_file, 'w') as f:
            f.write(result.stdout)
        print(f"✅ {requirements_file} has been updated with current dependencies.")
    except IOError as e:
        print(f"❌ Failed to write to {requirements_file}.")
        print(e)
    sys.exit(1) 	

if __name__ == "__main__":
    update_requirements()