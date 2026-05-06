"""Backend MQTT untuk sensor DHT22 dari MCU A dan MCU B."""

import time


class DHT22MQTTBackend:
    """
    Backend MQTT untuk sensor DHT22.

    Class ini tidak membuat koneksi MQTT sendiri.
    Tugasnya hanya subscribe topic sensor, menyimpan state terbaru,
    lalu menyediakan data ringkas lewat `fetch()`.
    """

    TOPIC_TEMP_A = "ecolab/mcuA/dht/temperature"
    TOPIC_HUM_A = "ecolab/mcuA/dht/humidity"
    TOPIC_TEMP_B = "ecolab/mcuB/dht/temperature"
    TOPIC_HUM_B = "ecolab/mcuB/dht/humidity"

    TEMP_MIN = -10.0
    TEMP_MAX = 60.0
    HUM_MIN = 0.0
    HUM_MAX = 100.0

    DATA_EXPIRY = 10

    def __init__(self, mqtt_client):
        """Menyimpan MQTT core bersama dan state awal sensor DHT."""
        self.mqtt = mqtt_client

        # State sensor disimpan bersama timestamp terakhirnya.
        self.temp_A = None
        self.hum_A = None
        self.temp_B = None
        self.hum_B = None

        self.temp_A_time = None
        self.hum_A_time = None
        self.temp_B_time = None
        self.hum_B_time = None

    def start(self):
        """Mulai subscribe semua topic DHT22 lewat MQTT core."""
        self.mqtt.subscribe(self.TOPIC_TEMP_A, self._on_message)
        self.mqtt.subscribe(self.TOPIC_HUM_A, self._on_message)
        self.mqtt.subscribe(self.TOPIC_TEMP_B, self._on_message)
        self.mqtt.subscribe(self.TOPIC_HUM_B, self._on_message)

    def _on_message(self, client, userdata, msg):
        """Memproses payload sensor masuk lalu menyimpannya jika valid."""
        payload = msg.payload.decode()

        try:
            value = float(payload)
        except ValueError:
            return

        # Validasi range dan filter outlier.
        is_temp = "temperature" in msg.topic
        is_hum = "humidity" in msg.topic

        if is_temp and not (self.TEMP_MIN <= value <= self.TEMP_MAX):
            return
        if is_hum and not (self.HUM_MIN <= value <= self.HUM_MAX):
            return

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

    def fetch(self) -> dict:
        """
        Mengambil data DHT22 terbaru beserta rata-ratanya.

        Logika:
        - Kalau 2 MCU aktif -> pakai rata-rata
        - Kalau 1 MCU mati -> pakai yang aktif saja
        - Kalau semua mati -> None
        - Data expire setelah 10 detik
        """
        now = time.time()

        # Cek expiry dan return None jika data sudah kadaluarsa.
        def get_value(value, timestamp):
            if value is None or timestamp is None:
                return None
            if now - timestamp > self.DATA_EXPIRY:
                return None
            return value

        temp_A = get_value(self.temp_A, self.temp_A_time)
        hum_A = get_value(self.hum_A, self.hum_A_time)
        temp_B = get_value(self.temp_B, self.temp_B_time)
        hum_B = get_value(self.hum_B, self.hum_B_time)

        temps = [t for t in (temp_A, temp_B) if t is not None]
        hums = [h for h in (hum_A, hum_B) if h is not None]

        # Hitung rata-rata hanya dari data yang valid.
        avg_temp = sum(temps) / len(temps) if temps else None
        avg_hum = sum(hums) / len(hums) if hums else None

        # Tentukan source data untuk kebutuhan info popup/UI.
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
            "temp_source": "+".join(temp_source) if temp_source else None,
            "hum_source": "+".join(hum_source) if hum_source else None,
        }
