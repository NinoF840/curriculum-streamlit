"""
PyInstaller hook per Streamlit - Risolve problemi di metadata
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Colleziona tutti i dati necessari per Streamlit
datas = collect_data_files('streamlit')

# Colleziona tutti i submoduli di Streamlit
hiddenimports = collect_submodules('streamlit')

# Aggiungi moduli specifici che potrebbero essere mancanti
hiddenimports += [
    'streamlit.web.cli',
    'streamlit.web.bootstrap', 
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.state',
    'streamlit.components.v1',
    'altair',
    'pyarrow',
    'tornado',
    'tornado.web',
    'tornado.websocket',
    'tornado.ioloop'
]
