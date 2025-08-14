#!/usr/bin/env python3
"""
Nino Medical AI - App Principale con Sistema di Protezione Pro
==============================================================

App Streamlit che integra autenticazione, licensing Pro e funzionalità demo.
Protegge le funzionalità avanzate e guida gli utenti verso l'upgrade.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import base64
import sys
import time
from pathlib import Path

# Importa moduli di autenticazione e licensing
try:
    from auth_system import AuthManager, SessionManager, render_login_form, render_user_profile, render_admin_panel, UserRole
    from pro_license_system import LicenseManager, ProFeatureGuard, demo_pro_features, show_upgrade_info
except ImportError as e:
    st.error(f"⚠️ Errore importazione moduli: {e}")
    st.stop()

# Importa moduli Google Analytics
try:
    from google_analytics import GoogleAnalytics, get_analytics, inject_analytics_script, track_visitor, track_comment, track_purchase
    from analytics_config import AnalyticsSettings, get_analytics_config, validate_config
    ANALYTICS_AVAILABLE = True
    
    # Importa moduli Engagement
    from engagement_tracker import get_engagement_tracker, track_page_engagement, show_engagement_badge
    from engaged_visitors_dashboard import render_engaged_visitors_dashboard
    ENGAGEMENT_TRACKER_AVAILABLE = True
    
except ImportError as e:
    print(f"⚠️ Google Analytics non disponibile: {e}")
    ANALYTICS_AVAILABLE = False
    ENGAGEMENT_TRACKER_AVAILABLE = False

# --- Page Configuration ---
st.set_page_config(
    page_title="Nino Medical AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Google Analytics Initialization ---
if ANALYTICS_AVAILABLE:
    # Inietta script Google Analytics
    inject_analytics_script(AnalyticsSettings.GA4_MEASUREMENT_ID)
    
    # Inizializza sessione analytics se non presente
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = datetime.now()
        st.session_state.page_views = 0
        st.session_state.session_id = str(int(time.time()))
        
        # Inizializza engagement tracker
        if ENGAGEMENT_TRACKER_AVAILABLE:
            get_engagement_tracker()
        
        # Traccia inizio sessione
        analytics = get_analytics()
        analytics.track_event('session_start', {
            'timestamp': st.session_state.session_start_time.isoformat()
        })

# --- Custom CSS ---
st.markdown("""
<style>
    /* General Styles */
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        color: #1f4e79;
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 0.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transform: translateY(-5px);
    }
    .metric-card {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .pro-banner {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .free-tier-notice {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem;
        margin-top: 4rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Application ---
def main():
    """Main function to render the Streamlit app."""
    
    # Check authentication
    if not SessionManager.is_authenticated():
        render_welcome_page()
        return
    
    # Authenticated user interface
    # Mostra engagement badge se applicabile
    if ENGAGEMENT_TRACKER_AVAILABLE:
        show_engagement_badge()
    
    render_authenticated_app()

def render_welcome_page():
    """Renders welcome page with login and demo."""
    # Track page view
    if ANALYTICS_AVAILABLE:
        analytics = get_analytics()
        analytics.track_page_view('/welcome', 'Welcome - Nino Medical AI')
        st.session_state.page_views += 1
    
    st.markdown('<h1 class="main-header">🏥 Nino Medical AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligenza Artificiale per la Medicina del Futuro</p>', unsafe_allow_html=True)
    
    # Banner principale
    st.markdown("""
    <div class="pro-banner">
        <h2>🚀 Benvenuto nella piattaforma di IA medica più avanzata</h2>
        <p>Scopri come l'Intelligenza Artificiale sta rivoluzionando la medicina con analisi predittive, elaborazione di imaging medico e integrazione di database globali.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs per contenuto
    tab1, tab2, tab3 = st.tabs(["🚪 Login/Registrazione", "🎯 Demo Gratuita", "💎 Versione Pro"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_free_demo()
    
    with tab3:
        show_upgrade_info()

def render_free_demo():
    """Renders free demo features."""
    st.markdown("## 🎯 Prova Gratuita - Funzionalità Base")
    
    st.markdown("""
    <div class="free-tier-notice">
        <strong>📍 Modalità Demo Gratuita</strong><br>
        Stai utilizzando la versione gratuita con funzionalità limitate. 
        Effettua il login o registrati per accedere a più funzionalità!
    </div>
    """, unsafe_allow_html=True)
    
    # Demo funzionalità base
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Database Medici - Demo")
        
        demo_query = st.text_input("Cerca pubblicazioni (demo):", placeholder="es. covid vaccine")
        
        if st.button("🔍 Cerca (Demo)"):
            if demo_query:
                # Track demo search
                if ANALYTICS_AVAILABLE:
                    analytics = get_analytics()
                    analytics.track_search_query(demo_query, 'demo', 5)
                
                with st.spinner("Ricerca demo in corso..."):
                    # Simulazione risultati limitati
                    st.success("Demo: Trovati 5 risultati (versione Pro: 500+ risultati)")
                    demo_data = {
                        'Titolo': [f'[DEMO] Studio su {demo_query} - {i+1}' for i in range(3)],
                        'Autori': ['Demo Author et al.' for _ in range(3)],
                        'Anno': [2023, 2022, 2021]
                    }
                    st.dataframe(pd.DataFrame(demo_data))
                    
                    st.info("💎 La versione Pro offre: Accesso completo a tutti i database, export PDF, analisi AI avanzate")
            else:
                st.warning("Inserisci un termine di ricerca")
    
    with col2:
        st.markdown("### 🧠 Analisi IA - Demo")
        
        st.info("Carica un'immagine per una demo di analisi")
        
        uploaded_file = st.file_uploader("Scegli un file (demo)", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Immagine caricata - Demo", width=300)
            
            if st.button("⚡ Analizza (Demo)"):
                # Track demo AI analysis
                if ANALYTICS_AVAILABLE:
                    analytics = get_analytics()
                    analytics.track_ai_analysis('demo_image_analysis', confidence_score=0.85)
                
                with st.spinner("Analisi demo in corso..."):
                    # Simulazione analisi limitata
                    st.success("✅ Analisi completata (modalità demo)")
                    
                    # Risultati demo limitati
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Confidence", "Demo: 85%")
                    with col_b:
                        st.metric("Categoria", "Demo Result")
                    
                    st.warning("💎 Versione Pro: Analisi completa, modelli specializzati, report dettagliati")

def render_authenticated_app():
    """Renders the main authenticated application."""
    render_sidebar()
    
    # Page routing
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        render_main_dashboard()
    elif page == 'databases':
        render_medical_databases_page()
    elif page == 'predictive_medicine':
        render_predictive_medicine_page()
    elif page == 'clinical_trials':
        render_clinical_trials_page()
    elif page == 'pro_features':
        render_pro_features_page()
    elif page == 'profile':
        render_user_profile()
    elif page == 'admin':
        render_admin_panel()
    elif page == 'analytics':
        render_analytics_page()
    elif page == 'engagement':
        render_engagement_page()
    elif page == 'about':
        render_about_page()
    
    render_footer()

def render_sidebar():
    """Renders the navigation sidebar."""
    with st.sidebar:
        user = SessionManager.get_current_user()
        
        st.markdown('<h1 style="text-align: center; color: #1f4e79;">Nino Medical AI</h1>', unsafe_allow_html=True)
        
        # User info
        if user:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: #f0f8ff; border-radius: 8px; margin-bottom: 20px;">
                <strong>👤 {user.full_name}</strong><br>
                <small>{user.role.value.title()}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Check Pro status
            license_manager = LicenseManager()
            is_pro_user = license_manager.validate_pro_access(user.id)
            
            if is_pro_user:
                st.markdown("✨ **UTENTE PRO** ✨")
            else:
                st.markdown("🆓 **Utente Gratuito**")
                if st.button("💎 Upgrade to Pro", key="sidebar_upgrade", use_container_width=True):
                    # Track upgrade button click
                    if ANALYTICS_AVAILABLE:
                        analytics = get_analytics()
                        analytics.track_event('upgrade_view', {
                            'source': 'sidebar',
                            'user_tier': 'free'
                        })
                    st.session_state.current_page = 'pro_features'
                    st.rerun()
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### 🏥 Navigazione")
        nav_buttons = {
            "📊 Dashboard": "dashboard",
            "🌍 Database Medici": "databases", 
            "🧠 Medicina Predittiva": "predictive_medicine",
            "🧪 Trial Clinici": "clinical_trials",
            "💎 Funzionalità Pro": "pro_features",
            "👤 Profilo": "profile",
            "👨‍💻 Chi Sono": "about"
        }
        
        # Add admin option for admin users
        if user and user.role == UserRole.ADMIN:
            nav_buttons["⚙️ Admin Panel"] = "admin"
            nav_buttons["📊 Analytics"] = "analytics"
            nav_buttons["🔥 Engagement"] = "engagement"
        
        for label, page_key in nav_buttons.items():
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                # Track navigation
                if ANALYTICS_AVAILABLE:
                    analytics = get_analytics()
                    analytics.track_page_view(f'/{page_key}', f'{label} - Nino Medical AI')
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            SessionManager.clear_session()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Statistiche")
        st.metric("🤖 Modelli AI", "45+", delta="5 recenti")
        st.metric("📄 Pubblicazioni", "1.2M+", delta="10k recenti")
        st.metric("📈 Analisi", "250k+")

def render_main_dashboard():
    """Renders the main dashboard."""
    user = SessionManager.get_current_user()
    license_manager = LicenseManager()
    is_pro_user = license_manager.validate_pro_access(user.id)
    
    # Track dashboard access
    if ANALYTICS_AVAILABLE:
        analytics = get_analytics()
        analytics.track_page_view('/dashboard', 'Dashboard - Nino Medical AI')
        st.session_state.page_views += 1
    
    st.markdown('<h1 class="main-header">🏥 Dashboard Principale</h1>', unsafe_allow_html=True)
    
    if is_pro_user:
        st.markdown('<p class="sub-header">✨ Benvenuto nella versione Pro Ultimate!</p>', unsafe_allow_html=True)
        render_pro_dashboard()
    else:
        st.markdown('<p class="sub-header">Versione Gratuita - Funzionalità Limitate</p>', unsafe_allow_html=True)
        render_free_dashboard()

def render_free_dashboard():
    """Renders limited dashboard for free users."""
    st.markdown("""
    <div class="free-tier-notice">
        🆓 <strong>Versione Gratuita Attiva</strong><br>
        Hai accesso alle funzionalità base. Upgrade alla versione Pro per sbloccare tutto!
    </div>
    """, unsafe_allow_html=True)
    
    # Limited metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔍 Ricerche", "5/10", delta="Limite gratuito")
    with col2:
        st.metric("📊 Analisi IA", "2/5", delta="Limite giornaliero")
    with col3:
        st.metric("💾 Export", "0/0", delta="Solo Pro")
    with col4:
        st.metric("⏰ Ultimo Accesso", datetime.now().strftime("%H:%M"))
    
    # Demo charts
    st.markdown("### 📈 Demo Funzionalità")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔬 Analisi Demo")
        demo_data = pd.DataFrame({
            'Categoria': ['Demo A', 'Demo B', 'Demo C'],
            'Valori': [40, 30, 30]
        })
        fig = px.pie(demo_data, values='Valori', names='Categoria', title="Dati Demo")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 📊 Statistiche Base")
        demo_trend = pd.DataFrame({
            'Giorno': ['Lun', 'Mar', 'Mer', 'Gio', 'Ven'],
            'Utilizzo': [3, 5, 2, 4, 1]
        })
        fig = px.line(demo_trend, x='Giorno', y='Utilizzo', title="Utilizzo Settimanale")
        st.plotly_chart(fig, use_container_width=True)

def render_pro_dashboard():
    """Renders full dashboard for Pro users."""
    st.success("✅ Funzionalità Pro attive!")
    
    # Full metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔍 Ricerche", "∞", delta="Illimitate")
    with col2:
        st.metric("📊 Analisi IA", "∞", delta="Illimitate")
    with col3:
        st.metric("💾 Export", "45", delta="+12 oggi")
    with col4:
        st.metric("⚡ Performance", "99.2%", delta="+2.1%")
    
    # Advanced charts
    st.markdown("### 🚀 Analytics Avanzate Pro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔬 Modelli AI Performance")
        models_data = pd.DataFrame({
            'Modello': ['CV Risk', 'Diabetes Pred', 'Cancer Screen', 'Drug Response'],
            'Accuratezza': [94.5, 91.2, 89.7, 92.1],
            'Utilizzo': [150, 89, 67, 201]
        })
        fig = px.scatter(models_data, x='Accuratezza', y='Utilizzo', size='Utilizzo',
                        color='Modello', title="Performance vs Utilizzo")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 📈 Trend Analisi Mensile")
        months = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu']
        analysis_counts = [120, 150, 180, 220, 250, 300]
        fig = px.bar(x=months, y=analysis_counts, title="Analisi per Mese")
        st.plotly_chart(fig, use_container_width=True)

@ProFeatureGuard.require_pro_feature('database_access')
def render_medical_databases_page():
    """Renders medical databases page - Pro feature."""
    st.markdown('<h2 class="section-header">🌍 Database Medici Globali</h2>', unsafe_allow_html=True)
    st.success("✅ Accesso Pro attivo - Database completi disponibili")
    
    # Pro database interface
    db_options = ["PubMed", "ClinicalTrials.gov", "FDA", "WHO", "UniProt", "Disease Ontology", "OMIM", "PharmGKB"]
    selected_db = st.selectbox("Database:", db_options)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Query di ricerca:", placeholder="es. BRCA1 mutations breast cancer")
    with col2:
        max_results = st.number_input("Max risultati:", 10, 1000, 100)
    
    if st.button("🔍 Ricerca Avanzata", use_container_width=True):
        if search_query:
            # Track Pro database search
            if ANALYTICS_AVAILABLE:
                analytics = get_analytics()
                analytics.track_search_query(search_query, selected_db, max_results)
                analytics.track_pro_feature_usage('database_search')
            
            with st.spinner(f"Ricerca su {selected_db}..."):
                # Simulazione ricerca Pro
                st.success(f"✅ Trovati {max_results} risultati in {selected_db}")
                
                # Results table
                results_data = {
                    'Titolo': [f'[PRO] {search_query} - Studio {i+1}' for i in range(10)],
                    'Autori': [f'Research Team {i+1} et al.' for i in range(10)],
                    'Journal': [f'Med Journal {i%3 + 1}' for i in range(10)],
                    'Anno': [2023-i%4 for i in range(10)],
                    'Citations': [np.random.randint(50, 500) for _ in range(10)],
                    'DOI': [f'10.1234/journal.{1000+i}' for i in range(10)]
                }
                
                df = pd.DataFrame(results_data)
                st.dataframe(df, use_container_width=True)
                
                # Pro export options
                st.markdown("### 💾 Opzioni Export Pro")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📄 Export PDF"):
                        if ANALYTICS_AVAILABLE:
                            analytics = get_analytics()
                            analytics.track_export_action('PDF', 'medical_research')
                        st.success("Report PDF generato!")
                with col2:
                    if st.button("📊 Export Excel"):
                        if ANALYTICS_AVAILABLE:
                            analytics = get_analytics()
                            analytics.track_export_action('Excel', 'medical_research')
                        st.success("File Excel creato!")
                with col3:
                    if st.button("🔗 Export BibTeX"):
                        if ANALYTICS_AVAILABLE:
                            analytics = get_analytics()
                            analytics.track_export_action('BibTeX', 'medical_research')
                        st.success("Bibliografia generata!")

def render_predictive_medicine_page():
    """Renders predictive medicine page with Pro protection for advanced features."""
    st.markdown('<h2 class="section-header">🧠 Medicina Predittiva</h2>', unsafe_allow_html=True)
    
    user = SessionManager.get_current_user()
    license_manager = LicenseManager()
    is_pro_user = license_manager.validate_pro_access(user.id)
    
    if is_pro_user:
        render_pro_predictive_medicine()
    else:
        render_basic_predictive_medicine()

def render_basic_predictive_medicine():
    """Basic predictive medicine for free users."""
    st.warning("🆓 Versione gratuita - Modello base disponibile")
    
    st.markdown("### 💓 Calcolatore Rischio Cardiovascolare Base")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Età", 20, 100, 45)
        cholesterol = st.number_input("Colesterolo (mg/dL)", 100, 400, 200)
    with col2:
        blood_pressure = st.number_input("Pressione (mmHg)", 80, 200, 120)
        smoker = st.radio("Fumatore", ["No", "Sì"])
    
    if st.button("🔍 Calcola (Base)"):
        # Track basic prediction usage
        if ANALYTICS_AVAILABLE:
            analytics = get_analytics()
            analytics.track_ai_analysis('cardiovascular_risk_basic', confidence_score=0.75)
        
        # Calcolo semplificato
        risk = (age/100 + cholesterol/400 + blood_pressure/200) * (1.5 if smoker == "Sì" else 1.0) / 3
        st.metric("Rischio Base", f"{risk:.2%}")
        
        st.info("💎 Versione Pro: Modelli avanzati, fattori aggiuntivi, analisi genetica")

@ProFeatureGuard.require_pro_feature('advanced_predictive')
def render_pro_predictive_medicine():
    """Advanced predictive medicine for Pro users."""
    st.success("✅ Modelli Predittivi Pro Attivi")
    
    model_type = st.selectbox("Modello Predittivo:", [
        "Rischio Cardiovascolare Avanzato",
        "Predizione Diabete Multi-fattoriale", 
        "Analisi Risposta Farmacologica",
        "Screening Oncologico Predittivo"
    ])
    
    if model_type == "Rischio Cardiovascolare Avanzato":
        st.markdown("#### 🫀 Modello Pro - Fattori Multipli")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider("Età", 20, 100, 55)
            weight = st.number_input("Peso (kg)", 40, 200, 75)
            height = st.number_input("Altezza (cm)", 140, 220, 175)
        
        with col2:
            cholesterol_total = st.number_input("Colesterolo Tot.", 100, 400, 220)
            cholesterol_hdl = st.number_input("HDL", 20, 100, 45)
            cholesterol_ldl = st.number_input("LDL", 50, 300, 130)
        
        with col3:
            bp_systolic = st.number_input("Pressione Sist.", 80, 200, 140)
            bp_diastolic = st.number_input("Pressione Diast.", 50, 120, 90)
            glucose = st.number_input("Glicemia", 50, 200, 90)
        
        # Advanced factors
        st.markdown("#### 🧬 Fattori Avanzati Pro")
        col1, col2 = st.columns(2)
        with col1:
            family_history = st.multiselect("Storia Familiare:", ["Infarto", "Ictus", "Diabete"])
            lifestyle = st.multiselect("Stile di Vita:", ["Fumatore", "Sedentario", "Stress Alto"])
        with col2:
            medications = st.multiselect("Farmaci:", ["ACE-inibitori", "Statine", "Beta-bloccanti"])
            genetic_factors = st.multiselect("Fattori Genetici:", ["APOE ε4", "9p21", "LPA"])
        
        if st.button("⚡ Analisi Predittiva Pro", use_container_width=True):
            # Track Pro prediction usage
            if ANALYTICS_AVAILABLE:
                start_time = time.time()
                analytics = get_analytics()
                analytics.track_pro_feature_usage('advanced_prediction')
            
            with st.spinner("Modello AI Pro in elaborazione..."):
                # Calcolo avanzato simulato
                bmi = weight / ((height/100)**2)
                risk_base = (age/100 + cholesterol_total/300 + bp_systolic/180) / 3
                risk_adj = risk_base * (1 + len(family_history)*0.1 + len(lifestyle)*0.15)
                
                st.success("🎯 Analisi Pro completata!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Rischio 10 anni", f"{risk_adj:.1%}", delta="Alto" if risk_adj > 0.3 else "Moderato")
                with col2:
                    st.metric("BMI", f"{bmi:.1f}", delta="Normale" if 18.5 <= bmi <= 24.9 else "Attenzione")
                with col3:
                    st.metric("Ratio Colest.", f"{cholesterol_total/cholesterol_hdl:.1f}")
                with col4:
                    st.metric("Confidence", "94.7%")
                
                # Pro insights
                st.markdown("#### 🔬 Insights Pro")
                st.info(f"📊 Il modello ha analizzato {len(family_history) + len(lifestyle) + len(medications) + len(genetic_factors) + 9} parametri")
                st.warning("⚠️ Raccomandazioni: Monitoraggio specialistico ogni 6 mesi")

def render_clinical_trials_page():
    """Clinical trials page with demo/Pro differentiation."""
    st.markdown('<h2 class="section-header">🧪 Trial Clinici</h2>', unsafe_allow_html=True)
    
    user = SessionManager.get_current_user()
    license_manager = LicenseManager()
    is_pro_user = license_manager.validate_pro_access(user.id)
    
    if not is_pro_user:
        st.info("🆓 Versione gratuita: Ricerca limitata nei trial pubblici")
        
        trial_query = st.text_input("Cerca trial (demo):", placeholder="cancer immunotherapy")
        if st.button("🔍 Cerca Trial Demo"):
            if trial_query:
                st.success("Demo: Trovati 3 trial (Pro: 150+ risultati)")
                demo_trials = pd.DataFrame({
                    'Trial': [f'DEMO-{i+1}' for i in range(3)],
                    'Fase': ['Fase II', 'Fase III', 'Fase I'],
                    'Sponsor': ['Demo Pharma', 'Research Inc', 'MedTech Ltd'],
                    'Stato': ['Recruiting', 'Active', 'Completed']
                })
                st.dataframe(demo_trials)
                st.info("💎 Pro: Accesso completo, filtering avanzato, matching pazienti")
    else:
        render_pro_clinical_trials()

@ProFeatureGuard.require_pro_feature('clinical_trials')
def render_pro_clinical_trials():
    """Pro clinical trials functionality."""
    st.success("✅ Accesso Pro ai Trial Clinici")
    
    st.markdown("#### 🎯 Ricerca Avanzata Trial")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        condition = st.text_input("Condizione:", placeholder="breast cancer")
        phase = st.multiselect("Fase:", ["Fase I", "Fase II", "Fase III", "Fase IV"])
    with col2:
        status = st.multiselect("Stato:", ["Recruiting", "Active", "Completed", "Suspended"])
        sponsor_type = st.selectbox("Sponsor:", ["Tutti", "Pharma", "Accademic", "Government"])
    with col3:
        location = st.text_input("Località:", placeholder="Italy, Europe")
        age_range = st.slider("Età:", 0, 100, (18, 65))
    
    if st.button("🔍 Ricerca Pro Completa"):
        with st.spinner("Ricerca nei database globali..."):
            st.success("✅ Trovati 247 trial corrispondenti")
            
            # Mock comprehensive results
            trials_data = {
                'NCT ID': [f'NCT{np.random.randint(10000000, 99999999)}' for _ in range(15)],
                'Titolo': [f'Trial {condition} - Studio {i+1}' for i in range(15)],
                'Fase': np.random.choice(phase if phase else ['Fase I', 'Fase II', 'Fase III'], 15),
                'Sponsor': [f'Sponsor {i+1}' for i in range(15)],
                'Locations': np.random.choice(['Milano', 'Roma', 'Torino', 'Multi-center'], 15),
                'Enrollment': [np.random.randint(50, 1000) for _ in range(15)],
                'Start Date': [f'2023-{np.random.randint(1,12):02d}-01' for _ in range(15)]
            }
            
            df_trials = pd.DataFrame(trials_data)
            st.dataframe(df_trials, use_container_width=True)
            
            # Pro tools
            st.markdown("#### 🛠️ Strumenti Pro")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👥 Patient Matching"):
                    st.success("Matching AI: 23 pazienti compatibili trovati")
            with col2:
                if st.button("📊 Export Dettagliato"):
                    st.success("Report completo generato!")
            with col3:
                if st.button("📧 Alert Setup"):
                    st.success("Alert configurati per nuovi trial!")

def render_pro_features_page():
    """Page showcasing Pro features and upgrade options."""
    st.markdown('<h2 class="section-header">💎 Funzionalità Pro</h2>', unsafe_allow_html=True)
    
    user = SessionManager.get_current_user()
    license_manager = LicenseManager()
    is_pro_user = license_manager.validate_pro_access(user.id)
    
    if is_pro_user:
        st.success("✨ Sei già un utente Pro! Grazie per il supporto.")
        render_pro_management_panel()
    else:
        show_upgrade_info()
        st.markdown("---")
        demo_pro_features()

def render_pro_management_panel():
    """Management panel for Pro users."""
    st.markdown("### ⚙️ Pannello Gestione Pro")
    
    # Pro user stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✨ Status", "PRO ATTIVO")
    with col2:
        st.metric("📅 Scadenza", "30 giorni")
    with col3:
        st.metric("🔥 Utilizzo", "847 analisi")
    
    # Pro features usage
    st.markdown("### 📊 Utilizzo Funzionalità Pro")
    
    usage_data = pd.DataFrame({
        'Funzionalità': ['Database Completi', 'IA Avanzata', 'Export Report', 'API Access'],
        'Utilizzi': [156, 89, 34, 12],
        'Limite': ['∞', '∞', '∞', '∞']
    })
    
    st.dataframe(usage_data, use_container_width=True)
    
    # Pro settings
    st.markdown("### ⚙️ Impostazioni Pro")
    
    col1, col2 = st.columns(2)
    with col1:
        auto_export = st.checkbox("Export automatico risultati", value=True)
        email_reports = st.checkbox("Report email settimanali", value=False)
    with col2:
        api_notifications = st.checkbox("Notifiche API", value=True)
        priority_support = st.checkbox("Supporto prioritario", value=True)
    
    if st.button("💾 Salva Impostazioni Pro"):
        st.success("✅ Impostazioni Pro salvate!")

def render_about_page():
    """About page with professional information."""
    st.markdown('<h2 class="section-header">👨‍💻 Chi Sono</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div style='text-align:center; font-size: 8rem;'>👨‍💻</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Antonino Piacenza</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #2e7d32;'>AI Research & MedTech Developer</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### 🎯 Missione
        Sviluppare soluzioni di Intelligenza Artificiale innovative, etiche e accessibili per rivoluzionare 
        la medicina e migliorare la qualità delle cure globali.
        
        ### 🔬 Specializzazioni
        - **🤖 AI/ML in Medicina**: Modelli predittivi e di classificazione per applicazioni cliniche
        - **🧬 Genomica Computazionale**: Analisi di dati genetici e medicina personalizzata  
        - **📊 Medical Data Science**: Big data analytics e integrazione di database eterogenei
        - **🏥 Digital Health**: Piattaforme per telemedicina e monitoraggio remoto
        
        ### 🚀 Progetti Attuali
        - Nino Medical AI Pro: Piattaforma integrata per ricerca medica
        - Partnership con ospedali per validazione clinica
        - Ricerca su federated learning per privacy dei dati medici
        
        ### 📞 Contatti & Collaborazioni
        - **Email**: ninomedical.ai@gmail.com
        - **LinkedIn**: linkedin.com/in/antoNinoF840
        - **Portfolio**: antonino-piacenza-portfolio.streamlit.app
        
        💡 *Aperto a collaborazioni per progetti Horizon Europe e partnership industriali*
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics_page():
    """Renders analytics page for admin users only."""
    user = SessionManager.get_current_user()
    
    # Check admin access
    if not user or user.role != UserRole.ADMIN:
        st.error("❌ Accesso negato. Solo amministratori possono visualizzare le analytics.")
        return
    
    # Import analytics dashboard
    try:
        from analytics_dashboard import render_analytics_dashboard, render_analytics_setup_guide
        
        # Track analytics page view
        if ANALYTICS_AVAILABLE:
            analytics = get_analytics()
            analytics.track_page_view('/admin/analytics', 'Admin Analytics Dashboard')
        
        # Render dashboard tabs
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Feedback Form", "⚙️ Setup"])
        
        with tab1:
            render_analytics_dashboard()
        
        with tab2:
            render_feedback_collection()
            
        with tab3:
            render_analytics_setup_guide()
            
    except ImportError as e:
        st.error(f"⚠️ Modulo analytics dashboard non disponibile: {e}")
        st.info("📋 Assicurati che analytics_dashboard.py sia presente nel progetto.")

def render_feedback_collection():
    """Renders feedback collection interface for tracking comments."""
    st.markdown("### 💬 Raccolta Feedback e Commenti")
    
    st.info("📝 Utilizza questo modulo per raccogliere feedback dagli utenti e tracciarlo con Google Analytics.")
    
    # Feedback form
    with st.form("feedback_form"):
        st.markdown("#### ✍️ Lascia il tuo Feedback")
        
        col1, col2 = st.columns(2)
        
        with col1:
            feedback_type = st.selectbox("Tipo di Feedback:", [
                "Generale", "Bug Report", "Feature Request", "Esperienza Utente", "Performance"
            ])
            
            rating = st.slider("Valutazione (1-5 stelle):", 1, 5, 4)
            
        with col2:
            user_type = st.selectbox("Sei un:", [
                "Medico", "Ricercatore", "Studente", "Paziente", "Sviluppatore", "Altro"
            ])
            
            would_recommend = st.radio("Consiglieresti l'app?", ["Sì", "No", "Forse"])
        
        feedback_text = st.text_area("Il tuo feedback:", 
                                    placeholder="Descrivi la tua esperienza, suggerimenti o problemi...")
        
        contact_email = st.text_input("Email (opzionale):", 
                                     placeholder="per eventuali follow-up")
        
        submitted = st.form_submit_button("📤 Invia Feedback")
        
        if submitted:
            if feedback_text.strip():
                # Track comment submission
                if ANALYTICS_AVAILABLE:
                    analytics = get_analytics()
                    analytics.track_comment_submission(
                        comment_type=feedback_type.lower().replace(' ', '_'),
                        rating=rating
                    )
                    
                    # Track additional feedback metrics
                    analytics.track_event('feedback_detailed', {
                        'feedback_type': feedback_type,
                        'user_type': user_type,
                        'rating': rating,
                        'would_recommend': would_recommend,
                        'has_contact': bool(contact_email.strip()),
                        'text_length': len(feedback_text)
                    })
                
                st.success("✅ Grazie per il tuo feedback! È stato registrato con successo.")
                
                # Display summary
                st.markdown("#### 📊 Riepilogo Feedback")
                feedback_summary = pd.DataFrame({
                    'Campo': ['Tipo', 'Valutazione', 'Utente', 'Raccomandazione', 'Contatto'],
                    'Valore': [feedback_type, f"{rating}/5 ⭐", user_type, would_recommend, 
                              '✅' if contact_email.strip() else '❌']
                })
                st.dataframe(feedback_summary, use_container_width=True)
            else:
                st.warning("⚠️ Per favore, inserisci il tuo feedback prima di inviare.")
    
    # Recent feedback stats (mock)
    st.markdown("---")
    st.markdown("### 📈 Statistiche Feedback Recenti")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 Feedback Totali", np.random.randint(45, 120), delta=f"+{np.random.randint(2, 8)}")
    with col2:
        st.metric("⭐ Rating Medio", f"{np.random.uniform(3.8, 4.7):.1f}/5", delta=f"+{np.random.uniform(0.1, 0.3):.1f}")
    with col3:
        st.metric("👍 Raccomandazioni", f"{np.random.randint(75, 95)}%", delta=f"+{np.random.randint(2, 8)}%")
    with col4:
        st.metric("🐛 Bug Reports", np.random.randint(3, 12), delta=f"-{np.random.randint(1, 4)}")

def render_engagement_page():
    """Renders engaged visitors page for admin users only."""
    user = SessionManager.get_current_user()
    
    # Check admin access
    if not user or user.role != UserRole.ADMIN:
        st.error("❌ Accesso negato. Solo amministratori possono visualizzare il dashboard engagement.")
        return
    
    if ENGAGEMENT_TRACKER_AVAILABLE:
        render_engaged_visitors_dashboard()
    else:
        st.error("⚠️ Modulo Engaged Visitors Dashboard non disponibile.")

def render_footer():
    """Application footer."""
    st.markdown("""
    <div class="footer">
        <p>© 2025 Nino Medical AI - Sviluppato da Antonino Piacenza</p>
        <p>🔬 Versione 2.0 Pro | 📧 ninomedical.ai@gmail.com | 🌐 antonino-piacenza-portfolio.streamlit.app</p>
        <p><em>Software per ricerca e dimostrazione. Non per uso clinico diretto.</em></p>
    </div>
    """, unsafe_allow_html=True)

# --- Entry Point ---
if __name__ == "__main__":
    main()
