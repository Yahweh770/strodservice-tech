# StrodService - Release Notes

## Overview
StrodService is a comprehensive construction management platform that includes:
- Backend API server with FastAPI
- Document tracking system for PTO (Project Technical Documentation)
- Construction remarks management system
- GPR (General Production Records) management
- Multi-user support with authentication and authorization
- Real-time notifications via WebSockets

## Features
- **Document Tracking**: Complete system for tracking sent and returned executive documentation
- **Construction Remarks**: Management system for construction control remarks
- **GPR Management**: General production records management
- **User Management**: Multi-user support with roles and permissions
- **Real-time Updates**: WebSocket-based real-time notifications
- **File Management**: Secure file upload and management system

## Prerequisites
- Python 3.8 or higher
- Node.js 14.x or higher (for Electron applications)
- npm package manager

## Installation & Setup

### Quick Start
1. Install Python dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py full-project`

### Detailed Setup
1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Install Node.js dependencies for desktop app: `cd desktop-app && npm install`
4. Start the full project: `python main.py full-project`

## Building the Release

### Windows
Run the build script: `build-full-project.bat`

This will:
- Install all dependencies
- Build the backend executable
- Package the desktop application
- Create distribution files
- Generate startup scripts

### Linux/macOS
Run the build script: `bash build-full-project.sh`

## Running the Application

### Development Mode
```bash
# Start the backend server
python main.py backend

# Start the full project
python main.py full-project

# Start the document tracking system
python main.py doc-tracker

# Start the construction remarks system
python main.py construction-remarks
```

### Production Mode
After building, use the generated executables in the `dist/` folder:
- Run `start-server.bat` (Windows) or `./start-server.sh` (Linux/macOS)

## Configuration
The application uses environment variables for configuration:
- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: Secret key for JWT tokens
- `ADMIN_USERNAME`: Admin username (default: Yahweh)
- `ADMIN_PASSWORD`: Admin password (default: 90vopepi)

## Database
- Default: SQLite (`strod_service_main.db`)
- Supports PostgreSQL for multi-user environments
- Tables are auto-created on first run

## Security
- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- Input validation and sanitization

## Multi-user Support
- Up to 50 concurrent users supported
- Session management with configurable timeouts
- User permissions system
- Audit logging capabilities

## API Endpoints
Once running, visit http://localhost:8000 for the web interface
API documentation available at http://localhost:8000/docs

## Troubleshooting
- If you encounter database errors, ensure the database directory is writable
- For dependency issues, try clearing the cache and reinstalling
- Check logs in the server.log file for detailed error information

## Version Information
- Backend Framework: FastAPI 0.104.1
- Database ORM: SQLAlchemy 2.0.23
- Frontend: Built-in HTML/CSS/JS templates
- WebSocket Support: Real-time notifications

## Support
For support, please contact the development team or submit an issue through the official channels.