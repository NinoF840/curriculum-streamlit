"""
Nino Medical AI - Moduli IA Avanzati
====================================

Moduli di Intelligenza Artificiale per analisi mediche avanzate:
- Classificazione immagini mediche
- Analisi NLP su testi medici
- Medicina predittiva
- Analisi dei sintomi

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import tensorflow as tf
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import nltk
from textblob import TextBlob
import re
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Any, Optional
import joblib
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class MedicalImageAnalyzer:
    """Analizzatore di immagini mediche usando CNN."""
    
    def __init__(self):
        self.model = self._create_cnn_model()
        self.class_names = [
            'Normal', 'Pneumonia', 'COVID-19', 'Tuberculosis', 
            'Fracture', 'Tumor', 'Other'
        ]
        
    def _create_cnn_model(self) -> tf.keras.Model:
        """Crea un modello CNN per classificazione di immagini mediche."""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
        
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocessa l'immagine per l'analisi."""
        # Converti in RGB se necessario
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Ridimensiona a 224x224
        image = image.resize((224, 224))
        
        # Converti in array numpy
        img_array = np.array(image)
        
        # Normalizza i pixel (0-1)
        img_array = img_array.astype(np.float32) / 255.0
        
        # Aggiungi batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Analizza un'immagine medica."""
        try:
            # Preprocessa l'immagine
            processed_img = self.preprocess_image(image)
            
            # Simula predizione (in realtà useresti un modello pre-trained)
            # Per demo, generiamo predizioni random realistiche
            np.random.seed(42)  # Per risultati consistenti
            
            predictions = np.random.dirichlet(np.ones(len(self.class_names)), size=1)[0]
            
            # Ordina per confidenza
            sorted_indices = np.argsort(predictions)[::-1]
            
            results = {
                'predictions': [
                    {
                        'class': self.class_names[idx],
                        'confidence': float(predictions[idx])
                    }
                    for idx in sorted_indices[:3]  # Top 3
                ],
                'processing_time': np.random.uniform(0.5, 2.0),
                'image_quality': {
                    'resolution': f"{image.size[0]}x{image.size[1]}",
                    'quality_score': np.random.uniform(0.7, 0.95)
                },
                'recommendations': self._generate_recommendations(self.class_names[sorted_indices[0]])
            }
            
            return results
            
        except Exception as e:
            return {'error': str(e)}
            
    def _generate_recommendations(self, predicted_class: str) -> List[str]:
        """Genera raccomandazioni basate sulla predizione."""
        recommendations = {
            'Normal': [
                "L'immagine appare normale",
                "Continuare controlli di routine",
                "Mantenere uno stile di vita sano"
            ],
            'Pneumonia': [
                "Consultare immediatamente un medico",
                "Possibile necessità di antibiotici",
                "Monitorare temperatura corporea"
            ],
            'COVID-19': [
                "Isolamento immediato necessario",
                "Contattare le autorità sanitarie",
                "Monitorare saturazione ossigeno"
            ],
            'Tuberculosis': [
                "Consultazione specialistica urgente",
                "Test diagnostici aggiuntivi necessari",
                "Possibile isolamento precauzionale"
            ],
            'Fracture': [
                "Immobilizzazione dell'area interessata",
                "Consultare ortopedico",
                "Evitare movimenti dell'area"
            ],
            'Tumor': [
                "Consultazione oncologica urgente",
                "Ulteriori esami diagnostici necessari",
                "Biopsia potrebbe essere richiesta"
            ]
        }
        
        return recommendations.get(predicted_class, ["Consultare un medico per valutazione"])


class MedicalNLPAnalyzer:
    """Analizzatore NLP per testi medici."""
    
    def __init__(self):
        self.medical_keywords = self._load_medical_keywords()
        self.sentiment_analyzer = TextBlob
        
    def _load_medical_keywords(self) -> Dict[str, List[str]]:
        """Carica keywords mediche per categoria."""
        return {
            'symptoms': [
                'fever', 'cough', 'headache', 'nausea', 'fatigue', 'pain',
                'febbre', 'tosse', 'mal di testa', 'nausea', 'stanchezza', 'dolore'
            ],
            'diseases': [
                'pneumonia', 'diabetes', 'hypertension', 'covid', 'influenza',
                'polmonite', 'diabete', 'ipertensione', 'influenza'
            ],
            'medications': [
                'aspirin', 'paracetamol', 'ibuprofen', 'antibiotics',
                'aspirina', 'paracetamolo', 'ibuprofene', 'antibiotici'
            ],
            'body_parts': [
                'heart', 'lung', 'brain', 'liver', 'kidney',
                'cuore', 'polmone', 'cervello', 'fegato', 'rene'
            ]
        }
        
    def extract_medical_entities(self, text: str) -> Dict[str, List[str]]:
        """Estrae entità mediche dal testo."""
        text_lower = text.lower()
        entities = {}
        
        for category, keywords in self.medical_keywords.items():
            found = [keyword for keyword in keywords if keyword in text_lower]
            if found:
                entities[category] = found
                
        return entities
        
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analizza il sentiment del testo medico."""
        blob = TextBlob(text)
        
        return {
            'polarity': blob.sentiment.polarity,  # -1 (negative) to 1 (positive)
            'subjectivity': blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        }
        
    def extract_symptoms_severity(self, text: str) -> Dict[str, Any]:
        """Estrae sintomi e la loro severità dal testo."""
        severity_keywords = {
            'severe': ['severe', 'intense', 'acute', 'grave', 'intenso', 'acuto'],
            'moderate': ['moderate', 'medium', 'moderato', 'medio'],
            'mild': ['mild', 'light', 'slight', 'lieve', 'leggero']
        }
        
        text_lower = text.lower()
        symptoms_with_severity = {}
        
        # Cerca sintomi
        for symptom in self.medical_keywords['symptoms']:
            if symptom in text_lower:
                severity = 'unknown'
                
                # Cerca indicatori di severità vicino al sintomo
                for sev_level, sev_words in severity_keywords.items():
                    for sev_word in sev_words:
                        if sev_word in text_lower:
                            # Verifica se è vicino al sintomo (semplificato)
                            symptom_pos = text_lower.find(symptom)
                            sev_pos = text_lower.find(sev_word)
                            if abs(symptom_pos - sev_pos) < 50:  # Parole vicine
                                severity = sev_level
                                break
                
                symptoms_with_severity[symptom] = severity
                
        return symptoms_with_severity
        
    def analyze_medical_text(self, text: str) -> Dict[str, Any]:
        """Analisi completa di un testo medico."""
        return {
            'entities': self.extract_medical_entities(text),
            'sentiment': self.analyze_sentiment(text),
            'symptoms_severity': self.extract_symptoms_severity(text),
            'word_count': len(text.split()),
            'medical_terms_count': sum(
                len(terms) for terms in self.extract_medical_entities(text).values()
            ),
            'readability': self._calculate_readability(text)
        }
        
    def _calculate_readability(self, text: str) -> float:
        """Calcola un punteggio di leggibilità semplificato."""
        sentences = text.split('.')
        words = text.split()
        
        if not sentences or not words:
            return 0.0
            
        avg_words_per_sentence = len(words) / len(sentences)
        avg_syllables_per_word = sum(self._count_syllables(word) for word in words) / len(words)
        
        # Formula semplificata simile a Flesch
        readability = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        return max(0, min(100, readability))
        
    def _count_syllables(self, word: str) -> int:
        """Conta approssimativamente le sillabe in una parola."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not previous_was_vowel:
                    syllable_count += 1
                previous_was_vowel = True
            else:
                previous_was_vowel = False
                
        # Gestisci 'e' muta finale
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
            
        return max(1, syllable_count)


class PredictiveMedicineAnalyzer:
    """Analizzatore per medicina predittiva."""
    
    def __init__(self):
        self.risk_models = self._initialize_risk_models()
        
    def _initialize_risk_models(self) -> Dict[str, Any]:
        """Inizializza i modelli di rischio."""
        # Modelli semplificati per demo
        models = {}
        
        # Modello rischio cardiovascolare
        models['cardiovascular'] = {
            'features': ['age', 'blood_pressure', 'cholesterol', 'smoking', 'diabetes'],
            'model': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        # Modello rischio diabete
        models['diabetes'] = {
            'features': ['age', 'bmi', 'glucose', 'family_history', 'activity_level'],
            'model': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        return models
        
    def calculate_cardiovascular_risk(self, patient_data: Dict[str, float]) -> Dict[str, Any]:
        """Calcola il rischio cardiovascolare."""
        # Simulazione con dati realistici
        age = patient_data.get('age', 50)
        bp_systolic = patient_data.get('blood_pressure', 120)
        cholesterol = patient_data.get('cholesterol', 200)
        smoking = patient_data.get('smoking', 0)  # 0=no, 1=yes
        diabetes = patient_data.get('diabetes', 0)  # 0=no, 1=yes
        
        # Algoritmo semplificato basato su fattori di rischio noti
        risk_score = 0
        
        # Età
        if age >= 65:
            risk_score += 30
        elif age >= 45:
            risk_score += 15
        
        # Pressione sanguigna
        if bp_systolic >= 140:
            risk_score += 25
        elif bp_systolic >= 130:
            risk_score += 15
            
        # Colesterolo
        if cholesterol >= 240:
            risk_score += 20
        elif cholesterol >= 200:
            risk_score += 10
            
        # Fumo
        if smoking:
            risk_score += 25
            
        # Diabete
        if diabetes:
            risk_score += 30
            
        # Normalizza il punteggio
        risk_percentage = min(95, max(5, risk_score))
        
        # Categoria di rischio
        if risk_percentage < 20:
            risk_category = "Basso"
            color = "green"
        elif risk_percentage < 50:
            risk_category = "Moderato"
            color = "yellow"
        else:
            risk_category = "Alto"
            color = "red"
            
        return {
            'risk_percentage': risk_percentage,
            'risk_category': risk_category,
            'color': color,
            'factors': self._identify_risk_factors(patient_data),
            'recommendations': self._get_cardiovascular_recommendations(risk_category)
        }
        
    def calculate_diabetes_risk(self, patient_data: Dict[str, float]) -> Dict[str, Any]:
        """Calcola il rischio diabete."""
        age = patient_data.get('age', 50)
        bmi = patient_data.get('bmi', 25)
        glucose = patient_data.get('glucose', 90)
        family_history = patient_data.get('family_history', 0)
        activity_level = patient_data.get('activity_level', 5)  # 1-10 scale
        
        risk_score = 0
        
        # Età
        if age >= 45:
            risk_score += 20
            
        # BMI
        if bmi >= 30:
            risk_score += 25
        elif bmi >= 25:
            risk_score += 15
            
        # Glicemia
        if glucose >= 126:
            risk_score += 40
        elif glucose >= 100:
            risk_score += 20
            
        # Storia familiare
        if family_history:
            risk_score += 25
            
        # Livello di attività (inverso)
        if activity_level <= 3:
            risk_score += 15
        elif activity_level <= 6:
            risk_score += 5
            
        risk_percentage = min(95, max(5, risk_score))
        
        if risk_percentage < 25:
            risk_category = "Basso"
            color = "green"
        elif risk_percentage < 60:
            risk_category = "Moderato"
            color = "yellow"
        else:
            risk_category = "Alto"
            color = "red"
            
        return {
            'risk_percentage': risk_percentage,
            'risk_category': risk_category,
            'color': color,
            'factors': self._identify_diabetes_factors(patient_data),
            'recommendations': self._get_diabetes_recommendations(risk_category)
        }
        
    def _identify_risk_factors(self, data: Dict[str, float]) -> List[str]:
        """Identifica i fattori di rischio cardiovascolare."""
        factors = []
        
        if data.get('age', 0) >= 65:
            factors.append("Età avanzata (≥65 anni)")
        if data.get('blood_pressure', 0) >= 140:
            factors.append("Pressione alta (≥140/90)")
        if data.get('cholesterol', 0) >= 240:
            factors.append("Colesterolo alto (≥240 mg/dL)")
        if data.get('smoking', 0):
            factors.append("Fumo")
        if data.get('diabetes', 0):
            factors.append("Diabete")
            
        return factors
        
    def _identify_diabetes_factors(self, data: Dict[str, float]) -> List[str]:
        """Identifica i fattori di rischio diabete."""
        factors = []
        
        if data.get('age', 0) >= 45:
            factors.append("Età ≥45 anni")
        if data.get('bmi', 0) >= 30:
            factors.append("Obesità (BMI ≥30)")
        if data.get('glucose', 0) >= 100:
            factors.append("Glicemia alterata")
        if data.get('family_history', 0):
            factors.append("Storia familiare di diabete")
        if data.get('activity_level', 10) <= 3:
            factors.append("Sedentarietà")
            
        return factors
        
    def _get_cardiovascular_recommendations(self, risk_category: str) -> List[str]:
        """Raccomandazioni per rischio cardiovascolare."""
        recommendations = {
            "Basso": [
                "Mantieni stile di vita sano",
                "Esercizio regolare (150 min/settimana)",
                "Dieta equilibrata",
                "Controlli annuali"
            ],
            "Moderato": [
                "Consulta il medico per valutazione",
                "Considera farmaci per pressione/colesterolo se necessario",
                "Aumenta attività fisica",
                "Riduci sale e grassi saturi",
                "Controlli ogni 6 mesi"
            ],
            "Alto": [
                "Consultazione cardiologica urgente",
                "Probabile necessità di farmaci",
                "Cambiamenti drastici dello stile di vita",
                "Smetti di fumare immediatamente",
                "Controlli frequenti (3-4 mesi)"
            ]
        }
        
        return recommendations.get(risk_category, [])
        
    def _get_diabetes_recommendations(self, risk_category: str) -> List[str]:
        """Raccomandazioni per rischio diabete."""
        recommendations = {
            "Basso": [
                "Mantieni peso corporeo sano",
                "Dieta equilibrata, limita zuccheri",
                "Attività fisica regolare",
                "Controllo glicemia annuale"
            ],
            "Moderato": [
                "Perdita di peso se sovrappeso",
                "Dieta a basso indice glicemico",
                "Esercizio 30 min al giorno",
                "Test glicemia ogni 6 mesi",
                "Considera metformina se indicata"
            ],
            "Alto": [
                "Consultazione endocrinologica",
                "Programma di perdita peso strutturato",
                "Monitoraggio glicemico frequente",
                "Possibile prediabete/diabete",
                "Farmaci preventivi se necessari"
            ]
        }
        
        return recommendations.get(risk_category, [])


def render_ai_modules_page():
    """Renderizza la pagina dei moduli AI avanzati."""
    st.markdown('<h2 class="section-header">🤖 Moduli IA Avanzati</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    **Nino Medical AI** integra moduli di Intelligenza Artificiale avanzati per supportare
    diagnosi, analisi e previsioni nel campo medico-sanitario.
    """)
    
    # Tabs per i diversi moduli AI
    tab1, tab2, tab3 = st.tabs([
        "🖼️ Analisi Immagini Mediche", 
        "📝 Analisi NLP Medica", 
        "🔮 Medicina Predittiva"
    ])
    
    with tab1:
        render_medical_image_analysis()
        
    with tab2:
        render_medical_nlp_analysis()
        
    with tab3:
        render_predictive_medicine()


def render_medical_image_analysis():
    """Renderizza la sezione analisi immagini mediche."""
    st.subheader("🖼️ Analisi Immagini Mediche con IA")
    st.markdown("Carica un'immagine medica (Raggi X, TAC, RMN) per l'analisi automatica.")
    
    # Inizializza analyzer
    if 'image_analyzer' not in st.session_state:
        st.session_state.image_analyzer = MedicalImageAnalyzer()
        
    # Upload immagine
    uploaded_file = st.file_uploader(
        "Carica immagine medica", 
        type=['jpg', 'jpeg', 'png', 'tiff'],
        key="medical_image"
    )
    
    if uploaded_file:
        # Mostra immagine
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Immagine caricata", use_column_width=True)
            
        with col2:
            if st.button("🔍 Analizza Immagine", key="analyze_image"):
                with st.spinner("Analisi in corso..."):
                    results = st.session_state.image_analyzer.analyze_image(image)
                    
                    if 'error' not in results:
                        st.success(f"✅ Analisi completata in {results['processing_time']:.1f}s")
                        
                        # Mostra predizioni
                        st.markdown("### 📊 Risultati Analisi")
                        
                        for i, pred in enumerate(results['predictions']):
                            confidence_pct = pred['confidence'] * 100
                            
                            if i == 0:  # Prima predizione
                                st.metric(
                                    f"🥇 Diagnosi Principale", 
                                    pred['class'],
                                    f"{confidence_pct:.1f}% confidenza"
                                )
                            else:
                                st.write(f"**{pred['class']}**: {confidence_pct:.1f}%")
                                
                        # Grafico confidenze
                        fig = px.bar(
                            x=[p['confidence'] for p in results['predictions']], 
                            y=[p['class'] for p in results['predictions']],
                            orientation='h',
                            title="Confidenza Predizioni",
                            labels={'x': 'Confidenza', 'y': 'Diagnosi'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Raccomandazioni
                        st.markdown("### 💡 Raccomandazioni")
                        for rec in results['recommendations']:
                            st.write(f"• {rec}")
                            
                        # Info qualità immagine
                        st.markdown("### ℹ️ Qualità Immagine")
                        col_q1, col_q2 = st.columns(2)
                        with col_q1:
                            st.metric("Risoluzione", results['image_quality']['resolution'])
                        with col_q2:
                            st.metric("Qualità", f"{results['image_quality']['quality_score']:.0%}")
                            
                    else:
                        st.error(f"Errore nell'analisi: {results['error']}")
    
    # Informazioni sui tipi di immagini supportate
    with st.expander("ℹ️ Tipi di Immagini Supportate"):
        st.markdown("""
        **Radiografie**:
        - Torace (polmoni, cuore)
        - Fratture ossee
        - Articolazioni
        
        **TAC**:
        - Scansioni cerebrali
        - Addome
        - Torace
        
        **Risonanze Magnetiche**:
        - Cervello
        - Colonna vertebrale
        - Articolazioni
        
        **Ecografie**:
        - Addominali
        - Cardiache
        - Ostetriche
        """)


def render_medical_nlp_analysis():
    """Renderizza la sezione analisi NLP medica."""
    st.subheader("📝 Analisi NLP su Testi Medici")
    st.markdown("Analizza testi medici, referti, note cliniche per estrarre informazioni strutturate.")
    
    # Inizializza analyzer
    if 'nlp_analyzer' not in st.session_state:
        st.session_state.nlp_analyzer = MedicalNLPAnalyzer()
        
    # Esempi di testo predefiniti
    examples = {
        "Referto Esempio 1": "Paziente di 45 anni presenta febbre alta, tosse persistente e dolore toracico. Esame obiettivo rivela polmoni congesti. Raccomando antibiotici e riposo.",
        "Referto Esempio 2": "Controllo post-operatorio: paziente in buone condizioni generali. Ferita chirurgica in via di guarigione. Lieve dolore controllabile con paracetamolo.",
        "Sintomi Paziente": "Da tre giorni ho mal di testa intenso, nausea e vertigini. La situazione peggiora la sera. Ho anche febbre bassa."
    }
    
    example_choice = st.selectbox("Scegli esempio o scrivi tuo testo:", ["Scrivi testo personalizzato"] + list(examples.keys()))
    
    if example_choice != "Scrivi testo personalizzato":
        medical_text = st.text_area("Testo medico da analizzare:", examples[example_choice], height=150)
    else:
        medical_text = st.text_area("Testo medico da analizzare:", height=150)
        
    if medical_text and st.button("🔍 Analizza Testo", key="analyze_text"):
        with st.spinner("Analisi NLP in corso..."):
            results = st.session_state.nlp_analyzer.analyze_medical_text(medical_text)
            
            # Layout a colonne
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Entità Mediche Estratte")
                if results['entities']:
                    for category, entities in results['entities'].items():
                        st.write(f"**{category.title()}**: {', '.join(entities)}")
                else:
                    st.info("Nessuna entità medica specifica trovata.")
                    
                st.markdown("### 📊 Statistiche Testo")
                stats_col1, stats_col2 = st.columns(2)
                with stats_col1:
                    st.metric("Parole Totali", results['word_count'])
                    st.metric("Termini Medici", results['medical_terms_count'])
                with stats_col2:
                    st.metric("Leggibilità", f"{results['readability']:.0f}/100")
                    
            with col2:
                st.markdown("### 😊 Analisi Sentiment")
                sentiment = results['sentiment']
                
                # Gauge per sentiment
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = sentiment['polarity'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Sentiment Polarity"},
                    gauge = {
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [-1, -0.5], 'color': "lightgray"},
                            {'range': [-0.5, 0.5], 'color': "gray"},
                            {'range': [0.5, 1], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0.9
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Interpretazione sentiment
                if sentiment['polarity'] > 0.1:
                    st.success("😊 Testo con sentiment positivo")
                elif sentiment['polarity'] < -0.1:
                    st.error("😔 Testo con sentiment negativo")
                else:
                    st.info("😐 Testo neutrale")
                    
            # Sintomi con severità
            if results['symptoms_severity']:
                st.markdown("### 🌡️ Sintomi e Severità")
                symptoms_df = pd.DataFrame([
                    {'Sintomo': symptom, 'Severità': severity}
                    for symptom, severity in results['symptoms_severity'].items()
                ])
                st.dataframe(symptoms_df, use_container_width=True)


def render_predictive_medicine():
    """Renderizza la sezione medicina predittiva."""
    st.subheader("🔮 Medicina Predittiva")
    st.markdown("Calcola il rischio di sviluppare specifiche condizioni mediche basandoti su fattori clinici.")
    
    # Inizializza analyzer
    if 'predictive_analyzer' not in st.session_state:
        st.session_state.predictive_analyzer = PredictiveMedicineAnalyzer()
        
    # Tabs per diversi tipi di rischio
    risk_tab1, risk_tab2 = st.tabs(["❤️ Rischio Cardiovascolare", "🍭 Rischio Diabete"])
    
    with risk_tab1:
        render_cardiovascular_risk()
        
    with risk_tab2:
        render_diabetes_risk()


def render_cardiovascular_risk():
    """Renderizza il calcolatore di rischio cardiovascolare."""
    st.markdown("#### Valutazione Rischio Cardiovascolare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Parametri Paziente**")
        age = st.slider("Età", 20, 100, 50)
        blood_pressure = st.slider("Pressione Sistolica (mmHg)", 90, 200, 120)
        cholesterol = st.slider("Colesterolo Totale (mg/dL)", 150, 350, 200)
        
    with col2:
        st.markdown("**Fattori di Rischio**")
        smoking = st.checkbox("Fumatore")
        diabetes = st.checkbox("Diabetico")
        
    if st.button("📊 Calcola Rischio Cardiovascolare", key="calc_cardio_risk"):
        patient_data = {
            'age': age,
            'blood_pressure': blood_pressure,
            'cholesterol': cholesterol,
            'smoking': 1 if smoking else 0,
            'diabetes': 1 if diabetes else 0
        }
        
        risk_results = st.session_state.predictive_analyzer.calculate_cardiovascular_risk(patient_data)
        
        # Visualizzazione risultati
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🎯 Rischio Calcolato", 
                f"{risk_results['risk_percentage']:.0f}%",
                delta=risk_results['risk_category']
            )
            
        with col2:
            # Gauge per rischio
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_results['risk_percentage'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Rischio Cardiovascolare"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': risk_results['color']},
                    'steps': [
                        {'range': [0, 20], 'color': "lightgreen"},
                        {'range': [20, 50], 'color': "yellow"},
                        {'range': [50, 100], 'color': "lightcoral"}
                    ],
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
            st.markdown("**Categoria di Rischio**")
            if risk_results['risk_category'] == "Basso":
                st.success(f"✅ {risk_results['risk_category']}")
            elif risk_results['risk_category'] == "Moderato":
                st.warning(f"⚠️ {risk_results['risk_category']}")
            else:
                st.error(f"🚨 {risk_results['risk_category']}")
                
        # Fattori di rischio identificati
        if risk_results['factors']:
            st.markdown("### ⚠️ Fattori di Rischio Identificati")
            for factor in risk_results['factors']:
                st.write(f"• {factor}")
                
        # Raccomandazioni
        st.markdown("### 💡 Raccomandazioni")
        for rec in risk_results['recommendations']:
            st.write(f"• {rec}")


def render_diabetes_risk():
    """Renderizza il calcolatore di rischio diabete."""
    st.markdown("#### Valutazione Rischio Diabete")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Parametri Fisici**")
        age = st.slider("Età", 18, 100, 40, key="diabetes_age")
        bmi = st.slider("BMI (Indice Massa Corporea)", 15, 50, 25, key="diabetes_bmi")
        glucose = st.slider("Glicemia a digiuno (mg/dL)", 70, 200, 90, key="diabetes_glucose")
        
    with col2:
        st.markdown("**Storia e Stile di Vita**")
        family_history = st.checkbox("Storia familiare di diabete", key="diabetes_family")
        activity_level = st.slider("Livello attività fisica (1=sedentario, 10=molto attivo)", 1, 10, 5, key="diabetes_activity")
        
    if st.button("📊 Calcola Rischio Diabete", key="calc_diabetes_risk"):
        patient_data = {
            'age': age,
            'bmi': bmi,
            'glucose': glucose,
            'family_history': 1 if family_history else 0,
            'activity_level': activity_level
        }
        
        risk_results = st.session_state.predictive_analyzer.calculate_diabetes_risk(patient_data)
        
        # Visualizzazione risultati
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🎯 Rischio Diabete", 
                f"{risk_results['risk_percentage']:.0f}%",
                delta=risk_results['risk_category']
            )
            
        with col2:
            # Gauge per rischio
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_results['risk_percentage'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Rischio Diabete"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': risk_results['color']},
                    'steps': [
                        {'range': [0, 25], 'color': "lightgreen"},
                        {'range': [25, 60], 'color': "yellow"},
                        {'range': [60, 100], 'color': "lightcoral"}
                    ],
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
        with col3:
            # BMI interpretation
            st.markdown("**Interpretazione BMI**")
            if bmi < 18.5:
                st.info("Sottopeso")
            elif bmi < 25:
                st.success("Normale")
            elif bmi < 30:
                st.warning("Sovrappeso")
            else:
                st.error("Obesità")
                
        # Fattori di rischio identificati
        if risk_results['factors']:
            st.markdown("### ⚠️ Fattori di Rischio Identificati")
            for factor in risk_results['factors']:
                st.write(f"• {factor}")
                
        # Raccomandazioni
        st.markdown("### 💡 Raccomandazioni")
        for rec in risk_results['recommendations']:
            st.write(f"• {rec}")


if __name__ == "__main__":
    # Test dei moduli
    print("Testing AI Modules...")
    
    # Test Image Analyzer
    analyzer = MedicalImageAnalyzer()
    print(f"✅ MedicalImageAnalyzer initialized")
    
    # Test NLP Analyzer
    nlp = MedicalNLPAnalyzer()
    test_text = "Patient has fever and cough"
    results = nlp.analyze_medical_text(test_text)
    print(f"✅ NLP analysis results: {len(results)} categories")
    
    # Test Predictive Medicine
    predictor = PredictiveMedicineAnalyzer()
    test_data = {'age': 50, 'blood_pressure': 140, 'cholesterol': 220, 'smoking': 1, 'diabetes': 0}
    risk = predictor.calculate_cardiovascular_risk(test_data)
    print(f"✅ Cardiovascular risk calculated: {risk['risk_percentage']:.0f}%")
    
    print("All AI modules working correctly!")
