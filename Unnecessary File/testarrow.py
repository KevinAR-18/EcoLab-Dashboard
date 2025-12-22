import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QPolygon, QFont


class FlowArrowCascade(QWidget):
    """
    6 segitiga ▶▶▶▶▶▶
    Nyala bertahap → fade out → ulang
    """

    def __init__(self, parent=None, count=6):
        super().__init__(parent)
        self.setFixedSize(220, 40)

        self.count = count
        self.active = False

        self.step = 0
        self.state = "grow"  # grow | fade
        self.alpha = 255

        self.timer = QTimer(self)
        self.timer.setInterval(120)
        self.timer.timeout.connect(self.animate)

    # ===== CONTROL =====
    def set_active(self, state: bool):
        if self.active == state:
            return

        self.active = state
        self.reset()

        if state:
            self.timer.start()
        else:
            self.timer.stop()
            self.update()

    def reset(self):
        self.step = 0
        self.state = "grow"
        self.alpha = 255

    def animate(self):
        if self.state == "grow":
            self.step += 1
            if self.step >= self.count:
                self.step = self.count
                self.state = "fade"

        elif self.state == "fade":
            self.alpha -= 100
            if self.alpha <= 0:
                self.reset()

        self.update()

    # ===== PAINT =====
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        base_color = QColor(200, 200, 200)
        active_color = QColor("#4CAF50")

        y = self.height() // 2
        size = 8
        spacing = 20
        start_x = 20

        for i in range(self.count):
            if not self.active:
                color = base_color
                alpha = 255
            else:
                if i < self.step:
                    color = active_color
                    alpha = self.alpha
                else:
                    color = base_color
                    alpha = 255

            c = QColor(color)
            c.setAlpha(alpha)

            p.setBrush(c)
            p.setPen(Qt.NoPen)

            x = start_x + i * spacing
            tri = QPolygon([
                QPoint(x, y - size),
                QPoint(x, y + size),
                QPoint(x + size + 6, y)
            ])

            p.drawPolygon(tri)


# ================= DEMO =================
class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flow Arrow Cascade")
        self.resize(360, 200)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #DEF0FF;
                border: 2px solid #CFE7FA;
                border-radius: 10px;
            }
        """)

        fl = QVBoxLayout(frame)
        fl.setAlignment(Qt.AlignCenter)
        fl.setSpacing(10)

        self.label = QLabel("Flow Value: 0.0")
        self.label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)

        self.arrow = FlowArrowCascade(count=6)

        fl.addWidget(self.label)
        fl.addWidget(self.arrow)
        layout.addWidget(frame)

        self.flow = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_flow)
        self.timer.start(1000)

    def update_flow(self):
        self.flow += 0.7
        if self.flow > 3:
            self.flow = 0

        self.label.setText(f"Flow Value: {self.flow:.1f}")
        self.arrow.set_active(self.flow > 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
