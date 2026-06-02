# -*- mode: python ; coding: utf-8 -*-
import sys

if sys.platform == 'darwin':
    icon_file = 'icon.icns'
elif sys.platform == 'win32':
    icon_file = 'icon.ico'
else:
    icon_file = None  # Linux: Icon kommt später ins AppImage

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('styles/default.qss', 'styles'),
        ('assets', 'assets'),
    ],
    hiddenimports=[],
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
    name='CoBalance',
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
)

if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='MeinProgramm.app',
        icon=icon_file,
        bundle_identifier='com.deinname.meinprogramm',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
        },
    )
