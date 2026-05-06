"""Worker thread untuk mengambil data Growatt tanpa memblokir UI utama."""

from PySide6.QtCore import QThread, Signal


class GrowattWorker(QThread):
    """Menjalankan satu siklus fetch Growatt di luar UI thread."""

    data_ready = Signal(dict)
    error = Signal(str)

    def __init__(self, backend):
        """Menyimpan backend Growatt dan state running worker."""
        super().__init__()
        self.backend = backend
        self._running = True

    def run(self):
        """Fetch sekali lalu kirim payload normalisasi lewat Qt signal."""
        try:
            if not self._running:
                return

            data = self.backend.fetch()
            self.data_ready.emit(data)
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        """Menandai worker agar dibatalkan sebelum fetch berikutnya dimulai."""
        self._running = False
