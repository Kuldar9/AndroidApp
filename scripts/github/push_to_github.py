import subprocess
import sys

def run_command(command, check=True, capture_output=False):
    """Run a command and return the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output, encoding='utf-8')
    
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        sys.exit(result.returncode)
    
    # If capture_output is True, ensure the result is not None before calling strip()
    if capture_output:
        if result.stdout:
            return result.stdout.strip()
        else:
            print(f"No output returned for command: {command}")
            return None
    return None

# Ensure the repository is connected to GitHub (origin remote)
remotes = run_command("git remote", capture_output=True)
if 'origin' not in remotes:
    print("GitHub repository not connected. Connecting now...")
    run_command("git remote add origin https://github.com/kuldar9/AndroidApp.git")
else:
    print("GitHub repository already connected.")

# Check the current branch and ensure it's on 'main'
current_branch = run_command("git branch --show-current")
if current_branch != "main":
    print("Switching to main branch...")
    run_command("git checkout main")

# Stage all changes
print("Staging changes...")
run_command("git add .")

# Check for staged changes before committing
diff_index = run_command("git diff --cached", capture_output=True)
if diff_index:
    commit_message = "Your commit message"  # Replace with your dynamic commit message if needed
    print(f"Committing changes with message: {commit_message}")
    run_command(f'git commit -m "{commit_message}"')
else:
    print("No changes to commit.")

# Push changes to GitHub (main branch)
print("Pushing changes to GitHub (main branch)...")
run_command("git push origin main")

print("Changes pushed to GitHub on the main branch.")