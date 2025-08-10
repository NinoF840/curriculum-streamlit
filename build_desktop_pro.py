#!/usr/bin/env python3
"""
Build Script per Nino Medical AI Pro Desktop
============================================

Script per creare l'eseguibile desktop senza Streamlit.

Author: Antonino Piacenza
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
from datetime import datetime

class DesktopProBuilder:
    """Builder per la versione desktop."""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.desktop_path = Path(os.path.expanduser("~")) / "Desktop"
        self.build_dir = self.project_dir / "build"
        
    def print_banner(self):
        """Stampa banner di avvio."""
        print("=" * 70)
        print("🏥 NINO MEDICAL AI PRO - BUILD DESKTOP")
        print("=" * 70)
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Progetto: {self.project_dir}")
        print(f"💾 Destinazione: {self.desktop_path}")
        print(f"🐍 Python: {sys.version}")
        print("=" * 70)
        
    def check_dependencies(self):
        """Verifica dipendenze necessarie."""
        print("🔍 Verifica dipendenze...")
        
        required = ['tkinter', 'pandas', 'numpy', 'PIL', 'matplotlib', 'pyinstaller']
        missing = []
        
        for package in required:
            try:
                if package == 'PIL':
                    __import__('PIL')
                elif package == 'pyinstaller':
                    __import__(package)
                else:
                    __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                missing.append(package)
                print(f"   ❌ {package}")
                
        if missing:
            print(f"\n⚠️ Pacchetti mancanti: {', '.join(missing)}")
            if 'tkinter' in missing:
                print("💡 tkinter dovrebbe essere incluso con Python")
            else:
                print(f"💡 Installa con: pip install {' '.join(missing)}")
            return False
        return True
        
    def clean_build(self):
        """Pulisce build precedenti."""
        print("🧹 Pulizia build precedenti...")
        
        try:
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                print("   🗑️ Rimossa directory build/")
            else:
                print("   ℹ️ Directory build/ non esistente")
                
            # Rimuovi eseguibile esistente
            exe_path = self.desktop_path / "Nino Medical AI Pro.exe"
            if exe_path.exists():
                exe_path.unlink()
                print("   🗑️ Rimosso eseguibile precedente")
                
            return True
        except Exception as e:
            print(f"   ⚠️ Errore pulizia: {e}")
            return True  # Non bloccare per questo
            
    def test_app(self):
        """Testa l'applicazione prima del build."""
        print("🧪 Test applicazione...")
        
        script_path = self.project_dir / "nino_medical_ai_desktop_pro.py"
        
        if not script_path.exists():
            print(f"   ❌ File principale non trovato: {script_path}")
            return False
            
        try:
            # Test importazione moduli
            import tkinter
            import pandas
            import numpy
            import matplotlib
            from PIL import Image
            print("   ✅ Tutti i moduli importati correttamente")
            return True
        except ImportError as e:
            print(f"   ❌ Errore importazione: {e}")
            return False
            
    def run_build(self):
        """Esegue il build con PyInstaller."""
        print("🔨 Avvio build PyInstaller...")
        
        spec_file = self.project_dir / "nino_medical_ai_desktop_pro.spec"
        
        if not spec_file.exists():
            print(f"❌ File spec non trovato: {spec_file}")
            return False
            
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm", 
            str(spec_file)
        ]
        
        print(f"📝 Comando: {' '.join(cmd)}")
        
        try:
            start_time = time.time()
            
            result = subprocess.run(
                cmd,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=900  # 15 minuti timeout
            )
            
            build_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Build completato in {build_time:.1f} secondi!")
                return True
            else:
                print(f"❌ Build fallito!")
                print("STDOUT:", result.stdout[-1000:])  # Ultimi 1000 caratteri
                print("STDERR:", result.stderr[-1000:])
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Build timeout dopo 15 minuti!")
            return False
        except Exception as e:
            print(f"❌ Errore durante build: {e}")
            return False
            
    def post_build_check(self):
        """Controlla il risultato del build."""
        print("📦 Controllo risultato...")
        
        exe_path = self.desktop_path / "Nino Medical AI Pro.exe"
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Eseguibile creato: {size_mb:.1f} MB")
            print(f"   📁 Path: {exe_path}")
            
            # Crea shortcut info
            info_path = exe_path.with_suffix('.txt')
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"Nino Medical AI Pro - Desktop\\n")
                f.write(f"================================\\n\\n")
                f.write(f"Build: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write(f"Dimensioni: {size_mb:.1f} MB\\n")
                f.write(f"Versione: Desktop Standalone (No Streamlit)\\n")
                f.write(f"\\nAutore: Antonino Piacenza\\n")
                f.write(f"Piattaforma: Windows Desktop Application\\n")
                f.write(f"\\nFunzionalità:\\n")
                f.write(f"• Dashboard con statistiche e grafici\\n")
                f.write(f"• Analisi immagini mediche (simulata)\\n")
                f.write(f"• Profilo ricercatore\\n")
                f.write(f"• Form contatti\\n")
                f.write(f"\\nNOTA: Versione dimostrativa a scopo illustrativo\\n")
                
            print(f"   📄 Creato file info")
            return True
        else:
            print(f"   ❌ Eseguibile non trovato!")
            return False
            
    def build(self):
        """Esegue il build completo."""
        self.print_banner()
        
        steps = [
            ("Verifica dipendenze", self.check_dependencies),
            ("Test applicazione", self.test_app),
            ("Pulizia build", self.clean_build),
            ("Build PyInstaller", self.run_build),
            ("Controllo risultato", self.post_build_check)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🚀 {step_name}...")
            
            try:
                if not step_func():
                    print(f"❌ Fallito: {step_name}")
                    return False
                    
            except Exception as e:
                print(f"❌ Errore in {step_name}: {e}")
                return False
                
        print("\n" + "=" * 70)
        print("🎉 BUILD COMPLETATO CON SUCCESSO!")
        print("🏥 Nino Medical AI Pro (Desktop) salvato sul Desktop!")
        print("🖥️ Versione standalone senza dipendenze Streamlit")
        print("=" * 70)
        
        return True

def main():
    """Funzione principale."""
    builder = DesktopProBuilder()
    
    try:
        success = builder.build()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Build interrotto dall'utente!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore inaspettato: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
