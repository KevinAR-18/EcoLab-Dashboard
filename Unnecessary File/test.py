import time

from backend.mqtt_client import MqttClient
from backend.mqtt_dht22_backend import DHT22MQTTBackend


def main():
    print("=== TEST MQTT DHT22 BACKEND ===")

    # 1. Buat MQTT core
    mqtt = MqttClient(
        broker="10.33.11.148",   # GANTI sesuai broker kamu
        port=1883
    )

    mqtt.start()
    print("[TEST] MQTT client started")

    # 2. Buat backend DHT22
    dht = DHT22MQTTBackend(mqtt)
    dht.start()
    print("[TEST] DHT22 backend started")

    print("[TEST] Menunggu data DHT22...\n")

    # 3. Loop baca data
    while True:
        data = dht.fetch()

        tempA = data.get("temp_A")
        humA = data.get("hum_A")
        tempB = data.get("temp_B")
        humB = data.get("hum_B")
        avgT = data.get("avg_temperature")
        avgH = data.get("avg_humidity")

        print(
            f"T_A={tempA} °C | H_A={humA} % | "
            f"T_B={tempB} °C | H_B={humB} % | "
            f"AVG_T={avgT} °C | AVG_H={avgH} %"
        )

        time.sleep(1)


if __name__ == "__main__":
    main()







