#!/bin/bash
# Script to run the password evaluation web server

echo "=========================================="
echo "Password Strength Evaluation Server"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the server
echo ""
echo "Starting server..."
echo "Open your browser and navigate to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py

