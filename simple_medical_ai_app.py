#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nino Medical AI - Versione Semplificata
Compatibile con versioni meno recenti di Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CSS Migliorato (Inserito direttamente nel HTML) ---
def load_enhanced_css():
    """Carica CSS migliorato per una UI moderna"""
    css = """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Enhanced Headers */
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(45deg, #1f4e79, #2e7d32, #e65100);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 1rem 0;
            animation: fadeIn 2s ease-in;
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        /* Cards with Glass Effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Metric Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin: 10px;
            backdrop-filter: blur(15px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        /* Status Indicators */
        .status-active {
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin: 5px;
        }
        
        .status-warning {
            background: linear-gradient(45deg, #ff9800, #ffb74d);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin: 5px;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Button Enhancements */
        .stButton button {
            background: linear-gradient(45deg, #1f4e79, #2e7d32);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        
        /* Footer */
        .footer {
            background: linear-gradient(45deg, #1f4e79, #2e7d32);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 15px;
            margin-top: 30px;
        }
    </style>
    """
    return css

def main():
    """Funzione principale dell'app"""
    
    # Carica CSS
    st.markdown(load_enhanced_css(), unsafe_allow_html=True)
    
    # Header principale
    st.markdown('<h1 class="main-header">🏥 Nino Medical AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Piattaforma Semplificata per la Ricerca Medica</p>', unsafe_allow_html=True)
    
    # Sidebar per navigazione
    render_sidebar()
    
    # Contenuto principale
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        render_dashboard()
    elif page == 'calcoli_renali':
        render_kidney_stones()
    elif page == 'fibromialgia':
        render_fibromyalgia()
    elif page == 'databases':
        render_databases()
    elif page == 'about':
        render_about()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Nino Medical AI - Versione Semplificata</p>
        <p>Sviluppato da Antonino Piacenza per scopi dimostrativi</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renderizza la sidebar di navigazione"""
    st.sidebar.markdown("# 🏥 Menu")
    st.sidebar.markdown("---")
    
    # Bottoni di navigazione
    if st.sidebar.button("📊 Dashboard"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    if st.sidebar.button("🪨 Analisi Calcoli Renali"):
        st.session_state.current_page = 'calcoli_renali'
        st.rerun()
    
    if st.sidebar.button("🌸 Valutazione Fibromialgia"):
        st.session_state.current_page = 'fibromialgia'
        st.rerun()
    
    if st.sidebar.button("🌍 Database Medici"):
        st.session_state.current_page = 'databases'
        st.rerun()
    
    if st.sidebar.button("👨‍💻 Chi Sono"):
        st.session_state.current_page = 'about'
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statistiche")
    st.sidebar.write("🤖 Modelli: 45+")
    st.sidebar.write("📄 Pubblicazioni: 1.2M+")
    st.sidebar.write(f"⏰ Ora: {datetime.now().strftime('%H:%M')}")

def render_dashboard():
    """Renderizza la pagina dashboard"""
    
    st.markdown("""
    <div class="glass-card">
        <h2>🚀 Benvenuto nella Piattaforma Medica AI</h2>
        <p>Questa versione semplificata include strumenti essenziali per l'analisi medica e la diagnosi assistita.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metriche di sistema
    st.subheader("📊 Stato del Sistema")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Database</h4>
            <div class="status-active">ATTIVO</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Moduli IA</h4>
            <div class="status-active">12 CARICATI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Sistema</h4>
            <div class="status-active">OPERATIVO</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Grafici semplici
    st.subheader("📈 Attività Recenti")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("##### Utilizzo Moduli (Ultimi 30 giorni)")
        
        # Dati di esempio
        data = {
            'Modulo': ['Predizione Rischio', 'Analisi Clinica', 'NLP Medico', 'Terapie'],
            'Utilizzo': [450, 320, 280, 190]
        }
        df = pd.DataFrame(data)
        st.bar_chart(df.set_index('Modulo'))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("##### Accuratezza Modelli (%)")
        
        accuracy_data = {
            'Modello': ['Cardiovascolare', 'Diabetico', 'Oncologico', 'Renale'],
            'Accuratezza': [94.5, 91.2, 89.7, 92.1]
        }
        df_acc = pd.DataFrame(accuracy_data)
        st.line_chart(df_acc.set_index('Modello'))
        st.markdown('</div>', unsafe_allow_html=True)

def render_kidney_stones():
    """Pagina per l'analisi dei sintomi di calcoli renali"""
    
    st.markdown('<h2>🪨 Analisi Sintomi Calcoli Renali</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <p><strong>⚠️ Disclaimer:</strong> Questo strumento è solo a scopo educativo. 
        Non sostituisce il consulto medico professionale.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Inserisci i Sintomi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sintomi Dolorifici:**")
        flank_pain = st.slider("Dolore al fianco (0-10)", 0, 10, 0)
        abdominal_pain = st.slider("Dolore addominale (0-10)", 0, 10, 0)
        back_pain = st.slider("Dolore lombare (0-10)", 0, 10, 0)
        
        st.markdown("**Sintomi Urinari:**")
        hematuria = st.selectbox("Sangue nelle urine", ["Assente", "Presente"])
        burning = st.selectbox("Bruciore urinario", ["Assente", "Lieve", "Moderato", "Grave"])
    
    with col2:
        st.markdown("**Sintomi Sistemici:**")
        nausea = st.selectbox("Nausea", ["Assente", "Lieve", "Moderata", "Grave"])
        vomiting = st.selectbox("Vomito", ["Assente", "Presente"])
        fever = st.number_input("Temperatura (°C)", 35.0, 42.0, 36.5, 0.1)
        
        st.markdown("**Storia Clinica:**")
        previous_stones = st.selectbox("Calcoli precedenti", ["No", "Sì"])
        family_history = st.selectbox("Familiarità", ["No", "Sì"])
    
    if st.button("🔍 Analizza Sintomi", key="analyze_stones"):
        # Calcolo semplificato del rischio
        pain_score = (flank_pain + abdominal_pain + back_pain) / 3
        hematuria_score = 3 if hematuria == "Presente" else 0
        systemic_score = {"Assente": 0, "Lieve": 1, "Moderata": 2, "Grave": 3}.get(nausea, 0)
        history_score = 2 if previous_stones == "Sì" else 0
        
        total_risk = min((pain_score * 10 + hematuria_score * 10 + systemic_score * 5 + history_score * 10), 95)
        
        st.markdown(f"""
        <div class="glass-card">
            <h3>📊 Risultati Analisi</h3>
            <p><strong>Probabilità Calcoli Renali:</strong> {total_risk:.1f}%</p>
            <p><strong>Livello:</strong> {'Alto' if total_risk > 70 else 'Medio' if total_risk > 40 else 'Basso'}</p>
            <p><strong>Raccomandazione:</strong> {'Consulto urgente' if total_risk > 80 else 'Consulto medico' if total_risk > 50 else 'Monitoraggio'}</p>
        </div>
        """, unsafe_allow_html=True)

def render_fibromyalgia():
    """Pagina per la valutazione della fibromialgia"""
    
    st.markdown('<h2>🌸 Valutazione Fibromialgia</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <p><strong>ℹ️ Info:</strong> Valutazione basata sui criteri ACR (American College of Rheumatology).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Widespread Pain Index (WPI)")
    st.write("Seleziona le aree dove hai dolore:")
    
    # Aree di dolore
    col1, col2, col3 = st.columns(3)
    
    pain_areas = {}
    with col1:
        st.markdown("**Lato Sinistro:**")
        pain_areas['shoulder_l'] = st.checkbox("Spalla sinistra")
        pain_areas['arm_l'] = st.checkbox("Braccio sinistro")
        pain_areas['hip_l'] = st.checkbox("Anca sinistra")
        pain_areas['leg_l'] = st.checkbox("Gamba sinistra")
    
    with col2:
        st.markdown("**Lato Destro:**")
        pain_areas['shoulder_r'] = st.checkbox("Spalla destra")
        pain_areas['arm_r'] = st.checkbox("Braccio destro")
        pain_areas['hip_r'] = st.checkbox("Anca destra")
        pain_areas['leg_r'] = st.checkbox("Gamba destra")
    
    with col3:
        st.markdown("**Area Centrale:**")
        pain_areas['neck'] = st.checkbox("Collo")
        pain_areas['chest'] = st.checkbox("Torace")
        pain_areas['upper_back'] = st.checkbox("Dorso superiore")
        pain_areas['lower_back'] = st.checkbox("Dorso inferiore")
    
    # Symptom Severity Scale
    st.subheader("Symptom Severity Scale (SSS)")
    
    col1, col2 = st.columns(2)
    with col1:
        fatigue = st.selectbox("Affaticamento", ["Assente", "Lieve", "Moderato", "Grave"])
        sleep = st.selectbox("Problemi di sonno", ["Assenti", "Lievi", "Moderati", "Gravi"])
    
    with col2:
        cognitive = st.selectbox("Problemi cognitivi", ["Assenti", "Lievi", "Moderati", "Gravi"])
        duration = st.selectbox("Durata sintomi", ["< 3 mesi", "3-6 mesi", "> 6 mesi"])
    
    if st.button("🔬 Valuta Fibromialgia", key="analyze_fibro"):
        # Calcolo WPI
        wpi_score = sum(pain_areas.values())
        
        # Calcolo SSS
        severity_map = {"Assente": 0, "Assenti": 0, "Lieve": 1, "Lievi": 1, 
                       "Moderato": 2, "Moderati": 2, "Grave": 3, "Gravi": 3}
        sss_score = (severity_map.get(fatigue, 0) + 
                    severity_map.get(sleep, 0) + 
                    severity_map.get(cognitive, 0))
        
        # Valutazione secondo criteri ACR
        duration_ok = duration in ["3-6 mesi", "> 6 mesi"]
        acr_positive = ((wpi_score >= 7 and sss_score >= 5) or 
                       (wpi_score >= 4 and sss_score >= 9)) and duration_ok
        
        probability = min(85 if acr_positive else max(20, (wpi_score + sss_score) * 5), 95)
        
        st.markdown(f"""
        <div class="glass-card">
            <h3>📊 Risultati Valutazione Fibromialgia</h3>
            <p><strong>WPI Score:</strong> {wpi_score}/19</p>
            <p><strong>SSS Score:</strong> {sss_score}/12</p>
            <p><strong>Criteri ACR:</strong> {'Soddisfatti' if acr_positive else 'Non soddisfatti'}</p>
            <p><strong>Probabilità:</strong> {probability:.1f}%</p>
            <p><strong>Raccomandazione:</strong> {'Consulto reumatologico' if probability > 70 else 'Monitoraggio' if probability > 40 else 'Poco probabile'}</p>
        </div>
        """, unsafe_allow_html=True)

def render_databases():
    """Pagina accesso database medici"""
    
    st.markdown('<h2>🌍 Accesso Database Medici</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <p>Interfaccia semplificata per l'accesso ai principali database medici.</p>
    </div>
    """, unsafe_allow_html=True)
    
    database = st.selectbox("Seleziona Database:", 
                          ["PubMed", "ClinicalTrials.gov", "FDA", "WHO"])
    
    query = st.text_input("Termini di ricerca:")
    
    if st.button("🔍 Cerca", key="search_db"):
        if query:
            st.success(f"Simulando ricerca di '{query}' in {database}...")
            
            # Risultati simulati
            results = {
                'Titolo': [f'Studio {i+1} su {query}' for i in range(5)],
                'Autori': [f'Team Ricerca {i+1}' for i in range(5)],
                'Anno': [2023-i for i in range(5)],
                'Rilevanza': [f'{95-i*5}%' for i in range(5)]
            }
            
            st.dataframe(pd.DataFrame(results))
        else:
            st.warning("Inserisci un termine di ricerca.")

def render_about():
    """Pagina informazioni"""
    
    st.markdown('<h2>👨‍💻 Informazioni</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3>🎯 Nino Medical AI</h3>
        <p><strong>Sviluppatore:</strong> Antonino Piacenza</p>
        <p><strong>Versione:</strong> Semplificata 1.0</p>
        <p><strong>Scopo:</strong> Dimostrativo ed educativo</p>
        
        <h4>🔧 Funzionalità:</h4>
        <ul>
            <li>Analisi sintomi calcoli renali</li>
            <li>Valutazione fibromialgia (criteri ACR)</li>
            <li>Accesso database medici (simulato)</li>
            <li>Dashboard con metriche di sistema</li>
        </ul>
        
        <h4>📧 Contatti:</h4>
        <p>Email: ninomedical.ai@gmail.com</p>
        <p>LinkedIn: linkedin.com/in/antoNinoF840</p>
        
        <p><strong>⚠️ Disclaimer:</strong> Questo software è solo per scopi dimostrativi. 
        Non utilizzare per diagnosi mediche reali.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Inizializza session state se necessario
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    main()
