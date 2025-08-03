# -*- mode: python ; coding: utf-8 -*-
"""
Optimized PyInstaller spec file for Nino Medical AI
App dependencies: streamlit, PIL only
Optimized for minimal size and fast startup
"""

import sys
from PyInstaller.utils.hooks import collect_data_files

# Collect only essential Streamlit data files (not all)
try:
    streamlit_datas = collect_data_files('streamlit', include_py_files=False)
    # Filter to only essential files to reduce size
    streamlit_datas = [(src, dest) for src, dest in streamlit_datas 
                      if 'static' in src or 'vendor' in src]
except:
    # Fallback if collection fails
    streamlit_datas = []

a = Analysis(
    ['nino_medical_ai_app.py'],
    pathex=[],
    binaries=[],
    datas=streamlit_datas + [('requirements.txt', '.')],
    hiddenimports=[
        # Essential Streamlit imports only
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state.session_state',
        'streamlit.web.server.server',
        'streamlit.runtime.caching.cache_data_api',
        'streamlit.elements.utils',
        'streamlit.delta_generator',
        # PIL essentials
        'PIL._imaging',
        'PIL.Image',
        'PIL.ImageFile',
        # Core dependencies
        'packaging.version',
        'packaging.specifiers',
        'email.mime.text',
        'email.mime.multipart',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Major exclusions for size optimization
        # GUI frameworks
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx', 'gtk', 'tkinter',
        
        # Unix/Linux specific
        'posix', 'pwd', 'grp', 'fcntl', 'termios', 'readline', '_curses',
        
        # Scientific computing (not used in this app)
        'numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn', 'plotly',
        'sklearn', 'tensorflow', 'torch', 'keras', 'numba', 'sympy',
        'astropy', 'dask', 'xarray', 'statsmodels', 'patsy',
        
        # Development and testing tools
        'pytest', 'unittest', 'doctest', 'pdb', 'pstats', 'profile',
        'cProfile', 'trace', 'tabnanny', 'pydoc', 'py_compile',
        'sphinx', 'black', 'coverage', 'mypy', 'flake8', 'pylint',
        
        # Alternative web frameworks
        'flask', 'django', 'fastapi', 'tornado', 'aiohttp', 'uvicorn',
        'gunicorn', 'werkzeug', 'jinja2.ext',
        
        # Database drivers
        'psycopg2', 'pymysql', 'sqlite3', 'sqlalchemy.dialects',
        'mongodb', 'redis', 'cassandra',
        
        # Cloud services
        'boto3', 'azure', 'google.cloud', 'kubernetes',
        
        # Jupyter and notebook environments
        'jupyter', 'ipython', 'notebook', 'jupyterlab', 'ipykernel',
        'ipywidgets', 'nbconvert', 'nbformat',
        
        # Alternative data formats
        'openpyxl', 'xlrd', 'xlsxwriter', 'h5py', 'pytables',
        'pyarrow', 'parquet', 'avro',
        
        # Image processing (beyond PIL basics)
        'opencv', 'skimage', 'imageio', 'tifffile',
        
        # Networking (not needed for standalone app)
        'requests.packages.urllib3.contrib', 'urllib3.contrib',
        'cryptography.hazmat', 'paramiko', 'fabric',
        
        # Multiprocessing (not used)
        'multiprocessing.pool', 'multiprocessing.managers',
        'concurrent.futures.process',
        
        # Compression (beyond basic)
        'lzma', 'bz2', 'zstandard', 'lz4',
        
        # XML/HTML parsing (not used)
        'lxml', 'html5lib', 'beautifulsoup4', 'bleach.linkifier',
        
        # Audio/Video processing
        'pyaudio', 'opencv-python', 'ffmpeg',
        
        # Alternative serialization
        'dill', 'cloudpickle', 'joblib.externals',
        
        # Locale and i18n (not needed for English app)
        'babel.localedata', 'locale',
        
        # Unused standard library modules
        'distutils', 'ensurepip', 'venv', 'turtle', 'tkinter',
        'audioop', 'sunau', 'wave', 'chunk', 'colorsys',
        'imghdr', 'sndhdr', 'ossaudiodev', 'spwd', 'nis',
        'crypt', 'grp', 'termios', 'tty', 'pty',
    ],
    noarchive=False,
    optimize=2,  # Maximum optimization
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Nino Medical AI Pro',
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
