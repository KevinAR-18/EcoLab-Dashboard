"""Utility recording in-memory untuk data monitoring Smart Socket."""

import csv
from datetime import datetime
from pathlib import Path


class SmartSocketRecorder:
    """Menyimpan sample monitoring per socket lalu mengekspornya ke CSV."""

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
        """Menyiapkan state recording terpisah untuk setiap Smart Socket."""
        self._recovery_dir = None
        # Setiap socket menyimpan state monitoring dan recording sendiri
        # agar popup bisa bekerja independen tanpa global bookkeeping tambahan.
        self._states = {
            socket_number: {
                "recording": False,
                "follow_schedule": False,
                "autosave_enabled": False,
                "autosave_dir": "",
                "records": [],
                "last_source": None,
                "last_record_at": None,
                "active_record_date": None,
                "record_interval_seconds": float(self.DEFAULT_RECORD_INTERVAL_SECONDS),
            }
            for socket_number in range(1, socket_count + 1)
        }

    def _state(self, socket_number):
        """Mengambil state internal milik satu socket dengan validasi nomor."""
        if socket_number not in self._states:
            raise ValueError(f"Unknown Smart Socket number: {socket_number}")
        return self._states[socket_number]

    def start(self, socket_number, source="manual"):
        """Memulai recording untuk satu socket."""
        state = self._state(socket_number)
        changed = not state["recording"]
        state["recording"] = True
        state["last_source"] = source
        state["last_record_at"] = None
        if not state.get("active_record_date"):
            state["active_record_date"] = datetime.now().date().isoformat()
        return changed

    def stop(self, socket_number, source="manual"):
        """Menghentikan recording untuk satu socket."""
        state = self._state(socket_number)
        changed = state["recording"]
        state["recording"] = False
        state["last_source"] = source
        return changed

    def is_recording(self, socket_number):
        """Mengecek apakah socket tertentu sedang merekam data."""
        return self._state(socket_number)["recording"]

    def set_follow_schedule(self, socket_number, enabled):
        """Mengatur apakah recording mengikuti trigger schedule."""
        state = self._state(socket_number)
        state["follow_schedule"] = bool(enabled)
        if enabled:
            state["autosave_enabled"] = True

    def is_follow_schedule(self, socket_number):
        """Mengecek apakah mode follow schedule aktif untuk socket tertentu."""
        return self._state(socket_number)["follow_schedule"]

    def set_autosave_enabled(self, socket_number, enabled):
        """Mengaktifkan atau menonaktifkan autosave untuk satu socket."""
        self._state(socket_number)["autosave_enabled"] = bool(enabled)

    def is_autosave_enabled(self, socket_number):
        """Mengecek apakah autosave aktif untuk socket tertentu."""
        return bool(self._state(socket_number)["autosave_enabled"])

    def set_autosave_dir(self, socket_number, directory):
        """Menyimpan folder autosave untuk satu socket."""
        self._state(socket_number)["autosave_dir"] = (directory or "").strip()

    def get_autosave_dir(self, socket_number):
        """Mengambil folder autosave yang dipakai socket tertentu."""
        return self._state(socket_number)["autosave_dir"] or ""

    def set_record_interval_seconds(self, socket_number, seconds):
        """Mengatur interval minimum antar record untuk satu socket."""
        seconds = float(seconds)
        if seconds <= 0:
            raise ValueError("record interval must be > 0 seconds")
        self._state(socket_number)["record_interval_seconds"] = seconds

    def get_record_interval_seconds(self, socket_number):
        """Mengambil interval recording yang aktif untuk satu socket."""
        return float(self._state(socket_number)["record_interval_seconds"])

    def handle_schedule_status(self, socket_number, status):
        """Menerjemahkan trigger schedule menjadi perubahan state recorder."""
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
        """Menambahkan satu sample monitoring jika socket sedang recording."""
        state = self._state(socket_number)
        # Sample hanya disimpan ketika mode recording aktif.
        if not state["recording"]:
            return None

        now = datetime.now()
        # Interval mencegah data terlalu rapat sehingga file CSV tidak membengkak.
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
        state["active_record_date"] = record["timestamp"][:10]
        # Recovery file menjaga data sementara tetap ada jika aplikasi tertutup sebelum export.
        self._append_recovery_record(socket_number, record)
        return record

    def get_records(self, socket_number):
        """Mengambil salinan record yang tersimpan untuk satu socket."""
        return list(self._state(socket_number)["records"])

    def clear_records(self, socket_number):
        """Menghapus semua record milik satu socket."""
        state = self._state(socket_number)
        state["records"].clear()
        state["last_record_at"] = None
        state["active_record_date"] = None
        self._remove_recovery_file(socket_number)

    def replace_records(self, socket_number, records):
        """Mengganti isi record socket, dipakai setelah rollover harian."""
        state = self._state(socket_number)
        state["records"] = [dict(record) for record in records]
        if state["records"]:
            state["active_record_date"] = state["records"][-1].get("timestamp", "")[:10]
        else:
            state["active_record_date"] = None
            state["last_record_at"] = None
        self._rewrite_recovery_file(socket_number)

    def count(self, socket_number):
        """Menghitung jumlah record yang tersimpan untuk satu socket."""
        return len(self._state(socket_number)["records"])

    def export_csv(self, socket_number, path):
        """Menulis semua sample milik satu socket ke file CSV."""
        records = self.get_records(socket_number)
        return self.export_records_csv(records, path)

    def export_records_csv(self, records, path):
        """Menulis kumpulan record tertentu ke file CSV."""
        with open(path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            writer.writeheader()
            writer.writerows(records)
        return len(records)

    def set_recovery_dir(self, directory):
        """Mengatur folder checkpoint recovery untuk data yang belum diekspor."""
        self._recovery_dir = Path(directory) if directory else None
        if self._recovery_dir:
            self._recovery_dir.mkdir(parents=True, exist_ok=True)

    def restore_recovery(self):
        """Memulihkan record yang tersisa dari checkpoint lokal."""
        restored = {}
        if not self._recovery_dir:
            return restored

        for socket_number in self._states:
            path = self._recovery_path(socket_number)
            if not path or not path.exists():
                continue

            records = []
            try:
                with open(path, "r", newline="", encoding="utf-8") as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        records.append(self._normalize_record(row, socket_number))
            except Exception:
                continue

            if records:
                self.replace_records(socket_number, records)
                restored[socket_number] = len(records)

        return restored

    def _recovery_path(self, socket_number):
        """Mengambil path checkpoint untuk satu socket."""
        if not self._recovery_dir:
            return None
        return self._recovery_dir / f"smartsocket_{socket_number}_recovery.csv"

    def _append_recovery_record(self, socket_number, record):
        """Menambahkan satu sample ke checkpoint tanpa rewrite file besar."""
        path = self._recovery_path(socket_number)
        if not path:
            return

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            write_header = not path.exists() or path.stat().st_size == 0
            with open(path, "a", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
                if write_header:
                    writer.writeheader()
                writer.writerow(record)
        except Exception:
            pass

    def _rewrite_recovery_file(self, socket_number):
        """Menyamakan checkpoint dengan records aktif setelah clear parsial."""
        path = self._recovery_path(socket_number)
        if not path:
            return

        records = self.get_records(socket_number)
        if not records:
            self._remove_recovery_file(socket_number)
            return

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            self.export_records_csv(records, path)
        except Exception:
            pass

    def _remove_recovery_file(self, socket_number):
        """Menghapus checkpoint ketika data sudah aman diekspor atau di-clear."""
        path = self._recovery_path(socket_number)
        if not path:
            return
        try:
            if path.exists():
                path.unlink()
        except Exception:
            pass

    def _normalize_record(self, row, socket_number):
        """Menormalkan row CSV recovery agar typenya sama seperti record baru."""
        return {
            "timestamp": row.get("timestamp", ""),
            "socket": int(row.get("socket") or socket_number),
            "relay_state": row.get("relay_state", ""),
            "voltage": self._to_float(row.get("voltage")),
            "current": self._to_float(row.get("current")),
            "power": self._to_float(row.get("power")),
            "energy": self._to_float(row.get("energy")),
            "frequency": self._to_float(row.get("frequency")),
            "pf": self._to_float(row.get("pf")),
        }

    @staticmethod
    def _to_float(value):
        """Mengubah nilai ke float secara aman untuk kebutuhan recording/export."""
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
