from datetime import datetime
import time

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
    QDoubleValidator,
    QIntValidator,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
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
from ui.ui_smartsocket_popup import Ui_SmartSocketPopup
from ui.ui_theme_helper import apply_light_theme_to_widget


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


class GlobalRecordingSettingsDialog(QDialog):
    """Dialog untuk mengatur recording semua Smart Socket sekaligus."""
    WINDOW_RADIUS_PX = 12

    def __init__(self, main_window, parent=None):
        """Menyiapkan form global settings untuk semua socket."""
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowTitle("All Sockets Recording Settings")
        self.setModal(True)
        self.setMinimumWidth(560)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._old_pos = None
        apply_light_theme_to_widget(self)
        self.setStyleSheet("""
            QDialog { background: transparent; }
            QLabel {
                color: #1F2D3A;
                background: transparent;
            }
            QCheckBox {
                color: #1F2D3A;
                spacing: 6px;
                background: transparent;
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
            QLineEdit {
                color: #1F2D3A;
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid #B8D4E3;
                border-radius: 6px;
                padding: 6px 8px;
            }
            QPushButton {
                background-color: #005C99;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 7px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0B74B8;
            }
            QPushButton:pressed {
                background-color: #004B7D;
            }
        """)

        settings = {}
        if hasattr(self.main_window, "get_global_socket_monitoring_settings"):
            settings = self.main_window.get_global_socket_monitoring_settings()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QLabel("All Sockets Recording Settings", self)
        title.setStyleSheet(
            "font-size: 17px; font-weight: 700; color: #0F4165; "
            "padding-bottom: 4px;"
        )
        layout.addWidget(title)

        info = QLabel(
            "Apply recording settings to all Smart Socket devices at once."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        row_follow = QHBoxLayout()
        self.chk_follow_schedule = QCheckBox("Follow Schedule for All", self)
        self.chk_follow_schedule.setChecked(bool(settings.get("follow_schedule", False)))
        row_follow.addWidget(self.chk_follow_schedule)
        row_follow.addStretch()
        layout.addLayout(row_follow)

        row_interval = QHBoxLayout()
        row_interval.addWidget(QLabel("Interval (s):"))
        self.input_record_interval = QLineEdit(self)
        self.input_record_interval.setFixedWidth(90)
        self.input_record_interval.setAlignment(Qt.AlignCenter)
        self.input_record_interval.setValidator(QIntValidator(1, 3600, self))
        interval_seconds = settings.get("record_interval_seconds", 5)
        try:
            interval_seconds = int(round(float(interval_seconds)))
        except Exception:
            interval_seconds = 5
        self.input_record_interval.setText(str(max(1, interval_seconds)))
        row_interval.addWidget(self.input_record_interval)
        row_interval.addStretch()
        layout.addLayout(row_interval)

        row_autosave = QHBoxLayout()
        self.chk_autosave = QCheckBox("Autosave for All", self)
        self.chk_autosave.setChecked(bool(settings.get("autosave_enabled", False)))
        row_autosave.addWidget(self.chk_autosave)
        self.input_autosave_dir = QLineEdit(self)
        self.input_autosave_dir.setText(settings.get("autosave_dir", "") or "")
        row_autosave.addWidget(self.input_autosave_dir, 1)
        self.btn_pick_folder = QPushButton("Folder...")
        self.btn_pick_folder.clicked.connect(self._pick_folder)
        row_autosave.addWidget(self.btn_pick_folder)
        layout.addLayout(row_autosave)

        self.chk_save_default = QCheckBox("Save as default in AppData", self)
        self.chk_save_default.setChecked(True)
        layout.addWidget(self.chk_save_default)

        actions = QHBoxLayout()
        self.btn_apply_all = QPushButton("Apply to All")
        self.btn_start_all = QPushButton("Start All")
        self.btn_stop_all = QPushButton("Stop All")
        self.btn_close = QPushButton("Close")
        self.btn_apply_all.setStyleSheet(
            "QPushButton { background-color: #0F8B4C; color: #FFFFFF; "
            "border: none; border-radius: 6px; padding: 7px 12px; font-weight: 600; }"
            "QPushButton:hover { background-color: #12A95D; }"
            "QPushButton:pressed { background-color: #0B6F3D; }"
        )
        self.btn_stop_all.setStyleSheet(
            "QPushButton { background-color: #EB5757; color: #FFFFFF; "
            "border: none; border-radius: 6px; padding: 7px 12px; font-weight: 600; }"
            "QPushButton:hover { background-color: #F06A6A; }"
            "QPushButton:pressed { background-color: #C43F3F; }"
        )
        self.btn_close.setStyleSheet(
            "QPushButton { background-color: #6B7280; color: #FFFFFF; "
            "border: none; border-radius: 6px; padding: 7px 12px; font-weight: 600; }"
            "QPushButton:hover { background-color: #7B8494; }"
            "QPushButton:pressed { background-color: #596170; }"
        )
        actions.addWidget(self.btn_apply_all)
        actions.addWidget(self.btn_start_all)
        actions.addWidget(self.btn_stop_all)
        actions.addStretch()
        actions.addWidget(self.btn_close)
        layout.addLayout(actions)

        self.btn_apply_all.clicked.connect(self._apply_to_all)
        self.btn_start_all.clicked.connect(self._start_all)
        self.btn_stop_all.clicked.connect(self._stop_all)
        self.btn_close.clicked.connect(self.accept)
        self._update_rounded_mask()

    def paintEvent(self, event):
        super().paintEvent(event)

        rect = self.rect().adjusted(1, 1, -1, -1)
        if rect.width() <= 2 or rect.height() <= 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()
        path.addRoundedRect(rect, float(self.WINDOW_RADIUS_PX), float(self.WINDOW_RADIUS_PX))

        gradient = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        gradient.setColorAt(0.0, QColor("#E7F4FB"))
        gradient.setColorAt(1.0, QColor("#F8FCFF"))
        painter.fillPath(path, gradient)

        pen = QPen(QColor("#B8D4E3"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)

    def _update_rounded_mask(self):
        """Membuat bentuk window benar-benar rounded tanpa title bar bawaan."""
        rect = self.rect()
        if rect.isEmpty():
            return

        path = QPainterPath()
        path.addRoundedRect(
            rect.adjusted(0, 0, -1, -1),
            self.WINDOW_RADIUS_PX,
            self.WINDOW_RADIUS_PX,
        )
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_rounded_mask()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_rounded_mask()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._old_pos and event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.pos() + delta)
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def _pick_folder(self):
        """Membuka folder picker untuk memilih lokasi autosave global."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Autosave Folder",
            self.input_autosave_dir.text().strip(),
        )
        if directory:
            self.input_autosave_dir.setText(directory)

    def _settings_payload(self):
        """Mengambil payload settings dari input dialog dalam format siap pakai."""
        text = self.input_record_interval.text().strip()
        try:
            interval_seconds = int(text)
        except ValueError:
            interval_seconds = 5
        interval_seconds = max(1, interval_seconds)
        self.input_record_interval.setText(str(interval_seconds))

        follow_schedule = self.chk_follow_schedule.isChecked()
        autosave_enabled = self.chk_autosave.isChecked() or follow_schedule

        return {
            "follow_schedule": follow_schedule,
            "record_interval_seconds": float(interval_seconds),
            "autosave_enabled": autosave_enabled,
            "autosave_dir": self.input_autosave_dir.text().strip(),
            "save_as_default": self.chk_save_default.isChecked(),
        }

    def _apply_to_all(self):
        """Menerapkan settings dialog ke semua socket lewat MainWindow."""
        if not hasattr(self.main_window, "apply_global_socket_monitoring_settings"):
            return False
        payload = self._settings_payload()
        if payload["autosave_enabled"] and not payload["autosave_dir"]:
            self._pick_folder()
            payload = self._settings_payload()
        if payload["autosave_enabled"] and not payload["autosave_dir"]:
            QMessageBox.warning(
                self,
                "Autosave Folder Required",
                "Select an autosave folder before enabling autosave or Follow Schedule.",
            )
            return False
        self.main_window.apply_global_socket_monitoring_settings(**payload)
        return True

    def _start_all(self):
        """Menerapkan settings lalu memulai recording semua socket."""
        if not self._apply_to_all():
            return
        if hasattr(self.main_window, "start_all_socket_recording"):
            self.main_window.start_all_socket_recording(source="manual")

    def _stop_all(self):
        """Menerapkan settings lalu menghentikan recording semua socket."""
        if not self._apply_to_all():
            return
        if hasattr(self.main_window, "stop_all_socket_recording"):
            self.main_window.stop_all_socket_recording(source="manual")


class SmartSocketPopup(QDialog, Ui_SmartSocketPopup):
    """Popup kontrol detail untuk satu Smart Socket beserta tab monitoringnya."""
    TABLE_DISPLAY_LIMIT = 500
    CHART_POINT_LIMIT = 300
    WINDOW_RADIUS_PX = 10
    WINDOW_WIDTH_PX = 1240
    WINDOW_HEIGHT_PX = 720

    def __init__(self, socket_number, backend, main_window, parent=None):
        """Menyiapkan popup socket, chart, table, warning, dan kontrol recording."""
        super().__init__(parent)
        self.socket_number = socket_number
        self.backend = backend  # SmartSocketBackend instance
        self.main_window = main_window  # Reference ke MainWindow untuk simpan format
        if hasattr(self.main_window, "get_socket_graph_range_overrides"):
            self.graph_range_overrides = self.main_window.get_socket_graph_range_overrides()
        else:
            self.graph_range_overrides = {}
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
        if hasattr(self.main_window, "socket_warning_state_changed"):
            self.main_window.socket_warning_state_changed.connect(
                self._on_warning_state_changed
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
        if hasattr(self.main_window, "socket_warning_state_changed"):
            try:
                self.main_window.socket_warning_state_changed.disconnect(
                    self._on_warning_state_changed
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
        self.resize(1180, 800)
        self.setMinimumSize(QSize(1120, 760))
        self.setMaximumSize(QSize(1320, 940))
        self.label_title.setMinimumSize(QSize(820, 55))
        self.label_title.setMaximumSize(QSize(1020, 60))

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
        self.warning_tab = QWidget(self.tabs)
        self.setting_tab = QWidget(self.tabs)
        self._build_data_tab()
        self._build_graph_tab()
        self._build_warning_tab()
        self._build_setting_tab()

        self.tabs.addTab(self.control_tab, "Control")
        self.tabs.addTab(self.data_tab, "Data")
        self.tabs.addTab(self.graph_tab, "Graph")
        self.tabs.addTab(self.warning_tab, "Warning")
        self.tabs.addTab(self.setting_tab, "Setting")
        if not getattr(self.main_window, "is_admin_user", lambda: False)():
            setting_index = self.tabs.indexOf(self.setting_tab)
            if setting_index >= 0:
                self.tabs.setTabEnabled(setting_index, False)
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
        self.btn_all_sockets = QPushButton("All Sockets...")

        self.btn_start_recording.setStyleSheet(self._button_style("#0F8B4C"))
        self.btn_stop_recording.setStyleSheet(self._button_style("#EB5757"))
        self.btn_clear_records.setStyleSheet(self._button_style("#6B7280"))
        self.btn_export_csv.setStyleSheet(self._button_style("#005C99"))
        self.btn_all_sockets.setStyleSheet(self._button_style("#0D6E6E"))

        top_layout.addWidget(self.btn_start_recording)
        top_layout.addWidget(self.btn_stop_recording)
        top_layout.addWidget(self.btn_clear_records)
        top_layout.addWidget(self.btn_export_csv)
        top_layout.addWidget(self.btn_all_sockets)
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
        self.btn_all_sockets.clicked.connect(self.on_open_all_sockets_settings)

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
        self.chk_graph_custom_range = QCheckBox("Custom Y-Axis", self.graph_tab)
        top_layout.addWidget(self.chk_graph_custom_range)
        top_layout.addWidget(QLabel("Min:"))
        self.input_graph_min = QLineEdit(self.graph_tab)
        self.input_graph_min.setFixedWidth(74)
        self.input_graph_min.setAlignment(Qt.AlignCenter)
        self.input_graph_min.setValidator(QDoubleValidator(self))
        top_layout.addWidget(self.input_graph_min)
        top_layout.addWidget(QLabel("Max:"))
        self.input_graph_max = QLineEdit(self.graph_tab)
        self.input_graph_max.setFixedWidth(74)
        self.input_graph_max.setAlignment(Qt.AlignCenter)
        self.input_graph_max.setValidator(QDoubleValidator(self))
        top_layout.addWidget(self.input_graph_max)
        self.btn_graph_apply_range = QPushButton("Apply")
        self.btn_graph_apply_range.setStyleSheet(self._button_style("#0F8B4C"))
        top_layout.addWidget(self.btn_graph_apply_range)
        self.btn_graph_reset_range = QPushButton("Reset")
        self.btn_graph_reset_range.setStyleSheet(self._button_style("#6B7280"))
        top_layout.addWidget(self.btn_graph_reset_range)
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
            self._on_graph_selection_changed
        )
        self.combo_graph_metric.currentIndexChanged.connect(
            self._on_graph_selection_changed
        )
        self.chk_graph_custom_range.stateChanged.connect(
            self._on_graph_custom_range_toggled
        )
        self.btn_graph_apply_range.clicked.connect(
            lambda: self._on_graph_apply_range(show_warning=True)
        )
        self.btn_graph_reset_range.clicked.connect(self._on_graph_reset_range)
        self.input_graph_min.editingFinished.connect(self._on_graph_range_edit_finished)
        self.input_graph_max.editingFinished.connect(self._on_graph_range_edit_finished)
        self._load_graph_range_controls()

    def _build_warning_tab(self):
        layout = QVBoxLayout(self.warning_tab)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        self.warning_tab.setStyleSheet("""
            QWidget {
                color: #1F2D3A;
                background: transparent;
            }
            QLabel {
                color: #1F2D3A;
                background: transparent;
            }
        """)

        self.label_warning_title = QLabel("Load Warning Status")
        self.label_warning_title.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(self.label_warning_title)

        self.label_warning_level = QLabel("Status: Safe")
        self.label_warning_level.setStyleSheet(
            "padding: 10px 12px; border-radius: 8px; background: #E6F7EC; "
            "color: #0F8B4C; font-weight: 700;"
        )
        layout.addWidget(self.label_warning_level)

        self.label_warning_message = QLabel("Tidak ada warning aktif.")
        self.label_warning_message.setWordWrap(True)
        self.label_warning_message.setStyleSheet(
            "padding: 12px; border: 1px solid #C7DCEC; border-radius: 8px; "
            "background: #F8FCFF;"
        )
        layout.addWidget(self.label_warning_message)

        self.label_warning_ack = QLabel("Acknowledgement: Not required")
        self.label_warning_ack.setStyleSheet("font-weight: 600; color: #52606D;")
        layout.addWidget(self.label_warning_ack)

        action_row = QHBoxLayout()
        self.btn_warning_ack = QPushButton("Acknowledge")
        self.btn_warning_ack.setStyleSheet(self._button_style("#C97A00"))
        self.btn_warning_ack.clicked.connect(self.on_acknowledge_warning)
        action_row.addWidget(self.btn_warning_ack)
        action_row.addStretch()
        layout.addLayout(action_row)
        layout.addStretch()
        self._update_setting_tab_access()

    def _build_setting_tab(self):
        layout = QVBoxLayout(self.setting_tab)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        self.setting_tab.setStyleSheet("""
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
                padding: 5px 8px;
            }
            QGroupBox {
                border: 1px solid #C7DCEC;
                border-radius: 8px;
                margin-top: 12px;
                padding: 12px;
                background: #F8FCFF;
                font-weight: 700;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
        """)

        info = QLabel(
            "Konfigurasi ini mengatur apakah Smart Socket boleh dimatikan oleh user biasa. "
            "Admin selalu dapat bypass proteksi saat menekan OFF."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        self.group_protection = QGroupBox("Edit Protection")
        group_layout = QVBoxLayout(self.group_protection)
        group_layout.setSpacing(10)

        self.chk_protection_enabled = QCheckBox("Enable power-off protection", self.group_protection)
        group_layout.addWidget(self.chk_protection_enabled)

        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Mode:"))
        self.combo_protection_mode = QComboBox(self.group_protection)
        self.combo_protection_mode.addItem("Blocked", "blocked")
        self.combo_protection_mode.addItem("Password required", "password")
        mode_row.addWidget(self.combo_protection_mode)
        mode_row.addStretch()
        group_layout.addLayout(mode_row)

        password_row = QHBoxLayout()
        password_row.addWidget(QLabel("Password:"))
        self.input_protection_password = QLineEdit(self.group_protection)
        self.input_protection_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_protection_password.setPlaceholderText("Leave blank to keep current password")
        password_row.addWidget(self.input_protection_password)
        group_layout.addLayout(password_row)

        self.label_password_state = QLabel("Saved password: loading...")
        self.label_password_state.setStyleSheet("color: #52606D; font-weight: 500;")
        group_layout.addWidget(self.label_password_state)

        note_row = QHBoxLayout()
        note_row.addWidget(QLabel("Description:"))
        self.input_protection_note = QLineEdit(self.group_protection)
        self.input_protection_note.setPlaceholderText("Example: Supply Raspberry Pi server")
        note_row.addWidget(self.input_protection_note)
        group_layout.addLayout(note_row)

        helper = QLabel(
            "Mode Blocked: user biasa tidak bisa OFF.\n"
            "Mode Password required: user biasa harus konfirmasi lalu memasukkan password."
        )
        helper.setWordWrap(True)
        helper.setStyleSheet("color: #52606D; font-weight: 500;")
        group_layout.addWidget(helper)

        layout.addWidget(self.group_protection)

        action_row = QHBoxLayout()
        action_row.addStretch()
        self.btn_protection_reload = QPushButton("Reload")
        self.btn_protection_reload.setStyleSheet(self._button_style("#6B7280"))
        self.btn_protection_save = QPushButton("Save")
        self.btn_protection_save.setStyleSheet(self._button_style("#0F8B4C"))
        action_row.addWidget(self.btn_protection_reload)
        action_row.addWidget(self.btn_protection_save)
        layout.addLayout(action_row)
        layout.addStretch()

        self.chk_protection_enabled.stateChanged.connect(
            self._on_protection_controls_changed
        )
        self.combo_protection_mode.currentIndexChanged.connect(
            self._on_protection_controls_changed
        )
        self.btn_protection_reload.clicked.connect(
            lambda: self._reload_socket_protection_settings(show_feedback=True)
        )
        self.btn_protection_save.clicked.connect(self._save_socket_protection_settings)
        self._reload_socket_protection_settings(show_feedback=False)
        self._on_protection_controls_changed()
        self._update_setting_tab_access()

    def _update_setting_tab_access(self):
        is_admin = getattr(self.main_window, "is_admin_user", lambda: False)()
        for widget in (
            getattr(self, "group_protection", None),
            getattr(self, "btn_protection_reload", None),
            getattr(self, "btn_protection_save", None),
        ):
            if widget is not None:
                widget.setEnabled(is_admin)

        if hasattr(self, "setting_tab"):
            self.setting_tab.setToolTip(
                "" if is_admin else "Setting tab is available for admin only."
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

    def _metric_y_range(self, metric):
        return {
            "voltage": (200.0, 240.0),
            "current": (0.0, 7.0),
            "power": (0.0, 1500.0),
            "energy": (0.0, 5.0),
            "frequency": (45.0, 55.0),
            "pf": (0.0, 1.1),
        }.get(metric)

    def _graph_range_key(self):
        return (
            self._selected_graph_socket(),
            self.combo_graph_metric.currentData() or "power",
        )

    def _load_graph_range_controls(self):
        if not hasattr(self, "chk_graph_custom_range"):
            return

        override = self.graph_range_overrides.get(self._graph_range_key())
        enabled = bool(override and override.get("enabled"))

        self.chk_graph_custom_range.blockSignals(True)
        self.chk_graph_custom_range.setChecked(enabled)
        self.chk_graph_custom_range.blockSignals(False)

        min_text = ""
        max_text = ""
        if override:
            min_value = override.get("min")
            max_value = override.get("max")
            min_text = "" if min_value is None else f"{min_value:g}"
            max_text = "" if max_value is None else f"{max_value:g}"

        self.input_graph_min.blockSignals(True)
        self.input_graph_min.setText(min_text)
        self.input_graph_min.blockSignals(False)
        self.input_graph_max.blockSignals(True)
        self.input_graph_max.setText(max_text)
        self.input_graph_max.blockSignals(False)

        self._update_graph_range_inputs_enabled()

    def _update_graph_range_inputs_enabled(self):
        enabled = (
            self.chk_graph_custom_range.isChecked()
            if hasattr(self, "chk_graph_custom_range")
            else False
        )
        for widget in (
            getattr(self, "input_graph_min", None),
            getattr(self, "input_graph_max", None),
            getattr(self, "btn_graph_apply_range", None),
        ):
            if widget is not None:
                widget.setEnabled(enabled)

    def _on_graph_selection_changed(self, *_):
        self._load_graph_range_controls()
        self.refresh_monitoring_view()

    def _on_graph_custom_range_toggled(self, *_):
        key = self._graph_range_key()
        state = self.graph_range_overrides.get(key, {}).copy()
        state["enabled"] = self.chk_graph_custom_range.isChecked()
        self.graph_range_overrides[key] = state
        self._update_graph_range_inputs_enabled()
        if state["enabled"]:
            self._on_graph_apply_range(show_warning=False)
        else:
            self.refresh_monitoring_view()

    def _on_graph_range_edit_finished(self):
        self._on_graph_apply_range(show_warning=False)

    @staticmethod
    def _parse_graph_range_value(text):
        normalized = (text or "").strip().replace(",", ".")
        if not normalized:
            raise ValueError("empty")
        return float(normalized)

    def _on_graph_apply_range(self, show_warning=False):
        if not self.chk_graph_custom_range.isChecked():
            return

        min_text = self.input_graph_min.text().strip()
        max_text = self.input_graph_max.text().strip()
        if not min_text or not max_text:
            return

        try:
            min_value = self._parse_graph_range_value(min_text)
            max_value = self._parse_graph_range_value(max_text)
        except ValueError:
            if show_warning:
                QMessageBox.warning(
                    self,
                    "Custom Y-Axis",
                    "Min dan Max harus berupa angka.",
                )
            return

        if min_value >= max_value:
            if show_warning:
                QMessageBox.warning(
                    self,
                    "Custom Y-Axis",
                    "Nilai Min harus lebih kecil dari Max.",
                )
            return

        self.graph_range_overrides[self._graph_range_key()] = {
            "enabled": True,
            "min": min_value,
            "max": max_value,
        }
        if hasattr(self.main_window, "set_socket_graph_range_override"):
            self.main_window.set_socket_graph_range_override(
                self._selected_graph_socket(),
                self.combo_graph_metric.currentData() or "power",
                self.graph_range_overrides[self._graph_range_key()],
            )
        self.input_graph_min.setText(f"{min_value:g}")
        self.input_graph_max.setText(f"{max_value:g}")
        self.refresh_monitoring_view()

    def _on_graph_reset_range(self):
        graph_socket = self._selected_graph_socket()
        metric = self.combo_graph_metric.currentData() or "power"
        self.graph_range_overrides.pop((graph_socket, metric), None)
        if hasattr(self.main_window, "clear_socket_graph_range_override"):
            self.main_window.clear_socket_graph_range_override(graph_socket, metric)
        self._load_graph_range_controls()
        self.refresh_monitoring_view()

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
        if enabled:
            try:
                directory = self.main_window.get_socket_autosave_dir(socket_number)
            except Exception:
                directory = ""
            if not directory:
                self._on_pick_autosave_folder()
                try:
                    directory = self.main_window.get_socket_autosave_dir(socket_number)
                except Exception:
                    directory = ""
            if not directory:
                self.chk_follow_schedule.blockSignals(True)
                self.chk_follow_schedule.setChecked(False)
                self.chk_follow_schedule.blockSignals(False)
                return
            if hasattr(self.main_window, "set_socket_autosave_enabled"):
                self.main_window.set_socket_autosave_enabled(socket_number, True)
        self.main_window.set_socket_follow_schedule(socket_number, enabled)
        if enabled and self._is_socket_schedule_window_active(socket_number):
            self.main_window.start_socket_recording(socket_number, source="schedule")
        self.refresh_monitoring_view()

    def _is_socket_schedule_window_active(self, socket_number):
        try:
            backend = self.main_window.smartsocket_manager.get_backend(socket_number)
        except Exception:
            backend = None

        if backend is None or not getattr(backend, "relay_state", False):
            return False

        schedule_status = getattr(backend, "schedule_status", None) or {}
        start_value = schedule_status.get("start")
        stop_value = schedule_status.get("stop")
        if not start_value or not stop_value:
            return False

        try:
            start_hour, start_minute = map(int, str(start_value).split(":", 1))
            stop_hour, stop_minute = map(int, str(stop_value).split(":", 1))
        except (TypeError, ValueError):
            return False

        now = datetime.now()
        now_minutes = now.hour * 60 + now.minute
        start_minutes = start_hour * 60 + start_minute
        stop_minutes = stop_hour * 60 + stop_minute

        if start_minutes == stop_minutes:
            return False
        if start_minutes < stop_minutes:
            return start_minutes <= now_minutes < stop_minutes
        return now_minutes >= start_minutes or now_minutes < stop_minutes

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
        try:
            follow_schedule = self.main_window.is_socket_follow_schedule(socket_number)
        except Exception:
            follow_schedule = False
        if follow_schedule and not enabled:
            self.chk_autosave.blockSignals(True)
            self.chk_autosave.setChecked(True)
            self.chk_autosave.blockSignals(False)
            return
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

    def _current_graph_override(self):
        override = self.graph_range_overrides.get(self._graph_range_key())
        if not override or not override.get("enabled"):
            return None
        min_value = override.get("min")
        max_value = override.get("max")
        if min_value is None or max_value is None or min_value >= max_value:
            return None
        return (float(min_value), float(max_value))

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

    def on_open_all_sockets_settings(self):
        dialog = GlobalRecordingSettingsDialog(self.main_window, self)
        dialog.exec()
        self.refresh_monitoring_view()

    def on_acknowledge_warning(self):
        if hasattr(self.main_window, "acknowledge_socket_warning"):
            self.main_window.acknowledge_socket_warning(self.socket_number)
        self._refresh_warning_tab(self.socket_number)

    def refresh_monitoring_view(self, *_):
        if not hasattr(self.main_window, "smartsocket_recorder"):
            return

        data_socket = self._selected_data_socket()
        graph_socket = self._selected_graph_socket()

        self._refresh_recording_controls(data_socket)
        self._refresh_table(data_socket)
        self._refresh_chart(graph_socket)
        self._refresh_warning_tab(self.socket_number)

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
            self.chk_autosave.setChecked(autosave_enabled or follow_schedule)
            self.chk_autosave.blockSignals(False)
            self.chk_autosave.setEnabled(not follow_schedule)
            if follow_schedule:
                self.chk_autosave.setToolTip("Autosave is required while Follow Schedule is active.")
            else:
                self.chk_autosave.setToolTip(
                    "Manual mode saves each day automatically while recording stays active."
                )
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
        override_range = self._current_graph_override()
        if override_range is not None:
            axis_y.setRange(*override_range)
            range_label = f"Custom Y: {override_range[0]:g} to {override_range[1]:g}"
        else:
            fixed_range = self._metric_y_range(metric)
            if fixed_range is not None:
                axis_y.setRange(*fixed_range)
                range_label = f"Default Y: {fixed_range[0]:g} to {fixed_range[1]:g}"
            elif values:
                min_value = min(values)
                max_value = max(values)
                if min_value == max_value:
                    padding = abs(min_value) * 0.1 or 1.0
                else:
                    padding = (max_value - min_value) * 0.1
                axis_y.setRange(min_value - padding, max_value + padding)
                range_label = "Y-Axis: Auto"
            else:
                axis_y.setRange(0, 1)
                range_label = "Y-Axis: Auto"

        self.label_graph_status.setText(
            f"Showing last {len(chart_records)} of {len(records)} samples | "
            f"{range_label}"
        )

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

    def _on_warning_state_changed(self, socket_number):
        if socket_number == self.socket_number:
            self._refresh_warning_tab(socket_number)

    def _selected_protection_mode(self):
        if not hasattr(self, "combo_protection_mode"):
            return "blocked"
        text = (self.combo_protection_mode.currentText() or "").strip().lower()
        return "password" if "password" in text else "blocked"

    def _reload_socket_protection_settings(self, show_feedback=False):
        load_success, _ = self._load_socket_protection_settings()
        self._on_protection_controls_changed()
        if not show_feedback:
            return

        if load_success:
            QMessageBox.information(
                self,
                "Reload Complete",
                f"Smart Socket {self.socket_number} protection reloaded from Firebase.",
            )
        else:
            QMessageBox.warning(
                self,
                "Reload Failed",
                "Failed to reload protection from Firebase. Showing cached value.",
            )

    def _load_socket_protection_settings(self):
        load_success = True
        protection = None
        if hasattr(self.main_window, "reload_one_socket_power_off_protection"):
            load_success, protection = self.main_window.reload_one_socket_power_off_protection(
                self.socket_number
            )
        elif hasattr(self.main_window, "reload_socket_power_off_protection"):
            load_success = bool(self.main_window.reload_socket_power_off_protection())

        if not hasattr(self.main_window, "get_socket_power_off_protection"):
            return False, {}

        if not isinstance(protection, dict):
            protection = self.main_window.get_socket_power_off_protection(self.socket_number)
        self.chk_protection_enabled.blockSignals(True)
        self.combo_protection_mode.blockSignals(True)
        self.input_protection_password.blockSignals(True)
        self.input_protection_note.blockSignals(True)

        self.chk_protection_enabled.setChecked(bool(protection.get("enabled")))
        if (protection.get("mode", "blocked") or "blocked") == "password":
            self.combo_protection_mode.setCurrentText("Password required")
        else:
            self.combo_protection_mode.setCurrentText("Blocked")
        self.input_protection_password.clear()
        self.input_protection_note.setText(protection.get("note", "") or "")
        self._update_password_state_label(protection, load_success)

        self.chk_protection_enabled.blockSignals(False)
        self.combo_protection_mode.blockSignals(False)
        self.input_protection_password.blockSignals(False)
        self.input_protection_note.blockSignals(False)
        return load_success, protection

    def _update_password_state_label(self, protection: dict, load_success: bool):
        if not hasattr(self, "label_password_state"):
            return

        has_password = bool(protection.get("password_hash"))
        status_text = f"Saved password: {'Set' if has_password else 'Not set'}"

        if not load_success:
            status_text += " | Firebase reload failed, showing cached value."

        self.label_password_state.setText(status_text)

    def _on_protection_controls_changed(self, *_):
        enabled = (
            self.chk_protection_enabled.isChecked()
            if hasattr(self, "chk_protection_enabled")
            else False
        )
        password_mode = (
            enabled
            and hasattr(self, "combo_protection_mode")
            and self._selected_protection_mode() == "password"
        )
        if hasattr(self, "combo_protection_mode"):
            self.combo_protection_mode.setEnabled(enabled)
        if hasattr(self, "input_protection_password"):
            self.input_protection_password.setEnabled(password_mode)
        if hasattr(self, "input_protection_note"):
            self.input_protection_note.setEnabled(enabled)

    def _save_socket_protection_settings(self):
        if not getattr(self.main_window, "is_admin_user", lambda: False)():
            QMessageBox.warning(
                self,
                "Admin Only",
                "Only admin can change Smart Socket protection settings.",
            )
            return

        enabled = self.chk_protection_enabled.isChecked()
        mode = self._selected_protection_mode()
        note = self.input_protection_note.text().strip()
        password_text = self.input_protection_password.text().strip()
        current = self.main_window.get_socket_power_off_protection(self.socket_number)
        password_hash = None

        if enabled and mode == "password":
            if password_text:
                password_hash = self.main_window._hash_socket_protection_password(
                    password_text
                )
            elif not current.get("password_hash"):
                QMessageBox.warning(
                    self,
                    "Password Required",
                    "Mode password membutuhkan password untuk Smart Socket ini.",
                )
                self.input_protection_password.setFocus()
                return

        try:
            saved = self.main_window.set_socket_power_off_protection(
                self.socket_number,
                enabled=enabled,
                mode=mode,
                password_hash=password_hash,
                note=note,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Protection Save Failed",
                f"Failed to save Smart Socket protection to Firebase:\n{exc}",
            )
            return
        self._update_password_state_label(saved, True)
        self._reload_socket_protection_settings(show_feedback=False)
        self._on_protection_controls_changed()
        QMessageBox.information(
            self,
            "Protection Saved",
            f"Protection for Smart Socket {self.socket_number} saved.",
        )

    def _refresh_warning_tab(self, socket_number):
        if not hasattr(self.main_window, "get_socket_warning_state"):
            return

        state = self.main_window.get_socket_warning_state(socket_number)
        active = bool(state.get("active"))
        level = state.get("level", "normal")
        current_value = float(state.get("current", 0.0) or 0.0)
        message = state.get("message", "") or ""
        acknowledged = bool(state.get("acknowledged", False))
        critical_stage = int(state.get("critical_stage", 0) or 0)
        critical_deadline = float(state.get("critical_deadline", 0.0) or 0.0)

        if not active:
            self.label_warning_level.setText("Status: Safe")
            self.label_warning_level.setStyleSheet(
                "padding: 10px 12px; border-radius: 8px; background: #E6F7EC; "
                "color: #0F8B4C; font-weight: 700;"
            )
            self.label_warning_message.setText("Tidak ada warning aktif.")
            self.label_warning_ack.setText("Acknowledgement: Not required")
            self.btn_warning_ack.setEnabled(False)
            return

        level_map = {
            "elevated": ("Status: Beban Cukup Tinggi", "#FFF6DB", "#A86A00"),
            "high": ("Status: Beban Tinggi", "#FFE8CC", "#C05621"),
            "critical": ("Status: Kurangi Beban Segera", "#FDECEC", "#C53030"),
        }
        level_text, bg_color, fg_color = level_map.get(
            level,
            ("Status: Warning", "#FFF6DB", "#A86A00"),
        )
        self.label_warning_level.setText(level_text)
        self.label_warning_level.setStyleSheet(
            f"padding: 10px 12px; border-radius: 8px; background: {bg_color}; "
            f"color: {fg_color}; font-weight: 700;"
        )
        self.label_warning_message.setText(
            f"Smart Socket {socket_number}\n"
            f"Current: {current_value:.3f} A\n"
            f"{message}"
        )
        if level == "critical":
            if critical_stage == 2 and critical_deadline > 0:
                remaining_seconds = max(0, int(round(critical_deadline - time.time())))
                ack_text = f"Protection: Auto OFF dalam {remaining_seconds} detik"
            elif critical_stage == 1:
                ack_text = "Protection: Menunggu verifikasi pengurangan beban"
            else:
                ack_text = "Protection: Critical mode aktif"
            self.label_warning_ack.setText(ack_text)
            self.btn_warning_ack.setEnabled(False)
        else:
            self.label_warning_ack.setText(
                "Acknowledgement: Acknowledged"
                if acknowledged else
                "Acknowledgement: Waiting for acknowledgement"
            )
            self.btn_warning_ack.setEnabled(not acknowledged)

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
        if (
            not getattr(self.main_window, "is_admin_user", lambda: False)()
            and getattr(self.main_window, "is_socket_schedule_active", lambda _socket: False)(
                self.socket_number
            )
        ):
            QMessageBox.warning(
                self,
                "Timer Tidak Dapat Diaktifkan",
                "Timer tidak dapat diaktifkan karena schedule sedang aktif.\n"
                "Hapus schedule terlebih dahulu.",
            )
            return

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
        if (
            not getattr(self.main_window, "is_admin_user", lambda: False)()
            and getattr(self.main_window, "is_socket_timer_active", lambda _socket: False)(
                self.socket_number
            )
        ):
            QMessageBox.warning(
                self,
                "Schedule Tidak Dapat Diaktifkan",
                "Schedule tidak dapat diaktifkan karena timer sedang berjalan.\n"
                "Batalkan timer terlebih dahulu.",
            )
            return

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
