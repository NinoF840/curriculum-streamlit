import yfinance as yf
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import streamlit as st

class PriceUpdater:
    """Classe per l'aggiornamento automatico dei prezzi degli investimenti"""
    
    # Simboli comuni per il settore energetico
    ENERGY_SYMBOLS = {
        'Shell': 'SHEL',
        'BP': 'BP',
        'TotalEnergies': 'TTE',
        'Chevron': 'CVX',
        'ExxonMobil': 'XOM',
        'ConocoPhillips': 'COP',
        'ENI': 'E',
        'Snam': 'SRG.MI',
        'Saipem': 'SPM.MI',
        'Tenaris': 'TEN.MI',
    }
    
    # ETF del settore energetico
    ENERGY_ETFS = {
        'Energy Select SPDR': 'XLE',
        'Vanguard Energy ETF': 'VDE',
        'iShares Global Energy ETF': 'IXC',
        'Invesco Dynamic Energy': 'PXE',
    }
    
    # API per i prezzi delle commodity
    COMMODITY_API_URL = "https://api.metals.live/v1/spot"
    
    def __init__(self):
        self.all_symbols = {**self.ENERGY_SYMBOLS, **self.ENERGY_ETFS}
    
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """Ottiene il prezzo corrente di un'azione tramite Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.history(period="1d")
            if not info.empty:
                return float(info['Close'].iloc[-1])
        except Exception as e:
            st.error(f"Errore nel recupero prezzo per {symbol}: {str(e)}")
        return None
    
    def search_symbol(self, company_name: str) -> Optional[str]:
        """Cerca il simbolo di borsa basandosi sul nome dell'azienda"""
        # Prima controlla nei simboli noti
        for name, symbol in self.all_symbols.items():
            if company_name.lower() in name.lower() or name.lower() in company_name.lower():
                return symbol
        
        # Prova una ricerca più generica
        try:
            # Crea un ticker con il nome e verifica se esiste
            potential_symbols = [
                company_name.upper(),
                company_name.upper() + ".MI",  # Borsa italiana
                company_name.upper() + ".PA",  # Borsa di Parigi
                company_name.upper() + ".L",   # Borsa di Londra
            ]
            
            for symbol in potential_symbols:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                if info and 'regularMarketPrice' in info:
                    return symbol
                    
        except Exception:
            pass
        
        return None
    
    def get_commodity_price(self, commodity_type: str) -> Optional[float]:
        """Ottiene il prezzo corrente delle commodity (WTI, Brent, Gas naturale)"""
        commodity_symbols = {
            'olio': 'CL=F',      # WTI Crude Oil
            'petrolio': 'BZ=F',   # Brent Crude Oil
            'gas': 'NG=F',       # Natural Gas
        }
        
        symbol = commodity_symbols.get(commodity_type.lower())
        if symbol:
            return self.get_stock_price(symbol)
        
        return None
    
    def update_investment_value(self, investment: Dict, new_price: float, quantity: Optional[float] = None) -> Dict:
        """Aggiorna il valore di un investimento basandosi sul nuovo prezzo"""
        updated_investment = investment.copy()
        
        if quantity and quantity > 0:
            # Se abbiamo la quantità, calcoliamo il nuovo valore totale
            updated_investment['current_value'] = new_price * quantity
            updated_investment['price_per_unit'] = new_price
        else:
            # Se non abbiamo la quantità, assumiamo una variazione proporzionale
            original_value = investment['amount_invested']
            # Questa è una semplificazione - in realtà dovresti avere il prezzo originale
            updated_investment['current_value'] = new_price
        
        updated_investment['last_updated'] = datetime.now().isoformat()
        return updated_investment
    
    def get_suggested_symbols(self, investment_name: str, investment_type: str) -> List[str]:
        """Suggerisce possibili simboli di borsa per un investimento"""
        suggestions = []
        
        # Cerca nei simboli noti
        for name, symbol in self.all_symbols.items():
            if (investment_name.lower() in name.lower() or 
                name.lower() in investment_name.lower()):
                suggestions.append(f"{symbol} ({name})")
        
        # Aggiungi simboli generici per tipo
        if investment_type.lower() in ['olio', 'petrolio']:
            suggestions.extend([
                'CL=F (WTI Crude Oil)',
                'BZ=F (Brent Crude Oil)',
                'XLE (Energy Select SPDR ETF)'
            ])
        elif investment_type.lower() == 'gas':
            suggestions.extend([
                'NG=F (Natural Gas)',
                'UNG (United States Natural Gas Fund)'
            ])
        
        return suggestions[:5]  # Limita a 5 suggerimenti


def create_price_update_interface(tracker):
    """Crea l'interfaccia per l'aggiornamento dei prezzi"""
    st.subheader("🔄 Aggiornamento Prezzi Automatico")
    
    if not tracker.investments:
        st.info("Aggiungi alcuni investimenti per utilizzare questa funzionalità!")
        return
    
    updater = PriceUpdater()
    
    # Selezione investimenti da aggiornare
    investment_options = [f"{inv['name']} ({inv['investment_type']})" for inv in tracker.investments]
    selected_investments = st.multiselect(
        "Seleziona investimenti da aggiornare:",
        range(len(investment_options)),
        format_func=lambda x: investment_options[x]
    )
    
    if selected_investments:
        st.subheader("Configurazione Simboli")
        
        symbol_mapping = {}
        for idx in selected_investments:
            investment = tracker.investments[idx]
            
            col1, col2 = st.columns([2, 1])
            with col1:
                # Input manuale del simbolo
                suggested_symbols = updater.get_suggested_symbols(
                    investment['name'], 
                    investment['investment_type']
                )
                
                if suggested_symbols:
                    st.write(f"**{investment['name']}** - Simboli suggeriti:")
                    for suggestion in suggested_symbols:
                        st.write(f"  • {suggestion}")
                
                symbol = st.text_input(
                    f"Simbolo per {investment['name']}:",
                    key=f"symbol_{idx}",
                    placeholder="Es: SHEL, CL=F, XLE"
                )
                symbol_mapping[idx] = symbol
            
            with col2:
                st.write("") # Spazio
                st.write("") # Spazio
                # Test del simbolo
                if symbol and st.button(f"Test", key=f"test_{idx}"):
                    price = updater.get_stock_price(symbol)
                    if price:
                        st.success(f"✅ Prezzo attuale: €{price:.2f}")
                    else:
                        st.error("❌ Simbolo non trovato")
        
        st.markdown("---")
        
        # Pulsante per aggiornare tutti i prezzi
        if st.button("🔄 Aggiorna Tutti i Prezzi", type="primary"):
            updated_count = 0
            errors = []
            
            for idx in selected_investments:
                symbol = symbol_mapping.get(idx, "").strip()
                if symbol:
                    investment = tracker.investments[idx]
                    new_price = updater.get_stock_price(symbol)
                    
                    if new_price:
                        # Aggiorna il valore
                        if investment.get('quantity') and investment['quantity'] > 0:
                            updated_value = new_price * investment['quantity']
                        else:
                            # Se non abbiamo quantità, mantieni il rapporto di investimento
                            updated_value = new_price
                        
                        updated_data = {
                            'current_value': updated_value,
                            'price_per_unit': new_price,
                            'symbol': symbol,
                            'last_updated': datetime.now().isoformat()
                        }
                        
                        tracker.update_investment(investment['id'], updated_data)
                        updated_count += 1
                    else:
                        errors.append(f"Impossibile aggiornare {investment['name']} (simbolo: {symbol})")
            
            if updated_count > 0:
                st.success(f"✅ {updated_count} investimenti aggiornati con successo!")
                st.rerun()
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
    
    # Sezione per aggiornamenti automatici programmati
    with st.expander("⚙️ Impostazioni Aggiornamento Automatico"):
        st.info("💡 **Prossima Funzionalità:** Aggiornamenti automatici programmati ogni ora/giorno")
        
        auto_update = st.checkbox("Abilita aggiornamenti automatici", disabled=True)
        update_frequency = st.selectbox(
            "Frequenza aggiornamento:",
            ["Ogni ora", "Ogni 4 ore", "Ogni giorno", "Ogni settimana"],
            disabled=True
        )
        
        st.warning("⚠️ Questa funzionalità sarà disponibile in una versione futura dell'app.")


# Aggiungi questa funzione al file principale investment_tracker.py
def add_price_update_page():
    """Aggiunge la pagina di aggiornamento prezzi al menu principale"""
    pass  # Questa sarà integrata nel file principale
