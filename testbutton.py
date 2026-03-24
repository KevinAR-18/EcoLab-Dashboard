import sys
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPainterPath, QLinearGradient, QRadialGradient, QPen, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class KCDCircleButton(QWidget):
    """
    Tombol KCD Bundar dengan Symbol Power
    - Lingkaran luar hitam
    - Dalam merah
    - ON: Merah terang + symbol O
    - OFF: Merah redup + symbol I
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_on = False
        self._led_alpha = 0.3  # LED mati = redup (30%)

        # Animasi LED
        self.led_anim = QPropertyAnimation(self, b"ledAlpha")
        self.led_anim.setDuration(300)
        self.led_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Size tombol - 220x144
        self.setFixedSize(220, 144)

    def getLedAlpha(self):
        return self._led_alpha

    def setLedAlpha(self, value):
        self._led_alpha = value
        self.update()

    ledAlpha = Property(float, getLedAlpha, setLedAlpha)

    def isOn(self):
        return self._is_on

    def setOn(self, state):
        if self._is_on == state:
            return

        self._is_on = state

        if state:
            # LED nyala terang (100%)
            self.led_anim.setStartValue(0.3)
            self.led_anim.setEndValue(1.0)
        else:
            # LED redup (30%)
            self.led_anim.setStartValue(self._led_alpha)
            self.led_anim.setEndValue(0.3)

        self.led_anim.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setOn(not self._is_on)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2

        # ================= LINGKARAN LUAR (Housing Hitam) =================
        outer_radius = 68

        # Shadow
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0, 0, 0, 40))
        p.drawEllipse(QPointF(cx + 3, cy + 3), outer_radius, outer_radius)

        # Housing luar - hitam metalik
        outer_grad = QRadialGradient(cx - 10, cy - 10, outer_radius)
        outer_grad.setColorAt(0, QColor("#3a3a3a"))
        outer_grad.setColorAt(0.7, QColor("#1a1a1a"))
        outer_grad.setColorAt(1, QColor("#0a0a0a"))

        p.setBrush(outer_grad)
        p.drawEllipse(QPointF(cx, cy), outer_radius, outer_radius)

        # Ring metalik
        ring_grad = QRadialGradient(cx - 5, cy - 5, outer_radius - 2)
        ring_grad.setColorAt(0, QColor("#4a4a4a"))
        ring_grad.setColorAt(1, QColor("#2a2a2a"))
        p.setBrush(ring_grad)
        p.drawEllipse(QPointF(cx, cy), outer_radius - 4, outer_radius - 4)

        # ================= LINGKARAN DALAM (Merah) =================
        inner_radius = 58

        # Base merah
        red_base = QColor("#8B0000")  # Dark red
        red_base.setAlphaF(0.3)  # Base opacity
        p.setPen(Qt.NoPen)
        p.setBrush(red_base)
        p.drawEllipse(QPointF(cx, cy), inner_radius, inner_radius)

        # LED merah dengan alpha
        led_color = QColor("#FF2222")
        led_color.setAlphaF(self._led_alpha)
        p.setBrush(led_color)
        p.drawEllipse(QPointF(cx, cy), inner_radius - 2, inner_radius - 2)

        # LED Glow effect saat terang
        if self._led_alpha > 0.5:
            glow_color = QColor("#FF4444")
            glow_color.setAlphaF((self._led_alpha - 0.5) * 0.6)

            for i in range(3):
                glow_r = (inner_radius - 2) + (i + 1) * 3
                p.setBrush(glow_color)
                p.drawEllipse(QPointF(cx, cy), glow_r, glow_r)

        # Highlight (kilatan)
        highlight_path = QPainterPath()
        highlight_path.addEllipse(QPointF(cx - 15, cy - 15), 25, 25)
        p.setBrush(QColor(255, 255, 255, 80))
        p.drawPath(highlight_path)

        # Inner frame
        p.setPen(QPen(QColor("#660000"), 2))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(QPointF(cx, cy), inner_radius - 3, inner_radius - 3)

        # ================= SYMBOL POWER (I / O) =================
        # Symbol di tengah tombol
        symbol_radius = 35

        p.setPen(QPen(QColor(255, 255, 255, 200), 5))
        p.setBrush(Qt.NoBrush)

        if self._is_on or self._led_alpha > 0.5:
            # Symbol O (lingkaran) - saat ON/close
            p.drawEllipse(QPointF(cx, cy), symbol_radius, symbol_radius)

            # Glow untuk symbol
            glow_symbol = QColor(255, 255, 255, 100)
            p.setPen(QPen(glow_symbol, 3))
            p.drawEllipse(QPointF(cx, cy), symbol_radius + 2, symbol_radius + 2)
        else:
            # Symbol I (garis vertikal) - saat OFF/open
            line_top = cy - symbol_radius + 5
            line_bottom = cy + symbol_radius - 5
            p.drawLine(QPointF(cx, line_top), QPointF(cx, line_bottom))

            # Glow untuk symbol I
            glow_symbol = QColor(255, 255, 255, 80)
            p.setPen(QPen(glow_symbol, 3))
            p.drawLine(QPointF(cx, line_top), QPointF(cx, line_bottom))


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KCD Circle Button - Power Symbol")
        self.setFixedSize(280, 200)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 10, 30, 10)
        layout.setSpacing(10)

        # Status label
        self.status_label = QLabel("Status: OPEN", self)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12pt;
                font-weight: bold;
                color: #2c3e50;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout.addWidget(self.status_label)

        # KCD Button
        self.button = KCDCircleButton(self)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connect
        self.button.led_anim.finished.connect(self.on_anim_finished)

    def on_anim_finished(self):
        """Update label setelah animasi selesai"""
        if self.button.isOn():
            self.status_label.setText("Status: CLOSE (ON)")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt;
                    font-weight: bold;
                    color: #FF4444;
                    qproperty-alignment: AlignCenter;
                }
            """)
        else:
            self.status_label.setText("Status: OPEN (OFF)")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 12pt;
                    font-weight: bold;
                    color: #2c3e50;
                    qproperty-alignment: AlignCenter;
                }
            """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
