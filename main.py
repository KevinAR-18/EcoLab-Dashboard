"""
Jendela dashboard utama untuk aplikasi desktop EcoLab.

Modul ini menyatukan UI hasil Qt Designer, widget kustom, backend MQTT,
layanan Growatt dan WeatherCloud, serta aksi user berbasis role
ke dalam satu jendela utama.
"""

import sys,random,os,time,hashlib
from datetime import datetime
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (
    QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QTimer, QUrl, Qt, QEvent, QStandardPaths, Signal
)


from PySide6.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
    QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient
)

from PySide6.QtWidgets import *

# Import UI hasil Qt Designer
from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_functions import UIFunctions

# Import Session Manager dan Auth Service untuk user features
from auth.session_manager import SessionManager
from auth.auth_service import FirebaseAuthService
from config.firebase_settings import get_env, get_env_bool, get_required_env
from config.path_utils import get_credentials_path, get_resource_path

# Import helper tema untuk message box yang konsisten dengan UI
from ui.ui_theme_helper import (
    show_styled_information,
    show_styled_warning,
    show_styled_critical,
    show_styled_question
)

from app.setup.lamp_setup import LampSetup
from app.setup.switch_setup import SwitchSetup
from app.setup.ac_setup import ACSetup
from app.setup.arrow_setup import ArrowSetup
from dialogs.smartsocket_popup import SmartSocketPopup
from app.setup.smartsocket_setup import SmartSocketSetup
from services.smartsocket_recorder import SmartSocketRecorder
from services.smartsocket_protection_store import SmartSocketProtectionStore
from services.smartsocket_settings_manager import SmartSocketSettingsManager

from widgets.lamp_button import LampButton
from backend.growatt_backend import GrowattBackend
from backend.weathercloud_backend import WeatherCloudBackend
from backend.mqtt_client import MqttClient
from backend.mqtt_dht22_backend import DHT22MQTTBackend
from backend.lampbutton_backend import LampButtonBackend
from backend.acbutton_backend import ACButtonBackend
from backend.growatt_worker import GrowattWorker
from backend.mcu_status_backend import MCUStatusBackend
from backend.smartsocket_backend import SmartSocketManager

# ============================================================
# KONFIGURASI MQTT TLS
# ============================================================
# Nilai ini dibaca saat modul di-import agar kesalahan konfigurasi runtime
# bisa terdeteksi lebih awal sebelum dashboard membuat object backend.
MQTT_BROKER = get_required_env("ECOLAB_MQTT_BROKER")
MQTT_PORT = int(get_env("ECOLAB_MQTT_PORT", "8883"))
MQTT_USERNAME = get_required_env("ECOLAB_MQTT_USERNAME")
MQTT_PASSWORD = get_required_env("ECOLAB_MQTT_PASSWORD")
MQTT_CA_CERT = get_env("ECOLAB_MQTT_CA_CERT", get_credentials_path("ca.crt"))
MQTT_USE_TLS = get_env_bool("ECOLAB_MQTT_USE_TLS", True)

# Helper sederhana untuk menampilkan jam dan tanggal realtime di header.
# Dipisah dari MainWindow agar tanggung jawab update waktu tetap kecil dan jelas.

class Date:
    def update_time(self, label: QLabel):
        """Memperbarui label jam dan tanggal pada header dashboard."""
        current_time = QDateTime.currentDateTime()

        time_text = current_time.toString("HH:mm")
        date_text = current_time.toString("dddd, dd MMMM yyyy")

        label.setText(QCoreApplication.translate("MainWindow", f"{time_text} - {date_text}", None))
        
# Kelas window utama dashboard
class MainWindow(QMainWindow):
    # Signal untuk notify launcher saat logout terjadi
    logout_signal = Signal()
    socket_recording_state_changed = Signal(int, bool)
    socket_warning_state_changed = Signal(int)

    # APP VERSION
    APP_VERSION = "v2.1.3"
    SOCKET_WARNING_ELEVATED_CURRENT = 6.0
    SOCKET_WARNING_HIGH_CURRENT = 6.5
    SOCKET_WARNING_CRITICAL_CURRENT = 7.0
    SOCKET_WARNING_ELEVATED_POPUP_INTERVAL_SECONDS = 60.0
    SOCKET_WARNING_HIGH_POPUP_INTERVAL_SECONDS = 30.0
    SOCKET_CRITICAL_RECHECK_DELAY_SECONDS = 15
    SOCKET_CRITICAL_AUTO_OFF_DELAY_SECONDS = 10
    SOCKET_CRITICAL_FIRST_RESPONSE_SECONDS = 15
    MQTT_LOG_MODE_NORMAL = "normal"
    MQTT_LOG_MODE_BAB4 = "communication"
    MQTT_LOG_MODE_TECHNICAL = "detail"

    def __init__(self, user_session=None):
        """
        Menginisialisasi seluruh jendela utama dashboard.

        Fungsi ini bertanggung jawab menyiapkan UI, backend data,
        koneksi MQTT, timer periodik, navigasi halaman, kontrol perangkat,
        dan fitur berbasis role user.
        """
        super().__init__()

        # Simpan sesi user dari launcher/login.
        # Nilai ini dipakai untuk menentukan role, nama user, dan akses fitur.
        self.user_session = user_session

        # Inisialisasi UI hasil generate Qt Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mqtt_log_mode = self.MQTT_LOG_MODE_NORMAL
        self.log_history = []
        self.max_log_history = 1000

        # Konfigurasi tampilan dasar window sebelum backend dijalankan.
        self.initUI()
        self.setup_logging_mode_ui()

        # Tampilkan versi aplikasi pada area footer.
        self.set_app_version(self.APP_VERSION)

        self.ui.logPlainEdit.setReadOnly(True)
        self._weather_initial_fetched = False

        # Bentuk komponen visual utama lebih dulu agar backend nanti tinggal
        # mengirim status dan UI sudah siap menerima update.
        LampSetup.setup(self.ui, self)
        ACSetup.setup(self.ui, self)
        ArrowSetup.setup(self.ui, self)

        # Siapkan semua tombol switch Smart Socket di dashboard.
        SwitchSetup.setup(self.ui, self)

        # Fitur pada halaman settings hanya diisi jika ada sesi user aktif.
        if self.user_session:
            self.setup_user_features()

        # Backend Growatt berjalan terpisah melalui worker agar fetch data
        # tidak membekukan UI utama.
        self.growatt = GrowattBackend()
        self.growatt_worker = None
        self._last_growatt_data = None
        self.start_growatt_worker()

        # Backend cuaca eksternal untuk page monitoring sensor luar ruangan.
        self.weather = WeatherCloudBackend("5476957392")

        # MQTT adalah jalur utama komunikasi ke perangkat IoT.
        # Semua backend device akan berbagi koneksi MQTT ini.
        self.mqtt = MqttClient(
            broker=MQTT_BROKER,
            port=MQTT_PORT,
            username=MQTT_USERNAME,
            password=MQTT_PASSWORD,
            ca_cert_path=MQTT_CA_CERT,
            use_tls=MQTT_USE_TLS,
            logger=self.log_mqtt,
            log_mode_getter=self.get_mqtt_log_mode,
        )
        self.mqtt.start()

        self.dht = DHT22MQTTBackend(self.mqtt)
        self.dht.start()

        # Backend kontrol lampu dan AC menerima status dari MQTT serta
        # mengirim command saat user menekan tombol di UI.
        self.lampbutton_backend = LampButtonBackend(self.mqtt, logger=self.log)
        self.lampbutton_backend.status_changed.connect(self._on_lamp_status_changed)
        self.acbutton_backend = ACButtonBackend(self.mqtt, logger=self.log)
        self.acbutton_backend.status_changed.connect(self._on_ac_status_changed)

        # Smart Socket paling kompleks karena selain baca/tulis MQTT, fitur ini
        # juga menyimpan state monitoring, recording, autosave, dan warning.
        self.smartsocket_manager = SmartSocketManager(self.mqtt, logger=self.log)
        self.smartsocket_manager.start()
        self.smartsocket_recorder = SmartSocketRecorder()
        self.smartsocket_settings_manager = SmartSocketSettingsManager()
        self.smartsocket_recorder.set_recovery_dir(
            os.path.join(
                os.path.dirname(str(self.smartsocket_settings_manager.settings_file)),
                "smartsocket_recovery",
            )
        )
        self.smartsocket_protection_store = SmartSocketProtectionStore()
        self.global_smartsocket_monitoring_settings = {}
        self.socket_graph_range_overrides = {}
        self.socket_power_off_protection = {}
        self.socket_protection_controls = {}

        # State warning disimpan per socket supaya popup warning tidak terus
        # muncul berulang tanpa kontrol, dan statusnya bisa di-acknowledge user.
        self.socket_load_warnings = {
            socket_number: {
                "active": False,
                "level": "normal",
                "message": "",
                "current": 0.0,
                "relay_on": False,
                "acknowledged": False,
                "last_popup_at": 0.0,
                "popup_open": False,
                "critical_stage": 0,
                "critical_recheck_pending": False,
                "critical_recheck_due_at": 0.0,
                "critical_second_popup_shown": False,
                "critical_deadline": 0.0,
                "auto_off_sent": False,
            }
            for socket_number in range(1, 6)
        }
        self.socket_critical_recheck_timers = {}
        self.socket_critical_auto_off_timers = {}
        self._last_mcu_status = {"mcuA": None, "mcuB": None}
        self._style_state_cache = {}
        self._socket_energy_label_cache = {
            socket_number: {}
            for socket_number in range(1, 6)
        }
        self._last_lamp_ui_states = {}
        self._last_ac_ui_state = None
        for socket_number in range(1, 6):
            recheck_timer = QTimer(self)
            recheck_timer.setSingleShot(True)
            recheck_timer.timeout.connect(
                lambda n=socket_number: self._recheck_socket_critical_load(n, force=True)
            )
            self.socket_critical_recheck_timers[socket_number] = recheck_timer

            auto_off_timer = QTimer(self)
            auto_off_timer.setSingleShot(True)
            auto_off_timer.timeout.connect(
                lambda n=socket_number: self._handle_socket_critical_timeout(n)
            )
            self.socket_critical_auto_off_timers[socket_number] = auto_off_timer
        self._load_smartsocket_monitoring_settings()
        self._restore_smartsocket_recovery()
        self._start_socket_daily_autosave_timer()

        # Simpan preferensi format timer per socket untuk tampilan popup/UI.
        self.socket_timer_formats = {}  # {socket_number: "hms" atau "seconds"}

        # Registrasi signal/slot Smart Socket lebih awal, lalu sinkronisasi
        # isi UI setelah MQTT punya sedikit waktu untuk menerima state awal.
        SmartSocketSetup.setup(self)
        QTimer.singleShot(500, self.sync_ui_from_mqtt)
        QTimer.singleShot(1500, self._sync_socket_states_from_backend)
        QTimer.singleShot(3000, self._sync_socket_states_from_backend)

        # Rapikan margin root layout agar window custom terlihat penuh.
        for w in [self.ui.styleSheet, self.ui.bgApp]:
            w.setContentsMargins(0, 0, 0, 0)
            if w.layout():
                w.layout().setContentsMargins(0, 0, 0, 0)
                w.layout().setSpacing(0)

        self.ui.contentTopBg.setContentsMargins(0, 0, 0, 0)

        # Window dibuat frameless agar mengikuti desain custom aplikasi.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Timer ini hanya untuk update jam pada header setiap 1 detik.
        self.date_helper = Date()
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            lambda: self.date_helper.update_time(self.ui.clockInfo)
        )
        self.timer.start(1000)

        # Helper UIFunctions menangani perilaku window custom seperti drag,
        # maximize/restore, dan animasi sidebar.
        self.ui_functions = UIFunctions(self)

        self.ui.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.ui.maximizeRestoreAppBtn.clicked.connect(
            self.ui_functions.toggle_max_restore
        )
        self.ui.closeAppBtn.clicked.connect(self.close)
        self.ui.btn_exit.clicked.connect(self.close)
    
        # AKTIFKAN DRAG PADA TITLE BAR
        self.ui.contentTopBg.mousePressEvent = self.ui_functions.mouse_press
        self.ui.contentTopBg.mouseMoveEvent = self.ui_functions.mouse_move
        self.ui.contentTopBg.mouseDoubleClickEvent = (
            self.ui_functions.mouse_double_click
        )

        # SEMENTARA: DRAG BG APP (seluruh background)
        # self.ui.bgApp.mousePressEvent = self.ui_functions.mouse_press
        # self.ui.bgApp.mouseMoveEvent = self.ui_functions.mouse_move
        # self.ui.bgApp.mouseDoubleClickEvent = self.ui_functions.mouse_double_click

        # TOMBOL UNTUK MEMBUKA/TUTUP SIDE MENU
        self.ui.toggleButton.clicked.connect(
            lambda: self.ui_functions.toggle_left_menu(self.ui.leftMenuBg)
        )

        # Navigasi antar halaman utama dashboard memakai stacked widget.
        self.ui.btn_growatt.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(
                self.ui.page1_growattMonitoring
            )
        )

        self.ui.btn_controlroom.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(
                self.ui.page2_controlRoom
            )
        )

        self.ui.btn_monitoringsensor.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(
                self.ui.page3_monitoringSensor
            )
        )

        self.ui.btn_smartsocket.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(
                self.ui.page4_smartsocket
            )
        )

        # Tiap tombol action socket membuka popup detail socket yang dipilih.
        self.ui.btn_action_socket1.clicked.connect(
            lambda: self.open_smartsocket_popup(1)
        )
        self.ui.btn_action_socket2.clicked.connect(
            lambda: self.open_smartsocket_popup(2)
        )
        self.ui.btn_action_socket3.clicked.connect(
            lambda: self.open_smartsocket_popup(3)
        )
        self.ui.btn_action_socket4.clicked.connect(
            lambda: self.open_smartsocket_popup(4)
        )
        self.ui.btn_action_socket5.clicked.connect(
            lambda: self.open_smartsocket_popup(5)
        )

        self.ui.btn_setting.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(
                self.ui.page5_settings
            )
        )

        self.ui.stackedWidget.setCurrentWidget(
            self.ui.page1_growattMonitoring
        )
        
        self.ac_buttons = [
            self.ac_button,
            self.ui.btn_temp_up,
            self.ui.btn_temp_down,
            self.ui.btn_cool_ac,
            self.ui.btn_fan_ac,
        ]
        
        # ===============================
        # Popup ini menampilkan rincian aliran daya Growatt saat judul diklik.
        # ===============================
        self.flowInfoPopup = QFrame(self, Qt.Popup)
        self.flowInfoPopup.setObjectName("flowInfoPopup")
        self.flowInfoPopup.setStyleSheet("""
        QFrame#flowInfoPopup {
            background: white;
            border-radius: 8px;
            padding: 10px;
        }
        """)

        layoutPopup = QVBoxLayout(self.flowInfoPopup)
        layoutPopup.setContentsMargins(10, 10, 10, 10)
        layoutPopup.setSpacing(6)
        
        self.lblFlowTitle = QLabel(
            "PV Off-grid Inverter：PV Charging+Loads Supporting"
        )
        self.lblFlowTitle.setStyleSheet(
            "font-weight: bold; font-size: 13px;"
        )
        self.lblFlowTitle.setAlignment(Qt.AlignLeft)
        self.lblFlowTitle.setContentsMargins(0, 0, 0, 6)
        self.lblFlowTitle.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #2c2c2c;"
        )
        layoutPopup.addWidget(self.lblFlowTitle)

        self.lblBattery = QLabel("Battery Voltage: -- V")
        self.lblPVVolt = QLabel("PV1/PV2 Voltage: -- / -- V")
        self.lblPVCurrent = QLabel("PV1/PV2 Recharging Current: -- / -- A")
        self.lblTotalCharge = QLabel("Total Charge Current: -- A")
        self.lblACIn = QLabel("AC Input Voltage/Frequency: -- V / -- Hz")
        self.lblACOut = QLabel("AC Output Voltage/Frequency: -- V / -- Hz")
        self.lblConsumption = QLabel("Consumption Power: -- W")
        self.lblLoad = QLabel("Load Percentage: -- %")

        for lbl in (
            self.lblBattery,
            self.lblPVVolt,
            self.lblPVCurrent,
            self.lblTotalCharge,
            self.lblACIn,
            self.lblACOut,
            self.lblConsumption,
            self.lblLoad,
        ):
            layoutPopup.addWidget(lbl)

        self.ui.titleFlow.mousePressEvent = self.show_flow_popup

        # ===============================
        # Popup ini menampilkan data sensor DHT yang lebih detail dibanding
        # ringkasan yang tampil di halaman monitoring.
        # ===============================
        self.dhtInfoPopup = QFrame(self, Qt.Popup)
        self.dhtInfoPopup.setObjectName("dhtInfoPopup")
        self.dhtInfoPopup.setStyleSheet("""
        QFrame#dhtInfoPopup {
            background: white;
            border-radius: 8px;
            padding: 10px;
        }
        """)

        layoutDHTPopup = QVBoxLayout(self.dhtInfoPopup)
        layoutDHTPopup.setContentsMargins(10, 10, 10, 10)
        layoutDHTPopup.setSpacing(6)

        self.lblDHTTitle = QLabel("Sensor DHT Status")
        self.lblDHTTitle.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #2c2c2c;"
        )
        self.lblDHTTitle.setAlignment(Qt.AlignLeft)
        layoutDHTPopup.addWidget(self.lblDHTTitle)

        # Labels untuk info sensor
        self.lblDHTSourceTemp = QLabel("Sumber Suhu: --")
        self.lblDHTSourceHum = QLabel("Sumber Kelembaban: --")
        self.lblDHTTempA = QLabel("MCU A Suhu: -- °C")
        self.lblDHTTempB = QLabel("MCU B Suhu: -- °C")
        self.lblDHTHumA = QLabel("MCU A Kelembaban: -- %")
        self.lblDHTHumB = QLabel("MCU B Kelembaban: -- %")
        self.lblDHTAvgTemp = QLabel("Rata-rata Suhu: -- °C")
        self.lblDHTAvgHum = QLabel("Rata-rata Kelembaban: -- %")

        for lbl in (
            self.lblDHTSourceTemp,
            self.lblDHTSourceHum,
            self.lblDHTTempA,
            self.lblDHTTempB,
            self.lblDHTHumA,
            self.lblDHTHumB,
            self.lblDHTAvgTemp,
            self.lblDHTAvgHum,
        ):
            lbl.setStyleSheet("font-size: 12px; color: #2c2c2c;")
            layoutDHTPopup.addWidget(lbl)

        # Pasang handler klik pada judul sensor indoor.
        self.ui.titleIndoor.mousePressEvent = self.show_dht_popup
       
        self.lampbutton_backend = LampButtonBackend(self.mqtt, logger=self.log)
        self.lampbutton_backend.status_changed.connect(self._on_lamp_status_changed)
        self.lampbutton_backend.start()
        
        self.acbutton_backend = ACButtonBackend(self.mqtt, logger=self.log)
        self.acbutton_backend.status_changed.connect(self._on_ac_status_changed)
        self.acbutton_backend.start()

        # AC CONTROL BUTTONS
        self.ui.btn_temp_up.clicked.connect(self.ac_temp_up)
        self.ui.btn_temp_down.clicked.connect(self.ac_temp_down)
        self.ui.btn_cool_ac.clicked.connect(self.ac_mode_cool)
        self.ui.btn_fan_ac.clicked.connect(self.ac_mode_fan)

        # Timer polling periodik untuk backend yang tidak mendorong data secara
        # realtime sendiri. Interval berbeda sesuai karakter tiap sumber data.
        # TIMERS: GROWATT
        self.timerGrowatt = QTimer(self)
        self.timerGrowatt.timeout.connect(self.start_growatt_worker)
        self.timerGrowatt.start(15000)  # 15 detik

        # TIMERS: WEATHER CLOUD
        self.timerWeathercloud = QTimer(self)
        self.timerWeathercloud.timeout.connect(self.update_dataWeathercloud)
        self.timerWeathercloud.start(5000)  # 5 detik

        # TIMERS: DHT MQTT
        self.timerDhtmqtt = QTimer(self)
        self.timerDhtmqtt.timeout.connect(self.update_dht_ui)
        self.timerDhtmqtt.start(1000)  # 1 detik

        # Status MCU dipakai untuk menentukan perangkat kontrol boleh ditekan
        # atau tidak, terutama saat device offline.
        self.mcu_status = MCUStatusBackend(self.mqtt)
        self.mcu_status.start()

        self.timerMCUStatus = QTimer(self)
        self.timerMCUStatus.timeout.connect(self.update_mcu_status_ui)
        self.timerMCUStatus.start(1000)  # 1 detik
        
        self.timerLampState = QTimer(self)
        self.timerLampState.timeout.connect(self.update_lamp_ui_from_state)
        self.timerLampState.start(700)
        
        self.timerACState = QTimer(self)
        self.timerACState.timeout.connect(self.update_ac_ui_from_state)
        self.timerACState.start(700)

        if hasattr(self.ui, "logPlainEdit"):
            self.ui.logPlainEdit.document().setMaximumBlockCount(500)

        # Tampilkan window setelah seluruh komponen utama siap.
        self.show()
        
    def show_flow_popup(self, event):
        """Menampilkan popup detail aliran daya Growatt di bawah judul flow."""
        # posisikan popup di bawah titleFlow
        pos = self.ui.titleFlow.mapToGlobal(
            self.ui.titleFlow.rect().bottomLeft()
        )
        self.flowInfoPopup.move(pos)
        self.flowInfoPopup.show()

    def show_dht_popup(self, event):
        """Menampilkan popup detail sensor DHT di bawah judul indoor."""
        pos = self.ui.titleIndoor.mapToGlobal(
            self.ui.titleIndoor.rect().bottomLeft()
        )
        self.dhtInfoPopup.move(pos)
        self.dhtInfoPopup.show()

    def update_dht_popup(self, data):
        """Memperbarui isi popup DHT menggunakan data sensor terbaru."""
        # Formatter kecil agar nilai None tidak langsung tampil sebagai teks
        # Python, tetapi diganti placeholder yang lebih ramah dibaca.
        def fmt(val, unit=""):
            """Memformat nilai popup DHT dan mengganti None menjadi placeholder."""
            if val is None:
                return "--"
            return f"{val}{unit}"

        # Perbarui informasi sumber data suhu dan kelembaban.
        temp_source = data.get("temp_source", "--")
        hum_source = data.get("hum_source", "--")

        self.lblDHTSourceTemp.setText(f"Sumber Suhu: {fmt(temp_source)}")
        self.lblDHTSourceHum.setText(f"Sumber Kelembaban: {fmt(hum_source)}")

        # Perbarui data sensor dari MCU A.
        self.lblDHTTempA.setText(f"MCU A Suhu: {fmt(data.get('temp_A'), ' °C')}")
        self.lblDHTHumA.setText(f"MCU A Kelembaban: {fmt(data.get('hum_A'), ' %')}")

        # Perbarui data sensor dari MCU B.
        self.lblDHTTempB.setText(f"MCU B Suhu: {fmt(data.get('temp_B'), ' °C')}")
        self.lblDHTHumB.setText(f"MCU B Kelembaban: {fmt(data.get('hum_B'), ' %')}")

        # Perbarui nilai rata-rata gabungan.
        avg_temp = data.get("avg_temperature")
        avg_hum = data.get("avg_humidity")
        self.lblDHTAvgTemp.setText(f"Rata-rata Suhu: {fmt(avg_temp, ' °C')}")
        self.lblDHTAvgHum.setText(f"Rata-rata Kelembaban: {fmt(avg_hum, ' %')}")


    def update_flow_popup(self, flow):
        """Memperbarui isi popup flow Growatt berdasarkan data terbaru."""
        if not flow:
            return

        # Formatter dipisah agar string label tetap konsisten dan mudah dibaca.
        def fmt(val, unit="", dec=1):
            """Memformat angka desimal untuk popup flow Growatt."""
            if val is None:
                return "--"
            return f"{val:.{dec}f}{unit}"

        def fmt_int(val, unit=""):
            """Memformat angka bilangan bulat untuk popup flow Growatt."""
            if val is None:
                return "--"
            return f"{int(val)}{unit}"

        # 🔋 Battery
        self.lblBattery.setText(
            f"Battery Voltage: {fmt(flow.get('battery_voltage'), ' V')}"
        )

        # ☀️ PV Voltage
        self.lblPVVolt.setText(
            f"PV1/PV2 Voltage: "
            f"{fmt(flow.get('pv1_voltage'))} / {fmt(flow.get('pv2_voltage'), ' V')}"
        )

        # ☀️ PV Charging Current
        self.lblPVCurrent.setText(
            f"PV1/PV2 Recharging Current: "
            f"{fmt(flow.get('pv1_charge_current'))} / {fmt(flow.get('pv2_charge_current'), ' A')}"
        )

        # 🔌 Total Charge
        self.lblTotalCharge.setText(
            f"Total Charge Current: {fmt(flow.get('total_charge_current'), 'A')}"
        )

        # ⚡ AC Input
        self.lblACIn.setText(
            f"AC Input Voltage/Frequency: "
            f"{fmt(flow.get('ac_input_voltage'))} / {fmt(flow.get('ac_input_frequency'), ' Hz')}"
        )

        # ⚡ AC Output
        self.lblACOut.setText(
            f"AC Output Voltage/Frequency: "
            f"{fmt(flow.get('ac_output_voltage'))} / {fmt(flow.get('ac_output_frequency'), ' Hz')}"
        )

        # 🏠 Consumption
        self.lblConsumption.setText(
            f"Consumption Power: {fmt_int(flow.get('consumption_power'), 'W')}/ {fmt_int(flow.get('rateVA'), 'VA')}"
        )

        # 📊 Load
        self.lblLoad.setText(
            f"Load Percentage: {fmt(flow.get('load_percentage'), '%')}"
        )


    def _format_energy_value(self, value):
        """
        Format energy value ke kWh atau mWh

        Args:
            value: Nilai energy dalam kWh

        Returns:
            tuple: (nilai_string, satuan_string)
                   Contoh: ("150.50", "kWh") atau ("1.50", "mWh")
        """
        if value is None:
            return "--", "kWh"

        try:
            val = float(value)

            # Jika >= 1000 kWh, tampilkan dalam mWh
            if val >= 1000:
                mwh = val / 1000
                return f"{mwh:.2f}", "mWh"
            else:
                return f"{val:.2f}", "kWh"

        except (ValueError, TypeError):
            return "--", "kWh"

    def update_growatt_ui(self, data: dict):
        """Mengisi komponen UI Growatt dengan data inverter terbaru."""
        if not data:
            return

        # Hindari redraw UI jika payload identik dengan data terakhir.
        if data == self._last_growatt_data:
            return
        
        self.ui.currentpvpower_value.setText(f"PV Power: {data['pv_power']}W")
        self.ui.currentimportgrid_value.setText(f"{data['grid_import_power']}W")
        self.ui.currentconsumppower_value.setText(f"{data['load_power']}W//{data['rateVA_power']}VA")
        self.ui.currentsocbat_value.setText(f"SoC Battery：{data['soc']}%")

        # Nilai harian tetap ditampilkan langsung dalam kWh.
        self.ui.pvtoday_value.setText(f"{data['pv_today']}")
        self.ui.loadtoday_value.setText(f"{data['load_today']}")

        # Nilai total bisa membesar, jadi format satuan disesuaikan otomatis
        # antara kWh dan mWh agar tampilan lebih enak dibaca.
        # PV Total
        pv_total_val, pv_total_unit = self._format_energy_value(data['pv_total'])
        self.ui.pvtotal_value.setText(pv_total_val)
        if hasattr(self.ui, 'labelkwh2'):
            self.ui.labelkwh2.setText(pv_total_unit)

        # Total konsumsi beban
        load_total_val, load_total_unit = self._format_energy_value(data['load_total'])
        self.ui.loadtotal_value.setText(load_total_val)
        if hasattr(self.ui, 'labelkwh4'):
            self.ui.labelkwh4.setText(load_total_unit)

        # Battery Charge Total
        charge_total_val, charge_total_unit = self._format_energy_value(data['battery_charge_total'])
        self.ui.chargingtotal_value.setText(charge_total_val)
        if hasattr(self.ui, 'labelkwh6'):
            self.ui.labelkwh6.setText(charge_total_unit)

        # Battery Discharge Total
        discharge_total_val, discharge_total_unit = self._format_energy_value(data['battery_discharge_total'])
        self.ui.dischargingtotal_value.setText(discharge_total_val)
        if hasattr(self.ui, 'labelkwh8'):
            self.ui.labelkwh8.setText(discharge_total_unit)

        # Grid Total
        grid_total_val, grid_total_unit = self._format_energy_value(data['grid_total'])
        self.ui.imporgridttotal_value.setText(grid_total_val)
        if hasattr(self.ui, 'labelkwh10'):
            self.ui.labelkwh10.setText(grid_total_unit)

        # TODAY VALUES (dengan safe energy check)
        charge_today = self._safe_energy_value(data.get("battery_charge_today"))
        grid_today = self._safe_energy_value(data.get("grid_today"))

        self.ui.chargingtoday_value.setText(f"{charge_today}")
        self.ui.imporgridttoday_value.setText(f"{grid_today}")

        pbat = data["battery_power"]

        if pbat < 0:
            self.ui.currentdischpower_value.setText(f"Charging Power : {abs(pbat)} W")
            self.arrows["soc_dynamic"].set_direction("down")
            self.arrows["soc_dynamic"].set_active(True)
        else:
            self.ui.currentdischpower_value.setText(f"Discharging Power : {pbat} W")
            self.arrows["soc_dynamic"].set_direction("up")
            self.arrows["soc_dynamic"].set_active(True)

                        
        # Arah panah dipakai sebagai indikator visual apakah jalur energi aktif.
        self.arrows["pv"].set_active(data["pv_power"] > 0)
        self.arrows["grid"].set_active(data["grid_import_power"] > 0)
        self.arrows["load"].set_active(data["load_power"] > 0)
        
        self.log("[Growatt] Data updated")
        
        self.update_flow_popup(data.get("flow_info"))


    @staticmethod
    def deg_to_compass(deg: float) -> str:
        """Mengubah derajat arah angin menjadi nama arah mata angin."""
        directions = [
            "North",
            "North East",
            "East",
            "South East",
            "South",
            "South West",
            "West",
            "North West",
        ]
        return directions[round(deg / 45) % 8]

    def update_dataWeathercloud(self):
        """Mengambil data WeatherCloud lalu memperbarui UI cuaca luar ruangan."""
        # Fetch pertama tetap dijalankan agar halaman sensor punya data awal.
        # Setelah itu, update dibatasi hanya saat halaman sensor sedang aktif.
        if not self._weather_initial_fetched:
            pass
        else:
            # Skip kalau halaman WeatherCloud tidak aktif
            if self.ui.stackedWidget.currentWidget() != self.ui.page3_monitoringSensor:
                return
    
        try:
            data = self.weather.fetch()
            
            
            # tandai initial fetch sudah dilakukan
            self._weather_initial_fetched = True
        
            self.ui.tempW_value.setText(f"{data['temperature']} °C")
            self.ui.humidW_value.setText(f"{data['humidity']} %")
            self.ui.pressureW_value.setText(f"{data['pressure']} hPa")
            self.ui.windspdW_value.setText(f"{data['wind_speed']} m/s")
            self.ui.windspdavgW_value.setText(f"{data['wind_speed_avg']} m/s")
            self.ui.windspddirW_value.setText(
                f"{data['wind_direction']}° / {MainWindow.deg_to_compass(data['wind_direction'])}"
            )
            self.ui.totalrainW_value.setText(f"{data['rain_total']} mm")
            self.ui.rainrateW_value.setText(f"{data['rain_rate']} mm/h")
            self.ui.heatindexW_value.setText(f"{data['heat_index']} °C")
            
            temp_outdoor = data.get("temperature")
            
            self.update_temp_style(
                temp_outdoor,
                self.ui.frameTempWeather,
                self.ui.titletempW
            )
            
            heat_index = data.get("heat_index")

            self.update_heatindex_style(
                heat_index,
                self.ui.frameHeatindexWeather,
                self.ui.titleheatindexW
            )
            
            humid_outdoor = data.get("humidity")

            self.update_humidity_style(
                humid_outdoor,
                self.ui.frameHumidWeather,
                self.ui.titlehumidw
            )


        except Exception as e:
            print("dataWeather Cloud:", e)
            self.log("dataWeather Cloud:", e)
            
    def update_dht_ui(self):
        """Memperbarui ringkasan suhu dan kelembaban indoor dari backend DHT."""
        # Data DHT berasal dari backend MQTT yang menggabungkan pembacaan MCU A
        # dan MCU B, lalu menghitung nilai rata-rata yang dipakai dashboard.
        data = self.dht.fetch()

        avg_temp = data.get("avg_temperature")
        avg_hum = data.get("avg_humidity")

        # Jangan ubah UI sebelum ada data nyata dari MQTT.
        if not hasattr(self, "_dht_initialized"):
            if avg_temp is not None or avg_hum is not None:
                self._dht_initialized = True
                self.log("[DHT] Data pertama diterima dari MQTT")
            else:
                return
        # ===============================

        # Perbarui tampilan suhu indoor.
        if avg_temp is not None:
            if avg_temp != getattr(self, "_last_dht_temp", None):
                self.ui.tempIndoor_value.setText(f"{avg_temp:.1f} °C")
                self._last_dht_temp = avg_temp

        # Perbarui tampilan kelembaban indoor.
        if avg_hum is not None:
            if avg_hum != getattr(self, "_last_dht_hum", None):
                self.ui.humidIndoor_value.setText(f"{avg_hum:.1f} %")
                self._last_dht_hum = avg_hum

        if self.ui.stackedWidget.currentWidget() != self.ui.page3_monitoringSensor:
            return
                   
        if avg_temp is not None:
            if not hasattr(self, "_last_dht_log"):
                self._last_dht_log = 0

            now = QDateTime.currentSecsSinceEpoch()
            if now - self._last_dht_log >= 30:  # log tiap 30 detik
                self.log(f"[DHT] Avg Temp: {avg_temp:.1f} °C")
                self._last_dht_log = now
                
        self.update_temp_style(
            avg_temp,
            self.ui.frameTempIndoor,
            self.ui.titleSuhuIndoor
        )

        self.update_humidity_style(
            avg_hum,
            self.ui.frameHumidIndoor,
            self.ui.titleHumidIndoor
        )

        # Perbarui isi popup detail DHT.
        self.update_dht_popup(data)


    def publish_lamp(self, lamp_index: int, state: bool):
        """Mengirim perintah ON atau OFF ke lampu melalui backend MQTT."""
        # self.lampbutton_backend.set_lamp(lamp_index, state)
        self.lampbutton_backend.publish(lamp_index, state)
        self.log(f"Lamp {lamp_index}: {state}")

    # ===============================
    # PERINTAH PERANGKAT & LOGGING
    # ===============================
    def publish_ac_power(self, state: bool):
        """Mengirim perintah daya utama AC melalui backend MQTT."""
        self.acbutton_backend.power(state)
        print(f"AC Power: {state}")
        self.log(f"AC Power: {state}")

    def on_switch_toggled(self, switch_index: int, state: bool):
        """Menangani klik switch Smart Socket lalu meneruskan ke backend."""
        self.log(f"Switch {switch_index}: {'ON' if state else 'OFF'}")

        blocked_reason = self.get_socket_manual_control_block_reason(switch_index)
        if blocked_reason:
            backend = getattr(self, "socket_backends", {}).get(switch_index)
            previous_state = getattr(backend, "relay_state", None)
            if previous_state is None:
                previous_state = not state
            self._revert_socket_switch_state(switch_index, bool(previous_state))
            self.log(f"[Socket {switch_index}] Manual control cancelled: {blocked_reason}")
            QMessageBox.warning(
                self,
                "Kontrol Smart Socket Ditolak",
                blocked_reason,
            )
            return

        if not state:
            allowed, reason = self._authorize_socket_power_off(switch_index)
            if not allowed:
                self._revert_socket_switch_state(switch_index, True)
                if reason:
                    self.log(f"[Socket {switch_index}] OFF cancelled: {reason}")
                return

        # Guard ini penting karena user bisa menekan tombol sebelum backend
        # Smart Socket selesai terpasang atau sebelum MQTT siap.
        if hasattr(self, 'socket_backends'):
            pass

        # Jika backend siap, kirim perintah relay ke device yang sesuai.
        if hasattr(self, 'socket_backends') and switch_index in self.socket_backends:
            backend = self.socket_backends[switch_index]
            backend.set_relay(state)
            self.log(f"[Socket {switch_index}] Relay command sent: {state}")
        else:
            self.log(f"[WARNING] Socket {switch_index} backend not ready yet!")
            # Jika belum siap, tampilkan pesan yang menjelaskan kemungkinan
            # penyebab agar user tidak bingung kenapa tombol belum bekerja.
            show_styled_warning(
                self,
                "Smart Socket Not Ready",
                f"⚠️ Smart Socket {switch_index} backend belum siap.\n\n"
                f"MQTT mungkin sedang menghubungkan...\n"
                f"Tunggu 2-3 detik setelah aplikasi terbuka, lalu coba lagi.\n\n"
                f"Pastikan:\n"
                f"• MQTT Broker (Mosquitto) sudah jalan\n"
                f"• Simulator smartsocket_simulator.py sudah berjalan"
            )

    def _revert_socket_switch_state(self, switch_index: int, state: bool):
        """Mengembalikan state visual switch tanpa memicu command baru."""
        if not (1 <= switch_index <= len(getattr(self, "switches", []))):
            return

        switch = self.switches[switch_index - 1]

        def _apply():
            switch.blockSignals(True)
            switch.setOn(state)
            switch.blockSignals(False)
            switch.update()

        QTimer.singleShot(0, _apply)

    def _current_user_role(self):
        """Mengambil role user aktif dengan fallback aman."""
        if not self.user_session:
            return "user"
        return (self.user_session.get("role") or "user").strip().lower()

    def is_admin_user(self):
        """Mengecek apakah session aktif adalah admin."""
        return self._current_user_role() == "admin"

    def is_socket_timer_active(self, socket_number: int) -> bool:
        """Mengecek apakah timer socket sedang berjalan berdasarkan status MQTT."""
        backend = getattr(self, "socket_backends", {}).get(socket_number)
        timer_status = str(getattr(backend, "timer_status", "") or "").strip().upper()
        return timer_status.startswith("ACTIVE:")

    def is_socket_schedule_active(self, socket_number: int) -> bool:
        """Mengecek apakah socket masih memiliki schedule aktif."""
        backend = getattr(self, "socket_backends", {}).get(socket_number)
        return self._socket_has_active_schedule(backend)

    def get_socket_manual_control_block_reason(self, socket_number: int) -> str:
        """Membatasi kontrol manual user ketika timer atau schedule sedang aktif."""
        if self._current_user_role() != "user":
            return ""

        if self.is_socket_schedule_active(socket_number):
            return (
                f"Smart Socket {socket_number} tidak dapat dikontrol secara manual "
                "karena schedule sedang aktif. Hapus schedule terlebih dahulu."
            )

        if self.is_socket_timer_active(socket_number):
            return (
                f"Smart Socket {socket_number} tidak dapat dikontrol secara manual "
                "karena timer sedang berjalan. Batalkan timer terlebih dahulu."
            )

        return ""

    def _hash_socket_protection_password(self, password: str):
        """Membuat hash password proteksi socket."""
        password = (password or "").strip()
        if not password:
            return ""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def get_socket_power_off_protection(self, socket_number: int):
        """Mengambil konfigurasi proteksi OFF socket dari cache lokal."""
        default = {
            "enabled": False,
            "mode": "blocked",
            "password_hash": "",
            "note": "",
        }
        state = getattr(self, "socket_power_off_protection", {}).get(socket_number)
        if not isinstance(state, dict):
            return dict(default)

        payload = dict(default)
        payload.update(state)
        payload["enabled"] = bool(payload.get("enabled", False))
        payload["mode"] = (payload.get("mode") or "blocked").strip().lower()
        payload["password_hash"] = payload.get("password_hash", "") or ""
        payload["note"] = payload.get("note", "") or ""
        return payload

    def reload_socket_power_off_protection(self):
        """Menyegarkan cache proteksi Smart Socket dari Firebase."""
        defaults = {
            socket_number: {
                "enabled": False,
                "mode": "blocked",
                "password_hash": "",
                "note": "",
            }
            for socket_number in range(1, 6)
        }

        try:
            remote = self.smartsocket_protection_store.get_all()
        except Exception as exc:
            self.log(f"[SmartSocket Protection] Failed to load from Firebase: {exc}")
            if not getattr(self, "socket_power_off_protection", None):
                self.socket_power_off_protection = dict(defaults)
            return False

        defaults.update(remote)
        self.socket_power_off_protection = defaults
        return True

    def reload_one_socket_power_off_protection(self, socket_number: int):
        """Menyegarkan satu proteksi Smart Socket langsung dari Firebase."""
        try:
            protection = self.smartsocket_protection_store.get_one(socket_number)
        except Exception as exc:
            self.log(
                f"[SmartSocket Protection] Failed to load socket {socket_number} from Firebase: {exc}"
            )
            return False, self.get_socket_power_off_protection(socket_number)

        self.socket_power_off_protection[socket_number] = dict(protection)
        return True, dict(protection)

    def set_socket_power_off_protection(
        self,
        socket_number: int,
        enabled: bool,
        mode: str,
        password_hash=None,
        note: str = "",
    ):
        """Menyimpan proteksi OFF socket ke cache dan file settings."""
        current = self.get_socket_power_off_protection(socket_number)
        updated = {
            "enabled": bool(enabled),
            "mode": (mode or "blocked").strip().lower(),
            "password_hash": current.get("password_hash", ""),
            "note": (note or "").strip(),
        }
        if password_hash is not None:
            updated["password_hash"] = password_hash or ""
        saved = self.smartsocket_protection_store.set_one(socket_number, updated)
        self.socket_power_off_protection[socket_number] = dict(saved)
        return dict(saved)

    def _socket_protection_message(self, socket_number: int, protection: dict):
        """Menyusun isi pesan proteksi OFF socket."""
        note = (protection.get("note", "") or "").strip()
        lines = [f"Smart Socket {socket_number} diproteksi untuk aksi OFF."]
        if note:
            lines.extend(["", f"Reason: {note}"])
        return "\n".join(lines)

    def _prompt_socket_protection_password(self, socket_number: int, protection: dict):
        """Meminta password proteksi sebelum mengizinkan OFF."""
        expected_hash = protection.get("password_hash", "") or ""
        if not expected_hash:
            show_styled_warning(
                self,
                "Protection Password Missing",
                (
                    f"Smart Socket {socket_number} memakai mode password, "
                    f"tetapi password belum tersimpan."
                ),
            )
            return False

        password, ok = QInputDialog.getText(
            self,
            "Socket Protection Password",
            f"Enter password to turn OFF Smart Socket {socket_number}:",
            QLineEdit.EchoMode.Password,
            "",
        )
        if not ok:
            return False

        password = (password or "").strip()
        return bool(password) and (
            self._hash_socket_protection_password(password) == expected_hash
        )

    def _authorize_socket_power_off(self, socket_number: int):
        """Menentukan apakah aksi OFF socket boleh diteruskan."""
        if self.is_admin_user():
            return True, "admin bypass"

        load_success, protection = self.reload_one_socket_power_off_protection(socket_number)
        if not load_success:
            self.log(
                f"[SmartSocket Protection] Using cached protection for socket {socket_number}"
            )
        else:
            self.log(
                f"[SmartSocket Protection] Refreshed protection for socket {socket_number} from Firebase"
            )

        if not protection.get("enabled"):
            return True, "protection disabled"

        mode = protection.get("mode", "blocked")
        message = self._socket_protection_message(socket_number, protection)

        if mode == "blocked":
            show_styled_warning(
                self,
                "Socket Protected",
                f"{message}\n\nUser biasa tidak dapat mematikan socket ini."
            )
            return False, "blocked for non-admin"

        reply = show_styled_question(
            self,
            "Confirm Socket OFF",
            f"{message}\n\nAre you sure you want to turn it OFF?"
        )
        if reply != QMessageBox.StandardButton.Yes:
            return False, "user cancelled confirmation"

        if self._prompt_socket_protection_password(socket_number, protection):
            return True, "password verified"

        show_styled_warning(
            self,
            "Wrong Password",
            f"Password untuk mematikan Smart Socket {socket_number} tidak valid."
        )
        return False, "invalid password"

    def ac_temp_up(self):
        """Mengirim perintah menaikkan suhu AC."""
        self.acbutton_backend.temp_up()

    def ac_temp_down(self):
        """Mengirim perintah menurunkan suhu AC."""
        self.acbutton_backend.temp_down()

    def ac_mode_cool(self):
        """Mengubah mode AC ke mode pendingin."""
        self.acbutton_backend.mode_cool()

    def ac_mode_fan(self):
        """Mengubah mode AC ke mode kipas."""
        self.acbutton_backend.mode_fan()

    def get_mqtt_log_mode(self):
        """Mengembalikan mode log MQTT aktif untuk backend."""
        return getattr(self, "mqtt_log_mode", self.MQTT_LOG_MODE_NORMAL)

    def _should_show_log_entry(self, entry) -> bool:
        """Menentukan apakah sebuah entri log tampil pada mode aktif."""
        mode = self.get_mqtt_log_mode()
        normalized = str(entry.get("level", "normal") or "normal").strip().lower()
        message = str(entry.get("message", "") or "")
        if mode == self.MQTT_LOG_MODE_TECHNICAL:
            return True
        if mode == self.MQTT_LOG_MODE_BAB4:
            if message.startswith("[Growatt"):
                return False
            if message.startswith("[SmartSocket Manager]") or message.startswith("[SmartSocket]"):
                return False
            if message.startswith("[MQTT DEBUG] Request subscribe dikirim:"):
                return False
            if normalized == "normal" and (
                message.startswith("[MQTT CORE] TLS enabled")
                or message.startswith("[MQTT CORE] Plain MQTT")
                or message.startswith("[MQTT CORE] Connecting to")
                or message.startswith("[MQTT CORE] Connected to")
                or message.startswith("[MQTT CORE] Subscribed to:")
            ):
                return False
            return normalized in {"normal", "communication"}
        return normalized == "normal"

    def _record_log_entry(self, message: str, level: str = "normal"):
        """Menyimpan satu entri log ke history memori."""
        timestamp = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.log_history.append(
            {
                "time": timestamp,
                "message": str(message),
                "level": str(level or "normal").strip().lower(),
            }
        )
        if len(self.log_history) > self.max_log_history:
            self.log_history = self.log_history[-self.max_log_history :]

    def _refresh_log_view(self):
        """Menggambar ulang panel log berdasarkan mode aktif."""
        if not hasattr(self.ui, "logPlainEdit"):
            return

        scrollbar = self.ui.logPlainEdit.verticalScrollBar()
        was_at_bottom = scrollbar.value() >= max(0, scrollbar.maximum() - 5)
        self.ui.logPlainEdit.setUpdatesEnabled(False)
        self.ui.logPlainEdit.clear()
        for entry in self.log_history:
            if self._should_show_log_entry(entry):
                self.ui.logPlainEdit.appendPlainText(
                    f"[{entry['time']}] {entry['message']}"
                )
        self.ui.logPlainEdit.setUpdatesEnabled(True)
        if was_at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def log_mqtt(self, message: str, level: str = "normal"):
        """Logger khusus MQTT yang diarahkan ke panel log utama."""
        self.log(message, level=level)

    def log(self, message: str, level: str = "normal"):
        """Menjadwalkan penambahan log ke UI secara aman dari event loop Qt."""
        # Pastikan append log selalu aman dipanggil dari konteks callback/timer.
        QTimer.singleShot(0, lambda: self._append_log(message, level))

    def _append_log(self, message: str, level: str = "normal"):
        """Menambahkan satu baris log ke history dan panel dashboard."""
        self._record_log_entry(message, level)
        if self._should_show_log_entry(self.log_history[-1]):
            time = self.log_history[-1]["time"]
            self.ui.logPlainEdit.appendPlainText(f"[{time}] {message}")
            self.ui.logPlainEdit.verticalScrollBar().setValue(
                self.ui.logPlainEdit.verticalScrollBar().maximum()
            )

    @staticmethod
    def _set_text_if_changed(widget, text: str):
        """Menghindari repaint bila teks widget tidak berubah."""
        if widget is not None and widget.text() != text:
            widget.setText(text)

    def _set_socket_metric_text(self, socket_number: int, metric: str, label, text: str):
        """Menyimpan cache teks label Smart Socket agar update identik dilewati."""
        if label is None:
            return

        cache = self._socket_energy_label_cache.setdefault(socket_number, {})
        if cache.get(metric) == text:
            return

        cache[metric] = text
        label.setText(text)

    def _apply_sensor_panel_style(
        self,
        cache_key: str,
        category: str,
        frame,
        title,
        frame_color: str,
        border_color: str,
        title_bg: str,
    ):
        """Menerapkan stylesheet panel sensor hanya saat kategorinya berubah."""
        if self._style_state_cache.get(cache_key) == category:
            return

        self._style_state_cache[cache_key] = category
        frame.setStyleSheet(f"""
        QFrame#{frame.objectName()} {{
            background-color: {frame_color};
            border: 2px solid {border_color};
            border-radius: 10px;
        }}
        """)

        title.setStyleSheet(f"""
        QLabel#{title.objectName()} {{
            font: bold 14pt "Segoe UI";
            color: white;
            background-color: {title_bg};
            border-radius: 8px;
            padding: 6px 10px;
            border: 1px solid {title_bg};
        }}
        """)

    def start_growatt_worker(self):
        """Menjalankan worker pengambil data Growatt jika belum ada yang aktif."""
        # Cegah worker ganda agar request ke Growatt tidak menumpuk.
        if self.growatt_worker and self.growatt_worker.isRunning():
            return

        self.growatt_worker = GrowattWorker(self.growatt)
        self.growatt_worker.data_ready.connect(self.update_growatt_ui)
        self.growatt_worker.error.connect(
            lambda err: self.log(f"[Growatt ERROR] {err}")
        )
        self.growatt_worker.start()
        
    def update_mcu_status_ui(self):
        """Memperbarui status online/offline MCU dan enable state kontrol device."""
        # Status online/offline MCU mempengaruhi apakah tombol device aktif.
        status = self.mcu_status.fetch()

        # Guest mode memang dibatasi aksesnya, jadi jangan sampai logika status
        # MCU justru membuka kembali tombol kontrol untuk guest.
        is_guest = self.user_session.get("role") == "guest" if self.user_session else False

        # ===== MCU A =====
        if status["mcuA"] is not None:
            statemcuA = status["mcuA"]
            changed_a = self._last_mcu_status.get("mcuA") != statemcuA

            if changed_a:
                self._set_text_if_changed(
                    self.ui.statusmcuA,
                    "MCU A: ONLINE" if statemcuA else "MCU A: OFFLINE"
                )
                self.ui.statusmcuA.setProperty(
                    "state", "on" if statemcuA else "off"
                )
                self.ui.statusmcuA.style().polish(self.ui.statusmcuA)
                self._last_mcu_status["mcuA"] = statemcuA

            # Hanya ubah status aktif tombol jika BUKAN guest mode
            if not is_guest and changed_a:
                disabled_lamps = {4}

                for idx, lamp in enumerate(self.lamps, start=1):
                    if idx in disabled_lamps:
                        if lamp.isEnabled():
                            lamp.setEnabled(False)
                    else:
                        if lamp.isEnabled() != statemcuA:
                            lamp.setEnabled(statemcuA)

        # ===== MCU B =====
        if status["mcuB"] is not None:
            statemcuB = status["mcuB"]
            changed_b = self._last_mcu_status.get("mcuB") != statemcuB

            if changed_b:
                self._set_text_if_changed(
                    self.ui.statusmcuB,
                    "MCU B: ONLINE" if statemcuB else "MCU B: OFFLINE"
                )
                self.ui.statusmcuB.setProperty(
                    "state", "on" if statemcuB else "off"
                )
                self.ui.statusmcuB.style().polish(self.ui.statusmcuB)
                self._last_mcu_status["mcuB"] = statemcuB

            # Hanya ubah status aktif tombol jika BUKAN guest mode
            if not is_guest and changed_b:
                for btn in self.ac_buttons:
                    if btn.isEnabled() != statemcuB:
                        btn.setEnabled(statemcuB)
    
    def update_temp_style(self, temperature, frame, title):
        """Mengubah warna panel suhu berdasarkan kategori temperatur."""
        if temperature is None:
            return

        try:
            temp = float(temperature)
        except (ValueError, TypeError):
            return

        if temp < 20:
            category = "cold"
            frame_color = "#E3F2FD"
            border_color = "#90CAF9"
            title_bg = "#42A5F5"
        elif temp < 26:
            category = "mild"
            frame_color = "#FFF3E6"
            border_color = "#FFD6B0"
            title_bg = "#F4A261"
        elif temp < 32:
            category = "warm"
            frame_color = "#FFF8E1"
            border_color = "#FFE082"
            title_bg = "#F9A825"
        else:
            category = "hot"
            frame_color = "#FDECEA"
            border_color = "#F5C6CB"
            title_bg = "#E53935"
        self._apply_sensor_panel_style(
            f"temp:{frame.objectName()}",
            category,
            frame,
            title,
            frame_color,
            border_color,
            title_bg,
        )
        
    def update_heatindex_style(self, heat_index, frame, title):
        """Mengubah warna panel heat index berdasarkan tingkat panas."""
        if heat_index is None:
            return

        try:
            hi = float(heat_index)
        except (ValueError, TypeError):
            return

        if hi < 27:
            category = "safe"
            frame_color = "#E8F5E9"   # hijau muda
            border_color = "#A5D6A7"
            title_bg = "#43A047"
        elif hi < 32:
            category = "caution"
            frame_color = "#FFFDE7"   # kuning muda
            border_color = "#FFF59D"
            title_bg = "#FBC02D"
        elif hi < 41:
            category = "warning"
            frame_color = "#FFF3E0"   # oranye muda
            border_color = "#FFCC80"
            title_bg = "#FB8C00"
        elif hi < 54:
            category = "danger"
            frame_color = "#FDECEA"   # merah muda
            border_color = "#EF9A9A"
            title_bg = "#E53935"
        else:
            category = "extreme"
            frame_color = "#4E342E"   # maroon gelap
            border_color = "#3E2723"
            title_bg = "#212121"
        self._apply_sensor_panel_style(
            f"heat:{frame.objectName()}",
            category,
            frame,
            title,
            frame_color,
            border_color,
            title_bg,
        )
        
    def update_humidity_style(self, humidity, frame, title):
        """Mengubah warna panel kelembaban berdasarkan rentang humidity."""
        if humidity is None:
            return

        try:
            h = float(humidity)
        except (ValueError, TypeError):
            return

        if h < 30:
            category = "dry"
            frame_color = "#E3F2FD"   # kering (biru)
            border_color = "#90CAF9"
            title_bg = "#42A5F5"
        elif h < 60:
            category = "ideal"
            frame_color = "#E8F5E9"   # ideal (hijau)
            border_color = "#A5D6A7"
            title_bg = "#43A047"
        elif h < 70:
            category = "humid"
            frame_color = "#E0F2F1"   # lembap (toska)
            border_color = "#80CBC4"
            title_bg = "#26A69A"
        else:
            category = "very_humid"
            frame_color = "#F3E5F5"   # sangat lembap (ungu)
            border_color = "#CE93D8"
            title_bg = "#8E24AA"
        self._apply_sensor_panel_style(
            f"hum:{frame.objectName()}",
            category,
            frame,
            title,
            frame_color,
            border_color,
            title_bg,
        )

    # ===============================
    # DASAR WINDOW & HELPER RESOURCE
    # ===============================
    def initUI(self):
        """Menyiapkan properti dasar window seperti judul dan ikon aplikasi."""
        # Pengaturan dasar window yang tidak bergantung pada backend.
        self.setWindowTitle("EcoLab Dashboard")

        # Mengatur Icon Aplikasi
        pixmap = QPixmap(self.resource_path("icon\\logoecolab.ico"))
        icon = QIcon(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setWindowIcon(icon)

    def set_app_version(self, version: str):
        """Menampilkan versi aplikasi pada label bagian bawah window."""
        self.ui.version.setText(version)

    def get_app_version(self) -> str:
        """Mengembalikan string versi aplikasi yang sedang dipakai."""
        return self.APP_VERSION
        
    def resource_path(self, relative_path):
        """Mengonversi path relatif resource menjadi path absolut.
        Berguna untuk memastikan file dapat ditemukan dari
        direktori aplikasi saat ini.

        Fungsi ini memakai `get_resource_path()` agar tetap kompatibel
        saat aplikasi dijalankan sebagai script maupun hasil PyInstaller.
        """
        return get_resource_path(relative_path)

    # ===============================
    # FITUR USER (HALAMAN SETTINGS)
    # ===============================
    def setup_user_features(self):
        """Menyiapkan fitur halaman settings sesuai role dan provider login."""
        if not self.user_session:
            return

        # 1. Muat data profil user
        self.load_user_profile()

        # 2. Cek role dan auth provider
        user_role = self.user_session.get("role", "user")
        auth_provider = self.user_session.get("auth_provider", "email")

        is_guest = user_role == "guest"
        is_admin = user_role == "admin"
        is_google = auth_provider == "google"

        # 3. Atur tombol Admin Panel
        if is_admin:
            # ADMIN: Enable dan connect tombol Admin Panel
            self.ui.btnAdminpanel.setEnabled(True)
            self.ui.btnAdminpanel.setToolTip("Open Admin Panel")
            self.ui.btnAdminpanel.clicked.connect(self.handle_open_admin_panel)
        else:
            # GUEST & REGULAR USER: Disable tombol Admin Panel
            self.ui.btnAdminpanel.setEnabled(False)
            if is_guest:
                self.ui.btnAdminpanel.setToolTip("Not available in Guest Mode")
            else:
                self.ui.btnAdminpanel.setToolTip("Admin access only")

        # 4. Atur tombol Update Password
        if is_guest or is_google:
            # GUEST atau GOOGLE: nonaktifkan tombol Update Password
            self.ui.btnUpdatePassword.setEnabled(False)
            if is_guest:
                self.ui.btnUpdatePassword.setToolTip("Not available in Guest Mode")
            else:  # is_google
                self.ui.btnUpdatePassword.setToolTip("Managed by Google authentication")
        else:
            # USER biasa dan ADMIN: aktifkan tombol Update Password
            self.ui.btnUpdatePassword.setEnabled(True)
            self.ui.btnUpdatePassword.setToolTip("")
            self.ui.btnUpdatePassword.clicked.connect(self.handle_update_password)

        # 5. Atur tombol Logout
        if is_guest:
            # GUEST: Disable tombol Logout
            self.ui.btnLogout.setEnabled(False)
            self.ui.btnLogout.setToolTip("Cannot logout from Guest Mode")
        else:
            # REGULAR USER & ADMIN (termasuk Google): Enable tombol Logout
            self.ui.btnLogout.setEnabled(True)
            self.ui.btnLogout.setToolTip("")
            self.ui.btnLogout.clicked.connect(self.handle_logout)

        # 6. Atur hak akses kontrol device (Smart Socket, Lampu, AC)
        self.setup_device_controls(is_guest)

    def setup_device_controls(self, is_guest):
        """Mengatur hak akses kontrol device berdasarkan mode guest atau bukan."""
        if is_guest:
            # GUEST: Disable semua kontrol devices (read-only mode)

            # === TOMBOL AKSI SMART SOCKET ===
            for i in range(1, 6):
                action_btn = getattr(self.ui, f"btn_action_socket{i}", None)
                if action_btn:
                    action_btn.setEnabled(False)
                    # Widget custom SmartSocketActionButton otomatis
                    # memberi tampilan redup saat disabled.
                    action_btn.setToolTip("Not available in Guest Mode (Read-only)")

            # === TOMBOL SWITCH SMART SOCKET ===
            if hasattr(self, 'switches'):
                for switch in self.switches:
                    switch.setEnabled(False)
                    switch.setToolTip("Not available in Guest Mode (Read-only)")

            # === TOMBOL LAMPU ===
            if hasattr(self, 'lamps'):
                for lamp in self.lamps:
                    lamp.setEnabled(False)
                    lamp.setToolTip("Not available in Guest Mode (Read-only)")

            # === TOMBOL AC ===
            if hasattr(self, 'ac_button'):
                self.ac_button.setEnabled(False)
                self.ac_button.setToolTip("Not available in Guest Mode (Read-only)")

            # === TOMBOL KONTROL AC ===
            ac_control_buttons = ['btn_temp_up', 'btn_temp_down', 'btn_cool_ac', 'btn_fan_ac']
            for btn_name in ac_control_buttons:
                btn = getattr(self.ui, btn_name, None)
                if btn:
                    btn.setEnabled(False)
                    btn.setToolTip("Not available in Guest Mode (Read-only)")
        else:
            # USER & ADMIN: Enable semua kontrol devices
            # Tombol aksi Smart Socket
            for i in range(1, 6):
                action_btn = getattr(self.ui, f"btn_action_socket{i}", None)
                if action_btn:
                    action_btn.setEnabled(True)
                    # Widget custom otomatis menghapus efek redup saat aktif.
                    action_btn.setToolTip("")

            # Tombol switch Smart Socket
            if hasattr(self, 'switches'):
                for switch in self.switches:
                    switch.setEnabled(True)
                    switch.setToolTip("")

            # Tombol lampu
            if hasattr(self, 'lamps'):
                for lamp in self.lamps:
                    # Lamp 4 tetap disabled (sesuai setup awal)
                    if lamp != self.lamps[3]:  # Index 3 adalah Lamp 4
                        lamp.setEnabled(True)
                    lamp.setToolTip("")

            # Tombol AC
            if hasattr(self, 'ac_button'):
                self.ac_button.setEnabled(True)
                self.ac_button.setToolTip("")

            # === TOMBOL KONTROL AC ===
            ac_control_buttons = ['btn_temp_up', 'btn_temp_down', 'btn_cool_ac', 'btn_fan_ac']
            for btn_name in ac_control_buttons:
                btn = getattr(self.ui, btn_name, None)
                if btn:
                    btn.setEnabled(True)
                    btn.setToolTip("")

    def setup_logging_mode_ui(self):
        """Menambahkan kontrol mode debug di panel log settings."""
        if getattr(self, "mqtt_log_mode_frame", None) is not None:
            return

        frame = QFrame(self.ui.logFrame)
        frame.setObjectName("mqttLogModeFrame")
        frame.setStyleSheet(
            "#mqttLogModeFrame {"
            "background-color: #F7FAFE;"
            "border: 1px solid #D6E2F1;"
            "border-radius: 10px;"
            "}"
            "QLabel#mqttLogModeTitle {"
            "font: bold 10.5pt 'Segoe UI';"
            "color: #27445D;"
            "}"
            "QLabel#mqttLogModeHint {"
            "color: #52606D;"
            "font: 9.5pt 'Segoe UI';"
            "}"
            "QComboBox#mqttLogModeCombo {"
            "background-color: #FFFFFF;"
            "color: #163247;"
            "border: 1px solid #B8CDE0;"
            "border-radius: 6px;"
            "padding: 5px 8px;"
            "font: 10pt 'Segoe UI';"
            "min-width: 160px;"
            "}"
            "QComboBox#mqttLogModeCombo QAbstractItemView {"
            "background-color: #FFFFFF;"
            "color: #163247;"
            "selection-background-color: #D9EBF8;"
            "selection-color: #0E2433;"
            "border: 1px solid #B8CDE0;"
            "outline: 0;"
            "}"
            "QComboBox#mqttLogModeCombo:disabled {"
            "color: #7A8A99;"
            "background-color: #F1F5F9;"
            "}"
        )

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        title = QLabel("Debug Mode", frame)
        title.setObjectName("mqttLogModeTitle")
        hint = QLabel(
            "Pilih tingkat tampilan debug tanpa menghapus riwayat log yang sudah tercatat.",
            frame,
        )
        hint.setObjectName("mqttLogModeHint")
        hint.setWordWrap(True)
        text_layout.addWidget(title)
        text_layout.addWidget(hint)

        combo = QComboBox(frame)
        combo.setObjectName("mqttLogModeCombo")
        combo.addItem("Mode Normal", self.MQTT_LOG_MODE_NORMAL)
        combo.addItem("Debug Communication", self.MQTT_LOG_MODE_BAB4)
        combo.addItem("Debug Detail", self.MQTT_LOG_MODE_TECHNICAL)
        combo.setCurrentIndex(max(0, combo.findData(self.mqtt_log_mode)))
        combo.currentIndexChanged.connect(self._on_mqtt_log_mode_changed)

        layout.addLayout(text_layout, 1)
        layout.addWidget(combo, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.ui.verticalLayout_71.insertWidget(1, frame)
        self.mqtt_log_mode_frame = frame
        self.mqtt_log_mode_combo = combo

    def _on_mqtt_log_mode_changed(self, index: int):
        """Memperbarui mode log MQTT aktif dari pilihan user."""
        if not hasattr(self, "mqtt_log_mode_combo"):
            return
        selected_mode = self.mqtt_log_mode_combo.itemData(index) or self.MQTT_LOG_MODE_NORMAL
        self.mqtt_log_mode = str(selected_mode)
        self._refresh_log_view()
        if self.mqtt_log_mode in {self.MQTT_LOG_MODE_BAB4, self.MQTT_LOG_MODE_TECHNICAL}:
            mqtt_client = getattr(self, "mqtt", None)
            if mqtt_client is not None and hasattr(mqtt_client, "emit_debug_snapshot"):
                mqtt_client.emit_debug_snapshot()
        self.log(
            f"[DEBUG] Display mode changed to {self.mqtt_log_mode_combo.currentText()}",
            level="normal",
        )

    def setup_socket_protection_settings_ui(self):
        """Membangun panel admin untuk mengatur proteksi OFF Smart Socket."""
        if hasattr(self, "admin_socket_protection_frame"):
            self.refresh_socket_protection_settings_ui()
            self._update_socket_protection_panel_visibility()
            return

        frame = QFrame(self.ui.settingsandlogFrame)
        frame.setObjectName("adminSocketProtectionFrame")
        frame.setStyleSheet(
            "#adminSocketProtectionFrame {"
            "background-color: #F6FBFF;"
            "border: 2px solid #D6E2F1;"
            "border-radius: 10px;"
            "}"
            "QLabel#adminSocketProtectionTitle {"
            "font: bold 12pt 'Segoe UI';"
            "color: white;"
            "background-color: #246B9F;"
            "border-radius: 8px;"
            "padding: 6px 10px;"
            "}"
            "QLineEdit, QComboBox {"
            "background-color: #FFFFFF;"
            "border: 1px solid #C9D8E6;"
            "border-radius: 6px;"
            "padding: 5px 8px;"
            "}"
            "QCheckBox { color: #1F2D3A; }"
        )
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("Socket Power-Off Protection", frame)
        title.setObjectName("adminSocketProtectionTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info = QLabel(
            "Admin dapat mengatur socket mana yang tidak boleh dimatikan atau "
            "memerlukan password khusus saat user biasa menekan OFF.",
            frame,
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        headers = ["Socket", "Enable", "Mode", "Password", "Description"]
        for col, header in enumerate(headers):
            label = QLabel(header, frame)
            label.setStyleSheet("font-weight: 700; color: #1F2D3A;")
            grid.addWidget(label, 0, col)

        self.socket_protection_controls = {}
        for row, socket_number in enumerate(range(1, 6), start=1):
            socket_label = QLabel(f"Socket {socket_number}", frame)
            enabled_checkbox = QCheckBox(frame)
            mode_combo = QComboBox(frame)
            mode_combo.addItem("Blocked", "blocked")
            mode_combo.addItem("Password required", "password")
            password_input = QLineEdit(frame)
            password_input.setEchoMode(QLineEdit.EchoMode.Password)
            password_input.setPlaceholderText("Leave blank to keep current password")
            note_input = QLineEdit(frame)
            note_input.setPlaceholderText("Example: Supply Raspberry Pi server")

            grid.addWidget(socket_label, row, 0)
            grid.addWidget(enabled_checkbox, row, 1, alignment=Qt.AlignCenter)
            grid.addWidget(mode_combo, row, 2)
            grid.addWidget(password_input, row, 3)
            grid.addWidget(note_input, row, 4)

            self.socket_protection_controls[socket_number] = {
                "enabled": enabled_checkbox,
                "mode": mode_combo,
                "password": password_input,
                "note": note_input,
            }

        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(4, 2)
        layout.addLayout(grid)

        actions = QHBoxLayout()
        actions.addStretch()
        refresh_button = QPushButton("Reload", frame)
        refresh_button.clicked.connect(self.refresh_socket_protection_settings_ui)
        save_button = QPushButton("Save Protection", frame)
        save_button.setStyleSheet(
            "QPushButton { background-color: #0F8B4C; color: #FFFFFF; "
            "border: none; border-radius: 6px; padding: 8px 16px; font-weight: 700; }"
            "QPushButton:hover { background-color: #12A95D; }"
        )
        save_button.clicked.connect(self.save_socket_protection_settings)
        actions.addWidget(refresh_button)
        actions.addWidget(save_button)
        layout.addLayout(actions)

        self.admin_socket_protection_frame = frame
        self.ui.verticalLayout_23.insertWidget(1, frame)
        self.refresh_socket_protection_settings_ui()
        self._update_socket_protection_panel_visibility()

    def _update_socket_protection_panel_visibility(self):
        """Menyesuaikan visibilitas panel proteksi berdasarkan role."""
        frame = getattr(self, "admin_socket_protection_frame", None)
        if frame is None:
            return
        frame.setVisible(self.is_admin_user())

    def refresh_socket_protection_settings_ui(self):
        """Mengisi ulang form proteksi socket dari settings tersimpan."""
        controls = getattr(self, "socket_protection_controls", {})
        if not controls:
            return

        for socket_number, widgets in controls.items():
            protection = self.get_socket_power_off_protection(socket_number)
            widgets["enabled"].setChecked(bool(protection.get("enabled")))
            mode_index = widgets["mode"].findData(protection.get("mode", "blocked"))
            widgets["mode"].setCurrentIndex(max(0, mode_index))
            widgets["password"].clear()
            widgets["note"].setText(protection.get("note", "") or "")

    def save_socket_protection_settings(self):
        """Menyimpan pengaturan proteksi OFF per socket dari panel admin."""
        if not self.is_admin_user():
            show_styled_warning(
                self,
                "Admin Only",
                "Hanya admin yang dapat mengubah proteksi Smart Socket."
            )
            return

        for socket_number, widgets in self.socket_protection_controls.items():
            enabled = widgets["enabled"].isChecked()
            mode = widgets["mode"].currentData() or "blocked"
            note = widgets["note"].text().strip()
            password_text = widgets["password"].text().strip()
            current = self.get_socket_power_off_protection(socket_number)
            password_hash = None

            if enabled and mode == "password":
                if password_text:
                    password_hash = self._hash_socket_protection_password(password_text)
                elif not current.get("password_hash"):
                    show_styled_warning(
                        self,
                        "Password Required",
                        f"Socket {socket_number} memakai mode password, jadi password harus diisi."
                    )
                    widgets["password"].setFocus()
                    return

            self.set_socket_power_off_protection(
                socket_number,
                enabled=enabled,
                mode=mode,
                password_hash=password_hash,
                note=note,
            )

        self.refresh_socket_protection_settings_ui()
        show_styled_information(
            self,
            "Protection Saved",
            "Pengaturan proteksi OFF Smart Socket berhasil disimpan."
        )

    def load_user_profile(self):
        """Mengisi username dan email user ke form halaman settings."""
        if self.user_session:
            # Isi username dan email ke field input.
            self.ui.inputUsername.setText(self.user_session.get("username", ""))
            self.ui.inputEmail.setText(self.user_session.get("email", ""))

            # Cek apakah guest mode
            is_guest = self.user_session.get("role") == "guest"

            # Atur read-only untuk guest mode (styling lewat Qt Designer).
            self.ui.inputUsername.setReadOnly(is_guest)
            self.ui.inputEmail.setReadOnly(is_guest)

    def handle_update_password(self):
        """Menangani proses update password untuk user non-Google."""
        if not self.user_session:
            return

        # Cek apakah user pakai Google Auth
        if self.user_session.get("auth_provider") == "google":
            show_styled_warning(
                self,
                "Update Password",
                "❌ Cannot update password for Google accounts.\n\n"
                "Google authentication is managed by Google."
            )
            return

        # Input dialog untuk password baru
        from PySide6.QtWidgets import QInputDialog
        new_password, ok = QInputDialog.getText(
            self,
            "Update Password",
            "Enter your new password:",
            QLineEdit.EchoMode.Password
        )

        if ok and new_password:
            # Validasi password
            if len(new_password) < 6:
                show_styled_warning(
                    self,
                    "Invalid Password",
                    "❌ Password must be at least 6 characters!"
                )
                return

            # Jalankan proses update password melalui Firebase.
            try:
                auth_service = FirebaseAuthService()

                result = auth_service.set_user_password(
                    self.user_session["uid"],
                    new_password
                )

                if result["status"] == "success":
                    show_styled_information(
                        self,
                        "Success",
                        "✅ Password updated successfully!"
                    )
                else:
                    show_styled_critical(
                        self,
                        "Error",
                        f"❌ Failed to update password:\n{result['message']}"
                    )

            except Exception as e:
                show_styled_critical(
                    self,
                    "Error",
                    f"❌ Failed to update password:\n{str(e)}"
                )

    def handle_logout(self):
        """Meminta konfirmasi logout lalu memberi sinyal ke launcher."""
        from PySide6.QtWidgets import QMessageBox
        reply = show_styled_question(
            self,
            "Logout",
            "Are you sure you want to logout?"
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Emit logout signal untuk launcher
            self.logout_signal.emit()

    def handle_open_admin_panel(self):
        """Membuka jendela admin panel jika fitur admin tersedia."""
        try:
            from dialogs.admin_window import AdminPanelWindow

            # Buka window admin panel.
            self.admin_panel_window = AdminPanelWindow(self)
            self.admin_panel_window.show()

        except Exception as e:
            show_styled_critical(
                self,
                "Error",
                f"❌ Failed to open Admin Panel:\n{str(e)}"
            )

    # ===============================
    # POPUP & ALUR KONTROL SMART SOCKET
    # ===============================
    def open_smartsocket_popup(self, socket_number):
        """Membuka dialog kontrol Smart Socket sambil mencegah popup ganda."""
        # Cek apakah popup untuk socket ini sudah terbuka
        popup_attr = f"_socket{socket_number}_popup"

        if hasattr(self, popup_attr):
            existing_popup = getattr(self, popup_attr)
            # Jika popup masih ada dan visible, fokus ke popup yang sudah ada
            try:
                if existing_popup.isVisible():
                    existing_popup.raise_()  # Bawa popup ke front
                    existing_popup.activateWindow()  # Aktifkan window
                    return  # Jangan buka popup baru
            except:
                # Popup sudah dihancurkan, hapus referensi
                delattr(self, popup_attr)

        try:
            backend = self.smartsocket_manager.get_backend(socket_number)
            popup = SmartSocketPopup(socket_number, backend, self)

            # Simpan referensi popup
            setattr(self, popup_attr, popup)

            popup.exec()  # Modal dialog

            # Hapus referensi setelah popup ditutup
            if hasattr(self, popup_attr):
                delattr(self, popup_attr)

        except Exception as e:
            show_styled_critical(
                self,
                "Error",
                f"❌ Failed to open Smart Socket Control:\n{str(e)}"
            )

    def setup_admin_features(self):
        """Placeholder untuk logika admin tambahan jika nanti diperlukan."""
        # Tombol Admin Panel sudah diatur di setup_user_features().
        pass
    def _on_lamp_status_changed(self, lamp_index: int, state: bool):
        """Menyinkronkan status lampu dari MQTT ke widget lampu terkait."""
        if 1 <= lamp_index <= len(self.lamps):
            lamp = self.lamps[lamp_index - 1]
            if lamp.isOn() != state:
                lamp.blockSignals(True)
                lamp.setChecked(state)
                lamp.blockSignals(False)
            self._last_lamp_ui_states[lamp_index] = state

    def update_lamp_ui_from_state(self):
        """Menyamakan tampilan semua tombol lampu dengan state backend terakhir."""
        for idx, lamp in enumerate(self.lamps, start=1):
            state = self.lampbutton_backend.states.get(idx)
            if state is not None and self._last_lamp_ui_states.get(idx) != state:
                lamp.blockSignals(True)
                lamp.setChecked(state)
                lamp.blockSignals(False)
                self._last_lamp_ui_states[idx] = state

    def _on_ac_status_changed(self, state: bool):
        """Menyinkronkan status AC dari MQTT ke tombol dan label UI."""
        if self.ac_button.isOn() != state:
            self.ac_button.blockSignals(True)
            self.ac_button.setChecked(state)
            self.ac_button.blockSignals(False)

        if hasattr(self, "update_ac_status") and self._last_ac_ui_state != state:
            self.update_ac_status(state)
        self._last_ac_ui_state = state

    def update_ac_ui_from_state(self):
        """Menyamakan tombol AC dengan state backend terakhir."""
        state = self.acbutton_backend.state
        if state is not None and self._last_ac_ui_state != state:
            self.ac_button.blockSignals(True)
            self.ac_button.setChecked(state)
            self.ac_button.blockSignals(False)

            if hasattr(self, "update_ac_status"):
                self.update_ac_status(state)
            self._last_ac_ui_state = state

    # ===============================
    # RECORDING & PENGATURAN SMART SOCKET
    # ===============================
    # Bagian ini mengatur recording data per socket, autosave CSV,
    # interval sampling, dan penyimpanan preferensi monitoring.
    def start_socket_recording(self, socket_number: int, source="manual"):
        """Memulai perekaman data monitoring untuk satu Smart Socket."""
        changed = self.smartsocket_recorder.start(socket_number, source=source)
        if changed:
            self.log(f"[Socket {socket_number}] Recording started ({source})")
            self.socket_recording_state_changed.emit(socket_number, True)
        return changed

    def stop_socket_recording(self, socket_number: int, source="manual"):
        """Menghentikan perekaman data monitoring untuk satu Smart Socket."""
        changed = self.smartsocket_recorder.stop(socket_number, source=source)
        if changed:
            self.log(f"[Socket {socket_number}] Recording stopped ({source})")
            self.socket_recording_state_changed.emit(socket_number, False)
        return changed

    def set_socket_follow_schedule(self, socket_number: int, enabled: bool):
        """Mengatur apakah recording socket mengikuti trigger schedule."""
        self.smartsocket_recorder.set_follow_schedule(socket_number, enabled)
        if enabled:
            self.smartsocket_recorder.set_autosave_enabled(socket_number, True)
        state = "enabled" if enabled else "disabled"
        self._persist_socket_monitoring_settings(socket_number)
        self.log(f"[Socket {socket_number}] Follow schedule recording {state}")

    def set_socket_record_interval_seconds(self, socket_number: int, seconds: float):
        """Mengatur interval sampling recording untuk satu Smart Socket."""
        self.smartsocket_recorder.set_record_interval_seconds(socket_number, seconds)
        self._persist_socket_monitoring_settings(socket_number)
        self.log(f"[Socket {socket_number}] Record interval set to {seconds}s")

    def get_socket_record_interval_seconds(self, socket_number: int):
        """Mengambil interval recording yang aktif untuk satu Smart Socket."""
        return self.smartsocket_recorder.get_record_interval_seconds(socket_number)

    def set_socket_autosave_enabled(self, socket_number: int, enabled: bool):
        """Mengaktifkan atau menonaktifkan autosave CSV untuk satu socket."""
        if self.is_socket_follow_schedule(socket_number) and not enabled:
            enabled = True
        self.smartsocket_recorder.set_autosave_enabled(socket_number, enabled)
        state = "enabled" if enabled else "disabled"
        self._persist_socket_monitoring_settings(socket_number)
        self.log(f"[Socket {socket_number}] Autosave {state}")

    def is_socket_autosave_enabled(self, socket_number: int):
        """Mengecek apakah autosave socket sedang aktif."""
        return self.smartsocket_recorder.is_autosave_enabled(socket_number)

    def set_socket_autosave_dir(self, socket_number: int, directory: str):
        """Menyimpan folder tujuan autosave CSV untuk satu socket."""
        self.smartsocket_recorder.set_autosave_dir(socket_number, directory)
        self._persist_socket_monitoring_settings(socket_number)
        self.log(f"[Socket {socket_number}] Autosave dir: {directory}")

    def get_socket_autosave_dir(self, socket_number: int):
        """Mengambil folder autosave CSV yang dipakai oleh satu socket."""
        return self.smartsocket_recorder.get_autosave_dir(socket_number)

    def is_socket_recording(self, socket_number: int):
        """Mengecek apakah socket tertentu sedang merekam data."""
        return self.smartsocket_recorder.is_recording(socket_number)

    def is_socket_follow_schedule(self, socket_number: int):
        """Mengecek apakah mode follow schedule aktif untuk socket tertentu."""
        return self.smartsocket_recorder.is_follow_schedule(socket_number)

    def get_socket_records(self, socket_number: int):
        """Mengambil data record sementara milik satu socket."""
        return self.smartsocket_recorder.get_records(socket_number)

    def clear_socket_records(self, socket_number: int):
        """Menghapus data record sementara milik satu Smart Socket."""
        self.smartsocket_recorder.clear_records(socket_number)
        self.log(f"[Socket {socket_number}] Recording data cleared")

    def export_socket_records_csv(self, socket_number: int, path: str):
        """Mengekspor data record Smart Socket ke file CSV."""
        count = self.smartsocket_recorder.export_csv(socket_number, path)
        self.log(f"[Socket {socket_number}] Exported {count} rows to CSV")
        return count

    def _start_socket_daily_autosave_timer(self):
        """Menjalankan pengecekan rollover harian untuk recording manual."""
        self.socket_daily_autosave_timer = QTimer(self)
        self.socket_daily_autosave_timer.setInterval(60 * 1000)
        self.socket_daily_autosave_timer.timeout.connect(self._check_socket_daily_rollover)
        self.socket_daily_autosave_timer.start()
        QTimer.singleShot(1000, self._check_socket_daily_rollover)

    def _restore_smartsocket_recovery(self):
        """Memulihkan checkpoint record yang belum sempat diekspor."""
        try:
            restored = self.smartsocket_recorder.restore_recovery()
        except Exception as exc:
            self.log(f"[SmartSocket] Recovery restore failed: {exc}")
            return

        for socket_number, count in restored.items():
            self.log(f"[Socket {socket_number}] Restored {count} unsaved recording rows")

    def _unique_csv_path(self, directory: str, filename: str):
        """Membuat path CSV tanpa menimpa file lama."""
        base, ext = os.path.splitext(filename)
        candidate = os.path.join(directory, filename)
        suffix = 2
        while os.path.exists(candidate):
            candidate = os.path.join(directory, f"{base}_{suffix}{ext}")
            suffix += 1
        return candidate

    def _autosave_socket_records(self, socket_number: int, records: list, filename: str):
        """Menyimpan batch record tertentu ke folder autosave socket."""
        autosave_dir = self.smartsocket_recorder.get_autosave_dir(socket_number)
        if not autosave_dir:
            self.log(f"[Socket {socket_number}] Autosave enabled but no folder set")
            return None, 0

        os.makedirs(autosave_dir, exist_ok=True)
        path = self._unique_csv_path(autosave_dir, filename)
        count = self.smartsocket_recorder.export_records_csv(records, path)
        self.log(f"[Socket {socket_number}] Autosaved {count} rows to {path}")
        return path, count

    def _split_socket_records_by_date(self, socket_number: int):
        """Memisahkan records socket menjadi data lama dan data hari ini."""
        today = datetime.now().date().isoformat()
        by_date = {}
        current_records = []

        for record in self.smartsocket_recorder.get_records(socket_number):
            record_date = str(record.get("timestamp", ""))[:10]
            if record_date and record_date < today:
                by_date.setdefault(record_date, []).append(record)
            else:
                current_records.append(record)

        return by_date, current_records

    def _check_socket_daily_rollover(self):
        """Autosave data hari lama tanpa menghentikan recording manual."""
        if not hasattr(self, "smartsocket_recorder"):
            return

        for socket_number in range(1, 6):
            if not self.smartsocket_recorder.is_autosave_enabled(socket_number):
                continue
            if (
                self.smartsocket_recorder.is_follow_schedule(socket_number)
                and self.smartsocket_recorder.is_recording(socket_number)
            ):
                continue

            old_records_by_date, current_records = self._split_socket_records_by_date(socket_number)
            if not old_records_by_date:
                continue

            remaining_records = list(current_records)
            for record_date, records in sorted(old_records_by_date.items()):
                if not records:
                    continue
                filename = f"smartsocket_{socket_number}_daily_{record_date}.csv"
                try:
                    _, count = self._autosave_socket_records(socket_number, records, filename)
                    if count <= 0:
                        remaining_records.extend(records)
                except Exception as exc:
                    remaining_records.extend(records)
                    self.log(f"[Socket {socket_number}] Daily autosave failed: {exc}")

            if len(remaining_records) != len(self.smartsocket_recorder.get_records(socket_number)):
                remaining_records.sort(key=lambda record: str(record.get("timestamp", "")))
                self.smartsocket_recorder.replace_records(socket_number, remaining_records)
                self.log(f"[Socket {socket_number}] Daily rollover completed")

    def _load_smartsocket_monitoring_settings(self):
        """Memuat pengaturan monitoring Smart Socket dari penyimpanan lokal."""
        if not hasattr(self, "smartsocket_settings_manager"):
            return

        self.global_smartsocket_monitoring_settings = (
            self.smartsocket_settings_manager.get_global_settings()
        )

        global_follow_schedule = bool(
            self.global_smartsocket_monitoring_settings.get("follow_schedule", False)
        )
        global_interval_seconds = self.global_smartsocket_monitoring_settings.get(
            "record_interval_seconds"
        )
        global_autosave_enabled = bool(
            self.global_smartsocket_monitoring_settings.get("autosave_enabled", False)
        )
        global_autosave_dir = (
            self.global_smartsocket_monitoring_settings.get("autosave_dir", "") or ""
        )

        for socket_number in range(1, 6):
            try:
                self.smartsocket_recorder.set_follow_schedule(
                    socket_number,
                    global_follow_schedule,
                )
            except Exception:
                pass

            try:
                if global_interval_seconds is not None:
                    self.smartsocket_recorder.set_record_interval_seconds(
                        socket_number,
                        float(global_interval_seconds),
                    )
            except Exception:
                pass

            try:
                self.smartsocket_recorder.set_autosave_enabled(
                    socket_number,
                    global_autosave_enabled,
                )
            except Exception:
                pass

            try:
                self.smartsocket_recorder.set_autosave_dir(
                    socket_number,
                    global_autosave_dir,
                )
            except Exception:
                pass

        for socket_number in range(1, 6):
            settings = self.smartsocket_settings_manager.get_socket_settings(socket_number)
            if not settings:
                continue

            try:
                self.smartsocket_recorder.set_follow_schedule(
                    socket_number,
                    bool(settings.get("follow_schedule", False)),
                )
            except Exception:
                pass

            try:
                interval_seconds = settings.get("record_interval_seconds")
                if interval_seconds is not None:
                    self.smartsocket_recorder.set_record_interval_seconds(
                        socket_number,
                        float(interval_seconds),
                    )
            except Exception:
                pass

            try:
                self.smartsocket_recorder.set_autosave_enabled(
                    socket_number,
                    bool(settings.get("autosave_enabled", False)),
                )
            except Exception:
                pass

            try:
                self.smartsocket_recorder.set_autosave_dir(
                    socket_number,
                    settings.get("autosave_dir", "") or "",
                )
            except Exception:
                pass

        self.socket_graph_range_overrides = (
            self.smartsocket_settings_manager.get_all_graph_ranges()
        )
        self.reload_socket_power_off_protection()

    def _persist_socket_monitoring_settings(self, socket_number: int):
        """Menyimpan ulang pengaturan monitoring untuk satu Smart Socket."""
        if not hasattr(self, "smartsocket_settings_manager"):
            return

        self.smartsocket_settings_manager.update_socket_settings(
            socket_number,
            follow_schedule=self.is_socket_follow_schedule(socket_number),
            record_interval_seconds=self.get_socket_record_interval_seconds(socket_number),
            autosave_enabled=self.is_socket_autosave_enabled(socket_number),
            autosave_dir=self.get_socket_autosave_dir(socket_number),
        )

    def get_socket_graph_range_overrides(self):
        """Mengambil override range grafik yang tersimpan untuk semua socket."""
        return dict(getattr(self, "socket_graph_range_overrides", {}))

    def set_socket_graph_range_override(self, socket_number: int, metric: str, override: dict):
        """Menyimpan override range grafik untuk metric socket tertentu."""
        self.socket_graph_range_overrides[(socket_number, metric)] = dict(override)
        if hasattr(self, "smartsocket_settings_manager"):
            self.smartsocket_settings_manager.set_graph_range(socket_number, metric, override)

    def clear_socket_graph_range_override(self, socket_number: int, metric: str):
        """Menghapus override range grafik untuk metric socket tertentu."""
        self.socket_graph_range_overrides.pop((socket_number, metric), None)
        if hasattr(self, "smartsocket_settings_manager"):
            self.smartsocket_settings_manager.set_graph_range(socket_number, metric, None)

    # ===============================
    # SISTEM PERINGATAN SMART SOCKET
    # ===============================
    # Warning arus berlebih dipisahkan dari update data biasa karena perlu
    # level warning, acknowledge user, dan jeda popup agar tidak spam.
    def get_socket_warning_state(self, socket_number: int):
        """Mengambil salinan state warning arus untuk satu Smart Socket."""
        return dict(self.socket_load_warnings.get(socket_number, {}))

    def acknowledge_socket_warning(self, socket_number: int):
        """Menandai warning socket sudah diketahui user agar popup tidak berulang."""
        state = self.socket_load_warnings.get(socket_number)
        if not state or not state.get("active") or state.get("level") == "critical":
            return
        if not state.get("acknowledged"):
            state["acknowledged"] = True
            self.socket_warning_state_changed.emit(socket_number)

    def _warning_from_current(self, current_value: float, relay_on: bool):
        """Menentukan level warning berdasarkan arus dan status relay."""
        if not relay_on:
            return {
                "active": False,
                "level": "normal",
                "message": "",
                "current": 0.0,
                "relay_on": False,
            }

        if current_value >= self.SOCKET_WARNING_CRITICAL_CURRENT:
            return {
                "active": True,
                "level": "critical",
                "message": "Cabut atau kurangi beban segera",
                "current": current_value,
                "relay_on": relay_on,
            }
        if current_value >= self.SOCKET_WARNING_HIGH_CURRENT:
            return {
                "active": True,
                "level": "high",
                "message": "Beban tinggi, harap kurangi beban",
                "current": current_value,
                "relay_on": relay_on,
            }
        if current_value >= self.SOCKET_WARNING_ELEVATED_CURRENT:
            return {
                "active": True,
                "level": "elevated",
                "message": "Beban cukup tinggi",
                "current": current_value,
                "relay_on": relay_on,
            }
        return {
            "active": False,
            "level": "normal",
            "message": "",
            "current": current_value,
            "relay_on": relay_on,
        }

    def _warning_popup_title(self, level: str):
        """Menghasilkan judul popup warning sesuai tingkat bahayanya."""
        return {
            "elevated": "Socket Load Warning",
            "high": "Socket Load Warning",
            "critical": "Socket Load Critical",
        }.get(level, "Socket Load Warning")

    def _show_socket_high_warning_popup(self, socket_number: int):
        """Menampilkan popup warning untuk level high."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state.get("active") or state.get("popup_open") or state.get("level") != "high":
            return

        text = (
            f"Smart Socket {socket_number}\n"
            f"Current: {float(state.get('current', 0.0)):.3f} A\n"
            f"{state.get('message', '')}"
        )
        state["last_popup_at"] = time.time()
        state["popup_open"] = True
        show_styled_warning(self, self._warning_popup_title("high"), text)
        current_state = self.socket_load_warnings.get(socket_number)
        if current_state is not None:
            current_state["popup_open"] = False

    def _show_socket_elevated_warning_popup(self, socket_number: int):
        """Menampilkan popup ringan untuk level elevated."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state.get("active") or state.get("popup_open") or state.get("level") != "elevated":
            return

        text = (
            f"Smart Socket {socket_number}\n"
            f"Current: {float(state.get('current', 0.0)):.3f} A\n"
            "Beban mulai meningkat. Pantau perangkat dan kurangi beban bila perlu."
        )
        state["last_popup_at"] = time.time()
        state["popup_open"] = True
        show_styled_information(self, self._warning_popup_title("elevated"), text)
        current_state = self.socket_load_warnings.get(socket_number)
        if current_state is not None:
            current_state["popup_open"] = False

    def _run_socket_critical_action_dialog(self, socket_number: int):
        """Menampilkan dialog aksi untuk overload critical tahap pertama."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state.get("active") or state.get("level") != "critical" or state.get("popup_open"):
            return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Socket Load Critical")
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(
            f"Smart Socket {socket_number}\n"
            f"Current: {float(state.get('current', 0.0)):.3f} A\n"
            f"Batas aman: {self.SOCKET_WARNING_CRITICAL_CURRENT:.1f} A\n\n"
            "Cabut atau kurangi beban sekarang."
        )
        btn_shutdown = msg_box.addButton("Matikan Sekarang", QMessageBox.ButtonRole.DestructiveRole)
        btn_recheck = msg_box.addButton("Saya Sudah Kurangi Beban", QMessageBox.ButtonRole.AcceptRole)
        msg_box.setDefaultButton(btn_recheck)
        msg_box.setEscapeButton(btn_shutdown)
        msg_box.setWindowFlag(Qt.WindowCloseButtonHint, False)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #000000;
                background-color: transparent;
                font-size: 10pt;
            }
            QMessageBox QPushButton {
                color: #000000;
                background-color: #FDECEC;
                border: 1px solid #E7B4B4;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 120px;
                font-size: 9pt;
            }
            QMessageBox QPushButton:hover {
                background-color: #F8DADA;
                border: 1px solid #C53030;
            }
        """)

        response_deadline = time.time() + self.SOCKET_CRITICAL_FIRST_RESPONSE_SECONDS
        auto_shutdown = {"value": False}

        def update_dialog_countdown():
            remaining_seconds = max(
                0,
                int(round(response_deadline - time.time()))
            )
            msg_box.setInformativeText(
                "Pilih 'Matikan Sekarang' untuk memutus daya, "
                "atau pilih 'Saya Sudah Kurangi Beban' untuk verifikasi ulang.\n\n"
                f"Auto OFF dalam {remaining_seconds} detik jika tidak ada respons."
            )

            if remaining_seconds <= 0:
                auto_shutdown["value"] = True
                countdown_timer.stop()
                msg_box.done(0)

        countdown_timer = QTimer(msg_box)
        countdown_timer.setInterval(1000)
        countdown_timer.timeout.connect(update_dialog_countdown)
        update_dialog_countdown()
        countdown_timer.start()

        state["popup_open"] = True
        msg_box.exec()
        current_state = self.socket_load_warnings.get(socket_number)
        if current_state is not None:
            current_state["popup_open"] = False
        countdown_timer.stop()
        state = self.socket_load_warnings.get(socket_number, state)
        clicked_button = msg_box.clickedButton()

        if auto_shutdown["value"]:
            self.log(
                f"[Socket {socket_number}] Critical overload ignored for "
                f"{int(self.SOCKET_CRITICAL_FIRST_RESPONSE_SECONDS)}s, auto protection starting"
            )
            self._shutdown_socket_for_overload(socket_number, automatic=True)
            return

        if clicked_button == btn_shutdown:
            self.log(f"[Socket {socket_number}] User chose immediate shutdown from critical popup")
            self._shutdown_socket_for_overload(socket_number, automatic=False)
            return

        state["critical_stage"] = 1
        state["critical_recheck_pending"] = True
        state["critical_recheck_due_at"] = (
            time.time() + self.SOCKET_CRITICAL_RECHECK_DELAY_SECONDS
        )
        self.socket_warning_state_changed.emit(socket_number)
        recheck_timer = self.socket_critical_recheck_timers.get(socket_number)
        if recheck_timer is not None:
            recheck_timer.start(int(self.SOCKET_CRITICAL_RECHECK_DELAY_SECONDS * 1000))
        self.log(
            f"[Socket {socket_number}] User reported load reduced, grace period "
            f"{int(self.SOCKET_CRITICAL_RECHECK_DELAY_SECONDS)}s started"
        )

    def _show_socket_critical_countdown_popup(self, socket_number: int):
        """Menampilkan popup kedua sebelum auto-off saat overload tetap tinggi."""
        state = self.socket_load_warnings.get(socket_number, {})
        if (
            not state.get("active")
            or state.get("level") != "critical"
            or state.get("popup_open")
            or state.get("critical_second_popup_shown")
        ):
            return

        state["critical_stage"] = 2
        state["critical_second_popup_shown"] = True
        state["critical_deadline"] = time.time() + self.SOCKET_CRITICAL_AUTO_OFF_DELAY_SECONDS
        self.socket_warning_state_changed.emit(socket_number)
        self.log(
            f"[Socket {socket_number}] Load still above "
            f"{self.SOCKET_WARNING_CRITICAL_CURRENT:.1f}A after grace period, "
            f"final warning shown"
        )
        auto_off_timer = self.socket_critical_auto_off_timers.get(socket_number)
        if auto_off_timer is not None:
            auto_off_timer.start(int(self.SOCKET_CRITICAL_AUTO_OFF_DELAY_SECONDS * 1000))

        text = (
            f"Smart Socket {socket_number}\n"
            f"Current: {float(state.get('current', 0.0)):.3f} A\n"
            f"Beban masih di atas {self.SOCKET_WARNING_CRITICAL_CURRENT:.1f} A.\n"
            f"Socket akan dimatikan otomatis dalam "
            f"{int(self.SOCKET_CRITICAL_AUTO_OFF_DELAY_SECONDS)} detik jika arus tidak turun."
        )
        state["last_popup_at"] = time.time()
        state["popup_open"] = True
        show_styled_critical(self, "Socket Load Critical", text)
        current_state = self.socket_load_warnings.get(socket_number)
        if current_state is not None:
            current_state["popup_open"] = False

    def _recheck_socket_critical_load(self, socket_number: int, force: bool = False):
        """Memverifikasi ulang arus setelah user mengaku sudah mengurangi beban."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state:
            return

        due_at = float(state.get("critical_recheck_due_at", 0.0) or 0.0)
        if (
            not force
            and state.get("critical_recheck_pending")
            and due_at
            and time.time() < due_at
        ):
            return

        state["critical_recheck_pending"] = False
        state["critical_recheck_due_at"] = 0.0
        live_current, relay_on = self._get_socket_live_load_state(socket_number)
        if (
            state.get("active")
            and state.get("level") == "critical"
            and not state.get("auto_off_sent")
            and live_current >= self.SOCKET_WARNING_CRITICAL_CURRENT
            and relay_on
        ):
            self._show_socket_critical_countdown_popup(socket_number)
        else:
            self.log(
                f"[Socket {socket_number}] Load recovered during grace period "
                f"({live_current:.3f}A), auto protection cancelled"
            )
            self.socket_warning_state_changed.emit(socket_number)

    def _get_socket_live_load_state(self, socket_number: int):
        """Mengambil arus dan relay state terbaru dari backend jika tersedia."""
        backend = self.smartsocket_manager.get_backend(socket_number)
        live_current = 0.0
        relay_on = False

        if backend is not None:
            try:
                live_current = float(
                    (getattr(backend, "energy_data", {}) or {}).get("current", 0.0) or 0.0
                )
            except (TypeError, ValueError):
                live_current = 0.0

            relay_state = getattr(backend, "relay_state", None)
            if relay_state is not None:
                relay_on = bool(relay_state)

        if not relay_on and socket_number <= len(getattr(self, "switches", [])):
            relay_on = bool(self.switches[socket_number - 1].isOn())

        if live_current <= 0.0:
            state = self.socket_load_warnings.get(socket_number, {})
            try:
                live_current = float(state.get("current", 0.0) or 0.0)
            except (TypeError, ValueError):
                live_current = 0.0

        return live_current, relay_on

    def _socket_has_active_schedule(self, backend) -> bool:
        """Menentukan apakah socket masih memiliki schedule aktif yang perlu dihapus."""
        if backend is None:
            return False

        schedule_status = getattr(backend, "schedule_status", {}) or {}
        if not isinstance(schedule_status, dict):
            return False

        mode = str(schedule_status.get("mode", "") or "").strip().lower()
        raw_status = str(schedule_status.get("raw", "") or "").strip().upper()
        if mode == "onetime" and raw_status == "STOP_TRIGGER":
            return False

        for key in ("start", "stop"):
            value = str(schedule_status.get(key, "") or "").strip().upper()
            if value and value not in {"N/A", "CLEAR", "NONE", "NULL"}:
                return True

        return raw_status == "START_TRIGGER"
        
    def _stop_socket_critical_timers(self, socket_number: int):
        """Menghentikan timer proteksi critical milik socket tertentu."""
        recheck_timer = self.socket_critical_recheck_timers.get(socket_number)
        if recheck_timer is not None:
            recheck_timer.stop()

        auto_off_timer = self.socket_critical_auto_off_timers.get(socket_number)
        if auto_off_timer is not None:
            auto_off_timer.stop()

    def _shutdown_socket_for_overload(self, socket_number: int, automatic: bool):
        """Mematikan socket akibat overload dan menghapus schedule bila perlu."""
        state = self.socket_load_warnings.get(socket_number, {})
        if state.get("auto_off_sent") and automatic:
            return

        backend = self.smartsocket_manager.get_backend(socket_number)
        if backend is None:
            return

        self._stop_socket_critical_timers(socket_number)
        if self._socket_has_active_schedule(backend):
            backend.clear_schedule()
            self.log(f"[Socket {socket_number}] Schedule cleared due to overload protection")

        backend.set_relay(False)
        self.log(
            f"[Socket {socket_number}] Relay forced OFF due to "
            f"{'automatic overload protection' if automatic else 'manual overload shutdown'}"
        )

        state["auto_off_sent"] = True
        state["critical_recheck_pending"] = False
        state["critical_recheck_due_at"] = 0.0
        state["critical_stage"] = 2 if automatic else 1
        self.socket_warning_state_changed.emit(socket_number)

        if automatic:
            show_styled_critical(
                self,
                "Socket Auto-Off",
                (
                    f"Smart Socket {socket_number} dimatikan otomatis karena "
                    f"arus tetap di atas {self.SOCKET_WARNING_CRITICAL_CURRENT:.1f} A."
                ),
            )

    def _handle_socket_critical_timeout(self, socket_number: int):
        """Menjalankan auto-off bila overload critical tetap bertahan hingga deadline."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state:
            return

        if (
            not state.get("active")
            or state.get("level") != "critical"
            or not state.get("relay_on")
            or state.get("auto_off_sent")
            or state.get("critical_stage") != 2
        ):
            return

        deadline = float(state.get("critical_deadline", 0.0) or 0.0)
        if deadline and time.time() + 0.25 < deadline:
            return

        live_current, relay_on = self._get_socket_live_load_state(socket_number)
        if relay_on and live_current >= self.SOCKET_WARNING_CRITICAL_CURRENT:
            self._shutdown_socket_for_overload(socket_number, automatic=True)

    def _show_socket_warning_popup(self, socket_number: int):
        """Menampilkan popup warning arus berlebih untuk socket tertentu."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state.get("active") or state.get("popup_open"):
            return

        level = state.get("level", "high")
        if level == "critical":
            self._run_socket_critical_action_dialog(socket_number)
            return
        if level == "high":
            self._show_socket_high_warning_popup(socket_number)
            return
        if level == "elevated":
            self._show_socket_elevated_warning_popup(socket_number)

    def _update_socket_warning_state(self, socket_number: int, current_value: float, relay_on: bool):
        """Memperbarui state warning socket dan memutuskan kapan popup muncul."""
        new_state = self._warning_from_current(current_value, relay_on)
        current_state = self.socket_load_warnings.get(socket_number, {})

        changed = (
            bool(current_state.get("active")) != bool(new_state.get("active"))
            or current_state.get("level") != new_state.get("level")
            or current_state.get("message") != new_state.get("message")
        )

        if not new_state["active"]:
            self._stop_socket_critical_timers(socket_number)
            if current_state.get("active") or current_state.get("current", 0.0) != 0.0:
                previous_level = current_state.get("level", "normal")
                self.socket_load_warnings[socket_number] = {
                    **new_state,
                    "acknowledged": False,
                    "last_popup_at": 0.0,
                    "popup_open": False,
                    "critical_stage": 0,
                    "critical_recheck_pending": False,
                    "critical_recheck_due_at": 0.0,
                    "critical_second_popup_shown": False,
                    "critical_deadline": 0.0,
                    "auto_off_sent": False,
                }
                if previous_level != "normal":
                    self.log(
                        f"[Socket {socket_number}] Warning cleared from {previous_level} "
                        f"({float(current_state.get('current', 0.0) or 0.0):.3f}A)"
                    )
                self.socket_warning_state_changed.emit(socket_number)
            return

        acknowledged = False if changed else bool(current_state.get("acknowledged", False))
        last_popup_at = 0.0 if changed else float(current_state.get("last_popup_at", 0.0) or 0.0)
        popup_open = bool(current_state.get("popup_open", False))
        critical_stage = 0 if changed else int(current_state.get("critical_stage", 0) or 0)
        critical_recheck_pending = False if changed else bool(current_state.get("critical_recheck_pending", False))
        critical_recheck_due_at = 0.0 if changed else float(current_state.get("critical_recheck_due_at", 0.0) or 0.0)
        critical_second_popup_shown = False if changed else bool(current_state.get("critical_second_popup_shown", False))
        critical_deadline = 0.0 if changed else float(current_state.get("critical_deadline", 0.0) or 0.0)
        auto_off_sent = False if changed else bool(current_state.get("auto_off_sent", False))

        if new_state["level"] not in {"elevated", "high"}:
            acknowledged = False

        self.socket_load_warnings[socket_number] = {
            **new_state,
            "acknowledged": acknowledged,
            "last_popup_at": last_popup_at,
            "popup_open": popup_open,
            "critical_stage": critical_stage,
            "critical_recheck_pending": critical_recheck_pending,
            "critical_recheck_due_at": critical_recheck_due_at,
            "critical_second_popup_shown": critical_second_popup_shown,
            "critical_deadline": critical_deadline,
            "auto_off_sent": auto_off_sent,
        }
        if changed:
            previous_level = current_state.get("level", "normal")
            self.log(
                f"[Socket {socket_number}] Warning level "
                f"{previous_level} -> {new_state['level']} "
                f"at {float(new_state.get('current', 0.0) or 0.0):.3f}A"
            )
        self.socket_warning_state_changed.emit(socket_number)

        if new_state["level"] == "critical":
            if changed and not popup_open:
                self._show_socket_warning_popup(socket_number)
            elif critical_recheck_pending and critical_recheck_due_at:
                self._recheck_socket_critical_load(socket_number)
            elif critical_stage == 2 and critical_deadline:
                self._handle_socket_critical_timeout(socket_number)
            return

        self._stop_socket_critical_timers(socket_number)
        if new_state["level"] != "high":
            if new_state["level"] != "elevated":
                return

        popup_interval = (
            self.SOCKET_WARNING_HIGH_POPUP_INTERVAL_SECONDS
            if new_state["level"] == "high"
            else self.SOCKET_WARNING_ELEVATED_POPUP_INTERVAL_SECONDS
        )
        should_popup = (
            not acknowledged and
            not popup_open and (
                changed or
                (time.time() - last_popup_at) >= popup_interval
            )
        )
        if should_popup:
            self._show_socket_warning_popup(socket_number)

    def get_global_socket_monitoring_settings(self):
        """Mengambil pengaturan monitoring global yang berlaku untuk semua socket."""
        return dict(getattr(self, "global_smartsocket_monitoring_settings", {}))

    def apply_global_socket_monitoring_settings(
        self,
        follow_schedule: bool,
        record_interval_seconds: float,
        autosave_enabled: bool,
        autosave_dir: str,
        save_as_default: bool = False,
    ):
        """Menerapkan satu paket pengaturan monitoring ke seluruh socket."""
        autosave_dir = (autosave_dir or "").strip()
        if follow_schedule:
            autosave_enabled = True
        for socket_number in range(1, 6):
            self.set_socket_follow_schedule(socket_number, follow_schedule)
            self.set_socket_record_interval_seconds(socket_number, record_interval_seconds)
            self.set_socket_autosave_enabled(socket_number, autosave_enabled)
            self.set_socket_autosave_dir(socket_number, autosave_dir)

        settings = {
            "follow_schedule": bool(follow_schedule),
            "record_interval_seconds": float(record_interval_seconds),
            "autosave_enabled": bool(autosave_enabled),
            "autosave_dir": autosave_dir,
        }
        self.global_smartsocket_monitoring_settings = dict(settings)

        if save_as_default and hasattr(self, "smartsocket_settings_manager"):
            self.smartsocket_settings_manager.update_global_settings(**settings)

    def start_all_socket_recording(self, source="manual"):
        """Memulai recording untuk semua Smart Socket sekaligus."""
        for socket_number in range(1, 6):
            self.start_socket_recording(socket_number, source=source)

    def stop_all_socket_recording(self, source="manual"):
        """Menghentikan recording untuk semua Smart Socket sekaligus."""
        for socket_number in range(1, 6):
            self.stop_socket_recording(socket_number, source=source)

    # ===============================
    # HANDLER DATA REALTIME SMART SOCKET
    # ===============================
    # Fungsi berikut menerima event dari backend Smart Socket untuk
    # menyinkronkan relay, energi, timer, jadwal, dan status device ke UI.
    def _on_socket_relay_status(self, socket_number: int, state: bool):
        """Menyinkronkan status relay Smart Socket ke switch dan label UI."""
        if 1 <= socket_number <= 5:
            # Perbarui state tombol switch.
            if socket_number <= len(self.switches):
                switch = self.switches[socket_number - 1]
                if switch.isOn() != state:
                    switch.blockSignals(True)
                    switch.setOn(state)
                    switch.blockSignals(False)

            # Perbarui label status relay.
            label = getattr(self.ui, f"label_switch_status_value{socket_number}", None)
            if label:
                desired_text = "ON" if state else "OFF"
                desired_state = "on" if state else "off"
                if label.text() != desired_text:
                    label.setText(desired_text)
                if label.property("state") != desired_state:
                    label.setProperty("state", desired_state)
                    label.style().polish(label)

            # Kosongkan label energi saat relay OFF.
            if not state:
                self._clear_socket_energy_labels(socket_number)

    def _on_socket_energy_data(self, socket_number: int, data: dict):
        """Memperbarui label energi Smart Socket dan data recording terkait."""
        if not data:
            return

        display_data = dict(data)
        try:
            current_value = float(display_data.get("current", 0) or 0)
        except (TypeError, ValueError):
            current_value = 0.0

        if current_value < 0.1:
            display_data["power"] = 0.0
            display_data["pf"] = 0.0
            display_data["energy"] = 0.0

        # Cek status relay dari backend MQTT, atau fallback ke switch button.
        backend = self.smartsocket_manager.get_backend(socket_number)
        if backend and backend.relay_state is not None:
            relay_on = backend.relay_state
        elif socket_number <= len(self.switches):
            relay_on = self.switches[socket_number - 1].isOn()
        else:
            relay_on = False

        self._update_socket_warning_state(socket_number, current_value, relay_on)

        if hasattr(self, "smartsocket_recorder"):
            self.smartsocket_recorder.append_energy(socket_number, display_data, relay_on)

        # Ambil semua label UI milik socket ini.
        voltage_label = getattr(self.ui, f"label_voltage{socket_number}", None)
        current_label = getattr(self.ui, f"label_current{socket_number}", None)
        power_label = getattr(self.ui, f"label_power{socket_number}", None)
        energy_label = getattr(self.ui, f"label_energy{socket_number}", None)
        freq_label = getattr(self.ui, f"label_frequency{socket_number}", None)
        pf_label = getattr(self.ui, f"label_powerfactor{socket_number}", None)

        # Perbarui label hanya saat relay ON.
        if relay_on:
            if voltage_label:
                self._set_socket_metric_text(
                    socket_number,
                    "voltage",
                    voltage_label,
                    f"Voltage: {display_data.get('voltage', 0):.1f} V",
                )
            if current_label:
                self._set_socket_metric_text(
                    socket_number,
                    "current",
                    current_label,
                    f"Current: {display_data.get('current', 0):.3f} A",
                )
            if power_label:
                self._set_socket_metric_text(
                    socket_number,
                    "power",
                    power_label,
                    f"Power: {display_data.get('power', 0):.1f} W",
                )
            if energy_label:
                self._set_socket_metric_text(
                    socket_number,
                    "energy",
                    energy_label,
                    f"Energy: {display_data.get('energy', 0):.3f} kWh",
                )
            if freq_label:
                self._set_socket_metric_text(
                    socket_number,
                    "frequency",
                    freq_label,
                    f"Frequency: {display_data.get('frequency', 0):.1f} Hz",
                )
            if pf_label:
                self._set_socket_metric_text(
                    socket_number,
                    "pf",
                    pf_label,
                    f"PF: {display_data.get('pf', 0):.2f}",
                )
        else:
            # Tampilkan "--" saat relay OFF
            self._update_socket_warning_state(socket_number, 0.0, False)
            if voltage_label:
                self._set_socket_metric_text(socket_number, "voltage", voltage_label, "Voltage: -- V")
            if current_label:
                self._set_socket_metric_text(socket_number, "current", current_label, "Current: -- A")
            if power_label:
                self._set_socket_metric_text(socket_number, "power", power_label, "Power: -- W")
            if energy_label:
                self._set_socket_metric_text(socket_number, "energy", energy_label, "Energy: -- kWh")
            if freq_label:
                self._set_socket_metric_text(socket_number, "frequency", freq_label, "Frequency: -- Hz")
            if pf_label:
                self._set_socket_metric_text(socket_number, "pf", pf_label, "PF: --")

    def _clear_socket_energy_labels(self, socket_number: int):
        """Mengosongkan tampilan label energi saat relay socket mati."""
        voltage_label = getattr(self.ui, f"label_voltage{socket_number}", None)
        current_label = getattr(self.ui, f"label_current{socket_number}", None)
        power_label = getattr(self.ui, f"label_power{socket_number}", None)
        energy_label = getattr(self.ui, f"label_energy{socket_number}", None)
        freq_label = getattr(self.ui, f"label_frequency{socket_number}", None)
        pf_label = getattr(self.ui, f"label_powerfactor{socket_number}", None)

        if voltage_label:
            self._set_socket_metric_text(socket_number, "voltage", voltage_label, "Voltage: -- V")
        if current_label:
            self._set_socket_metric_text(socket_number, "current", current_label, "Current: -- A")
        if power_label:
            self._set_socket_metric_text(socket_number, "power", power_label, "Power: -- W")
        if energy_label:
            self._set_socket_metric_text(socket_number, "energy", energy_label, "Energy: -- kWh")
        if freq_label:
            self._set_socket_metric_text(socket_number, "frequency", freq_label, "Frequency: -- Hz")
        if pf_label:
            self._set_socket_metric_text(socket_number, "pf", pf_label, "PF: --")

    def _on_socket_timer_status(self, socket_number: int, status: str):
        """Memperbarui label timer Smart Socket dari status backend."""
        label = getattr(self.ui, f"label_timer_status{socket_number}", None)
        if label:
            # Parse status dari backend: "ACTIVE:XXs" atau "INACTIVE".
            if status.startswith("ACTIVE:"):
                # Ambil sisa waktu dalam detik.
                seconds_str = status.replace("ACTIVE:", "").replace("s", "").strip()
                try:
                    remaining_seconds = int(seconds_str)

                    # Cek format yang digunakan user
                    format_type = self.socket_timer_formats.get(socket_number, "seconds")

                    if format_type == "hms":
                        # Konversi ke HH:MM:SS
                        hours = remaining_seconds // 3600
                        minutes = (remaining_seconds % 3600) // 60
                        seconds = remaining_seconds % 60
                        display_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                        self._set_text_if_changed(label, f"Active: {display_time}")
                    else:
                        # Tampilkan dalam detik
                        self._set_text_if_changed(label, f"Active: {remaining_seconds}s")

                    # Jangan ubah warna - biarkan stylesheet asli
                except ValueError:
                    self._set_text_if_changed(label, status)
            elif status == "INACTIVE":
                self._set_text_if_changed(label, "Inactive")
            else:
                self._set_text_if_changed(label, status)

    def _on_socket_schedule_status(self, socket_number: int, status: str):
        """Memperbarui status schedule dan trigger recording berbasis jadwal."""
        import json
        import os
        from datetime import datetime

        # DEBUG: cetak status mentah dari hardware
        # print(f"[DEBUG Schedule UI] Socket {socket_number} received: {repr(status)}")

        if hasattr(self, "smartsocket_recorder"):
            if (
                self.smartsocket_recorder.is_follow_schedule(socket_number)
                and status == "START_TRIGGER"
            ):
                self.smartsocket_recorder.set_autosave_enabled(socket_number, True)
                self._persist_socket_monitoring_settings(socket_number)
                self.start_socket_recording(socket_number, source="schedule")
            elif (
                self.smartsocket_recorder.is_follow_schedule(socket_number)
                and status == "STOP_TRIGGER"
            ):
                self.stop_socket_recording(socket_number, source="schedule")

                # Lakukan autosave saat recording berbasis jadwal selesai,
                # karena user bisa saja tidak sedang melihat popup socket.
                try:
                    self.smartsocket_recorder.set_autosave_enabled(socket_number, True)
                    records = self.smartsocket_recorder.get_records(socket_number)
                    if records:
                        filename = (
                            f"smartsocket_{socket_number}_schedule_"
                            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                        )
                        _, count = self._autosave_socket_records(
                            socket_number,
                            records,
                            filename,
                        )
                        if count > 0:
                            self.smartsocket_recorder.clear_records(socket_number)
                            self.log(f"[Socket {socket_number}] Schedule records cleared after autosave")
                except Exception as exc:
                    self.log(f"[Socket {socket_number}] Autosave failed: {exc}")

        if status == "START_TRIGGER":
            status_text = "Start Triggered"
        elif status == "STOP_TRIGGER":
            status_text = "Stop Triggered"
        else:
            try:
                data = json.loads(status)
                mode = data.get("mode", "N/A")
                start = data.get("start", "N/A")
                stop = data.get("stop", "N/A")

                # DEBUG: cetak hasil parsing data schedule
                # print(f"[DEBUG Schedule UI] Socket {socket_number} parsed - mode: {mode}, start: {start}, stop: {stop}")

                if start and stop:
                    status_text = f"{mode.capitalize()}: {start}-{stop}"
                elif start:
                    status_text = f"Start: {start}"
                elif stop:
                    status_text = f"Stop: {stop}"
                else:
                    status_text = "Not Set"
            except Exception as e:
                # print(f"[DEBUG Schedule UI] Socket {socket_number} JSON parse error: {e}")
                status_text = status

        label = getattr(self.ui, f"label_scheduling_status{socket_number}", None)
        if label:
            # print(f"[DEBUG Schedule UI] Socket {socket_number} updating label to: {repr(status_text)}")
            label.setText(status_text)
        else:
            # print(f"[DEBUG Schedule UI] Socket {socket_number} label NOT FOUND!")
            pass

    def _on_socket_device_status(self, socket_number: int, online: bool):
        """Memperbarui label online atau offline device Smart Socket."""
        label = getattr(self.ui, f"statussocket{socket_number}", None)
        if label:
            desired_text = "Status Device: Online" if online else "Status Device: Offline"
            desired_state = "on" if online else "off"
            if label.text() != desired_text:
                label.setText(desired_text)
            if label.property("state") != desired_state:
                label.setProperty("state", desired_state)
                label.style().polish(label)

    def _sync_socket_states_from_backend(self):
        """Menyelaraskan status device dan relay Smart Socket dari cache backend."""
        backends = getattr(self, "socket_backends", {})
        for socket_number in range(1, 6):
            backend = backends.get(socket_number)
            if backend is None:
                continue

            if backend.device_online is not None:
                self._on_socket_device_status(socket_number, backend.device_online)
            if backend.relay_state is not None:
                self._on_socket_relay_status(socket_number, backend.relay_state)

    def sync_ui_from_mqtt(self):
        """Menyinkronkan UI awal dengan state backend setelah koneksi aktif."""
        # Sinkronkan status lampu.
        self.update_lamp_ui_from_state()

        # Sinkronkan status AC.
        self.update_ac_ui_from_state()

        # Sinkronkan cache Smart Socket yang mungkin sudah diterima lebih dulu
        # dari retained/live MQTT sebelum UI sempat memproses semua signal.
        self._sync_socket_states_from_backend()

        # Inisialisasi label energi Smart Socket ke "--" hanya untuk socket
        # yang memang belum punya relay_state aktif.
        for i in range(1, 6):
            backend = getattr(self, "socket_backends", {}).get(i)
            relay_on = bool(backend.relay_state) if backend and backend.relay_state is not None else False
            if not relay_on:
                self._clear_socket_energy_labels(i)

    def _safe_energy_value(self, value, max_limit=100000):
        """
        Mengubah nilai energi ke float secara aman.

        Jika nilai tidak valid atau terlalu besar akibat bug device,
        fungsi ini mengembalikan 0 agar UI tetap stabil.
        """
        try:
            val = float(value)

            # Jika nilai terlalu besar, kemungkinan ada bug dari device.
            if abs(val) > max_limit:
                return 0

            return round(val, 2)

        except (ValueError, TypeError):
            return 0
                    
# Jalankan aplikasi saat file ini dieksekusi langsung.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
