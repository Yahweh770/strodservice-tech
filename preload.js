const { contextBridge, ipcRenderer } = require('electron');

// Экспортируем безопасные методы для взаимодействия с основным процессом
contextBridge.exposeInMainWorld('electronAPI', {
  // Методы для взаимодействия с Python-бэкендом
  sendRequest: (method, endpoint, data) => 
    ipcRenderer.invoke('send-request', method, endpoint, data),
  
  // Методы для получения системной информации
  getSystemPath: (name) => ipcRenderer.invoke('get-system-path', name),
  
  // Методы для управления окном
  minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
  maximizeWindow: () => ipcRenderer.invoke('maximize-window'),
  closeWindow: () => ipcRenderer.invoke('close-window'),
});