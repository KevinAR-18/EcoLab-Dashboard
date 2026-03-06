import ssl
import paho.mqtt.client as mqtt

BROKER = "DESKTOP-CVPE153"
PORT = 8883

USERNAME = "dashboard"
PASSWORD = "ecolab123"

TOPIC = "ecolab/socket/1/control"


def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)


client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(
    ca_certs=r"C:\Program Files\Mosquitto\certs\ca.crt",
    tls_version=ssl.PROTOCOL_TLSv1_2
)

# client.tls_insecure_set(True)

client.on_connect = on_connect

client.connect(BROKER, PORT, 60)

client.loop_start()

while True:

    cmd = input("Command (ON/OFF): ")

    if cmd == "ON":
        client.publish(TOPIC, "ON")

    if cmd == "OFF":
        client.publish(TOPIC, "OFF")