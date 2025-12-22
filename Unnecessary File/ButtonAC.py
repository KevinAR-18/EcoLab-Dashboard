from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer, Property, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont


def blend_color(c1: QColor, c2: QColor, t: float) -> QColor:
    """Campur dua warna (0.0–1.0)"""
    r = c1.red() + (c2.red() - c1.red()) * t
    g = c1.green() + (c2.green() - c1.green()) * t
    b = c1.blue() + (c2.blue() - c1.blue()) * t
    return QColor(int(r), int(g), int(b))


class SwitchButton(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None, width=90, height=42):
        super().__init__(parent)
        self.setFixedSize(width, height)

        # Warna pastel
        self.off_color = QColor("#DCE9F5")
        self.on_color = QColor("#A5E8FF")
        self._handle_pos = 3
        self._is_on = False
        self._radius = height // 2

        # Warna transisi
        self._bg_color = self.off_color

        # Animasi posisi bola
        self._anim_pos = QPropertyAnimation(self, b"handle_pos", self)
        self._anim_pos.setDuration(300)
        self._anim_pos.setEasingCurve(QEasingCurve.OutCubic)

        # Timer untuk animasi warna
        self._color_timer = QTimer(self)
        self._color_timer.timeout.connect(self.update_color)
        self._anim_progress = 0.0
        self._color_timer.setInterval(15)

    # Properti posisi bola
    def get_handle_pos(self):
        return self._handle_pos

    def set_handle_pos(self, pos):
        self._handle_pos = pos
        self.update()

    handle_pos = Property(float, get_handle_pos, set_handle_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()

    def toggle(self):
        self._is_on = not self._is_on
        self._anim_progress = 0.0
        self._color_timer.start()
        self.animate_switch()
        self.toggled.emit(self._is_on)

    def animate_switch(self):
        start = 3 if self._is_on else self.width() - self.height() + 3
        end = self.width() - self.height() + 3 if self._is_on else 3
        self._anim_pos.stop()
        self._anim_pos.setStartValue(start)
        self._anim_pos.setEndValue(end)
        self._anim_pos.start()

    def update_color(self):
        self._anim_progress += 0.05
        if self._anim_progress >= 1.0:
            self._anim_progress = 1.0
            self._color_timer.stop()

        if self._is_on:
            self._bg_color = blend_color(self.off_color, self.on_color, self._anim_progress)
        else:
            self._bg_color = blend_color(self.on_color, self.off_color, self._anim_progress)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.setBrush(QBrush(self._bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)

        # Handle (bola putih)
        handle_diam = self.height() - 6
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(QColor(210, 210, 210), 1))
        painter.drawEllipse(self._handle_pos, 3, handle_diam, handle_diam)


class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AC Switch Modern Animated")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        frame = QFrame()
        frame.setObjectName("acFrame")
        frame.setStyleSheet("""
            QFrame#acFrame {
                background-color: #def0ff;
                border: 2px solid #cfe7fa;
                border-radius: 10px;
            }
        """)

        vbox = QVBoxLayout(frame)
        vbox.setAlignment(Qt.AlignCenter)

        label = QLabel("AC Control ❄️")
        label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)

        self.switch = SwitchButton()
        self.status = QLabel("AC: OFF")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(QFont("Segoe UI", 10))

        vbox.addWidget(label)
        vbox.addWidget(self.switch)
        vbox.addWidget(self.status)

        layout.addWidget(frame)

        self.switch.toggled.connect(self.update_status)

    def update_status(self, state):
        self.status.setText("AC: ON ❄️" if state else "AC: OFF")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
