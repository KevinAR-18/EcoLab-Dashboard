"""MQTT-backed online/offline status tracker for the two laboratory MCUs."""


class MCUStatusBackend:
    """Cache the latest heartbeat state for MCU-A and MCU-B."""

    TOPIC_MCU_A = "ecolab/mcuA/status"
    TOPIC_MCU_B = "ecolab/mcuB/status"

    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.mcuA_online = None
        self.mcuB_online = None

    def start(self):
        """Subscribe to both MCU heartbeat topics."""
        self.mqtt.subscribe(self.TOPIC_MCU_A, self._on_message)
        self.mqtt.subscribe(self.TOPIC_MCU_B, self._on_message)

    def _on_message(self, client, userdata, msg):
        """Convert heartbeat payloads into cached boolean state."""
        payload = msg.payload.decode().lower()

        if msg.topic == self.TOPIC_MCU_A:
            self.mcuA_online = payload == "online"
        elif msg.topic == self.TOPIC_MCU_B:
            self.mcuB_online = payload == "online"

    def fetch(self):
        """Return the latest cached status for both MCUs."""
        return {
            "mcuA": self.mcuA_online,
            "mcuB": self.mcuB_online,
        }
