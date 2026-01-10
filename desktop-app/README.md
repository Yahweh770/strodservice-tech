# Desktop Application for Строд-Сервис Технолоджи

This is an Electron-based desktop application that wraps the Строд-Сервис Технолоджи web application into a native Windows executable.

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager

## Installation and Setup

1. Navigate to the desktop app directory:
   ```bash
   cd /workspace/desktop-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the frontend React application (if not already built):
   ```bash
   cd ../strodservice-tech/frontend
   npm install
   npm run build
   ```

4. Return to the desktop app directory:
   ```bash
   cd ../../desktop-app
   ```

## Running in Development Mode

```bash
npm start
```

## Building the Executable

To create a Windows executable (.exe):

```bash
npm run dist
```

The executable will be created in the `dist/` folder.

## Project Structure

- `main.js` - Main Electron process file
- `preload.js` - Security bridge between main and renderer processes
- `index.html` - Main application window HTML
- `styles.css` - Styling for the application
- `package.json` - Project configuration and build settings
- `assets/` - Application icons and other assets

## Notes

- Make sure the React frontend is built before attempting to package the Electron app
- The build process creates a standalone executable that does not require Node.js to run
- The application includes a menu with File and View options for better desktop integration