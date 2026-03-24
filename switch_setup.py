from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt
from widgets.switch_button import SwitchButton


class SwitchSetup:
    @staticmethod
    def setup(ui, main_window):
        frames = [
            ui.frame_switch_button_container,
            ui.frame_switch_button_container_2,
            ui.frame_switch_button_container_3,
            ui.frame_switch_button_container_4,
            ui.frame_switch_button_container_5,
        ]

        switch_locations = {
            1: "Switch 1",
            2: "Switch 2",
            3: "Switch 3",
            4: "Switch 4",
            5: "Switch 5",
        }

        main_window.switches = []

        for i, frame in enumerate(frames, start=1):
            layout = QVBoxLayout(frame)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Size tombol 140x140
            switch = SwitchButton(switch_index=i, size=140)

            # Tooltip
            switch.setToolTip(
                f"{switch_locations.get(i, '-')}\n"
                f"Klik untuk ON/OFF"
            )

            layout.addWidget(switch)
            main_window.switches.append(switch)

            # Connect signal
            switch.toggled.connect(
                lambda state, idx=i: main_window.on_switch_toggled(idx, state)
            )
