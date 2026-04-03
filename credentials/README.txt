╔══════════════════════════════════════════════════════════════════════════════╗
║                        CREDENTIALS FOLDER                                     ║
║                  Firebase & Google OAuth Credentials                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

📖 PANDUAN SETUP LENGKAP: Lihat file "SETUP_GUIDE.md" untuk panduan setup
                          Firebase dan Google Cloud untuk akun lab.

⚠️  SECURITY WARNING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Folder ini berisi file-file SENSITIF:
  • client_secret.json             - Google OAuth client secret
  • firebase_service_account.json  - Firebase admin credentials
  • ca.crt                         - MQTT TLS Certificate Authority

JANGAN:
  ❌ Commit ke Git / GitHub
  ❌ Bagikan ke orang lain
  ❌ Upload ke tempat publik
  ❌ Kirim via email/chat

FOLDER INI SUDAH DI-IGNORE DARI GIT (.gitignore)


📋 PENGGUNAAN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Secara otomatis, aplikasi akan mencari file-file ini di folder ini.
Jika Anda memindahkan file ke lokasi lain, set environment variable:

  Windows (Command Prompt):
  set TRIALLOGIN_FIREBASE_SERVICE_ACCOUNT=D:/path/to/firebase_service_account.json
  set MQTT_CA_CERT=D:/path/to/ca.crt

  Windows (PowerShell):
  $env:TRIALLOGIN_FIREBASE_SERVICE_ACCOUNT="D:/path/to/firebase_service_account.json"
  $env:MQTT_CA_CERT="D:/path/to/ca.crt"

  Linux/Mac:
  export TRIALLOGIN_FIREBASE_SERVICE_ACCOUNT=/path/to/firebase_service_account.json
  export MQTT_CA_CERT=/path/to/ca.crt


💡 TIPS UNTUK PC LAIN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cara termudah untuk setup di PC lain:

1. Copy folder "credentials/" ini ke PC lain
2. Paste di lokasi yang sama (sejajar dengan launcher.py)
3. Jalankan aplikasi

Atau simpan di Google Drive/Dropbox dan buat symlink ke folder ini.


🔗 UNTUK MENDAPATKAN CREDENTIALS BARU:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Client Secret (Google OAuth):
  1. Buka Google Cloud Console
  2. APIs & Services → Credentials
  3. Download OAuth 2.0 Client ID JSON

Firebase Service Account:
  1. Buka Firebase Console
  2. Project Settings → Service Accounts
  3. Click "Generate new private key"
  4. Download JSON file

CA Certificate (MQTT TLS):
  1. Copy dari Mosquitto installation: C:\Program Files\Mosquitto\certs\ca.crt
  2. Atau generate CA certificate sendiri untuk MQTT broker
  3. Letakkan di folder ini dengan nama "ca.crt"


📞 DUKUNGAN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Jika ada masalah dengan credentials:
  • Pastikan file tidak corrupt
  • Pastikan file ada di folder ini
  • Cek permission file
  • Cek Firebase/Google Cloud project masih aktif

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
