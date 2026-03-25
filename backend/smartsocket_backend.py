#!/usr/bin/env python3
"""
EcoLab Smart Socket MQTT Backend
Handle MQTT communication for Smart Socket devices
"""

import json
from PySide6.QtCore import QObject, Signal


class SmartSocketBackend(QObject):
    """Backend untuk single Smart Socket device"""

    # Signals untuk update GUI
    status_changed = Signal(bool)  # Relay state: True=ON, False=OFF
    energy_changed = Signal(dict)  # Energy data: {voltage, current, power, energy, frequency, pf}
    timer_status_changed = Signal(str)  # Timer status: "ACTIVE:XXs" / "INACTIVE"
    schedule_status_changed = Signal(str)  # Schedule JSON string
    device_status_changed = Signal(bool)  # Device online: True=ONLINE, False=OFFLINE

    def __init__(self, mqtt_client, socket_number, logger=None):
        super().__init__()
        self.mqtt = mqtt_client
        self.socket_number = socket_number
        self.logger = logger

        # State storage
        self.relay_state = None
        self.energy_data = {}
        self.timer_status = "INACTIVE"
        self.schedule_status = {}
        self.device_online = False

        # MQTT topics
        self.topic_prefix = f"ecolab/socket/{socket_number}"
        self.topics = {
            "relay": f"{self.topic_prefix}/relaystatus",
            "energy": f"{self.topic_prefix}/energy",
            "timer": f"{self.topic_prefix}/timer/status",
            "schedule": f"{self.topic_prefix}/schedule/status",
            "device": f"{self.topic_prefix}/devicestatus",
        }

        # Tidak perlu subscribe di sini, akan di-handle oleh Manager via register_handler
        if self.logger:
            self.logger(f"[Smart Socket {self.socket_number}] Backend initialized")

    def _subscribe_topics(self):
        """Method ini tidak dipakai - subscribe di-handle oleh Manager"""
        pass

    def on_message(self, topic, payload):
        """Handle MQTT message yang diterima"""
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
        """Handle relay status update"""
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
        """Handle energy data update"""
        try:
            data = json.loads(payload)
            self.energy_data = data
            self.energy_changed.emit(data)
            # Log hanya jika ada perubahan signifikan (optional)
            if self.logger and data.get("power", 0) > 0:
                v = data.get("voltage", 0)
                i = data.get("current", 0)
                p = data.get("power", 0)
                self.logger(f"[Socket {self.socket_number}] Energy: {v}V, {i}A, {p}W")
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger(f"[Socket {self.socket_number}] Error parsing energy: {e}")

    def _handle_timer_status(self, payload):
        """Handle timer status update"""
        if payload != self.timer_status:
            self.timer_status = payload
            self.timer_status_changed.emit(payload)
            if self.logger:
                self.logger(f"[Socket {self.socket_number}] Timer: {payload}")

    def _handle_schedule_status(self, payload):
        """Handle schedule status update"""
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
            # Jika bukan JSON, simpan sebagai string biasa
            self.schedule_status = {"raw": payload}
            self.schedule_status_changed.emit(payload)

    def _handle_device_status(self, payload):
        """Handle device status update (ONLINE/OFFLINE)"""
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

    # ================= PUBLISH METHODS =================

    def set_relay(self, state):
        """Publish relay control command"""
        payload = "ON" if state else "OFF"
        topic = f"{self.topic_prefix}/control"  # ecolab/socket/1/control
        self.mqtt.publish(topic, payload)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Control: {payload}")

    def set_timer(self, duration_seconds):
        """Publish timer command"""
        topic = f"{self.topic_prefix}/timer"
        self.mqtt.publish(topic, str(duration_seconds))
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Timer: {duration_seconds}s")

    def cancel_timer(self):
        """Cancel active timer"""
        self.set_timer(0)

    def set_schedule_start(self, time_str):
        """Set schedule start time (HH:MM or CLEAR)"""
        topic = f"{self.topic_prefix}/schedule/start"
        self.mqtt.publish(topic, time_str)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Schedule Start: {time_str}")

    def set_schedule_stop(self, time_str):
        """Set schedule stop time (HH:MM or CLEAR)"""
        topic = f"{self.topic_prefix}/schedule/stop"
        self.mqtt.publish(topic, time_str)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Schedule Stop: {time_str}")

    def set_schedule_mode(self, mode):
        """Set schedule mode (daily/onetime)"""
        topic = f"{self.topic_prefix}/schedule/mode"
        self.mqtt.publish(topic, mode)
        if self.logger:
            self.logger(f"[Socket {self.socket_number}] Schedule Mode: {mode}")

    def clear_schedule(self):
        """Clear all schedule settings"""
        self.set_schedule_start("CLEAR")
        self.set_schedule_stop("CLEAR")


class SmartSocketManager(QObject):
    """Manager untuk semua Smart Socket devices (1-5)"""

    def __init__(self, mqtt_client, logger=None):
        super().__init__()
        self.mqtt = mqtt_client
        self.logger = logger
        self.backends = {}

        # Create backend untuk 5 socket
        for i in range(1, 6):
            self.backends[i] = SmartSocketBackend(mqtt_client, i, logger)

        # Subscribe ke semua smart socket topics menggunakan wildcard
        smartsocket_wildcard = "ecolab/socket/#"

        # Buat wrapper function untuk callback sesuai signature Paho MQTT
        def _mqtt_callback(client, userdata, msg):
            """Wrapper untuk convert Paho MQTT callback ke (topic, payload)"""
            topic = msg.topic
            payload = msg.payload.decode()
            self._on_mqtt_message(topic, payload)

        self.mqtt.subscribe(smartsocket_wildcard, _mqtt_callback)
        if self.logger:
            self.logger(f"[SmartSocket Manager] Subscribed: {smartsocket_wildcard}")

        # Request initial status dari semua devices (trigger retained message)
        # Subscribe ke status topics untuk mendapatkan retained message
        for i in range(1, 6):
            status_topic = f"ecolab/socket/{i}/devicestatus"
            self.mqtt.subscribe(status_topic, _mqtt_callback)
            if self.logger:
                self.logger(f"[SmartSocket Manager] Requested status: {status_topic}")

    def _on_mqtt_message(self, topic, payload):
        """Route MQTT message ke backend yang sesuai"""
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
        """Get backend untuk specific socket"""
        return self.backends.get(socket_number)

    def start(self):
        """Start all backends"""
        if self.logger:
            self.logger("[SmartSocket Manager] Started monitoring 5 sockets")
