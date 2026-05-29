@echo off
echo ========================================
echo Building EcoLab Dashboard...
echo ========================================
echo.

REM Clean old build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Cleaning old build files... done
echo.
echo NOTE: launcher.py is the build entry point.
echo       This build expects external .env and credentials/ next to the exe.
echo.

echo Building PyInstaller...
echo.

.venv\Scripts\pyinstaller ^
  --name "EcoLab Dashboard" ^
  --onefile ^
  --windowed ^
  --icon=icon\logoecolab.ico ^
  --add-data "icon;icon" ^
  --hidden-import=PySide6.QtCore ^
  --hidden-import=PySide6.QtGui ^
  --hidden-import=PySide6.QtWidgets ^
  --hidden-import=PySide6.QtCharts ^
  --hidden-import=google.oauth2.service_account ^
  --hidden-import=google_auth_oauthlib.flow ^
  --hidden-import=google.auth.transport.requests ^
  --exclude-module=PySide6.QtWebEngineCore ^
  --exclude-module=PySide6.QtWebEngineWidgets ^
  --exclude-module=PySide6.QtWebEngineQuick ^
  --exclude-module=PySide6.QtQuick ^
  --exclude-module=PySide6.QtQml ^
  --exclude-module=PySide6.Qt3DCore ^
  --exclude-module=PySide6.Qt3DRender ^
  --exclude-module=PySide6.Qt3DInput ^
  --exclude-module=PySide6.Qt3DLogic ^
  --exclude-module=PySide6.Qt3DAnimation ^
  --exclude-module=PySide6.QtMultimedia ^
  --exclude-module=PySide6.QtMultimediaWidgets ^
  --exclude-module=PySide6.QtPdf ^
  --exclude-module=PySide6.QtPdfWidgets ^
  --exclude-module=PySide6.QtDesigner ^
  --exclude-module=PySide6.QtHelp ^
  --exclude-module=PySide6.QtSql ^
  --exclude-module=PySide6.QtTest ^
  --exclude-module=PySide6.QtBluetooth ^
  --exclude-module=PySide6.QtPositioning ^
  --exclude-module=PySide6.QtSerialPort ^
  --exclude-module=PySide6.QtNetworkAuth ^
  --exclude-module=PySide6.QtVirtualKeyboard ^
  --exclude-module=bleak ^
  --exclude-module=winrt ^
  --exclude-module=gevent ^
  --exclude-module=greenlet ^
  --exclude-module=google.cloud ^
  --exclude-module=google.cloud.storage ^
  launcher.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERROR: PyInstaller build failed!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo Copying local runtime files to dist...

if exist .env (
    copy /Y .env "dist\.env" >nul
    echo   - Copied .env
) else (
    echo   - WARNING: .env not found, exe may fail at startup
)

if exist credentials (
    xcopy credentials "dist\credentials\" /E /I /Y >nul
    echo   - Copied credentials\
) else (
    echo   - WARNING: credentials\ folder not found
)

if exist icon (
    xcopy icon "dist\icon\" /E /I /Y >nul
    echo   - Copied icon\
) else (
    echo   - WARNING: icon\ folder not found
)

echo.
echo ========================================
echo PyInstaller build complete!
echo Output: dist\EcoLab Dashboard.exe
echo ========================================
echo.
echo Next steps:
echo 1. Verify dist\.env, dist\credentials\, and dist\icon\
echo 2. Test EcoLab Dashboard.exe
echo ========================================
pause
