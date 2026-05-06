"""Helper untuk menempatkan widget panah aliran energi di dashboard."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

from widgets.flow_arrow import FlowArrow


class ArrowSetup:
    @staticmethod
    def setup(ui, main_window):
        """Memasang semua panah flow ke frame placeholder yang sesuai."""
        ui.arrow_pv = FlowArrow(direction="down")
        ArrowSetup._add(ui.downArrowFrame, ui.arrow_pv)

        ui.arrow_grid = FlowArrow(direction="right")
        ArrowSetup._add(ui.rightArrowFrame, ui.arrow_grid)

        ui.arrow_load = FlowArrow(direction="right")
        ArrowSetup._add(ui.leftArrowFrame, ui.arrow_load)

        ui.arrow_soc_dynamic = FlowArrow(direction="up")
        ArrowSetup._add(ui.upArrowFrame, ui.arrow_soc_dynamic)

        # Simpan referensi panah di satu tempat agar MainWindow mudah
        # mengubah arah dan status aktif dari data realtime.
        main_window.arrows = {
            "pv": ui.arrow_pv,
            "soc_dynamic": ui.arrow_soc_dynamic,
            "grid": ui.arrow_grid,
            "load": ui.arrow_load,
        }

    @staticmethod
    def _add(frame, widget):
        """Menaruh satu widget panah ke dalam frame tujuan."""
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(widget)
