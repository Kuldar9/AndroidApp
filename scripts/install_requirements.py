#!/bin/bash

# Create and activate the virtual environment (if not already created)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv python_venv
fi

# Activate the virtual environment
source venv/bin/activate  # For Linux/macOS
# source venv/Scripts/activate  # For Windows

# Install requirements from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found!"
fi

echo "Virtual environment setup and dependencies installed."