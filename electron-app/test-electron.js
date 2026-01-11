// Simple test to verify Electron app structure
const fs = require('fs');
const path = require('path');

const requiredFiles = ['package.json', 'main.js', 'index.html', 'style.css'];
let allFilesExist = true;

console.log('Checking Electron app structure...\n');

for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  const exists = fs.existsSync(filePath);
  
  if (exists) {
    console.log(`✓ ${file} - EXISTS`);
  } else {
    console.log(`✗ ${file} - MISSING`);
    allFilesExist = false;
  }
}

console.log('\nChecking package.json content...');
const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
const hasMainProperty = !!packageJson.main;
const hasScripts = !!packageJson.scripts;
const hasElectronDeps = packageJson.devDependencies && 
                       (packageJson.devDependencies.electron || packageJson.dependencies.electron);

console.log(hasMainProperty ? '✓ main property in package.json' : '✗ main property missing in package.json');
console.log(hasScripts ? '✓ scripts in package.json' : '✗ scripts missing in package.json');
console.log(hasElectronDeps ? '✓ Electron dependencies found' : '✗ Electron dependencies missing');

console.log('\nChecking main.js content...');
const mainJsContent = fs.readFileSync(path.join(__dirname, 'main.js'), 'utf8');
const hasBrowserWindow = mainJsContent.includes('BrowserWindow');
const hasLoadFile = mainJsContent.includes('loadFile');

console.log(hasBrowserWindow ? '✓ BrowserWindow import found' : '✗ BrowserWindow import missing');
console.log(hasLoadFile ? '✓ loadFile method found' : '✗ loadFile method missing');

console.log('\nChecking index.html...');
const indexHtmlContent = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const hasTitle = indexHtmlContent.includes('<title>');
const hasLinkStyle = indexHtmlContent.includes('style.css');

console.log(hasTitle ? '✓ Title element found' : '✗ Title element missing');
console.log(hasLinkStyle ? '✓ CSS link found' : '✗ CSS link missing');

if (allFilesExist && hasMainProperty && hasScripts && hasElectronDeps && hasBrowserWindow && hasLoadFile && hasTitle && hasLinkStyle) {
  console.log('\n🎉 All checks passed! The Electron app structure is complete and valid.');
  console.log('\nTo build the app:');
  console.log('1. Make sure you have enough system resources');
  console.log('2. Run: npm run build');
  console.log('3. Find the executable in the dist/ folder');
} else {
  console.log('\n❌ Some checks failed. Please review the missing components.');
}