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
        self.states = {}


    def set_lamp(self, lamp_index: int, state: bool):
        topic = f"{self.BASE_TOPIC}{lamp_index}"
        payload = "ON" if state else "OFF"
        print(f"[MQTT] {topic} -> {payload}")
        if self.logger:
            self.logger(f"[MQTT] {topic} -> {payload}")
        self.mqtt.publish(topic, payload)

    def start(self):
        for i in range(1, 6):
            topic = f"ui/mcuA/lamp{i}/state"
            self.mqtt.subscribe(topic, self._on_state)

            # publish default OFF (retain)
            self.mqtt.publish(topic, "OFF", retain=True)

    def _on_state(self, client, userdata, msg):
        lamp_id = int(msg.topic.split("lamp")[1].split("/")[0])
        state = msg.payload.decode().upper() == "ON"
        self.states[lamp_id] = state

        if self.logger:
            self.logger(f"[UI STATE] Lamp {lamp_id} = {state}")
    
    def publish(self, lamp_id, state):
        payload = "ON" if state else "OFF"

        self.mqtt.publish(
            f"ui/mcuA/lamp{lamp_id}/state",
            payload,
            retain=True
        )

        self.mqtt.publish(
            f"mcuA/lamp{lamp_id}",
            payload
        )

        self.states[lamp_id] = state

        if self.logger:
            self.logger(f"[MQTT] Lamp {lamp_id} -> {payload}")


