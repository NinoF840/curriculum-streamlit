import streamlit as st
from PIL import Image
import base64

# Configurazione della pagina
st.set_page_config(
    page_title="Antonino Piacenza - CV",
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
    .experience-card {
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
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">ANTONINO PIACENZA</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">🧠 Ricercatore IA</h2>', unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📄 Curriculum Vitae", "🏥 Nino Medical AI", "🇪🇺 Horizon Europe"])
    
    with tab1:
        render_cv_page()
    
    with tab2:
        render_nino_medical_ai_page()

    with tab3:
        render_horizon_europe_page()

def render_cv_page():
    
    # Sidebar con info di contatto
    with st.sidebar:
        st.markdown("### 📞 Contatti")
        st.write("📧 **Email:** ninomedical.ai@gmail.com")
        st.write("📱 **Telefono:** +39 3936789529")
        st.write("💬 **WhatsApp:** +39 3936789529")
        st.write("📍 **Ubicazione:** Castelvetrano (TP), Italia")
        st.write("🎂 **Anno di nascita:** 1958")
        
        st.markdown("---")
        st.markdown("### 🔗 Collegamenti")
        if st.button("📄 Scarica CV PDF"):
            st.write("PDF in preparazione...")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Profilo Professionale
        st.markdown('<h2 class="section-header">👨‍💼 Profilo Professionale</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="contact-info">
        Da sempre curioso e pratico, unisco esperienza tecnica e umana per contribuire a 
        progetti innovativi. Credo nell'IA come strumento utile, ma solo se resta l'uomo a guidarla.
        </div>
        """, unsafe_allow_html=True)
        
        # Hero Section - Nino Medical AI
        st.markdown("""
        <div class="hero-card">
            <div class="hero-title">🏥 Nino Medical AI</div>
            <div class="hero-subtitle">Progetto di Punta in Intelligenza Artificiale Medica</div>
            <p>🔬 Soluzioni innovative per ospedali, università e centri di ricerca</p>
            <p>📊 Supporto decisionale clinico • 🧠 Medicina predittiva • 🎯 Diagnostica assistita</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progetti e Ricerca
        st.markdown('<h2 class="section-header">🔬 Progetti e Ricerca</h2>', unsafe_allow_html=True)
        
        projects = [
            {
                "title": "🏥 Nino Medical AI",
                "description": "Progetto di ricerca in IA applicata alla medicina"
            },
            {
                "title": "🇪🇺 Contributi Horizon Europe",
                "description": "In attesa di validazione per finanziamenti europei"
            },
            {
                "title": "💡 Soluzioni Innovative Sanitarie",
                "description": "Sviluppo soluzioni innovative per il settore sanitario"
            },
            {
                "title": "🔬 Ricerca IA Medica",
                "description": "Ricerca e sviluppo in ambito IA medica"
            }
        ]
        
        for project in projects:
            st.markdown(f"""
            <div class="project-card">
                <h4>{project['title']}</h4>
                <p>{project['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Esperienze Professionali
        st.markdown('<h2 class="section-header">💼 Esperienze Professionali</h2>', unsafe_allow_html=True)
        
        experiences = [
            {
                "role": "🖥️ Sistemista Remoto e Hardware Specialist",
                "duration": "ca. 3 anni",
                "details": [
                    "Gestione e manutenzione server Linux (Slackware, Mint, RedHat, Fedora, PuppyLinux)",
                    "Assemblaggio PC, test hardware, configurazione di sistemi sicuri (TAILS, Tor)",
                    "Competenze: troubleshooting, autonomia tecnica, competenze informatiche open source"
                ]
            },
            {
                "role": "🚂 Macchinista – Ferrovie dello Stato Italiane",
                "duration": "",
                "details": [
                    "Conduzione e gestione treni su tratte regionali e nazionali",
                    "Responsabilità nella sicurezza, rispetto di tempistiche, protocolli e gestione emergenze",
                    "Competenze: attenzione al dettaglio, gestione dello stress, affidabilità operativa"
                ]
            },
            {
                "role": "⚓ Sergente – Marina Militare Italiana",
                "duration": "",
                "details": [
                    "Ruolo operativo e coordinativo su navi militari",
                    "Valori trasmessi: disciplina, leadership, spirito di squadra"
                ]
            }
        ]
        
        for exp in experiences:
            st.markdown(f"""
            <div class="experience-card">
                <h4>{exp['role']}</h4>
                <p><em>{exp['duration']}</em></p>
                <ul>
            """, unsafe_allow_html=True)
            for detail in exp['details']:
                st.markdown(f"<li>{detail}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with col2:
        # Istruzione
        st.markdown('<h2 class="section-header">🎓 Istruzione</h2>', unsafe_allow_html=True)
        st.markdown("""
        **📜 Diploma di Maturità Scientifica**  
        Castelvetrano (TP)
        
        **⚖️ Studi Universitari**  
        Facoltà di Giurisprudenza (3 anni)
        """)
        
        # Competenze
        st.markdown('<h2 class="section-header">🛠️ Competenze</h2>', unsafe_allow_html=True)
        
        skills = [
            ("Gestione sistemi Linux", 90),
            ("Assemblaggio/test hardware", 80),
            ("Utilizzo strumenti digitali", 95),
            ("Autonomia operativa", 85)
        ]
        
        for skill, level in skills:
            st.write(f"**{skill}**")
            st.progress(level/100)
        
        st.markdown("""
        **Altre competenze:**
        - Problem Solving tecnico-pratico
        - Sviluppo e test schede elettroniche
        - Conoscenza ambienti open-source
        - Ricerca e sviluppo in IA medica
        """)
        
        # Statistiche
        st.markdown('<h2 class="section-header">📊 In Numeri</h2>', unsafe_allow_html=True)
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Anni di Esperienza", "25+")
            st.metric("Progetti IA", "4+")
        with col_stat2:
            st.metric("Competenza Linux", "90%")
            st.metric("Problem Solving", "95%")

def render_nino_medical_ai_page():
    st.markdown('<h2 class="section-header">🏥 Nino Medical AI - Progetto di Ricerca</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    **Nino Medical AI** è un'iniziativa di ricerca e sviluppo dedicata a creare soluzioni di Intelligenza Artificiale a supporto del settore medico-sanitario. 
    L'obiettivo è fornire strumenti innovativi a **ospedali, cliniche, università e centri di ricerca** per migliorare la diagnostica, ottimizzare i processi e accelerare la scoperta scientifica.
    """)

    st.markdown('<h3 class="section-header">🎯 Aree di Intervento</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        🔍 **Supporto alla Diagnostica**
        - Analisi di immagini mediche (TAC, RMN, ecografie)
        - Assistenza ai medici nella diagnosi precoce
        - Interpretazione di dati clinici complessi
        
        🧠 **Medicina Predittiva**
        - Previsione insorgenza patologie
        - Analisi risposta a terapie
        - Modelli basati su dati storici e genetici
        """)
    
    with col2:
        st.markdown("""
        📊 **Ottimizzazione Trial Clinici**
        - Selezione intelligente dei pazienti
        - Monitoraggio andamento trial
        - Analisi risultati automatizzata
        
        ⚙️ **Automazione Ospedaliera**
        - Automazione task ripetitivi
        - Ottimizzazione flussi di lavoro
        - Supporto decisionale clinico
        """)

    st.markdown('<h3 class="section-header">🛠️ Stack Tecnologico</h3>', unsafe_allow_html=True)
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        **Linguaggi & Framework**
        - Python 3.11+
        - Streamlit
        - FastAPI (planned)
        """)
    
    with tech_col2:
        st.markdown("""
        **AI/ML Libraries**
        - TensorFlow/Keras
        - PyTorch
        - Scikit-learn
        - OpenCV
        """)
    
    with tech_col3:
        st.markdown("""
        **Data & Infrastructure**
        - Pandas, NumPy
        - Docker
        - Linux Systems
        - Cloud Deployment
        """)

    st.markdown('<h3 class="section-header">📈 Stato del Progetto</h3>', unsafe_allow_html=True)
    
    status_col1, status_col2 = st.columns([2, 1])
    
    with status_col1:
        st.info("🔬 **Fase Attuale**: Ricerca e Sviluppo")
        st.markdown("""
        - Esplorazione di partnership con istituzioni accademiche
        - Validazione modelli su dataset medici
        - Sviluppo prototipi per casi d'uso specifici
        - Collaborazioni con centri di ricerca sanitaria
        """)
    
    with status_col2:
        st.metric("Progetti in R&D", "4+")
        st.metric("Partnership Esplorate", "3")
        st.metric("Anni Esperienza IA", "2+")
    
    st.markdown('<h3 class="section-header">🎁 Obiettivi Futuri</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    🎯 **Obiettivi a Breve Termine (6-12 mesi)**:
    - Completare validazione prototipi su dataset reali
    - Stabilire partnership con almeno un ospedale o università
    - Pubblicare primi risultati di ricerca
    
    🚀 **Visione a Lungo Termine**:
    - Creare una piattaforma integrata per supporto decisionale medico
    - Contribuire alla ricerca scientifica con pubblicazioni peer-reviewed
    - Sviluppare soluzioni certificate per uso clinico
    """)
    
    st.markdown('<h3 class="section-header">🤝 Collaborazioni</h3>', unsafe_allow_html=True)
    st.markdown("""
    Interessato a collaborazioni con:
    - 🏥 **Ospedali e Cliniche**: per validazione e implementazione di soluzioni IA
    - 🎓 **Università e Centri di Ricerca**: per progetti di ricerca congiunti
    - 💼 **Aziende Sanitarie**: per sviluppo di prodotti innovativi
    - 🌍 **Progetti Horizon Europe**: per finanziamenti e collaborazioni internazionali
    """)

def render_horizon_europe_page():
    st.markdown('<h2 class="section-header">🇪🇺 Contributi per Horizon Europe</h2>', unsafe_allow_html=True)

    st.markdown("""
    **Horizon Europe** rappresenta un'opportunità fondamentale per finanziare e scalare progetti di ricerca innovativi in Europa. 
    La mia iniziativa **Nino Medical AI** è allineata con gli obiettivi di Horizon Europe, in particolare nei cluster dedicati a **Salute** e **Digitale, Industria e Spazio**.
    """)

    st.markdown('<h3 class="section-header">💡 Proposte di Progetto Principali</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="project-card">
            <h4>Piattaforma IA per Diagnostica Rurale</h4>
            <p>Sviluppo di una piattaforma IA centralizzata per supportare la diagnostica in aree rurali o con accesso limitato a specialisti, usando modelli federati per garantire la privacy dei dati.</p>
            <ul>
                <li><strong>Cluster</strong>: Salute, Digitale</li>
                <li><strong>Obiettivo</strong>: Ridurre le disparità sanitarie</li>
                <li><strong>Tecnologie</strong>: Federated Learning, AI, Cloud</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="project-card">
            <h4>IA per la Medicina di Precisione</h4>
            <p>Creazione di modelli predittivi per personalizzare le terapie oncologiche, analizzando dati genomici, clinici e di imaging per identificare i trattamenti più efficaci per ciascun paziente.</p>
            <ul>
                <li><strong>Cluster</strong>: Salute</li>
                <li><strong>Obiettivo</strong>: Migliorare l'efficacia delle cure</li>
                <li><strong>Tecnologie</strong>: Deep Learning, Big Data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">🎯 Ambiti di Interesse e Competenza</h3>', unsafe_allow_html=True)
    st.markdown("""
    - **Cluster 1: Health**
        - Staying healthy in a rapidly changing society
        - Tackling diseases and reducing disease burden
        - Unlocking the full potential of new tools, technologies and digital solutions for a healthy society
    
    - **Cluster 4: Digital, Industry and Space**
        - A data-driven economy
        - Artificial Intelligence and Robotics
        - Next Generation Internet
    
    - **Mission: Cancer**
        - Conquering cancer: mission possible
    """)

    st.markdown('<h3 class="section-header">🤝 Cerco Partner per Consorzi</h3>', unsafe_allow_html=True)
    st.success("""
    Sono attivamente alla ricerca di partner per formare consorzi e presentare proposte per le prossime call di Horizon Europe.
    
    **Chi cerco:**
    - **Università e Centri di Ricerca**: per validazione scientifica e ricerca di base.
    - **Ospedali e Strutture Sanitarie**: per l'accesso ai dati e la validazione clinica.
    - **Aziende e PMI Innovative**: per lo sviluppo, la commercializzazione e l'integrazione di soluzioni.
    - **Esperti di Regolamentazione**: per garantire la conformità normativa dei dispositivi medici basati su IA.
    
    Se sei interessato a collaborare, contattami per discutere di possibili sinergie.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>© 2025 Antonino Piacenza - Ricercatore IA</p>
    <p>Curriculum realizzato con Streamlit 🚀</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
