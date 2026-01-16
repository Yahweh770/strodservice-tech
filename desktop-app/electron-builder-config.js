/**
 * Конфигурационный файл для electron-builder
 */
module.exports = {
  appId: "com.strodservice.desktop",
  productName: "Строд-Сервис Технолоджи",
  directories: {
    output: "dist"
  },
  files: [
    "main.js",
    "index.html",
    "styles.css",
    "../src/frontend/dist/**/*", // assuming frontend build output is here
    "assets/**/*"
  ],
  win: {
    target: "nsis",
    icon: "assets/icon.ico"
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true
  }
};