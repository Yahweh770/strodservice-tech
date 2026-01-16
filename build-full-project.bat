@echo off
setlocal enabledelayedexpansion

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Creating build directory...
if exist dist rmdir /s /q dist
mkdir dist

echo Building backend...
pyinstaller --onefile --add-data "src;src" --add-data "electron-app;electron-app" --add-data "desktop-app;desktop-app" --add-data "assets;assets" --hidden-import=fastapi.encoders --hidden-import=fastapi.openapi --hidden-import=fastapi.openapi.models --hidden-import=fastapi.openapi.utils --hidden-import=uvicorn.protocols.http.h11_impl --hidden-import=uvicorn.protocols.http.httptools_impl --hidden-import=uvicorn.protocols.websockets.websockets_impl --hidden-import=uvicorn.protocols.websockets.wsproto_impl --hidden-import=uvicorn.lifespan.on --hidden-import=uvicorn.lifespan.off --hidden-import=python-multipart --collect-all fastapi --collect-all uvicorn main.py -n strod-service-backend

echo Building desktop app...
cd desktop-app
pip install -r requirements.txt
pyinstaller --onefile --add-data "src;src" --add-data "assets;assets" --hidden-import=fastapi.encoders --hidden-import=fastapi.openapi --hidden-import=fastapi.openapi.models --hidden-import=fastapi.openapi.utils --hidden-import=uvicorn.protocols.http.h11_impl --hidden-import=uvicorn.protocols.http.httptools_impl --hidden-import=uvicorn.protocols.websockets.websockets_impl --hidden-import=uvicorn.protocols.websockets.wsproto_impl --hidden-import=uvicorn.lifespan.on --hidden-import=uvicorn.lifespan.off --hidden-import=python-multipart --collect-all fastapi --collect-all uvicorn desktop_main.py -n strod-service-desktop
cd ..

echo Building electron app frontend...
cd electron-app
npm install
npm run build
cd ..

echo Copying files to dist...
if not exist dist mkdir dist
copy /Y desktop-app\dist\strod-service-desktop.exe dist\
copy /Y dist\strod-service-backend.exe dist\
xcopy /E /I electron-app\dist electron-app\
xcopy /E /I src dist\src\
xcopy /E /I assets dist\assets\

echo Build completed successfully!
pause