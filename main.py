import sys,random,os
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
from ui_mainwindow import Ui_MainWindow
from ui_functions import UIFunctions

# Import Session Manager dan Auth Service untuk user features
from session_manager import SessionManager
from auth_service import TrialLoginService

# Import Theme Helper untuk styled message boxes
from ui_theme_helper import (
    show_styled_information,
    show_styled_warning,
    show_styled_critical,
    show_styled_question
)

from lamp_setup import LampSetup
from switch_setup import SwitchSetup
from ac_setup import ACSetup
from arrow_setup import ArrowSetup
from smartsocket_popup import SmartSocketPopup
from smartsocket_setup import SmartSocketSetup

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
# MQTT TLS CONFIGURATION
# ============================================================
MQTT_BROKER = "DESKTOP-CVPE153"
# MQTT_BROKER = "10.33.11.148"
MQTT_PORT = 8883  # TLS Port (8883) atau Plain MQTT (1883)
MQTT_USERNAME = "dashboard"
MQTT_PASSWORD = "ecolab321"
# MQTT_CA_CERT = os.path.join(os.path.dirname(__file__), "credentials", "ca.crt")
MQTT_CA_CERT = os.path.join(os.path.dirname(__file__), "credentials", "ca2.crt")
MQTT_USE_TLS = True  # Set False untuk plain MQTT (testing)

# Class untuk mengatur Hari dan Waktu
class Date:
    def update_time(self, label: QLabel):
        current_time = QDateTime.currentDateTime()

        time_text = current_time.toString("HH:mm")
        date_text = current_time.toString("dddd, dd MMMM yyyy")

        label.setText(QCoreApplication.translate("MainWindow", f"{time_text} - {date_text}", None))
        
# Main Window
class MainWindow(QMainWindow):
    # Signal untuk notify launcher saat logout terjadi
    logout_signal = Signal()

    # APP VERSION
    APP_VERSION = "v2.0"

    def __init__(self, user_session=None):
        super().__init__()

        # Simpan user session
        self.user_session = user_session

        # SETUP UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Method untuk inisialisasi GUI yang saat aplikasi berjalan.
        self.initUI()

        # Set version label
        self.set_app_version(self.APP_VERSION)

        self.ui.logPlainEdit.setReadOnly(True)
        self._weather_initial_fetched = False

        # SETUP UI COMPONENTS (Lamp, AC, Arrow) FIRST
        LampSetup.setup(self.ui, self)
        ACSetup.setup(self.ui, self)
        ArrowSetup.setup(self.ui, self)

        # SETUP SWITCH BUTTONS
        SwitchSetup.setup(self.ui, self)

        # Setup user features (Settings page)
        if self.user_session:
            self.setup_user_features()

        # SETUP SMART SOCKET (Backend akan di-connect setelah MQTT start)
        QTimer.singleShot(1000, lambda: SmartSocketSetup.setup(self))

        # BACKEND: GROWATT
        self.growatt = GrowattBackend()
        self.growatt_worker = None
        self._last_growatt_data = None
        self.start_growatt_worker()

        # BACKEND: WEATHER CLOUD
        self.weather = WeatherCloudBackend("5476957392")

        # MQTT CORE & BACKEND (with TLS support)
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

        self.lampbutton_backend = LampButtonBackend(self.mqtt, logger=self.log)
        self.lampbutton_backend.status_changed.connect(self._on_lamp_status_changed)
        self.acbutton_backend = ACButtonBackend(self.mqtt, logger=self.log)
        self.acbutton_backend.status_changed.connect(self._on_ac_status_changed)

        # BACKEND: SMART SOCKET
        self.smartsocket_manager = SmartSocketManager(self.mqtt, logger=self.log)
        self.smartsocket_manager.start()

        # Simpan format timer per socket untuk display
        self.socket_timer_formats = {}  # {socket_number: "hms" atau "seconds"}

        # Setup SmartSocket langsung (tanpa delay)
        SmartSocketSetup.setup(self)
        QTimer.singleShot(500, self.sync_ui_from_mqtt)


        # ROOT & BODY LAYOUT
        for w in [self.ui.styleSheet, self.ui.bgApp]:
            w.setContentsMargins(0, 0, 0, 0)
            if w.layout():
                w.layout().setContentsMargins(0, 0, 0, 0)
                w.layout().setSpacing(0)

        self.ui.contentTopBg.setContentsMargins(0, 0, 0, 0)

        # WINDOW SETTINGS (FRAMELESS)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # DATE & CLOCK TIMER
        self.date_helper = Date()
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            lambda: self.date_helper.update_time(self.ui.clockInfo)
        )
        self.timer.start(1000)

        # UI FUNCTIONS & WINDOW BUTTONS
        self.ui_functions = UIFunctions(self)

        self.ui.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.ui.maximizeRestoreAppBtn.clicked.connect(
            self.ui_functions.toggle_max_restore
        )
        self.ui.closeAppBtn.clicked.connect(self.close)
        self.ui.btn_exit.clicked.connect(self.close)

        # DRAG TITLE BAR
        self.ui.contentTopBg.mousePressEvent = self.ui_functions.mouse_press
        self.ui.contentTopBg.mouseMoveEvent = self.ui_functions.mouse_move
        self.ui.contentTopBg.mouseDoubleClickEvent = (
            self.ui_functions.mouse_double_click
        )

        # SEMENTARA: DRAG BG APP (seluruh background)
        self.ui.bgApp.mousePressEvent = self.ui_functions.mouse_press
        self.ui.bgApp.mouseMoveEvent = self.ui_functions.mouse_move
        self.ui.bgApp.mouseDoubleClickEvent = self.ui_functions.mouse_double_click

        # TOGGLE LEFT MENU
        self.ui.toggleButton.clicked.connect(
            lambda: self.ui_functions.toggle_left_menu(self.ui.leftMenuBg)
        )

        # STACKED WIDGET NAVIGATION
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

        # Smart Socket Action Buttons - Open Popup Control
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
        # FLOW INFO POPUP (Growatt)
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
        # DHT INFO POPUP (Sensor Info)
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

        # Set click handler untuk titleIndoor
        self.ui.titleIndoor.mousePressEvent = self.show_dht_popup



        # Disable input IP & add button (belum digunakan)
        # self.ui.inputIP.setEnabled(False)
        # self.ui.btn_add.setEnabled(False)
        
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

        # MCU STATUS BACKEND & TIMER
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

        # SHOW WINDOW
        self.show()
        
    def show_flow_popup(self, event):
        # posisikan popup di bawah titleFlow
        pos = self.ui.titleFlow.mapToGlobal(
            self.ui.titleFlow.rect().bottomLeft()
        )
        self.flowInfoPopup.move(pos)
        self.flowInfoPopup.show()

    def show_dht_popup(self, event):
        """Show DHT popup di bawah titleIndoor"""
        pos = self.ui.titleIndoor.mapToGlobal(
            self.ui.titleIndoor.rect().bottomLeft()
        )
        self.dhtInfoPopup.move(pos)
        self.dhtInfoPopup.show()

    def update_dht_popup(self, data):
        """Update DHT info popup dengan data terbaru"""
        def fmt(val, unit=""):
            if val is None:
                return "--"
            return f"{val}{unit}"

        # Update source info
        temp_source = data.get("temp_source", "--")
        hum_source = data.get("hum_source", "--")

        self.lblDHTSourceTemp.setText(f"Sumber Suhu: {fmt(temp_source)}")
        self.lblDHTSourceHum.setText(f"Sumber Kelembaban: {fmt(hum_source)}")

        # Update MCU A data
        self.lblDHTTempA.setText(f"MCU A Suhu: {fmt(data.get('temp_A'), ' °C')}")
        self.lblDHTHumA.setText(f"MCU A Kelembaban: {fmt(data.get('hum_A'), ' %')}")

        # Update MCU B data
        self.lblDHTTempB.setText(f"MCU B Suhu: {fmt(data.get('temp_B'), ' °C')}")
        self.lblDHTHumB.setText(f"MCU B Kelembaban: {fmt(data.get('hum_B'), ' %')}")

        # Update average
        avg_temp = data.get("avg_temperature")
        avg_hum = data.get("avg_humidity")
        self.lblDHTAvgTemp.setText(f"Rata-rata Suhu: {fmt(avg_temp, ' °C')}")
        self.lblDHTAvgHum.setText(f"Rata-rata Kelembaban: {fmt(avg_hum, ' %')}")


    def update_flow_popup(self, flow):
        if not flow:
            return

        def fmt(val, unit="", dec=1):
            if val is None:
                return "--"
            return f"{val:.{dec}f}{unit}"

        def fmt_int(val, unit=""):
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

        
    def update_growatt_ui(self, data: dict):
        if not data:
            return

        # skip kalau data sama
        if data == self._last_growatt_data:
            return
        
        self.ui.currentpvpower_value.setText(f"PV Power: {data['pv_power']}W")
        self.ui.currentimportgrid_value.setText(f"{data['grid_import_power']}W")
        self.ui.currentconsumppower_value.setText(f"{data['load_power']}W//{data['rateVA_power']}VA")
        self.ui.currentsocbat_value.setText(f"SoC Battery：{data['soc']}%")
        self.ui.pvtoday_value.setText(f"{data['pv_today']}")
        self.ui.pvtotal_value.setText(f"{data['pv_total']}")
        self.ui.loadtoday_value.setText(f"{data['load_today']}")
        self.ui.loadtotal_value.setText(f"{data['load_total']}")
        self.ui.chargingtotal_value.setText(f"{data['battery_charge_total']}")
        self.ui.dischargingtoday_value.setText(f"{data['battery_discharge_today']}")
        self.ui.dischargingtotal_value.setText(f"{data['battery_discharge_total']}")
        self.ui.imporgridttotal_value.setText(f"{data['grid_total']}")
        
        # self.ui.chargingtoday_value.setText(f"{data['battery_charge_today']}")
        # self.ui.imporgridttoday_value.setText(f"{data['grid_today']}")
        
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

                        
        # ARROW
        self.arrows["pv"].set_active(data["pv_power"] > 0)
        self.arrows["grid"].set_active(data["grid_import_power"] > 0)
        self.arrows["load"].set_active(data["load_power"] > 0)
        
        self.log("[Growatt] Data updated")
        
        self.update_flow_popup(data.get("flow_info"))


    @staticmethod
    def deg_to_compass(deg: float) -> str:
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
        data = self.dht.fetch()

        avg_temp = data.get("avg_temperature")
        avg_hum = data.get("avg_humidity")

        # ===== DETEKSI DATA PERTAMA =====
        if not hasattr(self, "_dht_initialized"):
            if avg_temp is not None or avg_hum is not None:
                self._dht_initialized = True
                self.log("[DHT] Data pertama diterima dari MQTT")
            else:
                return
        # ===============================

        # Update suhu
        if avg_temp is not None:
            if avg_temp != getattr(self, "_last_dht_temp", None):
                self.ui.tempIndoor_value.setText(f"{avg_temp:.1f} °C")
                self._last_dht_temp = avg_temp

        # Update kelembaban
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

        # Update DHT info popup
        self.update_dht_popup(data)


    def publish_lamp(self, lamp_index: int, state: bool):
        # self.lampbutton_backend.set_lamp(lamp_index, state)
        self.lampbutton_backend.publish(lamp_index, state)
        self.log(f"Lamp {lamp_index}: {state}")

    def publish_ac_power(self, state: bool):
        self.acbutton_backend.power(state)
        print(f"AC Power: {state}")
        self.log(f"AC Power: {state}")

    def on_switch_toggled(self, switch_index: int, state: bool):
        """Handler saat switch button ditekan"""
        # print(f"[DEBUG] Switch {switch_index} toggled: {state}")  # Debug print
        self.log(f"Switch {switch_index}: {'ON' if state else 'OFF'}")

        # Debug: Cek apakah socket_backends ada
        # print(f"[DEBUG] hasattr(self, 'socket_backends'): {hasattr(self, 'socket_backends')}")
        if hasattr(self, 'socket_backends'):
            # print(f"[DEBUG] socket_backends: {self.socket_backends}")
            # print(f"[DEBUG] switch_index {switch_index} in socket_backends: {switch_index in self.socket_backends}")
            pass

        # Kirim command ke SmartSocket backend
        if hasattr(self, 'socket_backends') and switch_index in self.socket_backends:
            backend = self.socket_backends[switch_index]
            # print(f"[DEBUG] Backend found: {backend}")  # Debug print
            backend.set_relay(state)
            self.log(f"[Socket {switch_index}] Relay command sent: {state}")
        else:
            # print(f"[DEBUG] Backend NOT found!")  # Debug print
            self.log(f"[WARNING] Socket {switch_index} backend not ready yet!")
            # Tampilkan pesan ke user yang lebih jelas
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
        self.acbutton_backend.temp_up()

    def ac_temp_down(self):
        self.acbutton_backend.temp_down()

    def ac_mode_cool(self):
        self.acbutton_backend.mode_cool()

    def ac_mode_fan(self):
        self.acbutton_backend.mode_fan()
        
    def log(self, message: str):
        QTimer.singleShot(0, lambda: self._append_log(message))

    def _append_log(self, message: str):
        time = QDateTime.currentDateTime().toString("HH:mm:ss")
        self.ui.logPlainEdit.appendPlainText(f"[{time}] {message}")
        self.ui.logPlainEdit.verticalScrollBar().setValue(
            self.ui.logPlainEdit.verticalScrollBar().maximum()
        )

    def start_growatt_worker(self):
        if self.growatt_worker and self.growatt_worker.isRunning():
            return

        self.growatt_worker = GrowattWorker(self.growatt)
        self.growatt_worker.data_ready.connect(self.update_growatt_ui)
        self.growatt_worker.error.connect(
            lambda err: self.log(f"[Growatt ERROR] {err}")
        )
        self.growatt_worker.start()
        
    def update_mcu_status_ui(self):
        status = self.mcu_status.fetch()

        # Cek apakah guest mode - JANGAN override guest settings!
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

            # Hanya update enabled state jika BUKAN guest mode
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

            # Hanya update enabled state jika BUKAN guest mode
            if not is_guest:
                for btn in self.ac_buttons:
                    btn.setEnabled(statemcuB)
    
    def update_temp_style(self, temperature, frame, title):
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

    def initUI(self):
        """Pengaturan Awal GUI"""
        # Mengatur Judul Aplikasi
        self.setWindowTitle("EcoLab Dashboard")

        # Mengatur Icon Aplikasi
        pixmap = QPixmap(self.resource_path("icon\\logoecolab.ico"))
        icon = QIcon(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setWindowIcon(icon)

    def set_app_version(self, version: str):
        """Set version label di bottom bar"""
        self.ui.version.setText(version)

    def get_app_version(self) -> str:
        """Get current app version"""
        return self.APP_VERSION
        
    def resource_path(self, relative_path):
        """ Mengonversi path relatif menjadi path absolut.
        Berguna untuk memastikan file dapat ditemukan dari
        direktori aplikasi saat ini.
        """
        base_path = os.path.abspath(".")  # Mengatur ke directory saat ini.
        return os.path.join(base_path, relative_path)

    # ===============================
    # USER FEATURES (Settings Page)
    # ===============================
    def setup_user_features(self):
        """Setup user features di Settings page"""
        if not self.user_session:
            return

        # 1. Load user profile data
        self.load_user_profile()

        # 2. Cek role dan auth provider
        user_role = self.user_session.get("role", "user")
        auth_provider = self.user_session.get("auth_provider", "email")

        is_guest = user_role == "guest"
        is_admin = user_role == "admin"
        is_google = auth_provider == "google"

        # 3. Setup tombol Admin Panel
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

        # 4. Setup tombol Update Password
        if is_guest or is_google:
            # GUEST atau GOOGLE: Disable tombol Update Password
            self.ui.btnUpdatePassword.setEnabled(False)
            if is_guest:
                self.ui.btnUpdatePassword.setToolTip("Not available in Guest Mode")
            else:  # is_google
                self.ui.btnUpdatePassword.setToolTip("Managed by Google authentication")
        else:
            # REGULAR USER & ADMIN: Enable dan connect tombol Update Password
            self.ui.btnUpdatePassword.setEnabled(True)
            self.ui.btnUpdatePassword.setToolTip("")
            self.ui.btnUpdatePassword.clicked.connect(self.handle_update_password)

        # 5. Setup tombol Logout
        if is_guest:
            # GUEST: Disable tombol Logout
            self.ui.btnLogout.setEnabled(False)
            self.ui.btnLogout.setToolTip("Cannot logout from Guest Mode")
        else:
            # REGULAR USER & ADMIN (termasuk Google): Enable tombol Logout
            self.ui.btnLogout.setEnabled(True)
            self.ui.btnLogout.setToolTip("")
            self.ui.btnLogout.clicked.connect(self.handle_logout)

        # 6. Setup kontrol devices (Smart Socket, Lampu, AC)
        self.setup_device_controls(is_guest)

    def setup_device_controls(self, is_guest):
        """Setup device controls berdasarkan user role (guest atau bukan)"""
        if is_guest:
            # GUEST: Disable semua kontrol devices (read-only mode)

            # === SMART SOCKET ACTION BUTTONS ===
            for i in range(1, 6):
                action_btn = getattr(self.ui, f"btn_action_socket{i}", None)
                if action_btn:
                    action_btn.setEnabled(False)
                    # Custom widget SmartSocketActionButton akan otomatis
                    # set style redup via setEnabled() override
                    action_btn.setToolTip("Not available in Guest Mode (Read-only)")

            # === SMART SOCKET SWITCH BUTTONS ===
            if hasattr(self, 'switches'):
                for switch in self.switches:
                    switch.setEnabled(False)
                    switch.setToolTip("Not available in Guest Mode (Read-only)")

            # === LAMP BUTTONS ===
            if hasattr(self, 'lamps'):
                for lamp in self.lamps:
                    lamp.setEnabled(False)
                    lamp.setToolTip("Not available in Guest Mode (Read-only)")

            # === AC BUTTON ===
            if hasattr(self, 'ac_button'):
                self.ac_button.setEnabled(False)
                self.ac_button.setToolTip("Not available in Guest Mode (Read-only)")

            # === AC CONTROL BUTTONS ===
            ac_control_buttons = ['btn_temp_up', 'btn_temp_down', 'btn_cool_ac', 'btn_fan_ac']
            for btn_name in ac_control_buttons:
                btn = getattr(self.ui, btn_name, None)
                if btn:
                    btn.setEnabled(False)
                    btn.setToolTip("Not available in Guest Mode (Read-only)")
        else:
            # USER & ADMIN: Enable semua kontrol devices
            # Smart Socket Action Buttons
            for i in range(1, 6):
                action_btn = getattr(self.ui, f"btn_action_socket{i}", None)
                if action_btn:
                    action_btn.setEnabled(True)
                    # Custom widget akan otomatis menghapus opacity via paintEvent saat enabled
                    action_btn.setToolTip("")

            # Smart Socket Switch Buttons
            if hasattr(self, 'switches'):
                for switch in self.switches:
                    switch.setEnabled(True)
                    switch.setToolTip("")

            # Lamp Buttons
            if hasattr(self, 'lamps'):
                for lamp in self.lamps:
                    # Lamp 4 tetap disabled (sesuai setup awal)
                    if lamp != self.lamps[3]:  # Index 3 adalah Lamp 4
                        lamp.setEnabled(True)
                    lamp.setToolTip("")

            # AC Button
            if hasattr(self, 'ac_button'):
                self.ac_button.setEnabled(True)
                self.ac_button.setToolTip("")

            # === AC CONTROL BUTTONS ===
            ac_control_buttons = ['btn_temp_up', 'btn_temp_down', 'btn_cool_ac', 'btn_fan_ac']
            for btn_name in ac_control_buttons:
                btn = getattr(self.ui, btn_name, None)
                if btn:
                    btn.setEnabled(True)
                    btn.setToolTip("")

    def load_user_profile(self):
        """Load username dan email ke Settings page"""
        if self.user_session:
            # Set username dan email ke input fields
            self.ui.inputUsername.setText(self.user_session.get("username", ""))
            self.ui.inputEmail.setText(self.user_session.get("email", ""))

            # Cek apakah guest mode
            is_guest = self.user_session.get("role") == "guest"

            # Set read-only untuk guest mode (styling lewat Qt Designer)
            self.ui.inputUsername.setReadOnly(is_guest)
            self.ui.inputEmail.setReadOnly(is_guest)

    def handle_update_password(self):
        """Handle tombol Update Password diklik"""
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

            # Update password via Firebase
            try:
                from auth_service import TrialLoginService
                auth_service = TrialLoginService()

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
        """Handle tombol Logout diklik"""
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
        """Handle tombol Admin Panel diklik"""
        try:
            from admin_window import AdminPanelWindow

            # Buka admin panel window
            self.admin_panel_window = AdminPanelWindow(self)
            self.admin_panel_window.show()

        except Exception as e:
            show_styled_critical(
                self,
                "Error",
                f"❌ Failed to open Admin Panel:\n{str(e)}"
            )

    def open_smartsocket_popup(self, socket_number):
        """Buka popup kontrol Smart Socket - Cegah popup ganda"""
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
        """Setup fitur admin (buka admin panel)"""
        # Tombol Admin Panel sudah di-setup di setup_user_features()
        pass
    def _on_lamp_status_changed(self, lamp_index: int, state: bool):
        """Callback saat status lamp berubah dari MQTT"""
        # Update UI untuk lamp yang berubah saja
        if 1 <= lamp_index <= len(self.lamps):
            lamp = self.lamps[lamp_index - 1]
            lamp.blockSignals(True)
            lamp.setChecked(state)
            lamp.blockSignals(False)

    def update_lamp_ui_from_state(self):
        for idx, lamp in enumerate(self.lamps, start=1):
            state = self.lampbutton_backend.states.get(idx)
            if state is not None:
                lamp.blockSignals(True)
                lamp.setChecked(state)   # ✅ BENAR
                lamp.blockSignals(False)

    def _on_ac_status_changed(self, state: bool):
        """Callback saat status AC berubah dari MQTT"""
        # Update UI AC button
        self.ac_button.blockSignals(True)
        self.ac_button.setChecked(state)
        self.ac_button.blockSignals(False)

        # Update AC status label jika ada
        if hasattr(self, "update_ac_status"):
            self.update_ac_status(state)

    def update_ac_ui_from_state(self):
        state = self.acbutton_backend.state
        if state is not None:
            self.ac_button.blockSignals(True)
            self.ac_button.setChecked(state)
            self.ac_button.blockSignals(False)

            # 🔥 TAMBAHAN WAJIB
            if hasattr(self, "update_ac_status"):
                self.update_ac_status(state)

    # ================= SMART SOCKET HANDLERS =================
    def _on_socket_relay_status(self, socket_number: int, state: bool):
        """Update relay status UI untuk Smart Socket"""
        if 1 <= socket_number <= 5:
            # Update switch button state
            if socket_number <= len(self.switches):
                switch = self.switches[socket_number - 1]
                switch.blockSignals(True)
                switch.setOn(state)
                switch.blockSignals(False)

            # Update label status
            label = getattr(self.ui, f"label_switch_status_value{socket_number}", None)
            if label:
                label.setText("ON" if state else "OFF")
                label.setProperty("state", "on" if state else "off")
                label.style().polish(label)

            # Clear energy labels saat relay OFF
            if not state:
                self._clear_socket_energy_labels(socket_number)

    def _on_socket_energy_data(self, socket_number: int, data: dict):
        """Update energy data UI untuk Smart Socket - Hanya saat relay ON"""
        if not data:
            return

        # Cek status relay dari switch button
        if socket_number <= len(self.switches):
            relay_on = self.switches[socket_number - 1].isOn()
        else:
            relay_on = False

        # Get labels for this socket
        voltage_label = getattr(self.ui, f"label_voltage{socket_number}", None)
        current_label = getattr(self.ui, f"label_current{socket_number}", None)
        power_label = getattr(self.ui, f"label_power{socket_number}", None)
        energy_label = getattr(self.ui, f"label_energy{socket_number}", None)
        freq_label = getattr(self.ui, f"label_frequency{socket_number}", None)
        pf_label = getattr(self.ui, f"label_powerfactor{socket_number}", None)

        # Update labels HANYA saat relay ON
        if relay_on:
            if voltage_label:
                voltage_label.setText(f"Voltage: {data.get('voltage', 0):.1f} V")
            if current_label:
                current_label.setText(f"Current: {data.get('current', 0):.3f} A")
            if power_label:
                power_label.setText(f"Power: {data.get('power', 0):.1f} W")
            if energy_label:
                energy_label.setText(f"Energy: {data.get('energy', 0):.3f} kWh")
            if freq_label:
                freq_label.setText(f"Frequency: {data.get('frequency', 0):.1f} Hz")
            if pf_label:
                pf_label.setText(f"PF: {data.get('pf', 0):.2f}")
        else:
            # Tampilkan "--" saat relay OFF
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
        """Clear energy labels saat relay OFF"""
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
        """Update timer status UI untuk Smart Socket"""
        label = getattr(self.ui, f"label_timer_status{socket_number}", None)
        if label:
            # Parse status dari backend: "ACTIVE:XXs" atau "INACTIVE"
            if status.startswith("ACTIVE:"):
                # Extract detik
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
        """Update schedule status UI untuk Smart Socket"""
        import json

        # DEBUG: Print raw status dari hardware
        # print(f"[DEBUG Schedule UI] Socket {socket_number} received: {repr(status)}")

        try:
            data = json.loads(status)
            mode = data.get("mode", "N/A")
            start = data.get("start", "N/A")
            stop = data.get("stop", "N/A")

            # DEBUG: Print parsed data
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
        """Update device status UI untuk Smart Socket"""
        label = getattr(self.ui, f"statussocket{socket_number}", None)
        if label:
            label.setText("Status Device: Online" if online else "Status Device: Offline")
            label.setProperty("state", "on" if online else "off")
            label.style().polish(label)

    def sync_ui_from_mqtt(self):
        # sinkron lampu
        self.update_lamp_ui_from_state()

        # sinkron AC
        self.update_ac_ui_from_state()

        # Initialize Smart Socket energy labels to "--"
        for i in range(1, 6):
            self._clear_socket_energy_labels(i)

    def _safe_energy_value(self, value, max_limit=100000):
        """
        Convert value to float safely.
        Jika invalid / terlalu besar -> return 0
        """
        try:
            val = float(value)

            # jika nilai terlalu besar (bug device)
            if abs(val) > max_limit:
                return 0

            return round(val, 2)

        except (ValueError, TypeError):
            return 0
                    
# Run Application Mantap Sekali 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
