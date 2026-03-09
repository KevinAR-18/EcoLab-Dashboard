from __future__ import annotations

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

try:
    from .settings import (
        CLIENT_SECRET,
        get_admin_service_account_path,
        get_firebase_config,
        get_firebase_project_id,
    )
except ImportError:
    from settings import (
        CLIENT_SECRET,
        get_admin_service_account_path,
        get_firebase_config,
        get_firebase_project_id,
    )


class FirebaseAuthAdminClient:
    _SCOPES = ["https://www.googleapis.com/auth/identitytoolkit"]

    def __init__(self, project_id, service_account_path):
        self.project_id = project_id
        self.service_account_path = Path(service_account_path)
        self._credentials = None

    def is_configured(self):
        return self.service_account_path.is_file()

    def update_password(self, uid, password):
        return self._post("accounts:update", {"localId": uid, "password": password})

    def delete_user(self, uid):
        return self._post("accounts:delete", {"localId": uid})

    def _post(self, action, payload):
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
        if self._credentials is None:
            self._credentials = service_account.Credentials.from_service_account_file(
                str(self.service_account_path),
                scopes=self._SCOPES,
            )

        if not self._credentials.valid or self._credentials.expired:
            self._credentials.refresh(Request())

        return self._credentials


class TrialLoginService:
    def __init__(self):
        firebase_config = get_firebase_config()
        firebase = pyrebase.initialize_app(firebase_config)
        self.auth = firebase.auth()
        self.db = firebase.database()
        self.admin_client = FirebaseAuthAdminClient(
            project_id=get_firebase_project_id(),
            service_account_path=get_admin_service_account_path(),
        )

    def create_admin(self, email="admin@ecolab.com", password="admin123"):
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
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            uid = user["localId"]
            return self._build_login_result(uid, self.get_user_record(uid))
        except Exception as exc:
            return self._error_result(exc)

    def signup_with_email(self, email, password):
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            uid = user["localId"]

            self.db.child("users").child(uid).set(
                {
                    "username": email.split("@")[0],
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

    def login_with_google(self):
        try:
            userinfo = self._google_auth_login()
            uid = userinfo["id"]
            email = userinfo["email"]
            name = userinfo["name"]
            user = self.get_user_record(uid)

            if not user:
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

            return self._build_login_result(
                uid,
                self._normalize_user_record(uid, user),
                success_message="Google login success",
                pending_message="Google account registered, waiting admin approval",
            )
        except Exception as exc:
            return self._error_result(exc)

    def send_reset_password(self, email):
        try:
            self.auth.send_password_reset_email(email)
            return {"status": "success", "message": "Check your email"}
        except Exception as exc:
            return self._error_result(exc)

    def get_pending_users(self):
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
        users = self.get_all_users()
        return {
            "total": len(users),
            "pending": sum(1 for user in users if user["status"] == "pending"),
            "active": sum(1 for user in users if user["status"] == "active"),
            "blocked": sum(1 for user in users if user["status"] == "blocked"),
            "admins": sum(1 for user in users if user["role"] == "admin"),
        }

    def update_user_role(self, uid, role):
        user = self.get_user_record(uid)
        if not user:
            return {"status": "error", "message": "User data not found"}

        self.db.child("users").child(uid).update({"role": role, "role_request": role})
        return {"status": "success", "message": "Role updated", "user_id": uid}

    def update_user_status(self, uid, status):
        user = self.get_user_record(uid)
        if not user:
            return {"status": "error", "message": "User data not found"}

        self.db.child("users").child(uid).update({"status": status})
        return {"status": "success", "message": f"Status updated to {status}", "user_id": uid}

    def set_user_password(self, uid, new_password):
        try:
            self.admin_client.update_password(uid, new_password)
            return {"status": "success", "message": "Password updated", "user_id": uid}
        except Exception as exc:
            return self._error_result(exc)

    def delete_user(self, uid):
        try:
            self.admin_client.delete_user(uid)
            self.db.child("users").child(uid).remove()
            return {"status": "success", "message": "User deleted", "user_id": uid}
        except Exception as exc:
            return self._error_result(exc)

    def approve_user(self, uid):
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
        self.db.child("users").child(uid).remove()
        return {"status": "success", "message": "User rejected", "user_id": uid}

    def get_user_record(self, uid):
        return self.db.child("users").child(uid).get().val()

    def _google_auth_login(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRET),
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
        )

        credentials = flow.run_local_server(port=0)
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
        return {"status": "error", "message": str(exc)}

    @staticmethod
    def _today():
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def _normalize_user_record(uid, data):
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
        order = {"pending": 0, "active": 1, "blocked": 2}
        return order.get(status, 3)
