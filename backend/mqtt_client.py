import threading
import ssl
import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(
        self,
        broker="10.33.11.148",
        port=1883,
        username=None,
        password=None,
        ca_cert_path=None,
        use_tls=False,
        logger=None
    ):
        """
        MQTT Client with TLS support

        Args:
            broker: MQTT broker address
            port: MQTT port (1883 for plain, 8883 for TLS)
            username: MQTT username (optional)
            password: MQTT password (optional)
            ca_cert_path: Path to CA certificate (required for TLS)
            use_tls: Enable TLS encryption
            logger: Logger function for error messages
        """
        self.broker = broker
        self.port = port
        self.logger = logger
        self._subscriptions = []
        self._handlers = {}  # Handlers untuk routing messages

        # Create MQTT client
        self.client = mqtt.Client()

        # TLS Configuration
        if use_tls:
            if ca_cert_path is None:
                raise ValueError("ca_cert_path is required when use_tls=True")

            self.client.tls_set(
                ca_certs=ca_cert_path,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )

            # Set username/password for TLS
            if username and password:
                self.client.username_pw_set(username, password)

            self._log(f"[MQTT CORE] TLS enabled (port {port})")
        else:
            # Plain MQTT with optional auth
            if username and password:
                self.client.username_pw_set(username, password)
            self._log(f"[MQTT CORE] Plain MQTT (port {port})")

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _log(self, message):
        """Helper untuk logging"""
        if self.logger:
            self.logger(message)
        else:
            print(message)

    def start(self):
        """Start MQTT client in daemon thread"""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        """MQTT loop runner"""
        try:
            self._log(f"[MQTT CORE] Connecting to {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            error_msg = f"[MQTT ERROR] Connection failed: {e}"
            self._log(error_msg)

    def _on_connect(self, client, userdata, flags, rc):
        """Callback saat connect ke broker"""
        if rc == 0:
            self._log(f"[MQTT CORE] ✅ Connected to {self.broker}:{self.port}")

            # 🔥 DAFTARKAN ULANG SEMUA SUBSCRIBE
            for topic, callback in self._subscriptions:
                client.subscribe(topic)
                client.message_callback_add(topic, callback)
                self._log(f"[MQTT CORE] Subscribed to: {topic}")
        else:
            self._log(f"[MQTT CORE] ❌ Connection failed (rc={rc})")

    def subscribe(self, topic, callback):
        """
        Subscribe ke topic dengan callback

        Args:
            topic: MQTT topic (support wildcard +/#)
            callback: Function untuk handle message (client, userdata, msg)
        """
        # Simpan untuk resubscribe on reconnect
        self._subscriptions.append((topic, callback))

        # Kalau sudah connect, langsung subscribe
        if self.client.is_connected():
            self.client.subscribe(topic)
            self.client.message_callback_add(topic, callback)
            self._log(f"[MQTT CORE] Subscribed to: {topic}")

    def publish(self, topic, payload, retain=False):
        """
        Publish message ke topic

        Args:
            topic: MQTT topic
            payload: Message payload (string)
            retain: Retain message for new subscribers
        """
        try:
            self.client.publish(topic, payload, retain=retain)
        except Exception as e:
            self._log(f"[MQTT ERROR] Publish failed: {e}")

    def register_handler(self, name, handler):
        """
        Register message handler untuk routing pesan

        Args:
            name: Nama handler (untuk identifikasi)
            handler: Function dengan signature (topic, payload)
        """
        self._handlers[name] = handler
        self._log(f"[MQTT CORE] Registered handler: {name}")

    def _on_message(self, client, userdata, msg):
        """
        Global message callback - route ke semua handlers yang terdaftar
        """
        topic = msg.topic
        payload = msg.payload.decode()

        # Route ke semua handlers yang terdaftar
        for name, handler in self._handlers.items():
            try:
                handler(topic, payload)
            except Exception as e:
                self._log(f"[MQTT ERROR] Handler {name} failed: {e}")

