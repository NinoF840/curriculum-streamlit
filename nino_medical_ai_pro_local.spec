# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['streamlit_wrapper_local.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('nino_medical_ai_pro_local.py', '.'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'pandas',
        'numpy',
        'plotly',
        'plotly.express',
        'plotly.graph_objects',
        'PIL',
        'PIL.Image',
        'click',
        'altair',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Nino Medical AI Pro Local',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    distpath='C:/Users/nino1/Desktop/Nino Medical AI Pro Versions',
)
