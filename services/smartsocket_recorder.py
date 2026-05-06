"""In-memory recording utilities for Smart Socket monitoring data."""

import csv
from datetime import datetime


class SmartSocketRecorder:
    """Store per-socket monitoring samples and export them to CSV."""

    DEFAULT_RECORD_INTERVAL_SECONDS = 5

    FIELD_NAMES = [
        "timestamp",
        "socket",
        "relay_state",
        "voltage",
        "current",
        "power",
        "energy",
        "frequency",
        "pf",
    ]

    METRICS = {
        "voltage": "Voltage",
        "current": "Current",
        "power": "Power",
        "energy": "Energy",
        "frequency": "Frequency",
        "pf": "PF",
    }

    def __init__(self, socket_count=5):
        # Every socket keeps its own monitoring and recording state so popup
        # windows can work independently without extra global bookkeeping.
        self._states = {
            socket_number: {
                "recording": False,
                "follow_schedule": False,
                "autosave_enabled": False,
                "autosave_dir": "",
                "records": [],
                "last_source": None,
                "last_record_at": None,
                "record_interval_seconds": float(self.DEFAULT_RECORD_INTERVAL_SECONDS),
            }
            for socket_number in range(1, socket_count + 1)
        }

    def _state(self, socket_number):
        if socket_number not in self._states:
            raise ValueError(f"Unknown Smart Socket number: {socket_number}")
        return self._states[socket_number]

    def start(self, socket_number, source="manual"):
        """Start recording for one socket."""
        state = self._state(socket_number)
        changed = not state["recording"]
        state["recording"] = True
        state["last_source"] = source
        state["last_record_at"] = None
        return changed

    def stop(self, socket_number, source="manual"):
        """Stop recording for one socket."""
        state = self._state(socket_number)
        changed = state["recording"]
        state["recording"] = False
        state["last_source"] = source
        return changed

    def is_recording(self, socket_number):
        return self._state(socket_number)["recording"]

    def set_follow_schedule(self, socket_number, enabled):
        self._state(socket_number)["follow_schedule"] = bool(enabled)

    def is_follow_schedule(self, socket_number):
        return self._state(socket_number)["follow_schedule"]

    def set_autosave_enabled(self, socket_number, enabled):
        self._state(socket_number)["autosave_enabled"] = bool(enabled)

    def is_autosave_enabled(self, socket_number):
        return bool(self._state(socket_number)["autosave_enabled"])

    def set_autosave_dir(self, socket_number, directory):
        self._state(socket_number)["autosave_dir"] = (directory or "").strip()

    def get_autosave_dir(self, socket_number):
        return self._state(socket_number)["autosave_dir"] or ""

    def set_record_interval_seconds(self, socket_number, seconds):
        seconds = float(seconds)
        if seconds <= 0:
            raise ValueError("record interval must be > 0 seconds")
        self._state(socket_number)["record_interval_seconds"] = seconds

    def get_record_interval_seconds(self, socket_number):
        return float(self._state(socket_number)["record_interval_seconds"])

    def handle_schedule_status(self, socket_number, status):
        """Translate schedule triggers into recorder state changes."""
        state = self._state(socket_number)
        if not state["follow_schedule"]:
            return None

        if status == "START_TRIGGER":
            self.start(socket_number, source="schedule")
            return "started"

        if status == "STOP_TRIGGER":
            self.stop(socket_number, source="schedule")
            return "stopped"

        return None

    def append_energy(self, socket_number, data, relay_state):
        """Append one monitoring sample if the socket is actively recording."""
        state = self._state(socket_number)
        if not state["recording"]:
            return None

        now = datetime.now()
        last = state.get("last_record_at")
        interval = float(
            state.get("record_interval_seconds") or self.DEFAULT_RECORD_INTERVAL_SECONDS
        )
        if last is not None:
            elapsed = (now - last).total_seconds()
            if elapsed < interval:
                return None

        record = {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "socket": socket_number,
            "relay_state": "ON" if relay_state else "OFF",
            "voltage": self._to_float(data.get("voltage")),
            "current": self._to_float(data.get("current")),
            "power": self._to_float(data.get("power")),
            "energy": self._to_float(data.get("energy")),
            "frequency": self._to_float(data.get("frequency")),
            "pf": self._to_float(data.get("pf")),
        }
        state["last_record_at"] = now
        state["records"].append(record)
        return record

    def get_records(self, socket_number):
        return list(self._state(socket_number)["records"])

    def clear_records(self, socket_number):
        self._state(socket_number)["records"].clear()

    def count(self, socket_number):
        return len(self._state(socket_number)["records"])

    def export_csv(self, socket_number, path):
        """Write all stored samples for one socket to a CSV file."""
        records = self.get_records(socket_number)
        with open(path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            writer.writeheader()
            writer.writerows(records)
        return len(records)

    @staticmethod
    def _to_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
