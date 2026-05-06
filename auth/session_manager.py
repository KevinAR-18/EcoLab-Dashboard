"""
Session manager untuk EcoLab Dashboard.

Modul ini menyimpan local session ringan yang dipakai oleh fitur remember me.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


class SessionManager:
    """Menyimpan, memuat, memvalidasi, dan menghapus file local session."""

    def __init__(self):
        """Menentukan lokasi file session dan masa berlaku default session."""
        self.session_file = self._get_session_file_path()
        self.expiry_days = 7

    def _get_session_file_path(self):
        """Menentukan path session yang stabil untuk mode script dan executable."""
        appdata_dir = os.getenv("APPDATA")

        if appdata_dir:
            session_dir = Path(appdata_dir) / "EcoLab Dashboard"
        else:
            if getattr(sys, "frozen", False):
                base_dir = Path.home() / ".ecolab_dashboard"
            else:
                base_dir = Path(__file__).resolve().parent.parent / ".ecolab_dashboard"
            session_dir = base_dir

        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir / "ecolab_session.json"

    def save_session(self, user_data):
        """Menyimpan session ke file lengkap dengan created dan expiry time."""
        try:
            session_data = {
                **user_data,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=self.expiry_days)).isoformat(),
            }

            with open(self.session_file, "w", encoding="utf-8") as file:
                json.dump(session_data, file, indent=4)

            return {"status": "success", "message": "Session saved"}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def load_session(self):
        """Memuat session tersimpan jika ada dan belum expired."""
        try:
            if not self.session_file.exists():
                return None

            with open(self.session_file, "r", encoding="utf-8") as file:
                session_data = json.load(file)

            if not self._is_valid(session_data):
                self.delete_session()
                return None

            return session_data
        except Exception as exc:
            print(f"Error loading session: {exc}")
            return None

    def delete_session(self):
        """Menghapus file local session jika memang ada."""
        try:
            if self.session_file.exists():
                self.session_file.unlink()
            return {"status": "success", "message": "Session deleted"}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def is_valid(self):
        """Mengecek apakah session yang tersimpan masih valid dipakai."""
        return self.load_session() is not None

    def _is_valid(self, session_data):
        """Memvalidasi timestamp expiry yang tersimpan di session."""
        try:
            expires_at_str = session_data.get("expires_at")
            if not expires_at_str:
                return False

            expires_at = datetime.fromisoformat(expires_at_str)
            return datetime.now() < expires_at
        except Exception:
            return False

    def get_session_info(self):
        """Mengembalikan ringkasan session yang ramah dipakai oleh UI dashboard."""
        session = self.load_session()
        if not session:
            return None

        return {
            "username": session.get("username"),
            "email": session.get("email"),
            "role": session.get("role"),
            "created_at": session.get("created_at"),
            "expires_at": session.get("expires_at"),
            "remember_me": session.get("remember_me", False),
        }
