#!/usr/bin/env python3
"""
Real Developers & Clones Dashboard for Nino Medical AI
====================================================

Dashboard per tracciare chi sono realmente i 25 cloni e 23 sviluppatori unici
che hanno interagito con il progetto curriculum-streamlit.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import subprocess
import os

class RealDevelopersDashboard:
    """Dashboard per monitorare sviluppatori reali e cloni del repository."""
    
    def __init__(self):
        self.repo_owner = "NinoF840"
        self.repo_name = "curriculum-streamlit"
        self.real_data = self._fetch_real_github_data()
    
    def _fetch_real_github_data(self):
        """Fetch real data from GitHub API."""
        try:
            # Esegue comandi gh per ottenere dati reali
            clone_data = self._run_gh_command("api repos/NinoF840/curriculum-streamlit/traffic/clones")
            views_data = self._run_gh_command("api repos/NinoF840/curriculum-streamlit/traffic/views") 
            repo_data = self._run_gh_command("repo view --json stargazerCount,forkCount,watchers,createdAt,pushedAt")
            
            return {
                "clones": clone_data,
                "views": views_data,
                "repo": repo_data,
                "last_updated": datetime.now()
            }
        except Exception as e:
            st.error(f"Errore nel fetch dei dati GitHub: {e}")
            return self._get_fallback_data()
    
    def _run_gh_command(self, command):
        """Esegue comando GitHub CLI e ritorna JSON."""
        try:
            result = subprocess.run(
                f"gh {command}".split(),
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            st.warning(f"Comando gh fallito: {e}")
            return {}
    
    def _get_fallback_data(self):
        """Dati di fallback basati sui dati reali che abbiamo visto."""
        return {
            "clones": {
                "count": 25,
                "uniques": 23,
                "clones": [
                    {"timestamp": "2025-07-31T00:00:00Z", "count": 1, "uniques": 1},
                    {"timestamp": "2025-08-02T00:00:00Z", "count": 1, "uniques": 1},
                    {"timestamp": "2025-08-03T00:00:00Z", "count": 5, "uniques": 5},
                    {"timestamp": "2025-08-04T00:00:00Z", "count": 4, "uniques": 4},
                    {"timestamp": "2025-08-09T00:00:00Z", "count": 1, "uniques": 1},
                    {"timestamp": "2025-08-10T00:00:00Z", "count": 7, "uniques": 6},
                    {"timestamp": "2025-08-11T00:00:00Z", "count": 2, "uniques": 2},
                    {"timestamp": "2025-08-13T00:00:00Z", "count": 4, "uniques": 4}
                ]
            },
            "views": {"count": 0, "uniques": 0, "views": []},
            "repo": {
                "stargazerCount": 0,
                "forkCount": 0,
                "watchers": {"totalCount": 0}
            },
            "last_updated": datetime.now()
        }

    def render_dashboard(self):
        """Renders the complete real developers dashboard."""
        st.markdown('<h1 style="color: #1f77b4;">🔍 Chi Sono i Miei 25 Sviluppatori?</h1>', unsafe_allow_html=True)
        st.markdown('---')
        
        # Overview dei dati reali
        self.render_real_overview()
        
        # Tabs per diverse analisi
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Cloni Reali", 
            "👥 Analisi Sviluppatori", 
            "📈 Timeline Attività",
            "🔧 Actions"
        ])
        
        with tab1:
            self.render_real_clones_analysis()
        
        with tab2:
            self.render_developers_analysis()
            
        with tab3:
            self.render_activity_timeline()
            
        with tab4:
            self.render_tracking_actions()

    def render_real_overview(self):
        """Overview con dati reali GitHub."""
        st.markdown("### 📈 Statistiche Reali del Repository")
        
        clone_data = self.real_data.get("clones", {})
        repo_data = self.real_data.get("repo", {})
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_clones = clone_data.get("count", 0)
            st.metric("🔄 Cloni Totali", total_clones, delta=f"vs README: {41-total_clones}")
        
        with col2:
            unique_devs = clone_data.get("uniques", 0)
            st.metric("👨‍💻 Sviluppatori Unici", unique_devs, delta=f"vs README: {32-unique_devs}")
        
        with col3:
            stars = repo_data.get("stargazerCount", 0)
            st.metric("⭐ Stelle", stars)
            
        with col4:
            forks = repo_data.get("forkCount", 0)
            st.metric("🍴 Fork", forks)
        
        with col5:
            watchers = repo_data.get("watchers", {}).get("totalCount", 0)
            st.metric("👀 Watchers", watchers)

        # Alert per discrepanze
        if total_clones != 41 or unique_devs != 32:
            st.warning(f"""
            ⚠️ **Discrepanza Rilevata!**
            
            - README dice: 41 cloni, 32 sviluppatori
            - Dati GitHub reali: {total_clones} cloni, {unique_devs} sviluppatori unici
            
            I numeri nel README potrebbero includere dati storici o altre metriche.
            """)

    def render_real_clones_analysis(self):
        """Analisi dettagliata dei cloni reali."""
        st.markdown("### 🔍 Chi Ha Clonato il Tuo Progetto?")
        
        clone_data = self.real_data.get("clones", {})
        clones_list = clone_data.get("clones", [])
        
        if not clones_list:
            st.info("📊 Nessun dato di cloni disponibile nelle ultime 2 settimane.")
            return
        
        # Trasforma i dati per l'analisi
        df_clones = pd.DataFrame(clones_list)
        df_clones['timestamp'] = pd.to_datetime(df_clones['timestamp'])
        df_clones['date'] = df_clones['timestamp'].dt.date
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Cloni Giornalieri")
            fig = px.bar(df_clones, x='date', y='count', 
                        title="Cloni per Giorno",
                        labels={'count': 'Numero Cloni', 'date': 'Data'})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 👥 Sviluppatori Unici Giornalieri")
            fig = px.bar(df_clones, x='date', y='uniques',
                        title="Sviluppatori Unici per Giorno", 
                        labels={'uniques': 'Sviluppatori Unici', 'date': 'Data'},
                        color='uniques', color_continuous_scale='viridis')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabella dettagliata
        st.markdown("#### 📋 Dettagli Cloni per Giorno")
        df_display = df_clones.copy()
        df_display['Data'] = df_display['date']
        df_display['Cloni'] = df_display['count']
        df_display['Sviluppatori Unici'] = df_display['uniques']
        df_display['Ratio Clone/Dev'] = (df_display['count'] / df_display['uniques']).round(2)
        
        st.dataframe(
            df_display[['Data', 'Cloni', 'Sviluppatori Unici', 'Ratio Clone/Dev']],
            use_container_width=True
        )
        
        # Insights
        self.render_clones_insights(df_clones)

    def render_clones_insights(self, df_clones):
        """Genera insights dai dati dei cloni."""
        st.markdown("#### 🧠 Insights sui Cloni")
        
        total_clones = df_clones['count'].sum()
        unique_devs = df_clones['uniques'].sum()
        peak_day = df_clones.loc[df_clones['count'].idxmax()]
        avg_clones_per_dev = total_clones / unique_devs if unique_devs > 0 else 0
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.info(f"""
            📊 **Statistiche Periodo Analizzato:**
            - **Periodo più attivo**: {peak_day['date']} ({peak_day['count']} cloni)
            - **Media cloni per sviluppatore**: {avg_clones_per_dev:.2f}
            - **Giorni con attività**: {len(df_clones)} giorni
            """)
        
        with insight_col2:
            # Calcola pattern di comportamento
            multi_cloners = df_clones[df_clones['count'] > df_clones['uniques']]['count'].sum()
            if multi_cloners > 0:
                st.warning(f"""
                🔄 **Comportamenti di Cloning:**
                - Alcuni sviluppatori hanno clonato più volte
                - **{multi_cloners}** cloni multipli rilevati
                - Possibili motivi: aggiornamenti, test, curiosità
                """)
            else:
                st.success("✅ **Tutti i cloni sembrano da sviluppatori unici**")

    def render_developers_analysis(self):
        """Analisi profonda degli sviluppatori."""
        st.markdown("### 👨‍💻 Profiling degli Sviluppatori")
        
        # Cerchiamo di identificare pattern negli sviluppatori
        clone_data = self.real_data.get("clones", {})
        clones_list = clone_data.get("clones", [])
        
        if not clones_list:
            st.info("Non ci sono dati sufficienti per l'analisi degli sviluppatori.")
            return
        
        df_clones = pd.DataFrame(clones_list)
        df_clones['timestamp'] = pd.to_datetime(df_clones['timestamp'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Tipologie di Sviluppatori")
            
            # Categorizza i comportamenti
            single_cloners = len(df_clones[df_clones['count'] == df_clones['uniques']])
            multi_cloners = len(df_clones[df_clones['count'] > df_clones['uniques']])
            
            dev_types = pd.DataFrame({
                'Tipo': ['🔍 Esploratori', '🔄 Sviluppatori Attivi', '👀 Osservatori'],
                'Numero': [single_cloners, multi_cloners, 0],
                'Descrizione': [
                    'Clonano una volta per esplorare',
                    'Clonano multiple volte (sviluppo attivo)', 
                    'Non hanno ancora clonato'
                ]
            })
            
            fig = px.pie(dev_types, names='Tipo', values='Numero', 
                        title="Distribuzione Tipi Sviluppatori")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🌍 Potenziale Distribuzione Geografica")
            
            # Stima basata sui pattern orari
            df_clones['hour'] = df_clones['timestamp'].dt.hour
            hour_dist = df_clones['hour'].value_counts().sort_index()
            
            # Inferisci possibili timezone
            peak_hours = hour_dist.nlargest(3).index.tolist()
            
            timezone_guess = []
            for hour in peak_hours:
                if 8 <= hour <= 17:  # Orario lavorativo EU
                    timezone_guess.append("Europa/Italia")
                elif 14 <= hour <= 23:  # Orario lavorativo US East  
                    timezone_guess.append("America/New_York")
                elif 17 <= hour <= 2:  # Orario lavorativo US West
                    timezone_guess.append("America/Los_Angeles")
            
            st.info(f"""
            🕐 **Analisi Oraria dei Cloni:**
            - **Ore di picco**: {', '.join(map(str, peak_hours))}
            - **Possibili timezone**: {', '.join(set(timezone_guess)) if timezone_guess else 'Dati insufficienti'}
            
            *Questa è una stima basata sui pattern orari*
            """)
            
            # Grafico distribuzione oraria
            fig = px.bar(x=hour_dist.index, y=hour_dist.values,
                        title="Distribuzione Oraria Cloni",
                        labels={'x': 'Ora del Giorno', 'y': 'Numero Cloni'})
            st.plotly_chart(fig, use_container_width=True)

    def render_activity_timeline(self):
        """Timeline dell'attività degli sviluppatori."""
        st.markdown("### 📈 Timeline Attività Sviluppatori")
        
        clone_data = self.real_data.get("clones", {})
        clones_list = clone_data.get("clones", [])
        
        if not clones_list:
            st.info("Nessuna timeline disponibile.")
            return
        
        df_clones = pd.DataFrame(clones_list)
        df_clones['timestamp'] = pd.to_datetime(df_clones['timestamp'])
        
        # Timeline cumulativa
        df_clones_sorted = df_clones.sort_values('timestamp')
        df_clones_sorted['cumulative_clones'] = df_clones_sorted['count'].cumsum()
        df_clones_sorted['cumulative_uniques'] = df_clones_sorted['uniques'].cumsum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_clones_sorted['timestamp'],
            y=df_clones_sorted['cumulative_clones'], 
            mode='lines+markers',
            name='Cloni Cumulativi',
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=df_clones_sorted['timestamp'],
            y=df_clones_sorted['cumulative_uniques'],
            mode='lines+markers', 
            name='Sviluppatori Unici Cumulativi',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title="Crescita Cumulativa: Cloni vs Sviluppatori",
            xaxis_title="Data",
            yaxis_title="Numero Cumulativo"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Milestone detection
        st.markdown("#### 🎯 Milestone Raggiunte")
        
        milestones = []
        if df_clones_sorted['cumulative_clones'].max() >= 20:
            milestones.append("🎉 20+ cloni raggiunti!")
        if df_clones_sorted['cumulative_uniques'].max() >= 15:
            milestones.append("👥 15+ sviluppatori unici!")
        
        if milestones:
            for milestone in milestones:
                st.success(milestone)
        else:
            st.info("🚀 Prossimi milestone: 20 cloni, 15 sviluppatori unici")

    def render_tracking_actions(self):
        """Azioni per migliorare il tracking degli sviluppatori."""
        st.markdown("### 🔧 Come Tracciare Meglio i Tuoi Sviluppatori")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Azioni Immediate")
            
            actions = [
                "🌟 Aggiungi call-to-action per stelle GitHub",
                "📝 Crea issue template per feedback sviluppatori", 
                "💬 Aggiungi sezione discussioni al repo",
                "📊 Implementa Google Analytics nella app",
                "🔗 Aggiungi link social nel README",
                "📧 Crea mailing list per updates"
            ]
            
            for action in actions:
                if st.checkbox(action, key=f"action_{hash(action)}"):
                    st.success(f"✅ {action}")
        
        with col2:
            st.markdown("#### 📈 Tracking Avanzato")
            
            st.code("""
            # GitHub CLI commands per monitoraggio
            
            # Cloni (ultimi 14 giorni)
            gh api repos/NinoF840/curriculum-streamlit/traffic/clones
            
            # Visualizzazioni (ultimi 14 giorni) 
            gh api repos/NinoF840/curriculum-streamlit/traffic/views
            
            # Top referring sites
            gh api repos/NinoF840/curriculum-streamlit/traffic/popular/referrers
            
            # Top content
            gh api repos/NinoF840/curriculum-streamlit/traffic/popular/paths
            """, language="bash")
        
        # Quick update README
        st.markdown("#### 🔄 Aggiorna README con Dati Reali")
        
        clone_data = self.real_data.get("clones", {})
        real_clones = clone_data.get("count", 0)
        real_uniques = clone_data.get("uniques", 0)
        
        if st.button("🚀 Genera Testo README Aggiornato"):
            updated_text = f"""
            🚀 **{real_clones} cloni** e **{real_uniques} sviluppatori** hanno già scaricato il progetto!
            
            *Dati aggiornati automaticamente da GitHub API - {datetime.now().strftime('%d/%m/%Y')}*
            """
            
            st.code(updated_text, language="markdown")
            st.success("✅ Copia questo testo nel tuo README.md per avere numeri sempre aggiornati!")

def main():
    """Main function per la dashboard."""
    st.set_page_config(
        page_title="🔍 Real Developers Dashboard - Nino Medical AI",
        page_icon="🔍", 
        layout="wide"
    )
    
    dashboard = RealDevelopersDashboard()
    dashboard.render_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    🏥 <strong>Nino Medical AI</strong> - Real Developers Analytics<br>
    📧 ninomedical.ai@gmail.com | 🌍 Castelvetrano (TP), Italia
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
