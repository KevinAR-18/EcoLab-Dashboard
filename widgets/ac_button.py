"""Widget toggle AC custom dengan animasi untuk halaman control room."""

from PySide6.QtCore import QEasingCurve, Property, QPropertyAnimation, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


def blend_color(c1: QColor, c2: QColor, t: float) -> QColor:
    """Mencampur dua warna secara linear untuk animasi transisi background."""
    r = c1.red() + (c2.red() - c1.red()) * t
    g = c1.green() + (c2.green() - c1.green()) * t
    b = c1.blue() + (c2.blue() - c1.blue()) * t
    return QColor(int(r), int(g), int(b))


class ACButton(QWidget):
    """Tombol switch AC animatif yang berperilaku seperti toggle ringan."""

    toggled = Signal(bool)

    def __init__(self, parent=None, width=90, height=42):
        """Menyiapkan tampilan, warna, dan animasi dasar tombol AC."""
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)

        self.off_color = QColor("#DCE9F5")
        self.on_color = QColor("#A5E8FF")

        self._bg_color = self.off_color
        self._is_on = False
        self._radius = height // 2
        self._handle_pos = 3

        self._anim_pos = QPropertyAnimation(self, b"handle_pos", self)
        self._anim_pos.setDuration(260)
        self._anim_pos.setEasingCurve(QEasingCurve.OutCubic)

        self._anim_progress = 0.0
        self._color_timer = QTimer(self)
        self._color_timer.setInterval(15)
        self._color_timer.timeout.connect(self._update_color)

    def get_handle_pos(self):
        """Mengembalikan posisi handle sebagai Qt property yang bisa dianimasikan."""
        return self._handle_pos

    def set_handle_pos(self, pos):
        """Mengubah posisi handle lalu meminta repaint widget."""
        self._handle_pos = pos
        self.update()

    handle_pos = Property(float, get_handle_pos, set_handle_pos)

    def mousePressEvent(self, event):
        """Menangani klik mouse untuk toggle state saat widget aktif."""
        if not self.isEnabled():
            return

        if event.button() == Qt.LeftButton:
            self.toggle()

    def toggle(self):
        """Membalik state lokal lalu memulai animasi switch."""
        self._is_on = not self._is_on
        self._anim_progress = 0.0
        self._color_timer.start()
        self._animate_switch()
        self.toggled.emit(self._is_on)

    def isOn(self):
        """Mengembalikan state ON/OFF tombol AC saat ini."""
        return self._is_on

    def setOn(self, state: bool):
        """Menyinkronkan widget dengan perubahan state dari luar."""
        if self._is_on == state:
            return
        self._is_on = state
        self._animate_switch()
        self._color_timer.start()
        self.toggled.emit(state)

    def _animate_switch(self):
        """Menjalankan animasi posisi handle, sementara warna diupdate timer."""
        start = self._handle_pos
        end = self.width() - self.height() + 3 if self._is_on else 3

        self._anim_pos.stop()
        self._anim_pos.setStartValue(start)
        self._anim_pos.setEndValue(end)
        self._anim_pos.start()

    def _update_color(self):
        """Mengubah warna background bertahap selama animasi berjalan."""
        self._anim_progress += 0.06
        if self._anim_progress >= 1.0:
            self._anim_progress = 1.0
            self._color_timer.stop()

        if self._is_on:
            self._bg_color = blend_color(self.off_color, self.on_color, self._anim_progress)
        else:
            self._bg_color = blend_color(self.on_color, self.off_color, self._anim_progress)

        self.update()

    def paintEvent(self, event):
        """Menggambar track rounded dan handle bulat tombol AC."""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        if not self.isEnabled():
            p.setOpacity(0.4)

        p.setBrush(QBrush(self._bg_color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), self._radius, self._radius)

        diameter = self.height() - 6
        p.setBrush(Qt.white)
        p.setPen(QPen(QColor(200, 200, 200), 1))
        p.drawEllipse(self._handle_pos, 3, diameter, diameter)

    def setChecked(self, state: bool):
        """Menyinkronkan state AC dari MQTT atau restore state tanpa logika tambahan."""
        if self._is_on == state:
            return

        self._is_on = state
        self._animate_switch()
        self._color_timer.start()
        self.update()
