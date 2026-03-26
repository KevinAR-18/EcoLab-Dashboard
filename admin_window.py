"""
Admin Panel Window
Window untuk menampilkan admin panel dengan tombol back
"""
import os
from PySide6.QtCore import Qt, QTimer, QDateTime, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QComboBox, QPushButton, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QDialog, QInputDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QHeaderView
)

# Import Auth Service untuk Firebase
from auth_service import TrialLoginService


class Date:
    """Helper class untuk update waktu dan tanggal"""
    def update_time(self, label: QLabel):
        current_time = QDateTime.currentDateTime()

        time_text = current_time.toString("HH:mm")
        date_text = current_time.toString("dddd, dd MMMM yyyy")

        label.setText(QCoreApplication.translate("MainWindow", f"{time_text} - {date_text}", None))


class UserActionDialog(QDialog):
    """Dialog popup untuk action pada user"""

    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.user_data = user_data or {}
        self.choice = None
        self.setup_ui()

    def setup_ui(self):
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setWindowTitle("User Actions")

        # Set frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Main container
        container = QWidget()
        container.setObjectName("actionContainer")
        container.setStyleSheet("""
            QWidget#actionContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E1F2FB, stop:1 #F1F9F9);
                border-radius: 15px;
                border: 2px solid #005C99;
            }
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        # Title
        title = QLabel(f"User Actions: {self.user_data.get('username', 'N/A')}")
        title.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #1f3c5a;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # User info
        info_text = f"Email: {self.user_data.get('email', 'N/A')}\nStatus: {self.user_data.get('status', 'N/A')}\nAuth: {self.user_data.get('auth_provider', 'N/A')}"
        info = QLabel(info_text)
        info.setStyleSheet("""
            QLabel {
                font-size: 10pt;
                color: #4a647d;
                background: transparent;
                padding: 10px;
            }
        """)
        layout.addWidget(info)

        layout.addSpacing(10)

        # Action buttons
        self.approve_btn = QPushButton("✅ Approve Account")
        self.approve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.approve_btn.setMinimumHeight(40)
        self.approve_btn.setStyleSheet(self._button_style("#28a745"))
        self.approve_btn.clicked.connect(self.approve_action)

        # Disable approve button jika status bukan pending
        user_status = self.user_data.get('status', '')
        if user_status != 'pending':
            self.approve_btn.setEnabled(False)
            self.approve_btn.setText(f"✅ Approve Account ({user_status.capitalize()})")
            self.approve_btn.setStyleSheet(self._button_style("#cccccc"))

        layout.addWidget(self.approve_btn)

        self.password_btn = QPushButton("🔐 Update Password")
        self.password_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.password_btn.setMinimumHeight(40)
        self.password_btn.setStyleSheet(self._button_style("#17a2b8"))
        self.password_btn.clicked.connect(self.update_password_action)
        layout.addWidget(self.password_btn)

        self.block_btn = QPushButton("🚫 Block/Unblock Account")
        self.block_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.block_btn.setMinimumHeight(40)
        self.block_btn.setStyleSheet(self._button_style("#ffc107"))
        self.block_btn.clicked.connect(self.block_action)
        layout.addWidget(self.block_btn)

        self.delete_btn = QPushButton("🗑️ Delete User")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setStyleSheet(self._button_style("#dc3545"))
        self.delete_btn.clicked.connect(self.delete_action)
        layout.addWidget(self.delete_btn)

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

        # Disable update password untuk Google auth
        if self.user_data.get('auth_provider') == 'google':
            self.password_btn.setEnabled(False)
            self.password_btn.setText("🔐 Update Password (Google Auth - N/A)")
            self.password_btn.setStyleSheet(self._button_style("#cccccc"))

    def _button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 11pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}bb;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """

    def approve_action(self):
        self.choice = "approve"
        self.accept()

    def update_password_action(self):
        self.choice = "update_password"
        self.accept()

    def block_action(self):
        self.choice = "block_unblock"
        self.accept()

    def delete_action(self):
        self.choice = "delete"
        self.accept()


class AdminPanelWindow(QMainWindow):
    """Admin Panel Window dengan tombol back yang bisa kembali ke popup"""

    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window  # Simpan reference ke login window
        self.users_data = []  # Store user data for reference

        # Import admin panel UI
        from ui_adminpanel import Ui_MainWindow as AdminPanelUI
        from ui_functions import UIFunctions

        self.ui = AdminPanelUI()
        self.ui.setupUi(self)
        self.ui_functions = UIFunctions(self)

        # ROOT & BODY LAYOUT (SAMA SEPERTI MAIN.PY)
        for w in [self.ui.styleSheet, self.ui.bgApp]:
            w.setContentsMargins(0, 0, 0, 0)
            if w.layout():
                w.layout().setContentsMargins(0, 0, 0, 0)
                w.layout().setSpacing(0)

        self.ui.contentTop.setContentsMargins(0, 0, 0, 0)

        # WINDOW SETTINGS (SAMA SEPERTI MAIN.PY)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("EcoLab Admin Panel")

        # Mengatur Icon Aplikasi
        pixmap = QPixmap(self.resource_path("icon\\logoecolab.ico"))
        icon = QIcon(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.setWindowIcon(icon)

        # Connect signals
        self.ui.minimizeAppBtn.clicked.connect(self.showMinimized)
        self.ui.maximizeRestoreAppBtn.clicked.connect(self.ui_functions.toggle_max_restore)
        self.ui.closeAppBtn.clicked.connect(self.close)
        self.ui.btn_back.clicked.connect(self.go_back_to_selection)

        # Mouse events for dragging
        self.mousePressEvent = lambda e: self.ui_functions.mouse_press(e) if e.button() == Qt.MouseButton.LeftButton else None
        self.mouseMoveEvent = self.ui_functions.mouse_move

        # Setup Date & Clock Helper
        self.date_helper = Date()

        # Setup Firebase Auth Service
        self.auth_service = TrialLoginService()

        # Setup tabel
        self.setup_table()

        # Setup clock timer (update setiap 1 detik)
        self.setup_clock_timer()

        # Load data dari Firebase
        self.load_firebase_data()

    def setup_clock_timer(self):
        """Setup timer untuk update jam setiap 1 detik"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            lambda: self.date_helper.update_time(self.ui.clockInfo)
        )
        self.timer.start(1000)  # 1 detik

    def setup_table(self):
        """Setup struktur tabel"""
        table = self.ui.tabeldata

        # Set column count: No, Username, Email, Role, Status, Created, Action
        table.setColumnCount(7)

        # Set header labels
        table.setHorizontalHeaderLabels(["No", "Username", "Email", "Role", "Status", "Created", "Action"])

        # Set column resize mode - AUTO STRETCH
        header = table.horizontalHeader()

        # Kolom yang melebar otomatis (stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # No - auto
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)          # Username - stretch
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # Email - stretch
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)            # Role - FIXED
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Status - auto
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Created - auto
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)            # Action - FIXED

        # Set fixed width untuk Role dan Action
        table.setColumnWidth(3, 120)  # Role (dropdown) - FIXED
        table.setColumnWidth(6, 100)  # Action - FIXED

        # Set row height (lebih besar agar button dan dropdown nggak kepotong)
        table.verticalHeader().setDefaultSectionSize(50)

        # Set table properties
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

    def load_firebase_data(self):
        """Load semua data dari Firebase dan populate tabel & summary"""
        try:
            # Load summary data
            summary = self.auth_service.get_user_summary()

            # Update summary labels
            self.ui.labelAccountsCount.setText(str(summary["total"]))
            self.ui.labelPendingCount.setText(str(summary["pending"]))
            self.ui.labelActiveCount.setText(str(summary["active"]))
            self.ui.labelBlockedCount.setText(str(summary["blocked"]))
            self.ui.labelAdminsCount.setText(str(summary["admins"]))

            # Load user data untuk tabel
            users = self.auth_service.get_all_users()
            self.users_data = users  # Store untuk reference

            # Populate tabel
            self.populate_table(users)

        except Exception as e:
            print(f"Error loading Firebase data: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load data:\n{str(e)}")

    def populate_table(self, users):
        """Populate tabel dengan user data"""
        table = self.ui.tabeldata
        table.setRowCount(len(users))

        for row, user in enumerate(users):
            # Nomor (CENTER)
            no_item = QTableWidgetItem(str(row + 1))
            no_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 0, no_item)

            # Username
            username_item = QTableWidgetItem(user["username"])
            table.setItem(row, 1, username_item)

            # Email
            email_item = QTableWidgetItem(user["email"])
            table.setItem(row, 2, email_item)

            # Role (Dropdown)
            role_combo = QComboBox()
            role_combo.addItem("user")
            role_combo.addItem("admin")
            role_combo.setCurrentText(user["role"])
            role_combo.currentTextChanged.connect(
                lambda text, uid=user["uid"]: self.on_role_changed(uid, text)
            )
            role_combo.setStyleSheet("""
                QComboBox {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8f9fa, stop:1 #e9ecef);
                    color: #495057;
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-size: 10pt;
                    font-weight: 600;
                    min-width: 80px;
                }
                QComboBox:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f1f3f5);
                    border: 2px solid #adb5bd;
                }
                QComboBox:focus {
                    border: 2px solid #74c0fc;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f8f9fa);
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: right center;
                    width: 30px;
                    border: none;
                    border-radius: 6px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4dabf7, stop:1 #339af0);
                    margin-right: 4px;
                }
                QComboBox::drop-down:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #74c0fc, stop:1 #4dabf7);
                }
                QComboBox::drop-down:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #339af0, stop:1 #228be6);
                }
                QComboBox::down-arrow {
                    image: none;
                    border: 6px solid transparent;
                    border-top: 4px solid #ffffff;
                    width: 0;
                    height: 0;
                    margin-top: 2px;
                }
                QComboBox QAbstractItemView {
                    background: white;
                    border: 2px solid #dee2e6;
                    border-radius: 0px;
                    selection-background-color: transparent;
                    selection-color: #1971c2;
                    outline: none;
                    padding: 4px;
                    show-decoration-selected: 1;
                }
                QComboBox QAbstractItemView::item {
                    height: 24px;
                    padding: 4px 10px;
                    color: #495057;
                    font-weight: 600;
                    border-radius: 6px;
                    margin: 2px;
                }
                QComboBox QAbstractItemView::item:hover {
                    background: #f1f3f5;
                    color: #1971c2;
                }
                QComboBox QAbstractItemView::item:selected {
                    background: #e7f5ff;
                    color: #1971c2;
                }
            """)
            table.setCellWidget(row, 3, role_combo)

            # Status (CENTER)
            status_item = QTableWidgetItem(user["status"].capitalize())
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Color coding untuk status
            if user["status"] == "active":
                status_item.setForeground(Qt.GlobalColor.green)
            elif user["status"] == "pending":
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            elif user["status"] == "blocked":
                status_item.setForeground(Qt.GlobalColor.red)
            table.setItem(row, 4, status_item)

            # Created (CENTER)
            created_date = user["date"]  # Format: YYYY-MM-DD
            created_item = QTableWidgetItem(created_date)
            created_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 5, created_item)

            # Action Button (CENTER via widget alignment)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            action_btn = QPushButton("Action")
            action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            action_btn.setFixedSize(75, 30)
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2b6cb0;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 4px 8px;
                    font-size: 9pt;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1e4f8a;
                }
                QPushButton:pressed {
                    background-color: #174173;
                }
            """)
            action_btn.clicked.connect(lambda checked, u=user: self.show_action_dialog(u))
            action_layout.addWidget(action_btn)

            table.setCellWidget(row, 6, action_widget)

    def on_role_changed(self, uid, new_role):
        """Handle ketika role dropdown diubah"""
        try:
            # Confirm dialog
            reply = QMessageBox.question(
                self,
                "Confirm Role Change",
                f"Are you sure you want to change this user's role to '{new_role}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Update role di Firebase
                result = self.auth_service.update_user_role(uid, new_role)

                if result["status"] == "success":
                    QMessageBox.information(self, "Success", "✅ Role updated successfully!")
                    # Refresh data
                    self.load_firebase_data()
                else:
                    QMessageBox.critical(self, "Error", f"❌ Failed to update role:\n{result['message']}")
            else:
                # Refresh table untuk revert dropdown
                self.load_firebase_data()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Error changing role:\n{str(e)}")
            self.load_firebase_data()

    def show_action_dialog(self, user):
        """Tampilkan dialog action untuk user"""
        dialog = UserActionDialog(self, user_data=user)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            action = dialog.choice
            self.handle_user_action(user, action)

    def handle_user_action(self, user, action):
        """Handle action yang dipilih untuk user"""
        uid = user["uid"]
        username = user["username"]

        try:
            if action == "approve":
                # Approve account
                result = self.auth_service.approve_user(uid)
                if result["status"] == "success":
                    QMessageBox.information(self, "Success", f"✅ User '{username}' approved successfully!")
                else:
                    QMessageBox.critical(self, "Error", f"❌ Failed to approve:\n{result['message']}")

            elif action == "update_password":
                # Update password (hanya untuk non-Google auth)
                if user.get("auth_provider") == "google":
                    QMessageBox.warning(self, "Not Available", "Cannot update password for Google accounts.")
                    return

                # Input dialog untuk password baru
                new_password, ok = QInputDialog.getText(
                    self,
                    "Update Password",
                    f"Enter new password for '{username}':",
                    QLineEdit.EchoMode.Password
                )

                if ok and new_password:
                    if len(new_password) < 6:
                        QMessageBox.warning(self, "Invalid Password", "Password must be at least 6 characters!")
                        return

                    result = self.auth_service.set_user_password(uid, new_password)
                    if result["status"] == "success":
                        QMessageBox.information(self, "Success", f"✅ Password updated for '{username}'!")
                    else:
                        QMessageBox.critical(self, "Error", f"❌ Failed to update password:\n{result['message']}")

            elif action == "block_unblock":
                # Toggle block/unblock
                current_status = user["status"]
                new_status = "blocked" if current_status == "active" else "active"

                confirm_msg = f"Are you sure you want to {'block' if new_status == 'blocked' else 'unblock'} '{username}'?"

                reply = QMessageBox.question(
                    self,
                    f"{'Block' if new_status == 'blocked' else 'Unblock'} Account",
                    confirm_msg,
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    result = self.auth_service.update_user_status(uid, new_status)
                    if result["status"] == "success":
                        action_text = "blocked" if new_status == "blocked" else "unblocked"
                        QMessageBox.information(self, "Success", f"✅ User '{username}' {action_text} successfully!")
                    else:
                        QMessageBox.critical(self, "Error", f"❌ Failed to update status:\n{result['message']}")

            elif action == "delete":
                # Delete user
                reply = QMessageBox.question(
                    self,
                    "Delete User",
                    f"⚠️ Are you sure you want to delete '{username}'?\n\nThis action CANNOT be undone!",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    result = self.auth_service.delete_user(uid)
                    if result["status"] == "success":
                        # Cek jika ini Google user
                        if result.get("warning") == "google_auth":
                            QMessageBox.warning(
                                self,
                                "Partial Success",
                                f"⚠️ User '{username}' removed from database!\n\n"
                                f"However, this is a Google Auth account.\n"
                                f"User may still be able to login again with Google.\n\n"
                                f"To permanently block, use 'Block Account' instead."
                            )
                        else:
                            QMessageBox.information(self, "Success", f"✅ User '{username}' deleted successfully!")
                    else:
                        QMessageBox.critical(self, "Error", f"❌ Failed to delete user:\n{result['message']}")

            # Refresh data setelah action
            self.load_firebase_data()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Error performing action:\n{str(e)}")

    def go_back_to_selection(self):
        """Kembali ke popup pilihan dashboard/admin panel"""
        self.close()  # Close admin panel

        # Show login window lagi
        if self.login_window:
            self.login_window.show_admin_selection_dialog()

    def resource_path(self, relative_path):
        """ Mengonversi path relatif menjadi path absolut.
        Berguna untuk memastikan file dapat ditemukan dari
        direktori aplikasi saat ini.
        """
        base_path = os.path.abspath(".")  # Mengatur ke directory saat ini.
        return os.path.join(base_path, relative_path)
