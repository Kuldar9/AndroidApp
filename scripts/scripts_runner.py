import os
import subprocess
import sys

# Define the path to the Scripts directory
SCRIPTS_DIR = './scripts'

# Function to list files in the Scripts directory
def list_files_in_directory(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            # Only consider Python or Node.js files
            if filename.endswith('.py') or filename.endswith('.js'):
                files.append(os.path.join(root, filename))
    return files

# Function to execute the selected file
def run_selected_script(file_path):
    if file_path.endswith('.py'):
        # Run Python script
        print(f"Running Python script: {file_path}")
        subprocess.run(['python', file_path], check=True)  # Use default python executable
    elif file_path.endswith('.js'):
        # Run Node.js script
        print(f"Running Node.js script: {file_path}")
        subprocess.run(['node', file_path], check=True)

def main():
    # List all Python and Node.js scripts in the Scripts directory
    scripts = list_files_in_directory(SCRIPTS_DIR)
    
    if not scripts:
        print("❌ No Python or Node.js scripts found in the Scripts directory.")
        return

    # Display the numbered list of scripts
    print("🔎 Found the following scripts:")
    for idx, script in enumerate(scripts, 1):
        print(f"{idx}. {script}")
    
    # Prompt the user to select a script by number
    while True:
        try:
            selection = int(input("Please enter the number of the script you want to run: "))
            if selection < 1 or selection > len(scripts):
                print("❌ Invalid selection. Please choose a valid number from the list.")
                continue
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            continue
        
        # Run the selected script
        selected_script = scripts[selection - 1]
        run_selected_script(selected_script)
        break  # Exit the loop once a valid script has been selected and executed

    print("Script Runner done! Press Enter to exit...")
    input()  # This will pause until the user presses Enter
    sys.exit(0)

if __name__ == "__main__":
    main()