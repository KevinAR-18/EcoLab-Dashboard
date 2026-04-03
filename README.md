# EcoLab Dashboard - Smart Laboratory Management System

Dashboard EcoLab - Magang Lab Elektronika DTEDI 2025 X Tugas Akhir
**Author:** Stephanus Kevin Andika Rata

---

## 📋 Project Overview

EcoLab Dashboard adalah aplikasi **Smart Laboratory Management System** yang dibangun dengan **PySide6 (Qt)** dan **Firebase Authentication**. Aplikasi ini dirancang khusus untuk **Laboratorium EcoLab** DTEDI untuk memonitor dan mengontrol peralatan laboratorium secara real-time, termasuk Smart Socket, Smart Lamp, dan Smart AC Control.

### Key Features:
- ✅ **Firebase Authentication** (Email, Google Sign-In, Guest Mode)
- ✅ **Role-based Access Control** (User, Admin, Guest)
- ✅ **Session Management** dengan "Remember Me" (7 days expiry)
- ✅ **Admin Panel** untuk manajemen pengguna laboratorium
- ✅ **Smart Socket Control** untuk peralatan lab dengan MQTT scheduling
- ✅ **Smart Lamp Control** pencahayaan laboratorium
- ✅ **Smart AC Control** suhu ruangan laboratorium
- ✅ **Real-time Monitoring** dan kontrol peralatan lab IoT
- ✅ **Light Theme Enforcement** untuk konsistensi UI di Windows 11

---

## 🛠 Tech Stack

### Frontend:
- **PySide6** (Qt6) - GUI Framework
- **Python** 3.10+ (Recommended 3.12.5)

### Backend:
- **Firebase Authentication** - User authentication (Email, Google Sign-In)
- **Pyrebase4** - Firebase SDK for Python
- **MQTT** (paho-mqtt) - IoT communication protocol
- **Google Cloud Storage** - Config untuk Google Sign-Up/Sign-In

### Hardware:
- **ESP32C3** - Microcontroller untuk Smart Socket
- **Wemos D1 Mini** - Microcontroller untuk Smart Lamp dan Smart AC
- **MQTT** - Protokol komunikasi IoT untuk kontrol peralatan
- **IR (Infrared)** - Komunikasi untuk AC control

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
| **Guest** | View dashboard laboratorium only (no control) |
| **User** | Full dashboard features untuk kontrol peralatan lab (no admin panel) |
| **Admin** | Full dashboard + Admin Panel untuk manajemen user laboratorium |

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
│   ├── smartsocket_simulator.py      # Smart socket simulator untuk peralatan lab
│   ├── smartsocket2_simulator.py     # Socket 2 simulator
│   ├── smartsocket3_simulator.py     # Socket 3 simulator
│   ├── smartsocket4_simulator.py     # Socket 4 simulator
│   ├── smartsocket5_simulator.py     # Socket 5 simulator
│   ├── mcua_simulator.py             # MCU-A simulator
│   ├── mcub_simulator.py             # MCU-B simulator
│   ├── smartsocket.ino               # Arduino code untuk smart socket lab
│   ├── smartlampcontrol.ino          # Arduino code untuk smart lamp lab
│   └── smartaccontrol.ino            # Arduino code untuk smart AC lab
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

Folder `hardware_TA/` berisi program untuk microcontroller dan simulator peralatan laboratorium EcoLab:

### Arduino Programs (.ino):
1. **smartsocket.ino** - Smart Socket untuk kontrol peralatan lab dengan MQTT
2. **smartlampcontrol.ino** - Smart Lamp untuk pencahayaan lab dengan MQTT (*Developed with Ilham Purnomo*)
3. **smartaccontrol.ino** - Smart AC Control untuk suhu ruangan lab dengan IR (*Developed with Ilham Purnomo*)

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
- Kontrol ON/OFF peralatan lab
- Real-time status peralatan
- Schedule automation dengan MQTT
- Monitoring konsumsi daya
- 5 saluran socket independen untuk berbagai peralatan

### Smart Lamp Control:
- MQTT control untuk pencahayaan lab
- Kontrol kecerahan lampu
- Kontrol warna (RGB)
- On/Off control

### Smart AC Control:
- IR-based control untuk AC lab
- Kontrol suhu ruangan
- Pilihan mode (Cool, Heat, Fan, Dry)

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
Tugas Akhir - EcoLab Smart Laboratory

Laboratorium Elektronika DTEDI
Universitas Gadjah Mada

📧 Email: [kevinandika18@gmail.com](mailto:kevinandika18@gmail.com)

## 📄 License & Copyright

© 2025 **Stephanus Kevin Andika Rata**

This project is developed as part of **Magang Lab Elektronika DTEDI 2025** and **Final Project** at **Universitas Gadjah Mada**.

### Usage Terms:
- This project is for **educational and research purposes** only
- For academic and laboratory use at Laboratorium Elektronika DTEDI
- Please contact the author for any commercial usage or redistribution requests
