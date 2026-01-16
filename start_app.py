#!/usr/bin/env python3
"""
Application startup script for the StrodService project.
This script handles common startup issues and ensures proper initialization.
"""

import os
import sys
import subprocess
from pathlib import Path


def setup_environment():
    """Setup the Python path and environment variables for proper operation."""
    project_root = Path(__file__).parent
    backend_path = project_root / "src" / "backend-python"
    
    # Add paths to Python path to ensure proper imports
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(backend_path))
    
    # Set environment variables for the application
    os.environ.setdefault("DATABASE_URL", f"sqlite:///{project_root}/strod_service_main.db")
    os.environ.setdefault("SECRET_KEY", "your-super-secret-key-change-in-production")
    os.environ.setdefault("ADMIN_USERNAME", "admin")
    os.environ.setdefault("ADMIN_PASSWORD", "admin123")


def install_dependencies():
    """Install required dependencies from requirements.txt"""
    print("Installing dependencies...")
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ])
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def start_document_tracker():
    """Start the document tracking system."""
    setup_environment()
    
    try:
        from doc_tracking_system import run_cli_interface
        print("Starting Document Tracking System...")
        run_cli_interface()
    except ImportError as e:
        print(f"Error importing document tracking system: {e}")
        print("Make sure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"Unexpected error in document tracking system: {e}")
        return False
    
    return True


def start_backend_server():
    """Start the FastAPI backend server."""
    setup_environment()
    
    # Change to backend directory for proper relative imports
    backend_path = Path(__file__).parent / "src" / "backend-python"
    os.chdir(backend_path)
    
    try:
        import uvicorn
        # Import the main app module
        import main as backend_main
        print("Starting backend server on http://0.0.0.0:8000")
        uvicorn.run(
            backend_main.app, 
            host="0.0.0.0", 
            port=8000,
            reload=False  # Disable reload for production
        )
        return True
    except ImportError as e:
        print(f"Error importing backend: {e}")
        print("Make sure all dependencies are installed and backend files exist.")
        return False
    except Exception as e:
        print(f"Unexpected error starting backend: {e}")
        return False


def start_full_application():
    """Start the complete StrodService application."""
    setup_environment()
    
    print("Starting full StrodService application...")
    
    # Change to backend directory for proper operation
    backend_path = Path(__file__).parent / "src" / "backend-python"
    if backend_path.exists():
        os.chdir(backend_path)
        
        try:
            import uvicorn
            import importlib.util
            
            # Load the backend main module using importlib to avoid conflicts
            spec = importlib.util.spec_from_file_location("backend_main", backend_path / "main.py")
            backend_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(backend_module)
            
            print("Starting full backend server with all modules...")
            print("Access the application at http://0.0.0.0:8000")
            print("API documentation at http://0.0.0.0:8000/docs")
            
            uvicorn.run(
                backend_module.app,
                host="0.0.0.0",
                port=8000,
                reload=False
            )
            return True
        except Exception as e:
            print(f"Error starting full application: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print(f"Backend directory not found: {backend_path}")
        return False


def show_help():
    """Show help information."""
    print("""
StrodService Application Starter
===============================

Usage: python start_app.py [command]

Commands:
    doc-tracker     - Start the document tracking system (CLI)
    backend         - Start the backend server (FastAPI)
    full-app        - Start the complete application with all modules
    install         - Install required dependencies
    help            - Show this help message

Examples:
    python start_app.py doc-tracker    # Start document tracking system
    python start_app.py backend        # Start backend server only
    python start_app.py full-app       # Start complete application
    python start_app.py install        # Install dependencies first
    """)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1].lower()
    
    if command == "doc-tracker":
        return 0 if start_document_tracker() else 1
    elif command == "backend":
        return 0 if start_backend_server() else 1
    elif command == "full-app":
        return 0 if start_full_application() else 1
    elif command == "install":
        return 0 if install_dependencies() else 1
    elif command == "help":
        show_help()
        return 0
    else:
        print(f"Unknown command: {command}")
        show_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())