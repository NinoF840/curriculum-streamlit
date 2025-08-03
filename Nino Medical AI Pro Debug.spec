# -*- mode: python ; coding: utf-8 -*-
"""
Optimized Debug version for Nino Medical AI Pro
Includes console output for debugging
"""

a = Analysis(
    ['nino_medical_ai_app.py'],
    pathex=[],
    binaries=[],
    datas=[('requirements.txt', '.')],
    hiddenimports=[
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state.session_state',
        'streamlit.web.server.server',
        'PIL.Image',
        'packaging.version',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Still exclude major unused libraries for size
        'numpy', 'scipy', 'pandas', 'matplotlib',
        'sklearn', 'tensorflow', 'torch',
        'PyQt5', 'PyQt6', 'wx', 'gtk',
        'jupyter', 'ipython', 'notebook',
        'pytest', 'sphinx', 'black',
    ],
    noarchive=False,
    optimize=1,  # Some optimization but keep debug info
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Nino Medical AI Pro Debug',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
