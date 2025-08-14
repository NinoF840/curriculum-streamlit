import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os
from typing import Dict, List
from price_updater import create_price_update_interface

# Configurazione della pagina
st.set_page_config(
    page_title="Investment Tracker Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File per il salvataggio dei dati
DATA_FILE = "investments_data.json"

class InvestmentTracker:
    def __init__(self):
        self.data_file = DATA_FILE
        self.investments = self.load_data()
    
    def load_data(self) -> List[Dict]:
        """Carica i dati degli investimenti dal file JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_data(self):
        """Salva i dati degli investimenti nel file JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.investments, f, ensure_ascii=False, indent=2, default=str)
    
    def add_investment(self, investment: Dict):
        """Aggiunge un nuovo investimento"""
        investment['id'] = len(self.investments) + 1
        investment['date_added'] = datetime.now().isoformat()
        self.investments.append(investment)
        self.save_data()
    
    def update_investment(self, investment_id: int, updated_data: Dict):
        """Aggiorna un investimento esistente"""
        for i, inv in enumerate(self.investments):
            if inv['id'] == investment_id:
                self.investments[i].update(updated_data)
                self.save_data()
                break
    
    def delete_investment(self, investment_id: int):
        """Elimina un investimento"""
        self.investments = [inv for inv in self.investments if inv['id'] != investment_id]
        self.save_data()
    
    def get_portfolio_summary(self) -> Dict:
        """Calcola il riassunto del portafoglio"""
        if not self.investments:
            return {
                'total_invested': 0,
                'current_value': 0,
                'total_profit_loss': 0,
                'roi_percentage': 0,
                'active_investments': 0
            }
        
        df = pd.DataFrame(self.investments)
        total_invested = df['amount_invested'].sum()
        current_value = df['current_value'].sum()
        total_profit_loss = current_value - total_invested
        roi_percentage = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        return {
            'total_invested': total_invested,
            'current_value': current_value,
            'total_profit_loss': total_profit_loss,
            'roi_percentage': roi_percentage,
            'active_investments': len(df)
        }

def main():
    # Inizializzazione del tracker
    if 'tracker' not in st.session_state:
        st.session_state.tracker = InvestmentTracker()
    
    tracker = st.session_state.tracker
    
    # Header
    st.title("📈 Investment Tracker Pro")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Menu")
        page = st.selectbox(
            "Seleziona una sezione:",
            ["📊 Dashboard", "➕ Aggiungi Investimento", "📋 Gestisci Investimenti", "📈 Analytics", "🔄 Aggiorna Prezzi"]
        )
    
    # Dashboard
    if page == "📊 Dashboard":
        st.header("Dashboard del Portafoglio")
        
        # Metriche principali
        summary = tracker.get_portfolio_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Totale Investito",
                f"€{summary['total_invested']:,.2f}"
            )
        
        with col2:
            st.metric(
                "Valore Attuale",
                f"€{summary['current_value']:,.2f}",
                f"€{summary['total_profit_loss']:,.2f}"
            )
        
        with col3:
            st.metric(
                "ROI",
                f"{summary['roi_percentage']:,.2f}%"
            )
        
        with col4:
            st.metric(
                "Investimenti Attivi",
                summary['active_investments']
            )
        
        # Grafici se ci sono investimenti
        if tracker.investments:
            df = pd.DataFrame(tracker.investments)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribuzione per Tipo")
                type_distribution = df.groupby('investment_type')['current_value'].sum()
                fig_pie = px.pie(
                    values=type_distribution.values,
                    names=type_distribution.index,
                    title="Distribuzione del Portafoglio"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("Performance per Investimento")
                df['profit_loss'] = df['current_value'] - df['amount_invested']
                df['roi'] = (df['profit_loss'] / df['amount_invested'] * 100).round(2)
                
                fig_bar = px.bar(
                    df,
                    x='name',
                    y='roi',
                    color='roi',
                    color_continuous_scale=['red', 'yellow', 'green'],
                    title="ROI per Investimento (%)"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Tabella investimenti
            st.subheader("I Tuoi Investimenti")
            display_df = df[['name', 'investment_type', 'purchase_date', 'amount_invested', 'current_value', 'profit_loss', 'roi']].copy()
            display_df.columns = ['Nome', 'Tipo', 'Data Acquisto', 'Investito (€)', 'Valore Attuale (€)', 'Profitto/Perdita (€)', 'ROI (%)']
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("👋 Benvenuto! Inizia aggiungendo il tuo primo investimento usando il menu laterale.")
    
    # Aggiungi Investimento
    elif page == "➕ Aggiungi Investimento":
        st.header("Aggiungi Nuovo Investimento")
        
        with st.form("add_investment"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nome Investimento*", placeholder="Es: Shell Oil Stock")
                investment_type = st.selectbox(
                    "Tipo di Investimento*",
                    ["Olio", "Gas", "Petrolio", "Energia Rinnovabile", "Azioni Energetiche", "ETF Energia", "Altro"]
                )
                purchase_date = st.date_input("Data di Acquisto*", value=date.today())
            
            with col2:
                amount_invested = st.number_input("Importo Investito (€)*", min_value=0.01, step=0.01)
                current_value = st.number_input("Valore Attuale (€)*", min_value=0.01, step=0.01)
                quantity = st.number_input("Quantità", min_value=0.0, step=0.1, help="Opzionale: numero di azioni/unità")
            
            notes = st.text_area("Note", placeholder="Note aggiuntive sull'investimento...")
            
            submitted = st.form_submit_button("💾 Salva Investimento")
            
            if submitted:
                if name and investment_type and amount_invested > 0 and current_value >= 0:
                    investment = {
                        'name': name,
                        'investment_type': investment_type,
                        'purchase_date': purchase_date.isoformat(),
                        'amount_invested': amount_invested,
                        'current_value': current_value,
                        'quantity': quantity if quantity > 0 else None,
                        'notes': notes
                    }
                    
                    tracker.add_investment(investment)
                    st.success("✅ Investimento aggiunto con successo!")
                    st.rerun()
                else:
                    st.error("❌ Compila tutti i campi obbligatori!")
    
    # Gestisci Investimenti
    elif page == "📋 Gestisci Investimenti":
        st.header("Gestisci i Tuoi Investimenti")
        
        if not tracker.investments:
            st.info("Nessun investimento trovato. Aggiungi il primo investimento!")
            return
        
        # Selezione investimento da modificare
        investment_names = [f"{inv['name']} ({inv['investment_type']})" for inv in tracker.investments]
        selected_idx = st.selectbox("Seleziona investimento da modificare:", range(len(investment_names)), 
                                   format_func=lambda x: investment_names[x])
        
        selected_investment = tracker.investments[selected_idx]
        
        st.subheader(f"Modifica: {selected_investment['name']}")
        
        with st.form("edit_investment"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nome", value=selected_investment['name'])
                investment_type = st.selectbox(
                    "Tipo",
                    ["Olio", "Gas", "Petrolio", "Energia Rinnovabile", "Azioni Energetiche", "ETF Energia", "Altro"],
                    index=["Olio", "Gas", "Petrolio", "Energia Rinnovabile", "Azioni Energetiche", "ETF Energia", "Altro"].index(selected_investment['investment_type'])
                )
            
            with col2:
                current_value = st.number_input("Valore Attuale (€)", value=float(selected_investment['current_value']), min_value=0.01, step=0.01)
                quantity = st.number_input("Quantità", value=float(selected_investment.get('quantity', 0)), min_value=0.0, step=0.1)
            
            notes = st.text_area("Note", value=selected_investment.get('notes', ''))
            
            col1, col2 = st.columns(2)
            with col1:
                update_btn = st.form_submit_button("🔄 Aggiorna", type="primary")
            with col2:
                delete_btn = st.form_submit_button("🗑️ Elimina", type="secondary")
            
            if update_btn:
                updated_data = {
                    'name': name,
                    'investment_type': investment_type,
                    'current_value': current_value,
                    'quantity': quantity if quantity > 0 else None,
                    'notes': notes
                }
                tracker.update_investment(selected_investment['id'], updated_data)
                st.success("✅ Investimento aggiornato!")
                st.rerun()
            
            if delete_btn:
                tracker.delete_investment(selected_investment['id'])
                st.success("✅ Investimento eliminato!")
                st.rerun()
    
    # Analytics
    elif page == "📈 Analytics":
        st.header("Analisi Avanzate")
        
        if not tracker.investments:
            st.info("Aggiungi alcuni investimenti per vedere le analisi!")
            return
        
        df = pd.DataFrame(tracker.investments)
        df['profit_loss'] = df['current_value'] - df['amount_invested']
        df['roi'] = (df['profit_loss'] / df['amount_invested'] * 100)
        
        # Analisi per tipo
        st.subheader("📊 Analisi per Tipo di Investimento")
        type_analysis = df.groupby('investment_type').agg({
            'amount_invested': 'sum',
            'current_value': 'sum',
            'profit_loss': 'sum'
        }).reset_index()
        type_analysis['roi'] = (type_analysis['profit_loss'] / type_analysis['amount_invested'] * 100)
        
        st.dataframe(type_analysis, use_container_width=True)
        
        # Migliori e peggiori performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Migliori Performance")
            best_performers = df.nlargest(3, 'roi')[['name', 'roi', 'profit_loss']]
            for idx, row in best_performers.iterrows():
                st.success(f"**{row['name']}**: {row['roi']:.2f}% (€{row['profit_loss']:,.2f})")
        
        with col2:
            st.subheader("⚠️ Performance da Migliorare")
            worst_performers = df.nsmallest(3, 'roi')[['name', 'roi', 'profit_loss']]
            for idx, row in worst_performers.iterrows():
                st.error(f"**{row['name']}**: {row['roi']:.2f}% (€{row['profit_loss']:,.2f})")
    
    # Aggiorna Prezzi
    elif page == "🔄 Aggiorna Prezzi":
        create_price_update_interface(tracker)

if __name__ == "__main__":
    main()
