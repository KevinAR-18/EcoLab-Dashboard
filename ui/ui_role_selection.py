"""
Role Selection Dialog
Popup dialog untuk memilih dashboard atau admin panel setelah admin login
"""
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)


class RoleSelectionDialog(QDialog):
    """
    Popup dialog untuk memilih dashboard atau admin panel
    Desain simple dan clean mengikuti tema login page
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Destination")
        self.setModal(True)
        self.setFixedSize(400, 250)

        # Set frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._setup_ui()
        self._setup_animations()

    def _setup_ui(self):
        """Setup UI dengan styling mirip login page"""
        # Main container
        self.container = QFrame()
        self.container.setObjectName("dialogContainer")
        self.container.setStyleSheet("""
            QFrame#dialogContainer {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #E1F2FB,
                    stop:1 #F1F9F9
                );
                border-radius: 18px;
                border: 2px solid #005C99;
            }
        """)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        # Title
        title = QLabel("Welcome Admin! 🎉")
        title.setObjectName("dialogTitle")
        title.setStyleSheet("""
            QLabel#dialogTitle {
                font-size: 18pt;
                font-weight: bold;
                color: #1f3c5a;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Where do you want to go?")
        subtitle.setObjectName("dialogSubtitle")
        subtitle.setStyleSheet("""
            QLabel#dialogSubtitle {
                font-size: 11pt;
                color: #4a647d;
                background: transparent;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Spacer
        layout.addSpacing(10)

        # Buttons container
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        # Dashboard Button
        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setObjectName("dashboardBtn")
        self.dashboard_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dashboard_btn.setMinimumHeight(45)
        self.dashboard_btn.setStyleSheet("""
            QPushButton#dashboardBtn {
                background-color: #4c8ed9;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton#dashboardBtn:hover {
                background-color: #3979c7;
            }
            QPushButton#dashboardBtn:pressed {
                background-color: #2d6ab3;
            }
        """)
        self.dashboard_btn.clicked.connect(self.select_dashboard)
        buttons_layout.addWidget(self.dashboard_btn)

        # Admin Panel Button
        self.admin_btn = QPushButton("Admin Panel")
        self.admin_btn.setObjectName("adminBtn")
        self.admin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.admin_btn.setMinimumHeight(45)
        self.admin_btn.setStyleSheet("""
            QPushButton#adminBtn {
                background-color: #2b6cb0;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton#adminBtn:hover {
                background-color: #1e4f8a;
            }
            QPushButton#adminBtn:pressed {
                background-color: #174173;
            }
        """)
        self.admin_btn.clicked.connect(self.select_admin_panel)
        buttons_layout.addWidget(self.admin_btn)

        layout.addLayout(buttons_layout)

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        self.choice = None

    def _setup_animations(self):
        """Setup fade in animation"""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def select_dashboard(self):
        """User memilih dashboard"""
        self.choice = "dashboard"
        self.accept()

    def select_admin_panel(self):
        """User memilih admin panel"""
        self.choice = "admin_panel"
        self.accept()

    def center_dialog(self):
        """Center dialog on screen"""
        from PySide6.QtWidgets import QApplication

        screen = QApplication.primaryScreen().availableGeometry()
        dialog_rect = self.geometry()

        # Calculate center position
        x = (screen.width() - dialog_rect.width()) // 2
        y = (screen.height() - dialog_rect.height()) // 2

        # Set position
        self.move(x, y)

    def exec_with_animation(self):
        """Show dialog dengan fade in effect"""
        self.center_dialog()
        self.fade_animation.start()
        return self.exec()
