import paho.mqtt.client as mqtt

BROKER = "10.33.11.148"   # ganti kalau broker beda
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("[SNIFFER] Connected with result code", rc)
    client.subscribe("#")  # SUBSCRIBE SEMUA TOPIC

def on_message(client, userdata, msg):
    print(f"[SNIFFER] {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("[SNIFFER] Connecting to broker...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
