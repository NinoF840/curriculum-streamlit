import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import base64
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Nino Medical AI Pro Ultimate - Imaging",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .image-analysis-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #1f4e79;
        margin: 1rem 0;
    }
    .results-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
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
    elif page == 'image_analysis':
        render_image_analysis_page()
    elif page == 'dicom_viewer':
        render_dicom_viewer_page()
    elif page == 'ai_models':
        render_ai_models_page()
    elif page == 'batch_processing':
        render_batch_processing_page()
    elif page == 'about':
        render_about_page()
    
    render_footer()

# --- Sidebar ---
def render_sidebar():
    """Renders the navigation sidebar."""
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #1f4e79;'>Nino Medical AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Pro Ultimate - Imaging Edition</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🩺 Navigazione")
        nav_buttons = {
            "📊 Dashboard": "dashboard",
            "🖼️ Analisi Immagini": "image_analysis",
            "💾 Viewer DICOM": "dicom_viewer",
            "🤖 Modelli AI": "ai_models",
            "📦 Elaborazione Batch": "batch_processing",
            "👨‍💻 Chi Sono": "about"
        }
        
        for label, page_key in nav_buttons.items():
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Statistiche Imaging")
        st.metric("🖼️ Immagini Analizzate", "12.5k+", delta="250 oggi")
        st.metric("🎯 Accuratezza Media", "94.2%", delta="1.5%")
        st.metric("⚡ Modelli Attivi", "8", delta="2 nuovi")

# --- Pages ---
def render_main_dashboard():
    """Renders the main dashboard page."""
    st.markdown('<h1 class="main-header">Nino Medical AI Pro Ultimate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Imaging Edition - Analisi Avanzata di Immagini Mediche</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="image-analysis-card">'
                '<h2 style="text-align: center;">🩺 Benvenuto nella versione Imaging</h2>'
                '<p style="text-align: center;">Questa versione è specializzata nell\'analisi di immagini mediche con algoritmi di Deep Learning avanzati per radiologie, TAC, RMN e altre modalità di imaging diagnostico.</p>'
                '</div>', unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">Stato del Sistema Imaging</h2>', unsafe_allow_html=True)
    
    # System metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="card" style="text-align: center;"><h4>GPU Status</h4><p style="color: green; font-weight: bold;">✅ NVIDIA RTX Ready</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="text-align: center;"><h4>DICOM Support</h4><p style="color: green; font-weight: bold;">✅ Attivo</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card" style="text-align: center;"><h4>AI Models</h4><p style="color: green; font-weight: bold;">✅ Caricate (8)</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="card" style="text-align: center;"><h4>Processing Queue</h4><p style="color: blue; font-weight: bold;">2 in coda</p></div>', unsafe_allow_html=True)

    # Recent activity charts
    st.markdown("### 📈 Attività di Analisi Imaging")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("##### Tipi di Imaging Analizzati (Ultimi 30 giorni)")
        df_imaging = pd.DataFrame({
            'Tipo': ['RX Torace', 'TAC Addome', 'RMN Cranio', 'Ecografia', 'Mammografia'],
            'Quantità': [450, 220, 180, 320, 150]
        })
        fig = px.pie(df_imaging, values='Quantità', names='Tipo', title="Distribuzione per Tipo")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("##### Performance dei Modelli AI")
        df_performance = pd.DataFrame({
            'Modello': ['Pneumonia Detection', 'Fracture Detection', 'Cancer Screening', 'Anomaly Detection'],
            'Precisione': [96.2, 94.8, 92.1, 89.7],
            'Recall': [94.1, 92.3, 90.5, 87.2]
        })
        fig = px.bar(df_performance, x='Modello', y=['Precisione', 'Recall'], 
                    title="Metriche di Performance", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_image_analysis_page():
    """Renders the medical image analysis page."""
    st.markdown('<h2 class="section-header">🖼️ Analisi Immagini Mediche</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="warning-box">'
                '⚠️ <strong>IMPORTANTE:</strong> Questo strumento è destinato esclusivamente a scopi dimostrativi e di ricerca. Non utilizzare per diagnosi cliniche reali.'
                '</div>', unsafe_allow_html=True)

    # Image upload section
    st.markdown("#### 📁 Carica Immagine Medica")
    uploaded_file = st.file_uploader(
        "Seleziona un'immagine medica (JPEG, PNG, DICOM)",
        type=['jpg', 'jpeg', 'png', 'dcm'],
        help="Supportati: RX, TAC, RMN, Ecografie, Mammografie"
    )
    
    if uploaded_file is not None:
        # Display and analyze image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("##### 🖼️ Immagine Originale")
            
            # Load and display image
            if uploaded_file.type.startswith('image'):
                image = Image.open(uploaded_file)
                st.image(image, caption=f"File: {uploaded_file.name}", use_container_width=True)
                
                # Image preprocessing options
                st.write("**Preprocessing Options:**")
                brightness = st.slider("Luminosità", 0.5, 2.0, 1.0, 0.1)
                contrast = st.slider("Contrasto", 0.5, 2.0, 1.0, 0.1)
                
                # Apply preprocessing
                if brightness != 1.0 or contrast != 1.0:
                    enhanced_image = ImageEnhance.Brightness(image).enhance(brightness)
                    enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast)
                    st.image(enhanced_image, caption="Immagine Pre-processata", use_container_width=True)
                    image = enhanced_image
                    
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("##### 🤖 Configurazione Analisi")
            
            # Analysis options
            analysis_type = st.selectbox(
                "Tipo di Analisi:",
                ["Rilevamento Anomalie Generali", "Analisi Pneumonia", "Rilevamento Fratture", 
                 "Screening Tumori", "Analisi Densità Ossea", "Segmentazione Organi"]
            )
            
            confidence_threshold = st.slider("Soglia di Confidenza", 0.1, 0.9, 0.7, 0.1)
            
            if st.button("🔍 Avvia Analisi AI", use_container_width=True, type="primary"):
                with st.spinner("🧠 Analisi AI in corso... Attendere..."):
                    # Simulate AI analysis
                    import time
                    time.sleep(3)
                    
                    # Generate simulated results
                    results = generate_analysis_results(analysis_type, confidence_threshold)
                    st.session_state.analysis_results = results
                    
                st.success("✅ Analisi completata!")
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display results if available
        if 'analysis_results' in st.session_state:
            display_analysis_results(st.session_state.analysis_results)


def render_dicom_viewer_page():
    """Renders the DICOM viewer page."""
    st.markdown('<h2 class="section-header">💾 Viewer DICOM Avanzato</h2>', unsafe_allow_html=True)
    st.info("Visualizzatore per immagini DICOM con strumenti di misurazione e annotazione.")
    
    # DICOM upload
    dicom_file = st.file_uploader("Carica file DICOM (.dcm)", type=['dcm'])
    
    if dicom_file:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("##### 📊 Metadata DICOM")
        
        # Simulate DICOM metadata
        metadata = {
            "Paziente": "ANONIMO_001",
            "Modalità": "CT",
            "Data Studio": "2025-01-15",
            "Dimensioni": "512x512x150",
            "Spacing": "0.5mm x 0.5mm x 1.0mm",
            "Finestra/Livello": "400/40 HU"
        }
        
        col1, col2, col3 = st.columns(3)
        for i, (key, value) in enumerate(metadata.items()):
            col = [col1, col2, col3][i % 3]
            col.metric(key, value)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Viewing controls
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("##### 🎛️ Controlli di Visualizzazione")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            window_width = st.slider("Window Width", 1, 2000, 400)
        with col2:
            window_level = st.slider("Window Level", -1000, 1000, 40)
        with col3:
            slice_number = st.slider("Slice", 1, 150, 75)
        
        st.info(f"Visualizzando slice {slice_number}/150 con W/L: {window_width}/{window_level}")
        st.markdown('</div>', unsafe_allow_html=True)


def render_ai_models_page():
    """Renders the AI models management page."""
    st.markdown('<h2 class="section-header">🤖 Gestione Modelli AI</h2>', unsafe_allow_html=True)
    
    # Model status table
    st.write("### 📋 Modelli Disponibili")
    models_data = {
        'Modello': ['PneumoniaNet v2.1', 'FractureDetector v1.8', 'CancerScreening v3.0', 
                   'BoneAge v1.5', 'RetinalAnalyzer v2.3', 'BrainTumor v1.9',
                   'HeartSegment v2.0', 'LungNodule v1.7'],
        'Tipo': ['Classificazione', 'Rilevamento', 'Screening', 'Regressione', 
                'Segmentazione', 'Classificazione', 'Segmentazione', 'Rilevamento'],
        'Accuratezza': ['96.2%', '94.8%', '92.1%', '89.7%', '97.1%', '91.5%', '93.8%', '88.9%'],
        'Stato': ['✅ Attivo', '✅ Attivo', '✅ Attivo', '✅ Attivo', 
                 '✅ Attivo', '✅ Attivo', '✅ Attivo', '✅ Attivo'],
        'Ultima Update': ['2025-01-08', '2025-01-07', '2025-01-05', '2025-01-03',
                         '2025-01-08', '2025-01-06', '2025-01-04', '2025-01-02']
    }
    
    df_models = pd.DataFrame(models_data)
    st.dataframe(df_models, use_container_width=True)
    
    # Model performance metrics
    st.write("### 📊 Performance in Tempo Reale")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(df_models, x='Modello', y='Accuratezza', 
                    title="Accuratezza per Modello")
        fig.update_traces(marker_color='#1f4e79')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Simulate real-time usage
        usage_data = {
            'Modello': ['PneumoniaNet', 'FractureDetector', 'CancerScreening', 'Altri'],
            'Uso Giornaliero': [45, 32, 28, 15]
        }
        fig = px.pie(pd.DataFrame(usage_data), values='Uso Giornaliero', names='Modello',
                    title="Utilizzo Giornaliero (%)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_batch_processing_page():
    """Renders the batch processing page."""
    st.markdown('<h2 class="section-header">📦 Elaborazione Batch</h2>', unsafe_allow_html=True)
    st.info("Elabora multiple immagini mediche simultaneamente per analisi su larga scala.")
    
    # Batch upload
    st.write("#### 📁 Caricamento Multiplo")
    uploaded_files = st.file_uploader(
        "Seleziona multiple immagini mediche:",
        type=['jpg', 'jpeg', 'png', 'dcm'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"Caricate {len(uploaded_files)} immagini.")
        
        # Batch processing options
        st.write("#### ⚙️ Configurazione Batch")
        col1, col2 = st.columns(2)
        
        with col1:
            batch_analysis = st.selectbox(
                "Tipo di Analisi Batch:",
                ["Screening Automatico", "Rilevamento Anomalie", "Classificazione Patologie",
                 "Misurazione Automatica", "Quality Control"]
            )
            
        with col2:
            export_format = st.selectbox(
                "Formato Export:",
                ["CSV Report", "JSON Detailed", "PDF Summary", "Excel Workbook"]
            )
        
        if st.button("🚀 Avvia Elaborazione Batch", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate batch processing
            for i, file in enumerate(uploaded_files):
                progress = (i + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Elaborazione {file.name}... ({i+1}/{len(uploaded_files)})")
                import time
                time.sleep(0.5)
            
            status_text.text("✅ Elaborazione completata!")
            
            # Show batch results
            st.success("Elaborazione batch completata con successo!")
            
            # Generate sample batch results
            batch_results = pd.DataFrame({
                'File': [f.name for f in uploaded_files[:10]],  # Show first 10
                'Status': ['✅ Successo'] * min(10, len(uploaded_files)),
                'Confidenza': [f"{np.random.uniform(0.85, 0.99):.2%}" for _ in range(min(10, len(uploaded_files)))],
                'Risultato': [f"Risultato {i+1}" for i in range(min(10, len(uploaded_files)))]
            })
            
            st.dataframe(batch_results, use_container_width=True)


def render_about_page():
    """Renders the about page."""
    st.markdown('<h2 class="section-header">👨‍💻 Nino Medical AI - Imaging Edition</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 Specializzazione in Medical Imaging
    
    Questa versione di Nino Medical AI è specificamente progettata per l'analisi avanzata di immagini mediche, 
    utilizzando algoritmi di Deep Learning all'avanguardia per supportare radiologi e clinici nella diagnosi.
    
    #### 🔬 Tecnologie Implementate:
    - **Computer Vision Avanzata**: Modelli CNN personalizzati per diverse modalità di imaging
    - **Elaborazione DICOM**: Supporto completo per standard medicali
    - **Deep Learning**: Reti neurali specializzate per ciascun tipo di patologia
    - **Preprocessing Intelligente**: Algoritmi di miglioramento automatico delle immagini
    
    #### 📊 Modalità Supportate:
    - Radiografie (RX)
    - Tomografia Computerizzata (TAC/CT)
    - Risonanza Magnetica (RMN/MRI)
    - Ecografie (US)
    - Mammografie
    - Imaging retinico
    
    #### ⚡ Performance:
    - Elaborazione in tempo reale
    - Analisi batch per volumi elevati
    - Accuratezza media >90% sui dataset di validazione
    - Supporto GPU per accelerazione hardware
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# --- Helper Functions ---
def generate_analysis_results(analysis_type, confidence_threshold):
    """Generate simulated analysis results."""
    results = {
        'analysis_type': analysis_type,
        'confidence': np.random.uniform(confidence_threshold, 0.98),
        'findings': [],
        'metrics': {},
        'recommendations': []
    }
    
    if analysis_type == "Rilevamento Anomalie Generali":
        results['findings'] = [
            "Possibile nodulo polmonare rilevato nel lobo superiore destro",
            "Densità aumentata nell'area cardiaca sinistra",
            "Strutture costali nella norma"
        ]
        results['metrics'] = {
            'Anomalie rilevate': 2,
            'Confidenza media': f"{results['confidence']:.1%}",
            'Tempo elaborazione': "2.3s"
        }
        results['recommendations'] = [
            "Raccomandato approfondimento con TAC ad alta risoluzione",
            "Consultazione cardiologica per area di aumentata densità"
        ]
    
    return results

def display_analysis_results(results):
    """Display the analysis results in a formatted way."""
    st.markdown('<h3 class="section-header">📋 Risultati Analisi</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        st.write(f"**Tipo di Analisi:** {results['analysis_type']}")
        st.write(f"**Confidenza Generale:** {results['confidence']:.1%}")
        
        st.write("**Reperti Identificati:**")
        for finding in results['findings']:
            st.write(f"• {finding}")
        
        st.write("**Raccomandazioni:**")
        for rec in results['recommendations']:
            st.write(f"• {rec}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.write("**Metriche di Elaborazione:**")
        for key, value in results['metrics'].items():
            st.metric(key, value)

def render_footer():
    """Renders the application footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>© 2025 Nino Medical AI Pro Ultimate - Imaging Edition</p>
        <p>Sviluppato da Antonino Piacenza per la ricerca in Medical Imaging</p>
        <p><strong>Disclaimer:</strong> Solo per scopi dimostrativi e di ricerca. Non utilizzare per diagnosi cliniche.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Entry Point ---
if __name__ == "__main__":
    main()
