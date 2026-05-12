"""Penyimpanan proteksi power-off Smart Socket di Firebase Realtime Database."""

import types
import sys

try:
    import urllib3.contrib.appengine  # type: ignore[import-not-found]
except ModuleNotFoundError:
    appengine_stub = types.ModuleType("urllib3.contrib.appengine")
    appengine_stub.is_appengine_sandbox = lambda: False
    sys.modules["urllib3.contrib.appengine"] = appengine_stub

import pyrebase

from config.firebase_settings import get_firebase_config


class SmartSocketProtectionStore:
    """Membaca dan menulis proteksi Smart Socket ke Firebase."""

    ROOT_PATH = "smartsocket_protection"

    def __init__(self):
        firebase = pyrebase.initialize_app(get_firebase_config())
        self.db = firebase.database()

    def get_all(self):
        """Mengambil semua proteksi Smart Socket dari Firebase."""
        snapshot = self.db.child(self.ROOT_PATH).get()
        raw = snapshot.val() or {}
        if not isinstance(raw, dict):
            return {}

        result = {}
        for socket_key, payload in raw.items():
            try:
                socket_number = int(socket_key)
            except (TypeError, ValueError):
                continue
            result[socket_number] = self._normalize(payload)
        return result

    def get_one(self, socket_number):
        """Mengambil satu konfigurasi proteksi Smart Socket."""
        payload = self.db.child(self.ROOT_PATH).child(str(socket_number)).get().val() or {}
        return self._normalize(payload)

    def set_one(self, socket_number, payload):
        """Menyimpan satu konfigurasi proteksi Smart Socket."""
        normalized = self._normalize(payload)
        self.db.child(self.ROOT_PATH).child(str(socket_number)).set(normalized)
        return normalized

    @staticmethod
    def _normalize(payload):
        payload = payload if isinstance(payload, dict) else {}
        return {
            "enabled": bool(payload.get("enabled", False)),
            "mode": (payload.get("mode") or "blocked").strip().lower(),
            "password_hash": payload.get("password_hash", "") or "",
            "note": payload.get("note", "") or "",
        }
