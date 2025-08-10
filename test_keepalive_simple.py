#!/usr/bin/env python3
"""
Test Semplice Keepalive
=======================

Test rapido e semplice per verificare se il keepalive funziona.
"""

import subprocess
import time
import os
import requests
from pathlib import Path

def test_keepalive():
    """Test semplice del keepalive."""
    print("[*] Test Keepalive Semplice...")
    
    exe_path = Path(os.path.expanduser("~")) / "Desktop" / "Nino Medical AI Pro.exe"
    
    if not exe_path.exists():
        print("[!] Eseguibile non trovato!")
        return False
    
    print("[*] Avvio eseguibile...")
    process = None
    
    try:
        # Avvia eseguibile
        process = subprocess.Popen([str(exe_path)], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        print("[*] Attesa avvio server (60 secondi)...")
        time.sleep(60)  # Attesa più lunga per Streamlit
        
        # Test connessione su porte comuni
        ports_to_test = [8501, 8502, 8503, 8504, 8505]
        server_port = None
        
        for port in ports_to_test:
            try:
                response = requests.get(f"http://localhost:{port}", timeout=5)
                if response.status_code == 200:
                    server_port = port
                    print(f"[+] Server trovato su porta {port}")
                    break
            except:
                continue
        
        if not server_port:
            print("[!] Server non trovato su porte comuni")
            return False
        
        # Test keepalive - multiple richieste
        print("[*] Test keepalive con multiple richieste...")
        keepalive_success = 0
        
        for i in range(5):
            try:
                response = requests.get(f"http://localhost:{server_port}", timeout=3)
                if response.status_code == 200:
                    keepalive_success += 1
                    print(f"[+] Richiesta {i+1}/5 - OK")
                else:
                    print(f"[!] Richiesta {i+1}/5 - FAIL ({response.status_code})")
                time.sleep(2)
            except Exception as e:
                print(f"[!] Richiesta {i+1}/5 - ERROR: {e}")
        
        success_rate = (keepalive_success / 5) * 100
        print(f"[+] Keepalive success rate: {success_rate}%")
        
        if success_rate >= 80:
            print("[+] KEEPALIVE OK - Funziona correttamente!")
            return True
        else:
            print("[!] KEEPALIVE ISSUES - Problemi di connessione")
            return False
            
    except Exception as e:
        print(f"[!] Errore durante test: {e}")
        return False
        
    finally:
        if process:
            print("[*] Terminazione processo...")
            process.terminate()
            time.sleep(2)
            if process.poll() is None:
                process.kill()

def main():
    """Funzione principale."""
    print("=" * 50)
    print("🏥 NINO MEDICAL AI - KEEPALIVE TEST")
    print("=" * 50)
    
    success = test_keepalive()
    
    if success:
        print("\n✅ RISULTATO: Keepalive funziona correttamente!")
    else:
        print("\n❌ RISULTATO: Problemi con keepalive rilevati")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
