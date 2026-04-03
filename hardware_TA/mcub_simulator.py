#!/usr/bin/env python3
"""
EcoLab MCU B Simulator (Python)
Menirukan ESP32 untuk kontrol AC + DHT

- Subscribe: ecolab/mcuB/ac/control
import os
- Publish: ecolab/mcuB/ac/status
- Publish: ecolab/mcuB/dht/temperature, ecolab/mcuB/dht/humidity
- LWT: ecolab/mcuB/status
"""

import random
import time
import ssl
import paho.mqtt.client as mqtt
import os

# ============================================================
# CONFIG
# ============================================================
MQTT_BROKER = "DESKTOP-CVPE153"  # Ganti dengan IP broker
# MQTT_BROKER = "10.33.11.148"
MQTT_PORT = 8883  # TLS
MQTT_USERNAME = "mcub"
MQTT_PASSWORD = "mcub123"
# CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")
CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca2.crt")

# Topics
TOPIC_AC_CONTROL = "ecolab/mcuB/ac/control"
TOPIC_AC_STATUS = "ecolab/mcuB/ac/status"
TOPIC_DHT_TEMP = "ecolab/mcuB/dht/temperature"
TOPIC_DHT_HUM = "ecolab/mcuB/dht/humidity"
TOPIC_MCU_STATUS = "ecolab/mcuB/status"

# ============================================================
# STATE
# ============================================================
ac_state = False  # ON/OFF
ac_temperature = 24  # Default temperature
ac_mode = "COOL"  # COOL or FAN
client = None

# ============================================================
# MQTT CALLBACKS
# ============================================================
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code: {rc}")

    # Subscribe to AC command topic
    client.subscribe(TOPIC_AC_CONTROL)
    print(f"[MQTT] Subscribed: {TOPIC_AC_CONTROL}")

    # Send initial status
    send_mcu_status("ONLINE")
    send_ac_status()

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected: {rc}")

def on_message(client, userdata, msg):
    global ac_state, ac_temperature, ac_mode

    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\n[MQTT] Received: {topic} -> {payload}")

    if topic == TOPIC_AC_CONTROL:
        if payload == "ON":
            ac_state = True
            print(f"[AC] Power: ON")
            send_ac_status()

        elif payload == "OFF":
            ac_state = False
            print(f"[AC] Power: OFF")
            send_ac_status()

        elif payload == "TEMP_UP":
            if ac_state:
                ac_temperature = min(ac_temperature + 1, 30)  # Max 30°C
                print(f"[AC] Temperature: {ac_temperature}°C")
            else:
                print("[AC] Cannot change temp: AC is OFF")

        elif payload == "TEMP_DOWN":
            if ac_state:
                ac_temperature = max(ac_temperature - 1, 16)  # Min 16°C
                print(f"[AC] Temperature: {ac_temperature}°C")
            else:
                print("[AC] Cannot change temp: AC is OFF")

        elif payload == "MODE_COOL":
            if ac_state:
                ac_mode = "COOL"
                print(f"[AC] Mode: COOL")
            else:
                print("[AC] Cannot change mode: AC is OFF")

        elif payload == "MODE_FAN":
            if ac_state:
                ac_mode = "FAN"
                print(f"[AC] Mode: FAN")
            else:
                print("[AC] Cannot change mode: AC is OFF")

# ============================================================
# CONTROL FUNCTIONS
# ============================================================
def send_ac_status():
    """Publish AC status dengan retain=True"""
    payload = "ON" if ac_state else "OFF"
    client.publish(TOPIC_AC_STATUS, payload, retain=True)
    print(f"[MQTT] Published: {TOPIC_AC_STATUS} -> {payload} (retain)")

def send_dht_data():
    """Publish random DHT data"""
    # Random temperature (22-28°C)
    temperature = round(random.uniform(22, 28), 1)
    # Random humidity (50-70%)
    humidity = round(random.uniform(50, 70), 1)

    client.publish(TOPIC_DHT_TEMP, str(temperature))
    client.publish(TOPIC_DHT_HUM, str(humidity))

    print(f"[DHT] Temp: {temperature}°C, Hum: {humidity}%")

def send_mcu_status(status):
    """Publish MCU status (LWT)"""
    client.publish(TOPIC_MCU_STATUS, status, retain=True)
    print(f"[MQTT] Published: {TOPIC_MCU_STATUS} -> {status} (retain)")

# ============================================================
# MAIN
# ============================================================
def main():
    global client

    print("=" * 50)
    print("EcoLab MCU B Simulator (AC + DHT)")
    print("=" * 50)

    # Create MQTT client
    client = mqtt.Client(client_id="ecolab_mcub_simulator")

    # Set TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CA_CERT)
    client.tls_set_context(context)

    # Set callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Set LWT
    client.will_set(TOPIC_MCU_STATUS, "OFFLINE", qos=0, retain=True)

    # Connect
    print(f"\n[INFO] Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        # Main loop - send DHT data every 2 seconds
        last_dht_time = time.time()
        DHT_INTERVAL = 2

        print("\n[INFO] Simulator running. Press Ctrl+C to exit.")
        print(f"[INFO] Initial AC State: {'ON' if ac_state else 'OFF'}, Temp: {ac_temperature}°C, Mode: {ac_mode}\n")

        while True:
            try:
                # Send DHT data periodically
                current_time = time.time()
                if current_time - last_dht_time >= DHT_INTERVAL:
                    last_dht_time = current_time
                    send_dht_data()

                time.sleep(0.1)

            except KeyboardInterrupt:
                print("\n\n[INFO] Shutting down...")
                send_mcu_status("OFFLINE")
                client.loop_stop()
                client.disconnect()
                break

    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    main()
