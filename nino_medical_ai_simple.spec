# -*- mode: python ; coding: utf-8 -*-
"""
Simple optimized PyInstaller spec file for Nino Medical AI
Focuses on essential optimizations without aggressive exclusions
"""

import sys
from PyInstaller.utils.hooks import collect_data_files

# Minimal streamlit data collection
try:
    streamlit_datas = collect_data_files('streamlit')
except:
    streamlit_datas = []

a = Analysis(
    ['nino_medical_ai_app.py'],
    pathex=[],
    binaries=[],
    datas=streamlit_datas + [('requirements.txt', '.')],
    hiddenimports=[
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.web.server.server',
        'streamlit.runtime.state.session_state',
        'PIL.Image',
        'PIL._imaging',
        'packaging.version',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Only exclude clearly unused major libraries
        'numpy',
        'scipy', 
        'pandas',
        'matplotlib',
        'sklearn',
        'tensorflow',
        'torch',
        'PyQt5',
        'PyQt6',
        'PySide2', 
        'PySide6',
        'wx',
        'jupyter',
        'ipython',
        'notebook',
        'pytest',
        'sphinx',
    ],
    noarchive=False,
    optimize=1,  # Moderate optimization to avoid issues
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Nino Medical AI Simple',
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
    version=None,
    uac_admin=False,
    uac_uiaccess=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)
