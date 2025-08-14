#!/usr/bin/env python3
"""
Google Analytics Integration for Nino Medical AI
================================================

Modulo per l'integrazione con Google Analytics 4 (GA4) per tracciare:
- Visitors (visitatori)
- Comments (commenti/feedback)  
- Purchases (acquisti/upgrade Pro)
- User interactions e page views

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from urllib.parse import urlencode
import base64

class GoogleAnalytics:
    """Classe per l'integrazione con Google Analytics 4."""
    
    def __init__(self, measurement_id: str, api_secret: str = None):
        """
        Inizializza il client Google Analytics.
        
        Args:
            measurement_id (str): ID di misurazione GA4 (es. G-XXXXXXXXXX)
            api_secret (str): Secret per Measurement Protocol API (opzionale)
        """
        self.measurement_id = measurement_id
        self.api_secret = api_secret
        self.base_url = "https://www.google-analytics.com/mp/collect"
        self.debug_url = "https://www.google-analytics.com/debug/mp/collect"
        
        # Genera o recupera client_id univoco per sessione
        if 'ga_client_id' not in st.session_state:
            st.session_state.ga_client_id = str(uuid.uuid4())
    
    def get_client_id(self) -> str:
        """Ottiene il client ID univoco per la sessione."""
        return st.session_state.ga_client_id
    
    def get_user_properties(self) -> Dict[str, Any]:
        """Ottiene le proprietà utente per GA."""
        user_props = {
            'user_id': None,
            'user_role': 'guest',
            'user_tier': 'free'
        }
        
        # Se l'utente è autenticato, aggiungi informazioni
        if hasattr(st.session_state, 'user') and st.session_state.user:
            user = st.session_state.user
            user_props.update({
                'user_id': str(user.id),
                'user_role': user.role.value if hasattr(user, 'role') else 'user',
                'user_tier': 'pro' if getattr(user, 'is_pro', False) else 'free'
            })
        
        return user_props
    
    def track_event(self, event_name: str, parameters: Dict[str, Any] = None) -> bool:
        """
        Invia un evento a Google Analytics.
        
        Args:
            event_name (str): Nome dell'evento
            parameters (dict): Parametri aggiuntivi dell'evento
            
        Returns:
            bool: True se l'invio è riuscito
        """
        if not self.api_secret:
            # Se non c'è API secret, usa gtag frontend (inserito tramite HTML)
            return self._track_frontend_event(event_name, parameters)
        
        # Usa Measurement Protocol per tracking server-side
        return self._track_server_event(event_name, parameters)
    
    def _track_frontend_event(self, event_name: str, parameters: Dict[str, Any] = None) -> bool:
        """Traccia evento via frontend gtag."""
        try:
            params = parameters or {}
            params_js = json.dumps(params)
            
            # Inject JavaScript per gtag
            gtag_script = f"""
            <script>
                if (typeof gtag !== 'undefined') {{
                    gtag('event', '{event_name}', {params_js});
                    console.log('GA Event sent: {event_name}');
                }}
            </script>
            """
            
            st.components.v1.html(gtag_script, height=0)
            return True
            
        except Exception as e:
            st.error(f"Errore tracking frontend: {e}")
            return False
    
    def _track_server_event(self, event_name: str, parameters: Dict[str, Any] = None) -> bool:
        """Invia evento tramite Measurement Protocol."""
        try:
            params = parameters or {}
            user_props = self.get_user_properties()
            
            payload = {
                "client_id": self.get_client_id(),
                "events": [{
                    "name": event_name,
                    "params": {
                        **params,
                        "session_id": st.session_state.get('session_id', 'unknown'),
                        "page_title": st.get_option('browser.title', 'Nino Medical AI'),
                        "page_location": st.get_option('server.baseUrlPath', '/'),
                        **user_props
                    }
                }]
            }
            
            if user_props['user_id']:
                payload['user_id'] = user_props['user_id']
            
            url = f"{self.base_url}?measurement_id={self.measurement_id}&api_secret={self.api_secret}"
            
            response = requests.post(url, json=payload, timeout=5)
            
            return response.status_code == 204
            
        except Exception as e:
            # Log error but don't break the app
            print(f"GA tracking error: {e}")
            return False
    
    def track_page_view(self, page_path: str, page_title: str = None) -> bool:
        """Traccia visualizzazione pagina."""
        return self.track_event('page_view', {
            'page_location': page_path,
            'page_title': page_title or page_path,
            'timestamp': datetime.now().isoformat()
        })
    
    def track_user_login(self, user_id: str, method: str = 'email') -> bool:
        """Traccia login utente."""
        return self.track_event('login', {
            'user_id': user_id,
            'method': method
        })
    
    def track_user_signup(self, user_id: str, method: str = 'email') -> bool:
        """Traccia registrazione utente."""
        return self.track_event('sign_up', {
            'user_id': user_id,
            'method': method
        })
    
    def track_comment_submission(self, comment_type: str = 'feedback', rating: int = None) -> bool:
        """Traccia invio commento/feedback."""
        params = {
            'comment_type': comment_type,
            'timestamp': datetime.now().isoformat()
        }
        
        if rating:
            params['rating'] = rating
        
        return self.track_event('comment_submit', params)
    
    def track_purchase(self, transaction_id: str, value: float, currency: str = 'EUR', 
                      item_name: str = 'Pro License') -> bool:
        """Traccia acquisto/upgrade Pro."""
        return self.track_event('purchase', {
            'transaction_id': transaction_id,
            'value': value,
            'currency': currency,
            'items': [{
                'item_id': 'nino_medical_ai_pro',
                'item_name': item_name,
                'category': 'software_license',
                'quantity': 1,
                'price': value
            }]
        })
    
    def track_pro_feature_usage(self, feature_name: str, action: str = 'use') -> bool:
        """Traccia utilizzo funzionalità Pro."""
        return self.track_event('pro_feature_usage', {
            'feature_name': feature_name,
            'action': action,
            'timestamp': datetime.now().isoformat()
        })
    
    def track_search_query(self, query: str, database: str, results_count: int = 0) -> bool:
        """Traccia ricerca nei database medici."""
        return self.track_event('search', {
            'search_term': query,
            'database': database,
            'results_count': results_count
        })
    
    def track_ai_analysis(self, analysis_type: str, duration_seconds: float = None, 
                         confidence_score: float = None) -> bool:
        """Traccia analisi IA."""
        params = {
            'analysis_type': analysis_type,
            'timestamp': datetime.now().isoformat()
        }
        
        if duration_seconds:
            params['duration_seconds'] = duration_seconds
        if confidence_score:
            params['confidence_score'] = confidence_score
        
        return self.track_event('ai_analysis', params)
    
    def track_export_action(self, export_format: str, content_type: str) -> bool:
        """Traccia export di dati."""
        return self.track_event('export', {
            'export_format': export_format,
            'content_type': content_type,
            'timestamp': datetime.now().isoformat()
        })

class AnalyticsConfig:
    """Configurazione per Google Analytics."""
    
    # GA4 Measurement ID - SOSTITUISCI CON IL TUO
    MEASUREMENT_ID = "G-XXXXXXXXXX"  # Inserisci il tuo GA4 Measurement ID
    
    # API Secret per Measurement Protocol (opzionale) 
    API_SECRET = None  # Inserisci il tuo API Secret se usi server-side tracking
    
    # Eventi personalizzati
    EVENTS = {
        'PAGE_VIEW': 'page_view',
        'USER_LOGIN': 'login', 
        'USER_SIGNUP': 'sign_up',
        'COMMENT_SUBMIT': 'comment_submit',
        'PURCHASE': 'purchase',
        'PRO_FEATURE_USAGE': 'pro_feature_usage',
        'SEARCH_QUERY': 'search',
        'AI_ANALYSIS': 'ai_analysis',
        'EXPORT_ACTION': 'export'
    }

def get_gtag_script(measurement_id: str) -> str:
    """
    Genera script gtag per inserimento nell'HTML.
    
    Args:
        measurement_id (str): ID di misurazione GA4
        
    Returns:
        str: Script HTML per gtag
    """
    return f"""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{measurement_id}', {{
            'send_page_view': true,
            'anonymize_ip': true,
            'allow_google_signals': false,
            'allow_ad_personalization_signals': false
        }});
        
        // Custom dimensions per app medica
        gtag('config', '{measurement_id}', {{
            'custom_map': {{
                'custom_parameter_1': 'user_tier',
                'custom_parameter_2': 'user_role'
            }}
        }});
    </script>
    """

def inject_analytics_script(measurement_id: str):
    """Inietta script Google Analytics nell'app Streamlit."""
    if measurement_id and measurement_id != "G-XXXXXXXXXX":
        script = get_gtag_script(measurement_id)
        st.components.v1.html(script, height=0)

# Istanza globale Analytics
_analytics_instance = None

def get_analytics() -> GoogleAnalytics:
    """Ottiene l'istanza singleton di GoogleAnalytics."""
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = GoogleAnalytics(
            measurement_id=AnalyticsConfig.MEASUREMENT_ID,
            api_secret=AnalyticsConfig.API_SECRET
        )
    return _analytics_instance

# Decorators per tracking automatico
def track_page_access(page_name: str):
    """Decorator per tracciare accesso a pagina."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            analytics = get_analytics()
            analytics.track_page_view(page_name, f"Nino Medical AI - {page_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def track_pro_feature(feature_name: str):
    """Decorator per tracciare uso funzionalità Pro.""" 
    def decorator(func):
        def wrapper(*args, **kwargs):
            analytics = get_analytics()
            analytics.track_pro_feature_usage(feature_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Funzioni di convenienza
def track_visitor():
    """Traccia un visitatore."""
    analytics = get_analytics()
    return analytics.track_page_view('/', 'Home - Nino Medical AI')

def track_comment(comment_type: str = 'general', rating: int = None):
    """Traccia un commento/feedback."""
    analytics = get_analytics()
    return analytics.track_comment_submission(comment_type, rating)

def track_purchase(transaction_id: str, value: float):
    """Traccia un acquisto Pro."""
    analytics = get_analytics()
    return analytics.track_purchase(transaction_id, value)

if __name__ == "__main__":
    # Test del modulo
    print("Testing Google Analytics integration...")
    
    analytics = GoogleAnalytics("G-TEST123")
    
    # Test eventi
    test_events = [
        ("page_view", {"page": "test"}),
        ("login", {"user_id": "test_user"}),
        ("purchase", {"value": 29.99, "currency": "EUR"})
    ]
    
    for event_name, params in test_events:
        result = analytics.track_event(event_name, params)
        print(f"Event '{event_name}': {'✅' if result else '❌'}")
