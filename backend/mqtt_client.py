"""Client MQTT dasar dengan dukungan TLS dan routing handler sederhana."""

import ssl
import threading

import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(
        self,
        broker="localhost",
        port=1883,
        username=None,
        password=None,
        ca_cert_path=None,
        use_tls=False,
        logger=None,
    ):
        """
        Menyiapkan MQTT client dengan dukungan TLS opsional.

        Args:
            broker: Alamat MQTT broker
            port: Port MQTT, misalnya 1883 atau 8883
            username: Username MQTT jika dipakai
            password: Password MQTT jika dipakai
            ca_cert_path: Path sertifikat CA untuk TLS
            use_tls: Menentukan apakah TLS diaktifkan
            logger: Fungsi logger opsional
        """
        self.broker = broker
        self.port = port
        self.logger = logger
        self._subscriptions = []
        self._handlers = {}  # Handler untuk routing message global

        # Buat object MQTT client dari library Paho.
        self.client = mqtt.Client()

        # Konfigurasi TLS jika memang diaktifkan.
        if use_tls:
            if ca_cert_path is None:
                raise ValueError("ca_cert_path is required when use_tls=True")

            self.client.tls_set(
                ca_certs=ca_cert_path,
                tls_version=ssl.PROTOCOL_TLSv1_2,
            )

            # Pasang username/password juga saat memakai TLS.
            if username and password:
                self.client.username_pw_set(username, password)

            self._log(f"[MQTT CORE] TLS enabled (port {port})")
        else:
            # Mode MQTT biasa tanpa TLS, auth tetap opsional.
            if username and password:
                self.client.username_pw_set(username, password)
            self._log(f"[MQTT CORE] Plain MQTT (port {port})")

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _log(self, message):
        """Helper kecil untuk logging ke callback atau console."""
        if self.logger:
            self.logger(message)
        else:
            print(message)

    def start(self):
        """Menjalankan MQTT client di daemon thread terpisah."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        """Menjalankan loop koneksi dan event MQTT secara terus-menerus."""
        try:
            self._log(f"[MQTT CORE] Connecting to {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            self._log(f"[MQTT ERROR] Connection failed: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        """Callback saat koneksi ke broker berhasil atau gagal."""
        if rc == 0:
            self._log(f"[MQTT CORE] Connected to {self.broker}:{self.port}")

            # Daftarkan ulang semua subscription saat reconnect.
            for topic, callback in self._subscriptions:
                client.subscribe(topic)
                client.message_callback_add(topic, callback)
                self._log(f"[MQTT CORE] Subscribed to: {topic}")
        else:
            self._log(f"[MQTT CORE] Connection failed (rc={rc})")

    def subscribe(self, topic, callback):
        """
        Subscribe ke topic tertentu dengan callback lokal.

        Args:
            topic: MQTT topic, termasuk wildcard jika perlu
            callback: Function handler dengan signature `(client, userdata, msg)`
        """
        # Simpan agar bisa otomatis subscribe ulang saat reconnect.
        self._subscriptions.append((topic, callback))

        # Jika client sudah connect, langsung subscribe sekarang juga.
        if self.client.is_connected():
            self.client.subscribe(topic)
            self.client.message_callback_add(topic, callback)
            self._log(f"[MQTT CORE] Subscribed to: {topic}")

    def publish(self, topic, payload, retain=False):
        """
        Publish message ke topic tertentu.

        Args:
            topic: MQTT topic tujuan
            payload: Isi message
            retain: Apakah retain flag diaktifkan
        """
        try:
            self.client.publish(topic, payload, retain=retain)
        except Exception as e:
            self._log(f"[MQTT ERROR] Publish failed: {e}")

    def register_handler(self, name, handler):
        """
        Mendaftarkan handler global untuk routing pesan masuk.

        Args:
            name: Nama handler untuk identifikasi
            handler: Function dengan signature `(topic, payload)`
        """
        self._handlers[name] = handler
        self._log(f"[MQTT CORE] Registered handler: {name}")

    def _on_message(self, client, userdata, msg):
        """Meneruskan message masuk ke semua handler global yang terdaftar."""
        topic = msg.topic
        payload = msg.payload.decode()

        # Route ke semua handler global yang sudah didaftarkan.
        for name, handler in self._handlers.items():
            try:
                handler(topic, payload)
            except Exception as e:
                self._log(f"[MQTT ERROR] Handler {name} failed: {e}")
