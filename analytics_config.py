#!/usr/bin/env python3
"""
Google Analytics Configuration for Nino Medical AI
==================================================

File di configurazione per l'integrazione Google Analytics.
Contiene impostazioni, ID di tracking e configurazioni personalizzate.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import os
from typing import Dict, Any

class AnalyticsSettings:
    """Configurazione principale per Google Analytics."""
    
    # ========================================
    # CONFIGURAZIONE GOOGLE ANALYTICS
    # ========================================
    
    # GA4 Measurement ID - SOSTITUISCI CON IL TUO
    # Puoi trovarlo in Google Analytics 4 > Admin > Data Streams
    GA4_MEASUREMENT_ID = os.getenv('GA4_MEASUREMENT_ID', 'G-XXXXXXXXXX')
    
    # API Secret per Measurement Protocol (opzionale ma raccomandato)
    # Puoi generarlo in GA4 > Admin > Data Streams > Measurement Protocol API secrets
    GA4_API_SECRET = os.getenv('GA4_API_SECRET', None)
    
    # ========================================
    # CONFIGURAZIONI AVANZATE
    # ========================================
    
    # Abilita/disabilita tracking
    ANALYTICS_ENABLED = os.getenv('ANALYTICS_ENABLED', 'true').lower() == 'true'
    
    # Debug mode (usa endpoint di debug GA4)
    DEBUG_MODE = os.getenv('ANALYTICS_DEBUG', 'false').lower() == 'true'
    
    # Timeout per richieste HTTP (in secondi)
    REQUEST_TIMEOUT = int(os.getenv('ANALYTICS_TIMEOUT', '5'))
    
    # Anonimizza IP (compliance GDPR)
    ANONYMIZE_IP = True
    
    # Disabilita Google Signals (compliance privacy)
    DISABLE_GOOGLE_SIGNALS = True
    
    # ========================================
    # EVENTI PERSONALIZZATI
    # ========================================
    
    CUSTOM_EVENTS = {
        # Eventi base
        'PAGE_VIEW': 'page_view',
        'SESSION_START': 'session_start',
        'USER_ENGAGEMENT': 'user_engagement',
        
        # Eventi utente
        'USER_LOGIN': 'login',
        'USER_SIGNUP': 'sign_up',
        'USER_LOGOUT': 'logout',
        'PROFILE_UPDATE': 'profile_update',
        
        # Eventi contenuti
        'COMMENT_SUBMIT': 'comment_submit',
        'FEEDBACK_SUBMIT': 'feedback_submit',
        'RATING_SUBMIT': 'rating_submit',
        'CONTACT_FORM': 'contact_form',
        
        # Eventi business
        'PURCHASE': 'purchase',
        'UPGRADE_VIEW': 'upgrade_view',
        'PRICING_VIEW': 'pricing_view',
        'TRIAL_START': 'trial_start',
        
        # Eventi app specifica
        'PRO_FEATURE_USAGE': 'pro_feature_usage',
        'DATABASE_SEARCH': 'database_search',
        'AI_ANALYSIS': 'ai_analysis',
        'MEDICAL_EXPORT': 'medical_export',
        'PREDICTION_RUN': 'prediction_run',
        'CLINICAL_TRIAL_SEARCH': 'clinical_trial_search'
    }
    
    # ========================================
    # PARAMETRI PERSONALIZZATI
    # ========================================
    
    CUSTOM_PARAMETERS = {
        # User properties
        'user_tier': 'custom_parameter_1',      # free, pro
        'user_role': 'custom_parameter_2',      # guest, user, admin
        'subscription_status': 'custom_parameter_3',  # active, expired, trial
        
        # Content properties  
        'feature_type': 'custom_parameter_4',   # analytics, prediction, search
        'database_type': 'custom_parameter_5',  # pubmed, fda, who, etc.
        'analysis_type': 'custom_parameter_6',  # cardio, diabetes, oncology
        
        # Business properties
        'conversion_source': 'custom_parameter_7',  # organic, referral, direct
        'upgrade_trigger': 'custom_parameter_8',    # feature_limit, demo_end, cta
    }
    
    # ========================================
    # CONFIGURAZIONI E-COMMERCE
    # ========================================
    
    ECOMMERCE_CONFIG = {
        'currency': 'EUR',
        'items': {
            'nino_medical_ai_pro': {
                'item_id': 'nino_medical_ai_pro',
                'item_name': 'Nino Medical AI Pro License',
                'item_category': 'software_license',
                'item_category2': 'medical_ai',
                'item_brand': 'Nino Medical AI',
                'price': 29.99  # Prezzo base
            },
            'nino_medical_ai_enterprise': {
                'item_id': 'nino_medical_ai_enterprise', 
                'item_name': 'Nino Medical AI Enterprise License',
                'item_category': 'software_license',
                'item_category2': 'medical_ai',
                'item_brand': 'Nino Medical AI',
                'price': 99.99
            }
        }
    }
    
    # ========================================
    # AUDIENCE E CONVERSIONI
    # ========================================
    
    # Obiettivi di conversione
    CONVERSION_GOALS = {
        'pro_signup': {
            'event_name': 'purchase',
            'value_threshold': 1.0
        },
        'feature_engagement': {
            'event_name': 'pro_feature_usage',
            'frequency_threshold': 3
        },
        'user_retention': {
            'event_name': 'session_start',
            'time_window': '7_days'
        }
    }
    
    # Audience personalizzate
    CUSTOM_AUDIENCES = {
        'engaged_users': {
            'description': 'Users with high engagement',
            'criteria': 'session_duration > 5min OR page_views > 10'
        },
        'potential_pro_users': {
            'description': 'Users likely to upgrade',
            'criteria': 'pro_feature_usage >= 2 AND upgrade_view >= 1'
        },
        'medical_professionals': {
            'description': 'Healthcare professionals',
            'criteria': 'database_search contains medical terms'
        }
    }

class TrackingConfiguration:
    """Configurazioni specifiche per tracking eventi."""
    
    # ========================================
    # CONFIGURAZIONI PAGINE
    # ========================================
    
    PAGE_TRACKING = {
        'home': {
            'track_scroll': True,
            'track_time_on_page': True,
            'track_interactions': ['button_click', 'form_submit']
        },
        'dashboard': {
            'track_feature_usage': True,
            'track_pro_interactions': True,
            'track_exports': True
        },
        'databases': {
            'track_searches': True,
            'track_results_interaction': True,
            'track_export_actions': True
        },
        'predictive': {
            'track_model_usage': True,
            'track_input_parameters': False,  # Privacy
            'track_results_confidence': True
        },
        'clinical_trials': {
            'track_search_filters': True,
            'track_trial_interactions': True,
            'track_matching_requests': True
        }
    }
    
    # ========================================
    # PRIVACY E COMPLIANCE
    # ========================================
    
    PRIVACY_SETTINGS = {
        # GDPR compliance
        'anonymize_ip': True,
        'disable_advertising_features': True,
        'respect_do_not_track': True,
        
        # Data retention
        'data_retention_months': 14,  # GA4 default
        
        # Consent management
        'require_consent': True,
        'consent_categories': ['analytics', 'functionality'],
        
        # PII handling
        'mask_user_ids': True,
        'exclude_sensitive_params': ['email', 'medical_data', 'personal_info']
    }
    
    # ========================================
    # DEBUGGING E TESTING
    # ========================================
    
    DEBUG_CONFIG = {
        'log_events': True,
        'validate_events': True,
        'test_mode_users': ['test@ninomedical.ai', 'admin@ninomedical.ai'],
        'debug_overlay': False  # Show debug info in UI
    }

def get_analytics_config() -> Dict[str, Any]:
    """
    Restituisce la configurazione completa per Google Analytics.
    
    Returns:
        dict: Configurazione completa
    """
    return {
        'measurement_id': AnalyticsSettings.GA4_MEASUREMENT_ID,
        'api_secret': AnalyticsSettings.GA4_API_SECRET,
        'enabled': AnalyticsSettings.ANALYTICS_ENABLED,
        'debug': AnalyticsSettings.DEBUG_MODE,
        'timeout': AnalyticsSettings.REQUEST_TIMEOUT,
        'events': AnalyticsSettings.CUSTOM_EVENTS,
        'parameters': AnalyticsSettings.CUSTOM_PARAMETERS,
        'ecommerce': AnalyticsSettings.ECOMMERCE_CONFIG,
        'privacy': TrackingConfiguration.PRIVACY_SETTINGS,
        'page_tracking': TrackingConfiguration.PAGE_TRACKING
    }

def validate_config() -> bool:
    """
    Valida la configurazione Google Analytics.
    
    Returns:
        bool: True se la configurazione è valida
    """
    config = get_analytics_config()
    
    # Verifica ID di misurazione
    if not config['measurement_id'] or config['measurement_id'] == 'G-XXXXXXXXXX':
        print("⚠️ Measurement ID non configurato. Aggiorna GA4_MEASUREMENT_ID.")
        return False
    
    # Verifica formato ID
    if not config['measurement_id'].startswith('G-'):
        print("⚠️ Formato Measurement ID non valido. Deve iniziare con 'G-'.")
        return False
    
    print("✅ Configurazione Google Analytics valida.")
    return True

# Funzioni di utilità per environment variables
def load_config_from_env():
    """Carica configurazione da variabili d'ambiente."""
    print("📋 Caricamento configurazione Google Analytics...")
    
    config_vars = [
        'GA4_MEASUREMENT_ID',
        'GA4_API_SECRET', 
        'ANALYTICS_ENABLED',
        'ANALYTICS_DEBUG',
        'ANALYTICS_TIMEOUT'
    ]
    
    loaded_vars = {}
    for var in config_vars:
        value = os.getenv(var)
        if value:
            loaded_vars[var] = value
            print(f"✅ {var}: configurato")
        else:
            print(f"⚠️ {var}: non configurato (usando default)")
    
    return loaded_vars

def print_config_instructions():
    """Stampa istruzioni per la configurazione."""
    print("""
🔧 ISTRUZIONI CONFIGURAZIONE GOOGLE ANALYTICS
===============================================

1. Vai su Google Analytics 4 (analytics.google.com)
2. Crea una proprietà GA4 per la tua app
3. Vai su Admin > Data Streams > Scegli il tuo stream
4. Copia il Measurement ID (formato: G-XXXXXXXXXX)
5. Aggiorna GA4_MEASUREMENT_ID in analytics_config.py

Per tracking server-side (opzionale ma consigliato):
6. Sempre in Data Streams, vai su "Measurement Protocol API secrets"  
7. Crea un nuovo secret
8. Copia il secret e aggiorna GA4_API_SECRET

Variabili d'ambiente (alternative):
export GA4_MEASUREMENT_ID="G-TUOID"
export GA4_API_SECRET="tuo-secret"
export ANALYTICS_ENABLED="true"

🔒 PRIVACY E COMPLIANCE:
- IP anonimizzati automaticamente
- Google Signals disabilitato
- Retention dati: 14 mesi
- Compliance GDPR ready
""")

if __name__ == "__main__":
    print("🔍 Test Configurazione Google Analytics")
    print("=" * 50)
    
    # Carica e valida configurazione
    load_config_from_env()
    is_valid = validate_config()
    
    if not is_valid:
        print("\n📋 Istruzioni configurazione:")
        print_config_instructions()
    else:
        config = get_analytics_config()
        print(f"\n✅ Configurazione caricata con successo!")
        print(f"📊 Measurement ID: {config['measurement_id']}")
        print(f"🔧 API Secret: {'configurato' if config['api_secret'] else 'non configurato'}")
        print(f"🚀 Analytics abilitati: {config['enabled']}")
