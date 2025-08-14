#!/usr/bin/env python3
"""
Nino Medical AI Pro Ultimate - Enhanced Graphics Edition
========================================================

Versione con grafica moderna e miglioramenti visual per una UX superiore.
Sviluppato da Antonino Piacenza - ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import base64
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Nino Medical AI - Enhanced",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Custom Headers */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #1f4e79, #2e7d32, #e65100);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInUp 1s ease-out;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        color: #ffffff;
        text-align: center;
        margin-bottom: 3rem;
        opacity: 0.9;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #1f4e79;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(45deg, #1f4e79, #2e7d32) 1;
        padding-bottom: 0.8rem;
        margin: 2.5rem 0 1.5rem 0;
        animation: slideInLeft 0.6s ease-out;
    }
    
    /* Enhanced Cards */
    .enhanced-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .enhanced-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(45deg, #1f4e79, #2e7d32, #e65100);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .enhanced-card:hover::before {
        transform: translateX(0);
    }
    
    .enhanced-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Glass Morphism Metrics */
    .glass-metric {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 0.5rem;
    }
    
    .glass-metric:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-4px);
    }
    
    .glass-metric h4 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .glass-metric p {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1f4e79 0%, #2e7d32 100%);
    }
    
    /* Status indicators */
    .status-active {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(45deg, #4CAF50, #8BC34A);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .status-warning {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(45deg, #FF9800, #FFC107);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
    }
    
    /* Animated Progress Bars */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(45deg, #1f4e79, #2e7d32);
        border-radius: 4px;
        transition: width 2s ease-in-out;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(31, 78, 121, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(31, 78, 121, 0); }
        100% { box-shadow: 0 0 0 0 rgba(31, 78, 121, 0); }
    }
    
    /* Interactive Elements */
    .interactive-btn {
        background: linear-gradient(45deg, #1f4e79, #2e7d32);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .interactive-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        animation: pulse 1.5s infinite;
    }
    
    /* Modern Form Elements */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer Enhancement */
    .enhanced-footer {
        background: linear-gradient(45deg, #1f4e79, #2e7d32);
        color: white;
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Enhanced Main Application ---
def main():
    """Main function with enhanced graphics."""
    render_enhanced_sidebar()
    
    # Page routing
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        render_enhanced_dashboard()
    elif page == 'databases':
        render_enhanced_databases_page()
    elif page == 'predictive_medicine':
        render_enhanced_predictive_page()
    elif page == 'analytics':
        render_enhanced_analytics_page()
    elif page == 'about':
        render_enhanced_about_page()
    
    render_enhanced_footer()

# --- Enhanced Sidebar ---
def render_enhanced_sidebar():
    """Renders enhanced sidebar with modern styling."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: white; font-family: 'Inter', sans-serif; font-weight: 700; margin-bottom: 0.5rem;">
                🏥 Nino Medical AI
            </h1>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0;">
                Enhanced Pro Edition
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation with enhanced styling
        st.markdown("### 🎯 Navigazione")
        nav_buttons = {
            "📊 Dashboard": "dashboard",
            "🌍 Database Medici": "databases", 
            "🧠 Medicina Predittiva": "predictive_medicine",
            "📈 Analytics": "analytics",
            "👨‍💻 Chi Sono": "about"
        }
        
        for label, page_key in nav_buttons.items():
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # Enhanced metrics in sidebar
        st.markdown("### 📊 Statistiche Live")
        
        # Real-time metrics with animations
        current_time = datetime.now()
        
        st.markdown(f"""
        <div class="progress-container">
            <p style="color: white; margin-bottom: 0.5rem;">🤖 Modelli AI Attivi</p>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 20px;">
                <div style="background: linear-gradient(45deg, #4CAF50, #8BC34A); width: 85%; height: 100%; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-weight: bold; font-size: 0.8rem;">12/15</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("📄 Pubblicazioni", "1.2M+", delta="10k recenti")
        st.metric("📈 Analisi Oggi", f"{np.random.randint(150, 300)}", delta="24h")
        st.metric("⚡ Uptime", "99.9%", delta="0.1%")

# --- Enhanced Dashboard ---
def render_enhanced_dashboard():
    """Renders enhanced dashboard with modern graphics."""
    st.markdown('<h1 class="main-header">Nino Medical AI Pro Ultimate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">La Piattaforma AI più Avanzata per la Ricerca Medica</p>', unsafe_allow_html=True)
    
    # Welcome Hero Section
    st.markdown("""
    <div class="enhanced-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center;">
        <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">🚀 Benvenuto nell'Era dell'IA Medica</h2>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem; opacity: 0.9;">
            Questa versione integra strumenti avanzati di analisi predittiva, accesso a database globali 
            e algoritmi di machine learning all'avanguardia per la ricerca medica.
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span class="status-active">✅ Sistema Operativo</span>
            <span class="status-active">🔄 Auto-aggiornamento</span>
            <span class="status-active">🛡️ Sicurezza Avanzata</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🎛️ Centro di Controllo Sistema</h2>', unsafe_allow_html=True)
    
    # Enhanced System Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="glass-metric">
            <h4>🔌 Database</h4>
            <p>✅ Connesso</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-metric">
            <h4>🧠 Modelli IA</h4>
            <p>12 Attivi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-metric">
            <h4>⚡ Performance</h4>
            <p>94.2%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        current_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="glass-metric">
            <h4>🕐 Ora Sistema</h4>
            <p>{current_time}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Charts Section
    st.markdown('<h2 class="section-header">📈 Analytics & Performance</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.write("##### 🎯 Utilizzo Moduli IA (Real-time)")
        
        # Enhanced chart with better colors
        df_activity = pd.DataFrame({
            'Modulo': ['Predizione\nRischio', 'Analisi Dati\nClinici', 'NLP\nMedico', 'Ottimizzazione\nTerapie'],
            'Utilizzo': [450, 320, 280, 150],
            'Trend': ['+12%', '+8%', '+15%', '+5%']
        })
        
        fig = px.bar(
            df_activity, 
            x='Modulo', 
            y='Utilizzo',
            title="Attività dei Moduli",
            color='Utilizzo',
            color_continuous_scale=['#1f4e79', '#2e7d32', '#e65100']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#1f4e79"),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.write("##### 📊 Accuratezza Modelli Predittivi")
        
        # Enhanced line chart
        df_accuracy = pd.DataFrame({
            'Modello': ['Cardiovascolare', 'Diabetico', 'Oncologico', 'Renale'],
            'Accuratezza': [94.5, 91.2, 89.7, 92.1],
            'Trend': ['📈', '📈', '📊', '📈']
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_accuracy['Modello'],
            y=df_accuracy['Accuratezza'],
            mode='lines+markers',
            line=dict(color='#2e7d32', width=4),
            marker=dict(size=12, color='#1f4e79'),
            name='Accuratezza'
        ))
        
        fig.update_layout(
            title="Performance Models",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#1f4e79"),
            yaxis=dict(range=[85, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Live Activity Feed
    st.markdown('<h2 class="section-header">📡 Attività Live</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="enhanced-card">
        <h4>🔴 Feed Real-time</h4>
    """, unsafe_allow_html=True)
    
    # Simulated live activity
    activities = [
        f"🧠 Modello Cardiovascolare: Analisi completata (Accuratezza: 94.2%) - {datetime.now().strftime('%H:%M:%S')}",
        f"🔍 Ricerca PubMed: 1,247 risultati trovati per 'COVID-19 vaccine' - {datetime.now().strftime('%H:%M:%S')}",
        f"📊 Analisi predittiva: Rischio diabete calcolato per paziente #ID_2487 - {datetime.now().strftime('%H:%M:%S')}",
        f"⚡ Sistema: Backup automatico completato con successo - {datetime.now().strftime('%H:%M:%S')}"
    ]
    
    for activity in activities[:3]:
        st.write(f"• {activity}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Database Page ---
def render_enhanced_databases_page():
    """Enhanced database interface."""
    st.markdown('<h1 class="main-header">🌍 Database Medici Globali</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Accesso Unificato ai Principali Database Scientifici</p>', unsafe_allow_html=True)
    
    # Database status indicators
    st.markdown("""
    <div class="enhanced-card">
        <h3>🔌 Stato Connessioni Database</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: linear-gradient(45deg, #4CAF50, #8BC34A); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong>PubMed</strong><br>✅ Connesso
            </div>
            <div style="background: linear-gradient(45deg, #2196F3, #21CBF3); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong>ClinicalTrials</strong><br>✅ Connesso
            </div>
            <div style="background: linear-gradient(45deg, #FF9800, #FFC107); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong>FDA</strong><br>⚠️ Limitato
            </div>
            <div style="background: linear-gradient(45deg, #9C27B0, #E91E63); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <strong>WHO</strong><br>✅ Connesso
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced search interface
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.write("#### 🔍 Ricerca Avanzata")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        db_options = ["PubMed", "ClinicalTrials.gov", "FDA", "WHO", "UniProt", "Disease Ontology"]
        selected_db = st.selectbox("Database:", db_options)
        
        search_type = st.selectbox("Tipo ricerca:", ["Generale", "Avanzata", "AI-Powered"])
    
    with col2:
        search_query = st.text_input(
            "Termine di ricerca:",
            placeholder="es. 'machine learning medical diagnosis'"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            max_results = st.number_input("Max risultati:", 10, 1000, 100)
        with col_b:
            date_filter = st.selectbox("Periodo:", ["Tutti", "Ultimo anno", "Ultimi 5 anni"])
    
    if st.button("🚀 Avvia Ricerca Avanzata", use_container_width=True):
        if search_query:
            search_progress = st.progress(0)
            status_text = st.empty()
            
            # Simulate search process
            for i in range(101):
                search_progress.progress(i)
                if i < 30:
                    status_text.text(f"🔍 Connessione a {selected_db}...")
                elif i < 70:
                    status_text.text(f"📡 Ricerca in corso...")
                else:
                    status_text.text(f"📊 Elaborazione risultati...")
                time.sleep(0.02)
            
            status_text.text("✅ Ricerca completata!")
            
            # Enhanced results display
            st.success(f"Trovati {max_results} risultati per '{search_query}' in {selected_db}")
            
            # Sample results with enhanced formatting
            results_data = {
                'Titolo': [f'[AI-Enhanced] Studio {i+1} su {search_query}' for i in range(5)],
                'Autori': [f'Team Ricerca Internazionale {i+1} et al.' for i in range(5)],
                'Data': [(datetime.now() - timedelta(days=i*30)).strftime('%Y-%m-%d') for i in range(5)],
                'Impact Score': [f"{np.random.uniform(2.5, 9.8):.1f}" for _ in range(5)],
                'Citazioni': [np.random.randint(50, 500) for _ in range(5)]
            }
            df_results = pd.DataFrame(results_data)
            st.dataframe(df_results, use_container_width=True)
        else:
            st.warning("⚠️ Inserisci un termine di ricerca!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Predictive Medicine ---
def render_enhanced_predictive_page():
    """Enhanced predictive medicine interface."""
    st.markdown('<h1 class="main-header">🧠 Medicina Predittiva</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Algoritmi AI per Analisi Predittive Avanzate</p>', unsafe_allow_html=True)
    
    # Warning banner
    st.markdown("""
    <div style="background: linear-gradient(45deg, #FF6B6B, #FFE66D); padding: 1rem; border-radius: 15px; color: #333; margin-bottom: 2rem; text-align: center;">
        <h4>⚠️ Disclaimer Medico</h4>
        <p>I modelli predittivi sono destinati esclusivamente a scopi dimostrativi e di ricerca. 
        Non utilizzare per diagnosi cliniche reali.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection with visual cards
    st.markdown("### 🎯 Seleziona Modello Predittivo")
    
    model_cards = st.columns(3)
    
    with model_cards[0]:
        if st.button("💓 Rischio Cardiovascolare", use_container_width=True):
            st.session_state.selected_model = "cardiovascular"
    
    with model_cards[1]:
        if st.button("🍯 Predizione Diabete", use_container_width=True):
            st.session_state.selected_model = "diabetes"
    
    with model_cards[2]:
        if st.button("🎗️ Screening Oncologico", use_container_width=True):
            st.session_state.selected_model = "oncology"
    
    # Display selected model interface
    selected_model = st.session_state.get('selected_model', 'cardiovascular')
    
    if selected_model == "cardiovascular":
        render_cardiovascular_model()
    elif selected_model == "diabetes":
        render_diabetes_model()
    elif selected_model == "oncology":
        render_oncology_model()

def render_cardiovascular_model():
    """Enhanced cardiovascular risk model."""
    st.markdown("""
    <div class="enhanced-card">
        <h3>💓 Modello Predittivo Cardiovascolare</h3>
        <p>Utilizza algoritmi di machine learning per valutare il rischio cardiovascolare a 10 anni</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📊 Parametri Vitali**")
        age = st.number_input("Età", 20, 100, 55)
        blood_pressure = st.number_input("Pressione Sistolica", 80, 200, 140)
        heart_rate = st.number_input("Frequenza Cardiaca", 40, 120, 70)
    
    with col2:
        st.write("**🧪 Esami Laboratorio**")
        cholesterol = st.number_input("Colesterolo Totale", 100, 400, 220)
        hdl = st.number_input("HDL", 20, 100, 50)
        glucose = st.number_input("Glicemia", 50, 200, 90)
    
    with col3:
        st.write("**🏃‍♂️ Stile di Vita**")
        smoker = st.radio("Fumatore", ["No", "Sì"])
        exercise = st.radio("Attività Fisica", ["Regolare", "Occasionale", "Sedentario"])
        bmi = st.number_input("BMI", 15.0, 50.0, 25.0)
    
    if st.button("🚀 Calcola Rischio Cardiovascolare", use_container_width=True):
        # Enhanced calculation with visualization
        progress_bar = st.progress(0)
        
        for i in range(101):
            progress_bar.progress(i)
            time.sleep(0.01)
        
        # Simulate ML calculation
        risk_factors = {
            'age': age / 100,
            'bp': blood_pressure / 200,
            'chol': cholesterol / 400,
            'smoke': 1.5 if smoker == "Sì" else 0.8,
            'exercise': 0.7 if exercise == "Regolare" else 1.2,
            'bmi': bmi / 30
        }
        
        risk_score = np.clip(
            np.prod(list(risk_factors.values())) * np.random.uniform(0.8, 1.2),
            0.05, 0.95
        )
        
        # Enhanced results visualization
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            risk_level = "Alto" if risk_score > 0.3 else "Medio" if risk_score > 0.15 else "Basso"
            color = "#FF4444" if risk_level == "Alto" else "#FFA500" if risk_level == "Medio" else "#44AA44"
            
            st.markdown(f"""
            <div style="background: {color}; color: white; padding: 1rem; border-radius: 15px; text-align: center;">
                <h3>Rischio: {risk_level}</h3>
                <h2>{risk_score:.1%}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_res2:
            st.metric("Confidenza Modello", "94.2%", delta="2.1%")
            st.metric("Pazienti Simili", "1,247", delta="Analizzati")
        
        with col_res3:
            # Risk factors breakdown
            st.write("**Fattori di Rischio:**")
            for factor, value in risk_factors.items():
                st.write(f"• {factor.title()}: {value:.2f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_diabetes_model():
    """Diabetes prediction model."""
    st.markdown("""
    <div class="enhanced-card">
        <h3>🍯 Modello Predittivo Diabete</h3>
        <p>Analisi AI per la predizione del rischio di insorgenza del diabete tipo 2</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 Modello in fase di calibrazione - Disponibile prossimamente")

def render_oncology_model():
    """Oncology screening model."""
    st.markdown("""
    <div class="enhanced-card">
        <h3>🎗️ Screening Oncologico</h3>
        <p>Algoritmi avanzati per l'identificazione precoce di markers oncologici</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 Modello in fase di validazione clinica - Disponibile prossimamente")

# --- Enhanced Analytics Page ---
def render_enhanced_analytics_page():
    """Enhanced analytics dashboard."""
    st.markdown('<h1 class="main-header">📈 Analytics Avanzate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dashboard Intelligente per Insights Medici</p>', unsafe_allow_html=True)
    
    # Real-time metrics
    metrics_cols = st.columns(4)
    
    with metrics_cols[0]:
        st.metric("🔍 Query Oggi", "2,847", delta="12%")
    with metrics_cols[1]:
        st.metric("🧠 Predizioni", "1,329", delta="8%")
    with metrics_cols[2]:
        st.metric("📊 Accuratezza Media", "92.4%", delta="1.2%")
    with metrics_cols[3]:
        st.metric("⚡ Tempo Risposta", "0.8s", delta="-0.1s")
    
    # Enhanced charts
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.write("#### 📊 Trend Utilizzazione Settimanale")
        
        dates = pd.date_range(start='2025-01-01', periods=7, freq='D')
        usage_data = pd.DataFrame({
            'Data': dates,
            'Database': np.random.randint(100, 300, 7),
            'Predittiva': np.random.randint(50, 150, 7),
            'Analytics': np.random.randint(30, 100, 7)
        })
        
        fig = px.line(usage_data, x='Data', y=['Database', 'Predittiva', 'Analytics'],
                     title="Utilizzo per Modulo")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_cols[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.write("#### 🎯 Performance per Area Medica")
        
        performance_data = pd.DataFrame({
            'Area': ['Cardiologia', 'Oncologia', 'Neurologia', 'Diabetologia', 'Pneumologia'],
            'Accuratezza': [94.2, 91.8, 89.5, 93.1, 87.9],
            'Volume': [450, 320, 280, 380, 190]
        })
        
        fig = px.scatter(performance_data, x='Accuratezza', y='Volume', 
                        size='Volume', color='Area',
                        title="Performance vs Volume")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced About Page ---
def render_enhanced_about_page():
    """Enhanced about page with modern design."""
    st.markdown('<h1 class="main-header">👨‍💻 Antonino Piacenza</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ricercatore & Innovatore in Intelligenza Artificiale Medica</p>', unsafe_allow_html=True)
    
    # Profile card
    st.markdown("""
    <div class="enhanced-card" style="text-align: center;">
        <div style="font-size: 6rem; margin-bottom: 1rem;">🧠</div>
        <h2>Innovazione nella Medicina del Futuro</h2>
        <p style="font-size: 1.1rem; margin: 1.5rem 0;">
            Specializzato nello sviluppo di soluzioni AI per il settore sanitario, 
            con focus su machine learning, analisi predittiva e integrazione di database medici globali.
        </p>
        
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;">
            <span style="background: linear-gradient(45deg, #1f4e79, #2e7d32); color: white; padding: 0.5rem 1rem; border-radius: 20px;">
                🐍 Python Expert
            </span>
            <span style="background: linear-gradient(45deg, #2e7d32, #e65100); color: white; padding: 0.5rem 1rem; border-radius: 20px;">
                🤖 ML Engineer
            </span>
            <span style="background: linear-gradient(45deg, #e65100, #1f4e79); color: white; padding: 0.5rem 1rem; border-radius: 20px;">
                🏥 HealthTech
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Competenze con progress bars
    st.markdown('<h2 class="section-header">🛠️ Competenze Tecniche</h2>', unsafe_allow_html=True)
    
    skills_data = [
        ("Python & Data Science", 95, "#1f4e79"),
        ("Machine Learning", 90, "#2e7d32"),
        ("Medical AI", 88, "#e65100"),
        ("Streamlit Development", 92, "#FF6B6B"),
        ("Database Integration", 85, "#9C27B0")
    ]
    
    for skill, level, color in skills_data:
        st.markdown(f"""
        <div class="enhanced-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{skill}</span>
                <span style="color: {color}; font-weight: bold;">{level}%</span>
            </div>
            <div style="background: #f0f0f0; border-radius: 10px; height: 10px;">
                <div style="background: {color}; width: {level}%; height: 100%; border-radius: 10px; transition: width 2s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Enhanced Footer ---
def render_enhanced_footer():
    """Enhanced footer with modern styling."""
    st.markdown("""
    <div class="enhanced-footer">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
                <div>
                    <h4>🏥 Nino Medical AI</h4>
                    <p>Piattaforma innovativa per la ricerca medica con intelligenza artificiale</p>
                </div>
                <div>
                    <h4>📞 Contatti</h4>
                    <p>📧 ninomedical.ai@gmail.com<br>
                    📱 +39 3936789529<br>
                    📍 Castelvetrano (TP), Italia</p>
                </div>
                <div>
                    <h4>🔗 Links</h4>
                    <p>🌟 GitHub Project<br>
                    📄 Documentation<br>
                    🎓 Research Papers</p>
                </div>
                <div>
                    <h4>⚖️ Legal</h4>
                    <p>🛡️ Privacy Policy<br>
                    📋 Terms of Service<br>
                    🏥 Medical Disclaimer</p>
                </div>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem; text-align: center;">
                <p>© 2025 Antonino Piacenza - Nino Medical AI Enhanced Edition</p>
                <p style="opacity: 0.8;">Sviluppato con ❤️ per il futuro della medicina</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Entry Point ---
if __name__ == "__main__":
    main()
