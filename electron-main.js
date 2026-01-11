const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const axios = require('axios');

let mainWindow;
let pythonProcess;

// Запуск Python-сервера
function startPythonBackend() {
  const pythonPath = path.join(__dirname, 'src', 'backend-python');
  const mainPyPath = path.join(pythonPath, 'main.py');
  
  pythonProcess = spawn('python', [mainPyPath], {
    cwd: pythonPath,
    env: { ...process.env, PYTHONPATH: pythonPath }
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
}

// IPC обработчики для взаимодействия с рендер-процессом
ipcMain.handle('send-request', async (event, method, endpoint, data) => {
  try {
    // Подключаемся к Python-бэкенду, который должен быть запущен на порту 8000
    const response = await axios({
      method: method,
      url: `http://localhost:8000${endpoint}`,
      data: data,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error sending request to Python backend:', error.message);
    throw error;
  }
});

ipcMain.handle('get-system-path', (event, name) => {
  return app.getPath(name);
});

ipcMain.handle('minimize-window', () => {
  if (mainWindow) {
    mainWindow.minimize();
  }
});

ipcMain.handle('maximize-window', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  }
});

ipcMain.handle('close-window', () => {
  if (mainWindow) {
    mainWindow.close();
  }
});

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // Проверяем наличие собранного фронтенда
  const frontendBuildPath = path.join(__dirname, 'src', 'frontend', 'build', 'index.html');
  const fs = require('fs');
  
  if (fs.existsSync(frontendBuildPath)) {
    // Загружаем собранный React-приложение
    mainWindow.loadFile(frontendBuildPath);
  } else {
    // Если сборки нет, используем dev-сервер или локальный HTML
    mainWindow.loadURL('http://localhost:3000'); // Предполагаем, что запущен dev-сервер
  }

  mainWindow.setBackgroundColor('#f0f0f0');
  // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  startPythonBackend();
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  
  if (process.platform !== 'darwin') app.quit();
});