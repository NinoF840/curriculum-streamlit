#!/usr/bin/env python3
"""
Hook PyInstaller per Streamlit
Risolve problemi di importazione con Streamlit in eseguibili PyInstaller
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect Streamlit data files
datas = collect_data_files('streamlit')

# Hidden imports for Streamlit
hiddenimports = [
    'streamlit.web.cli',
    'streamlit.runtime',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.state',
    'streamlit.components.v1',
    'streamlit.delta_generator',
    'altair',
    'plotly',
    'plotly.express',
    'plotly.graph_objects',
    'watchdog',
    'watchdog.observers',
    'watchdog.events',
    'click',
    'toml',
    'validators',
    'tornado',
    'tornado.web',
    'tornado.websocket',
]

# Collect all submodules
hiddenimports += collect_submodules('streamlit')
hiddenimports += collect_submodules('altair')
hiddenimports += collect_submodules('plotly')
