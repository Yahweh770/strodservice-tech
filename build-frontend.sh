#!/bin/bash
# Script to build the React frontend for the Electron app

echo "Building React frontend..."

# Navigate to the frontend directory
cd /workspace/src/frontend

# Check if node_modules exists, if not try to install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    if command -v npm &> /dev/null; then
        npm install --no-audit --no-fund
    else
        echo "Error: npm is not installed or not in PATH"
        exit 1
    fi
fi

# Build the React app
echo "Running build command..."
if command -v npm &> /dev/null; then
    npm run build
else
    echo "Error: npm is not installed or not in PATH"
    exit 1
fi

echo "Frontend build completed!"
echo "Build files are located in /workspace/src/frontend/build/"