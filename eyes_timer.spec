# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['rumps'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure)

exe = EXE(pyz, a.scripts, exclude_binaries=True, name='Eyes Timer', console=False)

coll = COLLECT(exe, a.binaries, a.datas, name='Eyes Timer')

app = BUNDLE(
    coll,
    name='Eyes Timer.app',
    bundle_identifier='com.eyestimer.app',
    info_plist={
        'CFBundleName': 'Eyes Timer',
        'CFBundleDisplayName': 'Eyes Timer',
        'CFBundleVersion': '1.0.0',
        'LSUIElement': True,          # hides from Dock — menu bar app only
        'NSUserNotificationAlertStyle': 'alert',
    },
)
