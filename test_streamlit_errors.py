#!/usr/bin/env python3
"""
Test Approfondito per Errori Streamlit
======================================

Test completo per identificare errori di Streamlit, problemi di keepalive 
e altre possibili issue nell'eseguibile.
"""

import subprocess
import time
import os
import sys
import requests
import threading
from pathlib import Path

class StreamlitErrorTester:
    """Tester completo per errori Streamlit."""
    
    def __init__(self):
        self.exe_path = Path(os.path.expanduser("~")) / "Desktop" / "Nino Medical AI Pro.exe"
        self.process = None
        self.errors_found = []
        self.warnings_found = []
        self.port = None
        
    def test_executable_launch(self):
        """Testa il lancio dell'eseguibile."""
        print("[*] Testing executable launch...")
        
        if not self.exe_path.exists():
            print(f"[!] Executable not found: {self.exe_path}")
            return False
        
        try:
            # Lancia l'eseguibile e cattura output
            self.process = subprocess.Popen(
                [str(self.exe_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            print("[+] Executable launched successfully")
            return True
            
        except Exception as e:
            print(f"[!] Failed to launch executable: {e}")
            return False
    
    def monitor_process_output(self, duration=30):
        """Monitora l'output del processo per errori."""
        print(f"[*] Monitoring process output for {duration} seconds...")
        
        def read_output():
            while self.process and self.process.poll() is None:
                try:
                    # Leggi stderr per errori
                    if self.process.stderr:
                        line = self.process.stderr.readline()
                        if line:
                            line = line.strip()
                            print(f"[STDERR] {line}")
                            
                            # Analizza errori specifici
                            if "error" in line.lower():
                                self.errors_found.append(line)
                            elif "warning" in line.lower():
                                self.warnings_found.append(line)
                            elif "traceback" in line.lower():
                                self.errors_found.append(line)
                            elif "keepalive" in line.lower():
                                print(f"[KEEPALIVE] {line}")
                            elif "metadata" in line.lower():
                                print(f"[METADATA] {line}")
                    
                    # Leggi stdout per info
                    if self.process.stdout:
                        line = self.process.stdout.readline()
                        if line:
                            line = line.strip()
                            print(f"[STDOUT] {line}")
                            
                            # Cerca porta Streamlit
                            if "localhost:" in line:
                                try:
                                    port_start = line.find("localhost:") + 10
                                    port_end = line.find(" ", port_start)
                                    if port_end == -1:
                                        port_end = len(line)
                                    self.port = int(line[port_start:port_end])
                                    print(f"[+] Found Streamlit port: {self.port}")
                                except:
                                    pass
                                    
                except Exception as e:
                    print(f"[!] Error reading output: {e}")
                    break
        
        # Avvia thread di monitoraggio
        monitor_thread = threading.Thread(target=read_output)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Aspetta per il periodo specificato
        time.sleep(duration)
        
        return len(self.errors_found) == 0
    
    def test_streamlit_server(self):
        """Testa se il server Streamlit risponde correttamente."""
        print("[*] Testing Streamlit server response...")
        
        if not self.port:
            # Prova porte comuni
            common_ports = [8501, 8502, 8503, 8504, 8505]
            for port in common_ports:
                try:
                    response = requests.get(f"http://localhost:{port}", timeout=2)
                    if response.status_code == 200:
                        self.port = port
                        print(f"[+] Found Streamlit on port {port}")
                        break
                except:
                    continue
        
        if not self.port:
            print("[!] Could not find Streamlit server port")
            return False
        
        try:
            # Test connessione principale
            response = requests.get(f"http://localhost:{self.port}", timeout=5)
            print(f"[+] Server response: {response.status_code}")
            
            # Test endpoint healthz se esiste
            try:
                health_response = requests.get(f"http://localhost:{self.port}/healthz", timeout=2)
                print(f"[+] Health check: {health_response.status_code}")
            except:
                print("[i] No health endpoint available")
            
            # Test keepalive endpoint se esiste
            try:
                keepalive_response = requests.get(f"http://localhost:{self.port}/_stcore/health", timeout=2)
                print(f"[+] Streamlit core health: {keepalive_response.status_code}")
                return True
            except:
                print("[!] Streamlit core health check failed")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Server connection failed: {e}")
            return False
    
    def test_keepalive_functionality(self):
        """Testa specificamente la funzionalità keepalive."""
        print("[*] Testing keepalive functionality...")
        
        if not self.port:
            print("[!] No port available for keepalive test")
            return False
        
        try:
            # Test multipli richieste per verificare keepalive
            for i in range(5):
                response = requests.get(f"http://localhost:{self.port}", timeout=3)
                print(f"[+] Keepalive test {i+1}/5: {response.status_code}")
                time.sleep(1)
                
            print("[+] Keepalive functionality appears to be working")
            return True
            
        except Exception as e:
            print(f"[!] Keepalive test failed: {e}")
            return False
    
    def analyze_streamlit_logs(self):
        """Analizza i log di Streamlit per problemi."""
        print("[*] Analyzing Streamlit behavior...")
        
        # Verifica se ci sono errori comuni
        common_errors = [
            "no package metadata for streamlit",
            "AttributeError",
            "ImportError",
            "ModuleNotFoundError",
            "ConnectionError",
            "TimeoutError"
        ]
        
        errors_detected = []
        for error in common_errors:
            for found_error in self.errors_found:
                if error.lower() in found_error.lower():
                    errors_detected.append(error)
        
        if errors_detected:
            print(f"[!] Detected common errors: {errors_detected}")
            return False
        else:
            print("[+] No common Streamlit errors detected")
            return True
    
    def cleanup(self):
        """Pulisce il processo di test."""
        print("[*] Cleaning up test process...")
        
        if self.process:
            try:
                self.process.terminate()
                time.sleep(2)
                if self.process.poll() is None:
                    self.process.kill()
                print("[+] Process terminated successfully")
            except Exception as e:
                print(f"[!] Error terminating process: {e}")
    
    def run_comprehensive_test(self):
        """Esegue test completo."""
        print("=" * 60)
        print("STREAMLIT ERROR COMPREHENSIVE TEST")
        print("=" * 60)
        
        test_results = {
            "executable_launch": False,
            "output_monitoring": False,
            "server_response": False,
            "keepalive": False,
            "error_analysis": False
        }
        
        try:
            # Test 1: Lancio eseguibile
            test_results["executable_launch"] = self.test_executable_launch()
            
            if test_results["executable_launch"]:
                # Test 2: Monitora output per errori
                test_results["output_monitoring"] = self.monitor_process_output(20)
                
                # Test 3: Test server Streamlit
                test_results["server_response"] = self.test_streamlit_server()
                
                # Test 4: Test keepalive
                if test_results["server_response"]:
                    test_results["keepalive"] = self.test_keepalive_functionality()
                
                # Test 5: Analisi errori
                test_results["error_analysis"] = self.analyze_streamlit_logs()
            
        finally:
            self.cleanup()
        
        # Report finale
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        
        for test_name, result in test_results.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        # Errori trovati
        if self.errors_found:
            print(f"\n[!] ERRORS FOUND ({len(self.errors_found)}):")
            for error in self.errors_found:
                print(f"    - {error}")
        
        # Warning trovati
        if self.warnings_found:
            print(f"\n[!] WARNINGS FOUND ({len(self.warnings_found)}):")
            for warning in self.warnings_found:
                print(f"    - {warning}")
        
        overall_success = all(test_results.values())
        print(f"\n{'[SUCCESS]' if overall_success else '[FAILED]'} Overall Test Result")
        
        # Raccomandazioni
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)
        
        if not test_results["keepalive"]:
            print("- Keepalive issues detected. Consider implementing custom keepalive logic.")
        
        if self.errors_found:
            print("- Errors detected in Streamlit execution. Review error logs above.")
        
        if not test_results["server_response"]:
            print("- Server response issues. Check Streamlit configuration.")
        
        if overall_success:
            print("- All tests passed! Application appears to be working correctly.")
        
        return overall_success

def main():
    """Funzione principale."""
    tester = StreamlitErrorTester()
    success = tester.run_comprehensive_test()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
