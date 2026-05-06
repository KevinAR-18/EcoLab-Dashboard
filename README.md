# EcoLab Dashboard - Smart Laboratory Management System

EcoLab Dashboard - DTEDI Electronics Laboratory Internship 2025 x Final Project  
**Author:** Stephanus Kevin Andika Rata

---

## Project Overview

EcoLab Dashboard is a **Smart Laboratory Management System** desktop application built with **PySide6 (Qt)** and **Firebase Authentication** to monitor and control laboratory devices in real time.

The system currently supports:
- **EcoLab Power Monitoring (Growatt)**
- **Smart Socket**
- **Smart Lamp**
- **Smart AC Control**
- **Weather Station Monitoring**
- **Laboratory sensor and device status monitoring**

---

## Main Features

- **Firebase Authentication**: email/password, Google Sign-In, and Guest Mode
- **Role-based Access Control**: guest, user, and admin
- **Session Management**: remember-me support
- **Admin Panel**: laboratory user account management
- **Smart Socket Control**: relay, timer, schedule, and energy monitoring
- **Smart Socket Recording**: store monitoring data in application memory
- **Smart Socket Export**: export per-socket data to CSV
- **Smart Socket Graph**: per-socket monitoring charts inside the control popup
- **EcoLab Power Monitoring**: Growatt inverter monitoring on page 1
- **Weather Station Monitoring**: laboratory weather data monitoring
- **Smart Lamp Control**
- **Smart AC Control**
- **Windows 11 Dark Mode Handling**: light theme enforcement for key widgets

---

## Technology Stack

### Frontend
- **PySide6** (Qt6)
- **Python** 3.10+
- **PySide6.QtCharts** for Smart Socket charts

### Backend / Services
- **Firebase Authentication**
- **Pyrebase4**
- **MQTT** (`paho-mqtt`) for IoT device communication
- **Growatt data integration** for inverter monitoring
- **Weather data integration** for Weather Station monitoring
- **Google Cloud / OAuth config** for Google login

### Hardware
- **Growatt Inverter** for EcoLab Power Monitoring
- **ESP32-C3** for Smart Socket
- **Wemos D1 Mini** for Smart Lamp and Smart AC
- **PZEM-004T v3.0** for Smart Socket energy monitoring
- **DS1302 RTC** for Smart Socket timer and schedule

---

## Installation

### Prerequisites

```bash
Python 3.10 or higher
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Runtime configuration

The application needs three external setup areas:

1. Firebase web configuration in `.env`
2. Google OAuth client credential in `credentials/client_secret.json`
3. MQTT TLS certificate in `credentials/ca.crt` or `credentials/ca2.crt`

See [credentials/README.md](credentials/README.md) for the detailed credential guide.

### Firebase setup

1. Create or open the EcoLab project in Firebase Console.
2. Enable Authentication for Email/Password.
3. Enable Google Sign-In in Firebase Authentication if you want Google login.
4. Copy the Firebase web app values into the root `.env` file.
5. Generate a service account key and place it in `credentials/firebase_service_account.json`.

Example Firebase web config values:

```json
{
  "apiKey": "YOUR_API_KEY",
  "authDomain": "YOUR_PROJECT.firebaseapp.com",
  "databaseURL": "https://YOUR_PROJECT.firebaseio.com",
  "projectId": "YOUR_PROJECT_ID",
  "storageBucket": "YOUR_PROJECT.appspot.com",
  "messagingSenderId": "YOUR_SENDER_ID",
  "appId": "YOUR_APP_ID"
}
```

Required `.env` keys:

```env
ECOLAB_FIREBASE_API_KEY=
ECOLAB_FIREBASE_AUTH_DOMAIN=
ECOLAB_FIREBASE_DATABASE_URL=
ECOLAB_FIREBASE_PROJECT_ID=
ECOLAB_FIREBASE_STORAGE_BUCKET=
ECOLAB_FIREBASE_MESSAGING_SENDER_ID=
ECOLAB_FIREBASE_APP_ID=
ECOLAB_FIREBASE_SERVICE_ACCOUNT=
```

Notes:

- Leave `ECOLAB_FIREBASE_SERVICE_ACCOUNT` empty if you use `credentials/firebase_service_account.json`.
- Fill `ECOLAB_FIREBASE_SERVICE_ACCOUNT` only if the service account file is stored somewhere else.

### Google OAuth setup

Google Sign-In does not use only Firebase settings. It also needs a Google OAuth client JSON file.

Prepare:

- `credentials/client_secret.json`

Steps:

1. Open Google Cloud Console.
2. Select the same Google Cloud project linked to EcoLab.
3. Go to `APIs & Services` -> `Credentials`.
4. Create or open the OAuth client used by the app.
5. Download the client JSON.
6. Rename it to `client_secret.json`.
7. Place it inside the `credentials/` folder.

If Google Sign-In fails, the first thing to verify is whether `credentials/client_secret.json` matches the active Google Cloud project.

### MQTT TLS setup

MQTT communication for the IoT devices uses TLS and requires a CA certificate file.

Prepare:

- `credentials/ca.crt` as the default CA certificate
- `credentials/ca2.crt` as an optional backup CA certificate for some simulator or broker setups

Required `.env` keys:

```env
ECOLAB_MQTT_BROKER=
ECOLAB_MQTT_PORT=8883
ECOLAB_MQTT_USERNAME=
ECOLAB_MQTT_PASSWORD=
ECOLAB_MQTT_CA_CERT=credentials/ca.crt
ECOLAB_MQTT_USE_TLS=true
```

What to prepare for MQTT TLS:

1. MQTT broker hostname or IP
2. MQTT username and password
3. TLS-enabled MQTT port, usually `8883`
4. CA certificate file, usually `credentials/ca.crt`
5. Fallback CA certificate if your simulator or broker setup uses `ca2.crt`

Notes:

- `main.py` defaults to `credentials/ca.crt` when `ECOLAB_MQTT_CA_CERT` is not overridden.
- Some simulator files in `hardware_TA/` still point to `ca2.crt`, so keep both certificate files available unless you are standardizing them.
- Do not embed certificate contents directly into the firmware.

### Minimum files checklist

Before running the app, make sure these files exist:

```text
.env
credentials/client_secret.json
credentials/firebase_service_account.json
credentials/ca.crt
```

Optional but recommended:

```text
credentials/ca2.crt
```

---

## Usage

### Run the application

```bash
python launcher.py
```

### Authentication options

1. **Email Login**  
   Sign in with email and password.
2. **Google Sign-In**  
   Sign in with a Google account.
3. **Guest Mode**  
   Read-only access without device control.

### User roles

| Role | Access |
|------|--------|
| **Guest** | Monitoring only, without device control |
| **User** | Device control and main dashboard access |
| **Admin** | All user features plus the admin panel |

---

## Smart Socket Updates

The current Smart Socket feature set includes:

- Per-socket relay ON/OFF control
- Per-socket timer
- Start/stop schedules with **daily** and **onetime** modes
- Monitoring for **Voltage, Current, Power, Energy, Frequency, PF**
- Control popup with **Control**, **Data**, and **Graph** tabs
- Per-socket monitoring data recording
- Configurable recording interval from the popup
- **Follow Schedule** option to automatically start recording when a schedule becomes active
- **Autosave CSV** when schedule-based recording ends
- Per-socket CSV export
- Per-socket charts with selectable metrics
- Table and chart refresh only while recording is active

Implementation notes:
- The Python Smart Socket simulator has been aligned with the latest firmware concept.
- Firmware files from `smartsocket2.ino` to `smartsocket5.ino` were derived from `smartsocket.ino` with adjusted MQTT topics.

---

## Project Structure

The current project structure after refactoring is:

```text
Aplikasi EcoLab -  New/
|-- launcher.py
|-- loginmain.py
|-- main.py
|-- create_admin.py
|-- README.md
|-- requirements.txt
|-- build.bat
|-- .env.example
|-- auth/
|   |-- auth_service.py
|   `-- session_manager.py
|-- config/
|   |-- firebase_settings.py
|   |-- login_settings.py
|   `-- path_utils.py
|-- dialogs/
|   |-- admin_window.py
|   `-- smartsocket_popup.py
|-- services/
|   |-- smartsocket_recorder.py
|   `-- smartsocket_settings_manager.py
|-- app/
|   `-- setup/
|       |-- ac_setup.py
|       |-- arrow_setup.py
|       |-- lamp_setup.py
|       |-- smartsocket_setup.py
|       `-- switch_setup.py
|-- backend/
|   |-- mqtt_client.py
|   |-- mqtt_dht22_backend.py
|   |-- mcu_status_backend.py
|   |-- smartsocket_backend.py
|   |-- lampbutton_backend.py
|   |-- acbutton_backend.py
|   |-- growatt_backend.py
|   |-- growatt_worker.py
|   `-- weathercloud_backend.py
|-- widgets/
|   |-- ac_button.py
|   |-- flow_arrow.py
|   |-- lamp_button.py
|   `-- switch_button.py
|-- ui/
|   |-- ui_functions.py
|   |-- ui_theme_helper.py
|   |-- ui_loginpage.py
|   |-- ui_mainwindow.py
|   |-- ui_adminpanel.py
|   |-- ui_role_selection.py
|   `-- ui_smartsocket_popup.py
|-- credentials/
|-- file ui/
|-- icon/
|-- images/
|-- hardware_TA/
`-- resources_rc.py
```

---

## Architecture Overview

### Entry Flow

- `launcher.py` is the main application entry point.
- It loads any saved session through `auth/session_manager.py`.
- If a valid session exists, it opens the main dashboard.
- Otherwise, it opens `loginmain.py`.

### Authentication Layer

- `auth/auth_service.py` handles Firebase authentication and user records.
- `auth/session_manager.py` stores the local session file used by remember-me behavior.
- `create_admin.py` is a helper script for manually creating the first admin account.

### Main Application Layer

- `main.py` contains the main dashboard window and top-level application orchestration.
- `loginmain.py` handles login, sign-up, forgot password, guest mode, and the admin/dashboard selection flow.
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

- `ui/` contains helper code and generated Python modules from Qt Designer `.ui` files
- `widgets/` contains handwritten custom widgets used by the dashboard
- `resources_rc.py` contains the compiled Qt resource bindings

---

## Hardware TA

The `hardware_TA/` folder contains firmware and simulators used for development and device integration testing.

### Arduino / firmware

1. **smartsocket.ino** - Smart Socket 1 firmware based on MQTT
2. **smartsocket2.ino** - Smart Socket 2 firmware based on MQTT
3. **smartsocket3.ino** - Smart Socket 3 firmware based on MQTT
4. **smartsocket4.ino** - Smart Socket 4 firmware based on MQTT
5. **smartsocket5.ino** - Smart Socket 5 firmware based on MQTT
6. **smartlampcontrol.ino** - Smart Lamp firmware
7. **smartaccontrol.ino** - Smart AC Control firmware

### Python simulators

1. **smartsocket_simulator.py** - Smart Socket 1 simulator
2. **smartsocket2_simulator.py** - Smart Socket 2 simulator
3. **smartsocket3_simulator.py** - Smart Socket 3 simulator
4. **smartsocket4_simulator.py** - Smart Socket 4 simulator
5. **smartsocket5_simulator.py** - Smart Socket 5 simulator
6. **mcua_simulator.py** - MCU-A simulator
7. **mcub_simulator.py** - MCU-B simulator

### Example: run a simulator

```bash
cd hardware_TA
python smartsocket_simulator.py
```

---

## Feature Details

### Session management

- Save login sessions
- Remember-me support
- Auto-login when the session is still valid
- Application logout

### Admin panel

- View user list
- Approve accounts
- Update user/admin roles
- Block/unblock accounts
- Update passwords for non-Google users
- Delete accounts

### Smart Socket

- Device status monitoring
- Relay control
- Countdown timer
- Automatic scheduling
- Real-time energy monitoring
- Data recording, CSV export, and charts

### Smart Lamp

- Laboratory lamp control
- MQTT-based switching
- Supports multiple lamp channels in the control room page
- Developed together with **Ilham Purnomo**

### Smart AC

- IR-based AC control
- Cooling and fan modes
- Temperature settings
- Developed together with **Ilham Purnomo**

### EcoLab Power Monitoring

- Displays **Growatt inverter** data on page 1
- EcoLab power summary and live monitoring
- Serves as the main laboratory energy monitoring page

### Weather Station Monitoring

- Displays laboratory weather station data
- Environmental sensor monitoring on the dashboard
- Integrated into the monitoring page for surrounding condition tracking

---

## Authentication Flow

```text
launcher.py -> check session
  |- valid session -> open dashboard
  |- no session -> open login window
       |- email/password -> Firebase -> save session -> dashboard
       |- Google sign-in -> OAuth -> save session -> dashboard
       |- guest mode -> temp session -> dashboard (limited)
```

---

## Notes

- Use `launcher.py` as the main application entry point.
- The local session file is created automatically after a successful login.
- Firebase credential files are not included in the repository.
- Several key widgets are forced into a light theme to avoid text color issues on Windows 11 dark mode.
- Smart Socket MQTT firmware no longer stores the CA certificate contents directly inside the `.ino` files.

---

## Contact

**Stephanus Kevin Andika Rata**  
DTEDI Electronics Laboratory Internship 2025  
Final Project - EcoLab Smart Laboratory  
DTEDI Electronics Laboratory  
Universitas Gadjah Mada

Email: [kevinandika18@gmail.com](mailto:kevinandika18@gmail.com)

---

## License & Copyright

Copyright 2025 **Stephanus Kevin Andika Rata**

This project is developed as part of:
- **DTEDI Electronics Laboratory Internship 2025**
- **Final Project / Tugas Akhir**
- **Universitas Gadjah Mada**

Usage terms:
- For educational and research purposes
- For laboratory and academic usage
- Contact the author for commercial or redistribution requests
