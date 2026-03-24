import threading
import time
import paho.mqtt.client as mqtt


class DHT22MQTTBackend:
    """
    Backend MQTT untuk sensor DHT22
    - Tidak tahu UI
    - Tidak membuat koneksi MQTT sendiri
    - Hanya subscribe & simpan state
    - Data diambil lewat fetch()
    - Data expire setelah 10 detik (MCU offline)
    """

    TOPIC_TEMP_A = "ecolab/mcuA/dht/temperature"
    TOPIC_HUM_A  = "ecolab/mcuA/dht/humidity"
    TOPIC_TEMP_B = "ecolab/mcuB/dht/temperature"
    TOPIC_HUM_B  = "ecolab/mcuB/dht/humidity"

    # Valid range untuk DHT22
    TEMP_MIN = -10.0  # °C
    TEMP_MAX = 60.0   # °C
    HUM_MIN = 0.0     # %
    HUM_MAX = 100.0   # %

    # Data expiry time (detik)
    DATA_EXPIRY = 10

    def __init__(self, mqtt_client):
        # MQTT core (shared)
        self.mqtt = mqtt_client

        # State sensor (value, timestamp)
        self.temp_A = None
        self.hum_A  = None
        self.temp_B = None
        self.hum_B  = None

        self.temp_A_time = None
        self.hum_A_time  = None
        self.temp_B_time = None
        self.hum_B_time  = None

    # ======================================
    def start(self):
        """
        Subscribe topic DHT22 lewat MQTT core
        """
        self.mqtt.subscribe(self.TOPIC_TEMP_A, self._on_message)
        self.mqtt.subscribe(self.TOPIC_HUM_A,  self._on_message)
        self.mqtt.subscribe(self.TOPIC_TEMP_B, self._on_message)
        self.mqtt.subscribe(self.TOPIC_HUM_B,  self._on_message)

    # ======================================
    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode()

        try:
            value = float(payload)
        except ValueError:
            return

        # Validasi range dan filter outlier
        is_temp = "temperature" in msg.topic
        is_hum = "humidity" in msg.topic

        # Skip jika nilai di luar range valid
        if is_temp and not (self.TEMP_MIN <= value <= self.TEMP_MAX):
            return  # Skip invalid temperature
        if is_hum and not (self.HUM_MIN <= value <= self.HUM_MAX):
            return  # Skip invalid humidity

        if msg.topic == self.TOPIC_TEMP_A:
            self.temp_A = value
            self.temp_A_time = time.time()

        elif msg.topic == self.TOPIC_HUM_A:
            self.hum_A = value
            self.hum_A_time = time.time()

        elif msg.topic == self.TOPIC_TEMP_B:
            self.temp_B = value
            self.temp_B_time = time.time()

        elif msg.topic == self.TOPIC_HUM_B:
            self.hum_B = value
            self.hum_B_time = time.time()

    # ======================================
    def fetch(self) -> dict:
        """
        Ambil data DHT22 terbaru + rata-rata
        Dipanggil bebas dari main (timer/UI)

        Logika:
        - Kalau 2 MCU aktif → Pakai rata-rata
        - Kalau 1 MCU mati → Pakai yang aktif saja
        - Kalau semua mati → None
        - Data expire setelah 10 detik (MCU offline)
        """
        now = time.time()

        # Cek expiry dan return None jika expired
        def get_value(value, timestamp):
            if value is None or timestamp is None:
                return None
            if now - timestamp > self.DATA_EXPIRY:
                return None  # Data expired (MCU offline)
            return value

        temp_A = get_value(self.temp_A, self.temp_A_time)
        hum_A = get_value(self.hum_A, self.hum_A_time)
        temp_B = get_value(self.temp_B, self.temp_B_time)
        hum_B = get_value(self.hum_B, self.hum_B_time)

        temps = [t for t in (temp_A, temp_B) if t is not None]
        hums  = [h for h in (hum_A, hum_B) if h is not None]

        # Hitung rata-rata (hanya dari data valid)
        avg_temp = sum(temps) / len(temps) if temps else None
        avg_hum  = sum(hums)  / len(hums)  if hums  else None

        # Tentukan source data untuk info
        temp_source = []
        if temp_A is not None:
            temp_source.append("A")
        if temp_B is not None:
            temp_source.append("B")

        hum_source = []
        if hum_A is not None:
            hum_source.append("A")
        if hum_B is not None:
            hum_source.append("B")

        return {
            "temp_A": temp_A,
            "hum_A": hum_A,
            "temp_B": temp_B,
            "hum_B": hum_B,
            "avg_temperature": avg_temp,
            "avg_humidity": avg_hum,
            "temp_source": "+".join(temp_source) if temp_source else None,  # "A", "B", atau "A+B"
            "hum_source": "+".join(hum_source) if hum_source else None,
        }
