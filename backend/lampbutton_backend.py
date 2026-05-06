"""Backend MQTT untuk kontrol lampu di dashboard EcoLab."""

from PySide6.QtCore import QObject, Signal


class LampButtonBackend(QObject):
    """
    Backend MQTT khusus untuk kontrol lampu.

    Class ini tidak menangani UI secara langsung.
    Tugasnya fokus pada publish command lampu dan menerima status balik dari MCU.
    """

    BASE_TOPIC = "ecolab/mcuA/lamp"

    # Signal untuk memberi tahu UI saat status lampu berubah.
    status_changed = Signal(int, bool)  # lamp_index, state

    def __init__(self, mqtt_client, logger=None):
        """Menyimpan client MQTT, logger, dan cache state semua lampu."""
        super().__init__()
        self.mqtt = mqtt_client
        self.logger = logger
        self.states = {}

    def set_lamp(self, lamp_index: int, state: bool):
        """Mengirim command ON/OFF untuk satu lampu tertentu."""
        topic = f"{self.BASE_TOPIC}{lamp_index}/control"
        payload = "ON" if state else "OFF"
        print(f"[MQTT] {topic} -> {payload}")
        if self.logger:
            self.logger(f"[MQTT] {topic} -> {payload}")
        self.mqtt.publish(topic, payload)

    def start(self):
        """Mulai subscribe semua topic status lampu dari MCU."""
        for i in range(1, 6):
            topic = f"{self.BASE_TOPIC}{i}/status"
            self.mqtt.subscribe(topic, self._on_status)

    def publish(self, lamp_index: int, state: bool):
        """Mengirim command lampu ke MCU dan menyimpan state lokal sementara."""
        topic = f"{self.BASE_TOPIC}{lamp_index}/control"
        payload = "ON" if state else "OFF"

        self.mqtt.publish(topic, payload)
        self.states[lamp_index] = state

        if self.logger:
            self.logger(f"[LAMP] {topic} -> {payload}")

    def _on_status(self, client, userdata, msg):
        """Menerima status lampu dari MCU lalu emit ke UI lewat signal."""
        lamp_index = int(msg.topic.split("lamp")[1].split("/")[0])
        state = msg.payload.decode() == "ON"
        self.states[lamp_index] = state
        self.status_changed.emit(lamp_index, state)
