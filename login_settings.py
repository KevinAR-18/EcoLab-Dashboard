"""
Login UI Settings
Konfigurasi umum untuk UI Login Page
"""

# Password Settings
PASSWORD_MASK = "•"  # Karakter untuk mask password
SHOW_PASSWORD_DEFAULT = False  # Default state show password checkbox


# UI Behavior Settings
REMEMBER_ME_DEFAULT = False  # Default state remember me checkbox
AUTO_SWITCH_TO_SIGNUP = True  # Otomatis switch ke signup setelah klik "Create Account"


# Navigation Settings
DEFAULT_PAGE = "signin"  # Halaman default: "signin" atau "signup"


# Style Settings (bisa dikembangkan)
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
    Get echo mode untuk password field berdasarkan state show password

    Args:
        show_password (bool): True untuk show, False untuk hide

    Returns:
        QLineEdit.EchoMode: Normal atau Password
    """
    from PySide6.QtWidgets import QLineEdit

    return QLineEdit.EchoMode.Normal if show_password else QLineEdit.EchoMode.Password


def toggle_password_visibility(password_field, show_checkbox):
    """
    Toggle visibility password field

    Args:
        password_field: QLineEdit password field
        show_checkbox: QCheckBox untuk toggle visibility
    """
    from PySide6.QtWidgets import QLineEdit

    if show_checkbox.isChecked():
        password_field.setEchoMode(QLineEdit.EchoMode.Normal)
    else:
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
