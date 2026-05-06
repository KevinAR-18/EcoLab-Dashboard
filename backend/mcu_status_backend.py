"""Tracker status online/offline kedua MCU berbasis MQTT."""


class MCUStatusBackend:
    """Menyimpan cache heartbeat terbaru untuk MCU-A dan MCU-B."""

    TOPIC_MCU_A = "ecolab/mcuA/status"
    TOPIC_MCU_B = "ecolab/mcuB/status"

    def __init__(self, mqtt):
        """Menyimpan client MQTT dan menyiapkan state awal kedua MCU."""
        self.mqtt = mqtt
        self.mcuA_online = None
        self.mcuB_online = None

    def start(self):
        """Mulai subscribe kedua topic heartbeat MCU."""
        self.mqtt.subscribe(self.TOPIC_MCU_A, self._on_message)
        self.mqtt.subscribe(self.TOPIC_MCU_B, self._on_message)

    def _on_message(self, client, userdata, msg):
        """Mengubah payload heartbeat menjadi state boolean yang dicache."""
        payload = msg.payload.decode().lower()

        if msg.topic == self.TOPIC_MCU_A:
            self.mcuA_online = payload == "online"
        elif msg.topic == self.TOPIC_MCU_B:
            self.mcuB_online = payload == "online"

    def fetch(self):
        """Mengembalikan status terbaru kedua MCU dari cache."""
        return {
            "mcuA": self.mcuA_online,
            "mcuB": self.mcuB_online,
        }
