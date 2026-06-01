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
  --add-data "images;images" ^
  --add-data "icon;icon" ^
  --hidden-import=PySide6.QtCore ^
  --hidden-import=PySide6.QtGui ^
  --hidden-import=PySide6.QtWidgets ^
  --hidden-import=PySide6.QtCharts ^
  --hidden-import=pyrebase ^
  --hidden-import=requests ^
  --hidden-import=google.oauth2.service_account ^
  --hidden-import=google_auth_oauthlib.flow ^
  --hidden-import=google.auth.transport.requests ^
  --hidden-import=loginmain ^
  --hidden-import=auth.session_manager ^
  --hidden-import=auth.auth_service ^
  --hidden-import=config.firebase_settings ^
  --hidden-import=config.path_utils ^
  --hidden-import=config.login_settings ^
  --hidden-import=ui.ui_theme_helper ^
  --hidden-import=app.setup.lamp_setup ^
  --hidden-import=app.setup.switch_setup ^
  --hidden-import=app.setup.ac_setup ^
  --hidden-import=app.setup.arrow_setup ^
  --hidden-import=dialogs.admin_window ^
  --hidden-import=dialogs.smartsocket_popup ^
  --hidden-import=app.setup.smartsocket_setup ^
  --hidden-import=services.smartsocket_recorder ^
  --hidden-import=services.smartsocket_settings_manager ^
  --hidden-import=ui.ui_loginpage ^
  --hidden-import=ui.ui_adminpanel ^
  --hidden-import=ui.ui_mainwindow ^
  --hidden-import=ui.ui_smartsocket_popup ^
  --hidden-import=ui.ui_functions ^
  --hidden-import=ui.ui_role_selection ^
  --hidden-import=resources_rc ^
  --hidden-import=widgets.lamp_button ^
  --hidden-import=backend.growatt_backend ^
  --hidden-import=backend.weathercloud_backend ^
  --hidden-import=backend.mqtt_client ^
  --hidden-import=backend.mqtt_dht22_backend ^
  --hidden-import=backend.lampbutton_backend ^
  --hidden-import=backend.acbutton_backend ^
  --hidden-import=backend.growatt_worker ^
  --hidden-import=backend.mcu_status_backend ^
  --hidden-import=backend.smartsocket_backend ^
  --collect-all=pyrebase ^
  --collect-all=google ^
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
