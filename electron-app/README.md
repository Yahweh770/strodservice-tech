# Electron Application

This is a simple Electron application that demonstrates how to create a desktop application with HTML, CSS, and JavaScript.

## Project Structure

```
electron-app/
├── package.json
├── main.js
├── index.html
├── style.css
└── README.md
```

## Files Description

- **package.json**: Contains project metadata and dependencies
- **main.js**: Main process file for Electron
- **index.html**: Application UI
- **style.css**: Application styling

## How to Build

To build this application into an executable:

1. Install dependencies:
```bash
npm install
```

2. Build for Windows:
```bash
npm run build
```

This will create a distributable executable in the `dist/` folder that can run on Windows systems without additional dependencies.

## Key Features

- Cross-platform desktop application
- Uses native OS capabilities
- Bundled as standalone executable
- No external dependencies required for end users

## Development

To run the application during development:
```bash
npm start
```

This will launch the Electron application with hot reloading capabilities.