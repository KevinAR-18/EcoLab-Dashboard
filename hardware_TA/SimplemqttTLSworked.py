import ssl
import json
import paho.mqtt.client as mqtt

# ================= MQTT CONFIG =================

BROKER = "10.139.6.151"
PORT = 8883

USERNAME = "dashboard"
PASSWORD = "ecolab123"

TOPIC_CONTROL = "ecolab/socket/1/control"
TOPIC_STATUS = "ecolab/socket/1/status"
TOPIC_ENERGY = "ecolab/socket/1/energy"

CA_CERT = "ca.crt"   # path file ca.crt

# ================= MQTT CALLBACK =================

def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)

    client.subscribe(TOPIC_STATUS)
    client.subscribe(TOPIC_ENERGY)


def on_message(client, userdata, msg):

    topic = msg.topic
    payload = msg.payload.decode()

    if topic == TOPIC_STATUS:
        print("Socket Status:", payload)

    elif topic == TOPIC_ENERGY:

        try:
            data = json.loads(payload)

            print("\n===== ENERGY DATA =====")
            print("Voltage   :", data["voltage"], "V")
            print("Current   :", data["current"], "A")
            print("Power     :", data["power"], "W")
            print("Energy    :", data["energy"], "kWh")
            print("Frequency :", data["frequency"], "Hz")
            print("PF        :", data["pf"])
            print("=======================\n")

        except:
            print("Invalid energy data:", payload)


# ================= MQTT CLIENT =================

client = mqtt.Client()

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set(
    ca_certs=r"C:\Program Files\Mosquitto\certs\ca.crt",
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting MQTT...")
client.connect(BROKER, PORT, 60)

client.loop_start()


# ================= CONTROL LOOP =================

while True:

    cmd = input("Command (on/off): ")

    if cmd.lower() == "on":

        client.publish(TOPIC_CONTROL, "ON")
        print("Sent: ON")

    elif cmd.lower() == "off":

        client.publish(TOPIC_CONTROL, "OFF")
        print("Sent: OFF")