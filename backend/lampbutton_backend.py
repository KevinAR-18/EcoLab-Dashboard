class LampButtonBackend:
    """
    Backend MQTT untuk kontrol lampu
    - Tidak tahu UI
    - Tidak tahu DHT
    - Hanya publish perintah lampu
    """

    BASE_TOPIC = "mcuA/lamp"

    def __init__(self, mqtt_client, logger=None):
        self.mqtt = mqtt_client
        self.logger = logger


    def set_lamp(self, lamp_index: int, state: bool):
        topic = f"{self.BASE_TOPIC}{lamp_index}"
        payload = "ON" if state else "OFF"
        print(f"[MQTT] {topic} -> {payload}")
        if self.logger:
            self.logger(f"[MQTT] {topic} -> {payload}")
        self.mqtt.publish(topic, payload)
