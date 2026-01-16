#!/usr/bin/env python3
"""
Main entry point for the StrodService project.
This script allows starting different components of the application.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pyjwt",
        "passlib",
        "alembic"
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("Warning: Missing required Python packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nTo install dependencies quickly from vendor directory:")
        print("  bash install-vendor-deps.sh")
        print("Or:")
        print("  pip install -r requirements.txt")
        print()
        return False

    return True

def start_backend():
    """Start the Python FastAPI backend server."""
    if not check_dependencies():
        return False

    backend_path = Path(__file__).parent / "src" / "backend-python"
    if not backend_path.exists():
        print(f"Backend directory not found: {backend_path}")
        return False

    os.chdir(backend_path)
    cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    print(f"Starting backend server with command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=False)
        return True
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
        return True
    except FileNotFoundError:
        print("uvicorn not found. Please install it with: pip install uvicorn[standard]")
        return False


def start_doc_tracking_system():
    """Start the document tracking system UI"""
    try:
        # Import и запуск системы учета документов
        from doc_tracking_system import run_cli_interface
        run_cli_interface()
        return True
    except ImportError as e:
        print(f"Error importing document tracking system: {e}")
        print("Make sure all dependencies are installed.")
        return False


def start_full_project():
    """Start the complete StrodService project with both document tracking and other features."""
    print("Starting full StrodService project...")
    
    # Check if we're in the backend directory structure
    backend_path = Path(__file__).parent / "src" / "backend-python"
    if backend_path.exists():
        os.chdir(backend_path)
        
        # Set the PYTHONPATH to include the current directory
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{Path(__file__).parent.absolute()}:{env.get('PYTHONPATH', '')}"
        
        try:
            # Run the backend server
            cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
            print(f"Starting full backend server with command: {' '.join(cmd)}")
            
            import subprocess
            subprocess.run(cmd, check=True, env=env)
            return True
        except subprocess.CalledProcessError:
            print("Failed to start backend server. Make sure all dependencies are installed.")
            return False
        except FileNotFoundError:
            print("uvicorn not found. Please install it with: pip install uvicorn[standard]")
            return False
    else:
        print(f"Backend directory not found: {backend_path}")
        return False

def show_help():
    """Show help information."""
    print("""
StrodService Project Manager
===========================

Usage: python main.py [command]

Commands:
    backend         - Start the Python FastAPI backend server
    doc-tracker     - Start the document tracking system
    full-project    - Start the complete StrodService project with full functionality
    help            - Show this help message
    """)
    return True

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # Если нет аргументов, запускаем систему учета документов по умолчанию
        return 0 if start_doc_tracking_system() else 1

    command = sys.argv[1].lower()

    if command == "backend":
        return 0 if start_backend() else 1
    if command == "doc-tracker":
        return 0 if start_doc_tracking_system() else 1
    if command == "full-project":
        return 0 if start_full_project() else 1
    if command == "help":
        return 0 if show_help() else 1

    print(f"Unknown command: {command}. Use 'help' for available commands.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
