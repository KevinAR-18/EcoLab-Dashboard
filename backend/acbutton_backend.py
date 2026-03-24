class ACButtonBackend:
    """
    Backend MQTT untuk kontrol AC
    - Tidak tahu UI
    - Tidak tahu Lamp / DHT
    - Hanya publish command AC
    """

    TOPIC_AC = "ecolab/mcuB/ac/control"
    STATUS_TOPIC = "ecolab/mcuB/ac/status"

    def __init__(self, mqtt_client, logger=None):
        self.mqtt = mqtt_client
        self.logger = logger
        self.state = None

    def temp_up(self):
        self.mqtt.publish(self.TOPIC_AC, "TEMP_UP")
        print(f"[MQTT] {self.TOPIC_AC} -> TEMP_UP")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> TEMP_UP")

    def temp_down(self):
        self.mqtt.publish(self.TOPIC_AC, "TEMP_DOWN")
        print(f"[MQTT] {self.TOPIC_AC} -> TEMP_DOWN")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> TEMP_DOWN")

    def mode_cool(self):
        self.mqtt.publish(self.TOPIC_AC, "MODE_COOL")
        print(f"[MQTT] {self.TOPIC_AC} -> MODE_COOL")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> MODE_COOL")

    def mode_fan(self):
        self.mqtt.publish(self.TOPIC_AC, "MODE_FAN")
        print(f"[MQTT] {self.TOPIC_AC} -> MODE_FAN")
        if self.logger:
            self.logger(f"[MQTT] {self.TOPIC_AC} -> MODE_FAN")

    def start(self):
        # Subscribe ke status AC dari MCU (Opsi 1: MCU Source of Truth)
        self.mqtt.subscribe(self.STATUS_TOPIC, self._on_status)

    def power(self, state: bool):
        """
        Publish command ke MCU
        Topic: ecolab/mcuB/ac/control
        Payload: ON/OFF
        """
        payload = "ON" if state else "OFF"
        self.mqtt.publish(self.TOPIC_AC, payload)

        self.state = state

        if self.logger:
            self.logger(f"[AC] {self.TOPIC_AC} -> {payload}")

    def _on_status(self, client, userdata, msg):
        """
        Terima status dari MCU
        Topic: ecolab/mcuB/ac/status
        """
        self.state = msg.payload.decode() == "ON"
