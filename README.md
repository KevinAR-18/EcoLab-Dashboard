# EcoLab Dashboard

EcoLab Dashboard is a PySide6 desktop application for monitoring and controlling smart laboratory devices in EcoLab. The application combines Firebase-based authentication, MQTT-based IoT communication, Growatt inverter monitoring, and WeatherCloud data in one dashboard.

## Main Features

- Firebase authentication with email/password, Google Sign-In, and guest mode
- Role-based access control for guest, user, and admin
- Persistent session handling with optional remember-me behavior
- Admin panel for user approval, role updates, account blocking, and password reset
- Smart Socket control with relay, timer, schedule, monitoring, recording, charting, and CSV export
- Smart Lamp and Smart AC control through MQTT
- Growatt inverter monitoring for power and energy flow
- Weather station monitoring from WeatherCloud
- Light-theme enforcement to avoid Windows 11 dark mode palette issues

## Runtime Requirements

- Python 3.10 or newer
- Dependencies from `requirements.txt`
- Local `credentials/` folder
- Local `.env` file next to the application entry point or next to the built `.exe`

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python launcher.py
```

## Environment Configuration

The active application reads runtime configuration from `.env`.

Minimal `.env` layout:

```env
ECOLAB_FIREBASE_API_KEY=
ECOLAB_FIREBASE_AUTH_DOMAIN=
ECOLAB_FIREBASE_DATABASE_URL=
ECOLAB_FIREBASE_PROJECT_ID=
ECOLAB_FIREBASE_STORAGE_BUCKET=
ECOLAB_FIREBASE_MESSAGING_SENDER_ID=
ECOLAB_FIREBASE_APP_ID=
ECOLAB_FIREBASE_SERVICE_ACCOUNT=

ECOLAB_MQTT_BROKER=
ECOLAB_MQTT_PORT=8883
ECOLAB_MQTT_USERNAME=
ECOLAB_MQTT_PASSWORD=
ECOLAB_MQTT_CA_CERT=credentials/ca.crt
ECOLAB_MQTT_USE_TLS=true

ECOLAB_GROWATT_USERNAME=
ECOLAB_GROWATT_PASSWORD=
```

Notes:

- `.env` is intentionally ignored by Git.
- `credentials/` is intentionally kept outside the bundled executable.
- The application expects `.env` and `credentials/` to be placed next to `EcoLab Dashboard.exe` after packaging.

## Project Structure

The current project structure after refactoring is:

```text
Aplikasi EcoLab -  New/
├─ launcher.py
├─ loginmain.py
├─ main.py
├─ create_admin.py
├─ README.md
├─ requirements.txt
├─ build.bat
├─ .env.example
├─ auth/
│  ├─ auth_service.py
│  └─ session_manager.py
├─ config/
│  ├─ firebase_settings.py
│  ├─ login_settings.py
│  └─ path_utils.py
├─ dialogs/
│  ├─ admin_window.py
│  └─ smartsocket_popup.py
├─ services/
│  ├─ smartsocket_recorder.py
│  └─ smartsocket_settings_manager.py
├─ app/
│  └─ setup/
│     ├─ ac_setup.py
│     ├─ arrow_setup.py
│     ├─ lamp_setup.py
│     ├─ smartsocket_setup.py
│     └─ switch_setup.py
├─ backend/
│  ├─ mqtt_client.py
│  ├─ mqtt_dht22_backend.py
│  ├─ mcu_status_backend.py
│  ├─ smartsocket_backend.py
│  ├─ lampbutton_backend.py
│  ├─ acbutton_backend.py
│  ├─ growatt_backend.py
│  ├─ growatt_worker.py
│  └─ weathercloud_backend.py
├─ widgets/
│  ├─ ac_button.py
│  ├─ flow_arrow.py
│  ├─ lamp_button.py
│  └─ switch_button.py
├─ ui/
│  ├─ ui_functions.py
│  ├─ ui_theme_helper.py
│  ├─ ui_loginpage.py
│  ├─ ui_mainwindow.py
│  ├─ ui_adminpanel.py
│  ├─ ui_role_selection.py
│  └─ ui_smartsocket_popup.py
├─ credentials/
├─ file ui/
├─ icon/
├─ images/
├─ hardware_TA/
└─ resources_rc.py
```

## Architecture Overview

### Entry Flow

- `launcher.py` is the main entry point.
- It loads any saved session through `auth/session_manager.py`.
- If a valid session exists, it opens the main dashboard.
- Otherwise, it opens `loginmain.py`.

### Authentication Layer

- `auth/auth_service.py` handles Firebase authentication and user records.
- `auth/session_manager.py` stores the local session file used by remember-me behavior.
- `create_admin.py` is a helper script for creating the first admin account manually.

### Main Application Layer

- `main.py` contains the main dashboard window and the top-level application orchestration.
- `loginmain.py` handles login, sign-up, forgot password, guest mode, and the admin/dash selection flow.
- `dialogs/admin_window.py` contains the admin panel.
- `dialogs/smartsocket_popup.py` contains the detailed Smart Socket control and monitoring popup.

### Setup Helpers

The `app/setup/` modules are thin UI wiring helpers:

- `lamp_setup.py` creates and connects custom lamp buttons
- `switch_setup.py` creates and connects Smart Socket switch buttons
- `ac_setup.py` creates and connects the custom AC button
- `arrow_setup.py` creates and stores flow arrows
- `smartsocket_setup.py` connects Smart Socket backend signals to the main window

### Backend Layer

The `backend/` folder contains service and integration modules:

- `mqtt_client.py` manages the shared MQTT connection
- `mqtt_dht22_backend.py` stores and filters DHT22 sensor messages
- `mcu_status_backend.py` tracks MCU online/offline state
- `smartsocket_backend.py` handles MQTT topics for all Smart Socket devices
- `lampbutton_backend.py` and `acbutton_backend.py` send control commands
- `growatt_backend.py` fetches inverter data
- `growatt_worker.py` runs Growatt fetches outside the UI thread
- `weathercloud_backend.py` fetches weather station data

### UI and Widget Layer

- `ui/` contains helper code plus generated Python modules from Qt Designer `.ui` files
- `widgets/` contains handwritten custom widgets used by the dashboard
- `resources_rc.py` contains the compiled Qt resource bindings

## Packaging

Use:

```bash
build.bat
```

What `build.bat` does:

- removes old `build/` and `dist/`
- runs PyInstaller with `launcher.py` as the build entry point
- copies local `.env` to `dist/.env`
- copies `credentials/` to `dist/credentials/`

Expected packaged layout:

```text
dist/
├─ EcoLab Dashboard.exe
├─ .env
└─ credentials/
   ├─ client_secret.json
   ├─ firebase_service_account.json
   ├─ ca.crt
   └─ ca2.crt
```

## Notes

- Generated Qt files in `ui/` are not the best place for manual comments because they may be regenerated.
- Several local-only folders are intentionally ignored by Git, such as `trialloginpage/`, `Unnecessary File/`, `PlantUML_Diagrams/`, and writing/experiment folders.
- Hardware simulators and firmware in `hardware_TA/` are kept for development and integration testing.

## Contact

**Stephanus Kevin Andika Rata**  
Magang Lab Elektronika DTEDI 2025  
Final Project / Tugas Akhir  
Universitas Gadjah Mada
