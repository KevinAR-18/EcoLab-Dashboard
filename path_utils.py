"""
Path resolution utility untuk PyInstaller
Menghandle path relatif untuk development dan frozen executable
"""
import os
import sys
from pathlib import Path


def get_resource_path(relative_path):
    """
    Get absolute path ke resource file

    Args:
        relative_path: Path relatif dari project root

    Returns:
        Absolute path ke file

    Contoh:
        # Development
        get_resource_path("images/logo.png")
        → D:\Project\images\logo.png

        # PyInstaller (frozen)
        get_resource_path("images/logo.png")
        → C:\Users\...\AppData\Local\Temp\_MEI12345\images\logo.png
    """
    try:
        # PyInstaller creates temp folder & stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Development mode: gunakan script directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_base_path():
    """
    Get base path aplikasi

    Returns:
        Base path aplikasi (temp folder untuk frozen, script dir untuk dev)
    """
    try:
        return sys._MEIPASS
    except AttributeError:
        return os.path.abspath(".")


def get_credentials_path(filename):
    """
    Get path ke credentials folder

    Args:
        filename: Nama file di credentials folder

    Returns:
        Absolute path ke file credentials

    Note:
        Credentials TIDAK di-bundle di .exe, jadi selalu ambil dari folder eksternal
    """
    # Credentials selalu di folder eksternal (bukan di .exe)
    if getattr(sys, 'frozen', False):
        # Frozen mode: credentials di sebelah .exe
        exe_dir = os.path.dirname(sys.executable)
        return os.path.join(exe_dir, "credentials", filename)
    else:
        # Development mode: credentials di project folder
        return os.path.join(os.path.abspath("."), "credentials", filename)


def get_images_path(filename):
    """
    Get path ke images folder

    Args:
        filename: Nama file di images folder

    Returns:
        Absolute path ke file image
    """
    return get_resource_path(os.path.join("images", filename))


def get_icon_path(filename):
    """
    Get path ke icon folder

    Args:
        filename: Nama file di icon folder

    Returns:
        Absolute path ke file icon
    """
    return get_resource_path(os.path.join("icon", filename))


# Backward compatible aliases
def resource_path(relative_path):
    """Alias untuk get_resource_path()"""
    return get_resource_path(relative_path)
