class LampButtonBackend:
    """
    Backend MQTT untuk kontrol lampu
    - Tidak tahu UI
    - Tidak tahu DHT
    - Hanya publish perintah lampu
    """

    BASE_TOPIC = "ecolab/mcuA/lamp"

    def __init__(self, mqtt_client, logger=None):
        self.mqtt = mqtt_client
        self.logger = logger
        self.states = {}

    def set_lamp(self, lamp_index: int, state: bool):
        topic = f"{self.BASE_TOPIC}{lamp_index}/control"
        payload = "ON" if state else "OFF"
        print(f"[MQTT] {topic} -> {payload}")
        if self.logger:
            self.logger(f"[MQTT] {topic} -> {payload}")
        self.mqtt.publish(topic, payload)

    def start(self):
        # Subscribe ke status lampu dari MCU (Opsi 1: MCU Source of Truth)
        for i in range(1, 6):
            topic = f"{self.BASE_TOPIC}{i}/status"
            self.mqtt.subscribe(topic, self._on_status)

    def publish(self, lamp_index: int, state: bool):
        """
        Publish command ke MCU
        Topic: ecolab/mcuA/lamp1-5/control
        Payload: ON/OFF
        """
        topic = f"{self.BASE_TOPIC}{lamp_index}/control"
        payload = "ON" if state else "OFF"

        self.mqtt.publish(topic, payload)
        self.states[lamp_index] = state

        if self.logger:
            self.logger(f"[LAMP] {topic} -> {payload}")

    def _on_status(self, client, userdata, msg):
        """
        Terima status dari MCU
        Topic: ecolab/mcuA/lamp1-5/status
        """
        # Extract lamp index dari topic: ecolab/mcuA/lamp1/status
        lamp_index = int(msg.topic.split("lamp")[1].split("/")[0])
        state = msg.payload.decode() == "ON"
        self.states[lamp_index] = state


