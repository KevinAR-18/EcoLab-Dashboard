"""Persistent storage for Smart Socket popup preferences."""

import json
import os
import sys
from pathlib import Path


class SmartSocketSettingsManager:
    """Save global and per-socket monitoring settings to a JSON file."""

    def __init__(self):
        self.settings_file = self._get_settings_file_path()

    def _get_settings_file_path(self):
        """Resolve the settings file path for script and frozen modes."""
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
        """Load the JSON payload, always returning a valid structure."""
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
        """Write the normalized settings structure back to disk."""
        payload = data if isinstance(data, dict) else {"global": {}, "sockets": {}}
        payload.setdefault("global", {})
        payload.setdefault("sockets", {})
        with open(self.settings_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4)

    def get_global_settings(self):
        data = self.load_data()
        global_settings = data.get("global", {})
        return global_settings if isinstance(global_settings, dict) else {}

    def update_global_settings(self, **settings):
        data = self.load_data()
        global_settings = data.setdefault("global", {})
        for key, value in settings.items():
            global_settings[key] = value
        self.save_data(data)

    def get_socket_settings(self, socket_number):
        data = self.load_data()
        sockets = data.get("sockets", {})
        entry = sockets.get(str(socket_number), {})
        return entry if isinstance(entry, dict) else {}

    def update_socket_settings(self, socket_number, **settings):
        data = self.load_data()
        sockets = data.setdefault("sockets", {})
        entry = sockets.setdefault(str(socket_number), {})

        for key, value in settings.items():
            entry[key] = value

        self.save_data(data)

    def get_all_graph_ranges(self):
        """Flatten stored graph overrides into tuple keys for quick lookup."""
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
        """Create, update, or clear one stored chart range override."""
        data = self.load_data()
        sockets = data.setdefault("sockets", {})
        entry = sockets.setdefault(str(socket_number), {})
        graph_ranges = entry.setdefault("graph_ranges", {})

        if override is None:
            graph_ranges.pop(metric, None)
        else:
            graph_ranges[metric] = dict(override)

        self.save_data(data)
