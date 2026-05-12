#!/usr/bin/env python3
"""
Backend MQTT Smart Socket untuk EcoLab.

Modul ini menangani komunikasi MQTT untuk device Smart Socket,
baik sisi status, monitoring energi, timer, maupun schedule.
"""

import json
from PySide6.QtCore import QObject, Signal


class SmartSocketBackend(QObject):
    """Backend untuk satu device Smart Socket."""

    # Signal untuk update UI
    status_changed = Signal(bool)  # Relay state: True=ON, False=OFF
    energy_changed = Signal(dict)  # Energy data: {voltage, current, power, energy, frequency, pf}
    timer_status_changed = Signal(str)  # Timer status: "ACTIVE:XXs" / "INACTIVE"
    schedule_status_changed = Signal(str)  # Schedule JSON string
    device_status_changed = Signal(bool)  # Device online: True=ONLINE, False=OFFLINE

    def __init__(self, mqtt_client, socket_number, logger=None):
        """Menyimpan client MQTT, nomor socket, topic, dan state awal device."""
        super().__init__()
        self.mqtt = mqtt_client
        self.socket_number = socket_number
        self.logger = logger

        # State storage untuk cache status terakhir.
        self.relay_state = None
        self.energy_data = {}
        self.timer_status = "INACTIVE"
        self.schedule_status = {}
        self.device_online = False

        # Daftar topic MQTT milik socket ini.
        self.topic_prefix = f"ecolab/socket/{socket_number}"
        self.topics = {
            "relay": f"{self.topic_prefix}/relaystatus",
            "energy": f"{self.topic_prefix}/energy",
            "timer": f"{self.topic_prefix}/timer/status",
            "schedule": f"{self.topic_prefix}/schedule/status",
            "device": f"{self.topic_prefix}/devicestatus",
        }

        # Subscribe tidak dilakukan di sini, tetapi lewat manager.
        if self.logger:
            self.logger(f"[Smart Socket {self.socket_number}] Backend initialized")

    def _subscribe_topics(self):
        """Placeholder lama; subscribe sekarang di-handle oleh manager."""
        pass

    def on_message(self, topic, payload):
        """Menerima MQTT message lalu meneruskannya ke parser yang sesuai."""
        if topic == self.topics["relay"]:
            self._handle_relay_status(payload)

        elif topic == self.topics["energy"]:
            self._handle_energy_data(payload)

        elif topic == self.topics["timer"]:
            self._handle_timer_status(payload)

        elif topic == self.topics["schedule"]:
            self._handle_schedule_status(payload)

        elif topic == self.topics["device"]:
            self._handle_device_status(payload)

    def _handle_relay_status(self, payload):
        """Memproses update status relay."""
        try:
            state = payload == "ON"
            if state != self.relay_state:
                self.relay_state = state
                self.status_changed.emit(state)
                if self.logger:
                    self.logger(f"[Socket {self.socket_number}] Relay: {payload}")
        except Exception as e:
            if self.logger:
                self.logger(f"[Socket {self.socket_number}] Error parsing relay: {e}")

    def _handle_energy_data(self, payload):
        """Memproses update data energi dari payload JSON."""
        try:
            data = json.loads(payload)
            self.energy_data = data
            self.energy_changed.emit(data)
            # Log hanya saat ada daya yang benar-benar terbaca.
            if self.logger and data.get("power", 0) > 0:
                v = data.get("voltage", 0)
                i = data.get("current", 0)
                p = data.get("power", 0)
                self.logger(f"[Socket {self.socket_number}] Energy: {v}V, {i}A, {p}W")
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger(f"[Socket {self.socket_number}] Error parsing energy: {e}")

    def _handle_timer_status(self, payload):
        """Memproses update status timer."""
        if payload != self.timer_status:
            self.timer_status = payload
            self.timer_status_changed.emit(payload)
            if self.logger:
                self.logger(f"[Socket {self.socket_number}] Timer: {payload}")

    def _handle_schedule_status(self, payload):
        """Memproses update status schedule."""
        try:
            data = json.loads(payload)
            self.schedule_status = data
            self.schedule_status_changed.emit(payload)
            if self.logger:
                mode = data.get("mode", "N/A")
                start = data.get("start", "N/A")
                stop = data.get("stop", "N/A")
                self.logger(f"[Socket {self.socket_number}] Schedule: {mode} {start}-{stop}")
        except json.JSONDecodeError:
            # Jika payload bukan JSON, pertahankan detail jadwal terakhir
            # lalu simpan trigger mentah agar status aktif tidak hilang.
            previous = self.schedule_status if isinstance(self.schedule_status, dict) else {}
            self.schedule_status = {
                **previous,
                "raw": payload,
            }
            self.schedule_status_changed.emit(payload)

    def _handle_device_status(self, payload):
        """Memproses update status device ONLINE atau OFFLINE."""
        try:
            online = payload == "ONLINE"
            if online != self.device_online:
                self.device_online = online
                self.device_status_changed.emit(online)
                if self.logger:
                    self.logger(f"[Socket {self.socket_number}] Device: {payload}")
        except Exception as e:
            if self.logger:
                self.logger(f"[Socket {self.socket_number}] Error parsing device status: {e}")

    # ================= METHOD PUBLISH =================

    def set_relay(self, state):
        """Mengirim command relay ON/OFF ke socket."""
        payload = "ON" if state else "OFF"
        topic = f"{self.topic_prefix}/control"  # contoh: ecolab/socket/1/control
        self.mqtt.publish(topic, payload)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Control: {payload}")

    def set_timer(self, duration_seconds):
        """Mengirim command timer ke socket."""
        topic = f"{self.topic_prefix}/timer"
        self.mqtt.publish(topic, str(duration_seconds))
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Timer: {duration_seconds}s")

    def cancel_timer(self):
        """Membatalkan timer yang sedang aktif."""
        self.set_timer(0)

    def set_schedule_start(self, time_str):
        """Mengatur jam mulai schedule, misalnya `HH:MM` atau `CLEAR`."""
        topic = f"{self.topic_prefix}/schedule/start"
        self.mqtt.publish(topic, time_str)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Schedule Start: {time_str}")

    def set_schedule_stop(self, time_str):
        """Mengatur jam berhenti schedule, misalnya `HH:MM` atau `CLEAR`."""
        topic = f"{self.topic_prefix}/schedule/stop"
        self.mqtt.publish(topic, time_str)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Schedule Stop: {time_str}")

    def set_schedule_mode(self, mode):
        """Mengatur mode schedule seperti `daily` atau `onetime`."""
        topic = f"{self.topic_prefix}/schedule/mode"
        self.mqtt.publish(topic, mode)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Schedule Mode: {mode}")

    def clear_schedule(self):
        """Menghapus semua pengaturan schedule pada socket."""
        self.set_schedule_start("CLEAR")
        self.set_schedule_stop("CLEAR")


class SmartSocketManager(QObject):
    """Manager untuk seluruh device Smart Socket, default-nya 1 sampai 5."""

    def __init__(self, mqtt_client, logger=None):
        """Membuat semua backend socket lalu memasang wildcard subscription."""
        super().__init__()
        self.mqtt = mqtt_client
        self.logger = logger
        self.backends = {}

        # Buat backend untuk lima socket.
        for i in range(1, 6):
            self.backends[i] = SmartSocketBackend(mqtt_client, i, logger)

        # Subscribe ke semua topic Smart Socket dengan wildcard.
        smartsocket_wildcard = "ecolab/socket/#"

        # Buat wrapper callback sesuai signature bawaan Paho MQTT.
        def _mqtt_callback(client, userdata, msg):
            """Wrapper untuk mengubah callback Paho menjadi `(topic, payload)`."""
            topic = msg.topic
            payload = msg.payload.decode()
            self._on_mqtt_message(topic, payload)

        self.mqtt.subscribe(smartsocket_wildcard, _mqtt_callback)
        if self.logger:
            self.logger(f"[SmartSocket Manager] Subscribed: {smartsocket_wildcard}")

    def _on_mqtt_message(self, topic, payload):
        """Merutekan MQTT message ke backend socket yang sesuai."""
        # Parse topic: ecolab/socket/{N}/xxx
        parts = topic.split("/")
        if len(parts) >= 3:
            try:
                socket_num = int(parts[2])
                if socket_num in self.backends:
                    self.backends[socket_num].on_message(topic, payload)
            except ValueError:
                pass

    def get_backend(self, socket_number):
        """Mengambil backend untuk nomor socket tertentu."""
        return self.backends.get(socket_number)

    def start(self):
        """Menandai manager mulai aktif memonitor semua socket."""
        if self.logger:
            self.logger("[SmartSocket Manager] Started monitoring 5 sockets")
