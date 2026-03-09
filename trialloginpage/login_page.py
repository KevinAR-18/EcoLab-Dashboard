import importlib.util
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QInputDialog,
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


_ROOT_MAIN_MODULE_NAME = "_ecolab_root_main"
_ROOT_MAIN_PATH = Path(__file__).resolve().parent.parent / "main.py"


def _resolve_root_mainwindow_class():
    module = sys.modules.get(_ROOT_MAIN_MODULE_NAME)
    if module is None:
        spec = importlib.util.spec_from_file_location(_ROOT_MAIN_MODULE_NAME, _ROOT_MAIN_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Cannot load dashboard module from {_ROOT_MAIN_PATH}")

        module = importlib.util.module_from_spec(spec)
        root_dir = str(_ROOT_MAIN_PATH.parent)
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
        sys.modules[_ROOT_MAIN_MODULE_NAME] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(_ROOT_MAIN_MODULE_NAME, None)
            raise

    main_window = getattr(module, "MainWindow", None)
    if main_window is None:
        raise RuntimeError("Dashboard module does not expose MainWindow")

    return main_window


class LoginPage(QWidget):
    def __init__(self, service=None):
        super().__init__()
        self.service = service or TrialLoginService()
        self.admin = None
        self.dashboard = None

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
        forgot = QPushButton("Forgot Password")

        login.clicked.connect(self.login)
        signup.clicked.connect(self.signup)
        google.clicked.connect(self.google_login)
        forgot.clicked.connect(self.reset_password)

        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.showpass)
        layout.addWidget(login)
        layout.addWidget(signup)
        layout.addWidget(google)
        layout.addWidget(forgot)

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

    def reset_password(self):
        email, ok = QInputDialog.getText(self, "Reset Password", "Enter Email")
        if not ok:
            return

        result = self.service.send_reset_password(email)
        self._show_result(
            result,
            success_title="Email Sent",
            error_title="Error",
        )

    def _handle_login_result(self, result, error_title):
        status = result.get("status")
        message = result.get("message", "")

        if status == "admin":
            self.admin = AdminPage(self.service)
            self.admin.show()
            return

        if status == "success":
            self._open_dashboard()
            return

        if status in {"pending", "blocked", "missing_user_data", "error"}:
            title = self._warning_title(status, error_title)
            QMessageBox.warning(self, title, message)
            return

        QMessageBox.information(self, "Login", message)

    def _open_dashboard(self):
        try:
            dashboard_class = _resolve_root_mainwindow_class()
            self.dashboard = dashboard_class()
            self.dashboard.show()
        except Exception as exc:
            self.dashboard = None
            QMessageBox.warning(
                self,
                "Dashboard Error",
                f"Unable to open dashboard: {exc}",
            )
            return

        self.close()

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
