# EcoLab Dashboard - Smart Laboratory Management System

Dashboard EcoLab - Magang Lab Elektronika DTEDI 2025 x Tugas Akhir  
**Author:** Stephanus Kevin Andika Rata

---

## Gambaran Proyek

EcoLab Dashboard adalah aplikasi **Smart Laboratory Management System** berbasis **PySide6 (Qt)** dan **Firebase Authentication** untuk memonitor dan mengontrol perangkat laboratorium secara real-time.

Perangkat yang saat ini didukung:
- **EcoLab Power Monitoring (Growatt)**
- **Smart Socket**
- **Smart Lamp**
- **Smart AC Control**
- **Weather Station Monitoring**
- **Monitoring sensor dan status perangkat laboratorium**

---

## Fitur Utama

- **Firebase Authentication**: email/password, Google Sign-In, dan Guest Mode
- **Role-based Access Control**: guest, user, dan admin
- **Session Management**: dukungan "Remember Me"
- **Admin Panel**: manajemen akun pengguna laboratorium
- **Smart Socket Control**: relay, timer, schedule, dan monitoring energi
- **Smart Socket Recording**: simpan data monitoring ke memori aplikasi
- **Smart Socket Export**: export data per socket ke CSV
- **Smart Socket Graph**: grafik monitoring per socket di popup kontrol
- **EcoLab Power Monitoring**: monitoring data inverter Growatt pada page 1
- **Weather Station Monitoring**: monitoring data cuaca laboratorium
- **Smart Lamp Control**
- **Smart AC Control**
- **Windows 11 Dark Mode Handling**: light theme enforcement untuk widget penting

---

## Teknologi yang Digunakan

### Frontend
- **PySide6** (Qt6)
- **Python** 3.10+
- **PySide6.QtCharts** untuk grafik Smart Socket

### Backend / Services
- **Firebase Authentication**
- **Pyrebase4**
- **MQTT** (`paho-mqtt`) untuk komunikasi perangkat IoT
- **Growatt data integration** untuk monitoring inverter/page 1
- **Weather data integration** untuk monitoring Weather Station
- **Google Cloud / OAuth config** untuk login Google

### Hardware
- **Growatt Inverter** untuk EcoLab Power Monitoring
- **ESP32-C3** untuk Smart Socket
- **Wemos D1 Mini** untuk Smart Lamp dan Smart AC
- **PZEM-004T v3.0** untuk monitoring energi Smart Socket
- **DS1302 RTC** untuk timer/schedule Smart Socket

---

## Instalasi

### Kebutuhan Awal

```bash
Python 3.10 or higher
```

### Install dependensi

```bash
pip install -r requirements.txt
```

### Setup Firebase

1. Buat project di Firebase Console.
2. Enable Authentication untuk Email/Password dan Google Sign-In.
3. Setup Firebase Realtime Database jika diperlukan oleh konfigurasi project.
4. Buat file `credentials/firebase_config.json`.

Contoh:

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

## Penggunaan

### Menjalankan aplikasi

```bash
python launcher.py
```

### Opsi autentikasi

1. **Email Login**  
   Masuk dengan email dan password.
2. **Google Sign-In**  
   Login dengan akun Google.
3. **Guest Mode**  
   Akses read-only tanpa kontrol perangkat.

### Peran pengguna

| Role | Access |
|------|--------|
| **Guest** | Monitoring only, tanpa kontrol perangkat |
| **User** | Kontrol perangkat dan akses dashboard utama |
| **Admin** | Semua fitur user + admin panel |

---

## Update Smart Socket

Fitur Smart Socket saat ini mencakup:

- Kontrol relay ON/OFF per socket
- Timer per socket
- Schedule start/stop dengan mode **daily** dan **onetime**
- Monitoring **Voltage, Current, Power, Energy, Frequency, PF**
- Popup kontrol dengan tab **Control**, **Data**, dan **Graph**
- Recording data monitoring per socket
- Interval recording yang bisa diatur manual dari popup
- Opsi **Follow Schedule** untuk otomatis mulai recording saat schedule aktif
- **Autosave CSV** saat recording berbasis schedule selesai
- Export CSV per socket
- Grafik per socket dengan pilihan metric
- Refresh tabel dan grafik hanya saat recording aktif

Catatan implementasi:
- Smart Socket simulator Python sudah diselaraskan dengan konsep firmware terbaru.
- Firmware `smartsocket2.ino` sampai `smartsocket5.ino` sudah dibuat dari basis `smartsocket.ino` dengan topic MQTT yang disesuaikan.

---

## Struktur Proyek

Struktur proyek saat ini setelah refactor adalah:

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

## Gambaran Arsitektur

### Alur Masuk

- `launcher.py` adalah entry point utama aplikasi.
- File ini memuat session yang tersimpan melalui `auth/session_manager.py`.
- Jika session valid, aplikasi langsung membuka dashboard utama.
- Jika tidak ada session valid, aplikasi membuka `loginmain.py`.

### Lapisan Autentikasi

- `auth/auth_service.py` menangani autentikasi Firebase dan data user.
- `auth/session_manager.py` menyimpan file session lokal untuk fitur remember me.
- `create_admin.py` adalah script helper untuk membuat akun admin pertama secara manual.

### Lapisan Aplikasi Utama

- `main.py` berisi window dashboard utama dan orkestrasi aplikasi tingkat atas.
- `loginmain.py` menangani login, sign-up, lupa password, guest mode, dan alur pemilihan admin/dashboard.
- `dialogs/admin_window.py` berisi panel admin.
- `dialogs/smartsocket_popup.py` berisi popup kontrol dan monitoring Smart Socket yang lebih detail.

### Helper Setup

Modul `app/setup/` adalah helper tipis untuk wiring UI:

- `lamp_setup.py` membuat dan menghubungkan custom lamp button.
- `switch_setup.py` membuat dan menghubungkan tombol Smart Socket.
- `ac_setup.py` membuat dan menghubungkan custom AC button.
- `arrow_setup.py` membuat dan menyimpan flow arrow.
- `smartsocket_setup.py` menghubungkan signal backend Smart Socket ke main window.

### Lapisan Backend

Folder `backend/` berisi modul service dan integrasi:

- `mqtt_client.py` mengelola koneksi MQTT bersama.
- `mqtt_dht22_backend.py` menyimpan dan memfilter pesan sensor DHT22.
- `mcu_status_backend.py` melacak status online/offline MCU.
- `smartsocket_backend.py` menangani topic MQTT untuk semua device Smart Socket.
- `lampbutton_backend.py` dan `acbutton_backend.py` mengirim command kontrol.
- `growatt_backend.py` mengambil data inverter.
- `growatt_worker.py` menjalankan pengambilan data Growatt di luar UI thread.
- `weathercloud_backend.py` mengambil data weather station.

### Lapisan UI dan Widget

- `ui/` berisi helper code serta modul Python hasil generate dari file `.ui` Qt Designer.
- `widgets/` berisi custom widget buatan manual yang dipakai di dashboard.
- `resources_rc.py` berisi binding Qt resource yang sudah dikompilasi.

---

## Hardware TA

Folder `hardware_TA/` berisi firmware dan simulator yang digunakan untuk pengembangan serta pengujian integrasi perangkat laboratorium.

### Arduino / firmware

1. **smartsocket.ino** - Firmware Smart Socket 1 berbasis MQTT
2. **smartsocket2.ino** - Firmware Smart Socket 2 berbasis MQTT
3. **smartsocket3.ino** - Firmware Smart Socket 3 berbasis MQTT
4. **smartsocket4.ino** - Firmware Smart Socket 4 berbasis MQTT
5. **smartsocket5.ino** - Firmware Smart Socket 5 berbasis MQTT
6. **smartlampcontrol.ino** - Firmware Smart Lamp
7. **smartaccontrol.ino** - Firmware Smart AC Control

### Python simulators

1. **smartsocket_simulator.py** - Simulator Smart Socket 1
2. **smartsocket2_simulator.py** - Simulator Smart Socket 2
3. **smartsocket3_simulator.py** - Simulator Smart Socket 3
4. **smartsocket4_simulator.py** - Simulator Smart Socket 4
5. **smartsocket5_simulator.py** - Simulator Smart Socket 5
6. **mcua_simulator.py** - Simulator MCU-A
7. **mcub_simulator.py** - Simulator MCU-B

### Contoh menjalankan simulator

```bash
cd hardware_TA
python smartsocket_simulator.py
```

---

## Detail Fitur

### Manajemen session

- Simpan sesi login
- Dukungan remember me
- Auto login jika sesi masih valid
- Logout dari aplikasi

### Panel admin

- Lihat daftar user
- Approve akun
- Update role user/admin
- Block/unblock akun
- Update password user non-Google
- Delete akun

### Smart Socket

- Monitoring status perangkat
- Kontrol relay
- Timer countdown
- Schedule otomatis
- Monitoring energi real-time
- Data recording, export CSV, dan grafik

### Smart Lamp

- Kontrol lampu laboratorium
- MQTT-based switching
- Mendukung kontrol beberapa kanal lampu di page control room
- Dikembangkan bersama **Ilham Purnomo**

### Smart AC

- Kontrol AC berbasis IR
- Mode pendingin dan fan
- Pengaturan suhu
- Dikembangkan bersama **Ilham Purnomo**

### EcoLab Power Monitoring

- Menampilkan data **Growatt inverter** pada page 1
- Ringkasan dan live monitoring daya EcoLab
- Menjadi halaman utama monitoring energi laboratorium

### Weather Station Monitoring

- Menampilkan data cuaca/stasiun cuaca laboratorium
- Monitoring sensor lingkungan pada dashboard
- Terintegrasi ke halaman monitoring untuk pemantauan kondisi sekitar

---

## Alur Autentikasi

```text
launcher.py -> check session
  |- valid session -> open dashboard
  |- no session -> open login window
       |- email/password -> Firebase -> save session -> dashboard
       |- Google sign-in -> OAuth -> save session -> dashboard
       |- guest mode -> temp session -> dashboard (limited)
```

---

## Catatan

- Gunakan `launcher.py` sebagai entry point utama aplikasi.
- File session lokal dibuat otomatis saat login berhasil.
- File credential Firebase tidak di-include di repo.
- Beberapa widget penting sudah dipaksa ke light theme untuk menghindari masalah warna teks di Windows 11 dark mode.
- Firmware Smart Socket MQTT sekarang tidak lagi menyimpan isi sertifikat CA langsung di file `.ino`.

---

## Kontak

**Stephanus Kevin Andika Rata**  
Magang Lab Elektronika DTEDI 2025  
Tugas Akhir - EcoLab Smart Laboratory  
Laboratorium Elektronika DTEDI  
Universitas Gadjah Mada

Email: [kevinandika18@gmail.com](mailto:kevinandika18@gmail.com)

---

## Lisensi & Hak Cipta

Copyright 2025 **Stephanus Kevin Andika Rata**

Project ini dikembangkan sebagai bagian dari:
- **Magang Lab Elektronika DTEDI 2025**
- **Final Project / Tugas Akhir**
- **Universitas Gadjah Mada**

Ketentuan penggunaan:
- Untuk keperluan edukasi dan penelitian
- Untuk penggunaan laboratorium dan akademik
- Hubungi author untuk kebutuhan komersial atau redistribusi
