const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Building Electron application...');

// Check if node_modules exists
if (!fs.existsSync('./node_modules')) {
  console.log('Installing dependencies...');
  exec('npm install', (error, stdout, stderr) => {
    if (error) {
      console.error(`Installation error: ${error}`);
      return;
    }
    
    console.log('Dependencies installed successfully.');
    buildApp();
  });
} else {
  console.log('Dependencies already installed.');
  buildApp();
}

function buildApp() {
  console.log('Starting build process...');
  
  // Create dist directory if it doesn't exist
  if (!fs.existsSync('./dist')) {
    fs.mkdirSync('./dist', { recursive: true });
  }
  
  // Run electron-builder
  const buildProcess = exec('npx electron-builder --win --config ./electron-builder-config.js');
  
  buildProcess.stdout.on('data', (data) => {
    console.log(data);
  });
  
  buildProcess.stderr.on('data', (data) => {
    console.error(data);
  });
  
  buildProcess.on('close', (code) => {
    if (code === 0) {
      console.log('Build completed successfully!');
      console.log('Check the dist/ folder for your executable.');
    } else {
      console.error(`Build failed with code ${code}`);
    }
  });
}

// Create electron-builder config if it doesn't exist
const configPath = './electron-builder-config.js';
if (!fs.existsSync(configPath)) {
  const configContent = `module.exports = {
  appId: 'com.example.electron-app',
  productName: 'Electron App',
  copyright: 'Copyright © 2026',
  directories: {
    output: 'dist'
  },
  files: [
    'main.js',
    'index.html',
    'style.css',
    'package.json'
  ],
  win: {
    target: 'nsis',
    icon: 'icon.ico' // Optional: Add an icon file
  }
};`;
  
  fs.writeFileSync(configPath, configContent);
  console.log('Created electron-builder configuration file.');
}