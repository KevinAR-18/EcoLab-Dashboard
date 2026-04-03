#!/usr/bin/env python3
"""
EcoLab Smart Socket Simulator (Python) - Socket 3
Menirukan ESP32 Smart Socket dengan PZEM + RTC + Timer + Schedule

- Subscribe: ecolab/socket/3/control, ecolab/socket/3/timer, ecolab/socket/3/schedule/*
- Publish: ecolab/socket/3/energy, ecolab/socket/3/relaystatus, ecolab/socket/3/timer/status
- Publish: ecolab/socket/3/schedule/status, ecolab/socket/3/datetime/status
- LWT: ecolab/socket/3/devicestatus

REALISTIC MODE:
- Saat Relay OFF: V=220-240V, I=0A, P=0W, F=50Hz, PF=0
- Saat Relay ON: V=220-240V, I=input beban, P=V*I*PF, F=50Hz, PF=0.85-0.95
"""

import json
import os
import random
import time
import ssl
import threading
from datetime import datetime
import paho.mqtt.client as mqtt

# ============================================================
# CONFIG
# ============================================================
MQTT_BROKER = "DESKTOP-CVPE153"  # Ganti dengan IP broker
# MQTT_BROKER = "10.33.11.148"
MQTT_PORT = 8883  # TLS
MQTT_USERNAME = "smartsocket3"
MQTT_PASSWORD = "smart3"
CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")
# CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca2.crt")

# Topics
TOPIC_CONTROL = "ecolab/socket/3/control"
TOPIC_ENERGY = "ecolab/socket/3/energy"
TOPIC_DEVICE_STATUS = "ecolab/socket/3/devicestatus"
TOPIC_RELAY_STATUS = "ecolab/socket/3/relaystatus"
TOPIC_TIMER = "ecolab/socket/3/timer"
TOPIC_TIMER_STATUS = "ecolab/socket/3/timer/status"
TOPIC_SCHEDULE_START = "ecolab/socket/3/schedule/start"
TOPIC_SCHEDULE_STOP = "ecolab/socket/3/schedule/stop"
TOPIC_SCHEDULE_MODE = "ecolab/socket/3/schedule/mode"
TOPIC_SCHEDULE_STATUS = "ecolab/socket/3/schedule/status"
TOPIC_DATETIME_STATUS = "ecolab/socket/3/datetime/status"

# ============================================================
# STATE
# ============================================================
relay_state = False
client = None

# Timer state
timer_active = False
timer_start_millis = 0
timer_duration = 0

# Schedule state
schedule_start_active = False
schedule_stop_active = False
sched_start_hour = 0
sched_start_minute = 0
sched_stop_hour = 0
sched_stop_minute = 0
schedule_daily_mode = True
last_triggered_day = None
start_triggered = False
stop_triggered = False

# ================= REALISTIC SENSOR STATE =================
# User input beban (dalam Ampere)
load_current = 0.0  # Default 0A (tanpa beban)

# Base values (konstan)
base_voltage = 220.0  # V
base_frequency = 50.0  # Hz

# PZEM energy state (simulated)
accumulated_energy = 0.0  # kWh

# Flag untuk user input
running = True  # Flag untuk stop input thread

# ============================================================
# MQTT CALLBACKS
# ============================================================
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code: {rc}")

    # Subscribe to all command topics
    client.subscribe(TOPIC_CONTROL)
    client.subscribe(TOPIC_TIMER)
    client.subscribe(TOPIC_SCHEDULE_START)
    client.subscribe(TOPIC_SCHEDULE_STOP)
    client.subscribe(TOPIC_SCHEDULE_MODE)

    print(f"[MQTT] Subscribed: {TOPIC_CONTROL}")
    print(f"[MQTT] Subscribed: {TOPIC_TIMER}")
    print(f"[MQTT] Subscribed: {TOPIC_SCHEDULE_START}")
    print(f"[MQTT] Subscribed: {TOPIC_SCHEDULE_STOP}")
    print(f"[MQTT] Subscribed: {TOPIC_SCHEDULE_MODE}")

    # Send initial status
    send_device_status("ONLINE")
    publish_status_sync()

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected: {rc}")

def on_message(client, userdata, msg):
    global relay_state, timer_active, timer_start_millis, timer_duration
    global schedule_start_active, schedule_stop_active, sched_start_hour, sched_start_minute
    global sched_stop_hour, sched_stop_minute, schedule_daily_mode
    global last_triggered_day, start_triggered, stop_triggered

    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\n[MQTT] Received: {topic} -> {payload}")

    # ================= CONTROL RELAY =================
    if topic == TOPIC_CONTROL:
        if payload == "ON":
            relay_state = True
            print(f"[RELAY] Power: ON")
            send_relay_status()

        elif payload == "OFF":
            relay_state = False
            print(f"[RELAY] Power: OFF")
            send_relay_status()

    # ================= TIMER =================
    elif topic == TOPIC_TIMER:
        duration = int(payload)

        if duration == 0:
            # Cancel timer
            timer_active = False
            publish_status_sync()
            print("[TIMER] Cancelled")
        else:
            # Set timer (seconds to ms)
            timer_duration = duration * 1000
            timer_start_millis = current_millis()
            timer_active = True

            print(f"[TIMER] Set: {duration} seconds")
            publish_status_sync()

    # ================= SCHEDULE START =================
    elif topic == TOPIC_SCHEDULE_START:
        if payload == "CLEAR":
            schedule_start_active = False
            start_triggered = False
            publish_status_sync()
            save_schedule_to_file()
            print("[SCHEDULE] Start cancelled")
        else:
            # Format: HH:MM
            try:
                parts = payload.split(':')
                sched_start_hour = int(parts[0])
                sched_start_minute = int(parts[1])

                schedule_start_active = True
                start_triggered = False

                print(f"[SCHEDULE] Start set: {payload}")
                publish_status_sync()
                save_schedule_to_file()
            except:
                client.publish(TOPIC_SCHEDULE_STATUS, "FORMAT ERROR")

    # ================= SCHEDULE STOP =================
    elif topic == TOPIC_SCHEDULE_STOP:
        if payload == "CLEAR":
            schedule_stop_active = False
            stop_triggered = False
            publish_status_sync()
            save_schedule_to_file()
            print("[SCHEDULE] Stop cancelled")
        else:
            # Format: HH:MM
            try:
                parts = payload.split(':')
                sched_stop_hour = int(parts[0])
                sched_stop_minute = int(parts[1])

                schedule_stop_active = True
                stop_triggered = False

                print(f"[SCHEDULE] Stop set: {payload}")
                publish_status_sync()
                save_schedule_to_file()
            except:
                client.publish(TOPIC_SCHEDULE_STATUS, "FORMAT ERROR")

    # ================= SCHEDULE MODE =================
    elif topic == TOPIC_SCHEDULE_MODE:
        if payload == "daily":
            schedule_daily_mode = True
            last_triggered_day = None
            publish_status_sync()
            save_schedule_to_file()
            print("[SCHEDULE] Mode: Daily")
        elif payload == "onetime":
            schedule_daily_mode = False
            last_triggered_day = None
            start_triggered = False
            stop_triggered = False
            publish_status_sync()
            save_schedule_to_file()
            print("[SCHEDULE] Mode: Onetime")
        else:
            client.publish(TOPIC_SCHEDULE_STATUS, "MODE ERROR")

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def current_millis():
    """Get current time in milliseconds (simulating Arduino millis())"""
    return int(time.time() * 1000)

def send_device_status(status):
    """Publish device status (LWT)"""
    client.publish(TOPIC_DEVICE_STATUS, status, retain=True)
    print(f"[MQTT] Published: {TOPIC_DEVICE_STATUS} -> {status} (retain)")

def send_relay_status():
    """Publish relay status dengan retain=True"""
    payload = "ON" if relay_state else "OFF"
    client.publish(TOPIC_RELAY_STATUS, payload, retain=True)
    print(f"[MQTT] Published: {TOPIC_RELAY_STATUS} -> {payload} (retain)")

# ================= JSON SAVE/LOAD =================
SCHEDULE_FILE = "schedule_socket3.json"

def save_schedule_to_file():
    """Simpan state schedule ke file JSON"""
    global schedule_start_active, schedule_stop_active
    global sched_start_hour, sched_start_minute
    global sched_stop_hour, sched_stop_minute
    global schedule_daily_mode

    schedule_data = {
        "start_active": schedule_start_active,
        "start_hour": sched_start_hour,
        "start_minute": sched_start_minute,
        "stop_active": schedule_stop_active,
        "stop_hour": sched_stop_hour,
        "stop_minute": sched_stop_minute,
        "daily_mode": schedule_daily_mode
    }

    try:
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(schedule_data, f, indent=2)
        print(f"[JSON] Schedule saved to {SCHEDULE_FILE}")
    except Exception as e:
        print(f"[JSON] Error saving schedule: {e}")

def load_schedule_from_file():
    """Load state schedule dari file JSON"""
    global schedule_start_active, schedule_stop_active
    global sched_start_hour, sched_start_minute
    global sched_stop_hour, sched_stop_minute
    global schedule_daily_mode

    if not os.path.exists(SCHEDULE_FILE):
        print(f"[JSON] Schedule file not found, using defaults")
        return

    try:
        with open(SCHEDULE_FILE, "r") as f:
            schedule_data = json.load(f)

        schedule_start_active = schedule_data.get("start_active", False)
        sched_start_hour = schedule_data.get("start_hour", 0)
        sched_start_minute = schedule_data.get("start_minute", 0)
        schedule_stop_active = schedule_data.get("stop_active", False)
        sched_stop_hour = schedule_data.get("stop_hour", 0)
        sched_stop_minute = schedule_data.get("stop_minute", 0)
        schedule_daily_mode = schedule_data.get("daily_mode", True)

        mode_str = "Daily" if schedule_daily_mode else "Onetime"
        print(f"[JSON] Schedule loaded from {SCHEDULE_FILE}")
        print(f"[JSON] Mode: {mode_str}, Start: {sched_start_hour:02d}:{sched_start_minute:02d}, "
              f"Stop: {sched_stop_hour:02d}:{sched_stop_minute:02d}")
    except Exception as e:
        print(f"[JSON] Error loading schedule: {e}")

def send_energy_data():
    """Publish PZEM energy data (REALISTIC MODE)"""
    global accumulated_energy

    if relay_state:
        # ================= RELAY ON =================
        # Voltage: tetap 220-240V (dengan sedikit fluktuasi)
        voltage = round(base_voltage + random.uniform(-2, 2), 2)  # 218-242V

        # Current: sesuai input beban user (dengan sedikit fluktuasi)
        if load_current > 0:
            current = round(load_current + random.uniform(-0.01, 0.01), 3)
            current = max(0, current)  # Pastikan tidak negatif
        else:
            current = 0.0

        # Power Factor: 0.85-0.95 (random)
        pf = round(random.uniform(0.85, 0.95), 2)

        # Power: V x I x PF
        power = round(voltage * current * pf, 2)

        # Frequency: tetap ~50Hz
        frequency = round(base_frequency + random.uniform(-0.2, 0.2), 1)

        # Accumulate energy (kWh) - power in kW, time in hours (2 seconds = 2/3600 hours)
        energy_increment = (power / 1000) * (2 / 3600)
        accumulated_energy += energy_increment
        energy = round(accumulated_energy, 3)
    else:
        # ================= RELAY OFF =================
        # Voltage: TETAP terbaca (listrik masih ada)
        voltage = round(base_voltage + random.uniform(-2, 2), 2)  # 218-242V

        # Current: 0A (tidak ada beban)
        current = 0.0

        # Power: 0W
        power = 0.0

        # Frequency: tetap ~50Hz
        frequency = round(base_frequency + random.uniform(-0.2, 0.2), 1)

        # PF: 0 (tidak ada beban)
        pf = 0.0

        # Energy: keep accumulated (tidak bertambah)
        energy = round(accumulated_energy, 3)

    # Create JSON payload
    payload = {
        "voltage": voltage,
        "current": current,
        "power": power,
        "energy": energy,
        "frequency": frequency,
        "pf": pf
    }

    client.publish(TOPIC_ENERGY, json.dumps(payload))
    print(f"[PZEM] V:{voltage}V I:{current}A P:{power}W E:{energy}kWh F:{frequency}Hz PF:{pf}")

def publish_status_sync():
    """Publish all status (for multi-GUI sync)"""
    # Relay status
    send_relay_status()

    # Timer status
    if timer_active:
        elapsed = current_millis() - timer_start_millis
        remaining = max(0, timer_duration - elapsed)
        remaining_sec = int(remaining / 1000)
        timer_payload = f"ACTIVE:{remaining_sec}s"
        client.publish(TOPIC_TIMER_STATUS, timer_payload, retain=True)
    else:
        client.publish(TOPIC_TIMER_STATUS, "INACTIVE", retain=True)

    # Schedule status (JSON)
    schedule_payload = {}

    if schedule_start_active:
        schedule_payload["start"] = f"{sched_start_hour:02d}:{sched_start_minute:02d}"
    else:
        schedule_payload["start"] = None

    if schedule_stop_active:
        schedule_payload["stop"] = f"{sched_stop_hour:02d}:{sched_stop_minute:02d}"
    else:
        schedule_payload["stop"] = None

    schedule_payload["mode"] = "daily" if schedule_daily_mode else "onetime"

    client.publish(TOPIC_SCHEDULE_STATUS, json.dumps(schedule_payload), retain=True)

    # DateTime status (simulated NTP sync)
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # Day of week (1=Monday, 7=Sunday)
    day_of_week = now.isoweekday()
    status = f"OK:NTP_SYNCED:{datetime_str} {day_of_week}"
    client.publish(TOPIC_DATETIME_STATUS, status, retain=True)

# ============================================================
# TIMER & SCHEDULE HANDLING
# ============================================================
def handle_timer():
    """Handle timer countdown"""
    global timer_active, relay_state

    if timer_active:
        elapsed = current_millis() - timer_start_millis
        if elapsed >= timer_duration:
            timer_active = False
            relay_state = False  # Matikan relay

            print("[TIMER] Timer done - Relay OFF")

            # Publish relay status OFF ke MQTT
            send_relay_status()

            # Publish timer status DONE
            client.publish(TOPIC_TIMER_STATUS, "TIMER_DONE")

            # Publish full status sync
            publish_status_sync()

def handle_schedule():
    """Handle schedule (start/stop)"""
    global relay_state, start_triggered, stop_triggered, last_triggered_day

    if not schedule_start_active and not schedule_stop_active:
        return

    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_day = now.day

    # ================= RESET FOR NEW DAY (ONETIME MODE) =================
    if not schedule_daily_mode:
        if current_day != last_triggered_day:
            last_triggered_day = current_day
            start_triggered = False
            stop_triggered = False

    # ================= SCHEDULE START (TURN ON) =================
    if schedule_start_active:
        if current_hour == sched_start_hour and current_minute == sched_start_minute:
            if not start_triggered:
                start_triggered = True
                relay_state = True

                print("[SCHEDULE] Start triggered - Relay ON")
                send_relay_status()
                client.publish(TOPIC_SCHEDULE_STATUS, "START_TRIGGER")

    # ================= SCHEDULE STOP (TURN OFF) =================
    if schedule_stop_active:
        if current_hour == sched_stop_hour and current_minute == sched_stop_minute:
            if not stop_triggered:
                stop_triggered = True
                relay_state = False

                print("[SCHEDULE] Stop triggered - Relay OFF")
                send_relay_status()
                client.publish(TOPIC_SCHEDULE_STATUS, "STOP_TRIGGER")

    # ================= RESET TRIGGERS (DAILY MODE) =================
    if schedule_daily_mode:
        # Track last checked minute
        if not hasattr(handle_schedule, 'last_checked_minute'):
            handle_schedule.last_checked_minute = -1

        if current_minute != handle_schedule.last_checked_minute:
            handle_schedule.last_checked_minute = current_minute

            # Reset start trigger if past the scheduled time
            if current_hour != sched_start_hour or current_minute != sched_start_minute:
                if start_triggered:
                    start_triggered = False
                    print("[SCHEDULE] Start trigger reset (daily mode)")

            # Reset stop trigger if past the scheduled time
            if current_hour != sched_stop_hour or current_minute != sched_stop_minute:
                if stop_triggered:
                    stop_triggered = False
                    print("[SCHEDULE] Stop trigger reset (daily mode)")

    # ================= RECOVERY LOGIC =================
    # Kalau relay mati tapi seharusnya nyala (dalam rentang schedule), nyalakan lagi
    # Ini untuk recovery setelah reboot/power loss
    if not timer_active:  # Timer lebih prioritas, jangan override
        if schedule_start_active and schedule_stop_active:
            # Cek apakah sekarang dalam rentang schedule
            now_minutes = current_hour * 60 + current_minute
            start_minutes = sched_start_hour * 60 + sched_start_minute
            stop_minutes = sched_stop_hour * 60 + sched_stop_minute

            should_be_on = False

            # Untuk schedule yang melewati tengah malam (misal 23:00 - 02:00)
            if start_minutes < stop_minutes:
                # Normal: 07:00 - 20:00
                should_be_on = (now_minutes >= start_minutes and now_minutes < stop_minutes)
            else:
                # Lewat tengah malam: 23:00 - 02:00
                should_be_on = (now_minutes >= start_minutes or now_minutes < stop_minutes)

            # Recovery: Nyalakan jika seharusnya ON tapi sekarang OFF
            if should_be_on and not relay_state:
                relay_state = True
                send_relay_status()
                print(f"[RECOVERY] Relay ON (within schedule range: {sched_start_hour:02d}:{sched_start_minute:02d} - {sched_stop_hour:02d}:{sched_stop_minute:02d})")

# ============================================================
# USER INPUT THREAD (Beban/Load)
# ============================================================
def input_thread():
    """Thread untuk input beban dari user"""
    global load_current, running

    print("\n" + "=" * 60)
    print("📝 INPUT BEBAN (LOAD CURRENT) - SOCKET 3")
    print("=" * 60)
    print("Masukkan nilai arus beban dalam Ampere (A)")
    print("Contoh:")
    print("  0    = Tanpa beban (0 A)")
    print("  0.5  = Beban ringan (0.5 A)")
    print("  1.0  = Beban sedang (1.0 A)")
    print("  2.0  = Beban berat (2.0 A)")
    print("  q    = Keluar")
    print("-" * 60)

    while running:
        try:
            user_input = input("\n>> Masukkan beban (A): ").strip()

            if user_input.lower() == 'q':
                print("\n[INFO] Keluar dari input thread...")
                break

            # Parse input
            current_val = float(user_input)

            if current_val < 0:
                print("[ERROR] Nilai tidak boleh negatif!")
            elif current_val > 10:
                print("[WARNING] Nilai terlalu besar! Max 10A untuk safety.")
            else:
                load_current = current_val
                print(f"[INFO] Beban di-set ke: {load_current} A")
                print(f"[INFO] Saat Relay ON, power akan: V × {load_current}A × PF")

        except ValueError:
            print("[ERROR] Input tidak valid! Masukkan angka (contoh: 0.5)")
        except KeyboardInterrupt:
            print("\n[INFO] Input thread dihentikan...")
            break


# ============================================================
# LED SIMULATION (Console Output)
# ============================================================
def simulate_leds():
    """Simulate LED indicators via console"""
    status = []

    if relay_state:
        status.append("🟢 RELAY: ON")
    else:
        status.append("🔴 RELAY: OFF")

    # Load status
    if relay_state and load_current > 0:
        status.append(f"⚡ BEBAN: {load_current}A")
    elif relay_state:
        status.append("⚠️ BEBAN: 0A (Set beban dulu!)")
    else:
        status.append(f"📦 BEBAN: {load_current}A (standby)")

    if timer_active:
        elapsed = current_millis() - timer_start_millis
        remaining = max(0, timer_duration - elapsed)
        status.append(f"⏱️ TIMER: {remaining//1000}s")

    if schedule_start_active or schedule_stop_active:
        mode = "📅 DAILY" if schedule_daily_mode else "📆 ONETIME"
        status.append(mode)

        if schedule_start_active:
            status.append(f"▶️ START: {sched_start_hour:02d}:{sched_start_minute:02d}")
        if schedule_stop_active:
            status.append(f"⏹️ STOP: {sched_stop_hour:02d}:{sched_stop_minute:02d}")

    # Print status line (overwrite previous line)
    status_str = " | ".join(status)
    print(f"\r[SOCKET 3] {status_str}    ", end="", flush=True)


# ============================================================
# HELPER: Tampilkan Info Beban
# ============================================================
def show_load_info():
    """Tampilkan info beban saat ini"""
    print(f"\n{'=' * 60}")
    print(f"📊 KONDISI SAAT INI - SOCKET 3")
    print(f"{'=' * 60}")
    print(f"Relay       : {'ON' if relay_state else 'OFF'}")
    print(f"Beban (Load) : {load_current} A")
    print(f"\nEstimasi Power saat Relay ON:")
    if load_current > 0:
        estimated_power = base_voltage * load_current * 0.9  # Asumsi PF 0.9
        print(f"  V × I × PF = {base_voltage}V × {load_current}A × 0.9")
        print(f"  ≈ {estimated_power:.1f} Watt")
    else:
        print(f"  0 Watt (beban 0A)")
    print(f"{'=' * 60}\n")


# ============================================================
# MAIN
# ============================================================
def main():
    global client, running

    print("=" * 60)
    print("EcoLab Smart Socket Simulator - Socket 3")
    print("=" * 60)
    print("Features:")
    print("  - Relay Control (ON/OFF)")
    print("  - Timer Countdown")
    print("  - Schedule (Start/Stop) with Daily/Onetime mode")
    print("  - PZEM Energy Monitoring (REALISTIC MODE)")
    print("  - RTC with NTP Sync (simulated)")
    print("  - LED Indicators")
    print("  - Load Current Input (User Adjustable)")
    print("=" * 60)
    print("\n⚠️  REALISTIC MODE:")
    print("  - Saat Relay OFF: V=220V, I=0A, P=0W, F=50Hz, PF=0")
    print("  - Saat Relay ON: V=220V, I=input beban, P=V×I×PF, F=50Hz")
    print("\n💡 Anda bisa input beban (load current) kapan saja")
    print("   melalui input thread yang terpisah.\n")

    # Create MQTT client
    client = mqtt.Client(client_id="smartsocket3_simulator")

    # Set TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CA_CERT)
    client.tls_set_context(context)

    # Set callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Set LWT
    client.will_set(TOPIC_DEVICE_STATUS, "OFFLINE", qos=0, retain=True)

    # Connect
    print(f"\n[INFO] Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        # Load schedule dari file JSON
        load_schedule_from_file()

        # Main loop timing
        last_energy_time = time.time()
        last_status_sync_time = time.time()
        last_debug_time = time.time()

        ENERGY_INTERVAL = 2  # Send energy every 2 seconds
        STATUS_SYNC_INTERVAL = 2  # Send status sync every 2 seconds
        DEBUG_INTERVAL = 10  # Debug print every 10 seconds

        print("\n[INFO] Simulator running. Press Ctrl+C to exit.\n")

        # ================= START INPUT THREAD =================
        # Start thread untuk input beban
        input_thread_handle = threading.Thread(target=input_thread, daemon=True)
        input_thread_handle.start()

        # Tampilkan info awal
        show_load_info()

        # Main loop
        last_show_info_time = time.time()

        while True:
            try:
                current_time = time.time()

                # Send energy data periodically
                if current_time - last_energy_time >= ENERGY_INTERVAL:
                    last_energy_time = current_time
                    send_energy_data()
                    print()  # New line after energy data

                # Send status sync periodically
                if current_time - last_status_sync_time >= STATUS_SYNC_INTERVAL:
                    last_status_sync_time = current_time
                    publish_status_sync()

                # Debug print periodically
                if current_time - last_debug_time >= DEBUG_INTERVAL:
                    last_debug_time = current_time

                    now = datetime.now()
                    print(f"\n[RTC] {now.strftime('%Y-%m-%d %H:%M:%S')}")

                    if schedule_start_active or schedule_stop_active:
                        print(f"[SCHEDULE] Start: {sched_start_hour:02d}:{sched_start_minute:02d} "
                              f"Stop: {sched_stop_hour:02d}:{sched_stop_minute:02d} "
                              f"Mode: {'Daily' if schedule_daily_mode else 'Onetime'}")

                # Tampilkan info beban setiap 30 detik
                if current_time - last_show_info_time >= 30:
                    last_show_info_time = current_time
                    show_load_info()

                # Handle timer and schedule
                handle_timer()
                handle_schedule()

                # Simulate LED indicators
                simulate_leds()

                time.sleep(0.1)

            except KeyboardInterrupt:
                print("\n\n[INFO] Shutting down...")
                running = False  # Stop input thread
                send_device_status("OFFLINE")
                client.loop_stop()
                client.disconnect()
                break

    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    main()
