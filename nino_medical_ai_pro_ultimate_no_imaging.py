
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
import base64

# --- Page Configuration ---
# st.set_page_config() rimosso per compatibilità

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Enhanced Headers */
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
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 0.8rem;
        margin: 2.5rem 0 1.5rem 0;
    }
    
    /* Enhanced Cards with Glass Morphism */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
    }
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Glass Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        color: white;
        margin: 0.5rem;
    }
    .metric-card:hover {
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
    
    /* Charts Enhancement */
    .plotly-graph-div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Enhanced Footer */
    .footer {
        background: linear-gradient(45deg, #1f4e79, #2e7d32);
        color: white;
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Application ---
def main():
    """Main function to render the Streamlit app."""
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
    elif page == 'about':
        render_about_page()
    
    render_footer()

# --- Sidebar ---
def render_sidebar():
    """Renders the navigation sidebar."""
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Nino Medical AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Pro Ultimate Edition</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🏥 Navigazione")
        nav_buttons = {
            "📊 Dashboard": "dashboard",
            "🌍 Database Medici": "databases",
            "🧠 Medicina Predittiva": "predictive_medicine",
            "🧪 Trial Clinici": "clinical_trials",
            "👨‍💻 Chi Sono": "about"
        }
        
        for label, page_key in nav_buttons.items():
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Statistiche Globali")
        st.metric("🤖 Modelli AI Addestrati", "45+", delta="5 recenti")
        st.metric("📄 Pubblicazioni Indicizzate", "1.2M+", delta="10k recenti")
        st.metric("📈 Analisi Predittive Eseguite", "250k+")

# --- Pages ---
def render_main_dashboard():
    """Renders the main dashboard page."""
    st.markdown('<h1 class="main-header">Nino Medical AI Pro Ultimate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">La Piattaforma Integrata per la Ricerca e l\'Innovazione Medica</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="card" style="background: linear-gradient(135deg, #1f4e79 0%, #2e7d32 100%); color: white; text-align: center;">'
                '<h2>🚀 Benvenuto nella versione Ultimate</h2>'
                '<p>Questa versione integra strumenti avanzati per l\'analisi di dati medici, la medicina predittiva e la gestione di trial clinici, escludendo le funzionalità di imaging per una maggiore efficienza.</p>'
                '</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">Panoramica del Sistema</h2>', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h4>Connessione Database</h4><p style="color: green; font-weight: bold;">Attiva</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>Moduli Predittivi</h4><p style="color: green; font-weight: bold;">Caricati (12)</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4>Stato Sistema</h4><p style="color: green; font-weight: bold;">Operativo</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h4>Ora Server</h4><p style="color: #1f4e79; font-weight: bold;">{datetime.now().strftime("%H:%M:%S")}</p></div>', unsafe_allow_html=True)

    # Charts
    st.markdown("### 📈 Attività Recenti e Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("##### Utilizzo Moduli IA (Ultimi 30 giorni)")
        df_activity = pd.DataFrame({
            'Modulo': ['Predizione Rischio', 'Analisi Dati Clinici', 'NLP Medico', 'Ottimizzazione Terapie'],
            'Utilizzo': [np.random.randint(100, 500) for _ in range(4)]
        })
        fig = px.bar(df_activity, x='Modulo', y='Utilizzo', title="Attività dei Moduli", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("##### Accuratezza Modelli Predittivi")
        df_accuracy = pd.DataFrame({
            'Modello': ['Cardiovascolare', 'Diabetico', 'Oncologico', 'Renale'],
            'Accuratezza': [94.5, 91.2, 89.7, 92.1]
        })
        fig = px.line(df_accuracy, x='Modello', y='Accuratezza', title="Performance dei Modelli", markers=True)
        fig.update_traces(line_color='#2e7d32')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_medical_databases_page():
    """Renders the medical databases access page."""
    st.markdown('<h2 class="section-header">🌍 Accesso ai Database Medici Globali</h2>', unsafe_allow_html=True)
    st.info("Questa sezione fornisce un'interfaccia unificata per interrogare i principali database medici senza necessità di autenticazione.")

    db_options = ["PubMed", "ClinicalTrials.gov", "FDA", "WHO", "UniProt", "Disease Ontology"]
    selected_db = st.selectbox("Seleziona il database da interrogare:", db_options)
    
    search_query = st.text_input("Inserisci il termine di ricerca (es. 'cancer therapy', 'covid-19 vaccine'):", key="db_search")
    
    if st.button("🔍 Cerca", use_container_width=True):
        if search_query:
            with st.spinner(f"Ricerca in corso su {selected_db}..."):
                # Simulazione di una ricerca API
                st.success(f"Trovati 150 risultati per '{search_query}' in {selected_db}.")
                
                # Risultati simulati
                results_data = {
                    'Titolo': [f'Studio {i+1} su {search_query}' for i in range(10)],
                    'Autori': [f'Team di Ricerca {i+1}' for i in range(10)],
                    'Data': [f'{2023-i}-01-01' for i in range(10)],
                    'DOI': [f'10.1234/journal.00{i}' for i in range(10)]
                }
                df_results = pd.DataFrame(results_data)
                st.dataframe(df_results, use_container_width=True)
        else:
            st.warning("Per favore, inserisci un termine di ricerca.")

def render_predictive_medicine_page():
    """Renders the predictive medicine tools page."""
    st.markdown('<h2 class="section-header">🧠 Medicina Predittiva</h2>', unsafe_allow_html=True)
    st.warning("I modelli in questa sezione sono a scopo dimostrativo e non devono essere usati per diagnosi reali.")

    model_type = st.selectbox(
        "Seleziona il modello predittivo:",
        ["Predizione Rischio Cardiovascolare", "Predizione Insorgenza Diabete", "Analisi Risposta a Terapia Oncologica", "Analisi Sintomi Calcoli Renali", "Valutazione Fibromialgia"]
    )
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if model_type == "Predizione Rischio Cardiovascolare":
        st.write("#### Inserisci i dati del paziente (simulati):")
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Età", 20, 100, 55)
            cholesterol = st.number_input("Colesterolo (mg/dL)", 100, 400, 220)
        with col2:
            blood_pressure = st.number_input("Pressione Sistolica (mmHg)", 80, 200, 140)
            glucose = st.number_input("Glicemia (mg/dL)", 50, 200, 90)
        with col3:
            smoker = st.radio("Fumatore", ["Sì", "No"])
            exercise = st.radio("Esercizio Fisico", ["Sì", "No"])

        if st.button("⚡ Calcola Rischio", use_container_width=True):
            with st.spinner("Analisi in corso..."):
                # Simulazione calcolo
                risk_score = (age / 100) * (cholesterol / 300) * (blood_pressure / 180) * (1.5 if smoker == "Sì" else 0.8)
                st.success("Analisi completata!")
                st.metric("Rischio Cardiovascolare a 10 anni", f"{risk_score:.2%}", delta="Alto" if risk_score > 0.3 else "Basso")
    
    elif model_type == "Analisi Sintomi Calcoli Renali":
        st.write("#### 🪨 Analisi Sintomi Calcoli Renali (Nefrolitiasi)")
        st.info("Questo strumento analizza i sintomi per valutare la probabilità di presenza di calcoli renali.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Sintomi Dolorifici:**")
            flank_pain = st.slider("Dolore al fianco (0-10)", 0, 10, 0)
            abdominal_pain = st.slider("Dolore addominale (0-10)", 0, 10, 0)
            groin_pain = st.slider("Dolore inguinale (0-10)", 0, 10, 0)
            back_pain = st.slider("Dolore lombare (0-10)", 0, 10, 0)
            
            st.markdown("**Sintomi Urinari:**")
            hematuria = st.selectbox("Presenza di sangue nelle urine", ["Assente", "Microscopica", "Macroscopica"])
            dysuria = st.selectbox("Bruciore durante la minzione", ["Assente", "Lieve", "Moderato", "Grave"])
            urinary_frequency = st.selectbox("Frequenza urinaria aumentata", ["No", "Lieve", "Moderata", "Grave"])
            
        with col2:
            st.markdown("**Sintomi Sistemici:**")
            nausea = st.selectbox("Nausea", ["Assente", "Lieve", "Moderata", "Grave"])
            vomiting = st.selectbox("Vomito", ["Assente", "Occasionale", "Frequente"])
            fever = st.number_input("Temperatura corporea (°C)", 35.0, 42.0, 36.5, 0.1)
            restlessness = st.selectbox("Agitazione/Irrequietezza", ["Assente", "Lieve", "Moderata", "Grave"])
            
            st.markdown("**Fattori di Rischio:**")
            previous_stones = st.selectbox("Storia di calcoli renali precedenti", ["No", "Sì"])
            family_history = st.selectbox("Familiarità per nefrolitiasi", ["No", "Sì"])
            dehydration = st.selectbox("Scarsa idratazione abituale", ["No", "Sì"])
            
        if st.button("🔍 Analizza Sintomi", use_container_width=True):
            with st.spinner("Analisi dei sintomi in corso..."):
                # Calcolo score basato sui sintomi
                pain_score = (flank_pain + abdominal_pain + groin_pain + back_pain) / 4
                
                # Scoring per sintomi urinari
                hematuria_score = {"Assente": 0, "Microscopica": 2, "Macroscopica": 4}[hematuria]
                dysuria_score = {"Assente": 0, "Lieve": 1, "Moderato": 2, "Grave": 3}[dysuria]
                frequency_score = {"No": 0, "Lieve": 1, "Moderata": 2, "Grave": 3}[urinary_frequency]
                
                # Scoring per sintomi sistemici
                nausea_score = {"Assente": 0, "Lieve": 1, "Moderata": 2, "Grave": 3}[nausea]
                vomiting_score = {"Assente": 0, "Occasionale": 1, "Frequente": 3}[vomiting]
                fever_score = 2 if fever > 38.0 else 0
                restless_score = {"Assente": 0, "Lieve": 1, "Moderata": 2, "Grave": 3}[restlessness]
                
                # Fattori di rischio
                risk_score = 0
                if previous_stones == "Sì": risk_score += 3
                if family_history == "Sì": risk_score += 2
                if dehydration == "Sì": risk_score += 1
                
                # Calcolo probabilità totale
                total_score = (pain_score * 3 + hematuria_score + dysuria_score + frequency_score + 
                             nausea_score + vomiting_score + fever_score + restless_score + risk_score)
                
                probability = min(total_score / 30 * 100, 95)  # Normalizzazione a percentuale
                
                st.success("Analisi completata!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Probabilità Calcoli Renali", f"{probability:.1f}%", 
                             delta="Alta" if probability > 70 else "Media" if probability > 40 else "Bassa")
                with col2:
                    urgency = "🚨 Urgente" if probability > 80 or fever > 38.5 else "⚠️ Consulenza" if probability > 50 else "📋 Monitoraggio"
                    st.metric("Livello di Urgenza", urgency)
                with col3:
                    pain_level = "Severo" if pain_score > 7 else "Moderato" if pain_score > 4 else "Lieve"
                    st.metric("Intensità Dolore", pain_level, delta=f"{pain_score:.1f}/10")
                
                # Raccomandazioni
                st.markdown("#### 💡 Raccomandazioni Cliniche:")
                recommendations = []
                
                if probability > 80:
                    recommendations.append("🏥 **Valutazione urgente in Pronto Soccorso**")
                    recommendations.append("📱 **Contattare immediatamente il medico curante**")
                elif probability > 60:
                    recommendations.append("🩺 **Consulto urologico entro 24-48 ore**")
                    recommendations.append("🧪 **Esami ematochimici e urinocoltura**")
                elif probability > 30:
                    recommendations.append("📋 **Controllo medico di routine**")
                    recommendations.append("💧 **Aumentare l'idratazione**")
                else:
                    recommendations.append("🏠 **Monitoraggio domiciliare**")
                    recommendations.append("💧 **Mantenere buona idratazione**")
                
                # Raccomandazioni specifiche per sintomi
                if hematuria != "Assente":
                    recommendations.append("🔬 **Esame microscopico delle urine urgente**")
                if fever > 38.0:
                    recommendations.append("🌡️ **Monitoraggio temperatura e possibile terapia antibiotica**")
                if pain_score > 7:
                    recommendations.append("💊 **Gestione del dolore con analgesici appropriati**")
                
                for rec in recommendations:
                    st.markdown(f"- {rec}")
                
                # Esami diagnostici suggeriti
                if probability > 50:
                    st.markdown("#### 🔬 Esami Diagnostici Suggeriti:")
                    exams = {
                        "Ecografia renale e vescicale": "Prima scelta, non invasiva",
                        "Urocultura": "Escludere infezioni delle vie urinarie",
                        "Creatinina sierica": "Valutare funzionalità renale",
                        "Calcemia e fosfatemia": "Metabolismo del calcio",
                        "Acido urico": "Valutare tipo di calcoli"
                    }
                    if probability > 70:
                        exams["TC senza contrasto"] = "Gold standard per diagnosi definitiva"
                    
                    exam_df = pd.DataFrame(list(exams.items()), columns=['Esame', 'Indicazione'])
                    st.dataframe(exam_df, use_container_width=True)
    
    elif model_type == "Valutazione Fibromialgia":
        st.write("#### 🌸 Valutazione Fibromialgia (Sindrome Fibromialgica)")
        st.info("Questo strumento valuta i sintomi e i criteri diagnostici della fibromialgia secondo i criteri ACR (American College of Rheumatology).")
        
        # Sezione 1: Criteri ACR e Widespread Pain Index (WPI)
        st.markdown("### 📍 Widespread Pain Index (WPI)")
        st.markdown("*Seleziona le aree in cui hai avvertito dolore nell'ultima settimana (19 aree totali)*")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Arto Superiore Sinistro:**")
            shoulder_l = st.checkbox("Spalla sinistra")
            arm_l = st.checkbox("Braccio sinistro")
            forearm_l = st.checkbox("Avambraccio sinistro")
            
            st.markdown("**Arto Inferiore Sinistro:**")
            hip_l = st.checkbox("Anca sinistra")
            thigh_l = st.checkbox("Coscia sinistra")
            calf_l = st.checkbox("Polpaccio sinistro")
            
        with col2:
            st.markdown("**Arto Superiore Destro:**")
            shoulder_r = st.checkbox("Spalla destra")
            arm_r = st.checkbox("Braccio destro")
            forearm_r = st.checkbox("Avambraccio destro")
            
            st.markdown("**Arto Inferiore Destro:**")
            hip_r = st.checkbox("Anca destra")
            thigh_r = st.checkbox("Coscia destra")
            calf_r = st.checkbox("Polpaccio destro")
            
        with col3:
            st.markdown("**Regione Assiale:**")
            jaw_l = st.checkbox("Mandibola sinistra")
            jaw_r = st.checkbox("Mandibola destra")
            chest = st.checkbox("Torace")
            abdomen = st.checkbox("Addome")
            upper_back = st.checkbox("Dorso superiore")
            lower_back = st.checkbox("Dorso inferiore")
            neck = st.checkbox("Collo")
        
        # Calcolo WPI
        wpi_score = sum([shoulder_l, arm_l, forearm_l, hip_l, thigh_l, calf_l,
                        shoulder_r, arm_r, forearm_r, hip_r, thigh_r, calf_r,
                        jaw_l, jaw_r, chest, abdomen, upper_back, lower_back, neck])
        
        # Sezione 2: Symptom Severity Scale (SSS)
        st.markdown("### 🔄 Symptom Severity Scale (SSS)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Sintomi Principali (0-3 per ciascuno):**")
            fatigue = st.selectbox("Affaticamento/Stanchezza", [0, 1, 2, 3], 
                                 format_func=lambda x: ["Assente", "Lieve", "Moderato", "Grave"][x])
            waking_tired = st.selectbox("Svegliarsi non riposati", [0, 1, 2, 3],
                                      format_func=lambda x: ["Assente", "Lieve", "Moderato", "Grave"][x])
            cognitive = st.selectbox("Problemi cognitivi (nebbia mentale)", [0, 1, 2, 3],
                                   format_func=lambda x: ["Assente", "Lieve", "Moderato", "Grave"][x])
            
        with col2:
            st.markdown("**Sintomi Somatici (0-3):**")
            # Lista sintomi somatici per fibromialgia
            somatic_symptoms = st.multiselect(
                "Seleziona i sintomi somatici presenti:",
                ["Dolore/crampi addominali", "Depressione", "Cefalea", "Sindrome dell'intestino irritabile",
                 "Nausea", "Nervosismo", "Dolore toracico", "Visione offuscata", "Febbre",
                 "Diarrea", "Secchezza oculare", "Insonnia", "Perdita appetito", "Eruzioni cutanee",
                 "Sensibilità al sole", "Difficoltà uditive", "Facilità alle ecchimosi", "Perdita capelli",
                 "Minzione frequente", "Minzione dolorosa", "Spasmi vescicali"]
            )
            
            # Scoring sintomi somatici
            if len(somatic_symptoms) == 0:
                somatic_score = 0
            elif len(somatic_symptoms) <= 3:
                somatic_score = 1
            elif len(somatic_symptoms) <= 6:
                somatic_score = 2
            else:
                somatic_score = 3
        
        # Calcolo SSS totale
        sss_score = fatigue + waking_tired + cognitive + somatic_score
        
        # Sezione 3: Valutazione aggiuntiva
        st.markdown("### 📋 Informazioni Aggiuntive")
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.selectbox("Durata dei sintomi:", 
                                  ["< 3 mesi", "3-6 mesi", "6-12 mesi", "> 12 mesi"])
            morning_stiffness = st.slider("Rigidità mattutina (minuti)", 0, 180, 30)
            sleep_quality = st.selectbox("Qualità del sonno", 
                                       ["Buona", "Discreta", "Scarsa", "Pessima"])
            
        with col2:
            exercise_tolerance = st.selectbox("Tolleranza all'esercizio", 
                                            ["Normale", "Ridotta", "Molto ridotta", "Intolleranza"])
            stress_level = st.slider("Livello di stress (0-10)", 0, 10, 5)
            family_history = st.selectbox("Familiarità per fibromialgia/dolore cronico", ["No", "Sì"])
        
        if st.button("🔬 Valuta Fibromialgia", use_container_width=True):
            with st.spinner("Analisi dei criteri diagnostici in corso..."):
                # Criteri diagnostici ACR 2010/2016
                # Criterio 1: WPI ≥ 7 e SSS ≥ 5, oppure WPI 4-6 e SSS ≥ 9
                acr_criterion_1 = (wpi_score >= 7 and sss_score >= 5) or (4 <= wpi_score <= 6 and sss_score >= 9)
                
                # Criterio 2: Sintomi presenti per almeno 3 mesi
                duration_criterion = duration in ["3-6 mesi", "6-12 mesi", "> 12 mesi"]
                
                # Probabilità fibromialgia
                if acr_criterion_1 and duration_criterion:
                    fibro_probability = 85 + min(10, (wpi_score + sss_score) / 2)  # 85-95%
                    diagnosis_status = "Criteri ACR soddisfatti"
                elif acr_criterion_1 and not duration_criterion:
                    fibro_probability = 60 + (wpi_score + sss_score) * 2  # 60-80%
                    diagnosis_status = "Possibile fibromialgia precoce"
                elif wpi_score >= 4 or sss_score >= 4:
                    fibro_probability = 30 + (wpi_score + sss_score) * 1.5  # 30-60%
                    diagnosis_status = "Fibromialgia incerta"
                else:
                    fibro_probability = min(25, (wpi_score + sss_score) * 3)  # 0-25%
                    diagnosis_status = "Fibromialgia improbabile"
                
                fibro_probability = min(95, fibro_probability)
                
                st.success("Valutazione completata!")
                
                # Metriche principali
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("WPI Score", f"{wpi_score}/19", 
                             delta="Alto" if wpi_score >= 7 else "Medio" if wpi_score >= 4 else "Basso")
                with col2:
                    st.metric("SSS Score", f"{sss_score}/12",
                             delta="Alto" if sss_score >= 9 else "Medio" if sss_score >= 5 else "Basso")
                with col3:
                    st.metric("Probabilità Fibromialgia", f"{fibro_probability:.1f}%",
                             delta="Alta" if fibro_probability > 70 else "Media" if fibro_probability > 40 else "Bassa")
                with col4:
                    st.metric("Status Diagnostico", diagnosis_status)
                
                # Analisi dettagliata
                st.markdown("#### 📊 Analisi Dettagliata dei Criteri")
                
                criteria_analysis = {
                    "Criterio ACR 2016": "✅ Soddisfatto" if acr_criterion_1 else "❌ Non soddisfatto",
                    "Durata sintomi (≥3 mesi)": "✅ Soddisfatto" if duration_criterion else "❌ Non soddisfatto",
                    "WPI (Widespread Pain Index)": f"{wpi_score}/19 - {'Significativo' if wpi_score >= 7 else 'Moderato' if wpi_score >= 4 else 'Basso'}",
                    "SSS (Symptom Severity Scale)": f"{sss_score}/12 - {'Alto' if sss_score >= 9 else 'Moderato' if sss_score >= 5 else 'Basso'}",
                    "Sintomi somatici": f"{len(somatic_symptoms)} sintomi - Score: {somatic_score}/3"
                }
                
                analysis_df = pd.DataFrame(list(criteria_analysis.items()), 
                                         columns=['Criterio', 'Valutazione'])
                st.dataframe(analysis_df, use_container_width=True)
                
                # Raccomandazioni cliniche
                st.markdown("#### 💡 Raccomandazioni Cliniche:")
                recommendations = []
                
                if fibro_probability > 80:
                    recommendations.append("🏥 **Consulto reumatologico specialistico urgente**")
                    recommendations.append("📋 **Valutazione multidisciplinare (reumatologo, neurologo, psichiatra)**")
                    recommendations.append("💊 **Considerare terapia farmacologica specifica**")
                elif fibro_probability > 60:
                    recommendations.append("🩺 **Consulto reumatologico entro 4-6 settimane**")
                    recommendations.append("🔬 **Esami di laboratorio per esclusioni differenziali**")
                    recommendations.append("🧘 **Approccio multimodale: fisioterapia + gestione stress**")
                elif fibro_probability > 30:
                    recommendations.append("📋 **Monitoraggio sintomi per 3-6 mesi**")
                    recommendations.append("💪 **Programma di esercizio fisico graduale**")
                    recommendations.append("🧠 **Valutazione psicologica per gestione dolore cronico**")
                else:
                    recommendations.append("🔍 **Ricerca di diagnosi alternative**")
                    recommendations.append("📊 **Approfondimento diagnostico mirato**")
                
                # Raccomandazioni specifiche
                if morning_stiffness > 60:
                    recommendations.append("🌅 **Gestione rigidità mattutina con terapie locali**")
                if sleep_quality in ["Scarsa", "Pessima"]:
                    recommendations.append("😴 **Igiene del sonno e possibile consulto specialistico**")
                if stress_level > 7:
                    recommendations.append("🧘 **Tecniche di gestione stress e rilassamento**")
                if exercise_tolerance in ["Molto ridotta", "Intolleranza"]:
                    recommendations.append("🏃 **Programma di ricondizionamento fisico molto graduale**")
                
                for rec in recommendations:
                    st.markdown(f"- {rec}")
                
                # Esami suggeriti
                if fibro_probability > 50:
                    st.markdown("#### 🔬 Esami Diagnostici Suggeriti:")
                    
                    # Esami di esclusione
                    exclusion_exams = {
                        "Emocromo completo": "Escludere anemie e patologie ematologiche",
                        "VES e PCR": "Escludere processi infiammatori attivi",
                        "TSH, T3, T4": "Escludere disfunzioni tiroidee",
                        "Vitamina D": "Frequentemente carente nella fibromialgia",
                        "CPK": "Escludere miopatie",
                        "ANA, Anti-DNA": "Escludere connettivopatie",
                        "Fattore reumatoide": "Escludere artrite reumatoide"
                    }
                    
                    if wpi_score > 10 or sss_score > 8:
                        exclusion_exams["Risonanza Magnetica spinale"] = "Escludere patologie strutturali"
                        exclusion_exams["Elettromiografia"] = "Escludere neuropatie periferiche"
                    
                    exam_df = pd.DataFrame(list(exclusion_exams.items()), 
                                         columns=['Esame', 'Indicazione'])
                    st.dataframe(exam_df, use_container_width=True)
                    
                    # Piano terapeutico suggerito
                    st.markdown("#### 🎯 Piano Terapeutico Multimodale:")
                    treatment_plan = {
                        "Farmacologico": "Pregabalin/Gabapentin, Duloxetina, Amitriptilina",
                        "Fisioterapico": "Esercizi aerobici a basso impatto, stretching, idroterapia",
                        "Psicologico": "Terapia cognitivo-comportamentale, mindfulness",
                        "Complementare": "Agopuntura, massoterapia, tecniche di rilassamento",
                        "Stile di vita": "Igiene del sonno, gestione stress, dieta anti-infiammatoria"
                    }
                    
                    for approach, details in treatment_plan.items():
                        st.markdown(f"**{approach}:** {details}")
    
    else:
        st.write("Sezione in sviluppo.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_clinical_trials_page():
    """Renders the clinical trials optimization page."""
    st.markdown('<h2 class="section-header">🧪 Ottimizzazione Trial Clinici</h2>', unsafe_allow_html=True)
    st.info("Questo modulo aiuta a identificare coorti di pazienti idonei per i trial clinici basandosi su dati anonimizzati.")

    st.markdown("#### Filtri per la selezione dei pazienti")
    col1, col2 = st.columns(2)
    with col1:
        pathology = st.selectbox("Patologia di interesse:", ["Oncologia", "Cardiologia", "Diabetologia", "Malattie Rare"])
        min_age = st.slider("Età minima", 18, 100, 40)
    with col2:
        comorbidities = st.multiselect("Escludi co-morbilità:", ["Ipertensione", "Diabete", "Insufficienza Renale"])
        max_age = st.slider("Età massima", 18, 100, 70)

    if st.button("👤 Trova Pazienti Idonei", use_container_width=True):
        with st.spinner("Ricerca nel database pazienti anonimizzato..."):
            # Simulazione
            patient_count = np.random.randint(50, 200)
            st.success(f"Trovati {patient_count} pazienti potenzialmente idonei.")
            
            # Dati simulati
            patient_data = {
                'ID Paziente (anonimo)': [f'P{np.random.randint(1000,9999)}' for _ in range(10)],
                'Età': [np.random.randint(min_age, max_age) for _ in range(10)],
                'Patologia': [pathology] * 10,
                'Score Compatibilità': [f'{np.random.uniform(85, 99):.1f}%' for _ in range(10)]
            }
            df_patients = pd.DataFrame(patient_data)
            st.dataframe(df_patients, use_container_width=True)


def render_about_page():
    """Renders the about page with professional profile."""
    st.markdown('<h2 class="section-header">👨‍💻 Profilo Professionale</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        # Immagine placeholder o logo
        st.markdown("<div style='text-align:center; font-size: 8rem;'>👨‍💻</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Antonino Piacenza</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #2e7d32;'>AI Researcher & MedTech Developer</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### Visione
        Sviluppare soluzioni di Intelligenza Artificiale etiche, scalabili e ad alto impatto per trasformare il settore medico-sanitario, migliorando la qualità della vita dei pazienti e l'efficienza degli operatori.
        
        ### Aree di Specializzazione
        - **Medicina Predittiva**: Modelli per la previsione di patologie e la stratificazione del rischio.
        - **NLP Clinico**: Estrazione di informazioni strutturate da referti medici e letteratura scientifica.
        - **Analisi Dati Sanitari**: Integrazione e analisi di big data provenienti da fonti eterogenee.
        - **Federated Learning**: Sviluppo di modelli AI che garantiscono la privacy dei dati sensibili.

        ### Contatti per Collaborazioni
        - **Email**: `ninomedical.ai@gmail.com`
        - **LinkedIn**: `linkedin.com/in/antoNinoF840`
        - **Progetti**: Aperto a collaborazioni per Horizon Europe e partnership industriali.
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
def render_footer():
    """Renders the application footer."""
    st.markdown("""
    <div class="footer">
        <p>© 2025 Nino Medical AI Pro Ultimate - Sviluppato da Antonino Piacenza</p>
        <p>Questo software è distribuito solo per scopi dimostrativi e di ricerca.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Entry Point ---
if __name__ == "__main__":
    main()

