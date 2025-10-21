import tkinter as tk
import threading
import time
import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import paho.mqtt.client as mqtt

# -------------------- KONFIGURASI --------------------
BROKER = "10.33.11.148"
PORT = 1883

# Topics
TOPIC_MCUA_STATUS = "mcuA/status"
TOPIC_MCUB_STATUS = "mcuB/status"

STATUS_COLOR = {"online": "#4CAF50", "offline": "#F44336", "unknown": "grey"}
BTN_COLOR = "#2E7D32"
BTN_HOVER = "#1B5E20"
BG_COLOR = "#E8F5E9"

# Tuya config
ACCESS_ID = "fgrgqphjjk94prgs7vsn"
ACCESS_KEY = "9dee5983d1a246628c4fa543b91ae34c"
API_ENDPOINT = "https://openapi-sg.iotbing.com"

# -------------------- DASHBOARD --------------------
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 ECOLAB DTEDI Dashboard 🌿")
        self.root.geometry("600x750")
        self.root.configure(bg=BG_COLOR)

        # ---------- HEADER ----------
        header = tk.Label(root, text="ECOLAB DTEDI DASHBOARD",
                          font=("Arial Black", 18), fg="#1B5E20", bg=BG_COLOR)
        header.pack(pady=15)

        # ---------- DEVICE STATUS (MQTT) ----------
        status_frame = tk.LabelFrame(root, text="Device Status", padx=10, pady=10,
                                     font=("Arial", 12, "bold"), fg="#1B5E20", bg=BG_COLOR)
        status_frame.pack(fill="x", padx=15, pady=10)

        self.label_mcuA = tk.Label(status_frame, text="MCU A (Lampu):", font=("Arial", 12), bg=BG_COLOR)
        self.label_mcuA.grid(row=0, column=0, sticky="w")
        self.indicator_mcuA = tk.Label(status_frame, text="UNKNOWN", bg=STATUS_COLOR["unknown"], fg="white", width=12)
        self.indicator_mcuA.grid(row=0, column=1, padx=10)

        self.label_mcuB = tk.Label(status_frame, text="MCU B (AC Remote):", font=("Arial", 12), bg=BG_COLOR)
        self.label_mcuB.grid(row=1, column=0, sticky="w")
        self.indicator_mcuB = tk.Label(status_frame, text="UNKNOWN", bg=STATUS_COLOR["unknown"], fg="white", width=12)
        self.indicator_mcuB.grid(row=1, column=1, padx=10)

        # ---------- LAMPU CONTROL (MCU A) ----------
        lamp_frame = tk.LabelFrame(root, text="Kontrol Lampu (MCU A)", padx=10, pady=10,
                                   font=("Arial", 12, "bold"), fg="#1B5E20", bg=BG_COLOR)
        lamp_frame.pack(fill="x", padx=15, pady=10)

        for i in range(1, 6):
            btn_on = self.create_button(lamp_frame, f"Lampu {i} ON", lambda idx=i: self.publish(f"mcuA/lamp{idx}", "ON"))
            btn_off = self.create_button(lamp_frame, f"Lampu {i} OFF", lambda idx=i: self.publish(f"mcuA/lamp{idx}", "OFF"))
            btn_on.grid(row=i-1, column=0, padx=5, pady=3, sticky="ew")
            btn_off.grid(row=i-1, column=1, padx=5, pady=3, sticky="ew")

        # ---------- AC CONTROL (MCU B) ----------
        ac_frame = tk.LabelFrame(root, text="Kontrol AC (MCU B)", padx=10, pady=10,
                                 font=("Arial", 12, "bold"), fg="#1B5E20", bg=BG_COLOR)
        ac_frame.pack(fill="x", padx=15, pady=10)

        self.create_button(ac_frame, "AC ON", lambda: self.publish("mcuB/ac", "ON")).grid(row=0, column=0, padx=5, pady=3, sticky="ew")
        self.create_button(ac_frame, "AC OFF", lambda: self.publish("mcuB/ac", "OFF")).grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        self.create_button(ac_frame, "MODE COOL", lambda: self.publish("mcuB/ac", "MODE_COOL")).grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        self.create_button(ac_frame, "MODE FAN", lambda: self.publish("mcuB/ac", "MODE_FAN")).grid(row=1, column=1, padx=5, pady=3, sticky="ew")
        self.create_button(ac_frame, "TEMP +", lambda: self.publish("mcuB/ac", "TEMP_UP")).grid(row=2, column=0, padx=5, pady=3, sticky="ew")
        self.create_button(ac_frame, "TEMP -", lambda: self.publish("mcuB/ac", "TEMP_DOWN")).grid(row=2, column=1, padx=5, pady=3, sticky="ew")

        # ---------- SENSOR SUHU & HUMIDITY (TUYA) ----------
        tuya_frame = tk.LabelFrame(root, text="Sensor Suhu & Humidity", padx=10, pady=10,
                                   font=("Arial", 12, "bold"), fg="#1B5E20", bg=BG_COLOR)
        tuya_frame.pack(fill="x", padx=15, pady=10)

        # Frame untuk kolom kiri, tengah (garis), kanan
        left_frame = tk.Frame(tuya_frame, bg=BG_COLOR)
        left_frame.pack(side="left", fill="both", expand=True)

        separator = tk.Frame(tuya_frame, width=2, bg="grey")
        separator.pack(side="left", fill="y", padx=5, pady=5)

        right_frame = tk.Frame(tuya_frame, bg=BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True)

        # Label suhu
        self.label_temperature = tk.Label(left_frame, text="Suhu: --.-°C", font=("Arial", 12), bg=BG_COLOR)
        self.label_temperature.pack(pady=5, padx=5)

        # Label kelembaban
        self.label_humidity = tk.Label(right_frame, text="Humidity: --.-%", font=("Arial", 12), bg=BG_COLOR)
        self.label_humidity.pack(pady=5, padx=5)

        # ---------- MQTT CLIENT ----------
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.mqtt_thread = threading.Thread(target=self.run_mqtt)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()

        # ---------- TUYA API ----------
        TUYA_LOGGER.setLevel(logging.INFO)
        self.tuya_api = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        self.tuya_api.connect()

        self.tuya_thread = threading.Thread(target=self.update_sensor)
        self.tuya_thread.daemon = True
        self.tuya_thread.start()

    # ---------- BUTTON FACTORY ----------
    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command,
                        bg=BTN_COLOR, fg="white", activebackground=BTN_HOVER, activeforeground="white",
                        font=("Arial", 11, "bold"), relief="flat", width=15, height=1)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))
        return btn

    # ---------- MQTT CALLBACK ----------
    def on_connect(self, client, userdata, flags, rc):
        print("Connected to broker:", rc)
        client.subscribe(TOPIC_MCUA_STATUS)
        client.subscribe(TOPIC_MCUB_STATUS)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Message from {msg.topic}: {payload}")
        if msg.topic == TOPIC_MCUA_STATUS:
            self.update_indicator(self.indicator_mcuA, payload)
        elif msg.topic == TOPIC_MCUB_STATUS:
            self.update_indicator(self.indicator_mcuB, payload)

    def update_indicator(self, indicator, status):
        color = STATUS_COLOR.get(status, "grey")
        indicator.config(text=status.upper(), bg=color)

    def publish(self, topic, message):
        print(f"Publish: {topic} -> {message}")
        self.client.publish(topic, message)

    def run_mqtt(self):
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_forever()

    # ---------- TUYA SENSOR UPDATE ----------
    def update_sensor(self):
        DEVICE_IDS = [
            "a366ecc0ab15070f5dtf9x",  # Sensor 1
            "a398a1c762af33236bvfar"   # Sensor 2
        ]

        while True:
            try:
                temps, hums = [], []

                for device_id in DEVICE_IDS:
                    response = self.tuya_api.get(f"/v1.0/iot-03/devices/{device_id}/status")
                    status = response['result']

                    # Suhu
                    temp_item = next((item for item in status if item['code'] == 'va_temperature'), None)
                    if temp_item:
                        temps.append(temp_item['value'] / 10)

                    # Humidity
                    hum_item = next((item for item in status if item['code'] == 'va_humidity'), None)
                    if hum_item:
                        hums.append(hum_item['value'] / 10)

                # Hitung rata-rata
                if temps:
                    avg_temp = sum(temps) / len(temps)
                    self.label_temperature.after(0, lambda t=avg_temp: self.label_temperature.config(text=f"Suhu: {t:.1f}°C"))

                if hums:
                    avg_hum = sum(hums) / len(hums)
                    self.label_humidity.after(0, lambda h=avg_hum: self.label_humidity.config(text=f"Humidity: {h:.1f}%"))

            except Exception as e:
                print("Error update sensor:", e)

            time.sleep(5)  # update tiap 5 detik


# -------------------- RUN DASHBOARD --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()
