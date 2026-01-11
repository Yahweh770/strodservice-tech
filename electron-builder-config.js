module.exports = {
  appId: 'com.strodservice.desktop',
  productName: 'Строд-Сервис Технолоджи',
  directories: {
    output: 'dist'
  },
  files: [
    'electron-main.js',
    'preload.js',
    'src/frontend/build/**/*',
    'src/backend-python/**/*',
    '!node_modules',
    '!src/frontend/node_modules',
    '!src/backend-python/__pycache__',
    '!src/backend-python/*.log'
  ],
  extraResources: [
    {
      from: 'src/backend-python/',
      to: 'backend-python/',
      filter: ['**/*', '!__pycache__', '!*.log']
    }
  ],
  win: {
    target: 'nsis',
    icon: 'assets/icon.ico' || 'src/frontend/public/favicon.ico'
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true
  }
};