from PySide6.QtCore import QThread, Signal


class GrowattWorker(QThread):
    """Run one Growatt fetch cycle outside the UI thread."""

    data_ready = Signal(dict)
    error = Signal(str)

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self._running = True

    def run(self):
        """Fetch once and return the normalized payload through Qt signals."""
        try:
            if not self._running:
                return

            data = self.backend.fetch()
            self.data_ready.emit(data)

        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        """Mark the worker as cancelled before the next fetch starts."""
        self._running = False
