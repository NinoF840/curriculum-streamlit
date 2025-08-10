#!/usr/bin/env python3
"""
Test rapido per verificare che l'eseguibile funzioni senza errori metadata
"""

import subprocess
import time
import os
from pathlib import Path

def test_exe():
    """Testa l'eseguibile."""
    exe_path = Path(os.path.expanduser("~")) / "Desktop" / "Nino Medical AI Pro.exe"
    
    if not exe_path.exists():
        print("❌ Eseguibile non trovato!")
        return False
    
    print(f"🧪 Testing: {exe_path}")
    print("⏳ Avviando eseguibile...")
    
    try:
        # Avvia l'eseguibile in background
        process = subprocess.Popen([str(exe_path)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Aspetta qualche secondo per vedere se si avvia correttamente
        time.sleep(10)
        
        # Controlla se il processo è ancora in esecuzione
        if process.poll() is None:
            print("✅ Eseguibile avviato correttamente!")
            print("🌐 Dovrebbe aprirsi nel browser a breve...")
            
            # Termina il processo di test
            process.terminate()
            time.sleep(2)
            if process.poll() is None:
                process.kill()
            
            return True
        else:
            # Il processo è terminato, controlla l'output
            stdout, stderr = process.communicate()
            print(f"❌ Eseguibile terminato prematuramente!")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Errore durante test: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🏥 NINO MEDICAL AI PRO - TEST")
    print("=" * 50)
    
    success = test_exe()
    
    if success:
        print("✅ TEST PASSED - Nessun errore metadata!")
    else:
        print("❌ TEST FAILED - Verifica configurazione")
    
    print("=" * 50)
