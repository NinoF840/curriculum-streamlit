import streamlit as st
from PIL import Image
import base64

# Configurazione della pagina
st.set_page_config(
    page_title="Antonino Piacenza - AI Researcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1f4e79;
        border-bottom: 2px solid #1f4e79;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .contact-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .project-card {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2e7d32;
    }
    .skill-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f4e79;
    }
    .hero-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1.5rem;
    }
    .cta-button {
        background-color: #2e7d32;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Hero Section
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Antonino Piacenza</div>
        <div class="hero-subtitle">🧠 AI Researcher & Medical Technology Developer</div>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Sviluppo soluzioni di Intelligenza Artificiale per il settore medico-sanitario</p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">🇪🇺 Horizon Europe Ready</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">🏥 Clinical Validation</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">🤝 Partnership Oriented</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👨‍💻 Chi Sono", "🔬 Progetti", "🛠️ Competenze", "📞 Contatti"])

    with tab1:
        render_about_page()

    with tab2:
        render_projects_page()

    with tab3:
        render_skills_page()

    with tab4:
        render_contact_page()

def render_about_page():
    st.markdown('<h2 class="section-header">👨‍💻 Chi Sono</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Sono **Antonino Piacenza**, un ricercatore specializzato in **Intelligenza Artificiale applicata al settore medico-sanitario**.
        
        **Trasformo le sfide mediche in opportunità tecnologiche** attraverso soluzioni AI innovative che generano 
        valore concreto per ospedali, aziende farmaceutiche e centri di ricerca.
        
        ### 🎯 La Mia Proposta di Valore
        
        ✅ **ROI Dimostrabile**: Soluzioni che migliorano l'efficienza operativa e riducono i costi  
        ✅ **Time-to-Market Rapido**: Dalla ricerca al prototipo funzionale in tempi ottimizzati  
        ✅ **Compliance Garantita**: Rispetto di standard medici europei (MDR, GDPR, ISO 13485)  
        ✅ **Scalabilità Europea**: Progetti pronti per implementazione multi-paese  
        
        ### 🏆 Vantaggi Competitivi
        
        - **🔬 Ricerca + Business**: Combino rigore scientifico e visione commerciale
        - **🌍 Network Internazionale**: Accesso a partner accademici e industriali europei
        - **⚡ Prototipazione Rapida**: Dalla teoria alla demo funzionale
        - **📊 Validazione Clinica**: Esperienza nella validazione con strutture ospedaliere
        """)
    
    with col2:
        st.markdown("""
        <div class="contact-info">
            <h4>💼 Profilo Professionale</h4>
            <p><strong>📍 Base Operativa:</strong><br>Sicilia, Italia 🇮🇹</p>
            <p><strong>🎯 Target Market:</strong><br>EU Healthcare & MedTech</p>
            <p><strong>💰 Progetti:</strong><br>€50K - €2M+ (H2020/HE)</p>
            <p><strong>⏱️ Time-to-Market:</strong><br>6-18 mesi (MVP)</p>
            <p><strong>🤝 Partnership:</strong><br>Aperto a Joint Ventures</p>
        </div>
        """, unsafe_allow_html=True)

def render_projects_page():
    st.markdown('<h2 class="section-header">🔬 Progetti di Ricerca</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    I miei progetti si concentrano sull'applicazione dell'Intelligenza Artificiale in ambito medico, 
    con particolare attenzione all'innovazione sostenibile e alla collaborazione scientifica.
    """)
    
    # Progetto principale
    st.markdown('<h3 class="section-header">🏥 Nino Medical AI</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h4>🔍 Supporto alla Diagnostica</h4>
            <p>Sviluppo di algoritmi per l'analisi di immagini mediche e il supporto ai professionisti sanitari nelle diagnosi.</p>
            <ul>
                <li>Analisi di imaging medicale</li>
                <li>Pattern recognition</li>
                <li>Supporto decisionale clinico</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="project-card">
            <h4>🧠 Medicina Predittiva</h4>
            <p>Modelli predittivi per identificare pattern e tendenze nei dati sanitari, supportando la medicina preventiva.</p>
            <ul>
                <li>Analisi predittiva</li>
                <li>Modelli di rischio</li>
                <li>Prevenzione personalizzata</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h4>📊 Ottimizzazione Processi</h4>
            <p>Soluzioni per migliorare l'efficienza dei processi ospedalieri e della ricerca clinica.</p>
            <ul>
                <li>Automazione intelligente</li>
                <li>Ottimizzazione flussi di lavoro</li>
                <li>Gestione risorse sanitarie</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="project-card">
            <h4>🔬 Ricerca Scientifica</h4>
            <p>Collaborazioni con istituzioni accademiche per progetti di ricerca all'avanguardia nel campo dell'AI medica.</p>
            <ul>
                <li>Pubblicazioni scientifiche</li>
                <li>Collaborazioni internazionali</li>
                <li>Trasferimento tecnologico</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">💰 Opportunità di Business</h3>', unsafe_allow_html=True)
    
    # Business opportunities in columns
    bus_col1, bus_col2 = st.columns(2)
    
    with bus_col1:
        st.success("""
        **🎯 Target Clients**
        
        - 🏥 **Ospedali Privati** - Soluzioni per efficienza operativa
        - 💊 **Big Pharma** - AI per drug discovery e clinical trials
        - 🏭 **MedTech Companies** - Integrazione AI nei dispositivi
        - 🏛️ **Enti Pubblici** - Progetti di innovazione digitale
        """)
    
    with bus_col2:
        st.info("""
        **🚀 Funding Opportunities**
        
        - 🇪🇺 **Horizon Europe** - Partner per consorzi internazionali
        - 💰 **EIT Health** - Innovation projects fino a €2M
        - 🍋 **Sicilia FESR** - Progetti regionali €100K-€500K
        - 🏆 **EIC Accelerator** - Scale-up per startup MedTech
        """)

def render_skills_page():
    st.markdown('<h2 class="section-header">🛠️ Competenze Tecniche</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="skill-card">
            <h4>🐍 Linguaggi di Programmazione</h4>
            <ul>
                <li><strong>Python</strong> - Linguaggio principale</li>
                <li><strong>SQL</strong> - Gestione database</li>
                <li><strong>R</strong> - Analisi statistica</li>
                <li><strong>JavaScript</strong> - Frontend</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
            <h4>🤖 Machine Learning</h4>
            <ul>
                <li><strong>TensorFlow/Keras</strong></li>
                <li><strong>PyTorch</strong></li>
                <li><strong>Scikit-learn</strong></li>
                <li><strong>OpenCV</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="skill-card">
            <h4>📊 Data Science</h4>
            <ul>
                <li><strong>Pandas & NumPy</strong></li>
                <li><strong>Matplotlib & Seaborn</strong></li>
                <li><strong>Jupyter Notebooks</strong></li>
                <li><strong>Statistical Analysis</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
            <h4>🏥 Dominio Medico</h4>
            <ul>
                <li><strong>Medical Imaging</strong></li>
                <li><strong>Clinical Data Analysis</strong></li>
                <li><strong>Healthcare Standards</strong></li>
                <li><strong>Regulatory Compliance</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="skill-card">
            <h4>☁️ Tecnologie Cloud</h4>
            <ul>
                <li><strong>Docker</strong></li>
                <li><strong>Linux Systems</strong></li>
                <li><strong>Cloud Deployment</strong></li>
                <li><strong>API Development</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="skill-card">
            <h4>📱 Framework Web</h4>
            <ul>
                <li><strong>Streamlit</strong></li>
                <li><strong>FastAPI</strong></li>
                <li><strong>Flask</strong></li>
                <li><strong>React (base)</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">📈 Aree di Specializzazione</h3>', unsafe_allow_html=True)
    
    specialization_col1, specialization_col2 = st.columns(2)
    
    with specialization_col1:
        st.markdown("""
        ### 🔬 Ricerca e Sviluppo
        - **Deep Learning per Imaging Medico**
        - **Natural Language Processing per testi clinici**
        - **Analisi Predittiva in Sanità**
        - **Federated Learning per Privacy**
        """)
    
    with specialization_col2:
        st.markdown("""
        ### 💼 Applicazioni Pratiche
        - **Sviluppo Prototipi Clinici**
        - **Integrazione Sistemi Ospedalieri**
        - **Validazione Algoritmi**
        - **Trasferimento Tecnologico**
        """)

def render_contact_page():
    st.markdown('<h2 class="section-header">📞 Contatti</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    Sono sempre interessato a nuove collaborazioni e opportunità di ricerca. 
    Non esitare a contattarmi per discutere progetti, partnership o semplicemente per scambiare idee!
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="contact-info">
            <h3>📧 Informazioni di Contatto</h3>
            
            <p><strong>📧 Email Principale:</strong><br>
            <a href="mailto:ninomedical.ai@gmail.com">ninomedical.ai@gmail.com</a></p>
            
            <p><strong>📱 Telefono:</strong><br>
            <a href="tel:+393936789529">+39 393 678 9529</a></p>
            
            <p><strong>📍 Ubicazione:</strong><br>
            Castelvetrano (TP), Sicilia, Italia</p>
            
            <p><strong>🌐 Disponibilità:</strong><br>
            Collaborazioni remote e in presenza</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h3 class="section-header">🤝 Tipi di Collaborazione</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        **Sono interessato a:**
        
        - 🔬 **Progetti di Ricerca** con università e centri di ricerca
        - 🏥 **Collaborazioni Cliniche** con ospedali e strutture sanitarie
        - 💼 **Partnership Aziendali** per sviluppo prodotti innovativi
        - 🇪🇺 **Progetti Europei** (Horizon Europe, EIT Health, etc.)
        - 🍋 **Iniziative Regionali** in Sicilia (FESR, POR, etc.)
        - 📚 **Attività Didattiche** e formazione specialistica
        """)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h4>⚡ Risposta Rapida</h4>
            <p>Rispondo generalmente entro 24 ore durante i giorni lavorativi.</p>
        </div>
        
        <div class="project-card">
            <h4>🌍 Collaborazioni Internazionali</h4>
            <p>Disponibile per progetti in tutta Europa, con particolare focus su Horizon Europe.</p>
        </div>
        
        <div class="project-card">
            <h4>🎓 Formazione e Consulenza</h4>
            <p>Disponibile per formazione tecnica e consulenza su progetti AI in ambito medico.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("""
        **💡 Hai un'idea di progetto?**
        
        Contattami per una prima discussione gratuita sui tuoi obiettivi e su come l'AI può aiutare il tuo progetto o la tua organizzazione.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>© 2025 Antonino Piacenza - AI Researcher</p>
    <p>🧠 Innovazione Responsabile per un Futuro Migliore 🚀</p>
    <p><em>Portfolio realizzato con Streamlit</em></p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
