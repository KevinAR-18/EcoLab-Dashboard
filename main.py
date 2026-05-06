"""
Jendela dashboard utama untuk aplikasi desktop EcoLab.

Modul ini menyatukan UI hasil Qt Designer, widget kustom, backend MQTT,
layanan Growatt dan WeatherCloud, serta aksi user berbasis role
ke dalam satu jendela utama.
"""

import sys,random,os,time
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
    APP_VERSION = "v2.0"

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

        # Konfigurasi tampilan dasar window sebelum backend dijalankan.
        self.initUI()

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
            logger=self.log
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
        self.global_smartsocket_monitoring_settings = {}
        self.socket_graph_range_overrides = {}

        # State warning disimpan per socket supaya popup warning tidak terus
        # muncul berulang tanpa kontrol, dan statusnya bisa di-acknowledge user.
        self.socket_load_warnings = {
            socket_number: {
                "active": False,
                "level": "normal",
                "message": "",
                "current": 0.0,
                "acknowledged": False,
                "last_popup_at": 0.0,
                "popup_open": False,
            }
            for socket_number in range(1, 6)
        }
        self._load_smartsocket_monitoring_settings()

        # Simpan preferensi format timer per socket untuk tampilan popup/UI.
        self.socket_timer_formats = {}  # {socket_number: "hms" atau "seconds"}

        # Registrasi signal/slot Smart Socket lebih awal, lalu sinkronisasi
        # isi UI setelah MQTT punya sedikit waktu untuk menerima state awal.
        SmartSocketSetup.setup(self)
        QTimer.singleShot(500, self.sync_ui_from_mqtt)


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

        # # SEMENTARA: DRAG BG APP (seluruh background)
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
        self.timerLampState.start(300)
        
        self.timerACState = QTimer(self)
        self.timerACState.timeout.connect(self.update_ac_ui_from_state)
        self.timerACState.start(300)

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
        
    def log(self, message: str):
        """Menjadwalkan penambahan log ke UI secara aman dari event loop Qt."""
        # Pastikan append log selalu aman dipanggil dari konteks callback/timer.
        QTimer.singleShot(0, lambda: self._append_log(message))

    def _append_log(self, message: str):
        """Menambahkan satu baris log bertimestamp ke panel log dashboard."""
        time = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.ui.logPlainEdit.appendPlainText(f"[{time}] {message}")
        self.ui.logPlainEdit.verticalScrollBar().setValue(
            self.ui.logPlainEdit.verticalScrollBar().maximum()
        )

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

            self.ui.statusmcuA.setText(
                "MCU A: ONLINE" if statemcuA else "MCU A: OFFLINE"
            )
            self.ui.statusmcuA.setProperty(
                "state", "on" if statemcuA else "off"
            )
            self.ui.statusmcuA.style().polish(self.ui.statusmcuA)

            # Hanya ubah status aktif tombol jika BUKAN guest mode
            if not is_guest:
                disabled_lamps = {4}

                for idx, lamp in enumerate(self.lamps, start=1):
                    if idx in disabled_lamps:
                        lamp.setEnabled(False)
                    else:
                        lamp.setEnabled(statemcuA)

        # ===== MCU B =====
        if status["mcuB"] is not None:
            statemcuB = status["mcuB"]

            self.ui.statusmcuB.setText(
                "MCU B: ONLINE" if statemcuB else "MCU B: OFFLINE"
            )
            self.ui.statusmcuB.setProperty(
                "state", "on" if statemcuB else "off"
            )
            self.ui.statusmcuB.style().polish(self.ui.statusmcuB)

            # Hanya ubah status aktif tombol jika BUKAN guest mode
            if not is_guest:
                for btn in self.ac_buttons:
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
            frame_color = "#E3F2FD"
            border_color = "#90CAF9"
            title_bg = "#42A5F5"
        elif temp < 26:
            frame_color = "#FFF3E6"
            border_color = "#FFD6B0"
            title_bg = "#F4A261"
        elif temp < 32:
            frame_color = "#FFF8E1"
            border_color = "#FFE082"
            title_bg = "#F9A825"
        else:
            frame_color = "#FDECEA"
            border_color = "#F5C6CB"
            title_bg = "#E53935"

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
        
    def update_heatindex_style(self, heat_index, frame, title):
        """Mengubah warna panel heat index berdasarkan tingkat panas."""
        if heat_index is None:
            return

        try:
            hi = float(heat_index)
        except (ValueError, TypeError):
            return

        if hi < 27:
            frame_color = "#E8F5E9"   # hijau muda
            border_color = "#A5D6A7"
            title_bg = "#43A047"
        elif hi < 32:
            frame_color = "#FFFDE7"   # kuning muda
            border_color = "#FFF59D"
            title_bg = "#FBC02D"
        elif hi < 41:
            frame_color = "#FFF3E0"   # oranye muda
            border_color = "#FFCC80"
            title_bg = "#FB8C00"
        elif hi < 54:
            frame_color = "#FDECEA"   # merah muda
            border_color = "#EF9A9A"
            title_bg = "#E53935"
        else:
            frame_color = "#4E342E"   # maroon gelap
            border_color = "#3E2723"
            title_bg = "#212121"

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
        
    def update_humidity_style(self, humidity, frame, title):
        """Mengubah warna panel kelembaban berdasarkan rentang humidity."""
        if humidity is None:
            return

        try:
            h = float(humidity)
        except (ValueError, TypeError):
            return

        if h < 30:
            frame_color = "#E3F2FD"   # kering (biru)
            border_color = "#90CAF9"
            title_bg = "#42A5F5"
        elif h < 60:
            frame_color = "#E8F5E9"   # ideal (hijau)
            border_color = "#A5D6A7"
            title_bg = "#43A047"
        elif h < 70:
            frame_color = "#E0F2F1"   # lembap (toska)
            border_color = "#80CBC4"
            title_bg = "#26A69A"
        else:
            frame_color = "#F3E5F5"   # sangat lembap (ungu)
            border_color = "#CE93D8"
            title_bg = "#8E24AA"

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
        # Perbarui hanya lampu yang statusnya berubah.
        if 1 <= lamp_index <= len(self.lamps):
            lamp = self.lamps[lamp_index - 1]
            lamp.blockSignals(True)
            lamp.setChecked(state)
            lamp.blockSignals(False)

    def update_lamp_ui_from_state(self):
        """Menyamakan tampilan semua tombol lampu dengan state backend terakhir."""
        for idx, lamp in enumerate(self.lamps, start=1):
            state = self.lampbutton_backend.states.get(idx)
            if state is not None:
                lamp.blockSignals(True)
                lamp.setChecked(state)   # ✅ BENAR
                lamp.blockSignals(False)

    def _on_ac_status_changed(self, state: bool):
        """Menyinkronkan status AC dari MQTT ke tombol dan label UI."""
        # Perbarui tombol utama AC.
        self.ac_button.blockSignals(True)
        self.ac_button.setChecked(state)
        self.ac_button.blockSignals(False)

        # Perbarui label status AC jika helper-nya tersedia.
        if hasattr(self, "update_ac_status"):
            self.update_ac_status(state)

    def update_ac_ui_from_state(self):
        """Menyamakan tombol AC dengan state backend terakhir."""
        state = self.acbutton_backend.state
        if state is not None:
            self.ac_button.blockSignals(True)
            self.ac_button.setChecked(state)
            self.ac_button.blockSignals(False)

            # Pastikan label status tambahan ikut tersinkron.
            if hasattr(self, "update_ac_status"):
                self.update_ac_status(state)

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
        if not state or not state.get("active"):
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
            }

        if current_value >= 10.0:
            return {
                "active": True,
                "level": "critical",
                "message": "Kurangi beban segera",
                "current": current_value,
            }
        if current_value >= 8.0:
            return {
                "active": True,
                "level": "high",
                "message": "Beban tinggi, harap waspada",
                "current": current_value,
            }
        if current_value >= 6.0:
            return {
                "active": True,
                "level": "elevated",
                "message": "Beban cukup tinggi",
                "current": current_value,
            }
        return {
            "active": False,
            "level": "normal",
            "message": "",
            "current": current_value,
        }

    def _warning_popup_title(self, level: str):
        """Menghasilkan judul popup warning sesuai tingkat bahayanya."""
        return {
            "elevated": "Socket Load Warning",
            "high": "Socket Load Warning",
            "critical": "Socket Load Critical",
        }.get(level, "Socket Load Warning")

    def _show_socket_warning_popup(self, socket_number: int):
        """Menampilkan popup warning arus berlebih untuk socket tertentu."""
        state = self.socket_load_warnings.get(socket_number, {})
        if not state.get("active") or state.get("popup_open"):
            return

        title = self._warning_popup_title(state.get("level", "high"))
        text = (
            f"Smart Socket {socket_number}\n"
            f"Current: {float(state.get('current', 0.0)):.3f} A\n"
            f"{state.get('message', '')}"
        )
        state["last_popup_at"] = time.time()
        state["popup_open"] = True
        show_styled_warning(self, title, text)
        state["popup_open"] = False

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
            if current_state.get("active") or current_state.get("current", 0.0) != 0.0:
                self.socket_load_warnings[socket_number] = {
                    **new_state,
                    "acknowledged": False,
                    "last_popup_at": 0.0,
                    "popup_open": False,
                }
                self.socket_warning_state_changed.emit(socket_number)
            return

        acknowledged = False if changed else bool(current_state.get("acknowledged", False))
        last_popup_at = 0.0 if changed else float(current_state.get("last_popup_at", 0.0) or 0.0)
        popup_open = bool(current_state.get("popup_open", False))
        self.socket_load_warnings[socket_number] = {
            **new_state,
            "acknowledged": acknowledged,
            "last_popup_at": last_popup_at,
            "popup_open": popup_open,
        }
        self.socket_warning_state_changed.emit(socket_number)

        should_popup = (
            not acknowledged and
            not popup_open and (
                changed or
                (time.time() - last_popup_at) >= 30.0
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
                switch.blockSignals(True)
                switch.setOn(state)
                switch.blockSignals(False)

            # Perbarui label status relay.
            label = getattr(self.ui, f"label_switch_status_value{socket_number}", None)
            if label:
                label.setText("ON" if state else "OFF")
                label.setProperty("state", "on" if state else "off")
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
                voltage_label.setText(f"Voltage: {display_data.get('voltage', 0):.1f} V")
            if current_label:
                current_label.setText(f"Current: {display_data.get('current', 0):.3f} A")
            if power_label:
                power_label.setText(f"Power: {display_data.get('power', 0):.1f} W")
            if energy_label:
                energy_label.setText(f"Energy: {display_data.get('energy', 0):.3f} kWh")
            if freq_label:
                freq_label.setText(f"Frequency: {display_data.get('frequency', 0):.1f} Hz")
            if pf_label:
                pf_label.setText(f"PF: {display_data.get('pf', 0):.2f}")
        else:
            # Tampilkan "--" saat relay OFF
            self._update_socket_warning_state(socket_number, 0.0, False)
            if voltage_label:
                voltage_label.setText("Voltage: -- V")
            if current_label:
                current_label.setText("Current: -- A")
            if power_label:
                power_label.setText("Power: -- W")
            if energy_label:
                energy_label.setText("Energy: -- kWh")
            if freq_label:
                freq_label.setText("Frequency: -- Hz")
            if pf_label:
                pf_label.setText("PF: --")

    def _clear_socket_energy_labels(self, socket_number: int):
        """Mengosongkan tampilan label energi saat relay socket mati."""
        voltage_label = getattr(self.ui, f"label_voltage{socket_number}", None)
        current_label = getattr(self.ui, f"label_current{socket_number}", None)
        power_label = getattr(self.ui, f"label_power{socket_number}", None)
        energy_label = getattr(self.ui, f"label_energy{socket_number}", None)
        freq_label = getattr(self.ui, f"label_frequency{socket_number}", None)
        pf_label = getattr(self.ui, f"label_powerfactor{socket_number}", None)

        if voltage_label:
            voltage_label.setText("Voltage: -- V")
        if current_label:
            current_label.setText("Current: -- A")
        if power_label:
            power_label.setText("Power: -- W")
        if energy_label:
            energy_label.setText("Energy: -- kWh")
        if freq_label:
            freq_label.setText("Frequency: -- Hz")
        if pf_label:
            pf_label.setText("PF: --")

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
                        label.setText(f"Active: {display_time}")
                    else:
                        # Tampilkan dalam detik
                        label.setText(f"Active: {remaining_seconds}s")

                    # Jangan ubah warna - biarkan stylesheet asli
                except ValueError:
                    label.setText(status)
            elif status == "INACTIVE":
                label.setText("Inactive")
            else:
                label.setText(status)

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
                self.start_socket_recording(socket_number, source="schedule")
            elif (
                self.smartsocket_recorder.is_follow_schedule(socket_number)
                and status == "STOP_TRIGGER"
            ):
                self.stop_socket_recording(socket_number, source="schedule")

                # Lakukan autosave saat recording berbasis jadwal selesai,
                # karena user bisa saja tidak sedang melihat popup socket.
                try:
                    if self.smartsocket_recorder.is_autosave_enabled(socket_number):
                        autosave_dir = self.smartsocket_recorder.get_autosave_dir(socket_number)
                        if autosave_dir:
                            records = self.smartsocket_recorder.get_records(socket_number)
                            if records:
                                os.makedirs(autosave_dir, exist_ok=True)
                                filename = (
                                    f"smartsocket_{socket_number}_schedule_"
                                    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                                )
                                path = os.path.join(autosave_dir, filename)
                                count = self.export_socket_records_csv(socket_number, path)
                                self.log(f"[Socket {socket_number}] Autosaved {count} rows to {path}")
                        else:
                            self.log(f"[Socket {socket_number}] Autosave enabled but no folder set")
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
            label.setText("Status Device: Online" if online else "Status Device: Offline")
            label.setProperty("state", "on" if online else "off")
            label.style().polish(label)

    def sync_ui_from_mqtt(self):
        """Menyinkronkan UI awal dengan state backend setelah koneksi aktif."""
        # Sinkronkan status lampu.
        self.update_lamp_ui_from_state()

        # Sinkronkan status AC.
        self.update_ac_ui_from_state()

        # Inisialisasi label energi Smart Socket ke "--".
        for i in range(1, 6):
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
