"""Helper untuk menghubungkan signal backend Smart Socket ke UI dashboard."""


class SmartSocketSetup:
    @staticmethod
    def setup(main_window):
        """Menghubungkan semua backend Smart Socket ke handler milik MainWindow."""
        manager = main_window.smartsocket_manager

        if hasattr(main_window, "log"):
            main_window.log("[SmartSocket] Starting setup...")

        # Helper ini menjaga wiring lima socket tetap ringkas dan tidak
        # menumpuk di constructor MainWindow.
        for socket_number in range(1, 6):
            backend = manager.get_backend(socket_number)
            backend.status_changed.connect(
                lambda state, n=socket_number: main_window._on_socket_relay_status(n, state)
            )
            backend.energy_changed.connect(
                lambda data, n=socket_number: main_window._on_socket_energy_data(n, data)
            )
            backend.timer_status_changed.connect(
                lambda status, n=socket_number: main_window._on_socket_timer_status(n, status)
            )
            backend.schedule_status_changed.connect(
                lambda status, n=socket_number: main_window._on_socket_schedule_status(n, status)
            )
            backend.device_status_changed.connect(
                lambda online, n=socket_number: main_window._on_socket_device_status(n, online)
            )

        main_window.socket_backends = {
            socket_number: manager.get_backend(socket_number)
            for socket_number in range(1, 6)
        }

        if hasattr(main_window, "log"):
            main_window.log("[SmartSocket] Setup completed! All 5 sockets ready.")
            # main_window.log("[SmartSocket] Backend status initialized")
