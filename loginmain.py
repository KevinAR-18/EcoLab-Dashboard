"""
Login Main Entry Point
Frameless window dengan centered position, draggable, dan navigasi
"""
import sys
from PySide6.QtCore import Qt, Signal
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

# Import Session Manager untuk remember me
from session_manager import SessionManager

# Import Role Selection Dialog dan Admin Window
from ui_role_selection import RoleSelectionDialog
from admin_window import AdminPanelWindow


class LoginWindow(QMainWindow):
    # Signal untuk notify launcher saat login selesai (user memilih dashboard/admin)
    login_completed = Signal()

    def __init__(self):
        super().__init__()

        # SETUP UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # SETUP AUTH SERVICE
        self.auth_service = TrialLoginService()

        # SETUP SESSION MANAGER
        self.session_manager = SessionManager()
        self.user_session = None  # Store user session after login

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

    def _is_valid_email(self, email):
        """
        Validasi format email menggunakan regex

        Args:
            email: Email string yang akan divalidasi

        Returns:
            bool: True jika format valid, False jika tidak
        """
        import re

        # Pattern regex untuk validasi email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return True
        return False

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

        # Validasi format email
        if not self._is_valid_email(email):
            QMessageBox.warning(
                self,
                "Signup Error",
                "Invalid email format!\n\nPlease enter a valid email address.\nExample: user@example.com"
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
        # Buat guest session object
        self.user_session = {
            "uid": "guest_temp",
            "username": "Guest Viewer",
            "email": "Temporary Guest Viewer Mode",
            "role": "guest",
            "auth_provider": "guest",
            "remember_me": False
        }

        # Simpan guest session
        print(f"DEBUG: Guest session created: {self.user_session}")
        result = self.session_manager.save_session(self.user_session)
        print(f"DEBUG: Save result: {result}")

        # Tampilkan notifikasi
        QMessageBox.information(
            self,
            "Guest Mode",
            "🎭 Welcome, Guest!\n\n"
            "You are in Guest Viewer Mode.\n\n"
            "✅ Available Features (Monitoring Only):\n"
            "• EcoLab Power Monitoring\n"
            "• Monitoring Status Lampu dan AC\n"
            "• Environment Monitoring\n"
            "• Monitoring Status Smart Socket\n\n"
            "❌ Restrictions:\n"
            "• Cannot operate/modify any settings\n"
            "• Read-only access\n\n"
            "Enjoy browsing! 👀"
        )

        # Emit signal dan close window
        self.login_completed.emit()
        self.close()

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

        # NOTE: Jangan emit login_completed di sini
        # Signal akan di-emit oleh masing-masing method (_open_dashboard / _open_admin_panel)

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
        user_id = result.get("user_id")

        # ===== ADMIN LOGIN SUCCESS =====
        if status == "admin":
            # Load user data dari Firebase
            if self._load_and_save_user_session(user_id):
                # Tampilkan popup pilihan
                self.show_admin_selection_dialog()
            else:
                QMessageBox.critical(
                    self,
                    "Login Error",
                    "❌ Failed to load user data"
                )

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
                # Login berhasil - load user session
                if self._load_and_save_user_session(user_id):
                    QMessageBox.information(
                        self,
                        "Login Successful",
                        f"Welcome back! 🎉\n\n{message}"
                    )
                    # Emit signal dan close window
                    self.login_completed.emit()
                    self.close()
                else:
                    QMessageBox.critical(
                        self,
                        "Login Error",
                        "❌ Failed to load user session"
                    )

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
            # Tampilkan pesan error yang lebih user-friendly
            if operation_type == "Login":
                # Untuk login error, tampilkan pesan sederhana
                QMessageBox.warning(
                    self,
                    "Login Gagal",
                    "Username atau Password salah\n\nSilakan coba lagi."
                )
            else:
                # Untuk signup error, tampilkan pesan yang lebih jelas
                QMessageBox.warning(
                    self,
                    f"{operation_type} Gagal",
                    f"{message}\n\nSilakan coba lagi."
                )

        # ===== OTHER =====
        else:
            QMessageBox.information(
                self,
                operation_type,
                message
            )

    def _load_and_save_user_session(self, uid):
        """
        Load user data dari Firebase dan simpan ke session

        Args:
            uid: User ID dari Firebase

        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            # Get user record dari Firebase
            user_data = self.auth_service.get_user_record(uid)

            if not user_data:
                print(f"ERROR: User data not found for uid: {uid}")
                return False

            # Build session object
            self.user_session = {
                "uid": uid,
                "username": user_data.get("username", ""),
                "email": user_data.get("email", ""),
                "role": user_data.get("role", "user"),
                "auth_provider": user_data.get("auth_provider", "email"),
                "remember_me": self.ui.rememberCheck.isChecked()
            }

            print(f"DEBUG: User session created: {self.user_session}")

            # SIMPAN SESSION SETIAP LOGIN SUCCESS (ignore remember_me sementara)
            print(f"DEBUG: Saving session...")
            result = self.session_manager.save_session(self.user_session)
            print(f"DEBUG: Save result: {result}")

            return True

        except Exception as e:
            print(f"ERROR loading user session: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_user_session(self):
        """
        Get user session setelah login success

        Returns:
            dict: User session data atau None
        """
        return self.user_session

    def _open_dashboard(self):
        """Buka dashboard utama"""
        # Emit signal dulu untuk notify launcher
        self.login_completed.emit()

        # Lalu close login window agar launcher bisa buka dashboard
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
