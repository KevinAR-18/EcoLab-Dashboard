# EcoLab Dashboard - IoT Smart Home Application

Dashboard EcoLab - Magang Lab Elektronika DTEDI 2025 X Tugas Akhir
**Author:** Stephanus Kevin Andika Rata

---

## 📋 Project Overview

EcoLab Dashboard adalah aplikasi IoT Smart Home yang dibangun dengan **PySide6 (Qt)** dan **Firebase Authentication**. Aplikasi ini memungkinkan pengguna untuk memonitor dan mengontrol perangkat smart home secara real-time, termasuk Smart Socket, Smart Lamp, dan Smart AC Control.

### Key Features:
- ✅ **Firebase Authentication** (Email, Google Sign-In, Guest Mode)
- ✅ **Role-based Access Control** (User, Admin, Guest)
- ✅ **Session Management** dengan "Remember Me" (7 days expiry)
- ✅ **Admin Panel** untuk manajemen pengguna
- ✅ **Smart Socket Control** dengan MQTT scheduling
- ✅ **Smart Lamp Control**
- ✅ **Smart AC Control**
- ✅ **Real-time Monitoring** dan kontrol perangkat IoT
- ✅ **Light Theme Enforcement** untuk konsistensi UI di Windows 11

---

## 🛠 Tech Stack

### Frontend:
- **PySide6** (Qt6) - GUI Framework
- **Python** 3.10+

### Backend:
- **Firebase Authentication** - User authentication
- **Pyrebase4** - Firebase SDK for Python
- **MQTT** (paho-mqtt) - IoT communication protocol
- **Google Cloud Storage** - File storage

### Hardware:
- **Arduino/ESP8266** - Microcontroller programs
- **BLE (Bluetooth Low Energy)** - Device communication

---

## 🚀 Installation

### Prerequisites:
```bash
Python 3.10 or higher
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Firebase Setup:
1. Buat project Firebase di [Firebase Console](https://console.firebase.google.com/)
2. Enable Authentication (Email/Password, Google Sign-In)
3. Setup Firebase Realtime Database
4. Buat `credentials/firebase_config.json` dengan konfigurasi Firebase Anda:

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

---

## 🎯 Usage

### Start Application:
```bash
python launcher.py
```

### Authentication Options:

#### 1. **Email Login**
- Masukkan email dan password
- Checkbox "Remember Me" untuk menyimpan sesi 7 hari

#### 2. **Google Sign-In**
- Login dengan akun Google
- Tidak perlu password terpisah

#### 3. **Guest Mode**
- Akses tanpa registrasi/login
- Fitur terbatas (read-only)

### User Roles:

| Role | Features |
|------|----------|
| **Guest** | View dashboard only (no control) |
| **User** | Full dashboard features (no admin panel) |
| **Admin** | Full dashboard + Admin Panel access |

---

## 📁 Project Structure

```
Aplikasi EcoLab - New/
├── launcher.py                  # ⭐ Entry point application
├── loginmain.py                 # Login window with Google/Guest support
├── main.py                      # Main dashboard
├── auth_service.py              # Firebase authentication service
├── session_manager.py           # Session management (7 days expiry)
├── admin_window.py              # Admin panel for user management
├── smartsocket_popup.py         # Smart socket control popup
├── ui_theme_helper.py           # Light theme enforcement
│
├── ui/                          # UI components (Qt Designer)
│   ├── ui_loginpage.py
│   ├── ui_mainwindow.py
│   ├── ui_adminpanel.py
│   └── ...
│
├── hardware_TA/                 # 🔌 Hardware Tugas Akhir programs
│   ├── smartsocket_simulator.py      # Smart socket simulator
│   ├── smartsocket2_simulator.py     # Socket 2 simulator
│   ├── smartsocket3_simulator.py     # Socket 3 simulator
│   ├── smartsocket4_simulator.py     # Socket 4 simulator
│   ├── smartsocket5_simulator.py     # Socket 5 simulator
│   ├── mcua_simulator.py             # MCU-A simulator
│   ├── mcub_simulator.py             # MCU-B simulator
│   ├── smartsocketversi2.ino         # Arduino code for smart socket
│   ├── smartlampcontrol.ino          # Arduino code for smart lamp
│   └── smartaccontrol.ino            # Arduino code for smart AC
│
├── backend/                     # Backend services
├── credentials/                 # Firebase credentials (not in repo)
├── file ui/                     # UI files
├── widgets/                     # Custom widgets
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── ecolab_session.json          # Session storage (auto-generated)
```

---

## 🔌 Hardware TA - Arduino Programs

Folder `hardware_TA/` berisi program untuk microcontroller dan simulator:

### Arduino Programs (.ino):
1. **smartsocketversi2.ino** - Smart Socket dengan MQTT
2. **smartlampcontrol.ino** - Smart Lamp dengan BLE
3. **smartaccontrol.ino** - Smart AC Control dengan IR

### Python Simulators:
1. **smartsocket_simulator.py** - Simulasi Smart Socket 1
2. **smartsocket2_simulator.py** - Simulasi Smart Socket 2
3. **smartsocket3_simulator.py** - Simulasi Smart Socket 3
4. **smartsocket4_simulator.py** - Simulasi Smart Socket 4
5. **smartsocket5_simulator.py** - Simulasi Smart Socket 5
6. **mcua_simulator.py** - Simulasi MCU-A
7. **mcub_simulator.py** - Simulasi MCU-B

### Run Simulator:
```bash
cd hardware_TA
python smartsocket_simulator.py
```

---

## 🎨 Features in Detail

### Session Management:
- Auto-save sesi setelah login
- 7 days expiry (configurable)
- "Remember Me" checkbox
- Auto-login on app start
- Logout from settings page

### Admin Panel:
- User management (CRUD)
- Role assignment (user/admin)
- View all users
- Update user roles
- Delete users

### Smart Socket Control:
- On/Off control
- Real-time status
- Schedule automation (MQTT)
- Power consumption monitoring
- 5 independent socket channels

### Smart Lamp Control:
- BLE connectivity
- Brightness control
- Color control (RGB)
- On/Off control

### Smart AC Control:
- IR-based control
- Temperature control
- Mode selection (Cool, Heat, Fan, Dry)
- Timer scheduling

---

## 🔐 Authentication Flow

```
launcher.py → Check Session
    │
    ├─ Valid Session → Open Dashboard
    │
    └─ No Session → Show Login Window
                     │
                     ├─ Email/Password → Firebase → Save Session → Dashboard
                     ├─ Google Sign-In → OAuth → Save Session → Dashboard
                     └─ Guest Mode → Create Temp Session → Dashboard (limited)
```

---

## 🐛 Known Issues

- **Windows 11 Dark Mode**: Text color inversion on some widgets
  **Solution**: Global light theme enforcement di `ui_theme_helper.py`

---

## 📝 Notes

- **Entry Point**: Selalu gunakan `launcher.py` untuk menjalankan aplikasi
- **Session Storage**: `ecolab_session.json` (auto-generated)
- **Firebase Credentials**: Tidak di-include di repo (security reasons)
- **Theme**: Light theme di-enforce untuk menghindari color inversion di Windows 11

---

## 📞 Contact

**Stephanus Kevin Andika Rata**
Magang Lab Elektronika DTEDI 2025
Tugas Akhir - EcoLab Dashboard

---

## 📄 License

This project is part of Tugas Akhir for Magang Lab Elektronika DTEDI 2025
