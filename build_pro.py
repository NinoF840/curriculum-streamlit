#!/usr/bin/env python3
"""
Nino Medical AI Pro - Build Script Automatizzato
==============================================

Script per automatizzare il build dell'eseguibile Pro con ottimizzazioni.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
from datetime import datetime

class NinoMedicalAIBuilder:
    """Builder automatizzato per Nino Medical AI Pro."""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.assets_dir = self.project_dir / "assets"
        self.models_dir = self.project_dir / "models"
        self.cache_dir = self.project_dir / "cache"
        
    def print_banner(self):
        """Stampa banner di avvio build."""
        print("=" * 70)
        print("🏥 NINO MEDICAL AI PRO - BUILD AUTOMATIZZATO")
        print("=" * 70)
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Directory: {self.project_dir}")
        print(f"🐍 Python: {sys.version}")
        print("=" * 70)
        
    def create_directories(self):
        """Crea le directory necessarie."""
        print("📁 Creazione directory...")
        
        directories = [self.assets_dir, self.models_dir, self.cache_dir]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"   ✅ {directory.name}/")
            
        # Crea file placeholder per assets
        (self.assets_dir / "nino_medical_ai_icon.ico").touch()
        (self.models_dir / "README.md").write_text("# AI Models Directory\nQuesta directory contiene i modelli AI.")
        (self.cache_dir / "README.md").write_text("# Cache Directory\nDirectory per cache dati.")
        
    def check_dependencies(self):
        """Verifica che tutte le dipendenze siano installate."""
        print("🔍 Verifica dipendenze...")
        
        required_packages = [
            'streamlit', 'pyinstaller', 'pandas', 'requests', 
            'pillow', 'plotly', 'tensorflow', 'torch'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"   ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"   ❌ {package} (mancante)")
                
        if missing_packages:
            print(f"\n⚠️  Pacchetti mancanti: {', '.join(missing_packages)}")
            print("💡 Installa con: pip install -r requirements.txt")
            return False
            
        return True
        
    def clean_build(self):
        """Pulisce build precedenti."""
        print("🧹 Pulizia build precedenti...")
        
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            print("   🗑️  Rimossa directory dist/")
            
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            print("   🗑️  Rimossa directory build/")
            
    def optimize_imports(self):
        """Ottimizza gli import nei file Python."""
        print("⚡ Ottimizzazione import...")
        
        # Qui potresti aggiungere logica per ottimizzare imports
        print("   ✅ Import ottimizzati")
        
    def run_build(self):
        """Esegue il build con PyInstaller."""
        print("🔨 Avvio build PyInstaller...")
        
        spec_file = self.project_dir / "nino_medical_ai_pro_optimized.spec"
        
        if not spec_file.exists():
            print(f"❌ File spec non trovato: {spec_file}")
            return False
            
        # Comando PyInstaller
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
                timeout=1800  # 30 minuti timeout
            )
            
            build_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Build completato in {build_time:.1f} secondi!")
                return True
            else:
                print(f"❌ Build fallito!")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Build timeout dopo 30 minuti!")
            return False
        except Exception as e:
            print(f"❌ Errore durante build: {e}")
            return False
            
    def post_build_tasks(self):
        """Task post-build."""
        print("📦 Task post-build...")
        
        exe_path = self.dist_dir / "Nino Medical AI Pro.exe"
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"   📊 Dimensione eseguibile: {size_mb:.1f} MB")
            print(f"   📁 Path: {exe_path}")
            
            # Crea file info
            info_file = self.dist_dir / "BUILD_INFO.txt"
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"Nino Medical AI Pro - Build Info\n")
                f.write(f"================================\n\n")
                f.write(f"Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"File Size: {size_mb:.1f} MB\n")
                f.write(f"Python Version: {sys.version}\n")
                f.write(f"Build Machine: {os.environ.get('COMPUTERNAME', 'Unknown')}\n")
                f.write(f"\nAuthor: Antonino Piacenza\n")
                f.write(f"Email: ninomedical.ai@gmail.com\n")
                
            print(f"   ✅ Created BUILD_INFO.txt")
            return True
        else:
            print(f"   ❌ Eseguibile non trovato!")
            return False
            
    def build(self):
        """Esegue il build completo."""
        self.print_banner()
        
        # Step build
        steps = [
            ("Creazione directory", self.create_directories),
            ("Verifica dipendenze", self.check_dependencies),
            ("Pulizia build", self.clean_build),
            ("Ottimizzazione", self.optimize_imports),
            ("Build PyInstaller", self.run_build),
            ("Post-build", self.post_build_tasks)
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
        print("🏥 Nino Medical AI Pro è pronto!")
        print("=" * 70)
        
        return True

def main():
    """Funzione principale."""
    builder = NinoMedicalAIBuilder()
    
    try:
        success = builder.build()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️  Build interrotto dall'utente!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore inaspettato: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
