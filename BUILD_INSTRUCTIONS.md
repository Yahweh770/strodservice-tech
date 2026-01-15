# Document Tracking System - Build Instructions

## Overview
This project provides a document tracking system for managing sent and received executive documentation in PTO (Project Technical Office).

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
   - Build the executable as `doc_tracking_system` (Linux/macOS) or `doc_tracking_system.exe` (Windows)
   - Place the executable in the `dist/` folder

### Method 2: Manual Build Process
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile --console --add-data "pto_docs.db;." --add-data "assets/icon.ico;assets" --hidden-import=sqlite3 --clean doc_tracking_system.py -n doc_tracking_system
   ```

Note: On Linux/macOS systems, the executable will be named `doc_tracking_system` (without .exe extension), 
while on Windows it will be named `doc_tracking_system.exe`.

## Running the Application

### Direct Python Execution
```bash
python doc_tracking_system.py
```

### Using the Main Entry Point
```bash
python main.py doc-tracker
```

## Features
- Add new documents with number, title, project number, etc.
- Track document shipments to recipients
- Record document returns with condition notes
- Search through all documents
- View complete document history

## Database
The application uses SQLite database (`pto_docs.db`) to store all document information locally.