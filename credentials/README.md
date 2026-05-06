# Credentials Guide

This folder stores local credentials used by the EcoLab application.

Do not commit or share these files.

## Files in this folder

| File | Required | Purpose |
| --- | --- | --- |
| `client_secret.json` | Yes | Google OAuth client for "Sign in with Google" |
| `firebase_service_account.json` | Yes | Firebase Admin SDK credential |
| `ca.crt` | Usually yes | Default CA certificate for MQTT TLS |
| `ca2.crt` | Optional fallback | Backup CA certificate used by some simulator files |

## Important notes

- The app reads `client_secret.json` from `credentials/client_secret.json`.
- The app reads `firebase_service_account.json` from `credentials/firebase_service_account.json`.
- The app reads MQTT CA certificate from `.env`, usually `ECOLAB_MQTT_CA_CERT=credentials/ca.crt`.
- You can override the Firebase Admin credential path with `ECOLAB_FIREBASE_SERVICE_ACCOUNT`.

---

## English

### 1. What you need

Prepare these two JSON files:

1. `client_secret.json`
2. `firebase_service_account.json`

You should also keep `ca.crt` and `ca2.crt` in this folder unless you intentionally replace the MQTT certificate.

### 2. Folder layout

Keep this structure:

```text
credentials/
|-- client_secret.json
|-- firebase_service_account.json
|-- ca.crt
|-- ca2.crt
`-- README.md
```

### 3. How to get `client_secret.json`

1. Open `https://console.cloud.google.com/`.
2. Select the correct Google Cloud project for EcoLab.
3. Go to `APIs & Services` -> `Credentials`.
4. Create or open an `OAuth client ID`.
5. Download the JSON file.
6. Rename it to `client_secret.json`.
7. Put it in this `credentials/` folder.

Recommended OAuth settings:

- Application type: `Desktop app` or the type already used by your lab setup
- If your setup uses web redirect flow, keep the existing redirect/origin values from the current project configuration

### 4. How to get `firebase_service_account.json`

1. Open `https://console.firebase.google.com/`.
2. Select the EcoLab Firebase project.
3. Open `Project settings` -> `Service Accounts`.
4. Click `Generate new private key`.
5. Download the JSON file.
6. Rename it to `firebase_service_account.json`.
7. Put it in this `credentials/` folder.

### 5. Check `.env`

This project also requires Firebase and MQTT values in the root `.env` file.

Minimum related keys:

```env
ECOLAB_FIREBASE_API_KEY=
ECOLAB_FIREBASE_AUTH_DOMAIN=
ECOLAB_FIREBASE_DATABASE_URL=
ECOLAB_FIREBASE_PROJECT_ID=
ECOLAB_FIREBASE_STORAGE_BUCKET=
ECOLAB_FIREBASE_MESSAGING_SENDER_ID=
ECOLAB_FIREBASE_APP_ID=
ECOLAB_FIREBASE_SERVICE_ACCOUNT=
ECOLAB_MQTT_CA_CERT=credentials/ca.crt
```

Notes:

- Leave `ECOLAB_FIREBASE_SERVICE_ACCOUNT` empty if you use `credentials/firebase_service_account.json`.
- Set `ECOLAB_FIREBASE_SERVICE_ACCOUNT` only if the service account file is stored somewhere else.
- Change `ECOLAB_MQTT_CA_CERT` to `credentials/ca2.crt` only if your MQTT setup requires it.

### 6. Quick verification

1. Make sure the two JSON files exist in this folder.
2. Make sure the root `.env` file is filled.
3. Run:

```powershell
python launcher.py
```

4. Test email/password login.
5. Test Google Sign-In if enabled for the project.

### 7. Troubleshooting

`Google sign-in fails`

- Re-check `client_secret.json`.
- Re-download the OAuth client JSON from Google Cloud.
- Make sure the file name is exactly `client_secret.json`.

`Firebase auth/admin access fails`

- Re-check `firebase_service_account.json`.
- Make sure the Firebase project matches the `.env` Firebase values.
- If using a custom path, verify `ECOLAB_FIREBASE_SERVICE_ACCOUNT`.

`MQTT TLS fails`

- Verify `ECOLAB_MQTT_CA_CERT` in `.env`.
- Try `credentials/ca.crt` first.
- If your simulator or broker uses the backup certificate, switch to `credentials/ca2.crt`.

### 8. Security

- Never upload these credentials to GitHub or public storage.
- Never send them in public chat or email.
- Share them only through your lab's private storage or direct local transfer.

---

## Bahasa Indonesia

### 1. File yang dibutuhkan

Siapkan dua file JSON berikut:

1. `client_secret.json`
2. `firebase_service_account.json`

File `ca.crt` dan `ca2.crt` juga sebaiknya tetap ada di folder ini kecuali memang mau diganti untuk konfigurasi MQTT.

### 2. Struktur folder

Pastikan susunannya seperti ini:

```text
credentials/
|-- client_secret.json
|-- firebase_service_account.json
|-- ca.crt
|-- ca2.crt
`-- README.md
```

### 3. Cara mendapatkan `client_secret.json`

1. Buka `https://console.cloud.google.com/`.
2. Pilih project Google Cloud yang dipakai EcoLab.
3. Masuk ke `APIs & Services` -> `Credentials`.
4. Buat atau buka `OAuth client ID`.
5. Download file JSON.
6. Ubah namanya menjadi `client_secret.json`.
7. Simpan ke folder `credentials/` ini.

Saran konfigurasi OAuth:

- Tipe aplikasi: `Desktop app` atau tipe yang memang sudah dipakai setup lab
- Kalau project Anda memakai redirect/origin web, pertahankan konfigurasi yang sudah aktif di project tersebut

### 4. Cara mendapatkan `firebase_service_account.json`

1. Buka `https://console.firebase.google.com/`.
2. Pilih project Firebase EcoLab.
3. Buka `Project settings` -> `Service Accounts`.
4. Klik `Generate new private key`.
5. Download file JSON.
6. Ubah namanya menjadi `firebase_service_account.json`.
7. Simpan ke folder `credentials/` ini.

### 5. Cek file `.env`

Project ini juga butuh nilai Firebase dan MQTT di file `.env` pada root project.

Minimal bagian yang terkait:

```env
ECOLAB_FIREBASE_API_KEY=
ECOLAB_FIREBASE_AUTH_DOMAIN=
ECOLAB_FIREBASE_DATABASE_URL=
ECOLAB_FIREBASE_PROJECT_ID=
ECOLAB_FIREBASE_STORAGE_BUCKET=
ECOLAB_FIREBASE_MESSAGING_SENDER_ID=
ECOLAB_FIREBASE_APP_ID=
ECOLAB_FIREBASE_SERVICE_ACCOUNT=
ECOLAB_MQTT_CA_CERT=credentials/ca.crt
```

Catatan:

- Biarkan `ECOLAB_FIREBASE_SERVICE_ACCOUNT` kosong jika memakai `credentials/firebase_service_account.json`.
- Isi `ECOLAB_FIREBASE_SERVICE_ACCOUNT` hanya jika file service account disimpan di lokasi lain.
- Ganti `ECOLAB_MQTT_CA_CERT` ke `credentials/ca2.crt` hanya jika broker atau simulator memang memerlukannya.

### 6. Cara cek cepat

1. Pastikan dua file JSON ada di folder ini.
2. Pastikan file `.env` di root project sudah terisi.
3. Jalankan:

```powershell
python launcher.py
```

4. Coba login email/password.
5. Coba Google Sign-In jika fitur itu diaktifkan di project.

### 7. Troubleshooting

`Google sign-in gagal`

- Cek ulang `client_secret.json`.
- Download ulang OAuth client JSON dari Google Cloud.
- Pastikan nama filenya persis `client_secret.json`.

`Firebase auth/admin gagal`

- Cek ulang `firebase_service_account.json`.
- Pastikan project Firebase sama dengan nilai Firebase di `.env`.
- Kalau pakai path custom, cek `ECOLAB_FIREBASE_SERVICE_ACCOUNT`.

`MQTT TLS gagal`

- Periksa `ECOLAB_MQTT_CA_CERT` di `.env`.
- Coba `credentials/ca.crt` lebih dulu.
- Kalau simulator atau broker memakai sertifikat cadangan, ganti ke `credentials/ca2.crt`.

### 8. Keamanan

- Jangan upload credential ini ke GitHub atau tempat publik.
- Jangan kirim ke chat publik atau email umum.
- Bagikan hanya lewat penyimpanan privat lab atau transfer lokal langsung.
