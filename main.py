#!/usr/bin/env python3
"""
Main entry point for the StrodService project.
This script allows starting different components of the application.
"""

import sys
import subprocess
import os
from pathlib import Path

def start_backend():
    """Start the Python FastAPI backend server."""
    backend_path = Path(__file__).parent / "src" / "backend-python"
    if not backend_path.exists():
        print(f"Backend directory not found: {backend_path}")
        return False
    
    os.chdir(backend_path)
    cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    print(f"Starting backend server with command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
        return True
    except FileNotFoundError:
        print("uvicorn not found. Please install it with: pip install uvicorn[standard]")
        return False

def show_help():
    """Show help information."""
    print("""
StrodService Project Manager
===========================

Usage: python main.py [command]

Commands:
    backend     - Start the Python FastAPI backend server
    help        - Show this help message
    """)
    return True

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Please specify a command. Use 'help' for available commands.")
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "backend":
        return 0 if start_backend() else 1
    elif command == "help":
        return 0 if show_help() else 1
    else:
        print(f"Unknown command: {command}. Use 'help' for available commands.")
        return 1

if __name__ == "__main__":
    sys.exit(main())