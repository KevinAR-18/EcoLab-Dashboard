"""
Session Manager for EcoLab Dashboard
Handle remember me feature with plain JSON storage and 7 days expiry
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class SessionManager:
    """Manager untuk handle user session (remember me feature)"""

    def __init__(self):
        # Session file location (di project folder)
        self.session_file = Path(__file__).parent / "ecolab_session.json"
        self.expiry_days = 7  # Session expire dalam 7 hari

    def save_session(self, user_data):
        """
        Simpan user session ke file JSON

        Args:
            user_data (dict): User data dari Firebase
                {
                    "uid": str,
                    "username": str,
                    "email": str,
                    "role": str,
                    "auth_provider": str,
                    "remember_me": bool
                }
        """
        try:
            # Tambah timestamp
            session_data = {
                **user_data,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=self.expiry_days)).isoformat()
            }

            # Simpan ke file JSON
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=4)

            return {"status": "success", "message": "Session saved"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def load_session(self):
        """
        Load session dari file JSON

        Returns:
            dict: Session data jika valid dan belum expire
            None: Jika file tidak ada, expired, atau error
        """
        try:
            # Cek apakah file session ada
            if not self.session_file.exists():
                return None

            # Baca file JSON
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)

            # Cek expiry
            if not self._is_valid(session_data):
                # Session expired, hapus file
                self.delete_session()
                return None

            return session_data

        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def delete_session(self):
        """
        Hapus session file
        """
        try:
            if self.session_file.exists():
                self.session_file.unlink()
            return {"status": "success", "message": "Session deleted"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def is_valid(self):
        """
        Cek apakah session saat ini valid

        Returns:
            bool: True jika session valid dan belum expire
        """
        session = self.load_session()
        return session is not None

    def _is_valid(self, session_data):
        """
        Internal method untuk cek validity session

        Args:
            session_data (dict): Session data

        Returns:
            bool: True jika belum expire
        """
        try:
            expires_at_str = session_data.get("expires_at")
            if not expires_at_str:
                return False

            expires_at = datetime.fromisoformat(expires_at_str)
            return datetime.now() < expires_at

        except Exception:
            return False

    def get_session_info(self):
        """
        Get info tentang session saat ini

        Returns:
            dict: Session info atau None jika tidak ada session
        """
        session = self.load_session()
        if not session:
            return None

        return {
            "username": session.get("username"),
            "email": session.get("email"),
            "role": session.get("role"),
            "created_at": session.get("created_at"),
            "expires_at": session.get("expires_at"),
            "remember_me": session.get("remember_me", False)
        }
