import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['key_frame_label.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/huang/codes/nevian_lab/video_processing/logo.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='key_frame_label',
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
