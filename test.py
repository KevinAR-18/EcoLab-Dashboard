from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PySide6.QtGui import QPainter, QColor, QPixmap, QFont
from PySide6.QtCore import Qt, QSize
import sys

class EnergyWidget(QWidget):
    """Widget individual untuk setiap elemen energi (panel, grid, rumah, dsb)"""
    def __init__(self, title, color_on="#66B3FF", color_off="#A0A0A0"):
        super().__init__()
        self.title = title
        self.color_on = color_on
        self.color_off = color_off
        self.is_on = False

        self.setFixedSize(150, 150)
        self.label = QLabel(self.title, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.label.setStyleSheet("color: white;")

        self.icon = QLabel(self)
        self.icon.setFixedSize(70, 70)
        self.icon.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.icon, alignment=Qt.AlignCenter)
        layout.addWidget(self.label)

        self.update_icon()

    def update_icon(self):
        """Ganti warna ikon berdasarkan status"""
        pix = QPixmap(self.icon.size())
        pix.fill(Qt.transparent)

        painter = QPainter(pix)
        color = QColor(self.color_on if self.is_on else self.color_off)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(5, 5, 60, 60)
        painter.end()

        self.icon.setPixmap(pix)

    def toggle(self):
        """Ganti ON/OFF"""
        self.is_on = not self.is_on
        self.update_icon()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EcoLab Energy Dashboard")
        self.setFixedSize(900, 500)
        self.setStyleSheet("background-color: #0F1C2E; color: white;")

        # Elemen energi utama
        self.widgets = {
            "Photovoltaic": EnergyWidget("Photovoltaic Output"),
            "Charging": EnergyWidget("Charging"),
            "Discharging": EnergyWidget("Discharging"),
            "Load": EnergyWidget("Load Consumption"),
            "Grid": EnergyWidget("Power Grid"),
        }

        # Layout utama
        grid = QGridLayout()
        grid.setSpacing(30)

        row, col = 0, 0
        for i, w in enumerate(self.widgets.values()):
            grid.addWidget(w, row, col, alignment=Qt.AlignCenter)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Tombol kontrol
        control_layout = QHBoxLayout()
        for key, w in self.widgets.items():
            btn = QPushButton(f"Toggle {key}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E4976;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 6px 14px;
                }
                QPushButton:hover {
                    background-color: #3674B5;
                }
            """)
            btn.clicked.connect(w.toggle)
            control_layout.addWidget(btn)

        layout = QVBoxLayout(self)
        layout.addLayout(grid)
        layout.addLayout(control_layout)
        layout.addStretch()

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
