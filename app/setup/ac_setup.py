"""Helpers for creating and wiring the custom AC control widget."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

from widgets.ac_button import ACButton


class ACSetup:
    @staticmethod
    def setup(ui, main_window):
        """Create the custom AC button and connect it to dashboard callbacks."""
        layout = QVBoxLayout(ui.frameButtonOnOffAC)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        main_window.ac_button = ACButton()
        layout.addWidget(main_window.ac_button)

        # Keep label styling in one place so user clicks and MQTT refreshes reuse
        # the same UI update logic.
        def update_ac_status(state):
            ui.statusAC.setText("AC: ON ❄️" if state else "AC: OFF")
            ui.statusAC.setProperty("state", "on" if state else "off")
            ui.statusAC.style().polish(ui.statusAC)

        # Expose the updater so MainWindow can refresh the label from backend events.
        main_window.update_ac_status = update_ac_status

        main_window.ac_button.toggled.connect(update_ac_status)
        main_window.ac_button.toggled.connect(
            lambda state: main_window.publish_ac_power(state)
        )
