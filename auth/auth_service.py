from __future__ import annotations

"""Service authentication Firebase dan user management untuk aplikasi desktop."""

import sys
import types
from datetime import datetime
from pathlib import Path

try:
    import urllib3.contrib.appengine  # type: ignore[import-not-found]
except ModuleNotFoundError:
    appengine_stub = types.ModuleType("urllib3.contrib.appengine")
    appengine_stub.is_appengine_sandbox = lambda: False
    sys.modules["urllib3.contrib.appengine"] = appengine_stub

import pyrebase
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

from config.firebase_settings import (
    CLIENT_SECRET,
    get_admin_service_account_path,
    get_firebase_config,
    get_firebase_project_id,
)


class FirebaseAuthAdminClient:
    """REST client kecil untuk operasi admin Firebase yang butuh privilege."""
    _SCOPES = ["https://www.googleapis.com/auth/identitytoolkit"]

    def __init__(self, project_id, service_account_path):
        """Menyimpan project ID dan path service account untuk operasi admin."""
        self.project_id = project_id
        self.service_account_path = Path(service_account_path)
        self._credentials = None

    def is_configured(self):
        """Mengecek apakah file service account admin tersedia."""
        return self.service_account_path.is_file()

    def update_password(self, uid, password):
        """Mengirim request admin untuk update password user tertentu."""
        return self._post("accounts:update", {"localId": uid, "password": password})

    def delete_user(self, uid):
        """Mengirim request admin untuk menghapus user tertentu."""
        return self._post("accounts:delete", {"localId": uid})

    def _post(self, action, payload):
        """Menjalankan POST request ke Firebase Identity Toolkit API."""
        if not self.is_configured():
            raise RuntimeError("Firebase admin credentials are not configured")

        credentials = self._get_credentials()
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/projects/{self.project_id}/{action}",
            json=payload,
            headers={"Authorization": f"Bearer {credentials.token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.content else {}

    def _get_credentials(self):
        """Membuat atau me-refresh kredensial service account sebelum request."""
        if self._credentials is None:
            self._credentials = service_account.Credentials.from_service_account_file(
                str(self.service_account_path),
                scopes=self._SCOPES,
            )

        if not self._credentials.valid or self._credentials.expired:
            self._credentials.refresh(Request())

        return self._credentials


class FirebaseAuthService:
    """Service utama aplikasi untuk auth, signup, dan data user Firebase."""
    def __init__(self):
        """Menyiapkan client Pyrebase dan admin client untuk semua auth flow."""
        # Pyrebase dipakai untuk auth flow user biasa, sedangkan admin client
        # dipakai untuk operasi yang memang memerlukan service account.
        firebase_config = get_firebase_config()
        firebase = pyrebase.initialize_app(firebase_config)
        self.auth = firebase.auth()
        self.db = firebase.database()
        self.admin_client = FirebaseAuthAdminClient(
            project_id=get_firebase_project_id(),
            service_account_path=get_admin_service_account_path(),
        )

    def create_admin(self, email, password):
        """Membuat akun admin awal di Firebase Auth dan database user."""
        user = self.auth.create_user_with_email_and_password(email, password)
        uid = user["localId"]

        self.db.child("users").child(uid).set(
            {
                "username": "admin",
                "email": email,
                "role": "admin",
                "role_request": "admin",
                "status": "active",
                "date": self._today(),
                "auth_provider": "email",
            }
        )

        return {"status": "success", "message": "Admin created", "user_id": uid}

    def login_with_email(self, email, password):
        """Melakukan login user menggunakan email dan password."""
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            uid = user["localId"]
            return self._build_login_result(uid, self.get_user_record(uid))
        except Exception as exc:
            return self._error_result(exc)

    def signup_with_email(self, email, password, username=None):
        """Mendaftarkan user baru lewat email/password dengan status pending."""
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            uid = user["localId"]

            # Pakai username dari parameter, atau fallback ke prefix email.
            display_username = username or email.split("@")[0]

            self.db.child("users").child(uid).set(
                {
                    "username": display_username,
                    "email": email,
                    "role_request": "user",
                    "role": "user",
                    "status": "pending",
                    "date": self._today(),
                    "auth_provider": "email",
                }
            )

            return {"status": "success", "message": "Signup request sent", "user_id": uid}
        except Exception as exc:
            return self._error_result(exc)

    def login_with_google(self, create_if_not_exists=True):
        """
        Menjalankan login atau signup lewat Google OAuth.

        Args:
            create_if_not_exists: Jika True, auto create account jika belum ada.
                                 Jika False, hanya login dan return error jika akun belum ada.
        """
        try:
            userinfo = self._google_auth_login()
            uid = userinfo["id"]
            email = userinfo["email"]
            name = userinfo["name"]
            user = self.get_user_record(uid)

            if not user:
                # Jika user belum ada di database
                if create_if_not_exists:
                    # Mode sign up: auto create account baru.
                    self.db.child("users").child(uid).set(
                        {
                            "username": name,
                            "email": email,
                            "role_request": "user",
                            "role": "user",
                            "status": "pending",
                            "date": self._today(),
                            "auth_provider": "google",
                        }
                    )
                    return {
                        "status": "pending",
                        "message": "Google account registered, waiting admin approval",
                        "user_id": uid,
                    }
                else:
                    # Mode sign in: jangan create account baru.
                    return {
                        "status": "error",
                        "message": "Google account not registered. Please sign up first.",
                    }

            return self._build_login_result(
                uid,
                self._normalize_user_record(uid, user),
                success_message="Google login success",
                pending_message="Google account registered, waiting admin approval",
            )
        except Exception as exc:
            return self._error_result(exc)

    def send_reset_password(self, email):
        """Mengirim email reset password lewat Firebase."""
        try:
            self.auth.send_password_reset_email(email)
            return {"status": "success", "message": "Check your email"}
        except Exception as exc:
            return self._error_result(exc)

    def check_email_exists(self, email):
        """
        Mengecek apakah email sudah terdaftar di Firebase Authentication.

        Args:
            email: Email yang akan dicek

        Returns:
            dict: {"exists": bool, "message": str}
        """
        try:
            # Coba sign in dengan dummy password.
            # Firebase akan mengembalikan error spesifik:
            # - EMAIL_NOT_FOUND -> email belum terdaftar
            # - INVALID_PASSWORD -> email sudah ada, tapi password salah
            self.auth.sign_in_with_email_and_password(email, "__dummy_password_check_123__")
            return {"exists": False, "message": "Unexpected success"}
        except Exception as exc:
            error_msg = str(exc)

            # Parse error message dari Firebase.
            if "EMAIL_NOT_FOUND" in error_msg or "There is no user record" in error_msg:
                # Email belum terdaftar.
                return {"exists": False, "message": "Email available"}
            elif "INVALID_PASSWORD" in error_msg or "The password is invalid" in error_msg:
                # Email sudah terdaftar, hanya password dummy-nya yang salah.
                return {"exists": True, "message": "Email already registered"}
            else:
                # Error lain seperti network issue atau format email tidak valid.
                return {"exists": False, "message": f"Error: {error_msg}"}

    def get_pending_users(self):
        """Mengambil daftar user yang masih menunggu approval admin."""
        return [
            {
                "uid": user["uid"],
                "username": user["username"],
                "email": user["email"],
                "role_request": user["role_request"],
                "date": user["date"],
            }
            for user in self.get_all_users()
            if user["status"] == "pending"
        ]

    def get_all_users(self):
        """Mengambil semua user lalu menormalkannya untuk kebutuhan admin UI."""
        users = self.db.child("users").get()
        if not users.each():
            return []

        normalized = [
            self._normalize_user_record(user.key(), user.val() or {}) for user in users.each()
        ]
        return sorted(
            normalized,
            key=lambda user: (
                self._status_rank(user["status"]),
                user["created_date"],
                user["email"].lower(),
            ),
        )

    def get_user_summary(self):
        """Menghasilkan ringkasan jumlah user berdasarkan status dan role."""
        users = self.get_all_users()
        return {
            "total": len(users),
            "pending": sum(1 for user in users if user["status"] == "pending"),
            "active": sum(1 for user in users if user["status"] == "active"),
            "blocked": sum(1 for user in users if user["status"] == "blocked"),
            "admins": sum(1 for user in users if user["role"] == "admin"),
        }

    def update_user_role(self, uid, role):
        """Mengubah role user tertentu di database Firebase."""
        user = self.get_user_record(uid)
        if not user:
            return {"status": "error", "message": "User data not found"}

        self.db.child("users").child(uid).update({"role": role, "role_request": role})
        return {"status": "success", "message": "Role updated", "user_id": uid}

    def update_user_status(self, uid, status):
        """Mengubah status user tertentu seperti active atau blocked."""
        user = self.get_user_record(uid)
        if not user:
            return {"status": "error", "message": "User data not found"}

        self.db.child("users").child(uid).update({"status": status})
        return {"status": "success", "message": f"Status updated to {status}", "user_id": uid}

    def set_user_password(self, uid, new_password):
        """Mengubah password user tertentu lewat admin client Firebase."""
        try:
            self.admin_client.update_password(uid, new_password)
            return {"status": "success", "message": "Password updated", "user_id": uid}
        except Exception as exc:
            return self._error_result(exc)

    def delete_user(self, uid):
        """Menghapus user dari database dan Auth jika provider mengizinkan."""
        try:
            # Ambil data user untuk cek auth provider.
            user = self.get_user_record(uid)

            if not user:
                return {"status": "error", "message": "User data not found"}

            auth_provider = user.get("auth_provider", "email")

            if auth_provider == "google":
                # User Google Auth tidak dihapus dari Firebase Auth.
                # Yang dihapus hanya entry database-nya.
                self.db.child("users").child(uid).remove()
                return {
                    "status": "success",
                    "message": "Google user removed from database. Note: User may still be able to login with Google.",
                    "user_id": uid,
                    "warning": "google_auth"
                }
            else:
                # User email auth bisa dihapus dari Auth dan database.
                self.admin_client.delete_user(uid)
                self.db.child("users").child(uid).remove()
                return {"status": "success", "message": "User deleted successfully", "user_id": uid}

        except Exception as exc:
            return self._error_result(exc)

    def approve_user(self, uid):
        """Menyetujui user pending dan mengaktifkan role final-nya."""
        user = self.get_user_record(uid)
        if not user:
            return {"status": "missing_user_data", "message": "User data not found"}

        self.db.child("users").child(uid).update(
            {
                "status": "active",
                "role": user.get("role", user.get("role_request", "user")),
                "role_request": user.get("role_request", user.get("role", "user")),
            }
        )
        return {"status": "success", "message": "User approved", "user_id": uid}

    def reject_user(self, uid):
        """Menolak user pending dengan menghapus entry database-nya."""
        self.db.child("users").child(uid).remove()
        return {"status": "success", "message": "User rejected", "user_id": uid}

    def get_user_record(self, uid):
        """Mengambil raw user record dari database Firebase."""
        return self.db.child("users").child(uid).get().val()

    def _google_auth_login(self):
        """Menjalankan flow OAuth lokal lalu mengambil profil user Google."""
        # Local redirect server menjaga Google OAuth tetap cocok untuk
        # desktop app tanpa perlu embed web view khusus.
        # Gunakan port tetap untuk menghindari redirect_uri_mismatch.
        # Pastikan http://localhost:8080 terdaftar di Google Cloud Console.
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRET),
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            redirect_uri="http://localhost:8080/"
        )

        credentials = flow.run_local_server(port=8080)
        token = credentials.token

        return requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"access_token": token},
            timeout=30,
        ).json()

    def _build_login_result(
        self,
        uid,
        user_data,
        success_message="Login success",
        pending_message="Waiting admin approval",
    ):
        """Menyusun hasil login terstandar berdasarkan data user yang ditemukan."""
        if not user_data:
            return {"status": "missing_user_data", "message": "User data not found"}

        status = user_data.get("status")
        if status == "pending":
            return {"status": "pending", "message": pending_message, "user_id": uid}

        if status == "blocked":
            return {"status": "blocked", "message": "Account blocked", "user_id": uid}

        if user_data.get("role") == "admin":
            return {"status": "admin", "message": "Admin login", "user_id": uid}

        return {"status": "success", "message": success_message, "user_id": uid}

    def _error_result(self, exc):
        """Membungkus exception ke format error result yang konsisten."""
        return {"status": "error", "message": str(exc)}

    @staticmethod
    def _today():
        """Menghasilkan tanggal hari ini dalam format `YYYY-MM-DD`."""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def _normalize_user_record(uid, data):
        """Menormalkan record user agar field penting selalu tersedia."""
        role = data.get("role", data.get("role_request", "user")) or "user"
        return {
            "uid": uid,
            "username": data.get("username", "") or data.get("email", "").split("@")[0],
            "email": data.get("email", ""),
            "role": role,
            "role_request": data.get("role_request", role),
            "status": data.get("status", "pending"),
            "date": data.get("date", ""),
            "created_date": data.get("date", ""),
            "auth_provider": data.get("auth_provider", "email"),
        }

    @staticmethod
    def _status_rank(status):
        """Memberi ranking status untuk kebutuhan sorting di admin panel."""
        order = {"pending": 0, "active": 1, "blocked": 2}
        return order.get(status, 3)
