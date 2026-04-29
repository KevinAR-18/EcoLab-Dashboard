#!/usr/bin/env python3
"""
EcoLab Smart Socket Simulator (Python) - Socket 2
Menirukan ESP32 Smart Socket dengan PZEM + RTC + Timer + Schedule
"""

import json
import os
import random
import ssl
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt

MQTT_BROKER = "10.33.11.148"
MQTT_PORT = 8883
MQTT_USERNAME = "smartsocket2"
MQTT_PASSWORD = "smart2"
CA_CERT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "ca.crt")

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
TOPIC_DATETIME_STATUS = "ecolab/socket/2/datetime/status"

relay_state = False
manual_relay_state = False
client = None
mqtt_connected = False
last_mqtt_retry = 0.0
timer_active = False
timer_start_millis = 0
timer_duration = 0
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
    data = {
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
            json.dump(data, f, indent=2)
        print(f"[JSON] State saved to {SCHEDULE_FILE}")
    except Exception as exc:
        print(f"[JSON] Error saving state: {exc}")


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
            data = json.load(f)
        schedule_start_active = data.get("start_active", False)
        sched_start_hour = data.get("start_hour", 0)
        sched_start_minute = data.get("start_minute", 0)
        schedule_stop_active = data.get("stop_active", False)
        sched_stop_hour = data.get("stop_hour", 0)
        sched_stop_minute = data.get("stop_minute", 0)
        schedule_daily_mode = data.get("daily_mode", True)
        manual_relay_state = data.get("manual_relay_state", False)
    except Exception as exc:
        print(f"[JSON] Error loading state: {exc}")
    restore_relay_state()


def send_device_status(status, retain=True):
    if client is None:
        return
    client.publish(TOPIC_DEVICE_STATUS, status, retain=retain)


def send_relay_status():
    if client is None:
        return
    client.publish(TOPIC_RELAY_STATUS, "ON" if relay_state else "OFF", retain=True)


def publish_status_sync():
    send_relay_status()
    if timer_active:
        elapsed = current_millis() - timer_start_millis
        remaining = max(0, timer_duration - elapsed)
        client.publish(TOPIC_TIMER_STATUS, f"ACTIVE:{int(remaining / 1000)}s", retain=True)
    else:
        client.publish(TOPIC_TIMER_STATUS, "INACTIVE", retain=True)
    payload = {
        "start": f"{sched_start_hour:02d}:{sched_start_minute:02d}" if schedule_start_active else None,
        "stop": f"{sched_stop_hour:02d}:{sched_stop_minute:02d}" if schedule_stop_active else None,
        "mode": "daily" if schedule_daily_mode else "onetime",
    }
    client.publish(TOPIC_SCHEDULE_STATUS, json.dumps(payload), retain=True)
    now = datetime.now()
    client.publish(
        TOPIC_DATETIME_STATUS,
        f"OK:NTP_SYNCED:{now.strftime('%Y-%m-%d %H:%M:%S')} {now.isoweekday()}",
        retain=True,
    )


def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    mqtt_connected = rc == 0
    print(f"[MQTT] Connected with result code: {rc}")
    if not mqtt_connected:
        return
    for topic in (
        TOPIC_CONTROL,
        TOPIC_TIMER,
        TOPIC_SCHEDULE_START,
        TOPIC_SCHEDULE_STOP,
        TOPIC_SCHEDULE_MODE,
    ):
        client.subscribe(topic)
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

    if topic == TOPIC_CONTROL:
        if payload == "ON":
            relay_state = True
            manual_relay_state = True
            save_schedule_to_file()
            send_relay_status()
        elif payload == "OFF":
            relay_state = False
            manual_relay_state = False
            save_schedule_to_file()
            send_relay_status()
    elif topic == TOPIC_TIMER:
        try:
            duration = int(payload)
        except ValueError:
            duration = 0
        if duration == 0:
            timer_active = False
            client.publish(TOPIC_TIMER_STATUS, "INACTIVE", retain=True)
        else:
            timer_duration = duration * 1000
            timer_start_millis = current_millis()
            timer_active = True
            publish_status_sync()
    elif topic == TOPIC_SCHEDULE_START:
        if payload == "CLEAR":
            schedule_start_active = False
            start_triggered = False
            publish_status_sync()
            save_schedule_to_file()
        else:
            try:
                hh, mm = payload.split(":")
                sched_start_hour = int(hh)
                sched_start_minute = int(mm)
                schedule_start_active = True
                start_triggered = False
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
        else:
            try:
                hh, mm = payload.split(":")
                sched_stop_hour = int(hh)
                sched_stop_minute = int(mm)
                schedule_stop_active = True
                stop_triggered = False
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
        elif payload == "onetime":
            schedule_daily_mode = False
            last_triggered_day = None
            start_triggered = False
            stop_triggered = False
            publish_status_sync()
            save_schedule_to_file()
        else:
            client.publish(TOPIC_SCHEDULE_STATUS, "MODE ERROR")


def ensure_mqtt_connection():
    global last_mqtt_retry
    if mqtt_connected:
        return
    now = time.time()
    if now - last_mqtt_retry < 5:
        return
    last_mqtt_retry = now
    try:
        client.reconnect()
    except Exception as exc:
        print(f"[MQTT] Reconnect failed: {exc}")


def send_energy_data():
    global accumulated_energy
    if relay_state:
        voltage = round(base_voltage + random.uniform(-2, 2), 2)
        current = round(load_current + random.uniform(-0.01, 0.01), 3) if load_current > 0 else 0.0
        current = max(0, current)
        pf = round(random.uniform(0.85, 0.95), 2)
        power = round(voltage * current * pf, 2)
        frequency = round(base_frequency + random.uniform(-0.2, 0.2), 1)
        accumulated_energy += (power / 1000) * (2 / 3600)
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


def handle_timer():
    global timer_active, relay_state
    if timer_active and current_millis() - timer_start_millis >= timer_duration:
        timer_active = False
        relay_state = False
        send_relay_status()
        client.publish(TOPIC_TIMER_STATUS, "TIMER_DONE")
        publish_status_sync()


def handle_schedule():
    global relay_state, start_triggered, stop_triggered, last_triggered_day
    if not schedule_start_active and not schedule_stop_active:
        return
    now = datetime.now()
    if not schedule_daily_mode and now.day != last_triggered_day:
        last_triggered_day = now.day
        start_triggered = False
        stop_triggered = False
    if schedule_start_active and now.hour == sched_start_hour and now.minute == sched_start_minute and not start_triggered:
        start_triggered = True
        relay_state = True
        send_relay_status()
        client.publish(TOPIC_SCHEDULE_STATUS, "START_TRIGGER")
    if schedule_stop_active and now.hour == sched_stop_hour and now.minute == sched_stop_minute and not stop_triggered:
        stop_triggered = True
        relay_state = False
        send_relay_status()
        client.publish(TOPIC_SCHEDULE_STATUS, "STOP_TRIGGER")
    if schedule_daily_mode:
        if not hasattr(handle_schedule, "last_checked_minute"):
            handle_schedule.last_checked_minute = -1
        if now.minute != handle_schedule.last_checked_minute:
            handle_schedule.last_checked_minute = now.minute
            if (now.hour != sched_start_hour or now.minute != sched_start_minute) and start_triggered:
                start_triggered = False
            if (now.hour != sched_stop_hour or now.minute != sched_stop_minute) and stop_triggered:
                stop_triggered = False
    if not timer_active and schedule_start_active and schedule_stop_active and is_within_scheduled_on_window(now) and not relay_state:
        relay_state = True
        send_relay_status()
        publish_status_sync()


def input_thread():
    global load_current, running
    while running:
        try:
            user_input = input("\n>> Masukkan beban Socket 2 (A): ").strip()
            if user_input.lower() == "q":
                break
            current_val = float(user_input)
            if 0 <= current_val <= 10:
                load_current = current_val
        except Exception:
            pass


def simulate_leds():
    status = [f"MQTT: {'OK' if mqtt_connected else 'OFF'}", f"RELAY: {'ON' if relay_state else 'OFF'}"]
    print(f"\r[SOCKET 2] {' | '.join(status)}    ", end="", flush=True)


def main():
    global client, running
    client = mqtt.Client(client_id="smartsocket2_simulator")
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(CA_CERT)
    client.tls_set_context(context)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.will_set(TOPIC_DEVICE_STATUS, "OFFLINE", qos=0, retain=True)
    try:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        load_schedule_from_file()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        threading.Thread(target=input_thread, daemon=True).start()
        last_energy_time = time.time()
        last_status_sync_time = time.time()
        while True:
            try:
                now = time.time()
                ensure_mqtt_connection()
                if now - last_energy_time >= 2:
                    last_energy_time = now
                    if mqtt_connected:
                        send_energy_data()
                if now - last_status_sync_time >= 2:
                    last_status_sync_time = now
                    if mqtt_connected:
                        publish_status_sync()
                handle_timer()
                handle_schedule()
                simulate_leds()
                time.sleep(0.1)
            except KeyboardInterrupt:
                running = False
                send_device_status("OFFLINE", retain=True)
                client.loop_stop()
                client.disconnect()
                break
    except Exception as exc:
        print(f"[ERROR] Connection failed: {exc}")


if __name__ == "__main__":
    main()
