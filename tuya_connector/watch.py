import tkinter as tk
import threading
import time
import logging
import paho.mqtt.client as mqtt
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from time import strftime

# -------------------- KONFIGURASI --------------------
# Pastikan Anda menginstal semua library yang diperlukan:
# pip install paho-mqtt
# pip install tuya-connector-python
# pip install tk

BROKER = "10.33.11.148"
PORT = 1883

# Topics
TOPIC_MCUA_STATUS = "mcuA/status"
TOPIC_MCUB_STATUS = "mcuB/status"

STATUS_COLOR = {"online": "#4CAF50", "offline": "#F44336", "unknown": "grey"}
BTN_COLOR = "#2E7D32"
BTN_HOVER = "#1B5E20"
BG_COLOR = "#E8F5E9"
HEADER_COLOR = "#1B5E20"

# Tuya config
ACCESS_ID = "fgrgqphjjk94prgs7vsn"
ACCESS_KEY = "9dee5983d1a246628c4fa543b91ae34c"
API_ENDPOINT = "https://openapi-sg.iotbing.com"
DEVICE_IDS = [
    "a366ecc0ab15070f5dtf9x",  # Sensor 1
    "a398a1c762af33236bvfar"   # Sensor 2
]

# -------------------- DASHBOARD CLASS --------------------
class Dashboard:
    """
    Kelas utama untuk membangun dashboard ECOLAB DTEDI.
    Mengintegrasikan MQTT, Tuya, dan jam digital dalam satu antarmuka.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 ECOLAB DTEDI Dashboard 🌿")
        self.root.geometry("600x850")
        self.root.configure(bg=BG_COLOR)

        # State untuk setiap lampu
        self.lamp_states = {i: False for i in range(1, 6)}
        self.lamp_canvases = {}

        # ---------- HEADER & CLOCK ----------
        header_frame = tk.Frame(root, bg=BG_COLOR)
        header_frame.pack(pady=15, fill="x")

        header = tk.Label(header_frame, text="ECOLAB DTEDI DASHBOARD",
                          font=("Arial Black", 18), fg=HEADER_COLOR, bg=BG_COLOR)
        header.pack(pady=(0, 5))

        self.label_clock = tk.Label(header_frame, font=('calibri', 20, 'bold'),
                                    background=BG_COLOR,
                                    foreground=HEADER_COLOR)
        self.label_clock.pack(pady=(0, 10))

        # ---------- DEVICE STATUS (MQTT) ----------
        self.status_frame = self.create_labelframe(root, "Status Perangkat")
        self.status_frame.pack(fill="x", padx=15, pady=10)

        self.label_mcuA = tk.Label(self.status_frame, text="MCU A (Lampu):", font=("Arial", 12), bg=BG_COLOR)
        self.label_mcuA.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.indicator_mcuA = tk.Label(self.status_frame, text="UNKNOWN", bg=STATUS_COLOR["unknown"], fg="white", width=12)
        self.indicator_mcuA.grid(row=0, column=1, padx=10, pady=5)

        self.label_mcuB = tk.Label(self.status_frame, text="MCU B (AC Remote):", font=("Arial", 12), bg=BG_COLOR)
        self.label_mcuB.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.indicator_mcuB = tk.Label(self.status_frame, text="UNKNOWN", bg=STATUS_COLOR["unknown"], fg="white", width=12)
        self.indicator_mcuB.grid(row=1, column=1, padx=10, pady=5)
        
        # ---------- KONTROL LAMPU (MCU A) ----------
        self.lamp_frame = self.create_labelframe(root, "Kontrol Lampu")
        self.lamp_frame.pack(fill="x", padx=15, pady=10)
        
        # Tombol bohlam menggunakan Canvas
        for i in range(1, 6):
            canvas = self.create_lamp_canvas(self.lamp_frame, i)
            self.lamp_canvases[i] = canvas
            canvas.pack(side="left", padx=10, pady=5, expand=True)
            # Bind event click ke canvas
            canvas.bind("<Button-1>", lambda event, idx=i: self.toggle_lamp_state(idx))

        # ---------- KONTROL AC (MCU B) ----------
        self.ac_frame = self.create_labelframe(root, "Kontrol AC (MCU B)")
        self.ac_frame.pack(fill="x", padx=15, pady=10)

        self.create_button(self.ac_frame, "AC ON", lambda: self.publish("mcuB/ac", "ON")).grid(row=0, column=0, padx=5, pady=3, sticky="ew")
        self.create_button(self.ac_frame, "AC OFF", lambda: self.publish("mcuB/ac", "OFF")).grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        self.create_button(self.ac_frame, "MODE COOL", lambda: self.publish("mcuB/ac", "MODE_COOL")).grid(row=1, column=0, padx=5, pady=3, sticky="ew")
        self.create_button(self.ac_frame, "MODE FAN", lambda: self.publish("mcuB/ac", "MODE_FAN")).grid(row=1, column=1, padx=5, pady=3, sticky="ew")
        self.create_button(self.ac_frame, "TEMP +", lambda: self.publish("mcuB/ac", "TEMP_UP")).grid(row=2, column=0, padx=5, pady=3, sticky="ew")
        self.create_button(self.ac_frame, "TEMP -", lambda: self.publish("mcuB/ac", "TEMP_DOWN")).grid(row=2, column=1, padx=5, pady=3, sticky="ew")

        # ---------- SENSOR SUHU & HUMIDITY (TUYA) ----------
        self.tuya_frame = self.create_labelframe(root, "Sensor Suhu & Kelembaban")
        self.tuya_frame.pack(fill="x", padx=15, pady=10)

        left_frame = tk.Frame(self.tuya_frame, bg=BG_COLOR)
        left_frame.pack(side="left", fill="both", expand=True)

        separator = tk.Frame(self.tuya_frame, width=2, bg="grey")
        separator.pack(side="left", fill="y", padx=5, pady=5)

        right_frame = tk.Frame(self.tuya_frame, bg=BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True)

        self.label_temperature = tk.Label(left_frame, text="Suhu: --.-°C", font=("Arial", 12), bg=BG_COLOR)
        self.label_temperature.pack(pady=5, padx=5)

        self.label_humidity = tk.Label(right_frame, text="Kelembaban: --.-%", font=("Arial", 12), bg=BG_COLOR)
        self.label_humidity.pack(pady=5, padx=5)

        # ---------- START THREADS AND SERVICES ----------
        self.start_mqtt()
        self.start_tuya()
        self.update_clock()

    # ---------- HELPER METHODS ----------
    def create_labelframe(self, parent, text):
        """Menciptakan LabelFrame dengan gaya yang konsisten."""
        return tk.LabelFrame(parent, text=text, padx=10, pady=10,
                             font=("Arial", 12, "bold"), fg=HEADER_COLOR, bg=BG_COLOR)

    def create_button(self, parent, text, command):
        """Menciptakan Button standar dengan gaya yang konsisten."""
        btn = tk.Button(parent, text=text, command=command,
                        bg=BTN_COLOR, fg="white", activebackground=BTN_HOVER, activeforeground="white",
                        font=("Arial", 11, "bold"), relief="flat", width=15, height=1)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))
        return btn

    def create_lamp_canvas(self, parent, lamp_index):
        """Menciptakan canvas berbentuk bohlam."""
        canvas = tk.Canvas(parent, width=50, height=70, bg=BG_COLOR, highlightthickness=0)
        
        # Menggambar bohlam (oval)
        canvas.create_oval(10, 5, 40, 45, fill="#A9A9A9", outline="#A9A9A9", tags="bulb")
        # Menggambar fitting (persegi panjang)
        canvas.create_rectangle(15, 45, 35, 50, fill="#A9A9A9", outline="#A9A9A9", tags="base")
        canvas.create_rectangle(18, 50, 32, 55, fill="#A9A9A9", outline="#A9A9A9", tags="base")
        canvas.create_rectangle(20, 55, 30, 60, fill="#A9A9A9", outline="#A9A9A9", tags="base")
        
        return canvas
    
    def update_lamp_canvas(self, canvas, is_on):
        """Memperbarui warna bohlam di canvas berdasarkan statusnya."""
        if is_on:
            color = "#FFD700"  # Emas untuk ON
        else:
            color = "#A9A9A9"  # Abu-abu gelap untuk OFF
        
        canvas.itemconfig("bulb", fill=color, outline=color)
        canvas.itemconfig("base", fill=color, outline=color)

    def toggle_lamp_state(self, lamp_index):
        """Logika untuk mengubah status lampu dan mengirim pesan MQTT."""
        current_state = self.lamp_states[lamp_index]
        new_state = not current_state
        self.lamp_states[lamp_index] = new_state
        
        canvas = self.lamp_canvases[lamp_index]
        self.update_lamp_canvas(canvas, new_state)

        message = "ON" if new_state else "OFF"
        self.publish(f"mcuA/lamp{lamp_index}", message)

    def update_clock(self):
        """Memperbarui jam dan tanggal setiap detik."""
        string = strftime('%A, %d %B %Y | %H:%M:%S')
        self.label_clock.config(text=string)
        self.root.after(1000, self.update_clock)

    # ---------- MQTT LOGIC ----------
    def on_connect(self, client, userdata, flags, rc):
        """Callback ketika terhubung ke broker MQTT."""
        print("Connected to broker:", rc)
        client.subscribe(TOPIC_MCUA_STATUS)
        client.subscribe(TOPIC_MCUB_STATUS)

    def on_message(self, client, userdata, msg):
        """Callback ketika menerima pesan MQTT."""
        payload = msg.payload.decode()
        print(f"Message from {msg.topic}: {payload}")
        if msg.topic == TOPIC_MCUA_STATUS:
            self.update_indicator(self.indicator_mcuA, payload)
        elif msg.topic == TOPIC_MCUB_STATUS:
            self.update_indicator(self.indicator_mcuB, payload)

    def update_indicator(self, indicator, status):
        """Memperbarui label status perangkat."""
        color = STATUS_COLOR.get(status.lower(), "grey")
        indicator.config(text=status.upper(), bg=color)

    def publish(self, topic, message):
        """Menerbitkan pesan MQTT."""
        print(f"Publish: {topic} -> {message}")
        self.client.publish(topic, message)

    def run_mqtt(self):
        """Menjalankan klien MQTT dalam sebuah thread."""
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_forever()

    def start_mqtt(self):
        """Menginisialisasi dan memulai thread MQTT."""
        self.mqtt_thread = threading.Thread(target=self.run_mqtt)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()

    # ---------- TUYA LOGIC ----------
    def update_sensor(self):
        """Memperbarui data sensor Tuya dalam sebuah thread."""
        TUYA_LOGGER.setLevel(logging.INFO)
        self.tuya_api = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        self.tuya_api.connect()

        while True:
            try:
                temps, hums = [], []
                for device_id in DEVICE_IDS:
                    response = self.tuya_api.get(f"/v1.0/iot-03/devices/{device_id}/status")
                    if 'result' in response:
                        status = response['result']
                        temp_item = next((item for item in status if item['code'] == 'va_temperature'), None)
                        if temp_item:
                            temps.append(temp_item['value'] / 10)
                        
                        hum_item = next((item for item in status if item['code'] == 'va_humidity'), None)
                        if hum_item:
                            hums.append(hum_item['value'] / 10)

                if temps:
                    avg_temp = sum(temps) / len(temps)
                    self.label_temperature.after(0, lambda t=avg_temp: self.label_temperature.config(text=f"Suhu: {t:.1f}°C"))
                if hums:
                    avg_hum = sum(hums) / len(hums)
                    self.label_humidity.after(0, lambda h=avg_hum: self.label_humidity.config(text=f"Kelembaban: {h:.1f}%"))
            
            except Exception as e:
                print("Error update sensor:", e)
            
            time.sleep(5)  # update setiap 5 detik

    def start_tuya(self):
        """Menginisialisasi dan memulai thread Tuya."""
        self.tuya_thread = threading.Thread(target=self.update_sensor)
        self.tuya_thread.daemon = True
        self.tuya_thread.start()

# -------------------- RUN APPLICATION --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()