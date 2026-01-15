module.exports = {
  appId: 'com.strodservice.desktop',
  productName: 'Строд-Сервис Технолоджи',
  copyright: 'Copyright © 2024 Строд-Сервис Технолоджи',
  company: 'Строд-Сервис Технолоджи',
  buildVersion: '1.0.0',
  directories: {
    output: 'release/dist'
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
    icon: 'assets/icon.ico',
    publisherName: 'Строд-Сервис Технолоджи'
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    installerIcon: 'assets/icon.ico',
    uninstallerIcon: 'assets/icon.ico',
    installerHeaderIcon: 'assets/icon.ico',
    createDesktopShortcut: true,
    createStartMenuShortcut: true,
    shortcutName: 'Строд-Сервис Технолоджи'
  }
};