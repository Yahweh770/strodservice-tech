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
    },
    {
      from: 'src/frontend/build/',
      to: 'frontend-build/'
    }
  ],
  win: {
    target: 'nsis',
    icon: 'assets/icon.ico'
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true
  }
};