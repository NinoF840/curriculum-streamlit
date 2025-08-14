#!/usr/bin/env python3
"""
Script per aggiornare i riferimenti GitHub nel progetto
======================================================

Aggiorna tutti i riferimenti da 'NinoF840' a 'NinoF840'
e completa le informazioni di contatto.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import os
import re
from pathlib import Path

def update_github_references(project_dir):
    """Aggiorna i riferimenti GitHub nel progetto."""
    
    # Definisci le sostituzioni
    replacements = [
        # GitHub username
        ('NinoF840', 'NinoF840'),
        ('github.com/NinoF840', 'github.com/NinoF840'),
        
        # Telefono mascherato
        ('+39 3936789529', '+39 3936789529'),
        ('WhatsApp/Telefono: +39 3936789529', 'WhatsApp/Telefono: +39 3936789529'),
        
        # LinkedIn (se presente)
        ('linkedin.com/in/antoNinoF840', 'linkedin.com/in/antonino-piacenza-nino'),
    ]
    
    # File da escludere (binari, cache, etc.)
    exclude_patterns = [
        '*.pyc', '*.pyo', '*.pyd', '__pycache__',
        '.git', '.vscode', '.idea', 
        '*.exe', '*.dll', '*.so', '*.dylib',
        'node_modules', '.env'
    ]
    
    def should_exclude(file_path):
        """Verifica se un file dovrebbe essere escluso."""
        path_str = str(file_path)
        for pattern in exclude_patterns:
            if pattern.replace('*', '') in path_str:
                return True
        return False
    
    def update_file(file_path):
        """Aggiorna un singolo file."""
        if should_exclude(file_path):
            return False
            
        try:
            # Leggi il contenuto del file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            updated = False
            
            # Applica le sostituzioni
            for old_text, new_text in replacements:
                if old_text in content:
                    content = content.replace(old_text, new_text)
                    updated = True
                    print(f"  ✅ Sostituito '{old_text}' -> '{new_text}'")
            
            # Scrivi il file aggiornato se ci sono stati cambiamenti
            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception as e:
            print(f"  ❌ Errore nell'aggiornare {file_path}: {e}")
            
        return False
    
    # Cerca tutti i file nel progetto
    print("🔍 Ricerca file da aggiornare...")
    
    file_extensions = ['.py', '.md', '.txt', '.json', '.yml', '.yaml', '.html', '.css', '.js']
    files_updated = 0
    total_files = 0
    
    for root, dirs, files in os.walk(project_dir):
        # Esclude directory non necessarie
        dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
        
        for file in files:
            file_path = Path(root) / file
            
            # Verifica estensione file
            if file_path.suffix.lower() in file_extensions:
                total_files += 1
                print(f"\n📁 Controllando: {file_path.relative_to(project_dir)}")
                
                if update_file(file_path):
                    files_updated += 1
                else:
                    print(f"  ⏭️ Nessun aggiornamento necessario")
    
    return files_updated, total_files

def create_github_profile_summary():
    """Crea un riepilogo del profilo GitHub aggiornato."""
    
    profile_summary = """
# 🔗 PROFILO GITHUB AGGIORNATO

## 👤 Informazioni Profilo
- **Username:** NinoF840
- **Profile URL:** https://github.com/NinoF840
- **Repository principale:** curriculum-streamlit

## 📧 Contatti Completi
- **Email Professionale:** ninomedical.ai@gmail.com
- **Email Personale:** nino58150@gmail.com
- **Telefono/WhatsApp:** +39 3936789529
- **LinkedIn:** linkedin.com/in/antonino-piacenza-nino
- **Ubicazione:** Castelvetrano (TP), Italia

## 🚀 Repository Raccomandati
1. **nino-medical-ai** - Progetto principale IA medica
2. **medical-ai-research** - Ricerche e pubblicazioni
3. **streamlit-medical-apps** - Collezione app mediche
4. **ai-healthcare-tools** - Strumenti per settore sanitario

## 📊 GitHub Stats Obiettivi
- ⭐ Repositories pubblici: 10+
- 🍴 Followers: 100+
- 📈 Contributions: Attivo quotidianamente
- 🏷️ Topics: medical-ai, healthcare, streamlit, python, machine-learning

## 🎯 Prossimi Passi
1. Pubblicare curriculum-streamlit come repository pubblico
2. Creare README professionale con showcase progetti
3. Aggiungere badge e statistiche GitHub
4. Configurare GitHub Pages per portfolio online
"""
    
    return profile_summary

if __name__ == "__main__":
    # Directory del progetto
    project_dir = Path("C:\\Users\\nino1\\curriculum-streamlit")
    
    print("🚀 AGGIORNAMENTO RIFERIMENTI GITHUB")
    print("=" * 50)
    print(f"📁 Directory progetto: {project_dir}")
    print(f"🔄 Aggiornamento: 'NinoF840' → 'NinoF840'")
    print("=" * 50)
    
    # Esegui aggiornamento
    files_updated, total_files = update_github_references(project_dir)
    
    print("\n" + "=" * 50)
    print("📊 RISULTATI AGGIORNAMENTO:")
    print(f"├─ File controllati: {total_files}")
    print(f"├─ File aggiornati: {files_updated}")
    print(f"└─ GitHub username: NinoF840 ✅")
    
    # Crea riepilogo profilo
    profile_summary = create_github_profile_summary()
    
    # Salva riepilogo
    summary_file = project_dir / "GITHUB_PROFILE_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(profile_summary)
    
    print(f"\n📋 Riepilogo salvato in: {summary_file}")
    print("\n🎉 Aggiornamento completato!")
    print("\n🔗 Nuovo profilo GitHub: https://github.com/NinoF840")
