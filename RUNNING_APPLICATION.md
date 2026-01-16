# Running the StrodService Application

This document explains how to properly run the StrodService application with all its components.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Quick Start

### Method 1: Using the new start_app.py script (Recommended)

1. Install dependencies:
```bash
python start_app.py install
```

2. Choose one of the following options:
   - Start the document tracking system (CLI):
     ```bash
     python start_app.py doc-tracker
     ```
   
   - Start the backend server only:
     ```bash
     python start_app.py backend
     ```
   
   - Start the complete application:
     ```bash
     python start_app.py full-app
     ```

### Method 2: Using the original main.py script

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run specific components:
   - Document tracking system:
     ```bash
     python main.py doc-tracker
     ```
   
   - Backend server:
     ```bash
     python main.py backend
     ```
   
   - Full project:
     ```bash
     python main.py full-project
     ```

## Components Overview

### Document Tracking System
A CLI-based system for tracking sent and returned documents. Features include:
- Adding new documents
- Recording document shipments
- Tracking document returns
- Search functionality
- User management

### Backend Server (FastAPI)
A comprehensive web API with:
- Authentication and authorization
- Document management
- Construction remarks tracking
- File upload/download capabilities
- Real-time notifications via WebSockets
- Multi-user support

### Construction Remarks System
Integrated into the backend, tracks construction-related remarks and issues with:
- Status tracking
- Priority management
- Assignment capabilities
- Photo attachments
- History tracking

## Common Issues and Solutions

### 1. Import Errors
If you encounter import errors, make sure to:
- Install all dependencies with `pip install -r requirements.txt`
- Run the application from the project root directory
- Use the new `start_app.py` script which handles import paths properly

### 2. Database Connection Issues
The application uses SQLite by default. If you encounter database issues:
- Ensure the database file has proper read/write permissions
- Check that the database path is accessible

### 3. Port Already in Use
If the backend server fails to start due to port conflicts:
- Check if another process is using port 8000
- Kill the conflicting process or use a different port

## Configuration

The application can be configured using environment variables:

- `DATABASE_URL`: Database connection string (default: SQLite database)
- `SECRET_KEY`: Secret key for JWT tokens
- `ADMIN_USERNAME`: Admin username (default: admin)
- `ADMIN_PASSWORD`: Admin password (default: admin123)
- `MULTI_USER_MODE`: Enable multi-user mode (default: False)

## Development Mode

For development, you can enable auto-reload by modifying the startup scripts to include `reload=True` in the uvicorn.run() call.

## Troubleshooting

If the application fails to start:

1. Verify all dependencies are installed
2. Check that you're running from the correct directory (`/workspace`)
3. Ensure proper file permissions
4. Review the console output for specific error messages
5. Use the `start_app.py` script which includes better error handling

## Production Deployment

For production deployment:
- Set strong values for SECRET_KEY and admin credentials
- Use a production-ready database (PostgreSQL/MySQL)
- Configure proper logging
- Use a WSGI/ASGI server like Gunicorn
- Set MULTI_USER_MODE to True
- Configure HTTPS/TLS