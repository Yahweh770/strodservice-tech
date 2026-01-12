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

  // Определяем путь к собранному фронтенду
  // В режиме разработки используем dev-сервер, в продакшене - сборку
  const frontendBuildPath = path.join(__dirname, 'src', 'frontend', 'build', 'index.html');
  const fs = require('fs');
  
  // Если приложение запущено из собранного дистрибутива, __dirname будет в папке resources/app
  // В этом случае нужно использовать другой путь к файлам
  const appPath = path.dirname(require.main.filename);
  const packagedFrontendPath = path.join(appPath, '..', 'resources', 'app', 'src', 'frontend', 'build', 'index.html');
  
  if (fs.existsSync(frontendBuildPath)) {
    // Загружаем собранный React-приложение из стандартного пути
    mainWindow.loadFile(frontendBuildPath);
  } else if (fs.existsSync(packagedFrontendPath)) {
    // Загружаем собранный React-приложение из пути в упакованном приложении
    mainWindow.loadFile(packagedFrontendPath);
  } else {
    // Если сборки нет, проверяем, запущен ли dev-сервер
    // Иначе показываем сообщение об ошибке
    checkDevServer()
      .then(() => {
        mainWindow.loadURL('http://localhost:3000');
      })
      .catch(() => {
        // Показываем простую HTML-страницу с сообщением об ошибке
        mainWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(`
          <!DOCTYPE html>
          <html>
            <head>
              <title>Ошибка загрузки приложения</title>
              <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .error { color: #d32f2f; }
              </style>
            </head>
            <body>
              <h1 class="error">Ошибка загрузки фронтенда</h1>
              <p>Фронтенд-приложение не найдено. Пожалуйста, убедитесь, что выполнена сборка React-приложения.</p>
              <p>Выполните команду: npm run build-frontend</p>
            </body>
          </html>
        `)}`);
      });
  }

  mainWindow.setBackgroundColor('#f0f0f0');
  // mainWindow.webContents.openDevTools();
}

// Функция для проверки доступности dev-сервера
async function checkDevServer() {
  return new Promise((resolve, reject) => {
    const http = require('http');
    const options = {
      host: 'localhost',
      port: 3000,
      timeout: 5000,
      path: '/'
    };

    const request = http.request(options, (res) => {
      if (res.statusCode === 200) {
        resolve();
      } else {
        reject(new Error(`Dev server responded with status ${res.statusCode}`));
      }
    });

    request.on('error', (err) => {
      reject(err);
    });

    request.end();
  });
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