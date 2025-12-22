import time
import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER

ACCESS_ID = "fgrgqphjjk94prgs7vsn"
ACCESS_KEY = "9dee5983d1a246628c4fa543b91ae34c"
API_ENDPOINT = "https://openapi-sg.iotbing.com"

DEVICE_IDS = [
    "a366ecc0ab15070f5dtf9x",  # Sensor 1
    "a398a1c762af33236bvfar"   # Sensor 2
]

# Enable debug log (optional)
TUYA_LOGGER.setLevel(logging.INFO)

# Init OpenAPI and connect
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

print("Monitoring suhu 2 sensor... Tekan Ctrl+C untuk berhenti.")

try:
    while True:
        current_time = time.strftime("%H:%M:%S")
        temps = []

        for device_id in DEVICE_IDS:
            response = openapi.get(f"/v1.0/iot-03/devices/{device_id}/status")
            status = response['result']

            # Ambil nilai suhu (va_temperature) dan scale
            temperature = next(item['value'] for item in status if item['code'] == 'va_temperature') / 10
            temps.append(temperature)

        # Tampilkan di terminal
        print(f"[{current_time}] Sensor 1: {temps[0]:.1f}°C | Sensor 2: {temps[1]:.1f}°C")

        time.sleep(5)  # tunggu 5 detik sebelum update lagi

except KeyboardInterrupt:
    print("\nMonitoring dihentikan.")
