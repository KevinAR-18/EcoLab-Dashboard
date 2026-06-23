"""
Entry point untuk window login EcoLab.

Modul ini mengatur login window yang frameless, bisa di-drag,
punya flow sign in, sign up, forgot password, guest mode,
dan integrasi auth ke Firebase.
"""
import os
import sys
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialog
)
from PySide6.QtGui import QScreen, QPixmap, QIcon

# Import Qt Resources untuk load gambar
import resources_rc

# Import UI dan helper UI behavior
from ui.ui_loginpage import Ui_MainWindow
from ui.ui_functions import UIFunctions

# Import login settings
from config import login_settings

# Import auth service untuk Firebase
from auth.auth_service import FirebaseAuthService

# Import session manager untuk fitur remember me
from auth.session_manager import SessionManager

# Import dialog pilihan role dan admin panel
from ui.ui_role_selection import RoleSelectionDialog
from dialogs.admin_window import AdminPanelWindow
from ui.ui_theme_helper import (
    apply_light_theme_to_widget,
    show_styled_critical,
    show_styled_information,
    show_styled_question,
    show_styled_warning,
)
from config.path_utils import resource_path


class LoginWindow(QMainWindow):
    # Signal untuk notify launcher saat login selesai (user memilih dashboard/admin)
    login_completed = Signal()

    def __init__(self):
        """
        Menyiapkan seluruh login window beserta auth flow-nya.

        Constructor ini menginisialisasi UI, auth service, session manager,
        pengaturan window, serta semua signal yang dipakai pada halaman login.
        """
        super().__init__()

        # Setup UI hasil Qt Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup auth service.
        # Login window berkomunikasi ke Firebase lewat service layer ini.
        self.auth_service = FirebaseAuthService()

        # Setup session manager.
        self.session_manager = SessionManager()
        self.user_session = None  # Simpan user session setelah login berhasil

        # Setup helper UI untuk drag dan behavior window custom.
        self.ui_functions = UIFunctions(self)

        # Window settings: frameless dan transparan.
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Set window title.
        self.setWindowTitle("EcoLab Login")

        # Set window icon.
        pixmap = QPixmap(resource_path("icon\\logoecolab.ico"))
        icon = QIcon(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.setWindowIcon(icon)
        apply_light_theme_to_widget(self)

        # Center window ke tengah screen.
        self.center_window()

        # Connect semua signal UI.
        self._connect_signals()

        # Set halaman default.
        self._set_default_page()

    def _connect_signals(self):
        """
        Menghubungkan semua signal UI ke handler yang sesuai.

        Pemisahan wiring signal ke method ini membuat constructor lebih rapi
        dan memudahkan maintenance saat ada event UI baru.
        """

        # ===== NAVIGASI =====
        # Button untuk pindah ke sign up page
        self.ui.goto_signuppage.clicked.connect(self.show_signup_page)

        # Button untuk kembali ke sign in page
        self.ui.goto_signinpage.clicked.connect(self.show_signin_page)

        # Button untuk pindah ke forgot password page
        self.ui.goto_forgot_password.clicked.connect(self.show_forgot_password_page)

        # Button untuk kembali ke sign in dari forgot password page
        self.ui.backToSigninFromForgotBtn.clicked.connect(self.show_signin_page)

        # ===== FORGOT PASSWORD =====
        # Button untuk kirim reset email
        self.ui.sendResetEmailBtn.clicked.connect(self.handle_forgot_password_send_email)

        # Enter key di email input forgot password → auto click send
        self.ui.forgotPasswordEmailInput.returnPressed.connect(self.handle_forgot_password_send_email)

        # ===== SHOW PASSWORD =====
        # Checkbox show password sign in
        if hasattr(self.ui, 'showpasssigninCheck'):
            self.ui.showpasssigninCheck.stateChanged.connect(
                lambda: self._toggle_password_signin()
            )

        # Checkbox show password sign up
        if hasattr(self.ui, 'showpasssignupCheck'):
            self.ui.showpasssignupCheck.stateChanged.connect(
                lambda: self._toggle_password_signup()
            )

        # ===== CLOSE BUTTON =====
        self.ui.closeAppBtn.clicked.connect(self.close)

        # ===== GUEST BUTTON (opsional) =====
        self.ui.guestButton.clicked.connect(self.handle_guest_login)

        # ===== SIGN IN BUTTON =====
        self.ui.signinButton.clicked.connect(self.handle_signin)

        # ===== ENTER KEY FOR SIGN IN =====
        # Tekan Enter di email atau password field → auto click Sign In
        self.ui.emailInput.returnPressed.connect(self.handle_signin)
        self.ui.passwordInput.returnPressed.connect(self.handle_signin)

        # ===== ENTER KEY FOR REMEMBER ME CHECKBOX =====
        # Install event filter untuk menangani Enter key
        self.ui.rememberCheck.installEventFilter(self)

        # ===== ENTER KEY FOR SIGN IN BUTTON =====
        # Install event filter untuk menangani Enter key pada tombol
        self.ui.signinButton.installEventFilter(self)

        # ===== SIGN UP BUTTON =====
        self.ui.signupButton.clicked.connect(self.handle_signup)

        # ===== GOOGLE BUTTONS =====
        self.ui.googleSigninButton.clicked.connect(self.handle_google_signin)
        self.ui.googleSignupButton.clicked.connect(self.handle_google_signup)

    def _set_default_page(self):
        """Menentukan default page login berdasarkan config saat aplikasi mulai."""
        if login_settings.DEFAULT_PAGE == "signup":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_signup)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_signin)

    # ===== NAVIGASI =====
    def show_signin_page(self):
        """Memindahkan stacked widget ke halaman sign in."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_signin)

    def show_signup_page(self):
        """Memindahkan stacked widget ke halaman sign up."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_signup)

    def show_forgot_password_page(self):
        """Memindahkan stacked widget ke halaman forgot password."""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_forgot_password)

    # ===== TOGGLE PASSWORD =====
    def _toggle_password_signin(self):
        """Toggle visibility password pada form sign in."""
        login_settings.toggle_password_visibility(
            self.ui.passwordInput,
            self.ui.showpasssigninCheck
        )

    def _toggle_password_signup(self):
        """Toggle visibility password pada form sign up."""
        login_settings.toggle_password_visibility(
            self.ui.signupPasswordInput,
            self.ui.showpasssignupCheck
        )

    def toggle_remember_me(self):
        """Toggle checkbox Remember Me saat user menekan Enter."""
        current_state = self.ui.rememberCheck.isChecked()
        self.ui.rememberCheck.setChecked(not current_state)

    def _is_valid_email(self, email):
        """
        Mengecek format email dengan regex sederhana.

        Args:
            email: Email string yang akan divalidasi

        Returns:
            bool: True jika format email valid, False jika tidak
        """
        import re

        # Pattern regex untuk validasi email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return True
        return False

    # ===== HANDLERS =====
    def handle_signin(self):
        """Menangani proses sign in dengan email dan password."""
        email = self.ui.emailInput.text().strip()
        password = self.ui.passwordInput.text()

        # Validasi input dasar.
        if not email or not password:
            self.show_message_box("warning", "Login Error", "Please enter email and password!")
            return

        # Panggil auth service untuk proses login.
        # Status akun seperti admin, pending, blocked, dan success
        # dinormalkan di service lalu diproses di _handle_auth_result().
        result = self.auth_service.login_with_email(email, password)
        self._handle_auth_result(result, "Login")

    def handle_forgot_password_send_email(self):
        """Menangani pengiriman email reset password ke user."""
        email = self.ui.forgotPasswordEmailInput.text().strip()

        # Validasi input dasar.
        if not email:
            self.show_message_box("warning", "Email Required", "Please enter your email address!")
            return

        # Validasi format email.
        if not self._is_valid_email(email):
            self.show_message_box("warning", "Invalid Email", "Invalid email format!\n\nPlease enter a valid email address.\nExample: user@example.com")
            return

        # Minta konfirmasi sebelum kirim email reset.
        reply = show_styled_question(
            self,
            "Send Reset Email",
            f"Send password reset email to:\n\n{email}\n\nCheck your inbox/spam folder.",
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Kirim reset email via Firebase.
            result = self.auth_service.send_reset_password(email)

            if result["status"] == "success":
                self.show_message_box(
                    "information",
                    "Email Sent",
                    "✅ Password reset email has been sent!\n\n"
                    "Please check your inbox (and spam folder).\n"
                    "Follow the link in the email to reset your password."
                )
                # Clear input lalu kembali ke halaman sign in.
                self.ui.forgotPasswordEmailInput.clear()
                self.show_signin_page()
            else:
                self.show_message_box(
                    "critical",
                    "Error",
                    f"❌ Failed to send reset email:\n\n{result['message']}\n\n"
                    "Please check:\n"
                    "• Email is registered\n"
                    "• Internet connection"
                )

    def handle_signup(self):
        """Menangani proses sign up dengan email, username, dan password."""
        username = self.ui.usernameInput.text().strip()
        email = self.ui.signupEmailInput.text().strip()
        password = self.ui.signupPasswordInput.text()

        # Validasi input dasar.
        if not username or not email or not password:
            self.show_message_box("warning", "Signup Error", "Please fill all fields!\nUsername, Email, and Password are required.")
            return

        # Validasi format email.
        if not self._is_valid_email(email):
            self.show_message_box("warning", "Signup Error", "Invalid email format!\n\nPlease enter a valid email address.\nExample: user@example.com")
            return

        # Cek apakah email sudah terdaftar.
        email_check = self.auth_service.check_email_exists(email)

        if email_check["exists"]:
            self.show_message_box(
                "warning",
                "Email Already Registered",
                "⚠️ This email is already registered!\n\n"
                f"Email: {email}\n\n"
                "Please:\n"
                "• Use a different email, OR\n"
                "• Sign In with existing account, OR\n"
                "• Reset password if forgotten"
            )
            return

        if len(password) < 6:
            self.show_message_box("warning", "Signup Error", "Password must be at least 6 characters!")
            return

        # Panggil auth service untuk proses signup.
        # Akun baru dibuat pending supaya admin bisa memverifikasi sebelum user masuk.
        result = self.auth_service.signup_with_email(email, password, username=username)
        self._handle_auth_result(result, "Signup", signup_username=username)

    def handle_guest_login(self):
        """Membuat guest session lalu langsung masuk ke mode monitoring tamu."""
        # Buat object session untuk guest mode.
        # Guest tidak melalui Firebase karena hanya dipakai sebagai mode viewer.
        self.user_session = {
            "uid": "guest_temp",
            "username": "Guest Viewer",
            "email": "Temporary Guest Viewer Mode",
            "role": "guest",
            "auth_provider": "guest",
            "remember_me": False
        }

        # Simpan guest session.
        print(f"DEBUG: Guest session created: {self.user_session}")
        result = self.session_manager.save_session(self.user_session)
        print(f"DEBUG: Save result: {result}")

        # Tampilkan notifikasi mode guest.
        self.show_message_box(
            "information",
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

        # Emit signal lalu tutup login window.
        self.login_completed.emit()
        self.close()

    def handle_google_signin(self):
        """Menangani Google sign in tanpa membuat account baru otomatis."""
        try:
            # Panggil auth service untuk Google sign in tanpa auto create account.
            result = self.auth_service.login_with_google(create_if_not_exists=False)

            # Proses hasil auth.
            self._handle_auth_result(result, "Google Sign In")

        except Exception as e:
            self.show_message_box(
                "critical",
                "Google Sign In Error",
                f"❌ Failed to sign in with Google:\n\n{str(e)}\n\nPlease try again."
            )

    def handle_google_signup(self):
        """Menangani Google sign up dengan auto create account jika perlu."""
        try:
            # Panggil auth service untuk Google sign up dengan create account.
            result = self.auth_service.login_with_google(create_if_not_exists=True)

            # Proses hasil auth.
            self._handle_auth_result(result, "Google Sign Up")

        except Exception as e:
            self.show_message_box(
                "critical",
                "Google Sign Up Error",
                f"❌ Failed to sign up with Google:\n\n{str(e)}\n\nPlease try again."
            )

    def show_admin_selection_dialog(self):
        """Menampilkan dialog pilihan dashboard atau admin panel untuk admin."""
        dialog = RoleSelectionDialog(self)

        # Tampilkan dialog dengan animation.
        if dialog.exec_with_animation() == QDialog.DialogCode.Accepted:
            choice = dialog.choice

            if choice == "dashboard":
                self._open_dashboard()
            elif choice == "admin_panel":
                self._open_admin_panel()

        # Jangan emit login_completed di sini.
        # Signal akan di-emit oleh method tujuan yang dipilih user.

    def _handle_auth_result(self, result, operation_type, signup_username=None):
        """
        Menangani hasil operasi authentication dari auth service.

        Args:
            result: Dict hasil dari auth_service
            operation_type: Jenis operasi seperti "Login" atau "Signup"
            signup_username: Username tambahan untuk flow signup
        """
        status = result.get("status")
        message = result.get("message", "")
        user_id = result.get("user_id")

        # Auth service sudah menormalkan response Firebase ke beberapa status
        # inti agar semua keputusan UI bisa dipusatkan di method ini.
        # ===== ADMIN LOGIN SUCCESS =====
        if status == "admin":
            # Load user data dari Firebase.
            if self._load_and_save_user_session(user_id):
                # Tampilkan popup pilihan role admin.
                self.show_admin_selection_dialog()
            else:
                self.show_message_box(
                    "critical",
                    "Login Error",
                    "❌ Failed to load user data"
                )

        # ===== SUCCESS =====
        elif status == "success":
            if operation_type == "Signup":
                # Signup berhasil, tapi user masih perlu approval admin.
                self.show_message_box(
                    "information",
                    "Registration Successful",
                    f"✅ Account created successfully!\n\n"
                    f"Username: {signup_username or 'N/A'}\n"
                    f"Email: {self.ui.signupEmailInput.text()}\n\n"
                    f"⏳ Your account is pending admin approval.\n"
                    f"Please wait for confirmation before logging in."
                )
                # Clear form lalu kembali ke halaman sign in.
                self._clear_signup_form()
                self.show_signin_page()
            else:
                # Login berhasil, lanjut load user session.
                if self._load_and_save_user_session(user_id):
                    self.show_message_box(
                        "information",
                        "Login Successful",
                        f"Welcome back! 🎉\n\n{message}"
                    )
                    # Emit signal lalu tutup login window.
                    self.login_completed.emit()
                    self.close()
                else:
                    self.show_message_box(
                        "critical",
                        "Login Error",
                        "❌ Failed to load user session"
                    )

        # ===== PENDING (Need Admin Approval) =====
        elif status == "pending":
            self.show_message_box(
                "warning",
                "Account Pending Approval",
                f"⏳ {message}\n\n"
                f"Your account is waiting for admin approval.\n"
                f"Please contact the administrator."
            )

        # ===== BLOCKED =====
        elif status == "blocked":
            self.show_message_box(
                "critical",
                "Account Blocked",
                f"🚫 {message}\n\n"
                f"Your account has been blocked.\n"
                f"Please contact the administrator."
            )

        # ===== ERROR =====
        elif status == "error":
            # Tampilkan pesan error yang lebih user-friendly.
            if operation_type == "Login":
                # Untuk login error, tampilkan pesan yang singkat.
                self.show_message_box(
                    "warning",
                    "Login Gagal",
                    "Username atau Password salah\n\nSilakan coba lagi."
                )
            else:
                # Untuk signup error, tampilkan pesan yang lebih jelas.
                self.show_message_box(
                    "warning",
                    f"{operation_type} Gagal",
                    f"{message}\n\nSilakan coba lagi."
                )

        # ===== OTHER =====
        else:
            self.show_message_box(
                "information",
                operation_type,
                message
            )

    def _load_and_save_user_session(self, uid):
        """
        Load user data dari Firebase lalu simpan ke session lokal.

        Args:
            uid: User ID dari Firebase

        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            # Ambil user record dari Firebase.
            user_data = self.auth_service.get_user_record(uid)

            if not user_data:
                print(f"ERROR: User data not found for uid: {uid}")
                return False

            # Build object session untuk user aktif.
            # Session ini nanti dibaca dashboard untuk menentukan nama, role, dan hak akses.
            self.user_session = {
                "uid": uid,
                "username": user_data.get("username", ""),
                "email": user_data.get("email", ""),
                "role": user_data.get("role", "user"),
                "auth_provider": user_data.get("auth_provider", "email"),
                "remember_me": self.ui.rememberCheck.isChecked()
            }

            print(f"DEBUG: User session created: {self.user_session}")

            # Simpan session setiap login success.
            # Nilai remember_me tetap ikut disimpan dari checkbox UI.
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
        Mengambil user session setelah login success.

        Returns:
            dict: Data session user atau None
        """
        return self.user_session

    def _open_dashboard(self):
        """Mengirim signal ke launcher untuk membuka dashboard utama."""
        # Emit signal dulu agar launcher tahu flow login sudah selesai.
        self.login_completed.emit()

        # Setelah itu tutup login window agar launcher bisa lanjut buka dashboard.
        self.close()

    def _open_admin_panel(self):
        """Membuka admin panel untuk user dengan role admin."""
        try:
            # Buat admin panel window dengan reference ke login window.
            self.admin_window = AdminPanelWindow(self)
            self.admin_window.show()

            # Tampilkan notifikasi sukses.
            self.show_message_box(
                "information",
                "Admin Panel",
                "✅ Admin Panel berhasil dibuka!\n\nKlik tombol Back untuk kembali ke pilihan."
            )

            self.close()

        except Exception as e:
            self.show_message_box(
                "critical",
                "Error",
                f"❌ Gagal membuka Admin Panel:\n{str(e)}"
            )

    def _clear_signup_form(self):
        """Membersihkan form signup setelah proses registrasi selesai."""
        self.ui.usernameInput.clear()
        self.ui.signupEmailInput.clear()
        self.ui.signupPasswordInput.clear()
        self.ui.showpasssignupCheck.setChecked(False)

    # ===== WINDOW POSITION =====
    def center_window(self):
        """Meletakkan login window di tengah area screen yang aktif."""
        # Ambil geometry screen.
        screen = QScreen.availableGeometry(self.screen())

        # Ambil geometry window.
        window = self.geometry()

        # Hitung posisi tengah.
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Terapkan posisi ke window.
        self.move(x, y)

    # ===== DRAGGABLE WINDOW =====
    # NOTE: Kode ini dipakai untuk development mode.
    # Untuk production, biasanya hanya contentTopBg yang dibuat draggable.
    def mousePressEvent(self, event):
        """Meneruskan mouse press ke helper drag window."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.ui_functions.mouse_press(event)

    def mouseMoveEvent(self, event):
        """Meneruskan mouse move ke helper drag window."""
        self.ui_functions.mouse_move(event)

    def eventFilter(self, obj, event):
        """
        Event filter untuk menangani key press pada widget tertentu.

        Args:
            obj: Widget yang mengirim event
            event: Event yang sedang diproses

        Returns:
            bool: True jika event ditangani, False jika dibiarkan default
        """
        # Cek apakah event adalah KeyPress.
        if event.type() == QEvent.Type.KeyPress:
            # Handle Enter pada checkbox Remember Me.
            if obj == self.ui.rememberCheck:
                if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    # Toggle checkbox.
                    self.toggle_remember_me()
                    return True  # Event sudah ditangani

            # Handle Enter pada tombol Sign In.
            elif obj == self.ui.signinButton:
                if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    # Jalankan aksi sign in.
                    self.handle_signin()
                    return True  # Event sudah ditangani

        return False  # Biarkan event diproses default

    def show_message_box(self, icon_type, title, text):
        """
        Menampilkan styled message box sesuai jenis icon yang diminta.

        Args:
            icon_type: Jenis icon seperti information, warning, critical, atau question
            title: Judul message box
            text: Isi pesan yang ditampilkan
        """
        if icon_type == "information":
            show_styled_information(self, title, text)
        elif icon_type == "warning":
            show_styled_warning(self, title, text)
        elif icon_type == "critical":
            show_styled_critical(self, title, text)
        elif icon_type == "question":
            show_styled_question(self, title, text)
        else:
            show_styled_information(self, title, text)


def main():
    """Menjadi entry point lokal untuk menjalankan login window secara langsung."""
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
