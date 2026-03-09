from PySide6.QtWidgets import (
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class AdminPage(QWidget):
    def __init__(self, service):
        super().__init__()
        self.service = service

        self.setWindowTitle("Admin Panel")
        self.resize(900, 500)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.pending_tab = QWidget()
        self.active_tab = QWidget()
        self.block_tab = QWidget()

        self.tabs.addTab(self.pending_tab, "Signup Requests")
        self.tabs.addTab(self.active_tab, "Active Users")
        self.tabs.addTab(self.block_tab, "Blocked Users")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self._build_pending_table()
        self.refresh()

    def _build_pending_table(self):
        layout = QVBoxLayout()

        self.pending = QTableWidget()
        self.pending.setColumnCount(6)
        self.pending.setHorizontalHeaderLabels(
            ["Username", "Email", "Role Request", "Date", "Approve", "Reject"]
        )

        layout.addWidget(self.pending)
        self.pending_tab.setLayout(layout)

    def refresh(self):
        self.pending.setRowCount(0)

        for user in self.service.get_pending_users():
            row = self.pending.rowCount()
            self.pending.insertRow(row)

            self.pending.setItem(row, 0, QTableWidgetItem(user["username"]))
            self.pending.setItem(row, 1, QTableWidgetItem(user["email"]))
            self.pending.setItem(row, 2, QTableWidgetItem(user["role_request"]))
            self.pending.setItem(row, 3, QTableWidgetItem(user["date"]))

            approve = QPushButton("Approve")
            reject = QPushButton("Reject")

            approve.clicked.connect(lambda _, uid=user["uid"]: self.approve(uid))
            reject.clicked.connect(lambda _, uid=user["uid"]: self.reject(uid))

            self.pending.setCellWidget(row, 4, approve)
            self.pending.setCellWidget(row, 5, reject)

    def approve(self, uid):
        self.service.approve_user(uid)
        self.refresh()

    def reject(self, uid):
        self.service.reject_user(uid)
        self.refresh()
