from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from ui_smartsocket_popup import Ui_SmartSocketPopup


class SmartSocketPopup(QDialog, Ui_SmartSocketPopup):
    def __init__(self, socket_number, parent=None):
        super().__init__(parent)
        self.socket_number = socket_number
        self.setupUi(self)

        # Set borderless window with rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Setup drag functionality
        self._old_pos = None

        # Apply rounded corners to dialog
        self.setStyleSheet("#SmartSocketPopup{"
                          "    background: qlineargradient("
                          "        x1:0, y1:0, x2:0, y2:1,"
                          "        stop:0 #E1F2FB,"
                          "        stop:1 #F1F9F9"
                          "    );"
                          "    border: 2px solid #005C99;"
                          "    border-radius: 10px;"
                          "}")

        # Set dynamic title based on socket number
        self.label_title.setText(f"⚡ Smart Socket {self.socket_number} Control")

        # Connect buttons (placeholder functions for now)
        self.connect_buttons()

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

    # ================= TIMER HANDLERS =================
    def on_start_timer(self):
        """Handle Start Timer button click"""
        duration = self.input_timer_duration.text()
        if duration.isdigit():
            self.label_timer_status.setText(f"Status: Starting {duration}s timer...")
            self.label_timer_status.setStyleSheet("color: blue; font-weight: bold;")
            # TODO: Send MQTT command later
            print(f"[Socket {self.socket_number}] Start Timer: {duration}s")
        else:
            self.label_timer_status.setText("Status: Invalid input!")
            self.label_timer_status.setStyleSheet("color: red;")

    def on_cancel_timer(self):
        """Handle Cancel Timer button click"""
        self.label_timer_status.setText("Status: Cancelling...")
        self.label_timer_status.setStyleSheet("color: orange; font-weight: bold;")
        # TODO: Send MQTT command later
        print(f"[Socket {self.socket_number}] Cancel Timer")

    # ================= SCHEDULE HANDLERS =================
    def on_set_schedule(self):
        """Handle Set Schedule button click"""
        start_time = self.input_schedule_start.text().strip()
        stop_time = self.input_schedule_stop.text().strip()
        mode = "daily" if self.combo_schedule_mode.currentIndex() == 0 else "onetime"

        # Validate time format
        if start_time and not self.validate_time_format(start_time):
            self.label_schedule_status.setText("Status: Invalid start format (HH:MM)")
            self.label_schedule_status.setStyleSheet("color: red;")
            return

        if stop_time and not self.validate_time_format(stop_time):
            self.label_schedule_status.setText("Status: Invalid stop format (HH:MM)")
            self.label_schedule_status.setStyleSheet("color: red;")
            return

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

        # TODO: Send MQTT commands later
        print(f"[Socket {self.socket_number}] Set Schedule: {start_time} - {stop_time} ({mode})")

    def on_clear_schedule(self):
        """Handle Clear Schedule button click"""
        self.input_schedule_start.setText("")
        self.input_schedule_stop.setText("")
        self.combo_schedule_mode.setCurrentIndex(0)  # Reset to Daily

        self.label_schedule_status.setText("Status: Clearing...")
        self.label_schedule_status.setStyleSheet("color: orange; font-weight: bold;")

        # TODO: Send MQTT command later
        print(f"[Socket {self.socket_number}] Clear Schedule")

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
