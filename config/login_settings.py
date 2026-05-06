"""
Login UI settings untuk EcoLab.

Berisi konfigurasi sederhana yang dipakai oleh login page,
terutama untuk default behavior dan password field.
"""

# Password settings
PASSWORD_MASK = "•"  # Karakter untuk mask password
SHOW_PASSWORD_DEFAULT = False  # Default state show password checkbox


# UI behavior settings
REMEMBER_ME_DEFAULT = False  # Default state remember me checkbox
AUTO_SWITCH_TO_SIGNUP = True  # Otomatis switch ke signup setelah klik "Create Account"


# Navigation settings
DEFAULT_PAGE = "signin"  # Halaman default: "signin" atau "signup"


# Style settings
PASSWORD_FIELD_STYLE = """
QLineEdit {
    background: white;
    border: 1px solid #cfd8e3;
    border-radius: 8px;
    padding: 8px;
    font-size: 12pt;
}
QLineEdit:focus {
    border: 1px solid #2b6cb0;
}
"""


def get_echo_mode(show_password):
    """
    Mengembalikan echo mode password field berdasarkan state checkbox.

    Args:
        show_password (bool): True untuk show, False untuk hide

    Returns:
        QLineEdit.EchoMode: Mode normal atau password
    """
    from PySide6.QtWidgets import QLineEdit

    return QLineEdit.EchoMode.Normal if show_password else QLineEdit.EchoMode.Password


def toggle_password_visibility(password_field, show_checkbox):
    """
    Mengubah visibility password field sesuai state checkbox.

    Args:
        password_field: QLineEdit password field
        show_checkbox: QCheckBox untuk toggle visibility
    """
    from PySide6.QtWidgets import QLineEdit

    # Helper ini dipakai oleh halaman sign in dan sign up agar behavior
    # password field tetap konsisten di seluruh login window.

    if show_checkbox.isChecked():
        password_field.setEchoMode(QLineEdit.EchoMode.Normal)
    else:
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
