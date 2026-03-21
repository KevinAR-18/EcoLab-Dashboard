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
        self.login_completed_received = False  # Flag untuk track apakah login completed

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
            # Reset flag
            self.login_completed_received = False

            self.login_window = LoginWindow()
            self.login_window.show()

            # Connect signal login_completed (event-based, bukan polling)
            self.login_window.login_completed.connect(self.on_login_completed)

            # Connect signal ketika window di-close manual (X button atau destroy)
            self.login_window.destroyed.connect(self.on_login_window_destroyed)

            return True

        except Exception as e:
            QMessageBox.critical(
                None,
                "Login Error",
                f"❌ Failed to open login:\n{str(e)}"
            )
            return False

    def on_login_completed(self):
        """Handle saat login window selesai (user sudah pilih dashboard/admin)"""
        print("DEBUG: Login completed signal received")
        self.login_completed_received = True

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

    def on_login_window_destroyed(self):
        """Handle saat login window di-close manual (X button atau admin panel)"""
        print("DEBUG: Login window destroyed")

        # Cek apakah login completed signal sudah diterima
        if self.login_completed_received:
            # Login sudah completed, dashboard akan dibuka/di-handle oleh on_login_completed
            print("DEBUG: Login already completed, ignoring destroy event")
            return

        # Login belum completed, berarti user close manual atau buka admin panel
        # Cek apakah ada session
        session = self.session_manager.load_session()

        if session:
            # Ada session tapi login_completed tidak diterima
            # Kemungkinan: User buka admin panel (bukan dashboard)
            # Jangan buka dashboard, biarkan admin panel jalan
            print("DEBUG: Session exists but login not completed (likely admin panel), staying alive")
        else:
            # Tidak ada session dan window di-close manual → exit app
            print("DEBUG: No session and window closed manually, quitting app")
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
