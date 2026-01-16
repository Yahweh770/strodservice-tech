#!/usr/bin/env python3
"""
Main entry point for the StrodService project.
This script allows starting different components of the application.
"""

import sys
import subprocess
import os
import tempfile
from pathlib import Path

# Configure log file path dynamically
log_file_path = os.path.join(os.environ.get("TEMP", tempfile.gettempdir()), "strod_service_log.txt")


def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pyjwt",
        "passlib",
        "alembic",
        "python-multipart"
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
        # Add current directory to Python path to ensure proper imports
        import sys
        import os
        from pathlib import Path
        current_dir = str(Path(__file__).parent)
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
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
    
    # Add the project root to the Python path to ensure proper imports
    project_root = Path(__file__).parent
    backend_path = project_root / "src" / "backend-python"
    
    import sys
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    
    # Check if we're in the backend directory structure
    if backend_path.exists():
        os.chdir(backend_path)
        
        # Set the PYTHONPATH to include the current directory
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{str(project_root)}:{str(backend_path)}:{env.get('PYTHONPATH', '')}"
        
        try:
            # Run the backend server with full reload disabled for production
            cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
            print(f"Starting full backend server with command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, check=False, env=env)  # Changed check=True to check=False to handle graceful shutdowns
            return result.returncode == 0
        except FileNotFoundError:
            print("uvicorn not found. Please install it with: pip install uvicorn[standard]")
            return False
    else:
        print(f"Backend directory not found: {backend_path}")
        # Fallback: try to run from current directory
        try:
            # Import the backend modules directly
            import sys
            backend_dir = str(Path(__file__).parent / "src" / "backend-python")
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            
            # Import and run the main backend application
            os.chdir(backend_path)  # Change to backend directory to ensure proper relative imports
            sys.path.insert(0, str(backend_path))  # Ensure backend path is first
            
            import importlib.util
            spec = importlib.util.spec_from_file_location("backend_main", backend_path / "main.py")
            backend_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(backend_module)
            
            import uvicorn
            print("Starting full backend server from main directory...")
            uvicorn.run(backend_module.app, host="0.0.0.0", port=8000)
            return True
        except ImportError as e:
            print(f"Failed to import backend: {e}")
            print("Attempting to install dependencies and retry...")
            
            # Try to install dependencies first
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(Path(__file__).parent / "requirements.txt")])
                
                # Retry import after installing dependencies
                os.chdir(backend_path)  # Change to backend directory to ensure proper relative imports
                import importlib.util
                spec = importlib.util.spec_from_file_location("backend_main", backend_path / "main.py")
                backend_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(backend_module)
                
                import uvicorn
                print("Starting full backend server from main directory after installing dependencies...")
                uvicorn.run(backend_module.app, host="0.0.0.0", port=8000)
                return True
            except Exception as install_error:
                print(f"Failed to install dependencies: {install_error}")
                print("Make sure all dependencies are installed and backend files exist.")
                return False


def start_construction_remarks_system():
    """Start the construction remarks system"""
    try:
        # Try to run the demo construction remarks system
        import sys
        backend_dir = str(Path(__file__).parent / "src" / "backend-python")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        # Add the project root to path as well
        project_root = str(Path(__file__).parent)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Import with error handling
        try:
            from app.schemas.construction_remarks import RemarkStatus
            from app.crud_construction_remarks import get_construction_remarks
        except ImportError as schema_error:
            print(f"Could not import construction remarks modules: {schema_error}")
            print("These modules are available when running the full backend service.")
        
        print("Construction Remarks System is available as part of the backend service.")
        print("Run the full project to access the complete construction remarks functionality via web interface.")
        return True
    except ImportError as e:
        print(f"Error importing construction remarks system: {e}")
        print("Make sure all dependencies are installed.")
        return False


def start_electron_app():
    """Start the Electron desktop application"""
    electron_path = Path(__file__).parent / "electron-app"
    if electron_path.exists():
        os.chdir(electron_path)
        try:
            subprocess.run(["npm", "start"], check=True)
            return True
        except FileNotFoundError:
            print("npm not found. Please install Node.js and npm to run the Electron application.")
            return False
        except subprocess.CalledProcessError:
            print("Failed to start Electron application. Make sure all dependencies are installed with 'npm install'.")
            return False
    else:
        print(f"Electron app directory not found: {electron_path}")
        return False

def show_help():
    """Show help information."""
    print("""
StrodService Project Manager
===========================

Usage: python main.py [command]

Commands:
    backend             - Start the Python FastAPI backend server
    doc-tracker         - Start the document tracking system
    construction-remarks - Start the construction remarks system
    electron            - Start the Electron desktop application
    full-project        - Start the complete StrodService project with full functionality
    help                - Show this help message
    
All modules are integrated into the full project backend, accessible via web interface.
    """)
    return True

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # Если нет аргументов, показываем справку
        return 0 if show_help() else 1

    command = sys.argv[1].lower()

    if command == "backend":
        return 0 if start_backend() else 1
    if command == "doc-tracker":
        return 0 if start_doc_tracking_system() else 1
    if command == "construction-remarks":
        return 0 if start_construction_remarks_system() else 1
    if command == "electron":
        return 0 if start_electron_app() else 1
    if command == "full-project":
        return 0 if start_full_project() else 1
    if command == "help":
        return 0 if show_help() else 1

    print(f"Unknown command: {command}. Use 'help' for available commands.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
