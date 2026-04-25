import csv
from datetime import datetime


class SmartSocketRecorder:
    """In-memory recorder for Smart Socket monitoring samples."""

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
        self._states = {
            socket_number: {
                "recording": False,
                "follow_schedule": False,
                "records": [],
                "last_source": None,
            }
            for socket_number in range(1, socket_count + 1)
        }

    def _state(self, socket_number):
        if socket_number not in self._states:
            raise ValueError(f"Unknown Smart Socket number: {socket_number}")
        return self._states[socket_number]

    def start(self, socket_number, source="manual"):
        state = self._state(socket_number)
        changed = not state["recording"]
        state["recording"] = True
        state["last_source"] = source
        return changed

    def stop(self, socket_number, source="manual"):
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

    def handle_schedule_status(self, socket_number, status):
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
        state = self._state(socket_number)
        if not state["recording"]:
            return None

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "socket": socket_number,
            "relay_state": "ON" if relay_state else "OFF",
            "voltage": self._to_float(data.get("voltage")),
            "current": self._to_float(data.get("current")),
            "power": self._to_float(data.get("power")),
            "energy": self._to_float(data.get("energy")),
            "frequency": self._to_float(data.get("frequency")),
            "pf": self._to_float(data.get("pf")),
        }
        state["records"].append(record)
        return record

    def get_records(self, socket_number):
        return list(self._state(socket_number)["records"])

    def clear_records(self, socket_number):
        self._state(socket_number)["records"].clear()

    def count(self, socket_number):
        return len(self._state(socket_number)["records"])

    def export_csv(self, socket_number, path):
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
