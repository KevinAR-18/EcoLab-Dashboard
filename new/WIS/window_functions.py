from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

class WindowFunctions:
    def __init__(self, main_window, drop_shadow_frame):
        """
        Initialize custom window functionality.

        :param main_window: Instance of QMainWindow
        :param drop_shadow_frame: Frame to apply drop shadow and handle dragging
        """
        self.main_window = main_window
        self.drop_shadow_frame = drop_shadow_frame
        self.is_maximized = False

        # Remove default title bar
        self.main_window.setWindowFlag(Qt.FramelessWindowHint)
        self.main_window.setAttribute(Qt.WA_TranslucentBackground)

        # Add drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self.main_window)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.drop_shadow_frame.setGraphicsEffect(self.shadow)

        # Bind drag functionality
        self.drop_shadow_frame.mouseMoveEvent = self.move_window

    def toggle_maximize_restore(self, maximize_button):
        """
        Toggle between maximized and restored window states.

        :param maximize_button: Button used to toggle states (for tooltip updates)
        """
        if self.is_maximized:
            self.main_window.showNormal()
            self.is_maximized = False
            maximize_button.setToolTip("Maximize")
        else:
            self.main_window.showFullScreen()
            self.is_maximized = True
            maximize_button.setToolTip("Restore")

    def move_window(self, event):
        """
        Enable dragging of the frameless window.

        :param event: Mouse move event
        """
        if event.buttons() == Qt.LeftButton and not self.is_maximized:
            self.main_window.move(self.main_window.pos() + event.globalPosition().toPoint() - self.main_window.dragPos)
            self.main_window.dragPos = event.globalPosition().toPoint()
            event.accept()
