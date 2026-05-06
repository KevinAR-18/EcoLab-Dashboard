"""Backend MQTT untuk kontrol AC di dashboard EcoLab."""

from PySide6.QtCore import QObject, Signal


class ACButtonBackend(QObject):
    """
    Backend MQTT khusus untuk kontrol AC.

    Class ini tidak menangani UI secara langsung.
    Tugasnya fokus pada publish command AC dan menerima status balik dari MCU.
    """

    TOPIC_AC = "ecolab/mcuB/ac/control"
    STATUS_TOPIC = "ecolab/mcuB/ac/status"

    # Signal untuk memberi tahu UI saat state AC berubah.
    status_changed = Signal(bool)  # AC state: True=ON, False=OFF

    def __init__(self, mqtt_client, logger=None):
        """Menyimpan client MQTT, logger, dan cache state AC terakhir."""
        super().__init__()
        self.mqtt = mqtt_client
        self.logger = logger
        self.state = None

    def temp_up(self):
        """Mengirim command untuk menaikkan temperatur AC."""
        self.mqtt.publish(self.TOPIC_AC, "TEMP_UP")
        print(f"[MQTT] {self.TOPIC_AC} -> TEMP_UP")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> TEMP_UP")

    def temp_down(self):
        """Mengirim command untuk menurunkan temperatur AC."""
        self.mqtt.publish(self.TOPIC_AC, "TEMP_DOWN")
        print(f"[MQTT] {self.TOPIC_AC} -> TEMP_DOWN")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> TEMP_DOWN")

    def mode_cool(self):
        """Mengirim command untuk mengganti mode AC ke cool."""
        self.mqtt.publish(self.TOPIC_AC, "MODE_COOL")
        print(f"[MQTT] {self.TOPIC_AC} -> MODE_COOL")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> MODE_COOL")

    def mode_fan(self):
        """Mengirim command untuk mengganti mode AC ke fan."""
        self.mqtt.publish(self.TOPIC_AC, "MODE_FAN")
        print(f"[MQTT] {self.TOPIC_AC} -> MODE_FAN")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> MODE_FAN")

    def start(self):
        """Mulai subscribe topic status AC dari MCU."""
        self.mqtt.subscribe(self.STATUS_TOPIC, self._on_status)

    def power(self, state: bool):
        """
        Mengirim command power AC ke MCU.

        Payload yang dikirim adalah `ON` atau `OFF`.
        """
        payload = "ON" if state else "OFF"
        self.mqtt.publish(self.TOPIC_AC, payload)

        self.state = state

        if self.logger:
            self.logger(f"[AC] {self.TOPIC_AC} -> {payload}")

    def _on_status(self, client, userdata, msg):
        """Menerima status AC dari MCU lalu emit ke UI lewat signal."""
        self.state = msg.payload.decode() == "ON"
        self.status_changed.emit(self.state)
