import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QBrush, QPen, QPainter

class LampItem(QGraphicsEllipseItem):
    def __init__(self, x, y, w=40, h=40, label="Lampu"):
        super().__init__()
        self.setPos(x, y)
        self.default_w = w
        self.default_h = h
        self.is_on = False
        self.current_scale = 1.0
        self.target_scale = 1.0

        # warna default mati
        self.setBrush(QBrush(QColor("#A9A9A9")))
        self.setPen(QPen(Qt.black))
        self.setRect(-w/2, -h/2, w, h)  # pusat di tengah

        # Label
        self.text = QGraphicsTextItem(label)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setParentItem(self)
        self.text.setPos(-self.text.boundingRect().width()/2, h/2 + 5)

        # Timer animasi
        self.timer = QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.animate)
        self.animating = False

    def toggle(self):
        # ubah status nyala/mati
        self.is_on = not self.is_on
        self.setBrush(QBrush(QColor("#FFD700" if self.is_on else "#A9A9A9")))

        # animasi membesar sebentar
        self.current_scale = 1.0
        self.target_scale = 1.3
        self.animating = True
        self.timer.start()

    def animate(self):
        step = 0.05
        if self.animating:
            if self.current_scale < self.target_scale:
                self.current_scale += step
                if self.current_scale >= self.target_scale:
                    self.current_scale = self.target_scale
                    # balik ke ukuran awal
                    self.target_scale = 1.0
            elif self.current_scale > self.target_scale:
                self.current_scale -= step
                if self.current_scale <= self.target_scale:
                    self.current_scale = self.target_scale
                    self.animating = False
                    self.timer.stop()
            self.setRect(-self.default_w/2 * self.current_scale, -self.default_h/2 * self.current_scale,
                         self.default_w * self.current_scale, self.default_h * self.current_scale)
            self.text.setPos(-self.text.boundingRect().width()/2, self.default_h/2 * self.current_scale + 5)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lampu Animasi PySide6 (Flash Scale)")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.view = QGraphicsView()
        layout.addWidget(self.view)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing, True)

        self.lamps = []
        spacing = 70
        for i in range(5):
            lamp = LampItem(i*spacing, 0, label=f"Lampu {i+1}")
            self.scene.addItem(lamp)
            self.lamps.append(lamp)

        # Klik untuk toggle
        self.view.mousePressEvent = self.handle_click

    def handle_click(self, event):
        pos = self.view.mapToScene(event.position().toPoint())
        for lamp in self.lamps:
            if lamp.contains(lamp.mapFromScene(pos)):
                lamp.toggle()
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec())
