import subprocess
import os

def update_requirements():
    # Specify the path to your requirements.txt file
    requirements_file = 'requirements.txt'
    
    # Run pip freeze to get the current dependencies
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)
    
    # Save the output of pip freeze to the requirements.txt file
    with open(requirements_file, 'w') as f:
        f.write(result.stdout)
    
    print(f"{requirements_file} has been updated.")

# Run the function to update requirements
if __name__ == "__main__":
    update_requirements()