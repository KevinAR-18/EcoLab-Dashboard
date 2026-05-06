"""Helper untuk membuat dan memasang widget kontrol AC custom."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

from widgets.ac_button import ACButton


class ACSetup:
    @staticmethod
    def setup(ui, main_window):
        """Membuat tombol AC custom lalu menghubungkannya ke callback dashboard."""
        layout = QVBoxLayout(ui.frameButtonOnOffAC)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        main_window.ac_button = ACButton()
        layout.addWidget(main_window.ac_button)

        # Simpan logika update label di satu tempat agar klik user dan refresh
        # dari MQTT memakai format UI yang sama.
        def update_ac_status(state):
            """Memperbarui label status AC sesuai state terbaru."""
            ui.statusAC.setText("AC: ON ❄️" if state else "AC: OFF")
            ui.statusAC.setProperty("state", "on" if state else "off")
            ui.statusAC.style().polish(ui.statusAC)

        # Expose updater ini agar MainWindow bisa memakainya saat ada event backend.
        main_window.update_ac_status = update_ac_status

        main_window.ac_button.toggled.connect(update_ac_status)
        main_window.ac_button.toggled.connect(
            lambda state: main_window.publish_ac_power(state)
        )
