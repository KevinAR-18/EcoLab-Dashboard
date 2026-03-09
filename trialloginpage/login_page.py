from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from .admin_page import AdminPage
    from .auth_service import TrialLoginService
except ImportError:
    from admin_page import AdminPage
    from auth_service import TrialLoginService


class LoginPage(QWidget):
    def __init__(self, service=None):
        super().__init__()
        self.service = service or TrialLoginService()
        self.admin = None

        self.setWindowTitle("EcoLab Login")
        self.resize(350, 420)

        layout = QVBoxLayout()

        title = QLabel("EcoLab Login")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.showpass = QCheckBox("Show Password")
        self.showpass.stateChanged.connect(self.toggle_pass)

        login = QPushButton("Login")
        signup = QPushButton("Sign Up")
        google = QPushButton("Sign in with Google")

        login.clicked.connect(self.login)
        signup.clicked.connect(self.signup)
        google.clicked.connect(self.google_login)

        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.showpass)
        layout.addWidget(login)
        layout.addWidget(signup)
        layout.addWidget(google)

        self.setLayout(layout)

    def toggle_pass(self):
        self.password.setEchoMode(
            QLineEdit.Normal if self.showpass.isChecked() else QLineEdit.Password
        )

    def login(self):
        result = self.service.login_with_email(self.email.text(), self.password.text())
        self._handle_login_result(result, error_title="Login Failed")

    def signup(self):
        result = self.service.signup_with_email(self.email.text(), self.password.text())
        self._show_result(
            result,
            success_title="Signup",
            error_title="Signup Error",
        )

    def google_login(self):
        result = self.service.login_with_google()
        self._handle_login_result(result, error_title="Google Login Error")

    def _handle_login_result(self, result, error_title):
        status = result.get("status")
        message = result.get("message", "")

        if status == "admin":
            self.admin = AdminPage(self.service)
            self.admin.show()
            return

        if status in {"pending", "blocked", "missing_user_data", "error"}:
            title = self._warning_title(status, error_title)
            QMessageBox.warning(self, title, message)
            return

        QMessageBox.information(self, "Login", message)

    def _show_result(self, result, success_title, error_title):
        if result.get("status") == "error":
            QMessageBox.warning(self, error_title, result.get("message", "Unknown error"))
            return

        QMessageBox.information(self, success_title, result.get("message", "Success"))

    @staticmethod
    def _warning_title(status, default_title):
        titles = {
            "pending": "Wait",
            "blocked": "Blocked",
            "missing_user_data": "Error",
        }
        return titles.get(status, default_title)