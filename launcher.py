"""
Launcher utama untuk aplikasi EcoLab Dashboard.

Modul ini menjadi entry point aplikasi dan mengatur perpindahan
antara window login, dashboard utama, serta pengelolaan session
termasuk fitur remember me.
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, Signal, QTimer

# Import window login
from loginmain import LoginWindow

# Import manager untuk session login
from auth.session_manager import SessionManager

# Import helper tema terang agar tampilan konsisten
from ui.ui_theme_helper import get_light_theme_stylesheet


class AppLauncher(QObject):
    """Mengatur app flow dari login, dashboard, sampai logout."""

    # Signal untuk notify saat logout terjadi
    logout_signal = Signal()

    def __init__(self):
        """
        Menyiapkan object launcher dan state aplikasi level atas.

        Launcher menyimpan referensi window aktif dan session aktif
        agar perpindahan antar tampilan tidak perlu diurus oleh masing-masing
        window secara terpisah.
        """
        super().__init__()
        # Launcher memegang kontrol perpindahan window tingkat atas supaya
        # masing-masing window bisa fokus pada logika UI-nya sendiri.
        self.session_manager = SessionManager()
        self.main_window = None
        self.login_window = None
        self.login_completed_received = False  # Penanda apakah alur login sudah selesai
        self.current_session = None  # Simpan session yang sedang aktif

    def start(self):
        """
        Memulai aplikasi dengan mengecek session yang tersimpan lebih dulu.

        Jika session masih ada, launcher langsung membuka dashboard.
        Jika tidak ada session, launcher akan menampilkan window login.
        """
        # Pasang handler yang dipanggil saat aplikasi akan ditutup.
        QApplication.instance().aboutToQuit.connect(self.on_app_about_to_quit)

        # Cek apakah ada session login yang tersimpan di local storage.
        session = self.session_manager.load_session()

        if session:
            # Jika session ada, langsung buka dashboard.
            print(f"DEBUG: Found session, opening dashboard for user: {session.get('username')}")
            self.open_dashboard(session)
        else:
            # Jika tidak ada session, user harus login terlebih dahulu.
            print("DEBUG: No session found, showing login")
            self.open_login()

    def open_login(self):
        """
        Membuka window login dan memasang signal yang dibutuhkan.

        Fungsi ini menghubungkan event login selesai dan event destroy
        window agar launcher bisa menentukan langkah berikutnya.
        """
        try:
            # Reset penanda agar launcher tahu ini adalah alur login baru.
            self.login_completed_received = False

            self.login_window = LoginWindow()
            self.login_window.show()

            # Hubungkan signal login selesai secara event-based, bukan polling.
            self.login_window.login_completed.connect(self.on_login_completed)

            # Hubungkan event saat window ditutup manual atau dihancurkan.
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
        """
        Menangani kondisi saat proses login selesai.

        Setelah login selesai, launcher memeriksa session yang baru dibuat.
        Jika session tersedia maka dashboard dibuka, jika tidak maka aplikasi keluar.
        """
        print("DEBUG: Login completed signal received")
        self.login_completed_received = True

        # Cek apakah login berhasil membuat session yang valid.
        session = self.session_manager.load_session()

        if session:
            print(f"DEBUG: Session found! Opening dashboard for user: {session.get('username')}")
            # Simpan session aktif agar bisa dipakai di alur selanjutnya.
            self.current_session = session
            # Jika login sukses, buka dashboard.
            self.open_dashboard(session)
        else:
            print("DEBUG: No session found, quitting app")
            # Jika login batal atau gagal, tutup aplikasi.
            QApplication.quit()

    def on_login_window_destroyed(self):
        """
        Menangani kondisi saat window login ditutup manual.

        Penutupan window login bisa berarti user membatalkan login,
        atau bisa juga karena user masuk ke alur lain seperti admin panel.
        Fungsi ini membedakan kedua kondisi tersebut berdasarkan session.
        """
        print("DEBUG: Login window destroyed")

        # Cek apakah signal login selesai sudah diterima sebelumnya.
        if self.login_completed_received:
            # Jika login sudah selesai, event destroy ini tidak perlu diproses lagi.
            print("DEBUG: Login already completed, ignoring destroy event")
            return

        # Jika login belum selesai, cek apakah ternyata sudah ada session aktif.
        session = self.session_manager.load_session()

        if session:
            # Session ada tapi signal login selesai tidak diterima.
            # Kemungkinan user masuk ke admin panel, jadi jangan paksa buka dashboard.
            print("DEBUG: Session exists but login not completed (likely admin panel), staying alive")

            # Simpan session aktif untuk kasus admin panel.
            self.current_session = session

            # Jika remember me mati dan user tidak lanjut ke dashboard,
            # session harus dihapus sekarang juga agar tidak tertinggal.
            if not session.get("remember_me", False):
                print(f"DEBUG: remember_me is OFF (admin panel mode), deleting session IMMEDIATELY")
                result = self.session_manager.delete_session()
                print(f"DEBUG: Session delete result: {result}")
                # Jangan simpan referensi session yang sudah dihapus.
                self.current_session = None
        else:
            # Jika tidak ada session dan login ditutup manual, keluar dari app.
            print("DEBUG: No session and window closed manually, quitting app")
            QApplication.quit()

    def open_dashboard(self, session):
        """
        Membuka dashboard utama menggunakan data session user aktif.

        Session diteruskan ke MainWindow agar dashboard dapat mengatur
        hak akses fitur sesuai role user yang sedang login.
        """
        try:
            # Import dashboard saat benar-benar dibutuhkan agar launcher/login
            # tidak ikut gagal jika konfigurasi runtime dashboard belum lengkap.
            from main import MainWindow

            # Simpan session aktif di launcher.
            self.current_session = session

            # Buat dashboard utama dengan membawa data session user.
            self.main_window = MainWindow(user_session=session)

            # Hubungkan signal logout dari dashboard ke launcher.
            self.main_window.logout_signal.connect(self.handle_logout)

            # Tampilkan dashboard utama.
            self.main_window.show()

            # Jangan hapus session di sini.
            # Penghapusan session dikelola saat logout atau saat aplikasi ditutup.

            return True

        except Exception as e:
            QMessageBox.critical(
                None,
                "Dashboard Error",
                f"❌ Failed to open dashboard:\n{str(e)}"
            )
            return False

    def handle_logout(self):
        """
        Menangani proses logout dari dashboard.

        Fungsi ini menghapus session, menutup dashboard aktif,
        lalu mengembalikan user ke window login.
        """
        try:
            # Hapus session login dari penyimpanan lokal.
            self.session_manager.delete_session()

            # Kosongkan referensi session aktif.
            self.current_session = None

            # Tutup dashboard jika masih terbuka.
            if self.main_window:
                self.main_window.close()
                self.main_window = None

            # Kembali ke halaman login.
            self.open_login()

        except Exception as e:
            QMessageBox.critical(
                None,
                "Logout Error",
                f"❌ Failed to logout:\n{str(e)}"
            )

    def on_app_about_to_quit(self):
        """
        Menangani cleanup saat aplikasi akan ditutup.

        Jika session aktif tidak memakai remember me, session akan dihapus
        agar aplikasi tidak langsung login otomatis pada pembukaan berikutnya.
        """
        # Cek session aktif di memori, lalu fallback ke file jika perlu.
        session = self.current_session

        if not session:
            # Fallback ke file jika referensi session aktif belum terisi.
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
    """
    Menjadi entry point utama aplikasi desktop EcoLab.

    Fungsi ini membuat QApplication, menerapkan stylesheet global,
    membuat launcher, lalu menjalankan event loop Qt.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("EcoLab Dashboard")

    # Terapkan tema terang agar dark mode Windows 11 tidak mengganggu UI.
    app.setStyleSheet(get_light_theme_stylesheet())

    # Buat object launcher aplikasi.
    launcher = AppLauncher()

    # Mulai alur aplikasi.
    launcher.start()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
