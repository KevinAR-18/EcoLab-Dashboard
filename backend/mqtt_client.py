"""Client MQTT dasar dengan dukungan TLS dan routing handler sederhana."""

import os
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
        log_mode_getter=None,
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
        self.username = username
        self.password = password
        self.ca_cert_path = ca_cert_path
        self.use_tls = use_tls
        self.logger = logger
        self.ca_file_exists = bool(ca_cert_path and os.path.exists(ca_cert_path))
        self.tls_config_loaded = False
        self.tls_config_error = None
        self.last_connect_rc = None
        self.last_connect_error = None
        self._subscriptions = []
        self._subscription_mids = {}
        self._handlers = {}  # Handler untuk routing message global

        # Buat object MQTT client dari library Paho.
        self.client = mqtt.Client()

        # Konfigurasi TLS jika memang diaktifkan.
        if use_tls:
            if ca_cert_path is None:
                raise ValueError("ca_cert_path is required when use_tls=True")

            try:
                self.client.tls_set(
                    ca_certs=ca_cert_path,
                    tls_version=ssl.PROTOCOL_TLSv1_2,
                )
                self.tls_config_loaded = True
            except Exception as exc:
                self.tls_config_error = exc

            # Pasang username/password juga saat memakai TLS.
            if username and password:
                self.client.username_pw_set(username, password)

            self._log(f"[MQTT CORE] TLS enabled (port {port})", level="normal")
        else:
            # Mode MQTT biasa tanpa TLS, auth tetap opsional.
            if username and password:
                self.client.username_pw_set(username, password)
            self._log(f"[MQTT CORE] Plain MQTT (port {port})", level="normal")

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe

    @staticmethod
    def _mask_secret(secret):
        """Menyamarkan secret agar tetap aman saat ditampilkan di log."""
        if not secret:
            return "not set"
        return "*" * max(8, len(secret))

    @staticmethod
    def _describe_rc(rc):
        """Menerjemahkan kode hasil koneksi MQTT agar mudah dibaca."""
        rc_map = {
            0: "Connection accepted",
            1: "Protocol version rejected by broker",
            2: "Client identifier rejected",
            3: "Broker service unavailable",
            4: "Username or password rejected",
            5: "Not authorized by broker",
        }
        return rc_map.get(rc, "Unknown connection result")

    @staticmethod
    def _describe_subscribe_result(result_code):
        """Menerjemahkan hasil request subscribe dari sisi client."""
        result_map = {
            mqtt.MQTT_ERR_SUCCESS: "request subscribe diterima client",
            mqtt.MQTT_ERR_NO_CONN: "client belum terhubung ke broker",
            mqtt.MQTT_ERR_QUEUE_SIZE: "antrian client MQTT penuh",
        }
        return result_map.get(result_code, f"error code {result_code}")

    def _emit_connection_profile_logs(self):
        """Menuliskan ringkasan profil koneksi untuk mode BAB IV."""
        self._log(
            f"[MQTT DEBUG] Inisialisasi koneksi ke broker {self.broker}:{self.port}",
            level="communication",
        )
        if self.use_tls:
            self._log(
                f"[MQTT DEBUG] TLS aktif, sertifikat CA: {self.ca_cert_path} "
                f"({'ditemukan' if self.ca_file_exists else 'tidak ditemukan'})",
                level="communication",
            )
            if self.ca_file_exists:
                self._log(
                    "[MQTT DEBUG] File CA ditemukan pada path konfigurasi",
                    level="communication",
                )
                if self.tls_config_loaded:
                    self._log(
                        "[MQTT DEBUG] Sertifikat CA berhasil dimuat ke konfigurasi TLS",
                        level="communication",
                    )
                else:
                    self._log(
                        "[MQTT DEBUG] Sertifikat CA ditemukan tetapi gagal dimuat ke konfigurasi TLS",
                        level="communication",
                    )
                    self._log(
                        f"[MQTT DEBUG] Penyebab konfigurasi TLS: {self.tls_config_error}",
                        level="communication",
                    )
            else:
                self._log(
                    "[MQTT DEBUG] File CA tidak ditemukan, koneksi TLS tidak dapat diverifikasi",
                    level="communication",
                )
        else:
            self._log(
                "[MQTT DEBUG] TLS tidak aktif, koneksi menggunakan MQTT biasa",
                level="communication",
            )

        if self.username:
            self._log(
                f"[MQTT DEBUG] Username terkonfigurasi: {self.username}",
                level="communication",
            )
        else:
            self._log("[MQTT DEBUG] Username MQTT belum diatur", level="communication")

        if self.password:
            self._log(
                f"[MQTT DEBUG] Password terkonfigurasi: {self._mask_secret(self.password)}",
                level="communication",
            )
        else:
            self._log("[MQTT DEBUG] Password MQTT belum diatur", level="communication")

        self._log(
            f"[MQTT TRACE] connect(host={self.broker}, port={self.port}, "
            f"tls={self.use_tls}, username={self.username or 'not set'})",
            level="detail",
        )
        if self.use_tls:
            self._log(
                f"[MQTT TRACE] tls_config_loaded={self.tls_config_loaded} "
                f"ca_exists={self.ca_file_exists} error={self.tls_config_error}",
                level="detail",
            )

    def emit_debug_snapshot(self):
        """Menuliskan snapshot status MQTT saat ini untuk mode debug."""
        self._emit_connection_profile_logs()
        if self.client.is_connected():
            auth_text = (
                "broker menerima autentikasi username/password"
                if self.username and self.password
                else "broker menerima koneksi tanpa kredensial tambahan"
            )
            tls_text = "TLS handshake berhasil" if self.use_tls else "TLS tidak digunakan"
            self._log(
                f"[MQTT DEBUG] Connected: koneksi MQTT aktif, "
                f"{auth_text}, {tls_text}",
                level="communication",
            )
            if self.use_tls:
                self._log(
                    "[MQTT DEBUG] TLS aktif dan handshake berhasil diselesaikan",
                    level="communication",
                )
        elif self.last_connect_error is not None:
            self._log(
                f"[MQTT DEBUG] Status koneksi terakhir: "
                f"{self._describe_connection_exception(self.last_connect_error)}",
                level="communication",
            )
        elif self.last_connect_rc not in (None, 0):
            self._log(
                f"[MQTT DEBUG] Status koneksi terakhir: {self._describe_rc(self.last_connect_rc)}",
                level="communication",
            )
        else:
            self._log(
                "[MQTT DEBUG] Status koneksi: menunggu atau belum ada konfirmasi broker",
                level="communication",
            )

        seen_topics = set()
        for topic, _callback in self._subscriptions:
            if topic in seen_topics:
                continue
            seen_topics.add(topic)
            self._log(
                f"[MQTT DEBUG] Topic subscribe terdaftar: {topic}",
                level="communication",
            )

    def _describe_connection_exception(self, exc):
        """Memberi penjelasan yang lebih mudah dibaca untuk error koneksi."""
        text = str(exc)
        lowered = text.lower()

        if isinstance(exc, ssl.SSLError):
            if "certificate verify failed" in lowered:
                return (
                    "Handshake TLS gagal: sertifikat CA tidak cocok dengan broker "
                    "atau rantai sertifikat broker tidak valid"
                )
            if "pem lib" in lowered or "no certificate" in lowered or "x509" in lowered:
                return "Konfigurasi TLS gagal: isi file sertifikat CA tidak valid"
            return f"Kesalahan SSL/TLS: {text}"

        if isinstance(exc, FileNotFoundError):
            return "Koneksi TLS gagal: file sertifikat CA tidak ditemukan"

        if "connection refused" in lowered:
            return "Koneksi ditolak broker atau port tidak menerima koneksi"
        if "timed out" in lowered:
            return "Koneksi ke broker timeout"
        if "name or service not known" in lowered or "getaddrinfo failed" in lowered:
            return "Hostname broker tidak dapat di-resolve"

        return text

    def _log(self, message, level="normal"):
        """Helper kecil untuk logging ke callback atau console."""
        if self.logger:
            self.logger(message, level=level)
        else:
            print(message)

    def start(self):
        """Menjalankan MQTT client di daemon thread terpisah."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        """Menjalankan loop koneksi dan event MQTT secara terus-menerus."""
        try:
            self._emit_connection_profile_logs()
            if self.use_tls and not self.tls_config_loaded:
                raise RuntimeError(
                    "TLS tidak dapat dimulai karena sertifikat CA gagal dimuat"
                )
            self._log(f"[MQTT CORE] Connecting to {self.broker}:{self.port}...", level="normal")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            self.last_connect_error = e
            self._log(
                f"[MQTT DEBUG] Koneksi gagal: {self._describe_connection_exception(e)}",
                level="communication",
            )
            self._log(
                f"[MQTT TRACE] Connection exception type: {type(e).__name__}",
                level="detail",
            )
            self._log(f"[MQTT ERROR] Connection failed: {e}", level="normal")

    def _on_connect(self, client, userdata, flags, rc):
        """Callback saat koneksi ke broker berhasil atau gagal."""
        self.last_connect_rc = rc
        self.last_connect_error = None
        if rc == 0:
            self._log(f"[MQTT CORE] Connected to {self.broker}:{self.port}", level="normal")
            auth_text = (
                "broker menerima autentikasi username/password"
                if self.username and self.password
                else "broker menerima koneksi tanpa kredensial tambahan"
            )
            tls_text = "TLS handshake berhasil" if self.use_tls else "TLS tidak digunakan"
            self._log(
                f"[MQTT DEBUG] Connected: koneksi MQTT berhasil dibuat, "
                f"{auth_text}, {tls_text}",
                level="communication",
            )
            if self.use_tls:
                self._log(
                    "[MQTT DEBUG] TLS aktif dan handshake berhasil diselesaikan",
                    level="communication",
                )
            self._log(f"[MQTT TRACE] on_connect rc={rc} flags={flags}", level="detail")

            # Daftarkan ulang semua subscription saat reconnect.
            for topic, callback in self._subscriptions:
                result, mid = client.subscribe(topic)
                client.message_callback_add(topic, callback)
                self._handle_subscribe_request(topic, result, mid, source="reconnect")
        else:
            reason = self._describe_rc(rc)
            self._log(f"[MQTT DEBUG] Koneksi gagal: {reason}", level="communication")
            self._log(
                f"[MQTT TRACE] on_connect rc={rc} reason={reason}",
                level="detail",
            )
            self._log(f"[MQTT CORE] Connection failed (rc={rc})", level="normal")

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
            result, mid = self.client.subscribe(topic)
            self.client.message_callback_add(topic, callback)
            self._handle_subscribe_request(topic, result, mid, source="immediate")

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
            self._log(
                f"[MQTT TRACE] tx topic={topic} payload={payload} retain={retain}",
                level="detail",
            )
        except Exception as e:
            self._log(f"[MQTT ERROR] Publish failed: {e}", level="normal")

    def register_handler(self, name, handler):
        """
        Mendaftarkan handler global untuk routing pesan masuk.

        Args:
            name: Nama handler untuk identifikasi
            handler: Function dengan signature `(topic, payload)`
        """
        self._handlers[name] = handler
        self._log(f"[MQTT CORE] Registered handler: {name}", level="normal")

    def _handle_subscribe_request(self, topic, result, mid, source="unknown"):
        """Mencatat hasil request subscribe sebelum ack broker diterima."""
        if result == mqtt.MQTT_ERR_SUCCESS:
            self._subscription_mids[mid] = topic
            self._log(f"[MQTT CORE] Subscribed to: {topic}", level="normal")
            self._log(
                f"[MQTT DEBUG] Request subscribe dikirim: {topic}",
                level="communication",
            )
            self._log(
                f"[MQTT TRACE] subscribe topic={topic} result={source} mid={mid}",
                level="detail",
            )
            return

        reason = self._describe_subscribe_result(result)
        self._log(
            f"[MQTT DEBUG] Gagal mengirim subscribe: {topic} ({reason})",
            level="communication",
        )
        self._log(
            f"[MQTT TRACE] subscribe topic={topic} result_error={result} source={source}",
            level="detail",
        )

    def _on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """Konfirmasi dari broker bahwa subscribe telah diproses."""
        topic = self._subscription_mids.pop(mid, f"<unknown mid {mid}>")
        qos_values = list(granted_qos or [])
        if any(qos == 128 for qos in qos_values):
            self._log(
                f"[MQTT DEBUG] Subscribe gagal dikonfirmasi broker: {topic}",
                level="communication",
            )
            self._log(
                f"[MQTT TRACE] on_subscribe mid={mid} topic={topic} granted_qos={qos_values}",
                level="detail",
            )
            return

        self._log(
            f"[MQTT DEBUG] Subscribe berhasil: {topic}",
            level="communication",
        )
        self._log(
            f"[MQTT TRACE] on_subscribe mid={mid} topic={topic} granted_qos={qos_values}",
            level="detail",
        )

    def _on_message(self, client, userdata, msg):
        """Meneruskan message masuk ke semua handler global yang terdaftar."""
        topic = msg.topic
        payload = msg.payload.decode()

        # Route ke semua handler global yang sudah didaftarkan.
        for name, handler in self._handlers.items():
            try:
                handler(topic, payload)
            except Exception as e:
                self._log(f"[MQTT ERROR] Handler {name} failed: {e}", level="normal")
