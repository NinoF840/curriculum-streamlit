#!/usr/bin/env python3
import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    # Ottieni il percorso dell'eseguibile
    if getattr(sys, 'frozen', False):
        # Se siamo in un eseguibile PyInstaller
        app_dir = Path(sys._MEIPASS)
        script_path = app_dir / "nino_medical_ai_app.py"
    else:
        # Se siamo in sviluppo
        script_path = Path(__file__).parent / "nino_medical_ai_app.py"
    
    try:
        # Avvia Streamlit
        print("🏥 Avviando Nino Medical AI Pro...")
        print("🚀 Apertura in corso del browser...")
        
        # Configura le variabili d'ambiente per Streamlit
        env = os.environ.copy()
        env['STREAMLIT_SERVER_HEADLESS'] = 'true'
        env['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
        env['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
        
        # Avvia il processo Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", str(script_path),
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        process = subprocess.Popen(cmd, env=env)
        
        # Aspetta un po' e poi apri il browser
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        
        print("✅ Applicazione avviata su http://localhost:8501")
        print("📝 Premi Ctrl+C per fermare l'applicazione")
        
        # Attendi che il processo termini
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Applicazione fermata dall'utente")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")
        input("Premi Enter per chiudere...")

if __name__ == "__main__":
    main()
