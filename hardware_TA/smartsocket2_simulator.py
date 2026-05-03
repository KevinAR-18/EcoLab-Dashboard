#!/usr/bin/env python3
"""
EcoLab Smart Socket Simulator (Python)
Menirukan ESP32 Smart Socket dengan PZEM + RTC + Timer + Schedule

- Subscribe: ecolab/socket/2/control, ecolab/socket/2/timer, ecolab/socket/2/schedule/*
- Publish: ecolab/socket/2/energy, ecolab/socket/2/relaystatus, ecolab/socket/2/timer/status
- Publish: ecolab/socket/2/schedule/status
- LWT: ecolab/socket/2/devicestatus

FIRMWARE-LIKE MODE:
- Saat Relay OFF: V=0V, I=0A, P=0W, E=0kWh, F=0Hz, PF=0
- Saat Relay ON: V=220-240V, I=input beban, P=V*I*PF, F=50Hz, PF=0.85-0.95
"""

import json
import os
import random
import ssl
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# ============================================================
# CONFIG
# ============================================================
# MQTT_BROKER = "10.33.11.148"
MQTT_BROKER = "DESKTOP-CVPE153"
MQTT_PORT = 8883  # TLS
MQTT_USERNAME = "smartsocket2"
MQTT_PASSWORD = "smart2"
# CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")
CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca2.crt")

# Topics
TOPIC_CONTROL = "ecolab/socket/2/control"
TOPIC_ENERGY = "ecolab/socket/2/energy"
TOPIC_DEVICE_STATUS = "ecolab/socket/2/devicestatus"
TOPIC_RELAY_STATUS = "ecolab/socket/2/relaystatus"
TOPIC_TIMER = "ecolab/socket/2/timer"
TOPIC_TIMER_STATUS = "ecolab/socket/2/timer/status"
TOPIC_SCHEDULE_START = "ecolab/socket/2/schedule/start"
TOPIC_SCHEDULE_STOP = "ecolab/socket/2/schedule/stop"
TOPIC_SCHEDULE_MODE = "ecolab/socket/2/schedule/mode"
TOPIC_SCHEDULE_STATUS = "ecolab/socket/2/schedule/status"

# ============================================================
# STATE
# ============================================================
relay_state = False
manual_relay_state = False
client = None
mqtt_connected = False
last_mqtt_retry = 0.0

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

# ================= FIRMWARE-LIKE SENSOR STATE =================
load_current = 0.0
base_voltage = 220.0
base_frequency = 50.0
accumulated_energy = 0.0
running = True

SCHEDULE_FILE = "schedule_socket2.json"


def current_millis():
    return int(time.time() * 1000)


def is_within_scheduled_on_window(now):
    if not schedule_start_active or not schedule_stop_active:
        return False

    now_minutes = now.hour * 60 + now.minute
    start_minutes = sched_start_hour * 60 + sched_start_minute
    stop_minutes = sched_stop_hour * 60 + sched_stop_minute

    if start_minutes == stop_minutes:
        return False
    if start_minutes < stop_minutes:
        return start_minutes <= now_minutes < stop_minutes
    return now_minutes >= start_minutes or now_minutes < stop_minutes


def save_schedule_to_file():
    schedule_data = {
        "start_active": schedule_start_active,
        "start_hour": sched_start_hour,
        "start_minute": sched_start_minute,
        "stop_active": schedule_stop_active,
        "stop_hour": sched_stop_hour,
        "stop_minute": sched_stop_minute,
        "daily_mode": schedule_daily_mode,
        "manual_relay_state": manual_relay_state,
    }

    try:
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(schedule_data, f, indent=2)
        print(f"[JSON] State saved to {SCHEDULE_FILE}")
    except Exception as e:
        print(f"[JSON] Error saving state: {e}")


def restore_relay_state():
    global relay_state

    if schedule_start_active and schedule_stop_active:
        if is_within_scheduled_on_window(datetime.now()):
            relay_state = True
            print("[JSON] Relay restored from active schedule window: ON")
        else:
            relay_state = False
            print("[JSON] Relay restored from schedule window: OFF")
        return

    if schedule_start_active or schedule_stop_active:
        print("[JSON] Schedule partially active, fallback to saved manual relay state")

    relay_state = manual_relay_state
    print(f"[JSON] Restored manual relay state: {'ON' if relay_state else 'OFF'}")


def load_schedule_from_file():
    global schedule_start_active, schedule_stop_active
    global sched_start_hour, sched_start_minute
    global sched_stop_hour, sched_stop_minute
    global schedule_daily_mode, manual_relay_state

    if not os.path.exists(SCHEDULE_FILE):
        print("[JSON] Schedule file not found, using defaults")
        restore_relay_state()
        return

    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            schedule_data = json.load(f)

        schedule_start_active = schedule_data.get("start_active", False)
        sched_start_hour = schedule_data.get("start_hour", 0)
        sched_start_minute = schedule_data.get("start_minute", 0)
        schedule_stop_active = schedule_data.get("stop_active", False)
        sched_stop_hour = schedule_data.get("stop_hour", 0)
        sched_stop_minute = schedule_data.get("stop_minute", 0)
        schedule_daily_mode = schedule_data.get("daily_mode", True)
        manual_relay_state = schedule_data.get("manual_relay_state", False)

        mode_str = "Daily" if schedule_daily_mode else "Onetime"
        print(f"[JSON] State loaded from {SCHEDULE_FILE}")
        print(
            f"[JSON] Mode: {mode_str}, Start: {sched_start_hour:02d}:{sched_start_minute:02d}, "
            f"Stop: {sched_stop_hour:02d}:{sched_stop_minute:02d}"
        )
    except Exception as e:
        print(f"[JSON] Error loading state: {e}")

    restore_relay_state()


def send_device_status(status, retain=True):
    if client is None:
        return
    client.publish(TOPIC_DEVICE_STATUS, status, retain=retain)
    retain_text = "retain" if retain else "no retain"
    print(f"[MQTT] Published: {TOPIC_DEVICE_STATUS} -> {status} ({retain_text})")


def send_relay_status():
    if client is None:
        return
    payload = "ON" if relay_state else "OFF"
    client.publish(TOPIC_RELAY_STATUS, payload, retain=True)
    print(f"[MQTT] Published: {TOPIC_RELAY_STATUS} -> {payload} (retain)")


def publish_status_sync():
    send_relay_status()

    if timer_active:
        elapsed = current_millis() - timer_start_millis
        remaining = max(0, timer_duration - elapsed)
        remaining_sec = int(remaining / 1000)
        client.publish(TOPIC_TIMER_STATUS, f"ACTIVE:{remaining_sec}s", retain=True)
    else:
        client.publish(TOPIC_TIMER_STATUS, "INACTIVE", retain=True)

    schedule_payload = {
        "start": f"{sched_start_hour:02d}:{sched_start_minute:02d}" if schedule_start_active else None,
        "stop": f"{sched_stop_hour:02d}:{sched_stop_minute:02d}" if schedule_stop_active else None,
        "mode": "daily" if schedule_daily_mode else "onetime",
    }
    client.publish(TOPIC_SCHEDULE_STATUS, json.dumps(schedule_payload), retain=True)


def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    mqtt_connected = rc == 0
    print(f"[MQTT] Connected with result code: {rc}")

    if not mqtt_connected:
        return

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

    send_device_status("ONLINE")
    publish_status_sync()


def on_disconnect(client, userdata, rc):
    global mqtt_connected
    mqtt_connected = False
    print(f"[MQTT] Disconnected: {rc}")


def on_message(client, userdata, msg):
    global relay_state, manual_relay_state
    global timer_active, timer_start_millis, timer_duration
    global schedule_start_active, schedule_stop_active, sched_start_hour, sched_start_minute
    global sched_stop_hour, sched_stop_minute, schedule_daily_mode
    global last_triggered_day, start_triggered, stop_triggered

    topic = msg.topic
    payload = msg.payload.decode()

    print(f"\n[MQTT] Received: {topic} -> {payload}")

    if topic == TOPIC_CONTROL:
        if payload == "ON":
            relay_state = True
            manual_relay_state = True
            save_schedule_to_file()
            print("[RELAY] Power: ON")
            send_relay_status()
        elif payload == "OFF":
            relay_state = False
            manual_relay_state = False
            save_schedule_to_file()
            print("[RELAY] Power: OFF")
            send_relay_status()

    elif topic == TOPIC_TIMER:
        try:
            duration = int(payload)
        except ValueError:
            duration = 0

        if duration == 0:
            timer_active = False
            client.publish(TOPIC_TIMER_STATUS, "INACTIVE", retain=True)
            print("[TIMER] Cancelled")
        else:
            timer_duration = duration * 1000
            timer_start_millis = current_millis()
            timer_active = True
            print(f"[TIMER] Set: {duration} seconds")
            publish_status_sync()

    elif topic == TOPIC_SCHEDULE_START:
        if payload == "CLEAR":
            schedule_start_active = False
            start_triggered = False
            publish_status_sync()
            save_schedule_to_file()
            print("[SCHEDULE] Start cancelled")
        else:
            try:
                parts = payload.split(":")
                sched_start_hour = int(parts[0])
                sched_start_minute = int(parts[1])
                schedule_start_active = True
                start_triggered = False
                print(f"[SCHEDULE] Start set: {payload}")
                publish_status_sync()
                save_schedule_to_file()
            except Exception:
                client.publish(TOPIC_SCHEDULE_STATUS, "FORMAT ERROR")

    elif topic == TOPIC_SCHEDULE_STOP:
        if payload == "CLEAR":
            schedule_stop_active = False
            stop_triggered = False
            publish_status_sync()
            save_schedule_to_file()
            print("[SCHEDULE] Stop cancelled")
        else:
            try:
                parts = payload.split(":")
                sched_stop_hour = int(parts[0])
                sched_stop_minute = int(parts[1])
                schedule_stop_active = True
                stop_triggered = False
                print(f"[SCHEDULE] Stop set: {payload}")
                publish_status_sync()
                save_schedule_to_file()
            except Exception:
                client.publish(TOPIC_SCHEDULE_STATUS, "FORMAT ERROR")

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


def ensure_mqtt_connection():
    global mqtt_connected, last_mqtt_retry

    if mqtt_connected:
        return

    now = time.time()
    if now - last_mqtt_retry < 5:
        return

    last_mqtt_retry = now
    print("[MQTT] Attempting reconnect...")
    try:
        client.reconnect()
    except Exception as exc:
        print(f"[MQTT] Reconnect failed: {exc}")


def send_energy_data():
    global accumulated_energy

    if relay_state:
        voltage = round(base_voltage + random.uniform(-2, 2), 2)
        if load_current > 0:
            current = round(load_current + random.uniform(-0.01, 0.01), 3)
            current = max(0, current)
        else:
            current = 0.0
        pf = round(random.uniform(0.85, 0.95), 2)
        power = round(voltage * current * pf, 2)
        frequency = round(base_frequency + random.uniform(-0.2, 0.2), 1)
        energy_increment = (power / 1000) * (2 / 3600)
        accumulated_energy += energy_increment
        energy = round(accumulated_energy, 3)
    else:
        voltage = 0.0
        current = 0.0
        power = 0.0
        energy = 0.0
        frequency = 0.0
        pf = 0.0

    payload = {
        "voltage": voltage,
        "current": current,
        "power": power,
        "energy": energy,
        "frequency": frequency,
        "pf": pf,
    }

    client.publish(TOPIC_ENERGY, json.dumps(payload))
    print(f"[PZEM] V:{voltage}V I:{current}A P:{power}W E:{energy}kWh F:{frequency}Hz PF:{pf}")


def handle_timer():
    global timer_active, relay_state

    if timer_active:
        elapsed = current_millis() - timer_start_millis
        if elapsed >= timer_duration:
            timer_active = False
            relay_state = False
            print("[TIMER] Timer done - Relay OFF")
            client.publish(TOPIC_TIMER_STATUS, "TIMER_DONE")


def handle_schedule():
    global relay_state, start_triggered, stop_triggered, last_triggered_day

    if not schedule_start_active and not schedule_stop_active:
        return

    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    current_day = now.day

    if not schedule_daily_mode and current_day != last_triggered_day:
        last_triggered_day = current_day
        start_triggered = False
        stop_triggered = False

    if schedule_start_active and current_hour == sched_start_hour and current_minute == sched_start_minute:
        if not start_triggered:
            start_triggered = True
            relay_state = True
            print("[SCHEDULE] Start triggered - Relay ON")
            send_relay_status()
            client.publish(TOPIC_SCHEDULE_STATUS, "START_TRIGGER")

    if schedule_stop_active and current_hour == sched_stop_hour and current_minute == sched_stop_minute:
        if not stop_triggered:
            stop_triggered = True
            relay_state = False
            print("[SCHEDULE] Stop triggered - Relay OFF")
            send_relay_status()
            client.publish(TOPIC_SCHEDULE_STATUS, "STOP_TRIGGER")

    if schedule_daily_mode:
        if not hasattr(handle_schedule, "last_checked_minute"):
            handle_schedule.last_checked_minute = -1

        if current_minute != handle_schedule.last_checked_minute:
            handle_schedule.last_checked_minute = current_minute

            if current_hour != sched_start_hour or current_minute != sched_start_minute:
                if start_triggered:
                    start_triggered = False
                    print("[SCHEDULE] Start trigger reset (daily mode)")

            if current_hour != sched_stop_hour or current_minute != sched_stop_minute:
                if stop_triggered:
                    stop_triggered = False
                    print("[SCHEDULE] Stop trigger reset (daily mode)")

    if not timer_active and schedule_start_active and schedule_stop_active:
        should_be_on = is_within_scheduled_on_window(now)
        if should_be_on and not relay_state:
            relay_state = True
            send_relay_status()
            publish_status_sync()
            print(
                f"[RECOVERY] Relay ON (within schedule range: "
                f"{sched_start_hour:02d}:{sched_start_minute:02d} - "
                f"{sched_stop_hour:02d}:{sched_stop_minute:02d})"
            )


def input_thread():
    global load_current, running

    print("\n" + "=" * 60)
    print("INPUT BEBAN (LOAD CURRENT)")
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

            if user_input.lower() == "q":
                print("\n[INFO] Keluar dari input thread...")
                break

            current_val = float(user_input)

            if current_val < 0:
                print("[ERROR] Nilai tidak boleh negatif!")
            elif current_val > 10:
                print("[WARNING] Nilai terlalu besar! Max 10A untuk safety.")
            else:
                load_current = current_val
                print(f"[INFO] Beban di-set ke: {load_current} A")
                print(f"[INFO] Saat Relay ON, power akan: V x {load_current}A x PF")

        except ValueError:
            print("[ERROR] Input tidak valid! Masukkan angka (contoh: 0.5)")
        except KeyboardInterrupt:
            print("\n[INFO] Input thread dihentikan...")
            break


def simulate_leds():
    status = []

    status.append("BLUE: MQTT OK" if mqtt_connected else "BLUE: MQTT OFF")

    if timer_active:
        status.append("GREEN: TIMER BLINK")
    elif relay_state:
        status.append("GREEN: RELAY ON")
    else:
        status.append("GREEN: RELAY OFF")

    status.append(f"BEBAN: {load_current}A" if relay_state else f"BEBAN: {load_current}A (standby)")

    if timer_active:
        elapsed = current_millis() - timer_start_millis
        remaining = max(0, timer_duration - elapsed)
        status.append(f"TIMER: {remaining // 1000}s")

    if schedule_start_active or schedule_stop_active:
        status.append("DAILY" if schedule_daily_mode else "ONETIME")
        if schedule_start_active:
            status.append(f"START: {sched_start_hour:02d}:{sched_start_minute:02d}")
        if schedule_stop_active:
            status.append(f"STOP: {sched_stop_hour:02d}:{sched_stop_minute:02d}")

    print(f"\r[STATUS] {' | '.join(status)}    ", end="", flush=True)


def show_load_info():
    print(f"\n{'=' * 60}")
    print("KONDISI SAAT INI")
    print(f"{'=' * 60}")
    print(f"Relay       : {'ON' if relay_state else 'OFF'}")
    print(f"Beban (Load): {load_current} A")
    print("\nEstimasi Power saat Relay ON:")
    if load_current > 0:
        estimated_power = base_voltage * load_current * 0.9
        print(f"  V x I x PF = {base_voltage}V x {load_current}A x 0.9")
        print(f"  ~= {estimated_power:.1f} Watt")
    else:
        print("  0 Watt (beban 0A)")
    print(f"{'=' * 60}\n")


def main():
    global client, running

    print("=" * 60)
    print("EcoLab Smart Socket Simulator")
    print("=" * 60)
    print("Features:")
    print("  - Relay Control (ON/OFF)")
    print("  - Timer Countdown")
    print("  - Schedule (Start/Stop) with Daily/Onetime mode")
    print("  - PZEM Energy Monitoring (FIRMWARE-LIKE MODE)")
    print("  - MQTT auto reconnect")
    print("  - Load Current Input (User Adjustable)")
    print("=" * 60)

    client = mqtt.Client(client_id="smartsocket2_simulator")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CA_CERT)
    client.tls_set_context(context)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.will_set(TOPIC_DEVICE_STATUS, "OFFLINE", qos=0, retain=True)

    print(f"\n[INFO] Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        load_schedule_from_file()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        last_energy_time = time.time()
        last_status_sync_time = time.time()
        last_debug_time = time.time()
        last_show_info_time = time.time()

        input_thread_handle = threading.Thread(target=input_thread, daemon=True)
        input_thread_handle.start()
        show_load_info()

        while True:
            try:
                current_time = time.time()

                ensure_mqtt_connection()

                if current_time - last_energy_time >= 2:
                    last_energy_time = current_time
                    if mqtt_connected:
                        send_energy_data()
                        print()

                if current_time - last_status_sync_time >= 2:
                    last_status_sync_time = current_time
                    if mqtt_connected:
                        publish_status_sync()

                if current_time - last_debug_time >= 10:
                    last_debug_time = current_time
                    now = datetime.now()
                    print(f"\n[RTC] {now.strftime('%Y-%m-%d %H:%M:%S')}")
                    if schedule_start_active or schedule_stop_active:
                        print(
                            f"[SCHEDULE] Start: {sched_start_hour:02d}:{sched_start_minute:02d} "
                            f"Stop: {sched_stop_hour:02d}:{sched_stop_minute:02d} "
                            f"Mode: {'Daily' if schedule_daily_mode else 'Onetime'}"
                        )

                if current_time - last_show_info_time >= 30:
                    last_show_info_time = current_time
                    show_load_info()

                handle_timer()
                handle_schedule()
                simulate_leds()
                time.sleep(0.1)

            except KeyboardInterrupt:
                print("\n\n[INFO] Shutting down...")
                running = False
                send_device_status("OFFLINE", retain=True)
                client.loop_stop()
                client.disconnect()
                break

    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")


if __name__ == "__main__":
    main()
