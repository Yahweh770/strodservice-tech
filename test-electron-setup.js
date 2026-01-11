/**
 * Скрипт для проверки корректности настройки Electron-проекта
 */

const fs = require('fs');
const path = require('path');

console.log('Проверка корректности настройки Electron-проекта...\n');

// Проверяем наличие основных файлов
const requiredFiles = [
  'electron-main.js',
  'preload.js',
  'electron-builder-config.js',
  'package.json',
  'src/backend-python/main.py',
  'src/frontend/package.json'
];

let allFilesExist = true;

for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  const exists = fs.existsSync(filePath);
  
  if (exists) {
    console.log(`✓ ${file} - найден`);
  } else {
    console.log(`✗ ${file} - ОТСУТСТВУЕТ!`);
    allFilesExist = false;
  }
}

console.log('\nПроверка зависимостей в package.json...');

const packageJson = require('./package.json');
const requiredDeps = ['electron', 'axios'];
const requiredScripts = ['start-electron', 'dist-electron'];

let allDepsPresent = true;

for (const dep of requiredDeps) {
  if (packageJson.dependencies && packageJson.dependencies[dep]) {
    console.log(`✓ Зависимость ${dep} - присутствует`);
  } else if (packageJson.devDependencies && packageJson.devDependencies[dep]) {
    console.log(`✓ Зависимость ${dep} - присутствует (devDependencies)`);
  } else {
    console.log(`✗ Зависимость ${dep} - ОТСУТСТВУЕТ!`);
    allDepsPresent = false;
  }
}

console.log('\nПроверка скриптов в package.json...');

for (const script of requiredScripts) {
  if (packageJson.scripts && packageJson.scripts[script]) {
    console.log(`✓ Скрипт ${script} - определен`);
  } else {
    console.log(`✗ Скрипт ${script} - ОТСУТСТВУЕТ!`);
    allDepsPresent = false;
  }
}

console.log('\nПроверка структуры backend...');

const backendMain = path.join(__dirname, 'src/backend-python/main.py');
if (fs.existsSync(backendMain)) {
  const backendContent = fs.readFileSync(backendMain, 'utf8');
  if (backendContent.includes('FastAPI') && backendContent.includes('uvicorn')) {
    console.log('✓ Python backend корректно настроен с FastAPI');
  } else {
    console.log('✗ Python backend может быть некорректно настроен');
  }
} else {
  console.log('✗ Файл src/backend-python/main.py отсутствует');
}

console.log('\nПроверка структуры frontend...');

const frontendPackage = path.join(__dirname, 'src/frontend/package.json');
if (fs.existsSync(frontendPackage)) {
  const frontendJson = JSON.parse(fs.readFileSync(frontendPackage, 'utf8'));
  if (frontendJson.dependencies && frontendJson.dependencies.react) {
    console.log('✓ React frontend обнаружен');
  } else {
    console.log('? React не найден в зависимостях frontend');
  }
} else {
  console.log('✗ Файл src/frontend/package.json отсутствует');
}

console.log('\n' + '='.repeat(50));

if (allFilesExist && allDepsPresent) {
  console.log('✓ Проект корректно настроен для работы с Electron!');
  console.log('\nДля запуска приложения используйте:');
  console.log('  npm run start-electron');
  console.log('\nДля сборки приложения используйте:');
  console.log('  npm run dist-electron');
} else {
  console.log('✗ Проект настроен НЕКОРРЕКТНО. Требуется дополнительная настройка.');
}

console.log('='.repeat(50));