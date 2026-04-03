# 🔐 CREDENTIALS SETUP GUIDE

**Panduan Setup Firebase & Google Cloud untuk Akun Lab**

---

## 📋 DAFTAR ISI

1. [Struktur Folder](#struktur-folder)
2. [File yang Dibutuhkan](#file-yang-dibutuhkan)
3. [Setup Google Cloud Console](#setup-google-cloud-console)
4. [Setup Firebase Console](#setup-firebase-console)
5. [Replace File Credentials](#replace-file-credentials)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## 📁 STRUKTUR FOLDER

```
credentials/
├── ca.crt                          # MQTT TLS Certificate (jangan dihapus)
├── ca2.crt                         # MQTT TLS Certificate backup (jangan dihapus)
├── client_secret.json              # Google OAuth Client Secret (GANTI)
├── firebase_service_account.json   # Firebase Admin Credentials (GANTI)
├── README.txt                      # Penjelasan singkat
└── SETUP_GUIDE.md                  # File ini (panduan lengkap)
```

---

## 📝 FILE YANG DIBUTUHKAN

### **1. `client_secret.json` (Google OAuth)**

**Kegunaan:** Untuk fitur **Google Sign In** di login page

**Diambil dari:** Google Cloud Console

**Format:**
```json
{
  "web": {
    "client_id": "123456789-abc...apps.googleusercontent.com",
    "client_secret": "GOCSPX-...",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
  }
}
```

---

### **2. `firebase_service_account.json` (Firebase Admin)**

**Kegunaan:** Untuk **Firebase Authentication** (user management)

**Diambil dari:** Firebase Console

**Format:**
```json
{
  "type": "service_account",
  "project_id": "ecolab-lab",
  "private_key_id": "1...9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-...@ecolab-lab.iam.gserviceaccount.com",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

---

## 🔵 SETUP GOOGLE CONSOLE CLIENT SECRET

### **A. Buat Project Baru**

1. Buka: https://console.cloud.google.com/
2. Login dengan akun lab
3. Klik dropdown project → **"NEW PROJECT"**
4. Isi:
   - **Project name:** `EcoLab-Lab`
   - **Location:** No organization
5. Klik **"CREATE"**
6. Tunggu project dibuat (± 1 menit)

---

### **B. Enable Google+ API**

1. Di sidebar, menu: **APIs & Services → Library**
2. Search: `"Google+ API"`
3. Klik hasil pencarian
4. Klik **"ENABLE"**

---

### **C. Buat OAuth 2.0 Client ID**

1. Menu: **APIs & Services → Credentials**
2. Klik **"+ CREATE CREDENTIALS"**
3. Pilih: **"OAuth client ID"**
4. Jika diminta configure consent screen:
   - Klik "Configure consent screen"
   - User Type: **External**
   - Klik "Create"
   - Isi:
     - App name: `EcoLab Dashboard`
     - User support email: email lab
     - Developer contact: email lab
   - Klik "Save and Continue" (3x)
5. Kembali ke Create OAuth client ID:
   - **Application type:** Web application
   - **Name:** `EcoLab Web Client`

6. **Authorized JavaScript origins:**
   ```
   http://localhost
   http://127.0.0.1
   ```

7. **Authorized redirect URIs:**
   ```
   http://localhost
   http://127.0.0.1
   ```
   (atau biarkan kosong)

8. Klik **"CREATE"**
9. **DOWNLOAD** file JSON (klik tombol download 📥)
10. Rename file jadi: **`client_secret.json`**

---

## 🔴 SETUP FIREBASE SERVICE ACCOUNT

### **A. Buat Project Baru**

1. Buka: https://console.firebase.google.com/
2. Login dengan akun lab (sama dengan Google Cloud)
3. Klik **"Add project"**
4. Isi:
   - **Project name:** `EcoLab-Lab` (sama dengan Google Cloud)
5. (Opsional) Disable/Enable Google Analytics
6. Klik **"Create project"**
7. Tunggu project dibuat (± 1 menit)
8. Klik **"Continue"**

---

### **B. Link Firebase ke Google Cloud**

**PENTING:** Firebase dan Google Cloud harus ter-link!

1. Di Firebase Console, klik ⚙️ **Settings** (gear icon)
2. Pilih **"Project settings"**
3. Tab **"General"**
4. Scroll ke bawah, cari: **"Your apps"**
5. Di bagian **"Advanced"**, klik: **"Link to Google Cloud"**
6. Pilih Google Cloud project: `EcoLab-Lab`
7. Klik **"Link"**
8. Konfirmasi dengan klik **"Link"** lagi

---

### **C. Enable Authentication**

1. Menu: **Build → Authentication**
2. Klik **"Get Started"**
3. Tab **"Sign-in method"**
4. Enable **Email/Password:**
   - Toggle: **ON**
   - Klik **"Save"**
5. (Opsional) Enable **Google:**
   - Toggle: **ON**
   - Masukkan project ID dari Google Cloud
   - Klik **"Save"**

---

### **D. Generate Service Account Private Key**

1. Masih di **Project Settings**
2. Tab **"Service Accounts"**
3. Scroll ke bawah, cari: **"Firebase Admin SDK"**
4. Klik **"Generate new private key"**
5. Pastikan pilihan: **JSON**
6. Klik **"Generate"**
7. File akan terdownload otomatis
8. Rename file jadi: **`firebase_service_account.json`**

---

## 🔄 REPLACE FILE CREDENTIALS

Setelah mendapatkan 2 file dari atas:

### **Langkah 1: Backup File Lama**

```bash
# Masuk ke folder credentials
cd "D:\#File Kuliah TRIK\Semester 7 - Eco Lab\Aplikasi EcoLab -  New\credentials"

# Rename file lama
rename client_secret.json client_secret.json.old
rename firebase_service_account.json firebase_service_account.json.old
```

### **Langkah 2: Copy File Baru**

1. Copy `client_secret.json` dari Google Cloud Console
2. Paste ke folder `credentials/`
3. Copy `firebase_service_account.json` dari Firebase Console
4. Paste ke folder `credentials/`

### **Struktur Akhir:**

```
credentials/
├── ca.crt                          # ← TETAP (jangan dihapus)
├── ca2.crt                         # ← TETAP (jangan dihapus)
├── client_secret.json              # ← GANTI (file baru)
├── client_secret.json.old          # ← Backup lama
├── firebase_service_account.json   # ← GANTI (file baru)
├── firebase_service_account.json.old # ← Backup lama
├── README.txt
└── SETUP_GUIDE.md
```

---

## 🧪 TESTING

### **1. Test Login dengan Email/Password**

1. Buka Firebase Console
2. Menu: **Build → Authentication → Users**
3. Klik **"Add user"**
4. Isi:
   - **Email:** `test@lab.com`
   - **Password:** `Test123456`
   - Klik **"Add user"**
5. Jalankan aplikasi: `python launcher.py`
6. Coba login dengan email & password di atas

---

### **2. Test Google Sign In**

1. Pastikan sudah login di browser dengan akun lab
2. Jalankan aplikasi: `python launcher.py`
3. Di login page, klik **"Sign in with Google"**
4. Pilih akun Google lab
5. Jika berhasil, akan masuk ke dashboard

---

### **3. Test Simulator MQTT**

1. Cek file simulator (misal `smartsocket_simulator.py`)
2. Pastikan CA_CERT path mengarah ke file yang benar:
   ```python
   CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")
   # Atau gunakan ca2.crt:
   # CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca2.crt")
   ```
3. Jalankan simulator:
   ```bash
   cd hardware_TA/
   python smartsocket_simulator.py
   ```
4. Pastikan koneksi MQTT berhasil

---

## 🔧 TROUBLESHOOTING

### **Masalah 1: Google Sign In Error**

**Error:** `redirect_uri_mismatch` atau `unauthorized_client`

**Solusi:**
1. Cek Google Cloud Console
2. APIs & Services → Credentials
3. Edit OAuth 2.0 Client ID
4. Pastikan Authorized JavaScript origins:
   ```
   http://localhost
   http://127.0.0.1
   ```

---

### **Masalah 2: Firebase Auth Error**

**Error:** `Failed to get document` atau `Permission denied`

**Solusi:**
1. Pastikan `firebase_service_account.json` benar
2. Cek apakah file corrupt (buka dengan text editor)
3. Pastikan project ID di Firebase sama dengan di Google Cloud
4. Re-download service account key dari Firebase Console

---

### **Masalah 3: MQTT TLS Error**

**Error:** `handshake failure` atau `certificate verify failed`

**Solusi:**
1. Pastikan file `ca.crt` atau `ca2.crt` ada di folder credentials
2. Cek path di simulator:
   ```python
   # Untuk file di hardware_TA/
   CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")

   # Untuk file di root (main.py)
   MQTT_CA_CERT = os.path.join(os.path.dirname(__file__), "credentials", "ca.crt")
   ```
3. Jika masih error, coba ganti ke `ca2.crt`:
   ```python
   CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca2.crt")
   ```

---

### **Masalah 4: User Tidak Bisa Login**

**Error:** `INVALID_LOGIN_CREDENTIALS`

**Solusi:**
1. Buka Firebase Console
2. Build → Authentication → Users
3. Pastikan user sudah ada
4. Jika belum, klik **"Add user"**
5. Atau reset password user yang ada

---

## ⚠️ SECURITY NOTES

### **JANGAN:**
- ❌ Commit file `client_secret.json` ke Git
- ❌ Commit file `firebase_service_account.json` ke Git
- ❌ Bagikan ke orang lain
- ❌ Upload ke tempat publik (GitHub, GitLab, dll)
- ❌ Kirim via email/chat

### **BOLEH:**
- ✅ Simpan di Google Drive lab (private)
- ✅ Simpan di penyimpanan cloud lab (private)
- ✅ Share ke tim lab secara langsung (manual copy)

### **Folder ini SUDAH DI-IGNORE dari Git (.gitignore)**

---

## 📞 BANTUAN

Jika ada masalah:

1. **Cek log error** di console/terminal
2. **Baca error message** dengan teliti
3. **Cek file credentials:**
   - Pastikan file tidak corrupt
   - Pastikan file ada di folder yang benar
   - Pastikan nama file benar (case-sensitive)

---

## 📚 REFERENSI

- [Google Cloud Console](https://console.cloud.google.com/)
- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Authentication Docs](https://firebase.google.com/docs/auth)
- [Google OAuth 2.0 Docs](https://developers.google.com/identity/protocols/oauth2)

---

**Dibuat untuk:** EcoLab Dashboard Application
**Versi:** 1.0
**Terakhir diupdate:** 2026-04-03
