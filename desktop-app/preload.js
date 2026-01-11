// Preload script for Electron
// This script runs in a privileged context and can access Node.js APIs
// It serves as a bridge between the main process and renderer process

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Example API methods - add your specific methods here
  setTitle: (title) => ipcRenderer.invoke('set-title', title),
  getPath: (name) => ipcRenderer.invoke('get-path', name),
});