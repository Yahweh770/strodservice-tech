# Document Tracking System - Build Instructions

## Overview
This project provides a document tracking system for managing sent and received executive documentation in PTO (Project Technical Office).

## Building the Executable

### Prerequisites
- Python 3.8+
- Windows OS (for the batch file method)

### Method 1: Using the Batch File (Windows)
1. Double-click on `build-release.bat`
2. The script will:
   - Install required Python dependencies
   - Install PyInstaller
   - Build the executable as `doc_tracking_system.exe`
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