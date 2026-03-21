"""
EcoLab Dashboard Launcher
Entry point baru yang manage login flow dan remember me feature
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, Signal, QTimer

# Import Login Window
from loginmain import LoginWindow

# Import Session Manager
from session_manager import SessionManager


class AppLauncher(QObject):
    """Launcher untuk manage aplikasi flow dari login ke dashboard"""

    # Signal untuk notify saat logout terjadi
    logout_signal = Signal()

    def __init__(self):
        super().__init__()
        self.session_manager = SessionManager()
        self.main_window = None
        self.login_window = None

    def start(self):
        """Start aplikasi - cek session dulu"""
        # Cek apakah ada session tersimpan
        session = self.session_manager.load_session()

        if session:
            # Session ada → langsung buka dashboard (baik remember_me ON atau OFF)
            print(f"DEBUG: Found session, opening dashboard for user: {session.get('username')}")
            self.open_dashboard(session)
        else:
            # No session → login dulu
            print("DEBUG: No session found, showing login")
            self.open_login()

    def open_login(self):
        """Buka login window"""
        try:
            self.login_window = LoginWindow()
            self.login_window.show()

            # Setup timer untuk check apakah login window sudah close
            # dan apakah ada session tersimpan
            self.check_timer = QTimer()
            self.check_timer.timeout.connect(self.check_login_status)
            self.check_timer.start(500)  # Check setiap 500ms

            return True

        except Exception as e:
            QMessageBox.critical(
                None,
                "Login Error",
                f"❌ Failed to open login:\n{str(e)}"
            )
            return False

    def check_login_status(self):
        """Check apakah login window masih ada dan cek session status"""
        # Cek apakah login window masih visible
        if self.login_window and self.login_window.isVisible():
            # Login window masih ada, lanjut check
            return

        # Login window sudah tidak visible, stop timer
        self.check_timer.stop()

        print("DEBUG: Login window closed, checking session...")

        # Cek apakah ada session (berarti user berhasil login)
        session = self.session_manager.load_session()

        if session:
            print(f"DEBUG: Session found! Opening dashboard for user: {session.get('username')}")
            # Login success → buka dashboard
            self.open_dashboard(session)
        else:
            print("DEBUG: No session found, quitting app")
            # Login cancelled/failed → exit app
            QApplication.quit()

    def open_dashboard(self, session):
        """Buka dashboard utama dengan session data"""
        try:
            # Import main window di sini (lazy import)
            from main import MainWindow

            # Buat main window dengan session
            self.main_window = MainWindow(user_session=session)

            # Connect logout signal
            self.main_window.logout_signal.connect(self.handle_logout)

            # Show main window
            self.main_window.show()

            # Kalau remember_me = False, hapus session setelah dashboard terbuka
            # (Supaya next time harus login lagi)
            if not session.get("remember_me", False):
                print(f"DEBUG: remember_me is OFF, scheduling session deletion")
                # Hapus session setelah delay (supaya window benar-benar terbuka dulu)
                QTimer.singleShot(1000, lambda: self.session_manager.delete_session())

            return True

        except Exception as e:
            QMessageBox.critical(
                None,
                "Dashboard Error",
                f"❌ Failed to open dashboard:\n{str(e)}"
            )
            return False

    def handle_logout(self):
        """Handle logout dari dashboard"""
        try:
            # Hapus session
            self.session_manager.delete_session()

            # Close main window jika ada
            if self.main_window:
                self.main_window.close()
                self.main_window = None

            # Balik ke login
            self.open_login()

        except Exception as e:
            QMessageBox.critical(
                None,
                "Logout Error",
                f"❌ Failed to logout:\n{str(e)}"
            )


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("EcoLab Dashboard")

    # Buat launcher
    launcher = AppLauncher()

    # Start aplikasi
    launcher.start()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
