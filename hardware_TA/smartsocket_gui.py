import sys
import os
import json
import ssl
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QLineEdit,
                               QGroupBox, QComboBox, QGridLayout)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPalette, QColor
import paho.mqtt.client as mqtt


# ================= MQTT CONFIG =================
BROKER = "DESKTOP-CVPE153"
PORT = 8883
USERNAME = "dashboard"
PASSWORD = "ecolab123"

CA_CERT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")

# MQTT Topics
TOPIC_CONTROL = "ecolab/socket/1/control"
TOPIC_ENERGY = "ecolab/socket/1/energy"
TOPIC_DEVICE_STATUS = "ecolab/socket/1/devicestatus"
TOPIC_RELAY_STATUS = "ecolab/socket/1/relaystatus"
TOPIC_TIMER = "ecolab/socket/1/timer"
TOPIC_TIMER_STATUS = "ecolab/socket/1/timer/status"
TOPIC_SCHEDULE_START = "ecolab/socket/1/schedule/start"
TOPIC_SCHEDULE_STOP = "ecolab/socket/1/schedule/stop"
TOPIC_SCHEDULE_MODE = "ecolab/socket/1/schedule/mode"
TOPIC_SCHEDULE_STATUS = "ecolab/socket/1/schedule/status"
# TOPIC_DATETIME_SET tidak dipakai lagi (NTP sync)
TOPIC_DATETIME_STATUS = "ecolab/socket/1/datetime/status"


# ================= MQTT THREAD =================
class MQTTThread(QThread):
    energy_data = Signal(dict)
    relay_status = Signal(str)
    device_status = Signal(str)
    timer_status = Signal(str)
    schedule_status = Signal(str)
    datetime_status = Signal(str)
    connected = Signal()

    def __init__(self):
        super().__init__()
        self.client = None
        self.running = True

    def run(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(USERNAME, PASSWORD)
        self.client.tls_set(
            ca_certs=CA_CERT_PATH,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()

            while self.running:
                self.msleep(100)

        except Exception as e:
            print(f"MQTT Error: {e}")

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code: {rc}")
        self.connected.emit()

        client.subscribe(TOPIC_ENERGY)
        client.subscribe(TOPIC_RELAY_STATUS)
        client.subscribe(TOPIC_DEVICE_STATUS)
        client.subscribe(TOPIC_TIMER_STATUS)
        client.subscribe(TOPIC_SCHEDULE_STATUS)
        client.subscribe(TOPIC_DATETIME_STATUS)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic == TOPIC_ENERGY:
            try:
                data = json.loads(payload)
                self.energy_data.emit(data)
            except:
                pass

        elif topic == TOPIC_RELAY_STATUS:
            self.relay_status.emit(payload)

        elif topic == TOPIC_DEVICE_STATUS:
            self.device_status.emit(payload)

        elif topic == TOPIC_TIMER_STATUS:
            self.timer_status.emit(payload)

        elif topic == TOPIC_SCHEDULE_STATUS:
            self.schedule_status.emit(payload)

        elif topic == TOPIC_DATETIME_STATUS:
            self.datetime_status.emit(payload)

    def publish(self, topic, message):
        if self.client:
            self.client.publish(topic, message)

    def stop(self):
        self.running = False
        if self.client:
            self.client.loop_stop()
        self.wait()


# ================= MAIN WINDOW =================
class SmartSocketGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.relay_on = False
        self.init_ui()
        self.init_mqtt()

    def init_ui(self):
        self.setWindowTitle("EcoLab Smart Socket Control")
        self.setGeometry(100, 100, 550, 750)  # Tambah tinggi untuk tombol cancel/clear

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("⚡ Smart Socket Dashboard")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Device Status
        self.device_status_label = QLabel("🔴 Device: OFFLINE")
        self.device_status_label.setFont(QFont("Arial", 12))
        self.device_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.device_status_label)

        # ================= ENERGY DISPLAY =================
        energy_group = QGroupBox("📊 Energy Monitor")
        energy_layout = QVBoxLayout()

        self.voltage_label = self.create_value_label("Voltage", "-- V")
        self.current_label = self.create_value_label("Current", "-- A")
        self.power_label = self.create_value_label("Power", "-- W")
        self.energy_label = self.create_value_label("Energy", "-- kWh")
        self.freq_label = self.create_value_label("Frequency", "-- Hz")
        self.pf_label = self.create_value_label("Power Factor", "--")

        energy_layout.addWidget(self.voltage_label)
        energy_layout.addWidget(self.current_label)
        energy_layout.addWidget(self.power_label)
        energy_layout.addWidget(self.energy_label)
        energy_layout.addWidget(self.freq_label)
        energy_layout.addWidget(self.pf_label)

        energy_group.setLayout(energy_layout)
        layout.addWidget(energy_group)

        # ================= RELAY CONTROL =================
        relay_group = QGroupBox("🎛️ Relay Control")
        relay_layout = QVBoxLayout()

        self.status_label = QLabel("Status: OFF")
        self.status_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        relay_layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        self.btn_on = QPushButton("ON")
        self.btn_on.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_on.setFixedHeight(50)
        self.btn_on.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_on.clicked.connect(lambda: self.send_control("ON"))

        self.btn_off = QPushButton("OFF")
        self.btn_off.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_off.setFixedHeight(50)
        self.btn_off.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #b9150a;
            }
        """)
        self.btn_off.clicked.connect(lambda: self.send_control("OFF"))

        btn_layout.addWidget(self.btn_on)
        btn_layout.addWidget(self.btn_off)
        relay_layout.addLayout(btn_layout)

        relay_group.setLayout(relay_layout)
        layout.addWidget(relay_group)

        # ================= TIMER CONTROL =================
        timer_group = QGroupBox("⏱️ Timer")
        timer_layout = QVBoxLayout()

        timer_input_layout = QHBoxLayout()
        timer_input_layout.addWidget(QLabel("Duration (seconds):"))
        self.timer_input = QLineEdit()
        self.timer_input.setPlaceholderText("60")
        timer_input_layout.addWidget(self.timer_input)

        self.btn_timer = QPushButton("Start Timer")
        self.btn_timer.clicked.connect(self.send_timer)
        self.btn_timer.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)

        self.btn_cancel_timer = QPushButton("Cancel Timer")
        self.btn_cancel_timer.clicked.connect(self.cancel_timer)
        self.btn_cancel_timer.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        self.timer_status_label = QLabel("Status: INACTIVE")
        self.timer_status_label.setStyleSheet("color: gray;")

        timer_layout.addLayout(timer_input_layout)
        timer_layout.addWidget(self.btn_timer)
        timer_layout.addWidget(self.btn_cancel_timer)
        timer_layout.addWidget(self.timer_status_label)

        timer_group.setLayout(timer_layout)
        layout.addWidget(timer_group)

        # ================= SCHEDULE CONTROL (UPDATED) =================
        schedule_group = QGroupBox("📅 Schedule")
        schedule_layout = QVBoxLayout()

        # Mode Selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.schedule_mode_combo = QComboBox()
        self.schedule_mode_combo.addItems(["Daily", "Onetime"])
        self.schedule_mode_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border-radius: 3px;
            }
        """)
        mode_layout.addWidget(self.schedule_mode_combo)
        schedule_layout.addLayout(mode_layout)

        # Start Time
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Time (ON):"))
        self.schedule_start_input = QLineEdit()
        self.schedule_start_input.setPlaceholderText("08:00")
        start_layout.addWidget(self.schedule_start_input)
        schedule_layout.addLayout(start_layout)

        # Stop Time
        stop_layout = QHBoxLayout()
        stop_layout.addWidget(QLabel("Stop Time (OFF):"))
        self.schedule_stop_input = QLineEdit()
        self.schedule_stop_input.setPlaceholderText("17:00")
        stop_layout.addWidget(self.schedule_stop_input)
        schedule_layout.addLayout(stop_layout)

        # Set Schedule Button
        self.btn_schedule = QPushButton("Set Schedule")
        self.btn_schedule.clicked.connect(self.send_schedule)
        self.btn_schedule.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)

        # Clear Schedule Button
        self.btn_clear_schedule = QPushButton("Clear Schedule")
        self.btn_clear_schedule.clicked.connect(self.clear_schedule)
        self.btn_clear_schedule.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        # Status Display (Shows current schedule config)
        self.schedule_status_label = QLabel("Status: Not Set")
        self.schedule_status_label.setStyleSheet("color: gray;")
        self.schedule_status_label.setWordWrap(True)

        schedule_layout.addWidget(self.btn_schedule)
        schedule_layout.addWidget(self.btn_clear_schedule)
        schedule_layout.addWidget(self.schedule_status_label)

        schedule_group.setLayout(schedule_layout)
        layout.addWidget(schedule_group)

        # ================= DATETIME SYNC (NTP AUTO-SYNC) =================
        datetime_group = QGroupBox("🕐 RTC DateTime (NTP Sync)")
        datetime_layout = QVBoxLayout()

        # RTC Status Label
        self.datetime_status_label = QLabel("RTC: Syncing from NTP...")
        self.datetime_status_label.setStyleSheet("color: gray; font-size: 11pt;")
        self.datetime_status_label.setWordWrap(True)
        datetime_layout.addWidget(self.datetime_status_label)

        # Info label (no button, auto-sync from NTP)
        info_label = QLabel("ℹ️ RTC auto-synced from NTP time server")
        info_label.setStyleSheet("color: blue; font-size: 9pt; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        datetime_layout.addWidget(info_label)

        datetime_group.setLayout(datetime_layout)
        layout.addWidget(datetime_group)

        layout.addStretch()

    def create_value_label(self, name, value):
        label = QLabel(f"{name}: {value}")
        label.setFont(QFont("Arial", 11))
        return label

    def init_mqtt(self):
        self.mqtt_thread = MQTTThread()
        self.mqtt_thread.energy_data.connect(self.update_energy)
        self.mqtt_thread.relay_status.connect(self.update_relay_status)
        self.mqtt_thread.device_status.connect(self.update_device_status)
        self.mqtt_thread.timer_status.connect(self.update_timer_status)
        self.mqtt_thread.schedule_status.connect(self.update_schedule_status)
        self.mqtt_thread.datetime_status.connect(self.update_datetime_status)
        self.mqtt_thread.start()

    def update_energy(self, data):
        # Voltage: SELALU tampil
        self.voltage_label.setText(f"Voltage: {data['voltage']} V")

        # Frequency: SELALU tampil
        self.freq_label.setText(f"Frequency: {data['frequency']} Hz")

        # Cek threshold current > 0 untuk menampilkan data beban
        if data['current'] > 0:
            # Ada beban → tampil nilai asli
            self.current_label.setText(f"Current: {data['current']} A")
            self.power_label.setText(f"Power: {data['power']} W")
            self.energy_label.setText(f"Energy: {data['energy']} kWh")
            self.pf_label.setText(f"Power Factor: {data['pf']}")
        else:
            # Tidak ada beban → tampil 0
            self.current_label.setText(f"Current: 0 A")
            self.power_label.setText(f"Power: 0 W")
            self.energy_label.setText(f"Energy: 0 kWh")
            self.pf_label.setText(f"Power Factor: 0")

    def update_relay_status(self, status):
        self.relay_on = (status == "ON")
        if self.relay_on:
            self.status_label.setText("Status: ON")
            self.status_label.setStyleSheet("color: green; font-size: 14pt; font-weight: bold;")
        else:
            self.status_label.setText("Status: OFF")
            self.status_label.setStyleSheet("color: red; font-size: 14pt; font-weight: bold;")

    def update_device_status(self, status):
        if status == "ONLINE":
            self.device_status_label.setText("🟢 Device: ONLINE")
            self.device_status_label.setStyleSheet("color: green; font-size: 12pt;")
        else:
            self.device_status_label.setText("🔴 Device: OFFLINE")
            self.device_status_label.setStyleSheet("color: red; font-size: 12pt;")

    def update_timer_status(self, status):
        self.timer_status_label.setText(f"Status: {status}")

        if "ACTIVE" in status:
            self.timer_status_label.setStyleSheet("color: green; font-weight: bold;")
        elif "INACTIVE" in status:
            self.timer_status_label.setStyleSheet("color: gray;")
        elif "DONE" in status:
            self.timer_status_label.setStyleSheet("color: blue;")
        else:
            self.timer_status_label.setStyleSheet("color: orange;")

    def update_schedule_status(self, status):
        try:
            # Parse JSON format: {"start":"08:00","stop":"17:00","mode":"daily"}
            data = json.loads(status)

            start = data.get('start', 'null')
            stop = data.get('stop', 'null')
            mode = data.get('mode', 'unknown')

            # HANYA update status label, JANGAN update input field
            if start != 'null' and stop != 'null':
                mode_display = "Daily" if mode == "daily" else "One-time"
                display_text = f"Status: ACTIVE\nStart: {start} | Stop: {stop}\nMode: {mode_display}"
                self.schedule_status_label.setText(display_text)
                self.schedule_status_label.setStyleSheet("color: green; font-weight: bold;")

            elif start != 'null':
                self.schedule_status_label.setText(f"Status: Start Set: {start}")
                self.schedule_status_label.setStyleSheet("color: orange;")

            elif stop != 'null':
                self.schedule_status_label.setText(f"Status: Stop Set: {stop}")
                self.schedule_status_label.setStyleSheet("color: orange;")

            else:
                self.schedule_status_label.setText("Status: Not Set")
                self.schedule_status_label.setStyleSheet("color: gray;")

        except json.JSONDecodeError:
            # Legacy format or error message
            self.schedule_status_label.setText(f"Status: {status}")
            if "ERROR" in status:
                self.schedule_status_label.setStyleSheet("color: red;")

    def send_control(self, command):
        self.mqtt_thread.publish(TOPIC_CONTROL, command)
        print(f"Sent: {command}")

    def send_timer(self):
        duration = self.timer_input.text()
        if duration.isdigit():
            self.mqtt_thread.publish(TOPIC_TIMER, duration)
            print(f"Timer sent: {duration} seconds")
        else:
            self.timer_status_label.setText("Status: Invalid input!")
            self.timer_status_label.setStyleSheet("color: red;")

    def cancel_timer(self):
        self.mqtt_thread.publish(TOPIC_TIMER, "0")
        print("Timer cancelled")
        self.timer_status_label.setText("Status: Cancelling...")
        self.timer_status_label.setStyleSheet("color: orange;")

    def send_schedule(self):
        # Validate and send start time
        start_time = self.schedule_start_input.text().strip()
        if start_time:
            if self.validate_time_format(start_time):
                self.mqtt_thread.publish(TOPIC_SCHEDULE_START, start_time)
                print(f"Schedule start sent: {start_time}")
            else:
                self.schedule_status_label.setText("Status: Invalid start format (HH:MM)")
                self.schedule_status_label.setStyleSheet("color: red;")
                return
        else:
            # Jika start kosong, user hanya mau set stop time
            pass

        # Validate and send stop time
        stop_time = self.schedule_stop_input.text().strip()
        if stop_time:
            if self.validate_time_format(stop_time):
                self.mqtt_thread.publish(TOPIC_SCHEDULE_STOP, stop_time)
                print(f"Schedule stop sent: {stop_time}")
            else:
                self.schedule_status_label.setText("Status: Invalid stop format (HH:MM)")
                self.schedule_status_label.setStyleSheet("color: red;")
                return
        else:
            # Jika stop kosong, user hanya mau set start time
            pass

        # Send mode (selalu kirim mode jika ada start/stop)
        if start_time or stop_time:
            mode = "daily" if self.schedule_mode_combo.currentIndex() == 0 else "onetime"
            self.mqtt_thread.publish(TOPIC_SCHEDULE_MODE, mode)
            print(f"Schedule mode sent: {mode}")

            # Feedback sementara sampai dapat update dari ESP32
            self.schedule_status_label.setText("Status: Setting...")
            self.schedule_status_label.setStyleSheet("color: blue;")

    def validate_time_format(self, time_str):
        try:
            parts = time_str.split(':')
            if len(parts) == 2:
                hour = int(parts[0])
                minute = int(parts[1])
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    return True
            return False
        except:
            return False

    def clear_schedule(self):
        # Kirim CLEAR ke start dan stop schedule
        self.mqtt_thread.publish(TOPIC_SCHEDULE_START, "CLEAR")
        self.mqtt_thread.publish(TOPIC_SCHEDULE_STOP, "CLEAR")

        # Reset mode ke default
        self.mqtt_thread.publish(TOPIC_SCHEDULE_MODE, "daily")

        # Clear input fields
        self.schedule_start_input.setText("")
        self.schedule_stop_input.setText("")

        print("Schedule cleared")
        self.schedule_status_label.setText("Status: Clearing...")
        self.schedule_status_label.setStyleSheet("color: orange;")

    def update_datetime_status(self, status):
        """Update RTC datetime status from ESP32"""
        if status.startswith("OK:NTP_SYNCED:"):
            # Format: "OK:NTP_SYNCED:2026-03-22 14:30:00 5"
            datetime_str = status[14:]  # Remove "OK:NTP_SYNCED:" prefix
            self.datetime_status_label.setText(f"🟢 RTC: {datetime_str}")
            self.datetime_status_label.setStyleSheet("color: green; font-size: 10pt;")
        elif status.startswith("INFO:"):
            # Info message (e.g., manual sync disabled)
            self.datetime_status_label.setText(f"ℹ️ {status[5:]}")
            self.datetime_status_label.setStyleSheet("color: blue; font-size: 10pt;")
        elif status.startswith("ERROR:"):
            self.datetime_status_label.setText(f"⚠️ {status}")
            self.datetime_status_label.setStyleSheet("color: orange; font-size: 10pt;")
        else:
            self.datetime_status_label.setText(f"RTC: {status}")
            self.datetime_status_label.setStyleSheet("color: gray; font-size: 10pt;")

    def closeEvent(self, event):
        self.mqtt_thread.stop()
        event.accept()


# ================= MAIN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SmartSocketGUI()
    window.show()

    sys.exit(app.exec())
