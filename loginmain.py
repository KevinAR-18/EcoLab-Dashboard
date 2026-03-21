"""
Login Main Entry Point
Frameless window dengan centered position, draggable, dan navigasi
"""
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialog
)
from PySide6.QtGui import QScreen

# Import Qt Resources untuk load gambar
import resources_rc

# Import UI dan UIFunctions
from ui_loginpage import Ui_MainWindow
from ui_functions import UIFunctions

# Import Login Settings
import login_settings

# Import Auth Service untuk Firebase
from auth_service import TrialLoginService

# Import Role Selection Dialog dan Admin Window
from ui_role_selection import RoleSelectionDialog
from admin_window import AdminPanelWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # SETUP AUTH SERVICE
        self.auth_service = TrialLoginService()

        # SETUP UI FUNCTIONS (untuk draggable window)
        self.ui_functions = UIFunctions(self)

        # WINDOW SETTINGS - FRAMELESS & TRANSPARENT
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Set window title
        self.setWindowTitle("EcoLab Login")

        # Center window on screen
        self.center_window()

        # Connect semua signals
        self._connect_signals()

        # Set default page
        self._set_default_page()

    def _connect_signals(self):
        """Connect semua UI signals ke handlers"""

        # ===== NAVIGASI =====
        # Button untuk pindah ke sign up page
        self.ui.goto_signuppage.clicked.connect(self.show_signup_page)

        # Button untuk kembali ke sign in page
        self.ui.goto_signinpage.clicked.connect(self.show_signin_page)

        # ===== SHOW PASSWORD SIGN IN =====
        self.ui.showpasssigninCheck.stateChanged.connect(
            lambda: self._toggle_password_signin()
        )

        # ===== SHOW PASSWORD SIGN UP =====
        self.ui.showpasssignupCheck.stateChanged.connect(
            lambda: self._toggle_password_signup()
        )

        # ===== CLOSE BUTTON =====
        self.ui.closeAppBtn.clicked.connect(self.close)

        # ===== GUEST BUTTON (opsional) =====
        self.ui.guestButton.clicked.connect(self.handle_guest_login)

        # ===== SIGN IN BUTTON =====
        self.ui.signinButton.clicked.connect(self.handle_signin)

        # ===== SIGN UP BUTTON =====
        self.ui.signupButton.clicked.connect(self.handle_signup)

        # ===== GOOGLE BUTTONS =====
        self.ui.googleSigninButton.clicked.connect(self.handle_google_signin)
        self.ui.googleSignupButton.clicked.connect(self.handle_google_signup)

    def _set_default_page(self):
        """Set halaman default berdasarkan settings"""
        if login_settings.DEFAULT_PAGE == "signup":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_signup)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_signin)

    # ===== NAVIGASI =====
    def show_signin_page(self):
        """Tampilkan halaman sign in"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_signin)

    def show_signup_page(self):
        """Tampilkan halaman sign up"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_signup)

    # ===== TOGGLE PASSWORD =====
    def _toggle_password_signin(self):
        """Toggle visibility password di halaman sign in"""
        login_settings.toggle_password_visibility(
            self.ui.passwordInput,
            self.ui.showpasssigninCheck
        )

    def _toggle_password_signup(self):
        """Toggle visibility password di halaman sign up"""
        login_settings.toggle_password_visibility(
            self.ui.signupPasswordInput,
            self.ui.showpasssignupCheck
        )

    # ===== HANDLERS =====
    def handle_signin(self):
        """Handle tombol sign in diklik"""
        email = self.ui.emailInput.text().strip()
        password = self.ui.passwordInput.text()

        # Validasi input
        if not email or not password:
            QMessageBox.warning(
                self,
                "Login Error",
                "Please enter email and password!"
            )
            return

        # Panggil auth service untuk login
        result = self.auth_service.login_with_email(email, password)
        self._handle_auth_result(result, "Login")

    def handle_signup(self):
        """Handle tombol sign up diklik"""
        username = self.ui.usernameInput.text().strip()
        email = self.ui.signupEmailInput.text().strip()
        password = self.ui.signupPasswordInput.text()

        # Validasi input
        if not username or not email or not password:
            QMessageBox.warning(
                self,
                "Signup Error",
                "Please fill all fields!\nUsername, Email, and Password are required."
            )
            return

        if len(password) < 6:
            QMessageBox.warning(
                self,
                "Signup Error",
                "Password must be at least 6 characters!"
            )
            return

        # Panggil auth service untuk signup
        result = self.auth_service.signup_with_email(email, password, username=username)
        self._handle_auth_result(result, "Signup", signup_username=username)

    def handle_guest_login(self):
        """Handle tombol guest login diklik"""
        QMessageBox.information(
            self,
            "Guest Login",
            "Guest login feature coming soon!"
        )
        # TODO: Implementasi guest login logic

    def handle_google_signin(self):
        """Handle tombol Google sign in diklik - HANYA LOGIN, jangan create account"""
        try:
            # Panggil auth service untuk Google sign in (JANGAN create account)
            result = self.auth_service.login_with_google(create_if_not_exists=False)

            # Handle hasil
            self._handle_auth_result(result, "Google Sign In")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Google Sign In Error",
                f"❌ Failed to sign in with Google:\n\n{str(e)}\n\nPlease try again."
            )

    def handle_google_signup(self):
        """Handle tombol Google sign up diklik - Auto create account jika belum ada"""
        try:
            # Panggil auth service untuk Google sign up (BOLEH create account)
            result = self.auth_service.login_with_google(create_if_not_exists=True)

            # Handle hasil
            self._handle_auth_result(result, "Google Sign Up")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Google Sign Up Error",
                f"❌ Failed to sign up with Google:\n\n{str(e)}\n\nPlease try again."
            )

    def show_admin_selection_dialog(self):
        """Tampilkan popup pilihan dashboard/admin panel"""
        dialog = RoleSelectionDialog(self)

        # Show dialog dengan animation
        if dialog.exec_with_animation() == QDialog.DialogCode.Accepted:
            choice = dialog.choice

            if choice == "dashboard":
                self._open_dashboard()
            elif choice == "admin_panel":
                self._open_admin_panel()

    def _handle_auth_result(self, result, operation_type, signup_username=None):
        """
        Handle hasil operasi authentication (login/signup)

        Args:
            result: Dict hasil dari auth_service
            operation_type: "Login" atau "Signup"
            signup_username: Username (untuk signup saja)
        """
        status = result.get("status")
        message = result.get("message", "")

        # ===== ADMIN LOGIN SUCCESS =====
        if status == "admin":
            # Tampilkan popup pilihan
            self.show_admin_selection_dialog()

        # ===== SUCCESS =====
        elif status == "success":
            if operation_type == "Signup":
                # Signup berhasil - user perlu approval admin
                QMessageBox.information(
                    self,
                    "Registration Successful",
                    f"✅ Account created successfully!\n\n"
                    f"Username: {signup_username or 'N/A'}\n"
                    f"Email: {self.ui.signupEmailInput.text()}\n\n"
                    f"⏳ Your account is pending admin approval.\n"
                    f"Please wait for confirmation before logging in."
                )
                # Clear form dan kembali ke sign in page
                self._clear_signup_form()
                self.show_signin_page()
            else:
                # Login berhasil - buka dashboard
                QMessageBox.information(
                    self,
                    "Login Successful",
                    f"Welcome back! 🎉\n\n{message}"
                )
                # TODO: Buka dashboard utama
                self._open_dashboard()
                self.close()

        # ===== PENDING (Need Admin Approval) =====
        elif status == "pending":
            QMessageBox.warning(
                self,
                "Account Pending Approval",
                f"⏳ {message}\n\n"
                f"Your account is waiting for admin approval.\n"
                f"Please contact the administrator."
            )

        # ===== BLOCKED =====
        elif status == "blocked":
            QMessageBox.critical(
                self,
                "Account Blocked",
                f"🚫 {message}\n\n"
                f"Your account has been blocked.\n"
                f"Please contact the administrator."
            )

        # ===== ERROR =====
        elif status == "error":
            QMessageBox.critical(
                self,
                f"{operation_type} Error",
                f"❌ {message}"
            )

        # ===== OTHER =====
        else:
            QMessageBox.information(
                self,
                operation_type,
                message
            )

    def _open_dashboard(self):
        """Buka dashboard utama"""
        QMessageBox.information(
            self,
            "Opening Dashboard",
            "Dashboard akan dibuka... 🚀\n\nTODO: Implementasi buka dashboard"
        )
        # TODO: Implementasi buka dashboard
        self.close()

    def _open_admin_panel(self):
        """Buka admin panel"""
        try:
            # Buat admin panel window dengan reference ke login window
            self.admin_window = AdminPanelWindow(self)
            self.admin_window.show()

            # Tampilkan notifikasi sukses
            QMessageBox.information(
                self,
                "Admin Panel",
                "✅ Admin Panel berhasil dibuka!\n\nKlik tombol Back untuk kembali ke pilihan."
            )

            self.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"❌ Gagal membuka Admin Panel:\n{str(e)}"
            )

    def _clear_signup_form(self):
        """Clear form signup setelah berhasil"""
        self.ui.usernameInput.clear()
        self.ui.signupEmailInput.clear()
        self.ui.signupPasswordInput.clear()
        self.ui.showpasssignupCheck.setChecked(False)

    # ===== WINDOW POSITION =====
    def center_window(self):
        """Center window on screen"""
        # Get screen geometry
        screen = QScreen.availableGeometry(self.screen())

        # Get window geometry
        window = self.geometry()

        # Calculate center position
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Set position
        self.move(x, y)

    # ===== DRAGGABLE WINDOW =====
    def mousePressEvent(self, event):
        """Handle mouse press untuk drag window"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.ui_functions.mouse_press(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move untuk drag window"""
        self.ui_functions.mouse_move(event)


def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
