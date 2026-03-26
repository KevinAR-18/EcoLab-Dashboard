from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from ui_smartsocket_popup import Ui_SmartSocketPopup


class SmartSocketPopup(QDialog, Ui_SmartSocketPopup):
    def __init__(self, socket_number, backend, main_window, parent=None):
        super().__init__(parent)
        self.socket_number = socket_number
        self.backend = backend  # SmartSocketBackend instance
        self.main_window = main_window  # Reference ke MainWindow untuk simpan format
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

        # Send MQTT commands
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
