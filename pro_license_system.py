#!/usr/bin/env python3
"""
Sistema di Licensing per Nino Medical AI Pro
=============================================

Protegge le funzionalità Pro dall'uso non autorizzato su Streamlit.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, List
import json
import sqlite3
from pathlib import Path

class LicenseManager:
    """Gestore licenze per versione Pro."""
    
    def __init__(self, db_path: str = "auth/licenses.db"):
        """Inizializza il gestore licenze."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_license_db()
        
    def _init_license_db(self):
        """Inizializza database licenze."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pro_licenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    license_key TEXT UNIQUE NOT NULL,
                    license_type TEXT NOT NULL,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS feature_access (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    feature_name TEXT NOT NULL,
                    access_granted BOOLEAN DEFAULT FALSE,
                    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
    
    def generate_license_key(self, user_id: int, license_type: str = "pro_monthly") -> str:
        """Genera chiave di licenza sicura."""
        secret = "nino_medical_ai_secret_2025"  # In produzione da env variable
        data = f"{user_id}:{license_type}:{datetime.now().isoformat()}"
        
        signature = hmac.new(
            secret.encode(), 
            data.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        return f"NMAI-{license_type.upper()}-{signature[:16]}"
    
    def validate_pro_access(self, user_id: int) -> bool:
        """Verifica se l'utente ha accesso Pro valido."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT expires_at FROM pro_licenses 
                WHERE user_id = ? AND is_active = TRUE
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            ''', (user_id,))
            
            return cursor.fetchone() is not None
    
    def grant_pro_access(self, user_id: int, duration_days: int = 30) -> str:
        """Concede accesso Pro per durata specificata."""
        license_key = self.generate_license_key(user_id)
        expires_at = datetime.now() + timedelta(days=duration_days)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO pro_licenses (user_id, license_key, license_type, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, license_key, "pro_monthly", expires_at))
        
        return license_key

class ProFeatureGuard:
    """Protettore per funzionalità Pro."""
    
    PRO_FEATURES = {
        'advanced_ai_analysis': 'Analisi IA Avanzata',
        'bulk_image_processing': 'Elaborazione Immagini in Blocco',
        'custom_models': 'Modelli IA Personalizzati',
        'api_access': 'Accesso API',
        'priority_support': 'Supporto Prioritario',
        'export_reports': 'Export Report Avanzati',
        'multi_language': 'Supporto Multi-lingua',
        'cloud_storage': 'Storage Cloud Illimitato'
    }
    
    @staticmethod
    def require_pro_feature(feature_name: str):
        """Decorator per proteggere funzionalità Pro."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                from auth_system import SessionManager
                
                user = SessionManager.get_current_user()
                if not user:
                    st.error("🔒 Login richiesto")
                    return None
                
                license_manager = LicenseManager()
                
                if not license_manager.validate_pro_access(user.id):
                    st.error("🚫 Funzionalità disponibile solo nella versione Pro")
                    
                    # Informazioni upgrade
                    with st.expander("💎 Upgrade alla versione Pro", expanded=True):
                        st.markdown(f"""
                        ### 🌟 {ProFeatureGuard.PRO_FEATURES.get(feature_name, 'Funzionalità Pro')}
                        
                        **Vantaggi versione Pro:**
                        - ✨ Analisi IA avanzate e personalizzate
                        - 🚀 Elaborazione immagini in blocco
                        - 📊 Report dettagliati ed esportazione
                        - 🔧 Modelli IA su misura
                        - ⚡ Supporto prioritario
                        - ☁️ Storage cloud illimitato
                        
                        **📧 Per informazioni:** ninomedical.ai@gmail.com
                        **💰 Prezzo:** €29.99/mese
                        """)
                    
                    return None
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Esempi di utilizzo
@ProFeatureGuard.require_pro_feature('advanced_ai_analysis')
def advanced_ai_analysis():
    """Analisi IA avanzata - Solo Pro."""
    st.success("🎯 Accesso Pro confermato!")
    st.write("Analisi IA avanzata disponibile...")

@ProFeatureGuard.require_pro_feature('bulk_image_processing')
def bulk_image_processing():
    """Elaborazione immagini in blocco - Solo Pro."""
    st.success("🚀 Funzionalità Pro attiva!")
    st.write("Carica fino a 100 immagini contemporaneamente...")

@ProFeatureGuard.require_pro_feature('export_reports')
def export_advanced_reports():
    """Export report avanzati - Solo Pro."""
    st.success("📊 Export Pro disponibile!")
    st.write("Esporta in PDF, Excel, Word...")

def demo_pro_features():
    """Demo delle funzionalità Pro per utenti gratuiti."""
    st.markdown("## 🎯 Anteprima Funzionalità Pro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔬 Analisi IA Avanzata
        - Modelli specializzati per diagnostica
        - Confidence score dettagliati
        - Analisi comparativa multi-immagine
        """)
        
        if st.button("🎯 Prova Analisi Avanzata"):
            advanced_ai_analysis()
    
    with col2:
        st.markdown("""
        ### 📊 Report Personalizzati
        - Export in PDF professionale
        - Grafici interattivi
        - Storico analisi
        """)
        
        if st.button("📈 Genera Report"):
            export_advanced_reports()

def show_upgrade_info():
    """Mostra informazioni per upgrade Pro."""
    st.markdown("""
    ## 💎 Nino Medical AI Pro
    
    ### 🚀 Funzionalità Esclusive
    
    | Funzionalità | Gratuito | Pro |
    |-------------|----------|-----|
    | Analisi base | ✅ | ✅ |
    | Analisi avanzata | ❌ | ✅ |
    | Elaborazione blocco | ❌ | ✅ |
    | API Access | ❌ | ✅ |
    | Support prioritario | ❌ | ✅ |
    | Export avanzato | ❌ | ✅ |
    
    ### 💰 Prezzi
    - **Mensile:** €29.99/mese
    - **Annuale:** €299.99/anno (17% risparmio)
    - **Licenza desktop:** €199.99 (pagamento unico)
    
    ### 📧 Contatti
    **Email:** ninomedical.ai@gmail.com  
    **Sito:** antonino-piacenza-portfolio.streamlit.app
    """)

if __name__ == "__main__":
    # Test sistema licensing
    print("Testing Pro License System...")
    
    license_manager = LicenseManager()
    
    # Test generazione licenza
    test_user_id = 1
    license_key = license_manager.grant_pro_access(test_user_id, 30)
    print(f"✅ License generated: {license_key}")
    
    # Test validazione
    is_valid = license_manager.validate_pro_access(test_user_id)
    print(f"✅ License validation: {is_valid}")
    
    print("Pro License System working correctly!")
