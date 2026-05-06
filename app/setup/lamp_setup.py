"""Helpers for creating and wiring custom lamp widgets."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

from widgets.lamp_button import LampButton


class LampSetup:
    @staticmethod
    def setup(ui, main_window):
        """Create all lamp buttons and connect them to publish callbacks."""
        frames = [
            ui.framebtnlamp1,
            ui.framebtnlamp2,
            ui.framebtnlamp3,
            ui.framebtnlamp4,
            ui.framebtnlamp5,
        ]

        lamp_locations = {
            1: "Lampu Atas Tengah",
            2: "Lampu Atas Utara dan Selatan",
            3: "Lampu Belakang TV",
            4: "Tidak Terpakai",
            5: "Lampu Depan Pintu",
        }

        main_window.lamps = []

        for i, frame in enumerate(frames, start=1):
            layout = QVBoxLayout(frame)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            lamp = LampButton(size=100)

            # Tooltips make the physical lamp mapping visible to the operator.
            lamp.setToolTip(
                f"Lampu {i}\n"
                f"Lokasi: {lamp_locations.get(i, '-')}"
            )

            # Lamp 4 is intentionally disabled because that channel is unused.
            if i == 4:
                lamp.setEnabled(False)

            layout.addWidget(lamp)
            main_window.lamps.append(lamp)

            lamp.toggled.connect(
                lambda state, idx=i: main_window.publish_lamp(idx, state)
            )
