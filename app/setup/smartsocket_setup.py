"""
SmartSocket Setup
Setup UI connections untuk Smart Socket features
"""

from PySide6.QtCore import QTimer


class SmartSocketSetup:
    @staticmethod
    def setup(main_window):
        """
        Setup SmartSocket UI connections dan updates

        Args:
            main_window: MainWindow instance
        """
        print("[DEBUG] SmartSocketSetup.setup() called!")  # Debug print
        ui = main_window.ui
        manager = main_window.smartsocket_manager

        # Log start setup
        if hasattr(main_window, 'log'):
            main_window.log("[SmartSocket] Starting setup...")

        # ================= SOCKET 1 =================
        backend1 = manager.get_backend(1)
        backend1.status_changed.connect(
            lambda state: main_window._on_socket_relay_status(1, state)
        )
        backend1.energy_changed.connect(
            lambda data: main_window._on_socket_energy_data(1, data)
        )
        backend1.timer_status_changed.connect(
            lambda status: main_window._on_socket_timer_status(1, status)
        )
        backend1.schedule_status_changed.connect(
            lambda status: main_window._on_socket_schedule_status(1, status)
        )
        backend1.device_status_changed.connect(
            lambda online: main_window._on_socket_device_status(1, online)
        )

        # ================= SOCKET 2 =================
        backend2 = manager.get_backend(2)
        backend2.status_changed.connect(
            lambda state: main_window._on_socket_relay_status(2, state)
        )
        backend2.energy_changed.connect(
            lambda data: main_window._on_socket_energy_data(2, data)
        )
        backend2.timer_status_changed.connect(
            lambda status: main_window._on_socket_timer_status(2, status)
        )
        backend2.schedule_status_changed.connect(
            lambda status: main_window._on_socket_schedule_status(2, status)
        )
        backend2.device_status_changed.connect(
            lambda online: main_window._on_socket_device_status(2, online)
        )

        # ================= SOCKET 3 =================
        backend3 = manager.get_backend(3)
        backend3.status_changed.connect(
            lambda state: main_window._on_socket_relay_status(3, state)
        )
        backend3.energy_changed.connect(
            lambda data: main_window._on_socket_energy_data(3, data)
        )
        backend3.timer_status_changed.connect(
            lambda status: main_window._on_socket_timer_status(3, status)
        )
        backend3.schedule_status_changed.connect(
            lambda status: main_window._on_socket_schedule_status(3, status)
        )
        backend3.device_status_changed.connect(
            lambda online: main_window._on_socket_device_status(3, online)
        )

        # ================= SOCKET 4 =================
        backend4 = manager.get_backend(4)
        backend4.status_changed.connect(
            lambda state: main_window._on_socket_relay_status(4, state)
        )
        backend4.energy_changed.connect(
            lambda data: main_window._on_socket_energy_data(4, data)
        )
        backend4.timer_status_changed.connect(
            lambda status: main_window._on_socket_timer_status(4, status)
        )
        backend4.schedule_status_changed.connect(
            lambda status: main_window._on_socket_schedule_status(4, status)
        )
        backend4.device_status_changed.connect(
            lambda online: main_window._on_socket_device_status(4, online)
        )

        # ================= SOCKET 5 =================
        backend5 = manager.get_backend(5)
        backend5.status_changed.connect(
            lambda state: main_window._on_socket_relay_status(5, state)
        )
        backend5.energy_changed.connect(
            lambda data: main_window._on_socket_energy_data(5, data)
        )
        backend5.timer_status_changed.connect(
            lambda status: main_window._on_socket_timer_status(5, status)
        )
        backend5.schedule_status_changed.connect(
            lambda status: main_window._on_socket_schedule_status(5, status)
        )
        backend5.device_status_changed.connect(
            lambda online: main_window._on_socket_device_status(5, online)
        )

        # Simpan backend references di main_window
        main_window.socket_backends = {
            1: backend1,
            2: backend2,
            3: backend3,
            4: backend4,
            5: backend5,
        }

        # Log setup selesai
        if hasattr(main_window, 'log'):
            main_window.log("[SmartSocket] Setup completed! All 5 sockets ready.")
            main_window.log("[SmartSocket] Backend status initialized")
