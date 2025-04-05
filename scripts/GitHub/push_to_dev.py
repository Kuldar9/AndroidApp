import subprocess

def run_command(command, check=True, capture_output=False):
    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        exit(result.returncode)
    return result.stdout.strip() if capture_output else None

# Check if the repository is connected to a remote
remotes = run_command("git remote", capture_output=True)
if 'origin' not in remotes:
    print("GitHub repository not connected. Connecting now...")
    run_command("git remote add origin https://github.com/kuldar9/AndroidApp.git")
else:
    print("GitHub repository already connected.")

# Check if the 'dev' branch exists and switch to it
branches = run_command("git branch", capture_output=True).splitlines()
branches = [b.strip().replace("* ", "") for b in branches]
if "dev" in branches:
    print("Switching to existing dev branch...")
    run_command("git checkout dev")
else:
    print("Creating and switching to new dev branch...")
    run_command("git checkout -b dev")

# Add and commit changes
print("Staging changes...")
run_command("git add .")

# Check for staged changes before committing
diff_index = run_command("git diff --cached", capture_output=True)
if diff_index:
    commit_message = "Your commit message"  # Replace or make dynamic if needed
    run_command(f'git commit -m "{commit_message}"')
    print("Changes committed.")
else:
    print("No changes to commit.")

# Push to GitHub
print("Pushing changes to GitHub...")
run_command("git push --set-upstream origin dev")
print("Changes pushed to GitHub on dev branch.")