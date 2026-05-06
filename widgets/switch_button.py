from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import (
    Qt, QTimer, Signal, QSize,
    Property, QPropertyAnimation, QEasingCurve, QRectF, QPointF, QParallelAnimationGroup
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QPainterPath, QLinearGradient, QRadialGradient, QFont, QBrush
)
from math import cos, radians


class SwitchButton(QWidget):
    """
    Tombol switch model KCD dengan animasi dan safety cover.

    Karakter utamanya:
    - Bentuk kotak rounded
    - LED merah terang saat ON
    - Symbol `I` saat ON dan `O` saat OFF
    - Safety cover yang harus dibuka lebih dulu sebelum toggle
    """

    toggled = Signal(int, bool)  # switch_index, state

    def __init__(self, parent=None, switch_index=1, size=140):
        """Menyiapkan state switch, safety cover, dan animasi visualnya."""
        super().__init__(parent)

        self.switch_index = switch_index
        self._is_on = False
        self._led_alpha = 0.3  # LED mati = redup (30%)
        self._size = size

        # === Safety Cover ===
        self._cover_open = False  # False = cover tertutup, True = cover terbuka
        self._cover_angle = 0.0  # 0 = closed, 90 = fully open

        self.setCursor(Qt.PointingHandCursor)

        # === glow/pulse animation ===
        self._glow_alpha = 0.0
        self._pulse_dir = 1

        # === fade animation ===
        self.fade_anim = QPropertyAnimation(self, b"ledAlpha")
        self.fade_anim.setDuration(300)
        self.fade_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # === pulse timer ===
        self.pulse_timer = QTimer(self)
        self.pulse_timer.setInterval(45)
        self.pulse_timer.timeout.connect(self._pulse)

        # === cover animation ===
        self.cover_anim = QPropertyAnimation(self, b"coverAngle")
        self.cover_anim.setDuration(450)
        self.cover_anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.cover_anim.finished.connect(self._on_cover_anim_finished)

        # Timer untuk auto-close cover 5 detik setelah terbuka.
        self.cover_timer = QTimer(self)
        self.cover_timer.setSingleShot(True)
        self.cover_timer.timeout.connect(self.close_cover)

        # Size tombol default berbentuk kotak.
        self.setFixedSize(QSize(size, size))

    def getLedAlpha(self):
        """Mengembalikan alpha LED sebagai Qt property."""
        return self._led_alpha

    def setLedAlpha(self, value):
        """Mengubah alpha LED lalu meminta repaint widget."""
        self._led_alpha = value
        self.update()

    ledAlpha = Property(float, getLedAlpha, setLedAlpha)

    def getGlowOpacity(self):
        """Mengembalikan opacity glow sebagai Qt property."""
        return self._glow_alpha

    def setGlowOpacity(self, value):
        """Mengubah opacity glow lalu meminta repaint widget."""
        self._glow_alpha = value
        self.update()

    glowOpacity = Property(float, getGlowOpacity, setGlowOpacity)

    def getCoverAngle(self):
        """Mengembalikan sudut safety cover saat ini."""
        return self._cover_angle

    def setCoverAngle(self, value):
        """Mengubah sudut safety cover dan sinkronkan state open/close."""
        self._cover_angle = value
        self._cover_open = value >= 80  # Consider open if angle >= 80
        self.update()

    coverAngle = Property(float, getCoverAngle, setCoverAngle)

    def open_cover(self):
        """Membuka safety cover dengan animasi."""
        self.cover_anim.stop()
        self.cover_anim.setStartValue(self._cover_angle)
        self.cover_anim.setEndValue(90.0)
        self.cover_anim.start()
        # Start timer untuk auto-close setelah 5 detik.
        self.cover_timer.stop()
        self.cover_timer.start(5000)

    def close_cover(self):
        """Menutup safety cover dengan animasi."""
        self.cover_timer.stop()
        self.cover_anim.stop()
        self.cover_anim.setStartValue(self._cover_angle)
        self.cover_anim.setEndValue(0.0)
        self.cover_anim.start()

    def _on_cover_anim_finished(self):
        """Menyinkronkan state cover setelah animasi selesai."""
        if self._cover_angle >= 80:
            self._cover_open = True
        else:
            self._cover_open = False

    def _pulse(self):
        """Menjalankan pulse animation saat switch dalam keadaan ON."""
        step = 0.02
        self._glow_alpha += step * self._pulse_dir

        if self._glow_alpha >= 0.5:
            self._glow_alpha = 0.5
            self._pulse_dir = -1
        elif self._glow_alpha <= 0.3:
            self._glow_alpha = 0.3
            self._pulse_dir = 1

        # Update LED alpha berdasarkan glow saat ini.
        base_alpha = 0.3 + (self._glow_alpha * 0.7)
        self._led_alpha = base_alpha
        self.update()

    def setOn(self, state: bool):
        """Mengubah state switch lalu menjalankan animasi yang sesuai."""
        if self._is_on == state:
            return

        self._is_on = state
        self.fade_anim.stop()
        self.pulse_timer.stop()  # Stop pulse animation

        if state:
            # Fade in saat switch menyala.
            self.fade_anim.setStartValue(0.3)
            self.fade_anim.setEndValue(1.0)
            self.fade_anim.start()
        else:
            # Fade out saat switch mati.
            self.fade_anim.setStartValue(self._led_alpha)
            self.fade_anim.setEndValue(0.3)
            self.fade_anim.start()

        self.toggled.emit(self.switch_index, state)

    def _startPulse(self):
        """Memulai pulse animation saat switch dalam keadaan ON."""
        if self._is_on:
            self._pulse_dir = 1
            self.pulse_timer.start()

    def isOn(self) -> bool:
        """Mengembalikan state ON/OFF switch saat ini."""
        return self._is_on

    def mousePressEvent(self, event):
        """Menangani klik utama untuk toggle setelah cover terbuka."""
        if event.button() == Qt.LeftButton:
            if self._cover_open:
                # Cover sudah terbuka, jadi tombol boleh di-toggle.
                new_state = not self._is_on
                self.setOn(new_state)
                # Tutup cover otomatis setelah toggle.
                QTimer.singleShot(300, self.close_cover)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """Membuka safety cover lewat double-click."""
        if event.button() == Qt.LeftButton and not self._cover_open:
            # Jika cover masih tertutup, buka lebih dulu.
            self.open_cover()
        super().mouseDoubleClickEvent(event)

    def paintEvent(self, event):
        """Menggambar switch, LED, symbol power, dan safety cover."""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()

        # Scale factor berdasarkan ukuran widget.
        scale = self._size / 100.0

        # ================= KOTAK MERAH =================
        # Hitung area kotak utama dengan margin.
        margin_x = int(8 * scale)
        margin_y = int(6 * scale)
        rect_x = margin_x
        rect_y = margin_y
        rect_w = w - 2 * margin_x
        rect_h = h - 2 * margin_y
        corner_radius = int(12 * scale)

        # Gambar shadow dasar.
        p.setPen(Qt.NoPen)
        shadow_color = QColor(0, 0, 0, 50)
        p.setBrush(shadow_color)
        p.drawRoundedRect(QRectF(rect_x + 3, rect_y + 3, rect_w, rect_h), corner_radius, corner_radius)

        # Gambar base merah gelap.
        red_base = QColor("#8B0000")
        red_base.setAlphaF(0.3)
        p.setBrush(red_base)
        p.drawRoundedRect(QRectF(rect_x, rect_y, rect_w, rect_h), corner_radius, corner_radius)

        # Gambar LED merah dengan alpha dinamis.
        led_color = QColor("#FF2222")
        led_color.setAlphaF(self._led_alpha)

        p.setBrush(led_color)
        p.drawRoundedRect(QRectF(rect_x, rect_y, rect_w, rect_h), corner_radius, corner_radius)

        # Tambahkan glow effect saat switch aktif.
        if self._glow_alpha > 0:
            glow_color = QColor("#FF4444")  # Warna glow merah
            glow_color.setAlphaF(self._glow_alpha * 0.4)

            # Glow di sekitar tombol.
            for i in range(2):
                glow_offset = (i + 1) * 3
                p.setBrush(glow_color)
                p.drawRoundedRect(
                    QRectF(rect_x - glow_offset, rect_y - glow_offset,
                           rect_w + 2 * glow_offset, rect_h + 2 * glow_offset),
                    corner_radius + glow_offset, corner_radius + glow_offset
                )

        # Glow berlapis di luar tombol, lebih terang saat ON.
        glow_base_alpha = 0.1 + (self._led_alpha * 0.3)

        # Warna glow berubah tergantung state.
        if self._is_on or self._led_alpha > 0.5:
            glow_color_base = QColor("#FF3333")  # Merah saat ON
        else:
            glow_color_base = QColor("#808080")  # Abu-abu saat OFF

        for i in range(3):
            glow_offset = (i + 1) * 4
            glow_layer = QColor(glow_color_base)
            glow_layer.setAlphaF(glow_base_alpha / (i + 1))
            p.setBrush(glow_layer)
            p.drawRoundedRect(
                QRectF(rect_x - glow_offset, rect_y - glow_offset,
                       rect_w + 2 * glow_offset, rect_h + 2 * glow_offset),
                corner_radius + glow_offset, corner_radius + glow_offset
            )

        # Tambahkan highlight hanya saat ON.
        if self._is_on or self._led_alpha > 0.5:
            highlight_size = int(rect_w * 0.30)
            highlight_offset_x = int(rect_w * 0.15)  # 15% dari kiri
            highlight_offset_y = int(rect_h * 0.15)  # 15% dari atas
            highlight_path = QPainterPath()
            highlight_path.addRoundedRect(
                QRectF(rect_x + highlight_offset_x, rect_y + highlight_offset_y,
                       highlight_size, highlight_size),
                corner_radius / 2, corner_radius / 2
            )
            p.setBrush(QColor(255, 255, 255, 50))
            p.drawPath(highlight_path)

        # Gambar border/frame dalam.
        p.setPen(QPen(QColor("#660000"), int(2 * scale)))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(rect_x + 2, rect_y + 2, rect_w - 4, rect_h - 4), corner_radius - 2, corner_radius - 2)

        # ================= SYMBOL POWER (I / O) =================
        cx, cy = w // 2, h // 2
        symbol_size = int(30 * scale)

        p.setPen(QPen(QColor(255, 255, 255, 220), int(5 * scale), Qt.SolidLine, Qt.RoundCap))
        p.setBrush(Qt.NoBrush)

        if self._is_on or self._led_alpha > 0.5:
            # Symbol I (garis vertikal) saat ON.
            line_top = cy - symbol_size + 6
            line_bottom = cy + symbol_size - 6
            p.drawLine(QPointF(cx, line_top), QPointF(cx, line_bottom))
        else:
            # Symbol O (lingkaran) saat OFF.
            p.drawEllipse(QPointF(cx, cy), symbol_size, symbol_size)

        # ================= SAFETY COVER (Kaca Penutup) =================
        if self._cover_angle < 90:
            p.save()

            # Pivot point di kiri tombol.
            pivot_x = rect_x
            pivot_y = rect_y + rect_h

            # Transform untuk animasi flip dari kiri bawah.
            p.translate(pivot_x, pivot_y)

            # Skala horizontal berdasarkan angle untuk efek flip 3D.
            scale_x = cos(radians(self._cover_angle))
            p.scale(scale_x, 1.0)

            p.translate(-pivot_x, -pivot_y)

            # Gambar cover transparan.
            cover_opacity = int(180 * (1 - self._cover_angle / 90))  # Fade out saat terbuka

            # Warna cover berubah sesuai state ON/OFF.
            if self._is_on or self._led_alpha > 0.5:
                cover_color = QColor(255, 200, 200, cover_opacity)  # Merah muda kaca
                border_color = QColor(200, 100, 100, cover_opacity)
            else:
                cover_color = QColor(200, 220, 255, cover_opacity)  # Biru muda kaca
                border_color = QColor(100, 150, 200, cover_opacity)

            p.setPen(QPen(border_color, int(3 * scale)))
            p.setBrush(cover_color)
            p.drawRoundedRect(QRectF(rect_x, rect_y, rect_w, rect_h), corner_radius, corner_radius)

            # Gambar handle/grip di tengah cover.
            handle_size = int(20 * scale)
            handle_rect = QRectF(cx - handle_size, cy - handle_size / 2, handle_size * 2, handle_size)

            # Gradient untuk handle.
            handle_grad = QLinearGradient(handle_rect.left(), handle_rect.top(),
                                        handle_rect.left(), handle_rect.bottom())
            handle_grad.setColorAt(0, QColor(180, 180, 180, cover_opacity))
            handle_grad.setColorAt(0.5, QColor(220, 220, 220, cover_opacity))
            handle_grad.setColorAt(1, QColor(180, 180, 180, cover_opacity))

            p.setPen(QPen(QColor(80, 80, 80, cover_opacity), 2))
            p.setBrush(handle_grad)
            p.drawRoundedRect(handle_rect, 5, 5)

            # Teks "OPEN" kecil di atas handle.
            if self._cover_angle < 45:
                p.setPen(QColor(50, 50, 50, cover_opacity))
                font = QFont()
                font.setPixelSize(int(10 * scale))
                font.setBold(True)
                p.setFont(font)
                p.drawText(QRectF(cx - 30, cy - 40, 60, 20), Qt.AlignCenter, "OPEN")

            # Reflection/glare pada cover.
            
            glare_path = QPainterPath()
            glare_size = int(rect_w * 0.3)
            glare_path.addRoundedRect(
                QRectF(rect_x + 8, rect_y + 8, glare_size, glare_size * 0.6),
                corner_radius / 2, corner_radius / 2
            )
            p.setBrush(QColor(255, 255, 255, int(100 * (1 - self._cover_angle / 90))))
            p.setPen(Qt.NoPen)
            p.drawPath(glare_path)

            p.restore()
"""Widget switch Smart Socket dengan safety cover dan animasi visual."""
