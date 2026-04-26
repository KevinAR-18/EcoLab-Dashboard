from datetime import datetime

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QTimer, QSize, QDateTime, QPoint
from PySide6.QtGui import (
    QColor,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRegion,
    QIntValidator,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QDialog,
    QProxyStyle,
    QStyle,
)
from ui_smartsocket_popup import Ui_SmartSocketPopup
from ui_theme_helper import apply_light_theme_to_widget


class _ComboArrowStyle(QProxyStyle):
    """Draw a consistent down-arrow regardless of Windows dark mode/palette."""

    ARROW_COLOR = QColor("#005C99")

    def drawComplexControl(self, control, option, painter, widget=None):
        super().drawComplexControl(control, option, painter, widget)

        if control != QStyle.ComplexControl.CC_ComboBox or painter is None:
            return

        try:
            arrow_rect = self.subControlRect(
                QStyle.ComplexControl.CC_ComboBox,
                option,
                QStyle.SubControl.SC_ComboBoxArrow,
                widget,
            )
        except Exception:
            return

        r = arrow_rect.adjusted(0, 0, -1, -1)
        if r.width() <= 6 or r.height() <= 6:
            return

        w = max(8, min(r.width() - 8, 14))
        h = max(6, min(r.height() - 8, 10))
        cx = r.center().x()
        cy = r.center().y()

        points = [
            QPoint(cx - w // 2, cy - h // 3),
            QPoint(cx + w // 2, cy - h // 3),
            QPoint(cx, cy + h // 2),
        ]

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.ARROW_COLOR)
        painter.drawPolygon(points)
        painter.restore()

    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PrimitiveElement.PE_IndicatorArrowDown:
            if painter is None:
                return

            r = option.rect
            # Draw a filled triangle centered in rect
            w = max(6, min(r.width(), 12))
            h = max(4, min(r.height(), 8))
            cx = r.center().x()
            cy = r.center().y()

            points = [
                QPoint(cx - w // 2, cy - h // 2),
                QPoint(cx + w // 2, cy - h // 2),
                QPoint(cx, cy + h // 2),
            ]

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.ARROW_COLOR)
            painter.drawPolygon(points)
            painter.restore()
            return

        super().drawPrimitive(element, option, painter, widget)


class SmartSocketPopup(QDialog, Ui_SmartSocketPopup):
    TABLE_DISPLAY_LIMIT = 500
    CHART_POINT_LIMIT = 300
    WINDOW_RADIUS_PX = 10
    WINDOW_WIDTH_PX = 1024
    WINDOW_HEIGHT_PX = 650

    def __init__(self, socket_number, backend, main_window, parent=None):
        super().__init__(parent)
        self.socket_number = socket_number
        self.backend = backend  # SmartSocketBackend instance
        self.main_window = main_window  # Reference ke MainWindow untuk simpan format
        self.setupUi(self)

        # Ensure dropdown arrows are visible even under Windows 11 dark mode.
        for combo in self.findChildren(QComboBox):
            combo.setStyle(_ComboArrowStyle(combo.style()))

        # Override the .ui fixed size so Data tab buttons don't get clipped.
        self.setMinimumSize(QSize(self.WINDOW_WIDTH_PX, self.WINDOW_HEIGHT_PX))
        self.setMaximumSize(QSize(self.WINDOW_WIDTH_PX, self.WINDOW_HEIGHT_PX))

        # Match app icon (used in Login/Main window).
        try:
            pixmap = QPixmap(self.main_window.resource_path("icon\\logoecolab.ico"))
            if not pixmap.isNull():
                icon = QIcon(
                    pixmap.scaled(
                        64,
                        64,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                self.setWindowIcon(icon)
        except Exception:
            pass

        # Set borderless window with rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Needed for true rounded corners on a frameless window.
        # Without this, the stylesheet may look rounded but the native window
        # surface is still rectangular (corners look "siku-siku").
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Setup drag functionality
        self._old_pos = None

        # NOTE:
        # We draw the dialog background manually in paintEvent so the window can
        # be truly rounded (with WA_TranslucentBackground) without turning the
        # content area transparent.
        self.setStyleSheet("#SmartSocketPopup{ background: transparent; }")
        apply_light_theme_to_widget(self)

        # Set dynamic title based on socket number
        self.label_title.setText(f"⚡ Smart Socket {self.socket_number} Control")

        # Set placeholder untuk input timer
        self.input_timer_duration.setPlaceholderText("HH:MM:SS or seconds")

        # Set tooltip untuk input timer
        self.input_timer_duration.setToolTip(
            "Timer Duration Format:\n"
            "• HH:MM:SS → 01:30:00 = 1 jam 30 menit\n"
            "• MM:SS → 05:30 = 5 menit 30 detik\n"
            "• Seconds → 3600 = 3600 detik (1 jam)\n\n"
            "Examples:\n"
            "• 00:05:00 = 5 menit\n"
            "• 01:00:00 = 1 jam\n"
            "• 02:30:45 = 2 jam 30 menit 45 detik"
        )

        # Connect buttons (placeholder functions for now)
        self.connect_buttons()

        # Refresh timer harus dibuat SEBELUM refresh_monitoring_view()
        # Refresh timer hanya aktif saat recording
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_monitoring_view)
        self.refresh_timer.stop()  # Mulai dengan timer OFF

        if hasattr(self.main_window, "socket_recording_state_changed"):
            self.main_window.socket_recording_state_changed.connect(
                self._on_recording_state_changed
            )

        self._setup_monitoring_ui()
        self.refresh_monitoring_view()
        self._update_rounded_mask()

    def paintEvent(self, event):
        super().paintEvent(event)

        # Paint rounded gradient background + border.
        r = float(self.WINDOW_RADIUS_PX)
        rect = self.rect().adjusted(1, 1, -1, -1)
        if rect.width() <= 2 or rect.height() <= 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()
        path.addRoundedRect(rect, r, r)

        grad = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        grad.setColorAt(0.0, QColor("#E1F2FB"))
        grad.setColorAt(1.0, QColor("#F1F9F9"))

        painter.fillPath(path, grad)

        pen = QPen(QColor("#005C99"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPath(path)

    def _update_rounded_mask(self):
        """Make the actual window shape rounded (not only the border)."""
        r = int(self.WINDOW_RADIUS_PX)
        if r <= 0:
            self.clearMask()
            return

        rect = self.rect()
        path = QPainterPath()
        # -1 to avoid occasional 1px artifacts on the bottom/right edge
        path.addRoundedRect(rect.adjusted(0, 0, -1, -1), r, r)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_rounded_mask()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_rounded_mask()

    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self._old_pos and event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.pos() + delta)
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def closeEvent(self, event):
        if hasattr(self.main_window, "socket_recording_state_changed"):
            try:
                self.main_window.socket_recording_state_changed.disconnect(
                    self._on_recording_state_changed
                )
            except (RuntimeError, TypeError):
                pass
        super().closeEvent(event)

    def connect_buttons(self):
        """Connect all buttons to their handlers"""
        # Timer buttons
        self.btn_start_timer.clicked.connect(self.on_start_timer)
        self.btn_cancel_timer.clicked.connect(self.on_cancel_timer)

        # Schedule buttons
        self.btn_set_schedule.clicked.connect(self.on_set_schedule)
        self.btn_clear_schedule.clicked.connect(self.on_clear_schedule)

        # Close button
        self.btn_close.clicked.connect(self.accept)

    # ================= MONITORING UI =================
    def _setup_monitoring_ui(self):
        self.resize(980, 760)
        self.setMinimumSize(QSize(900, 720))
        self.setMaximumSize(QSize(1200, 900))
        self.label_title.setMinimumSize(QSize(700, 55))
        self.label_title.setMaximumSize(QSize(900, 60))

        self.verticalLayout.removeWidget(self.groupBox_timer)
        self.verticalLayout.removeWidget(self.groupBox_schedule)

        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #B0D6E8;
                border-radius: 6px;
                background: #FFFFFF;
            }
            QTabBar::tab {
                background: #D8ECF8;
                color: #1F2D3A;
                padding: 8px 18px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #005C99;
                color: white;
            }
        """)

        self.control_tab = QWidget(self.tabs)
        control_layout = QVBoxLayout(self.control_tab)
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.setSpacing(10)
        control_layout.addWidget(self.groupBox_timer)
        control_layout.addWidget(self.groupBox_schedule)
        control_layout.addStretch()

        self.data_tab = QWidget(self.tabs)
        self.graph_tab = QWidget(self.tabs)
        self._build_data_tab()
        self._build_graph_tab()

        self.tabs.addTab(self.control_tab, "Control")
        self.tabs.addTab(self.data_tab, "Data")
        self.tabs.addTab(self.graph_tab, "Graph")
        self.verticalLayout.addWidget(self.tabs)

    def _build_data_tab(self):
        layout = QVBoxLayout(self.data_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        self.data_tab.setStyleSheet("""
            QWidget {
                color: #1F2D3A;
                background: transparent;
            }
            QLabel {
                color: #1F2D3A;
                background: transparent;
            }
            QCheckBox {
                color: #1F2D3A;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #A8C7DC;
                border-radius: 4px;
                background: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background: #005C99;
                border-color: #005C99;
            }
            QLineEdit, QComboBox {
                color: #1F2D3A;
                background: #FFFFFF;
                border: 1px solid #B8D4E3;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QComboBox {
                padding-right: 28px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #B8D4E3;
                background: #F3F9FD;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox QAbstractItemView {
                color: #1F2D3A;
                background: #FFFFFF;
                selection-background-color: #005C99;
                selection-color: #FFFFFF;
                border: 1px solid #B8D4E3;
            }
        """)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("View:"))
        self.combo_data_socket = self._create_socket_combo()
        top_layout.addWidget(self.combo_data_socket)

        self.chk_follow_schedule = QCheckBox("Follow Schedule")
        self.chk_follow_schedule.setToolTip(
            "Start recording on START_TRIGGER and stop on STOP_TRIGGER."
        )
        top_layout.addWidget(self.chk_follow_schedule)

        top_layout.addWidget(QLabel("Interval (s):"))
        self.input_record_interval = QLineEdit(self.data_tab)
        self.input_record_interval.setFixedWidth(56)
        self.input_record_interval.setAlignment(Qt.AlignCenter)
        self.input_record_interval.setValidator(QIntValidator(1, 3600, self))
        self.input_record_interval.setToolTip(
            "Interval pengambilan data saat recording (detik)."
        )
        try:
            seconds = int(round(self.main_window.get_socket_record_interval_seconds(self.socket_number)))
        except Exception:
            seconds = 5
        self.input_record_interval.setText(str(max(1, seconds)))
        top_layout.addWidget(self.input_record_interval)

        self.chk_autosave = QCheckBox("Autosave")
        self.chk_autosave.setToolTip(
            "Autosave CSV when schedule recording stops (STOP_TRIGGER)."
        )
        top_layout.addWidget(self.chk_autosave)

        self.btn_autosave_folder = QPushButton("Folder...")
        self.btn_autosave_folder.setToolTip("Set autosave folder")
        self.btn_autosave_folder.setStyleSheet(self._button_style("#6B7280"))
        top_layout.addWidget(self.btn_autosave_folder)
        top_layout.addStretch()

        self.btn_start_recording = QPushButton("Start Recording")
        self.btn_stop_recording = QPushButton("Stop Recording")
        self.btn_clear_records = QPushButton("Clear Data")
        self.btn_export_csv = QPushButton("Export CSV")

        self.btn_start_recording.setStyleSheet(self._button_style("#0F8B4C"))
        self.btn_stop_recording.setStyleSheet(self._button_style("#EB5757"))
        self.btn_clear_records.setStyleSheet(self._button_style("#6B7280"))
        self.btn_export_csv.setStyleSheet(self._button_style("#005C99"))

        top_layout.addWidget(self.btn_start_recording)
        top_layout.addWidget(self.btn_stop_recording)
        top_layout.addWidget(self.btn_clear_records)
        top_layout.addWidget(self.btn_export_csv)
        layout.addLayout(top_layout)

        self.label_recording_status = QLabel("Recording: OFF")
        self.label_recording_status.setStyleSheet(
            "font-weight: 600; color: #1F2D3A;"
        )
        layout.addWidget(self.label_recording_status)

        self.table_records = QTableWidget(self.data_tab)
        self.table_records.setColumnCount(8)
        self.table_records.setHorizontalHeaderLabels([
            "Timestamp",
            "Relay",
            "Voltage",
            "Current",
            "Power",
            "Energy",
            "Frequency",
            "PF",
        ])
        self.table_records.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_records.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_records.setAlternatingRowColors(True)
        self.table_records.verticalHeader().setVisible(False)
        self.table_records.setStyleSheet("""
            QTableWidget {
                background: #F8FCFF;
                alternate-background-color: #EEF6FC;
                border: 1px solid #C7DCEC;
                border-radius: 6px;
                gridline-color: #D8E6F2;
                color: #1F2D3A;
                selection-background-color: #DCEEFF;
                selection-color: #1F2D3A;
                font-size: 10.5pt;
            }
            QHeaderView::section {
                background: #005C99;
                color: white;
                font-weight: 600;
                border: none;
                padding: 6px 8px;
            }
        """)

        header = self.table_records.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setStretchLastSection(False)

        # Timestamp menyerap sisa ruang; kolom angka dibuat stabil agar PF tidak melebar.
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        column_widths = {
            1: 78,
            2: 92,
            3: 92,
            4: 92,
            5: 92,
            6: 104,
            7: 70,
        }
        for index, width in column_widths.items():
            header.setSectionResizeMode(index, QHeaderView.Fixed)
            self.table_records.setColumnWidth(index, width)
        layout.addWidget(self.table_records)

        self.combo_data_socket.setCurrentIndex(self.socket_number - 1)
        self.combo_data_socket.currentIndexChanged.connect(
            self._on_data_socket_changed
        )
        self.chk_follow_schedule.stateChanged.connect(
            self._on_follow_schedule_changed
        )
        self.input_record_interval.editingFinished.connect(
            self._on_record_interval_changed
        )
        self.chk_autosave.stateChanged.connect(self._on_autosave_changed)
        self.btn_autosave_folder.clicked.connect(self._on_pick_autosave_folder)
        self.btn_start_recording.clicked.connect(self.on_start_recording)
        self.btn_stop_recording.clicked.connect(self.on_stop_recording)
        self.btn_clear_records.clicked.connect(self.on_clear_records)
        self.btn_export_csv.clicked.connect(self.on_export_csv)

    def _build_graph_tab(self):
        layout = QVBoxLayout(self.graph_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        self.graph_tab.setStyleSheet("""
            QWidget {
                color: #1F2D3A;
                background: transparent;
            }
            QLabel {
                color: #1F2D3A;
                background: transparent;
            }
            QComboBox {
                color: #1F2D3A;
                background: #FFFFFF;
                border: 1px solid #B8D4E3;
                border-radius: 5px;
                padding: 4px 8px;
                padding-right: 28px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #B8D4E3;
                background: #F3F9FD;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox QAbstractItemView {
                color: #1F2D3A;
                background: #FFFFFF;
                selection-background-color: #005C99;
                selection-color: #FFFFFF;
                border: 1px solid #B8D4E3;
            }
            QChartView {
                background: #FFFFFF;
                border: 1px solid #C7DCEC;
                border-radius: 6px;
            }
        """)

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Socket:"))
        self.combo_graph_socket = self._create_socket_combo()
        top_layout.addWidget(self.combo_graph_socket)
        top_layout.addWidget(QLabel("Metric:"))
        self.combo_graph_metric = QComboBox(self.graph_tab)
        for key, label in self._metric_options():
            self.combo_graph_metric.addItem(label, key)
        top_layout.addWidget(self.combo_graph_metric)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.label_graph_status = QLabel("No data")
        self.label_graph_status.setStyleSheet("font-weight: 600; color: #1F2D3A;")
        layout.addWidget(self.label_graph_status)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setBackgroundVisible(True)
        self.chart.setBackgroundBrush(QColor("#FFFFFF"))
        self.chart.setPlotAreaBackgroundVisible(True)
        self.chart.setPlotAreaBackgroundBrush(QColor("#FFFFFF"))
        self.chart.setTitleBrush(QColor("#1F2D3A"))
        self.chart_view = QChartView(self.chart, self.graph_tab)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(430)
        layout.addWidget(self.chart_view)

        self.combo_graph_socket.setCurrentIndex(self.socket_number - 1)
        self.combo_graph_socket.currentIndexChanged.connect(
            self.refresh_monitoring_view
        )
        self.combo_graph_metric.currentIndexChanged.connect(
            self.refresh_monitoring_view
        )

    def _create_socket_combo(self):
        combo = QComboBox(self)
        for socket_number in range(1, 6):
            combo.addItem(f"Smart Socket {socket_number}", socket_number)
        return combo

    def _button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 7px 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                color: #FFFFFF;
            }}
            QPushButton:pressed {{
                color: #FFFFFF;
            }}
            QPushButton:disabled {{
                background-color: #B8C2CC;
                color: #F8FAFC;
            }}
        """

    def _metric_options(self):
        return [
            ("voltage", "Voltage"),
            ("current", "Current"),
            ("power", "Power"),
            ("energy", "Energy"),
            ("frequency", "Frequency"),
            ("pf", "PF"),
        ]

    def _metric_unit(self, metric):
        return {
            "voltage": "V",
            "current": "A",
            "power": "W",
            "energy": "kWh",
            "frequency": "Hz",
            "pf": "",
        }.get(metric, "")

    def _on_data_socket_changed(self, *_):
        socket_number = self._selected_data_socket()
        self.combo_graph_socket.blockSignals(True)
        self.combo_graph_socket.setCurrentIndex(socket_number - 1)
        self.combo_graph_socket.blockSignals(False)
        # Sync interval field to selected socket
        if hasattr(self, "input_record_interval"):
            try:
                seconds = int(round(self.main_window.get_socket_record_interval_seconds(socket_number)))
            except Exception:
                seconds = 5
            self.input_record_interval.setText(str(max(1, seconds)))
        if hasattr(self, "chk_autosave"):
            try:
                enabled = bool(self.main_window.is_socket_autosave_enabled(socket_number))
            except Exception:
                enabled = False
            self.chk_autosave.blockSignals(True)
            self.chk_autosave.setChecked(enabled)
            self.chk_autosave.blockSignals(False)
        self.refresh_monitoring_view()

    def _on_follow_schedule_changed(self, *_):
        socket_number = self._selected_data_socket()
        enabled = self.chk_follow_schedule.isChecked()
        self.main_window.set_socket_follow_schedule(socket_number, enabled)
        if enabled:
            self.main_window.start_socket_recording(socket_number, source="schedule")
        self.refresh_monitoring_view()

    def _on_record_interval_changed(self):
        socket_number = self._selected_data_socket()
        text = (self.input_record_interval.text() if hasattr(self, "input_record_interval") else "").strip()
        try:
            seconds = int(text)
        except ValueError:
            seconds = 5
        seconds = max(1, seconds)
        if hasattr(self, "input_record_interval"):
            self.input_record_interval.setText(str(seconds))

        if hasattr(self.main_window, "set_socket_record_interval_seconds"):
            self.main_window.set_socket_record_interval_seconds(socket_number, float(seconds))

        # Update refresh cadence if recording is active.
        self._update_refresh_timer_state()

    def _on_pick_autosave_folder(self):
        socket_number = self._selected_data_socket()
        try:
            current_dir = self.main_window.get_socket_autosave_dir(socket_number)
        except Exception:
            current_dir = ""

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Autosave Folder",
            current_dir or "",
        )
        if not directory:
            return

        if hasattr(self.main_window, "set_socket_autosave_dir"):
            self.main_window.set_socket_autosave_dir(socket_number, directory)
        # If user set folder, allow enabling autosave without warning
        if hasattr(self, "chk_autosave") and not self.chk_autosave.isChecked():
            self.chk_autosave.setChecked(True)

    def _on_autosave_changed(self, *_):
        socket_number = self._selected_data_socket()
        enabled = self.chk_autosave.isChecked() if hasattr(self, "chk_autosave") else False
        if enabled:
            try:
                directory = self.main_window.get_socket_autosave_dir(socket_number)
            except Exception:
                directory = ""
            if not directory:
                # Force user to pick folder first.
                self._on_pick_autosave_folder()
                try:
                    directory = self.main_window.get_socket_autosave_dir(socket_number)
                except Exception:
                    directory = ""
                if not directory:
                    self.chk_autosave.blockSignals(True)
                    self.chk_autosave.setChecked(False)
                    self.chk_autosave.blockSignals(False)
                    return

        if hasattr(self.main_window, "set_socket_autosave_enabled"):
            self.main_window.set_socket_autosave_enabled(socket_number, enabled)

    def _selected_data_socket(self):
        return self.combo_data_socket.currentData() or self.socket_number

    def _selected_graph_socket(self):
        return self.combo_graph_socket.currentData() or self.socket_number

    def _refresh_interval_ms(self):
        sockets = {self._selected_data_socket(), self._selected_graph_socket()}
        intervals = []
        for s in sockets:
            try:
                intervals.append(float(self.main_window.get_socket_record_interval_seconds(s)))
            except Exception:
                intervals.append(5.0)
        seconds = max(1.0, min(intervals) if intervals else 5.0)
        return int(seconds * 1000)

    def on_start_recording(self):
        self.main_window.start_socket_recording(self._selected_data_socket())
        self.refresh_monitoring_view()

    def on_stop_recording(self):
        self.main_window.stop_socket_recording(self._selected_data_socket())
        self.refresh_monitoring_view()

    def on_clear_records(self):
        socket_number = self._selected_data_socket()
        reply = QMessageBox.question(
            self,
            "Clear Data",
            f"Clear recorded data for Smart Socket {socket_number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.main_window.clear_socket_records(socket_number)
            self.refresh_monitoring_view()

    def on_export_csv(self):
        socket_number = self._selected_data_socket()
        records = self.main_window.get_socket_records(socket_number)
        if not records:
            QMessageBox.warning(
                self,
                "Export CSV",
                f"No recorded data for Smart Socket {socket_number}.",
            )
            return

        default_name = (
            f"smartsocket_{socket_number}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Smart Socket CSV",
            default_name,
            "CSV Files (*.csv)",
        )
        if not path:
            return
        if not path.lower().endswith(".csv"):
            path += ".csv"

        try:
            count = self.main_window.export_socket_records_csv(socket_number, path)
            QMessageBox.information(
                self,
                "Export CSV",
                f"Exported {count} rows for Smart Socket {socket_number}.",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Export CSV",
                f"Failed to export CSV:\n{exc}",
            )

    def refresh_monitoring_view(self, *_):
        if not hasattr(self.main_window, "smartsocket_recorder"):
            return

        data_socket = self._selected_data_socket()
        graph_socket = self._selected_graph_socket()

        self._refresh_recording_controls(data_socket)
        self._refresh_table(data_socket)
        self._refresh_chart(graph_socket)

    def _refresh_recording_controls(self, socket_number):
        recording = self.main_window.is_socket_recording(socket_number)
        follow_schedule = self.main_window.is_socket_follow_schedule(socket_number)
        try:
            autosave_enabled = bool(self.main_window.is_socket_autosave_enabled(socket_number))
        except Exception:
            autosave_enabled = False
        try:
            interval_seconds = int(round(self.main_window.get_socket_record_interval_seconds(socket_number)))
        except Exception:
            interval_seconds = 5
        records = self.main_window.get_socket_records(socket_number)

        self.chk_follow_schedule.blockSignals(True)
        self.chk_follow_schedule.setChecked(follow_schedule)
        self.chk_follow_schedule.blockSignals(False)

        if hasattr(self, "chk_autosave"):
            self.chk_autosave.blockSignals(True)
            self.chk_autosave.setChecked(autosave_enabled)
            self.chk_autosave.blockSignals(False)
        if hasattr(self, "input_record_interval"):
            self.input_record_interval.blockSignals(True)
            self.input_record_interval.setText(str(max(1, interval_seconds)))
            self.input_record_interval.blockSignals(False)

        self.btn_start_recording.setEnabled(not recording)
        self.btn_stop_recording.setEnabled(recording)

        recording_text = "ON" if recording else "OFF"
        follow_text = "ON" if follow_schedule else "OFF"
        shown = min(len(records), self.TABLE_DISPLAY_LIMIT)
        self.label_recording_status.setText(
            f"Smart Socket {socket_number} | Recording: {recording_text} | "
            f"Follow Schedule: {follow_text} | Rows: {len(records)} "
            f"(showing last {shown})"
        )
        self._update_refresh_timer_state()

    def _refresh_table(self, socket_number):
        records = self.main_window.get_socket_records(socket_number)
        display_records = records[-self.TABLE_DISPLAY_LIMIT:]
        self.table_records.setRowCount(len(display_records))

        for row, record in enumerate(display_records):
            values = [
                record.get("timestamp", ""),
                record.get("relay_state", ""),
                self._fmt(record.get("voltage"), 2),
                self._fmt(record.get("current"), 3),
                self._fmt(record.get("power"), 2),
                self._fmt(record.get("energy"), 3),
                self._fmt(record.get("frequency"), 1),
                self._fmt(record.get("pf"), 2),
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if col >= 2:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table_records.setItem(row, col, item)

        if display_records:
            self.table_records.scrollToBottom()

    def _refresh_chart(self, socket_number):
        records = self.main_window.get_socket_records(socket_number)
        metric = self.combo_graph_metric.currentData() or "power"
        metric_label = self.combo_graph_metric.currentText() or "Power"
        metric_unit = self._metric_unit(metric)
        axis_label = (
            f"{metric_label} ({metric_unit})" if metric_unit else metric_label
        )
        chart_records = records[-self.CHART_POINT_LIMIT:]

        self.chart.removeAllSeries()
        for axis in list(self.chart.axes()):
            self.chart.removeAxis(axis)

        self.chart.setTitle(
            f"Smart Socket {socket_number} - {axis_label} "
            f"({len(records)} rows)"
        )
        self.label_graph_status.setText(
            f"Showing last {len(chart_records)} of {len(records)} samples"
        )

        series = QLineSeries()
        series.setName(axis_label)

        values = []
        timestamps = []
        for record in chart_records:
            value = self._to_float(record.get(metric))
            values.append(value)

            # Parse timestamp string ke QDateTime
            timestamp_str = record.get("timestamp", "")
            dt = self._parse_timestamp(timestamp_str)
            if dt:
                timestamps.append(dt.toMSecsSinceEpoch())
            else:
                # Fallback: gunakan index jika timestamp invalid
                timestamps.append(len(timestamps) * 1000)

        # Plot dengan timestamp (msec since epoch)
        for i, (ts, val) in enumerate(zip(timestamps, values)):
            series.append(ts, val)

        self.chart.addSeries(series)

        # Gunakan QDateTimeAxis untuk sumbu X (waktu)
        axis_x = QDateTimeAxis()
        axis_x.setTitleText("Time")
        axis_x.setFormat("HH:mm:ss")
        axis_x.setTickCount(6)
        axis_x.setLabelsColor(QColor("#1F2D3A"))
        axis_x.setTitleBrush(QColor("#1F2D3A"))
        axis_x.setGridLineColor(QColor("#D8E6F2"))
        axis_x.setLinePenColor(QColor("#8FB7CF"))

        if timestamps:
            min_ts = min(timestamps)
            max_ts = max(timestamps)
            axis_x.setRange(QDateTime.fromMSecsSinceEpoch(min_ts),
                          QDateTime.fromMSecsSinceEpoch(max_ts))
        else:
            # Default range jika tidak ada data
            now = QDateTime.currentDateTime()
            axis_x.setRange(now.addSecs(-60), now)

        axis_y = QValueAxis()
        axis_y.setTitleText(axis_label)
        axis_y.setLabelsColor(QColor("#1F2D3A"))
        axis_y.setTitleBrush(QColor("#1F2D3A"))
        axis_y.setGridLineColor(QColor("#D8E6F2"))
        axis_y.setLinePenColor(QColor("#8FB7CF"))
        if values:
            min_value = min(values)
            max_value = max(values)
            if min_value == max_value:
                padding = abs(min_value) * 0.1 or 1.0
            else:
                padding = (max_value - min_value) * 0.1
            axis_y.setRange(min_value - padding, max_value + padding)
        else:
            axis_y.setRange(0, 1)

        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def _update_refresh_timer_state(self):
        if not hasattr(self, "refresh_timer"):
            return

        active_socket_numbers = {
            self._selected_data_socket(),
            self._selected_graph_socket(),
        }
        should_refresh = any(
            self.main_window.is_socket_recording(socket_number)
            for socket_number in active_socket_numbers
        )

        if should_refresh:
            interval_ms = self._refresh_interval_ms()
            if (not self.refresh_timer.isActive()) or (self.refresh_timer.interval() != interval_ms):
                self.refresh_timer.start(interval_ms)
        elif self.refresh_timer.isActive():
            self.refresh_timer.stop()

    def _on_recording_state_changed(self, socket_number, is_recording):
        selected_sockets = {
            self._selected_data_socket(),
            self._selected_graph_socket(),
        }
        if socket_number in selected_sockets:
            self.refresh_monitoring_view()
        else:
            self._update_refresh_timer_state()

    def _fmt(self, value, decimals):
        return f"{self._to_float(value):.{decimals}f}"

    def _parse_timestamp(self, timestamp_str):
        """
        Parse timestamp string ke QDateTime
        Format: "YYYY-MM-DD HH:MM:SS"
        """
        if not timestamp_str:
            return None

        try:
            # Parse timestamp string format: "2026-04-25 14:30:45"
            dt = QDateTime.fromString(timestamp_str, "yyyy-MM-dd HH:mm:ss")
            if dt.isValid():
                return dt
        except Exception:
            pass

        return None

    @staticmethod
    def _to_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    # ================= TIMER HANDLERS =================
    def on_start_timer(self):
        """Handle Start Timer button click"""
        duration_input = self.input_timer_duration.text().strip()

        # Cek apakah input dalam format HH:MM:SS atau hanya detik
        total_seconds = self.parse_timer_duration(duration_input)

        if total_seconds is not None and total_seconds > 0:
            # Tentukan format input
            if ':' in duration_input:
                format_type = "hms"  # Format jam:menit:detik
                display_text = f"Status: Starting {duration_input} timer..."
            else:
                format_type = "seconds"  # Format detik saja
                display_text = f"Status: Starting {total_seconds}s timer..."

            # Simpan format di main window
            if hasattr(self.main_window, 'socket_timer_formats'):
                self.main_window.socket_timer_formats[self.socket_number] = format_type

            self.label_timer_status.setText(display_text)
            self.label_timer_status.setStyleSheet("color: blue; font-weight: bold;")
            # Send MQTT command (total detik)
            self.backend.set_timer(total_seconds)
        else:
            self.label_timer_status.setText("Status: Invalid input!\nUse HH:MM:SS or seconds")
            self.label_timer_status.setStyleSheet("color: red;")

    def parse_timer_duration(self, duration_str):
        """
        Parse timer duration dari format HH:MM:SS, MM:SS, atau detik saja

        Args:
            duration_str: String durasi (HH:MM:SS, MM:SS, atau detik)

        Returns:
            Total detik (int) atau None jika invalid
        """
        duration_str = duration_str.strip()

        # Cek format dengan titik dua (HH:MM:SS atau MM:SS)
        if ':' in duration_str:
            parts = duration_str.split(':')

            if len(parts) == 3:
                # Format HH:MM:SS
                try:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2])

                    # Validasi range
                    if hours >= 0 and minutes >= 0 and minutes <= 59 and seconds >= 0 and seconds <= 59:
                        # Konversi ke total detik
                        total = (hours * 3600) + (minutes * 60) + seconds
                        return total if total > 0 else None
                    else:
                        return None
                except ValueError:
                    return None

            elif len(parts) == 2:
                # Format MM:SS (menit:detik)
                try:
                    minutes = int(parts[0])
                    seconds = int(parts[1])

                    # Validasi range
                    if minutes >= 0 and seconds >= 0 and seconds <= 59:
                        # Konversi ke total detik
                        total = (minutes * 60) + seconds
                        return total if total > 0 else None
                    else:
                        return None
                except ValueError:
                    return None

            else:
                return None
        else:
            # Format detik saja
            try:
                seconds = int(duration_str)
                return seconds if seconds > 0 else None
            except ValueError:
                return None

    def on_cancel_timer(self):
        """Handle Cancel Timer button click"""
        self.label_timer_status.setText("Status: Cancelling...")
        self.label_timer_status.setStyleSheet("color: orange; font-weight: bold;")
        # Send MQTT command
        self.backend.cancel_timer()

    # ================= SCHEDULE HANDLERS =================
    def on_set_schedule(self):
        """Handle Set Schedule button click"""
        start_time = self.input_schedule_start.text().strip()
        stop_time = self.input_schedule_stop.text().strip()

        # Get mode from combo box (0=Daily, 1=Onetime)
        current_index = self.combo_schedule_mode.currentIndex()
        if current_index == 0:
            mode = "daily"
        elif current_index == 1:
            mode = "onetime"
        else:
            mode = "daily"  # Default fallback

        # Validate time format
        if start_time and not self.validate_time_format(start_time):
            self.label_schedule_status.setText("Status: Invalid start format (HH:MM)")
            self.label_schedule_status.setStyleSheet("color: red;")
            return

        if stop_time and not self.validate_time_format(stop_time):
            self.label_schedule_status.setText("Status: Invalid stop format (HH:MM)")
            self.label_schedule_status.setStyleSheet("color: red;")
            return

        # Debug: Print ke console untuk cek
        # print(f"[DEBUG Schedule] currentIndex: {current_index}, mode: {mode}, start: {start_time}, stop: {stop_time}")

        # Update status
        if start_time and stop_time:
            self.label_schedule_status.setText(
                f"Status: Setting...\nStart: {start_time} | Stop: {stop_time}\nMode: {mode.capitalize()}"
            )
        elif start_time:
            self.label_schedule_status.setText(f"Status: Setting start: {start_time}")
        elif stop_time:
            self.label_schedule_status.setText(f"Status: Setting stop: {stop_time}")
        else:
            self.label_schedule_status.setText("Status: No input provided")
            return

        self.label_schedule_status.setStyleSheet("color: blue; font-weight: bold;")

        # Send MQTT commands
        # print(f"[DEBUG Schedule] Sending mode: {mode}")  # Debug
        self.backend.set_schedule_mode(mode)
        if start_time:
            self.backend.set_schedule_start(start_time)
        if stop_time:
            self.backend.set_schedule_stop(stop_time)

    def on_clear_schedule(self):
        """Handle Clear Schedule button click"""
        self.input_schedule_start.setText("")
        self.input_schedule_stop.setText("")
        self.combo_schedule_mode.setCurrentIndex(0)  # Reset to Daily

        self.label_schedule_status.setText("Status: Clearing...")
        self.label_schedule_status.setStyleSheet("color: orange; font-weight: bold;")

        # Send MQTT command
        self.backend.clear_schedule()

    # ================= HELPER FUNCTIONS =================
    def validate_time_format(self, time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.split(':')
            if len(parts) == 2:
                hour = int(parts[0])
                minute = int(parts[1])
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    return True
            return False
        except:
            return False
