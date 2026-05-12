"""Penyimpanan persisten untuk preference popup Smart Socket."""

import json
import os
import sys
from pathlib import Path


class SmartSocketSettingsManager:
    """Menyimpan pengaturan global dan per-socket ke file JSON."""

    def __init__(self):
        """Menentukan lokasi file settings yang akan dipakai aplikasi."""
        self.settings_file = self._get_settings_file_path()

    def _get_settings_file_path(self):
        """Menentukan path file settings untuk mode script maupun executable."""
        appdata_dir = os.getenv("APPDATA")

        if appdata_dir:
            settings_dir = Path(appdata_dir) / "EcoLab Dashboard"
        else:
            if getattr(sys, "frozen", False):
                base_dir = Path.home() / ".ecolab_dashboard"
            else:
                base_dir = Path(__file__).resolve().parent.parent / ".ecolab_dashboard"
            settings_dir = base_dir

        settings_dir.mkdir(parents=True, exist_ok=True)
        return settings_dir / "smartsocket_monitoring_settings.json"

    def load_data(self):
        """Memuat payload JSON dan selalu mengembalikan struktur yang valid."""
        if not self.settings_file.exists():
            return {"global": {}, "sockets": {}}

        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception:
            return {"global": {}, "sockets": {}}

        if not isinstance(data, dict):
            return {"global": {}, "sockets": {}}
        if not isinstance(data.get("global"), dict):
            data["global"] = {}
        if not isinstance(data.get("sockets"), dict):
            data["sockets"] = {}
        return data

    def save_data(self, data):
        """Menyimpan struktur settings yang sudah dinormalisasi ke disk."""
        payload = data if isinstance(data, dict) else {"global": {}, "sockets": {}}
        payload.setdefault("global", {})
        payload.setdefault("sockets", {})
        with open(self.settings_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4)

    def get_global_settings(self):
        """Mengambil pengaturan global yang dipakai semua popup Smart Socket."""
        data = self.load_data()
        global_settings = data.get("global", {})
        return global_settings if isinstance(global_settings, dict) else {}

    def update_global_settings(self, **settings):
        """Menggabungkan satu atau lebih global settings ke payload tersimpan."""
        data = self.load_data()
        global_settings = data.setdefault("global", {})
        for key, value in settings.items():
            global_settings[key] = value
        self.save_data(data)

    def get_socket_settings(self, socket_number):
        """Mengambil settings tersimpan untuk satu nomor socket."""
        data = self.load_data()
        sockets = data.get("sockets", {})
        entry = sockets.get(str(socket_number), {})
        return entry if isinstance(entry, dict) else {}

    def update_socket_settings(self, socket_number, **settings):
        """Menggabungkan settings khusus socket ke payload tersimpan."""
        data = self.load_data()
        sockets = data.setdefault("sockets", {})
        entry = sockets.setdefault(str(socket_number), {})

        for key, value in settings.items():
            entry[key] = value

        self.save_data(data)

    def get_socket_power_off_protection(self, socket_number):
        """Mengambil konfigurasi proteksi OFF untuk satu socket."""
        settings = self.get_socket_settings(socket_number)
        return {
            "enabled": bool(settings.get("power_off_protection_enabled", False)),
            "mode": settings.get("power_off_protection_mode", "blocked") or "blocked",
            "password_hash": settings.get("power_off_protection_password_hash", "") or "",
            "note": settings.get("power_off_protection_note", "") or "",
        }

    def update_socket_power_off_protection(
        self,
        socket_number,
        enabled,
        mode,
        password_hash=None,
        note=None,
    ):
        """Menyimpan konfigurasi proteksi OFF untuk satu socket."""
        payload = {
            "power_off_protection_enabled": bool(enabled),
            "power_off_protection_mode": (mode or "blocked").strip().lower(),
        }
        if password_hash is not None:
            payload["power_off_protection_password_hash"] = password_hash or ""
        if note is not None:
            payload["power_off_protection_note"] = (note or "").strip()
        self.update_socket_settings(socket_number, **payload)

    def get_all_graph_ranges(self):
        """Meratakan override range grafik ke key tuple agar mudah dipakai UI."""
        data = self.load_data()
        result = {}

        for socket_key, socket_settings in data.get("sockets", {}).items():
            if not isinstance(socket_settings, dict):
                continue
            graph_ranges = socket_settings.get("graph_ranges", {})
            if not isinstance(graph_ranges, dict):
                continue
            try:
                socket_number = int(socket_key)
            except (TypeError, ValueError):
                continue

            for metric, override in graph_ranges.items():
                if isinstance(override, dict):
                    result[(socket_number, metric)] = dict(override)

        return result

    def set_graph_range(self, socket_number, metric, override):
        """Membuat, mengubah, atau menghapus override range grafik."""
        data = self.load_data()
        sockets = data.setdefault("sockets", {})
        entry = sockets.setdefault(str(socket_number), {})
        graph_ranges = entry.setdefault("graph_ranges", {})

        if override is None:
            graph_ranges.pop(metric, None)
        else:
            graph_ranges[metric] = dict(override)

        self.save_data(data)
