#!/usr/bin/env python3
"""
Nino Medical AI - Enhanced Graphics (Compatible Version)
========================================================

Versione grafica migliorata compatibile con versioni più vecchie di Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Background */
    .main > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* Enhanced Headers */
    .main-title {
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
    
    .sub-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        color: #ffffff;
        text-align: center;
        margin-bottom: 3rem;
        opacity: 0.9;
    }
    
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #1f4e79;
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 0.8rem;
        margin: 2rem 0 1.5rem 0;
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
        transition: all 0.4s ease;
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
        color: white;
    }
    
    .glass-metric:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-4px);
    }
    
    /* Status Badges */
    .status-active {
        display: inline-block;
        background: linear-gradient(45deg, #4CAF50, #8BC34A);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .status-warning {
        display: inline-block;
        background: linear-gradient(45deg, #FF9800, #FFC107);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.2rem;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
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
    
    /* Chart Enhancement */
    .plotly-graph-div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Footer */
    .enhanced-footer {
        background: linear-gradient(45deg, #1f4e79, #2e7d32);
        color: white;
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(180deg, #1f4e79, #2e7d32); border-radius: 15px; margin-bottom: 1rem;">
            <h2 style="color: white; margin: 0;">🏥 Nino Medical AI</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">Enhanced Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Navigazione")
        
        # Navigation buttons
        if st.button("📊 Dashboard", key="nav_dashboard"):
            st.session_state.current_page = "dashboard"
        if st.button("🌍 Database Medici", key="nav_databases"):
            st.session_state.current_page = "databases"
        if st.button("🧠 Medicina Predittiva", key="nav_predictive"):
            st.session_state.current_page = "predictive"
        if st.button("📈 Analytics", key="nav_analytics"):
            st.session_state.current_page = "analytics"
        if st.button("👨‍💻 Chi Sono", key="nav_about"):
            st.session_state.current_page = "about"
        
        st.markdown("---")
        st.markdown("### 📊 Statistiche Live")
        
        # Live metrics
        st.markdown("""
        <div class="glass-metric">
            <h4>🤖 Modelli AI</h4>
            <h3>12/15 Attivi</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("📄 Pubblicazioni", "1.2M+", delta="10k")
        st.metric("📈 Analisi Oggi", f"{np.random.randint(150, 300)}")
        st.metric("⚡ Uptime", "99.9%", delta="0.1%")
    
    # Main content routing
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        render_dashboard()
    elif page == 'databases':
        render_databases()
    elif page == 'predictive':
        render_predictive()
    elif page == 'analytics':
        render_analytics()
    elif page == 'about':
        render_about()

def render_dashboard():
    """Enhanced Dashboard."""
    st.markdown('<h1 class="main-title">Nino Medical AI Pro Ultimate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">La Piattaforma AI più Avanzata per la Ricerca Medica</p>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="enhanced-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center;">
        <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">🚀 Benvenuto nell'Era dell'IA Medica</h2>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
            Questa versione integra strumenti avanzati di analisi predittiva, accesso a database globali 
            e algoritmi di machine learning all'avanguardia per la ricerca medica.
        </p>
        <div style="text-align: center;">
            <span class="status-active">✅ Sistema Operativo</span>
            <span class="status-active">🔄 Auto-aggiornamento</span>
            <span class="status-active">🛡️ Sicurezza Avanzata</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">🎛️ Centro di Controllo Sistema</h2>', unsafe_allow_html=True)
    
    # System Metrics
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
    
    st.markdown('<h2 class="section-title">📈 Analytics & Performance</h2>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("##### 🎯 Utilizzo Moduli IA (Real-time)")
        df_activity = pd.DataFrame({
            'Modulo': ['Predizione\nRischio', 'Analisi Dati\nClinici', 'NLP\nMedico', 'Ottimizzazione\nTerapie'],
            'Utilizzo': [450, 320, 280, 150]
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
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("##### 📊 Accuratezza Modelli Predittivi")
        df_accuracy = pd.DataFrame({
            'Modello': ['Cardiovascolare', 'Diabetico', 'Oncologico', 'Renale'],
            'Accuratezza': [94.5, 91.2, 89.7, 92.1]
        })
        
        fig = px.line(
            df_accuracy, 
            x='Modello', 
            y='Accuratezza',
            title="Performance Models",
            markers=True
        )
        fig.update_traces(line_color='#2e7d32', marker_color='#1f4e79', marker_size=12)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(range=[85, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Live Activity Feed
    st.markdown('<h2 class="section-title">📡 Attività Live</h2>', unsafe_allow_html=True)
    
    activities = [
        f"🧠 Modello Cardiovascolare: Analisi completata (Accuratezza: 94.2%) - {datetime.now().strftime('%H:%M:%S')}",
        f"🔍 Ricerca PubMed: 1,247 risultati trovati per 'COVID-19 vaccine' - {datetime.now().strftime('%H:%M:%S')}",
        f"📊 Analisi predittiva: Rischio diabete calcolato - {datetime.now().strftime('%H:%M:%S')}"
    ]
    
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.write("#### 🔴 Feed Real-time")
    for activity in activities:
        st.write(f"• {activity}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_databases():
    """Enhanced Database Interface."""
    st.markdown('<h1 class="main-title">🌍 Database Medici Globali</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Accesso Unificato ai Principali Database Scientifici</p>', unsafe_allow_html=True)
    
    # Database Status
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
    
    # Search Interface
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.write("#### 🔍 Ricerca Avanzata")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        db_options = ["PubMed", "ClinicalTrials.gov", "FDA", "WHO", "UniProt", "Disease Ontology"]
        selected_db = st.selectbox("Database:", db_options)
        search_type = st.selectbox("Tipo ricerca:", ["Generale", "Avanzata", "AI-Powered"])
    
    with col2:
        search_query = st.text_input("Termine di ricerca:", placeholder="es. 'machine learning medical diagnosis'")
        col_a, col_b = st.columns(2)
        with col_a:
            max_results = st.number_input("Max risultati:", 10, 1000, 100)
        with col_b:
            date_filter = st.selectbox("Periodo:", ["Tutti", "Ultimo anno", "Ultimi 5 anni"])
    
    if st.button("🚀 Avvia Ricerca Avanzata"):
        if search_query:
            # Progress simulation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(101):
                progress_bar.progress(i)
                if i < 30:
                    status_text.text(f"🔍 Connessione a {selected_db}...")
                elif i < 70:
                    status_text.text("📡 Ricerca in corso...")
                else:
                    status_text.text("📊 Elaborazione risultati...")
                time.sleep(0.01)
            
            status_text.text("✅ Ricerca completata!")
            st.success(f"Trovati {max_results} risultati per '{search_query}' in {selected_db}")
            
            # Sample results
            results_data = {
                'Titolo': [f'[AI-Enhanced] Studio {i+1} su {search_query}' for i in range(5)],
                'Autori': [f'Team Ricerca {i+1} et al.' for i in range(5)],
                'Data': [(datetime.now() - timedelta(days=i*30)).strftime('%Y-%m-%d') for i in range(5)],
                'Impact Score': [f"{np.random.uniform(2.5, 9.8):.1f}" for _ in range(5)],
                'Citazioni': [np.random.randint(50, 500) for _ in range(5)]
            }
            df_results = pd.DataFrame(results_data)
            st.dataframe(df_results)
        else:
            st.warning("⚠️ Inserisci un termine di ricerca!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_predictive():
    """Enhanced Predictive Medicine."""
    st.markdown('<h1 class="main-title">🧠 Medicina Predittiva</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Algoritmi AI per Analisi Predittive Avanzate</p>', unsafe_allow_html=True)
    
    # Warning
    st.markdown("""
    <div style="background: linear-gradient(45deg, #FF6B6B, #FFE66D); padding: 1rem; border-radius: 15px; color: #333; margin-bottom: 2rem; text-align: center;">
        <h4>⚠️ Disclaimer Medico</h4>
        <p>I modelli predittivi sono destinati esclusivamente a scopi dimostrativi e di ricerca. 
        Non utilizzare per diagnosi cliniche reali.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Selection
    st.markdown("### 🎯 Seleziona Modello Predittivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💓 Rischio Cardiovascolare"):
            st.session_state.selected_model = "cardiovascular"
    
    with col2:
        if st.button("🍯 Predizione Diabete"):
            st.session_state.selected_model = "diabetes"
    
    with col3:
        if st.button("🎗️ Screening Oncologico"):
            st.session_state.selected_model = "oncology"
    
    # Model Interface
    selected_model = st.session_state.get('selected_model', 'cardiovascular')
    
    if selected_model == "cardiovascular":
        render_cardiovascular_model()
    else:
        st.info("🚧 Modello in fase di sviluppo - Disponibile prossimamente")

def render_cardiovascular_model():
    """Cardiovascular Risk Model."""
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
    
    if st.button("🚀 Calcola Rischio Cardiovascolare"):
        # Calculation with progress bar
        progress_bar = st.progress(0)
        for i in range(101):
            progress_bar.progress(i)
            time.sleep(0.01)
        
        # Risk calculation
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
        
        # Results
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
            st.write("**Fattori di Rischio:**")
            for factor, value in risk_factors.items():
                st.write(f"• {factor.title()}: {value:.2f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    """Analytics Dashboard."""
    st.markdown('<h1 class="main-title">📈 Analytics Avanzate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Dashboard Intelligente per Insights Medici</p>', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔍 Query Oggi", "2,847", delta="12%")
    with col2:
        st.metric("🧠 Predizioni", "1,329", delta="8%")
    with col3:
        st.metric("📊 Accuratezza Media", "92.4%", delta="1.2%")
    with col4:
        st.metric("⚡ Tempo Risposta", "0.8s", delta="-0.1s")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 📊 Trend Settimanale")
        dates = pd.date_range(start='2025-01-01', periods=7, freq='D')
        usage_data = pd.DataFrame({
            'Data': dates,
            'Database': np.random.randint(100, 300, 7),
            'Predittiva': np.random.randint(50, 150, 7),
            'Analytics': np.random.randint(30, 100, 7)
        })
        
        fig = px.line(usage_data, x='Data', y=['Database', 'Predittiva', 'Analytics'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("#### 🎯 Performance per Area")
        performance_data = pd.DataFrame({
            'Area': ['Cardiologia', 'Oncologia', 'Neurologia', 'Diabetologia', 'Pneumologia'],
            'Accuratezza': [94.2, 91.8, 89.5, 93.1, 87.9],
            'Volume': [450, 320, 280, 380, 190]
        })
        
        fig = px.scatter(performance_data, x='Accuratezza', y='Volume', 
                        size='Volume', color='Area')
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def render_about():
    """About Page."""
    st.markdown('<h1 class="main-title">👨‍💻 Antonino Piacenza</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Ricercatore & Innovatore in Intelligenza Artificiale Medica</p>', unsafe_allow_html=True)
    
    # Profile
    st.markdown("""
    <div class="enhanced-card" style="text-align: center;">
        <div style="font-size: 6rem; margin-bottom: 1rem;">🧠</div>
        <h2>Innovazione nella Medicina del Futuro</h2>
        <p style="font-size: 1.1rem; margin: 1.5rem 0;">
            Specializzato nello sviluppo di soluzioni AI per il settore sanitario, 
            con focus su machine learning, analisi predittiva e integrazione di database medici globali.
        </p>
        
        <div style="text-align: center; margin-top: 2rem;">
            <span style="background: linear-gradient(45deg, #1f4e79, #2e7d32); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                🐍 Python Expert
            </span>
            <span style="background: linear-gradient(45deg, #2e7d32, #e65100); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                🤖 ML Engineer
            </span>
            <span style="background: linear-gradient(45deg, #e65100, #1f4e79); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                🏥 HealthTech
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills
    st.markdown('<h2 class="section-title">🛠️ Competenze Tecniche</h2>', unsafe_allow_html=True)
    
    skills = [
        ("Python & Data Science", 95),
        ("Machine Learning", 90),
        ("Medical AI", 88),
        ("Streamlit Development", 92),
        ("Database Integration", 85)
    ]
    
    for skill, level in skills:
        st.markdown(f"""
        <div class="enhanced-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{skill}</span>
                <span style="color: #1f4e79; font-weight: bold;">{level}%</span>
            </div>
            <div style="background: #f0f0f0; border-radius: 10px; height: 8px;">
                <div style="background: linear-gradient(45deg, #1f4e79, #2e7d32); width: {level}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
def render_footer():
    """Render footer."""
    st.markdown("""
    <div class="enhanced-footer">
        <div style="max-width: 1000px; margin: 0 auto;">
            <h4>🏥 Nino Medical AI Enhanced Edition</h4>
            <p>📧 ninomedical.ai@gmail.com | 📱 +39 3936789529 | 📍 Castelvetrano (TP), Italia</p>
            <p>© 2025 Antonino Piacenza - Sviluppato con ❤️ per il futuro della medicina</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    render_footer()
