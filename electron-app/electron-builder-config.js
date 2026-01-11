module.exports = {
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
};