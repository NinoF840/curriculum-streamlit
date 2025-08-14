#!/usr/bin/env python3
"""
Analytics Dashboard for Nino Medical AI
=======================================

Dashboard component per visualizzare le metriche di Google Analytics
all'interno dell'app per utenti admin.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
import json

# Simulazione dati analytics (in produzione userai Google Analytics Reporting API)
class AnalyticsDashboard:
    """Dashboard per visualizzare metriche analytics."""
    
    def __init__(self):
        self.mock_data = self._generate_mock_data()
    
    def _generate_mock_data(self) -> Dict[str, Any]:
        """Genera dati mock per demo dashboard."""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30), 
            end=datetime.now(), 
            freq='D'
        )
        
        return {
            # Visitatori
            'visitors': {
                'daily_visitors': [np.random.randint(50, 200) for _ in dates],
                'unique_visitors': [np.random.randint(30, 150) for _ in dates],
                'returning_visitors': [np.random.randint(10, 50) for _ in dates],
                'dates': dates
            },
            
            # Page Views
            'page_views': {
                'total_views': [np.random.randint(100, 500) for _ in dates],
                'pages': {
                    '/dashboard': np.random.randint(2000, 5000),
                    '/databases': np.random.randint(800, 2000),
                    '/predictive_medicine': np.random.randint(600, 1500),
                    '/clinical_trials': np.random.randint(400, 1000),
                    '/pro_features': np.random.randint(300, 800),
                    '/welcome': np.random.randint(1000, 3000)
                }
            },
            
            # User Engagement
            'engagement': {
                'avg_session_duration': '4:32',
                'bounce_rate': 0.35,
                'pages_per_session': 3.2,
                'conversion_rate': 0.042
            },
            
            # Business Metrics
            'business': {
                'pro_conversions': [np.random.randint(0, 5) for _ in dates[-7:]],  # Ultimi 7 giorni
                'demo_interactions': [np.random.randint(10, 50) for _ in dates[-7:]],
                'search_queries': [np.random.randint(20, 100) for _ in dates[-7:]],
                'ai_analyses': [np.random.randint(5, 30) for _ in dates[-7:]]
            },
            
            # Traffic Sources
            'traffic_sources': {
                'organic': 45.2,
                'direct': 28.7,
                'referral': 15.3,
                'social': 8.5,
                'email': 2.3
            },
            
            # Device/Browser
            'technical': {
                'devices': {
                    'desktop': 67.4,
                    'mobile': 28.9,
                    'tablet': 3.7
                },
                'browsers': {
                    'chrome': 52.3,
                    'firefox': 21.8,
                    'safari': 15.2,
                    'edge': 7.9,
                    'other': 2.8
                }
            }
        }
    
    def render_dashboard(self):
        """Renders the complete analytics dashboard."""
        st.markdown('<h2 class="section-header">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
        
        # Overview metrics
        self.render_overview_metrics()
        
        # Tabs per diverse sezioni
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👥 Visitatori", 
            "📄 Pagine", 
            "💼 Business", 
            "🌐 Traffico",
            "⚙️ Tecnico"
        ])
        
        with tab1:
            self.render_visitors_analytics()
        
        with tab2:
            self.render_page_analytics()
            
        with tab3:
            self.render_business_analytics()
            
        with tab4:
            self.render_traffic_analytics()
            
        with tab5:
            self.render_technical_analytics()
    
    def render_overview_metrics(self):
        """Overview metrics cards."""
        st.markdown("### 📈 Metriche Principali (Ultimi 30 giorni)")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_visitors = sum(self.mock_data['visitors']['daily_visitors'])
        total_views = sum(self.mock_data['page_views']['total_views'])
        pro_conversions = sum(self.mock_data['business']['pro_conversions'])
        avg_duration = self.mock_data['engagement']['avg_session_duration']
        bounce_rate = self.mock_data['engagement']['bounce_rate']
        
        with col1:
            st.metric("👥 Visitatori Totali", f"{total_visitors:,}", delta=f"+{np.random.randint(10,30)}%")
        
        with col2:
            st.metric("📄 Visualizzazioni", f"{total_views:,}", delta=f"+{np.random.randint(5,25)}%")
        
        with col3:
            st.metric("💎 Conversioni Pro", pro_conversions, delta=f"+{np.random.randint(1,8)}")
            
        with col4:
            st.metric("⏱️ Durata Media", avg_duration, delta=f"+{np.random.randint(10,45)}s")
        
        with col5:
            st.metric("📉 Bounce Rate", f"{bounce_rate:.1%}", delta=f"-{np.random.randint(1,8)}%")
    
    def render_visitors_analytics(self):
        """Visitor analytics section."""
        st.markdown("### 👥 Analisi Visitatori")
        
        # Trend visitatori
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Trend Visitatori Giornalieri")
            visitors_df = pd.DataFrame({
                'Data': self.mock_data['visitors']['dates'],
                'Visitatori Unici': self.mock_data['visitors']['unique_visitors'],
                'Visitatori Totali': self.mock_data['visitors']['daily_visitors'],
                'Visitatori di Ritorno': self.mock_data['visitors']['returning_visitors']
            })
            
            fig = px.line(visitors_df, x='Data', 
                         y=['Visitatori Unici', 'Visitatori Totali', 'Visitatori di Ritorno'],
                         title="Trend Visitatori")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🌍 Geolocalizzazione (Mock)")
            # Mock geographic data
            geo_data = pd.DataFrame({
                'Paese': ['Italia', 'USA', 'Germania', 'Francia', 'UK', 'Spagna'],
                'Visitatori': [1240, 890, 567, 445, 389, 234],
                'Percentuale': [42.3, 30.4, 19.3, 15.2, 13.3, 8.0]
            })
            
            fig = px.bar(geo_data, x='Paese', y='Visitatori', 
                        title="Visitatori per Paese")
            st.plotly_chart(fig, use_container_width=True)
        
        # Dettagli engagement
        st.markdown("#### 📈 Metriche di Engagement")
        
        engagement_cols = st.columns(4)
        
        with engagement_cols[0]:
            st.metric("⏱️ Durata Sessione", self.mock_data['engagement']['avg_session_duration'])
        with engagement_cols[1]:
            st.metric("📄 Pagine/Sessione", f"{self.mock_data['engagement']['pages_per_session']:.1f}")
        with engagement_cols[2]:
            st.metric("📉 Bounce Rate", f"{self.mock_data['engagement']['bounce_rate']:.1%}")
        with engagement_cols[3]:
            st.metric("💎 Tasso Conversione", f"{self.mock_data['engagement']['conversion_rate']:.2%}")
    
    def render_page_analytics(self):
        """Page analytics section.""" 
        st.markdown("### 📄 Analisi Pagine")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔝 Pagine Più Visitate")
            
            pages_data = pd.DataFrame([
                {'Pagina': page, 'Visualizzazioni': views} 
                for page, views in self.mock_data['page_views']['pages'].items()
            ]).sort_values('Visualizzazioni', ascending=False)
            
            fig = px.bar(pages_data, x='Visualizzazioni', y='Pagina', 
                        orientation='h', title="Visualizzazioni per Pagina")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("#### 📈 Trend Visualizzazioni Giornaliere")
            
            views_df = pd.DataFrame({
                'Data': self.mock_data['visitors']['dates'],
                'Visualizzazioni': self.mock_data['page_views']['total_views']
            })
            
            fig = px.line(views_df, x='Data', y='Visualizzazioni',
                         title="Visualizzazioni nel Tempo")
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabella dettagliata
        st.markdown("#### 📋 Dettagli Pagine")
        
        # Mock detailed page data
        detailed_pages = pd.DataFrame({
            'Pagina': list(self.mock_data['page_views']['pages'].keys()),
            'Visualizzazioni': list(self.mock_data['page_views']['pages'].values()),
            'Tempo Medio': [f"{np.random.randint(1,8)}:{np.random.randint(10,59):02d}" for _ in range(6)],
            'Bounce Rate': [f"{np.random.uniform(0.2, 0.6):.1%}" for _ in range(6)],
            'Exit Rate': [f"{np.random.uniform(0.3, 0.8):.1%}" for _ in range(6)]
        })
        
        st.dataframe(detailed_pages, use_container_width=True)
    
    def render_business_analytics(self):
        """Business metrics analytics."""
        st.markdown("### 💼 Metriche Business")
        
        # Conversioni Pro
        st.markdown("#### 💎 Conversioni Pro (Ultimi 7 giorni)")
        
        business_df = pd.DataFrame({
            'Data': pd.date_range(end=datetime.now(), periods=7, freq='D'),
            'Conversioni Pro': self.mock_data['business']['pro_conversions'],
            'Interazioni Demo': self.mock_data['business']['demo_interactions'],
            'Query Ricerca': self.mock_data['business']['search_queries'],
            'Analisi IA': self.mock_data['business']['ai_analyses']
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(business_df, x='Data', y='Conversioni Pro',
                        title="Conversioni Pro Giornaliere")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(business_df, x='Data', 
                         y=['Interazioni Demo', 'Query Ricerca', 'Analisi IA'],
                         title="Attività Utenti")
            st.plotly_chart(fig, use_container_width=True)
        
        # Funnel di conversione
        st.markdown("#### 🔄 Funnel di Conversione")
        
        funnel_data = pd.DataFrame({
            'Fase': ['Visitatori', 'Demo Interactions', 'Pro Features View', 'Conversioni'],
            'Utenti': [1000, 450, 180, 12],
            'Tasso': ['100%', '45%', '18%', '1.2%']
        })
        
        fig = px.funnel(funnel_data, x='Utenti', y='Fase', 
                       title="Funnel di Conversione Pro")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(funnel_data, use_container_width=True)
    
    def render_traffic_analytics(self):
        """Traffic sources analytics."""
        st.markdown("### 🌐 Sorgenti Traffico")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Sorgenti Principali")
            
            traffic_df = pd.DataFrame([
                {'Sorgente': source, 'Percentuale': percent}
                for source, percent in self.mock_data['traffic_sources'].items()
            ])
            
            fig = px.pie(traffic_df, names='Sorgente', values='Percentuale',
                        title="Distribuzione Sorgenti Traffico")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Trend Sorgenti (Mock)")
            
            # Mock trend data for different sources
            trend_dates = pd.date_range(end=datetime.now(), periods=14, freq='D')
            trend_df = pd.DataFrame({
                'Data': trend_dates,
                'Organic Search': [np.random.randint(20, 80) for _ in trend_dates],
                'Direct': [np.random.randint(15, 50) for _ in trend_dates],
                'Referral': [np.random.randint(5, 25) for _ in trend_dates]
            })
            
            fig = px.line(trend_df, x='Data', y=['Organic Search', 'Direct', 'Referral'],
                         title="Trend Sorgenti Traffico")
            st.plotly_chart(fig, use_container_width=True)
        
        # Dettagli sorgenti
        st.markdown("#### 📋 Dettagli Sorgenti")
        
        detailed_sources = pd.DataFrame({
            'Sorgente': ['Google Search', 'Direct Access', 'LinkedIn', 'GitHub', 'Email Campaign'],
            'Sessioni': [1250, 890, 340, 180, 75],
            'Nuovi Utenti': [980, 234, 298, 156, 67],
            'Durata Media': ['4:52', '3:21', '5:18', '6:45', '3:12'],
            'Conversioni': [8, 3, 2, 1, 0]
        })
        
        st.dataframe(detailed_sources, use_container_width=True)
    
    def render_technical_analytics(self):
        """Technical analytics (devices, browsers, etc.)."""
        st.markdown("### ⚙️ Analytics Tecnici")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📱 Dispositivi")
            
            devices_df = pd.DataFrame([
                {'Dispositivo': device, 'Percentuale': percent}
                for device, percent in self.mock_data['technical']['devices'].items()
            ])
            
            fig = px.pie(devices_df, names='Dispositivo', values='Percentuale',
                        title="Distribuzione Dispositivi")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🌐 Browser")
            
            browsers_df = pd.DataFrame([
                {'Browser': browser, 'Percentuale': percent}
                for browser, percent in self.mock_data['technical']['browsers'].items()
            ])
            
            fig = px.bar(browsers_df, x='Browser', y='Percentuale',
                        title="Utilizzo Browser")
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics
        st.markdown("#### ⚡ Performance dell'App")
        
        performance_metrics = pd.DataFrame({
            'Metrica': [
                'Tempo Caricamento Medio',
                'First Contentful Paint',
                'Time to Interactive', 
                'Core Web Vitals Score',
                'Error Rate'
            ],
            'Valore': ['2.1s', '1.3s', '3.2s', '92/100', '0.2%'],
            'Status': ['Buono', 'Ottimo', 'Buono', 'Ottimo', 'Ottimo'],
            'Trend': ['+0.3s', '-0.1s', '-0.5s', '+2 pt', '-0.1%']
        })
        
        st.dataframe(performance_metrics, use_container_width=True)
        
        # Real-time stats
        st.markdown("#### 🔴 Metriche in Tempo Reale")
        
        realtime_col1, realtime_col2, realtime_col3, realtime_col4 = st.columns(4)
        
        with realtime_col1:
            st.metric("👥 Utenti Attivi", np.random.randint(15, 45))
        with realtime_col2:
            st.metric("📄 Pagine Attive", np.random.randint(8, 25))
        with realtime_col3:
            st.metric("🌍 Paesi", np.random.randint(3, 12))
        with realtime_col4:
            st.metric("📱 Dispositivi", np.random.randint(10, 35))

def render_analytics_dashboard():
    """Main function to render analytics dashboard."""
    dashboard = AnalyticsDashboard()
    dashboard.render_dashboard()

def render_analytics_setup_guide():
    """Guide for setting up Google Analytics."""
    st.markdown("### 🔧 Configurazione Google Analytics")
    
    with st.expander("📋 Guida Setup", expanded=False):
        st.markdown("""
        #### 1. Configura Google Analytics 4
        
        1. Vai su [Google Analytics](https://analytics.google.com)
        2. Crea una proprietà GA4 per "Nino Medical AI"
        3. Configura un Data Stream per la tua app web
        4. Copia il **Measurement ID** (formato: G-XXXXXXXXXX)
        
        #### 2. Aggiorna Configurazione App
        
        ```python
        # In analytics_config.py
        GA4_MEASUREMENT_ID = "G-TUO-MEASUREMENT-ID"
        GA4_API_SECRET = "tuo-api-secret"  # opzionale
        ```
        
        #### 3. Eventi Personalizzati Configurati
        
        - **Visitatori**: page_view, session_start
        - **Business**: purchase, upgrade_view, trial_start
        - **Engagement**: pro_feature_usage, search, ai_analysis
        - **Content**: comment_submit, export, feedback_submit
        
        #### 4. Metriche Importanti da Monitorare
        
        - **Conversioni**: Free to Pro upgrades
        - **Engagement**: Feature usage, session duration
        - **Content**: Most used features, search queries
        - **Technical**: Performance, error rates
        """)
    
    # Configuration status
    st.markdown("#### 📊 Stato Configurazione")
    
    config_status = pd.DataFrame({
        'Componente': [
            'Google Analytics 4',
            'Measurement ID',
            'Event Tracking', 
            'Custom Parameters',
            'E-commerce Tracking'
        ],
        'Status': [
            '❌ Non configurato' if True else '✅ Configurato',
            '❌ Placeholder' if True else '✅ Valido',
            '✅ Implementato',
            '✅ Configurati',
            '✅ Ready'
        ],
        'Note': [
            'Aggiorna GA4_MEASUREMENT_ID',
            'Sostituisci G-XXXXXXXXXX',
            'Eventi pronti per tracking',
            'Parametri medici configurati',
            'Conversioni Pro trackate'
        ]
    })
    
    st.dataframe(config_status, use_container_width=True)

if __name__ == "__main__":
    # Test dashboard
    st.set_page_config(
        page_title="Analytics Dashboard Test",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🔍 Test Analytics Dashboard")
    
    tab1, tab2 = st.tabs(["📊 Dashboard", "⚙️ Setup"])
    
    with tab1:
        render_analytics_dashboard()
    
    with tab2:
        render_analytics_setup_guide()
