import paho.mqtt.client as mqtt
import ssl

# ================= CONFIG =================

BROKER = "DESKTOP-CVPE153"   # hostname sesuai certificate
PORT = 8883
TOPIC = "test/topic"

CA_CERT = r"C:\Program Files\mosquitto\certs\ca.crt"

# ================= CALLBACK =================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT TLS broker")
        client.subscribe(TOPIC)
    else:
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"[MQTT] {msg.topic} -> {msg.payload.decode()}")

# ================= CLIENT =================

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# TLS configuration
client.tls_set(
    ca_certs=CA_CERT,
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

print("Connecting to broker...")

client.connect(BROKER, PORT, 60)

client.loop_forever()