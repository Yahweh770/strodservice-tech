# StrodService - Full Project Build Instructions

## Overview
This project provides a comprehensive document tracking system and construction management platform for managing sent and received executive documentation in PTO (Project Technical Office), with additional features for construction remarks and GPR tracking.

## Building the Executable

### Prerequisites
- Python 3.8+

### Method 1: Using the Shell Script (Linux/macOS) or Batch File (Windows)
1. Make the script executable and run it (Linux/macOS):
   ```bash
   chmod +x build-pyinstaller.sh
   ./build-pyinstaller.sh
   ```
   
   Or double-click on `build-release.bat` (Windows)

2. The script will:
   - Install required Python dependencies
   - Install PyInstaller
   - Build the executable as `StrodService` (Linux/macOS) or `StrodService.exe` (Windows)
   - Place the executable in the `dist/` folder

### Method 2: Manual Build Process
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r src/backend-python/requirements.txt
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile --console --add-data "pto_docs.db;." --add-data "assets/icon.ico;assets" --add-data "src;src" --hidden-import=sqlite3 --hidden-import=sqlalchemy --hidden-import=fastapi --hidden-import=uvicorn --clean main.py -n StrodService
   ```

Note: On Linux/macOS systems, the executable will be named `StrodService` (without .exe extension), 
while on Windows it will be named `StrodService.exe`.

## Running the Application

### Direct Python Execution
```bash
python main.py full-project
```

### Using Different Modes
```bash
# Full project with web interface and all features
python main.py full-project

# Just the backend server
python main.py backend

# CLI document tracker only
python main.py doc-tracker
```

## Features
- Complete document tracking system with sending/receiving
- Web interface via FastAPI
- Construction remarks management
- GPR (General Production Records) tracking
- User authentication and permissions
- Real-time notifications via WebSockets
- Material stock management
- Work session tracking
- Multi-user support

## Database
The application uses SQLite database (`pto_docs.db`) to store all document information locally.