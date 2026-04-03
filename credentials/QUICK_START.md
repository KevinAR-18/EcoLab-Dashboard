# 🚀 QUICK START - SETUP CREDENTIALS

**Panduan cepat setup Firebase & Google Cloud untuk akun lab**

---

## 📋 FILE YANG HARUS DIDAPATKAN

| File | Dari Mana | Kegunaan |
|------|-----------|----------|
| **client_secret.json** | Google Cloud Console | Google Sign In |
| **firebase_service_account.json** | Firebase Console | Firebase Auth |

---

## 🔵 GOOGLE CONSOLE - CLIENT SECRET

### **Langkah-langkah:**

1. **Buka:** https://console.cloud.google.com/
2. **Create Project:** "EcoLab-Lab"
3. **Enable API:** APIs & Services → Library → Search "Google+ API" → Enable
4. **Create OAuth:**
   - APIs & Services → Credentials
   - Create Credentials → OAuth client ID
   - Application type: Web application
   - Authorized JavaScript origins: `http://localhost`
   - Klik "Create" → **Download JSON**
5. **Rename:** `client_secret.json`

---

## 🔴 FIREBASE - SERVICE ACCOUNT

### **Langkah-langkah:**

1. **Buka:** https://console.firebase.google.com/
2. **Create Project:** "EcoLab-Lab" (sama dengan Google Cloud)
3. **Link Project:**
   - Project Settings → General → Advanced
   - "Link to Google Cloud" → Pilih "EcoLab-Lab"
4. **Enable Auth:**
   - Build → Authentication → Get Started
   - Sign-in method → Enable "Email/Password" → Save
5. **Generate Key:**
   - Project Settings → Service Accounts
   - "Generate new private key" → **Download JSON**
6. **Rename:** `firebase_service_account.json`

---

## 📂 COPY KE FOLDER CREDENTIALS

```
credentials/
├── client_secret.json              # ← Copy dari Google Cloud
├── firebase_service_account.json   # ← Copy dari Firebase
├── ca.crt                          # ← Jangan dihapus
├── ca2.crt                         # ← Jangan dihapus
├── README.txt
├── SETUP_GUIDE.md                  # ← Panduan lengkap
└── QUICK_START.md                  # ← File ini
```

---

## ✅ TESTING

### **1. Test Email/Password Login**

1. Firebase Console → Authentication → Users
2. "Add user" → Email: `test@lab.com`, Password: `Test123456`
3. Run: `python launcher.py`
4. Login dengan email di atas

### **2. Test Google Sign In**

1. Run: `python launcher.py`
2. Klik "Sign in with Google"
3. Pilih akun lab

---

## 📖 PANDUAN LENGKAP

Untuk panduan detail, lihat: **`SETUP_GUIDE.md`**

---

**Estimasi waktu:** 15-20 menit
**Difficulty:** Medium
