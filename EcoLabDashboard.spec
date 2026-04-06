# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('images', 'images'), ('icon', 'icon')]
binaries = []
hiddenimports = ['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'pyrebase', 'requests', 'google.oauth2.service_account', 'google_auth_oauthlib.flow', 'google.auth.transport.requests', 'loginmain', 'admin_window', 'session_manager', 'auth_service', 'firebase_settings', 'ui_theme_helper', 'lamp_setup', 'switch_setup', 'ac_setup', 'arrow_setup', 'smartsocket_popup', 'smartsocket_setup', 'ui_loginpage', 'ui_mainwindow', 'ui_functions', 'ui_role_selection', 'widgets.lamp_button', 'backend.growatt_backend', 'backend.weathercloud_backend', 'backend.mqtt_client', 'backend.mqtt_dht22_backend', 'backend.lampbutton_backend', 'backend.acbutton_backend', 'backend.growatt_worker', 'backend.mcu_status_backend', 'backend.smartsocket_backend']
tmp_ret = collect_all('pyrebase')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('google')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EcoLabDashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon\\logoecolab.ico'],
)
