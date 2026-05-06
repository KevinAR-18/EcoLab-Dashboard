"""Custom glowing lamp widget used on the control-room page."""

from PySide6.QtCore import QEasingCurve, Property, QPropertyAnimation, Qt, QTimer, Signal, QSize
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget


class LampButton(QWidget):
    """Lamp-shaped widget with glow and pulse feedback."""

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
        self._pulse_dir = 1

        self.fade_anim = QPropertyAnimation(self, b"glowOpacity", self)
        self.fade_anim.setDuration(350)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.pulse_timer = QTimer(self)
        self.pulse_timer.setInterval(45)
        self.pulse_timer.timeout.connect(self._pulse)

        self.setFixedSize(QSize(self._size, int(self._size * 1.4)))

    def getGlowOpacity(self):
        return self._glow_alpha

    def setGlowOpacity(self, value):
        self._glow_alpha = value
        self.update()

    glowOpacity = Property(float, getGlowOpacity, setGlowOpacity)

    def _pulse(self):
        """Pulse the glow while the lamp is on."""
        step = 0.015
        self._glow_alpha += step * self._pulse_dir

        if self._glow_alpha >= 0.6:
            self._glow_alpha = 0.6
            self._pulse_dir = -1
        elif self._glow_alpha <= 0.35:
            self._glow_alpha = 0.35
            self._pulse_dir = 1

        self.update()

    def setOn(self, state: bool):
        """Apply a new logical state and start the visual transition."""
        if self._is_on == state:
            return

        self._is_on = state
        self.fade_anim.stop()

        if state:
            self.fade_anim.setStartValue(self._glow_alpha)
            self.fade_anim.setEndValue(0.3)
            self.fade_anim.finished.connect(self._startPulse)
            self.fade_anim.start()
        else:
            self.pulse_timer.stop()
            self.fade_anim.setStartValue(self._glow_alpha)
            self.fade_anim.setEndValue(0.0)
            self.fade_anim.start()

        self.toggled.emit(state)

    def _startPulse(self):
        if self._is_on:
            self._pulse_dir = 1
            self.pulse_timer.start()

    def isOn(self) -> bool:
        return self._is_on

    def mousePressEvent(self, event):
        if not self.isEnabled():
            return

        if event.button() == Qt.LeftButton:
            self.setOn(not self._is_on)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if not self.isEnabled():
            p.setOpacity(0.4)

        w, h = self.width(), self.height()
        cx = w // 2

        egg_w = int(w * 0.62)
        egg_h = int(h * 0.62)
        top = int(h * 0.05)

        base_radius = int(egg_w * 0.16)
        base_y = top + egg_h - 4

        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0, 0, 0, 20))
        p.drawEllipse(cx - base_radius, base_y + base_radius + 4,
                      base_radius * 2, 10)

        if self._glow_alpha > 0:
            for i, scale in enumerate((1.45, 1.25, 1.1)):
                alpha = int(255 * (self._glow_alpha * (0.55 - i * 0.15)))
                if alpha <= 0:
                    continue
                color = QColor(self.on_color)
                color.setAlpha(alpha)
                p.setBrush(color)
                p.drawEllipse(
                    cx - int(egg_w * scale / 2),
                    top - int(egg_h * scale * 0.08),
                    int(egg_w * scale),
                    int(egg_h * scale)
                )

        egg = QPainterPath()
        egg.moveTo(cx, top)
        egg.cubicTo(cx + egg_w * 0.55, top + egg_h * 0.15,
                    cx + egg_w * 0.5, top + egg_h * 0.72,
                    cx, top + egg_h)
        egg.cubicTo(cx - egg_w * 0.5, top + egg_h * 0.72,
                    cx - egg_w * 0.55, top + egg_h * 0.15,
                    cx, top)

        p.setBrush(self.on_color if self._is_on else self.off_color)
        p.setPen(Qt.NoPen)
        p.drawPath(egg)

        highlight = QColor(self.on_color if self._is_on else self.off_color).lighter(120)
        p.setBrush(highlight)
        p.drawEllipse(cx - egg_w * 0.32,
                      top + egg_h * 0.2,
                      egg_w * 0.64,
                      egg_h * 0.55)

        p.setPen(QPen(QColor(255, 255, 255, 185), 2))
        filament_y = top + egg_h * 0.48
        filament = QPainterPath()
        filament.moveTo(cx - egg_w * 0.22, filament_y)
        filament.cubicTo(cx - egg_w * 0.12, filament_y - egg_h * 0.28,
                         cx + egg_w * 0.12, filament_y - egg_h * 0.28,
                         cx + egg_w * 0.22, filament_y)
        p.drawPath(filament)

        p.setPen(QPen(QColor(0, 0, 0, 35), 1))
        p.setBrush(QColor("#D3D6DB"))
        p.drawEllipse(cx - base_radius, base_y,
                      base_radius * 2, base_radius * 2)

        p.setPen(QPen(QColor(0, 0, 0, 30), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(egg)

    def setChecked(self, state: bool):
        """Synchronize the widget from external state without changing ownership."""
        if self._is_on == state:
            return

        self._is_on = state
        self.fade_anim.stop()

        if state:
            self.fade_anim.setStartValue(self._glow_alpha)
            self.fade_anim.setEndValue(0.3)
            self.fade_anim.finished.connect(self._startPulse)
            self.fade_anim.start()
        else:
            self.pulse_timer.stop()
            self.fade_anim.setStartValue(self._glow_alpha)
            self.fade_anim.setEndValue(0.0)
            self.fade_anim.start()

        self.update()
