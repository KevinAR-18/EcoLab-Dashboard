from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class AdminPage(QWidget):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.role_changes = {}
        self.summary_labels = {}

        self.setWindowTitle("EcoLab User Management")
        self.resize(1280, 760)
        self.setObjectName("adminPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        heading = self._build_heading()
        summary = self._build_summary_cards()
        self.table = self._build_users_table()

        layout.addWidget(heading)
        layout.addLayout(summary)
        layout.addWidget(self.table)

        self._apply_styles()
        self.refresh()

    def _build_heading(self):
        wrapper = QFrame()
        wrapper.setObjectName("heroCard")
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(6)

        eyebrow = QLabel("ADMIN EDITORIAL")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("User management desk")
        title.setObjectName("pageTitle")
        subtitle = QLabel(
            "Review every account in one surface, confirm role changes deliberately, "
            "and use guarded actions for password and deletion flows."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        return wrapper

    def _build_summary_cards(self):
        layout = QHBoxLayout()
        layout.setSpacing(14)

        for key, label in (
            ("total", "Accounts"),
            ("pending", "Pending"),
            ("active", "Active"),
            ("blocked", "Blocked"),
            ("admins", "Admins"),
        ):
            card = QFrame()
            card.setObjectName("summaryCard")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 16, 18, 16)
            card_layout.setSpacing(2)

            value = QLabel("0")
            value.setObjectName("summaryValue")
            caption = QLabel(label)
            caption.setObjectName("summaryLabel")

            card_layout.addWidget(value)
            card_layout.addWidget(caption)
            layout.addWidget(card)
            self.summary_labels[key] = value

        return layout

    def _build_users_table(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["Username", "Email", "Role", "Status", "Created", "Actions"]
        )
        table.setAlternatingRowColors(False)
        table.setShowGrid(False)
        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        table.setMouseTracking(True)
        return table

    def refresh(self):
        users = self.service.get_all_users()
        summary = self.service.get_user_summary()

        self.table.setRowCount(0)
        for key, widget in self.summary_labels.items():
            widget.setText(str(summary.get(key, 0)))

        for user in users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setRowHeight(row, 58)

            self.table.setItem(row, 0, self._text_item(user["username"] or "Unknown"))
            self.table.setItem(row, 1, self._text_item(user["email"]))
            self.table.setCellWidget(row, 2, self._build_role_editor(user))
            self.table.setItem(row, 3, self._status_item(user["status"]))
            self.table.setItem(row, 4, self._text_item(user["date"] or "-"))
            self.table.setCellWidget(row, 5, self._build_actions(user))

    def approve(self, uid):
        self._show_result(self.service.update_user_status(uid, "active"))
        self.refresh()

    def block(self, uid):
        self._show_result(self.service.update_user_status(uid, "blocked"))
        self.refresh()

    def unblock(self, uid):
        self._show_result(self.service.update_user_status(uid, "active"))
        self.refresh()

    def confirm_role_change(self, uid):
        selected_role = self.role_changes.get(uid)
        user = self.service.get_user_record(uid) or {}
        if not selected_role or selected_role == user.get("role", user.get("role_request", "user")):
            return

        result = self.service.update_user_role(uid, selected_role)
        self._show_result(result)
        if result.get("status") == "success":
            self.role_changes.pop(uid, None)
            self.refresh()

    def open_password_dialog(self, user):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set user password")
        dialog.setModal(True)
        dialog.setObjectName("passwordDialog")

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        context = QLabel(f"{user['username']} <{user['email']}>")
        context.setObjectName("dialogContext")
        password = QLineEdit()
        password.setPlaceholderText("New password")
        password.setEchoMode(QLineEdit.Password)

        actions = QHBoxLayout()
        cancel = QPushButton("Cancel")
        confirm = QPushButton("Update Password")
        confirm.setObjectName("primaryButton")
        actions.addWidget(cancel)
        actions.addWidget(confirm)

        layout.addWidget(context)
        layout.addWidget(password)
        layout.addLayout(actions)

        cancel.clicked.connect(dialog.reject)

        def submit():
            if not password.text().strip():
                QMessageBox.warning(dialog, "Password Required", "Enter a password first.")
                return

            result = self.service.set_user_password(user["uid"], password.text().strip())
            self._show_result(result)
            if result.get("status") == "success":
                dialog.accept()

        confirm.clicked.connect(submit)
        dialog.exec()

    def confirm_delete(self, user):
        answer = QMessageBox.question(
            self,
            "Delete User",
            (
                f"Delete {user['email']}?\n\n"
                "This removes the Firebase Auth account and the database record."
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        self._show_result(self.service.delete_user(user["uid"]))
        self.refresh()

    def _build_role_editor(self, user):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        combo = QComboBox()
        combo.addItems(["admin", "user"])
        combo.setCurrentText(user["role"])

        confirm = QPushButton("Confirm")
        confirm.setProperty("kind", "quiet")
        confirm.setEnabled(False)

        def on_role_changed(value):
            if value == user["role"]:
                self.role_changes.pop(user["uid"], None)
                confirm.setEnabled(False)
                return

            self.role_changes[user["uid"]] = value
            confirm.setEnabled(True)

        combo.currentTextChanged.connect(on_role_changed)
        confirm.clicked.connect(lambda: self.confirm_role_change(user["uid"]))

        layout.addWidget(combo)
        layout.addWidget(confirm)
        return container

    def _build_actions(self, user):
        container = QWidget()
        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(8)
        layout.setVerticalSpacing(6)

        column = 0
        for label, callback, kind in self._status_actions(user):
            button = QPushButton(label)
            button.setProperty("kind", kind)
            button.clicked.connect(callback)
            layout.addWidget(button, 0, column)
            column += 1

        password = QPushButton("Password")
        password.setProperty("kind", "secondary")
        password.clicked.connect(lambda: self.open_password_dialog(user))
        layout.addWidget(password, 1, 0)

        delete = QPushButton("Delete")
        delete.setProperty("kind", "danger")
        delete.clicked.connect(lambda: self.confirm_delete(user))
        layout.addWidget(delete, 1, 1)
        return container

    def _status_actions(self, user):
        status = user["status"]
        if status == "pending":
            return [
                ("Approve", lambda: self.approve(user["uid"]), "primary"),
                ("Block", lambda: self.block(user["uid"]), "secondary"),
            ]
        if status == "active":
            return [("Block", lambda: self.block(user["uid"]), "secondary")]
        if status == "blocked":
            return [("Unblock", lambda: self.unblock(user["uid"]), "primary")]
        return []

    def _show_result(self, result):
        if result.get("status") == "success":
            QMessageBox.information(self, "Admin", result.get("message", "Success"))
            return

        QMessageBox.warning(self, "Admin Error", result.get("message", "Unknown error"))

    @staticmethod
    def _text_item(text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        return item

    @staticmethod
    def _status_item(status):
        labels = {
            "pending": "Pending review",
            "active": "Active",
            "blocked": "Blocked",
        }
        item = QTableWidgetItem(labels.get(status, status.title()))
        item.setTextAlignment(Qt.AlignCenter)
        if status == "pending":
            item.setForeground(QColor("#8f5a00"))
        elif status == "blocked":
            item.setForeground(QColor("#8a1c1c"))
        else:
            item.setForeground(QColor("#21543d"))
        return item

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QWidget#adminPage {
                background: #f4efe6;
                color: #171412;
                font-family: "Georgia";
            }
            QFrame#heroCard, QFrame#summaryCard {
                background: #fcfaf5;
                border: 1px solid #d8cfbf;
                border-radius: 20px;
            }
            QLabel#eyebrow {
                color: #7f6b4d;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }
            QLabel#pageTitle {
                font-size: 34px;
                font-weight: 700;
                color: #111111;
            }
            QLabel#subtitle {
                font-size: 14px;
                color: #52473a;
            }
            QLabel#summaryValue {
                font-size: 24px;
                font-weight: 700;
                color: #111111;
            }
            QLabel#summaryLabel {
                font-size: 12px;
                color: #6d6254;
                text-transform: uppercase;
            }
            QHeaderView::section {
                background: transparent;
                color: #665846;
                border: none;
                padding: 10px 12px;
                font-size: 12px;
                font-weight: 700;
            }
            QTableWidget {
                background: #fcfaf5;
                border: 1px solid #d8cfbf;
                border-radius: 20px;
                gridline-color: transparent;
                padding: 10px;
                alternate-background-color: #f9f3e8;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ece3d4;
            }
            QTableWidget::item:hover {
                background: #f2eadc;
            }
            QPushButton {
                min-height: 30px;
                border-radius: 15px;
                padding: 0 14px;
                border: 1px solid #cdbfa8;
                background: #f7f1e5;
                color: #1d1a17;
            }
            QPushButton:hover {
                background: #efe5d4;
            }
            QPushButton#primaryButton,
            QPushButton[kind="primary"] {
                background: #1b4d3e;
                border-color: #1b4d3e;
                color: #fffdf7;
            }
            QPushButton#primaryButton:hover,
            QPushButton[kind="primary"]:hover {
                background: #173f34;
            }
            QPushButton[kind="secondary"] {
                background: #ece3d4;
            }
            QPushButton[kind="quiet"] {
                background: #f9f5ed;
            }
            QPushButton[kind="danger"] {
                background: #fff0ec;
                border-color: #d9a49c;
                color: #912f1f;
            }
            QComboBox, QLineEdit {
                min-height: 32px;
                border-radius: 16px;
                border: 1px solid #cdbfa8;
                background: #fffdf8;
                padding: 0 10px;
            }
            QDialog#passwordDialog {
                background: #fcfaf5;
            }
            QLabel#dialogContext {
                color: #5f5344;
            }
            """
        )
