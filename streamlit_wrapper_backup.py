#!/usr/bin/env python3
"""
Wrapper per avviare Nino Medical AI Pro Local
Avvia Streamlit con il file appropriato
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Avvia l'app Streamlit Pro Local."""
    
    # Trova il percorso dello script principale
    if getattr(sys, 'frozen', False):
        # Se siamo in un eseguibile PyInstaller
        app_path = Path(sys._MEIPASS) / "nino_medical_ai_pro_local.py"
    else:
        # Se siamo in sviluppo
        app_path = Path(__file__).parent / "nino_medical_ai_pro_local.py"
    
    # Avvia Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.runOnSave", "false",
        "--logger.level", "error"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Applicazione chiusa dall'utente")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Errore nell'avvio dell'applicazione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
