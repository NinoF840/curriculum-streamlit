"""
Nino Medical AI - Dashboard Analytics Avanzata
===============================================

Dashboard interattiva per visualizzazioni avanzate e analytics predittive.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


class AdvancedAnalyticsDashboard:
    """Dashboard per analytics avanzate."""
    
    def __init__(self):
        self.patient_data = self._load_patient_data()
        self.symptoms_data = self._load_symptoms_data()
        
    def _load_patient_data(self, num_patients: int = 200) -> pd.DataFrame:
        """Genera un dataset di pazienti sintetici."""
        np.random.seed(42)
        
        data = {
            'age': np.random.randint(20, 85, num_patients),
            'gender': np.random.choice(['Male', 'Female'], num_patients, p=[0.5, 0.5]),
            'bmi': np.random.uniform(18, 40, num_patients),
            'blood_pressure_systolic': np.random.randint(90, 180, num_patients),
            'blood_pressure_diastolic': np.random.randint(60, 110, num_patients),
            'cholesterol': np.random.randint(150, 300, num_patients),
            'glucose': np.random.randint(70, 200, num_patients),
            'smoker': np.random.choice([True, False], num_patients, p=[0.3, 0.7]),
            'disease': np.random.choice(
                ['Healthy', 'Hypertension', 'Diabetes', 'Heart Disease', 'Flu'], 
                num_patients, 
                p=[0.4, 0.2, 0.15, 0.1, 0.15]
            ),
            'admission_date': [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(num_patients)]
        }
        
        return pd.DataFrame(data)
        
    def _load_symptoms_data(self, num_records: int = 500) -> pd.DataFrame:
        """Genera un dataset di sintomi riportati."""
        np.random.seed(42)
        
        symptoms = [
            'fever', 'cough', 'headache', 'fatigue', 'sore throat', 'muscle pain', 'shortness of breath'
        ]
        
        data = {
            'symptom': np.random.choice(symptoms, num_records),
            'severity': np.random.choice(['Mild', 'Moderate', 'Severe'], num_records, p=[0.4, 0.4, 0.2]),
            'date': [datetime.now() - timedelta(days=np.random.randint(1, 180)) for _ in range(num_records)]
        }
        
        return pd.DataFrame(data)
        
    def render(self):
        """Renderizza la dashboard completa."""
        st.markdown('<h2 class="section-header">📈 Dashboard Analytics Predittiva</h2>', unsafe_allow_html=True)
        st.markdown("Visualizzazioni interattive e analisi predittive su dati sanitari aggregati.")
        
        # Filtri globali
        st.sidebar.title("Filtri Dashboard")
        age_filter = st.sidebar.slider("Filtro Età", 20, 85, (20, 85))
        gender_filter = st.sidebar.multiselect("Filtro Genere", self.patient_data['gender'].unique(), default=self.patient_data['gender'].unique())
        disease_filter = st.sidebar.multiselect("Filtro Patologia", self.patient_data['disease'].unique(), default=self.patient_data['disease'].unique())
        
        # Applica filtri
        filtered_data = self.patient_data[
            (self.patient_data['age'] >= age_filter[0]) & 
            (self.patient_data['age'] <= age_filter[1]) & 
            (self.patient_data['gender'].isin(gender_filter)) & 
            (self.patient_data['disease'].isin(disease_filter))
        ]
        
        # Metriche principali
        st.markdown("### 📊 Metriche Chiave")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pazienti Totali", len(filtered_data))
        with col2:
            st.metric("Età Media", f"{filtered_data['age'].mean():.1f} anni")
        with col3:
            st.metric("Pressione Media", f"{filtered_data['blood_pressure_systolic'].mean():.0f}/{filtered_data['blood_pressure_diastolic'].mean():.0f}")
        with col4:
            st.metric("Colesterolo Medio", f"{filtered_data['cholesterol'].mean():.0f} mg/dL")
            
        # Visualizzazioni
        st.markdown("### 🎨 Visualizzazioni Interattive")
        
        # Layout a 2 colonne
        vis_col1, vis_col2 = st.columns(2)
        
        with vis_col1:
            self.plot_age_distribution(filtered_data)
            self.plot_disease_correlation(filtered_data)
            
        with vis_col2:
            self.plot_disease_distribution(filtered_data)
            self.plot_symptom_trends()
            
        # Analisi predittiva
        st.markdown("### 🔮 Analisi Predittiva")
        self.predictive_analysis_section(filtered_data)
        
    def plot_age_distribution(self, data: pd.DataFrame):
        """Plot distribuzione età."""
        fig = px.histogram(
            data, 
            x='age', 
            color='gender', 
            title="Distribuzione Età per Genere",
            labels={'age': 'Età', 'gender': 'Genere'},
            marginal='box'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    def plot_disease_distribution(self, data: pd.DataFrame):
        """Plot distribuzione patologie."""
        fig = px.pie(
            data, 
            names='disease', 
            title="Distribuzione Patologie",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
        
    def plot_disease_correlation(self, data: pd.DataFrame):
        """Plot correlazione tra patologie e fattori di rischio."""
        correlation_data = data[['age', 'bmi', 'blood_pressure_systolic', 'cholesterol', 'glucose']]
        correlation_matrix = correlation_data.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Viridis'
        ))
        
        fig.update_layout(title="Matrice di Correlazione Fattori di Rischio")
        st.plotly_chart(fig, use_container_width=True)
        
    def plot_symptom_trends(self):
        """Plot andamento temporale dei sintomi."""
        self.symptoms_data['month'] = self.symptoms_data['date'].dt.to_period('M')
        symptom_trends = self.symptoms_data.groupby(['month', 'symptom']).size().reset_index(name='count')
        symptom_trends['month'] = symptom_trends['month'].astype(str)
        
        fig = px.line(
            symptom_trends, 
            x='month', 
            y='count', 
            color='symptom', 
            title="Andamento Temporale Sintomi",
            labels={'month': 'Mese', 'count': 'Numero Casi', 'symptom': 'Sintomo'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
    def predictive_analysis_section(self, data: pd.DataFrame):
        """Sezione di analisi predittiva."""
        st.markdown("#### Previsione Insorgenza Epidemie")
        
        # Simula una previsione
        last_month_cases = self.symptoms_data[self.symptoms_data['date'] > datetime.now() - timedelta(days=30)].shape[0]
        prev_month_cases = self.symptoms_data[
            (self.symptoms_data['date'] > datetime.now() - timedelta(days=60)) & 
            (self.symptoms_data['date'] < datetime.now() - timedelta(days=30))
        ].shape[0]
        
        trend = (last_month_cases - prev_month_cases) / prev_month_cases if prev_month_cases > 0 else 0
        
        # Messaggio di allerta
        if trend > 0.5:
            st.error("🚨 Allerta: Trend in forte aumento! Possibile focolaio.")
        elif trend > 0.1:
            st.warning("⚠️ Attenzione: Trend in aumento.")
        else:
            st.success("✅ Trend stabile o in diminuzione.")
            
        # Grafico previsione
        months = [(datetime.now() + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(3)]
        predicted_cases = [last_month_cases * (1 + trend) ** i for i in range(3)]
        
        fig = go.Figure() 
        fig.add_trace(go.Scatter(x=months, y=predicted_cases, mode='lines+markers', name='Previsione Casi'))
        fig.update_layout(title="Previsione Casi Sintomatici (Prossimi 3 Mesi)")
        st.plotly_chart(fig, use_container_width=True)


def render_analytics_dashboard_page():
    """Renderizza la pagina della dashboard di analytics."""
    dashboard = AdvancedAnalyticsDashboard()
    dashboard.render()


if __name__ == "__main__":
    # Test della dashboard
    print("Testing Analytics Dashboard...")
    dashboard = AdvancedAnalyticsDashboard()
    print(f"✅ Dashboard initialized with {len(dashboard.patient_data)} patients.")
    print("Dashboard ready for rendering.")
