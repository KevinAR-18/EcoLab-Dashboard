"""
Utility path resolution untuk EcoLab.

Modul ini membantu resolve path resource saat aplikasi dijalankan
di development mode maupun saat sudah dibundle jadi executable.
"""
import os
import sys
from pathlib import Path


def _project_root():
    """Mengembalikan root aplikasi untuk mode script atau executable."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_resource_path(relative_path):
    """
    Mengubah path relatif resource menjadi absolute path.

    Args:
        relative_path: Path relatif dari project root

    Returns:
        str: Absolute path ke file resource

    Contoh:
        # Development
        get_resource_path("images/logo.png")
        -> D:\\Project\\images\\logo.png

        # PyInstaller (frozen)
        get_resource_path("images/logo.png")
        -> C:\\Users\\...\\AppData\\Local\\Temp\\_MEI12345\\images\\logo.png
    """
    try:
        # PyInstaller membuat folder temp dan menyimpannya di `_MEIPASS`.
        base_path = sys._MEIPASS
    except AttributeError:
        # Development mode: gunakan root project.
        base_path = str(_project_root())

    return os.path.join(base_path, relative_path)


def get_base_path():
    """
    Mengambil base path aplikasi saat ini.

    Returns:
        str: Base path aplikasi
    """
    try:
        return sys._MEIPASS
    except AttributeError:
        return str(_project_root())


def get_credentials_path(filename):
    """
    Menghasilkan absolute path ke file di folder `credentials`.

    Args:
        filename: Nama file di credentials folder

    Returns:
        str: Absolute path ke file credentials

    Note:
        File credentials tidak di-bundle ke dalam `.exe`,
        jadi selalu diambil dari folder eksternal.
    """
    # Credentials selalu berada di folder eksternal, bukan di dalam bundle exe.
    if getattr(sys, 'frozen', False):
        # Frozen mode: credentials berada di sebelah file exe.
        exe_dir = os.path.dirname(sys.executable)
        return os.path.join(exe_dir, "credentials", filename)
    else:
        # Development mode: credentials berada di folder project.
        return os.path.join(str(_project_root()), "credentials", filename)


def get_images_path(filename):
    """
    Menghasilkan absolute path ke file di folder `images`.

    Args:
        filename: Nama file di images folder

    Returns:
        str: Absolute path ke file gambar
    """
    return get_resource_path(os.path.join("images", filename))


def get_icon_path(filename):
    """
    Menghasilkan absolute path ke file di folder `icon`.

    Args:
        filename: Nama file di icon folder

    Returns:
        str: Absolute path ke file icon
    """
    return get_resource_path(os.path.join("icon", filename))


# Alias untuk backward compatibility
def resource_path(relative_path):
    """Alias lama untuk `get_resource_path()`."""
    return get_resource_path(relative_path)
