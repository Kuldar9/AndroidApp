import subprocess
import sys

def run_command(command, check=True, capture_output=False):
    result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)
    if check and result.returncode != 0:
        print(f"Error running command: {command}")
        if result.stderr:
            print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip() if capture_output else None

# Fetch latest changes
print("Fetching latest changes from GitHub...")
run_command("git fetch origin")

# Check if 'dev' branch exists locally
branches = run_command("git branch", capture_output=True)
if 'dev' not in [b.strip().replace("* ", "") for b in branches.splitlines()]:
    print("No dev branch found locally. Exiting...")
    sys.exit(1)

# Switch to main branch
print("Switching to main branch...")
run_command("git checkout main")

# Merge dev into main
print("Merging dev into main...")
run_command('git merge dev -m "Merging dev into main"')

# Push to GitHub
print("Pushing merged changes to GitHub...")
run_command("git push origin main")

# Delete the local dev branch
print("Deleting local dev branch...")
run_command("git branch -d dev")

# Delete the remote dev branch
print("Deleting remote dev branch...")
run_command("git push origin --delete dev")

print("Merged dev into main and deleted dev branch locally and remotely.")