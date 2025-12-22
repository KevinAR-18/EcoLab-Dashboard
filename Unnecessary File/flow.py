from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from widgets.flow_arrow import FlowArrow
import sys

app = QApplication(sys.argv)

w = QWidget()
layout = QVBoxLayout(w)

arrow_up = FlowArrow(direction="up")
arrow_down = FlowArrow(direction="down")
arrow_left = FlowArrow(direction="left")
arrow_right = FlowArrow(direction="right")

layout.addWidget(arrow_up)
layout.addWidget(arrow_down)
layout.addWidget(arrow_left)
layout.addWidget(arrow_right)

# aktifkan semua buat tes
arrow_up.set_active(True)
arrow_down.set_active(True)
arrow_left.set_active(True)
arrow_right.set_active(True)

w.show()
sys.exit(app.exec())
