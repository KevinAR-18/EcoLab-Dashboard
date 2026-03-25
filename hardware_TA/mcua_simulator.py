#!/usr/bin/env python3
"""
EcoLab MCU A Simulator (Python)
Menirukan Wemos D1 Mini untuk testing

- Subscribe: ecolab/mcuA/lamp1-5/control
import os
- Publish: ecolab/mcuA/lamp1-5/status
- Publish: ecolab/mcuA/dht/temperature, ecolab/mcuA/dht/humidity
- LWT: ecolab/mcuA/status
"""

import json
import random
import time
import ssl
import paho.mqtt.client as mqtt

# ============================================================
# CONFIG
# ============================================================
MQTT_BROKER = "DESKTOP-CVPE153"  # Ganti dengan IP broker
MQTT_PORT = 8883  # TLS
MQTT_USERNAME = "mcua"
MQTT_PASSWORD = "mcua123"
CA_CERT = r"C:\Program Files\Mosquitto\certs\ca.crt"  # Ganti path CA cert

# Topics
TOPIC_LAMP_CMD_PREFIX = "ecolab/mcuA/lamp"
TOPIC_LAMP_STATUS_PREFIX = "ecolab/mcuA/lamp"
TOPIC_DHT_TEMP = "ecolab/mcuA/dht/temperature"
TOPIC_DHT_HUM = "ecolab/mcuA/dht/humidity"
TOPIC_MCU_STATUS = "ecolab/mcuA/status"

NUM_RELAYS = 5

# ============================================================
# STATE
# ============================================================
relay_states = [False] * NUM_RELAYS
client = None

# ============================================================
# MQTT CALLBACKS
# ============================================================
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code: {rc}")

    # Subscribe to lamp command topics
    for i in range(1, NUM_RELAYS + 1):
        topic = f"{TOPIC_LAMP_CMD_PREFIX}{i}/control"
        client.subscribe(topic)
        print(f"[MQTT] Subscribed: {topic}")

    # Send initial status
    send_mcu_status("ONLINE")
    send_all_relay_status()

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\n[MQTT] Received: {topic} -> {payload}")

    # Parse lamp index from topic
    # Topic format: ecolab/mcuA/lamp1/control
    if TOPIC_LAMP_CMD_PREFIX in topic:
        try:
            # Extract lamp number
            lamp_part = topic.split("/")[-2]  # "lamp1", "lamp2", etc.
            lamp_index = int(lamp_part.replace("lamp", ""))

            if 1 <= lamp_index <= NUM_RELAYS:
                if payload == "ON":
                    control_relay(lamp_index, True)
                elif payload == "OFF":
                    control_relay(lamp_index, False)
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Failed to parse topic: {e}")

# ============================================================
# CONTROL FUNCTIONS
# ============================================================
def control_relay(relay_index, state):
    """Control relay and publish status"""
    relay_states[relay_index - 1] = state
    print(f"[RELAY] Lamp {relay_index}: {'ON' if state else 'OFF'}")
    send_relay_status(relay_index)

def send_relay_status(relay_index):
    """Publish relay status dengan retain=True"""
    state = relay_states[relay_index - 1]
    topic = f"{TOPIC_LAMP_STATUS_PREFIX}{relay_index}/status"
    payload = "ON" if state else "OFF"

    client.publish(topic, payload, retain=True)  # Retain agar status tersimpan
    print(f"[MQTT] Published: {topic} -> {payload} (retain)")

def send_all_relay_status():
    """Publish all relay status"""
    for i in range(1, NUM_RELAYS + 1):
        send_relay_status(i)
        time.sleep(0.1)

def send_dht_data():
    """Publish random DHT data"""
    temperature = round(random.uniform(20, 30), 1)
    humidity = round(random.uniform(40, 80), 1)

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
    print("EcoLab MCU A Simulator")
    print("=" * 50)

    # Create MQTT client
    client = mqtt.Client(client_id="ecolab_mcua_simulator")

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

        print("\n[INFO] Simulator running. Press Ctrl+C to exit.\n")

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
