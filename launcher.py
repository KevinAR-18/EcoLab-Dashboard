"""
EcoLab Dashboard Launcher
Entry point baru yang manage login flow dan remember me feature
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, Signal, QTimer

# Import Login Window
from loginmain import LoginWindow

# Import Main Window (moved here for PyInstaller compatibility)
from main import MainWindow

# Import Session Manager
from session_manager import SessionManager

# Import Theme Helper for light theme
from ui_theme_helper import get_light_theme_stylesheet


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
        self.current_session = None  # Simpan session yang sedang aktif

    def start(self):
        """Start aplikasi - cek session dulu"""
        # Setup handler untuk saat aplikasi akan quit
        QApplication.instance().aboutToQuit.connect(self.on_app_about_to_quit)

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
            # Simpan session yang sedang aktif
            self.current_session = session
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

            # Simpan session yang sedang aktif (untuk admin panel case)
            self.current_session = session

            # 🔥 BUG FIX: Hapus session SEKARANG JUGA jika remember_me=False
            # Admin panel tidak akan membuka dashboard, jadi kita harus hapus sekarang
            if not session.get("remember_me", False):
                print(f"DEBUG: remember_me is OFF (admin panel mode), deleting session IMMEDIATELY")
                result = self.session_manager.delete_session()
                print(f"DEBUG: Session delete result: {result}")
                # Jangan simpan session yang sudah dihapus
                self.current_session = None
        else:
            # Tidak ada session dan window di-close manual → exit app
            print("DEBUG: No session and window closed manually, quitting app")
            QApplication.quit()

    def open_dashboard(self, session):
        """Buka dashboard utama dengan session data"""
        try:
            # Simpan session yang sedang aktif
            self.current_session = session

            # Buat main window dengan session
            self.main_window = MainWindow(user_session=session)

            # Connect logout signal
            self.main_window.logout_signal.connect(self.handle_logout)

            # Show main window
            self.main_window.show()

            # ⚠️ JANGAN hapus session di sini lagi
            # Session akan dihapus saat aplikasi quit (lihat on_app_about_to_quit)

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

            # Clear current session
            self.current_session = None

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

    def on_app_about_to_quit(self):
        """Handler saat aplikasi akan quit - hapus session jika remember_me=False"""
        # Cek current session dulu, lalu fallback ke load dari file
        session = self.current_session

        if not session:
            # Fallback: load dari file jika current_session belum di-set
            session = self.session_manager.load_session()

        if session and not session.get("remember_me", False):
            print(f"DEBUG: App quitting, remember_me is OFF, deleting session")
            result = self.session_manager.delete_session()
            print(f"DEBUG: Session delete result: {result}")
        else:
            if session:
                print(f"DEBUG: App quitting, keeping session (remember_me is ON)")
            else:
                print(f"DEBUG: App quitting, no session to delete")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("EcoLab Dashboard")

    # Apply light theme untuk mencegah Dark Mode Windows 11 interference
    app.setStyleSheet(get_light_theme_stylesheet())

    # Buat launcher
    launcher = AppLauncher()

    # Start aplikasi
    launcher.start()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
