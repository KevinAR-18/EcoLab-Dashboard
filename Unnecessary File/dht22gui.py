# file: dashboard_with_box_weather.py
import tkinter as tk
from tkinter import ttk
import threading
import time
import paho.mqtt.client as mqtt
from time import strftime
from PIL import Image, ImageTk
import math
import requests
import os

# --- Tambahkan/modifikasi fungsi fetch_weather_data jika weather_module.py tidak ada ---
URL_DATA = "https://app.weathercloud.net/device/values/5476957392"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://app.weathercloud.net/device/5476957392",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

def fetch_weather_data():
    """Ambil data cuaca dari API eksternal."""
    try:
        r = requests.get(URL_DATA, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Weather API Error: {r.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network Error fetching weather: {e}")
        return None
# ----------------------------------------------------------------------------------------

# -------------------- KONFIGURASI --------------------
BROKER = "10.33.11.148"
PORT = 1883

# Topics status perangkat
TOPIC_MCUA_STATUS = "mcuA/status"
TOPIC_MCUB_STATUS = "mcuB/status"

# --- Topik DHT22 dari MCU A & MCU B ---
TOPIC_DHT22_TEMP_A = "mcuA/dht/temperature"
TOPIC_DHT22_HUM_A  = "mcuA/dht/humidity"

TOPIC_DHT22_TEMP_B = "mcuB/dht/temperature"
TOPIC_DHT22_HUM_B  = "mcuB/dht/humidity"

# Warna modern
COLORS = {
    "primary": "#1a535c",
    "secondary": "#4ecdc4",
    "accent": "#ff6b6b",
    "light": "#f7fff7",
    "dark": "#1a1a2e",
    "success": "#4CAF50",
    "warning": "#FFC107",
    "danger": "#F44336",
    "card_bg": "#ffffff",
    "text_light": "#ffffff",
    "text_dark": "#333333"
}

# -------------------- MODERN WIDGETS --------------------
class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, width=120, height=40, bg=COLORS["primary"], fg=COLORS["text_light"]):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        self.command = command
        self.bg = bg
        self.fg = fg
        self.width = width
        self.height = height
        
        # Draw rounded rectangle
        self.rect = self.create_rounded_rect(5, 5, width-5, height-5, radius=15, fill=bg)
        self.text = self.create_text(width/2, height/2, text=text, fill=fg, font=("Arial", 10, "bold"))
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def on_click(self, event):
        self.command()
    
    def on_enter(self, event):
        self.itemconfig(self.rect, fill=COLORS["secondary"])
    
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg)

class ModernCard(tk.Frame):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, bg=COLORS["light"], **kwargs)
        self.config(highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Title
        title_frame = tk.Frame(self, bg=COLORS["primary"], height=30)
        title_frame.pack(fill="x", padx=1, pady=(1, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=title, bg=COLORS["primary"], 
                               fg=COLORS["text_light"], font=("Arial", 10, "bold"))
        title_label.pack(side="left", padx=10, pady=5)
        
        self.content_frame = tk.Frame(self, bg=COLORS["card_bg"])
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

class StatusIndicator(tk.Canvas):
    def __init__(self, parent, text="UNKNOWN", width=100, height=30):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        self.text = text
        self.status = "unknown"
        self.draw_indicator()
    
    def draw_indicator(self):
        self.delete("all")
        color = COLORS["warning"] if self.status == "unknown" else \
                 COLORS["success"] if self.status == "online" else COLORS["danger"]
        
        # Draw rounded background
        self.create_rounded_rect(2, 2, 98, 28, radius=10, fill=color, outline="")
        
        # Draw text
        self.create_text(50, 15, text=self.text.upper(), fill=COLORS["text_light"], 
                         font=("Arial", 9, "bold"))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def update_status(self, status):
        self.status = status.lower()
        self.text = status.upper()
        self.draw_indicator()

class AnimatedLamp(tk.Canvas):
    def __init__(self, parent, lamp_index, command, width=60, height=80):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=COLORS["card_bg"])
        self.lamp_index = lamp_index
        self.command = command
        self.is_on = False
        self.width = width
        self.height = height
        self.animation_id = None
        
        self.draw_lamp()
        self.bind("<Button-1>", self.toggle)
    
    def draw_lamp(self):
        self.delete("all")
        
        # Colors
        bulb_color = "#FFD700" if self.is_on else "#A9A9A9"
        base_color = "#d4af37" if self.is_on else "#b0b0b0"
        glow_color = "#FFF8DC" if self.is_on else "transparent"
        
        # Draw glow effect when on
        if self.is_on:
            self.create_oval(15, 10, 45, 40, fill=glow_color, outline="", tags="glow")
        
        # Draw bulb
        self.create_oval(15, 10, 45, 40, fill=bulb_color, outline=bulb_color, tags="bulb")
        
        # Draw base
        self.create_rectangle(20, 40, 40, 45, fill=base_color, outline=base_color, tags="base")
        self.create_rectangle(23, 45, 37, 50, fill=base_color, outline=base_color, tags="base")
        self.create_rectangle(25, 50, 35, 55, fill=base_color, outline=base_color, tags="base")
        
        # Draw label
        self.create_text(30, 65, text=f"Lampu {self.lamp_index}", 
                         font=("Arial", 8, "bold"), fill=COLORS["text_dark"])
    
    def toggle(self, event=None):
        self.is_on = not self.is_on
        self.animate_toggle()
        self.command(self.lamp_index)
    
    def animate_toggle(self):
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        target_scale = 1.2 if self.is_on else 1.0
        self.animate_scale(1.0, target_scale)
    
    def animate_scale(self, current_scale, target_scale):
        if abs(current_scale - target_scale) > 0.05:
            new_scale = current_scale + (target_scale - current_scale) * 0.3
            self.scale("all", 30, 25, new_scale, new_scale)
            self.animation_id = self.after(50, lambda: self.animate_scale(new_scale, target_scale))
        else:
            self.scale("all", 30, 25, target_scale, target_scale)
            self.draw_lamp()

class SensorDisplay(tk.Canvas):
    # SensorDisplay asli, sekarang dipakai untuk DHT22 via MQTT (rata-rata A+B)
    def __init__(self, parent, title, unit, width=150, height=100):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=COLORS["card_bg"])
        self.title = title
        self.unit = unit
        self.value = "--.-"
        self.width = width
        self.height = height
        self.animation_id = None
        
        self.draw_display()
    
    def draw_display(self):
        self.delete("all")
        
        # Draw background circle (original shape)
        self.create_oval(10, 10, 140, 90, fill="#f0f8ff", outline=COLORS["secondary"], width=2)
        
        # Draw value
        self.create_text(75, 45, text=f"{self.value}{self.unit}", 
                         font=("Arial", 16, "bold"), fill=COLORS["primary"])
        
        # Draw title
        self.create_text(75, 75, text=self.title, 
                         font=("Arial", 10), fill=COLORS["text_dark"])
    
    def update_value(self, new_value):
        # new_value expected string or numeric convertible to float
        try:
            if isinstance(new_value, str):
                if new_value == "--.-":
                    new_value_float = None
                else:
                    new_value_float = float(new_value)
            else:
                new_value_float = float(new_value)
        except Exception:
            # fallback: set raw string
            self.value = str(new_value)
            self.draw_display()
            return

        # animate only if previous is numeric
        if self.value != "--.-":
            try:
                old_value = float(self.value)
            except Exception:
                old_value = new_value_float
        else:
            old_value = new_value_float

        if new_value_float is None:
            self.value = "--.-"
            self.draw_display()
            return

        # Smooth animation from old_value to new_value_float
        if old_value is None:
            self.value = f"{new_value_float:.1f}"
            self.draw_display()
            return

        if old_value != new_value_float:
            self.animate_value_change(old_value, new_value_float)
        else:
            self.value = f"{new_value_float:.1f}"
            self.draw_display()
    
    def animate_value_change(self, start, end):
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        current = start
        step = (end - start) / 10 if end != start else 0
        
        def update():
            nonlocal current
            current += step
            if (step > 0 and current >= end) or (step < 0 and current <= end) or step == 0:
                self.value = f"{end:.1f}"
                self.draw_display()
            else:
                self.value = f"{current:.1f}"
                self.draw_display()
                self.animation_id = self.after(50, update)
        
        update()

# --- KELAS BARU UNTUK DISPLAY WEATHER STATION (KOTAK SEPERTI REMOTE AC) ---
class BoxSensorDisplay(tk.Canvas):
    def __init__(self, parent, title, unit, width=120, height=90, bg_color="#f0f8ff", primary_color=COLORS["primary"]):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=COLORS["card_bg"])
        self.title = title
        self.unit = unit
        self.value = "--.-"
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.primary_color = primary_color
        self.animation_id = None
        
        self.draw_display()

    def draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Menggambar rounded rectangle sederhana."""
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def draw_display(self):
        self.delete("all")
        
        # Draw background box (Kotak mirip remote AC)
        box_padding = 5
        self.draw_rounded_rect(
            box_padding, box_padding, 
            self.width - box_padding, self.height - box_padding, 
            radius=15, fill=self.bg_color, outline=COLORS["primary"], width=2
        )
        
        # Draw Title (Di bagian atas kotak)
        self.create_text(
            self.width / 2, 
            box_padding + 10, 
            text=self.title, 
            font=("Arial", 9, "bold"), 
            fill=COLORS["dark"]
        )
        
        # Draw Value + Unit (Di tengah kotak)
        self.create_text(
            self.width / 2, 
            self.height / 2 + 5, 
            text=f"{self.value}{self.unit}", 
            font=("Arial", 14, "bold"), 
            fill=self.primary_color
        )
    
    def update_value(self, new_value):
        try:
            if isinstance(new_value, str):
                if new_value == "--.-":
                    new_value_float = None
                else:
                    new_value_float = float(new_value)
            else:
                new_value_float = float(new_value)
        except Exception:
            self.value = str(new_value)
            self.draw_display()
            return

        if self.value != "--.-":
            try:
                old_value = float(self.value)
            except Exception:
                old_value = new_value_float
        else:
            old_value = new_value_float

        if new_value_float is None:
            self.value = "--.-"
            self.draw_display()
            return

        if old_value is None:
            self.value = f"{new_value_float:.1f}"
            self.draw_display()
            return

        if old_value != new_value_float:
            self.animate_value_change(old_value, new_value_float)
        else:
            self.value = f"{new_value_float:.1f}"
            self.draw_display()
    
    def animate_value_change(self, start, end):
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        current = start
        step = (end - start) / 10 if end != start else 0
        
        def update():
            nonlocal current
            current += step
            if (step > 0 and current >= end) or (step < 0 and current <= end) or step == 0:
                self.value = f"{end:.1f}"
                self.draw_display()
            else:
                self.value = f"{current:.1f}"
                self.draw_display()
                self.animation_id = self.after(50, update)
        
        update()
# -----------------------------------------------------------------------------

# -------------------- DASHBOARD CLASS --------------------
class ModernDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 ECOLAB DTEDI Dashboard 🌿")
        self.root.geometry("800x1200")
        self.root.configure(bg=COLORS["light"])
        
        # State untuk setiap lampu
        self.lamp_states = {i: False for i in range(1, 6)}
        self.lamp_widgets = {}

        # Variabel untuk menyimpan nilai DHT22 dari MCU A & MCU B
        self.temp_A = None
        self.hum_A  = None
        self.temp_B = None
        self.hum_B  = None
        
        self.setup_ui()
        self.start_services()
    
    def setup_ui(self):
        self.setup_header()

        main_frame = tk.Frame(self.root, bg=COLORS["light"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Atur bobot grid agar seimbang
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # --- Susun layout 2 kolom ---
        # Card Status (baris 0, rentang 2 kolom)
        self.setup_status_card(main_frame)
        
        # Card Lampu dan AC (baris 1, 2 kolom)
        self.setup_lamp_card(main_frame) 
        self.setup_ac_card(main_frame)
        
        # Card Sensor DHT22 (baris 2, 2 kolom)
        self.setup_sensor_card(main_frame)
        
        # Card Weather Station (baris 3, 2 kolom)
        self.setup_weather_card(main_frame)
        
        # Card Log (baris 4, 2 kolom)
        self.setup_log_card(main_frame)

    
    def setup_header(self):
        header_frame = tk.Frame(self.root, bg=COLORS["primary"], height=120)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, text="ECOLAB DTEDI DASHBOARD", 
                               font=("Arial Black", 20), fg=COLORS["text_light"], 
                               bg=COLORS["primary"])
        title_label.pack(pady=(20, 5))
        
        # Clock
        self.clock_label = tk.Label(header_frame, font=('Arial', 14),
                                     bg=COLORS["primary"], fg=COLORS["text_light"])
        self.clock_label.pack(pady=(0, 10))
        
        # Connection status
        self.connection_label = tk.Label(header_frame, text="● Menghubungkan...", 
                                         font=("Arial", 10), fg=COLORS["warning"], 
                                         bg=COLORS["primary"])
        self.connection_label.pack()
    
    def setup_status_card(self, parent):
        card = ModernCard(parent, "Status Perangkat")
        card.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # MCU A Status
        tk.Label(card.content_frame, text="MCU A (Lampu):", font=("Arial", 10), 
                 bg=COLORS["card_bg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.indicator_mcuA = StatusIndicator(card.content_frame)
        self.indicator_mcuA.grid(row=0, column=1, padx=10, pady=5)
        
        # MCU B Status
        tk.Label(card.content_frame, text="MCU B (AC Remote):", font=("Arial", 10), 
                 bg=COLORS["card_bg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.indicator_mcuB = StatusIndicator(card.content_frame)
        self.indicator_mcuB.grid(row=1, column=1, padx=10, pady=5)
    
    def setup_lamp_card(self, parent):
        card = ModernCard(parent, "Kontrol Lampu")
        card.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        lamp_frame = tk.Frame(card.content_frame, bg=COLORS["card_bg"])
        lamp_frame.pack(fill="both", expand=True)
        
        for i in range(1, 6):
            lamp = AnimatedLamp(lamp_frame, i, self.toggle_lamp_state)
            lamp.pack(side="left", padx=10, pady=10)
            self.lamp_widgets[i] = lamp
    
    def setup_ac_card(self, parent):
        card = ModernCard(parent, "Kontrol AC (MCU B)")
        card.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # AC controls grid
        controls = [
            ("AC ON", lambda: self.publish("mcuB/ac", "ON")),
            ("AC OFF", lambda: self.publish("mcuB/ac", "OFF")),
            ("MODE COOL", lambda: self.publish("mcuB/ac", "MODE_COOL")),
            ("MODE FAN", lambda: self.publish("mcuB/ac", "MODE_FAN")),
            ("TEMP +", lambda: self.publish("mcuB/ac", "TEMP_UP")),
            ("TEMP -", lambda: self.publish("mcuB/ac", "TEMP_DOWN"))
        ]
        
        for i, (text, command) in enumerate(controls):
            btn = ModernButton(card.content_frame, text, command, width=110, height=35)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
    
    def setup_sensor_card(self, parent):
        card = ModernCard(parent, "Sensor Suhu & Kelembaban (DHT22)")
        card.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        sensor_frame = tk.Frame(card.content_frame, bg=COLORS["card_bg"])
        sensor_frame.pack(fill="both", expand=True, pady=10)
        
        # Menggunakan SensorDisplay untuk RATA-RATA DHT22 (MCU A & MCU B)
        self.temp_display = SensorDisplay(sensor_frame, "TEMP (Avg)", "°C")
        self.temp_display.pack(side="left", padx=20, pady=10)
        
        self.humidity_display = SensorDisplay(sensor_frame, "HUM (Avg)", "%")
        self.humidity_display.pack(side="right", padx=20, pady=10)

    def setup_weather_card(self, parent):
        """Menyiapkan kartu Weather Station dengan display kotak."""
        card = ModernCard(parent, "Weather Station")
        card.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        frame = tk.Frame(card.content_frame, bg=COLORS["card_bg"])
        frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)

        # Suhu Luar
        self.weather_temp = BoxSensorDisplay(frame, "Suhu Luar", "°C")
        self.weather_temp.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Kelembaban Luar
        self.weather_hum = BoxSensorDisplay(frame, "Kelembaban", "%")
        self.weather_hum.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Angin
        self.weather_wind = BoxSensorDisplay(frame, "Angin", " km/h")
        self.weather_wind.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Curah Hujan
        self.weather_rain = BoxSensorDisplay(frame, "Curah Hujan", " mm")
        self.weather_rain.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    def setup_log_card(self, parent):
        card = ModernCard(parent, "Log Aktivitas")
        card.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        log_frame = tk.Frame(card.content_frame, bg=COLORS["card_bg"])
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, height=6, font=("Courier New", 9),
                                 bg="#f8f9fa", fg=COLORS["text_dark"])
        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.log("Dashboard dimulai...")
    # --------------------------------

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
    
    def toggle_lamp_state(self, lamp_index):
        self.lamp_states[lamp_index] = not self.lamp_states[lamp_index]
        message = "ON" if self.lamp_states[lamp_index] else "OFF"
        self.publish(f"mcuA/lamp{lamp_index}", message)
        self.log(f"Lampu {lamp_index} diubah ke: {message}")
    
    def update_clock(self):
        string = time.strftime('%A, %d %B %Y | %H:%M:%S')
        self.clock_label.config(text=string)
        self.root.after(1000, self.update_clock)
    
    def update_connection_status(self, status):
        color = COLORS["success"] if status == "connected" else COLORS["danger"]
        self.connection_label.config(text=f"● {status.capitalize()}", fg=color)

    # ---------- LOGIKA RATA-RATA DHT22 ----------
    def update_avg_dht(self):
        """Hitung rata-rata suhu & kelembaban dari MCU A & MCU B, lalu update display."""
        temps = [t for t in (self.temp_A, self.temp_B) if t is not None]
        hums  = [h for h in (self.hum_A, self.hum_B) if h is not None]

        # Suhu rata-rata
        if temps:
            avg_temp = sum(temps) / len(temps)
            self.temp_display.update_value(avg_temp)
        else:
            self.temp_display.update_value("--.-")

        # Kelembaban rata-rata
        if hums:
            avg_hum = sum(hums) / len(hums)
            self.humidity_display.update_value(avg_hum)
        else:
            self.humidity_display.update_value("--.-")
    
    # ---------- MQTT LOGIC ----------
    def on_connect(self, client, userdata, flags, rc):
        self.log("Terhubung ke broker MQTT")
        self.update_connection_status("connected")
        client.subscribe(TOPIC_MCUA_STATUS)
        client.subscribe(TOPIC_MCUB_STATUS)

        # Subscribe DHT22 MCU A & MCU B
        client.subscribe(TOPIC_DHT22_TEMP_A)
        client.subscribe(TOPIC_DHT22_HUM_A)
        client.subscribe(TOPIC_DHT22_TEMP_B)
        client.subscribe(TOPIC_DHT22_HUM_B)
    
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        self.log(f"Pesan dari {msg.topic}: {payload}")
        
        if msg.topic == TOPIC_MCUA_STATUS:
            self.indicator_mcuA.update_status(payload)

        elif msg.topic == TOPIC_MCUB_STATUS:
            self.indicator_mcuB.update_status(payload)

        # --- DHT22 MCU A ---
        elif msg.topic == TOPIC_DHT22_TEMP_A:
            try:
                self.temp_A = float(payload)
                # Update rata-rata di main thread
                self.root.after(0, self.update_avg_dht)
            except ValueError:
                self.log(f"Payload suhu MCU A tidak valid: {payload}")

        elif msg.topic == TOPIC_DHT22_HUM_A:
            try:
                self.hum_A = float(payload)
                self.root.after(0, self.update_avg_dht)
            except ValueError:
                self.log(f"Payload kelembaban MCU A tidak valid: {payload}")

        # --- DHT22 MCU B ---
        elif msg.topic == TOPIC_DHT22_TEMP_B:
            try:
                self.temp_B = float(payload)
                self.root.after(0, self.update_avg_dht)
            except ValueError:
                self.log(f"Payload suhu MCU B tidak valid: {payload}")

        elif msg.topic == TOPIC_DHT22_HUM_B:
            try:
                self.hum_B = float(payload)
                self.root.after(0, self.update_avg_dht)
            except ValueError:
                self.log(f"Payload kelembaban MCU B tidak valid: {payload}")
    
    def publish(self, topic, message):
        self.log(f"Publish: {topic} -> {message}")
        if hasattr(self, 'client'):
            self.client.publish(topic, message)
    
    def run_mqtt(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_forever()
        except Exception as e:
            self.log(f"Error MQTT: {e}")
            self.update_connection_status("disconnected")
    
    def start_services(self):
        # Start MQTT thread
        self.mqtt_thread = threading.Thread(target=self.run_mqtt)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()
        
        # Start clock
        self.update_clock()
        
        # Start Weather thread
        self.weather_thread = threading.Thread(target=self.update_weather_loop)
        self.weather_thread.daemon = True
        self.weather_thread.start()

    def extract_rain_from_dict(self, data_dict):
        """
        Mencoba ekstrak curah hujan dari berbagai kemungkinan key/struktur
        Mengembalikan float (mm) atau None jika tidak ditemukan.
        """
        if not isinstance(data_dict, dict):
            return None

        RAIN_KEYS = ["rain", "precip", "rainfall", "rr", "p", "precipitation"]
        for k in RAIN_KEYS:
            if k in data_dict:
                val = data_dict[k]
                if isinstance(val, dict):
                    for subk, subv in val.items():
                        try:
                            return float(subv)
                        except Exception:
                            continue
                else:
                    try:
                        return float(val)
                    except Exception:
                        continue

        for v in data_dict.values():
            if isinstance(v, dict):
                for k2 in RAIN_KEYS:
                    if k2 in v:
                        try:
                            sub = v[k2]
                            if isinstance(sub, dict):
                                for subv in sub.values():
                                    try:
                                        return float(subv)
                                    except Exception:
                                        continue
                            else:
                                return float(sub)
                        except Exception:
                            continue
        return None

    def update_weather_loop(self):
        """Loop untuk ambil data cuaca secara berkala"""
        while True:
            try:
                data = fetch_weather_data()
                if data:
                    suhu = data.get("temp") if "temp" in data else data.get("temperature")
                    kelembaban = data.get("hum") if "hum" in data else data.get("humidity")
                    angin = data.get("wspd") if "wspd" in data else data.get("wind_speed")

                    rain = self.extract_rain_from_dict(data)

                    if suhu is not None:
                        try:
                            self.weather_temp.after(0, lambda s=suhu: self.weather_temp.update_value(f"{float(s):.1f}"))
                        except Exception:
                            pass
                    if kelembaban is not None:
                        try:
                            self.weather_hum.after(0, lambda h=kelembaban: self.weather_hum.update_value(f"{float(h):.1f}"))
                        except Exception:
                            pass
                    if angin is not None:
                        try:
                            self.weather_wind.after(0, lambda w=angin: self.weather_wind.update_value(f"{float(w):.1f}"))
                        except Exception:
                            pass
                    if rain is not None:
                        try:
                            self.weather_rain.after(0, lambda r=rain: self.weather_rain.update_value(f"{float(r):.1f}"))
                        except Exception:
                            pass
                    else:
                        self.weather_rain.after(0, lambda: self.weather_rain.update_value("--.-"))
                else:
                    self.log("⚠️ Gagal mengambil data cuaca (data kosong)")
            except Exception as e:
                self.log(f"⚠️ Error di weather thread: {e}")

            time.sleep(5) 

# -------------------- RUN APPLICATION --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDashboard(root)
    root.mainloop()
