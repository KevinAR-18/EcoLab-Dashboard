"""Shared frameless-window behaviors used by EcoLab top-level windows."""

from PySide6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QTimer, Qt


class UIFunctions:
    """Bundle repeated window interactions such as dragging and menu animation."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.drag_pos = None
        self.is_maximized = False
        self.menu_expanded = False
        # Keep a reference so the animation is not garbage-collected mid-transition.
        self.animation = None

    def toggle_max_restore(self):
        """Toggle the current window between maximized and normal size."""
        if self.is_maximized:
            self.main_window.showNormal()
            self.is_maximized = False
        else:
            self.main_window.showMaximized()
            self.is_maximized = True

    def mouse_press(self, event):
        """Remember the drag origin when the user presses the title area."""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouse_move(self, event):
        """Move the frameless window while the left mouse button is held."""
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            if self.is_maximized:
                self.toggle_max_restore()

            self.main_window.move(
                self.main_window.pos()
                + event.globalPosition().toPoint()
                - self.drag_pos
            )
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouse_double_click(self, event):
        """Use a delayed toggle to avoid fighting with the native double-click event."""
        if event.type() == QEvent.MouseButtonDblClick:
            QTimer.singleShot(100, self.toggle_max_restore)

    def toggle_left_menu(self, menu):
        """Animate the left navigation menu between collapsed and expanded widths."""
        collapsed_width = 60
        expanded_width = 240
        current_width = menu.width()

        self.animation = QPropertyAnimation(menu, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(current_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        if self.menu_expanded:
            menu.setMinimumWidth(0)
            self.animation.setEndValue(collapsed_width)
            self.menu_expanded = False
        else:
            menu.setMaximumWidth(expanded_width)
            self.animation.setEndValue(expanded_width)
            self.animation.finished.connect(
                lambda: menu.setMinimumWidth(expanded_width)
            )
            self.menu_expanded = True

        self.animation.start()
