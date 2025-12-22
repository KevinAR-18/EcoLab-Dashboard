# from PySide6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QFrame, QLabel
# )
# from PySide6.QtCore import Qt, QTimer, Signal, QSize
# from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QPainterPath, QFont


# class LampButton(QWidget):
#     toggled = Signal(bool)

#     def __init__(self, parent=None, size=100, on_color=QColor("#FFD166"), off_color=QColor("#D6E6EE")):
#         super().__init__(parent)
#         self.setCursor(Qt.PointingHandCursor)
#         self._is_on = False
#         self._size = size
#         self.on_color = on_color
#         self.off_color = off_color

#         # glow animation params
#         self._glow_alpha = 0.0
#         self._glow_dir = 1

#         self.timer = QTimer(self)
#         self.timer.setInterval(50)
#         self.timer.timeout.connect(self._pulse)

#         self.setFixedSize(QSize(self._size, int(self._size * 1.2)))

#     def sizeHint(self):
#         return QSize(self._size, int(self._size * 1.2))

#     def _pulse(self):
#         # pulse glow alpha between 0.15 .. 0.6
#         step = 0.03
#         self._glow_alpha += step * self._glow_dir
#         if self._glow_alpha >= 0.6:
#             self._glow_alpha = 0.6
#             self._glow_dir = -1
#         elif self._glow_alpha <= 0.15:
#             self._glow_alpha = 0.15
#             self._glow_dir = 1
#         self.update()

#     def setOn(self, state: bool):
#         if self._is_on == state:
#             return
#         self._is_on = state
#         if state:
#             self.timer.start()
#             self._glow_alpha = 0.25
#             self._glow_dir = 1
#         else:
#             self.timer.stop()
#             self._glow_alpha = 0.0
#         self.toggled.emit(self._is_on)
#         self.update()

#     def isOn(self) -> bool:
#         return self._is_on

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.setOn(not self._is_on)
#         super().mousePressEvent(event)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         w, h = self.width(), self.height()

#         # coordinates for bulb
#         bulb_radius = int(min(w, h) * 0.36)
#         bulb_cx = w // 2
#         bulb_cy = int(h * 0.5)   # sedikit lebih ke tengah

#         # draw subtle shadow
#         shadow_color = QColor(0, 0, 0, 18)
#         painter.setBrush(QBrush(shadow_color))
#         painter.setPen(Qt.NoPen)
#         painter.drawEllipse(bulb_cx - bulb_radius - 4, bulb_cy + bulb_radius - 4, (bulb_radius * 2) + 8, 12)

#         # bulb off base
#         painter.setPen(Qt.NoPen)
#         painter.setBrush(QBrush(self.off_color))
#         painter.drawEllipse(bulb_cx - bulb_radius, bulb_cy - bulb_radius, bulb_radius * 2, bulb_radius * 2)

#         # draw glow if on
#         if self._is_on and self._glow_alpha > 0:
#             glow = QColor(self.on_color)
#             glow.setAlphaF(self._glow_alpha)
#             painter.setBrush(QBrush(glow))
#             painter.setPen(Qt.NoPen)
#             for i, scale in enumerate((1.6, 1.25, 1.05)):
#                 alpha = int(255 * (self._glow_alpha * (0.5 - i * 0.15)))
#                 if alpha < 0:
#                     alpha = 0
#                 c = QColor(self.on_color)
#                 c.setAlpha(alpha)
#                 painter.setBrush(QBrush(c))
#                 r = int(bulb_radius * scale)
#                 painter.drawEllipse(bulb_cx - r, bulb_cy - r, r * 2, r * 2)

#         # inner highlight (bright when on)
#         if self._is_on:
#             painter.setBrush(QBrush(self.on_color))
#         else:
#             tint = QColor(self.off_color).lighter(108)
#             painter.setBrush(QBrush(tint))
#         painter.setPen(Qt.NoPen)
#         painter.drawEllipse(bulb_cx - bulb_radius + 6, bulb_cy - bulb_radius + 6, (bulb_radius - 6) * 2, (bulb_radius - 6) * 2)

#         # filament / inner detail
#         painter.setPen(QPen(QColor(255, 255, 255, 180), 2))
#         path = QPainterPath()
#         path.moveTo(bulb_cx - bulb_radius * 0.35, bulb_cy + bulb_radius * 0.05)
#         path.cubicTo(bulb_cx - bulb_radius * 0.15, bulb_cy - bulb_radius * 0.25,
#                      bulb_cx + bulb_radius * 0.15, bulb_cy - bulb_radius * 0.25,
#                      bulb_cx + bulb_radius * 0.35, bulb_cy + bulb_radius * 0.05)
#         painter.drawPath(path)

#         # outline subtle
#         painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
#         painter.setBrush(Qt.NoBrush)
#         painter.drawEllipse(bulb_cx - bulb_radius, bulb_cy - bulb_radius, bulb_radius * 2, bulb_radius * 2)

#     def enterEvent(self, event):
#         # optional hover effect
#         if not self._is_on:
#             self.off_color = QColor("#E9F3FB")
#             self.update()

#     def leaveEvent(self, event):
#         if not self._is_on:
#             self.off_color = QColor("#D6E6EE")
#             self.update()


# # Example usage
# class DemoWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Lamp Button (No Base)")
#         self.resize(800, 480)

#         main_layout = QVBoxLayout(self)
#         frame = QFrame()
#         frame.setObjectName("flowFrame")
#         frame.setStyleSheet("""
#             QFrame#flowFrame {
#                 background-color: #def0ff;
#                 border: 2px solid #cfe7fa;
#                 border-radius: 10px;
#             }
#         """)
#         frame_layout = QVBoxLayout(frame)
#         frame_layout.setAlignment(Qt.AlignCenter)

#         title = QLabel("Modern Lamp")
#         title.setAlignment(Qt.AlignCenter)
#         title.setFont(QFont("Segoe UI", 12, QFont.Bold))

#         lamp = LampButton(size=120, on_color=QColor("#FFD166"), off_color=QColor("#F1F6FA"))
#         lamp.toggled.connect(lambda s: print("Lamp is on?", s))

#         frame_layout.addWidget(title)
#         frame_layout.addWidget(lamp)
#         main_layout.addWidget(frame)


# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     w = DemoWindow()
#     w.show()
#     sys.exit(app.exec())
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFrame, QLabel
)
from PySide6.QtCore import Qt, QTimer, Signal, QSize
from PySide6.QtGui import (
    QPainter, QBrush, QColor, QPen,
    QPainterPath, QFont
)


class LampButton(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None, size=120,
                 on_color=QColor("#FFD166"),
                 off_color=QColor("#E6EEF5")):
        super().__init__(parent)

        self.setCursor(Qt.PointingHandCursor)
        self._is_on = False
        self._size = size
        self.on_color = on_color
        self.off_color = off_color

        self._glow_alpha = 0.0
        self._glow_dir = 1

        self.timer = QTimer(self)
        self.timer.setInterval(45)
        self.timer.timeout.connect(self._pulse)

        self.setFixedSize(QSize(self._size, int(self._size * 1.4)))

    def sizeHint(self):
        return QSize(self._size, int(self._size * 1.4))

    def _pulse(self):
        step = 0.03
        self._glow_alpha += step * self._glow_dir
        if self._glow_alpha >= 0.6:
            self._glow_alpha = 0.6
            self._glow_dir = -1
        elif self._glow_alpha <= 0.2:
            self._glow_alpha = 0.2
            self._glow_dir = 1
        self.update()

    def setOn(self, state: bool):
        if self._is_on == state:
            return
        self._is_on = state
        if state:
            self.timer.start()
            self._glow_alpha = 0.3
        else:
            self.timer.stop()
            self._glow_alpha = 0.0
        self.toggled.emit(state)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setOn(not self._is_on)

    # ================= PAINT =================
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx = w // 2

        egg_w = int(w * 0.62)
        egg_h = int(h * 0.62)
        top = int(h * 0.05)

        base_radius = int(egg_w * 0.16)
        base_y = top + egg_h - 4

        # ---------- SHADOW ----------
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0, 0, 0, 20))
        p.drawEllipse(cx - base_radius,
                      base_y + base_radius + 4,
                      base_radius * 2, 10)

        # ---------- GLOW ----------
        if self._is_on:
            for i, scale in enumerate((1.45, 1.25, 1.1)):
                alpha = int(255 * (self._glow_alpha * (0.55 - i * 0.15)))
                if alpha <= 0:
                    continue
                g = QColor(self.on_color)
                g.setAlpha(alpha)
                p.setBrush(g)
                p.drawEllipse(
                    cx - int(egg_w * scale / 2),
                    top - int(egg_h * scale * 0.08),
                    int(egg_w * scale),
                    int(egg_h * scale)
                )

        # ---------- EGG BODY ----------
        egg = QPainterPath()
        egg.moveTo(cx, top)
        egg.cubicTo(cx + egg_w * 0.55, top + egg_h * 0.15,
                     cx + egg_w * 0.5, top + egg_h * 0.72,
                     cx, top + egg_h)
        egg.cubicTo(cx - egg_w * 0.5, top + egg_h * 0.72,
                     cx - egg_w * 0.55, top + egg_h * 0.15,
                     cx, top)

        p.setPen(Qt.NoPen)
        p.setBrush(self.on_color if self._is_on else self.off_color)
        p.drawPath(egg)

        # ---------- INNER HIGHLIGHT ----------
        hi = QColor(self.on_color if self._is_on else self.off_color).lighter(120)
        p.setBrush(hi)
        p.drawEllipse(
            cx - egg_w * 0.32,
            top + egg_h * 0.2,
            egg_w * 0.64,
            egg_h * 0.55
        )

        # ---------- FILAMENT (DECORATIVE) ----------
        p.setPen(QPen(QColor(255, 255, 255, 185), 2))
        fy = top + egg_h * 0.48

        fil = QPainterPath()
        fil.moveTo(cx - egg_w * 0.22, fy)
        fil.cubicTo(cx - egg_w * 0.12, fy - egg_h * 0.28,
                     cx + egg_w * 0.12, fy - egg_h * 0.28,
                     cx + egg_w * 0.22, fy)

        fil.moveTo(cx - egg_w * 0.18, fy + 14)
        fil.cubicTo(cx - egg_w * 0.06, fy - egg_h * 0.05,
                     cx + egg_w * 0.06, fy - egg_h * 0.05,
                     cx + egg_w * 0.18, fy + 14)

        p.drawPath(fil)

        # ---------- SMALL BASE (RING / DOT) ----------
        p.setPen(QPen(QColor(0, 0, 0, 35), 1))
        p.setBrush(QColor("#D3D6DB"))
        p.drawEllipse(
            cx - base_radius,
            base_y,
            base_radius * 2,
            base_radius * 2
        )

        # ---------- OUTLINE ----------
        p.setPen(QPen(QColor(0, 0, 0, 30), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(egg)


# ================= DEMO =================
class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Egg Lamp – Minimal Base")
        self.resize(800, 480)

        layout = QVBoxLayout(self)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #DEF0FF;
                border: 2px solid #CFE7FA;
                border-radius: 12px;
            }
        """)

        fl = QVBoxLayout(frame)
        fl.setAlignment(Qt.AlignCenter)

        title = QLabel("Egg Lamp ")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        lamp = LampButton()
        lamp.toggled.connect(lambda s: print("Lamp ON:", s))

        fl.addWidget(title)
        fl.addWidget(lamp)
        layout.addWidget(frame)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
