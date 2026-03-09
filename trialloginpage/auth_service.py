from __future__ import annotations

from datetime import datetime

import pyrebase
import requests
from google_auth_oauthlib.flow import InstalledAppFlow

try:
    from .settings import CLIENT_SECRET, get_firebase_config
except ImportError:
    from settings import CLIENT_SECRET, get_firebase_config


class TrialLoginService:
    def __init__(self):
        firebase = pyrebase.initialize_app(get_firebase_config())
        self.auth = firebase.auth()
        self.db = firebase.database()

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
                    }
                )
                return {
                    "status": "success",
                    "message": "Google signup request sent",
                    "user_id": uid,
                }

            return self._build_login_result(uid, user, success_message="Google login success")
        except Exception as exc:
            return self._error_result(exc)

    def send_reset_password(self, email):
        try:
            self.auth.send_password_reset_email(email)
            return {"status": "success", "message": "Check your email"}
        except Exception as exc:
            return self._error_result(exc)

    def get_pending_users(self):
        users = self.db.child("users").get()
        pending_users = []

        if not users.each():
            return pending_users

        for user in users.each():
            data = user.val() or {}
            if data.get("status") != "pending":
                continue

            pending_users.append(
                {
                    "uid": user.key(),
                    "username": data.get("username", ""),
                    "email": data.get("email", ""),
                    "role_request": data.get("role_request", ""),
                    "date": data.get("date", ""),
                }
            )

        return pending_users

    def approve_user(self, uid):
        user = self.get_user_record(uid)
        if not user:
            return {"status": "missing_user_data", "message": "User data not found"}

        self.db.child("users").child(uid).update(
            {"status": "active", "role": user.get("role_request", "user")}
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

    def _build_login_result(self, uid, user_data, success_message="Login success"):
        if not user_data:
            return {"status": "missing_user_data", "message": "User data not found"}

        status = user_data.get("status")
        if status == "pending":
            return {"status": "pending", "message": "Waiting admin approval", "user_id": uid}

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
