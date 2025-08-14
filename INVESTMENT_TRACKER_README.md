# 📈 Investment Tracker Pro

Un'applicazione Streamlit completa per tracciare i tuoi investimenti nel settore energetico (olio, gas, petrolio) e oltre.

## 🎯 Caratteristiche Principali

### 📊 Dashboard Completa
- **Metriche in tempo reale**: Totale investito, valore attuale, ROI, profitti/perdite
- **Grafici interattivi**: Distribuzione del portafoglio e performance per investimento
- **Tabella dettagliata**: Visualizzazione completa di tutti i tuoi investimenti

### ➕ Gestione Investimenti
- **Aggiunta facile**: Form intuitivo per aggiungere nuovi investimenti
- **Modifica e eliminazione**: Gestione completa dei tuoi investimenti
- **Supporto per quantity**: Traccia il numero di azioni/unità possedute

### 📈 Analytics Avanzate
- **Analisi per tipo**: Performance raggruppate per categoria di investimento
- **Migliori/peggiori performance**: Identifica rapidamente i tuoi investimenti top e bottom
- **ROI dettagliato**: Calcoli precisi del ritorno sull'investimento

### 🔄 Aggiornamento Prezzi Automatico
- **Integrazione Yahoo Finance**: Prezzi in tempo reale per azioni e ETF
- **Commodity tracking**: Prezzi di WTI, Brent, Gas Naturale
- **Suggerimenti intelligenti**: Simboli suggeriti basati sul nome dell'investimento
- **Test dei simboli**: Verifica i simboli prima dell'aggiornamento

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.11.7 (raccomandato)
- Anaconda (opzionale ma raccomandato)

### Installazione

1. **Assicurati di essere nella cartella corretta**
   ```bash
   cd C:\Users\nino1\curriculum-streamlit
   ```

2. **Installa le dipendenze** (se non già installate)
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvia l'applicazione**
   ```bash
   streamlit run investment_tracker.py
   ```

4. **Apri il browser**
   L'applicazione si aprirà automaticamente nel tuo browser all'indirizzo `http://localhost:8501`

## 📖 Come Usare l'Applicazione

### 1. Aggiungere il Primo Investimento
1. Vai nella sezione "➕ Aggiungi Investimento"
2. Compila tutti i campi obbligatori:
   - Nome dell'investimento (es: "Shell Oil Stock")
   - Tipo di investimento (Olio, Gas, Petrolio, ecc.)
   - Data di acquisto
   - Importo investito in Euro
   - Valore attuale in Euro
3. Opzionalmente, aggiungi la quantità e note
4. Clicca "💾 Salva Investimento"

### 2. Visualizzare le Performance
- La **Dashboard** mostra automaticamente tutte le metriche principali
- I grafici si aggiornano in tempo reale con i tuoi dati
- La tabella mostra tutti gli investimenti con calcoli automatici di ROI

### 3. Aggiornare i Prezzi Automaticamente
1. Vai nella sezione "🔄 Aggiorna Prezzi"
2. Seleziona gli investimenti da aggiornare
3. Inserisci i simboli di borsa (es: SHEL per Shell, CL=F per WTI Oil)
4. Usa il pulsante "Test" per verificare i simboli
5. Clicca "🔄 Aggiorna Tutti i Prezzi"

### 4. Analisi Avanzate
- Vai nella sezione "📈 Analytics" per vedere:
  - Performance per tipo di investimento
  - I tuoi 3 migliori e peggiori investimenti
  - Analisi dettagliate del portafoglio

## 💡 Simboli di Borsa Supportati

### Azioni Energetiche Principali
- **Shell**: SHEL
- **BP**: BP
- **TotalEnergies**: TTE
- **Chevron**: CVX
- **ExxonMobil**: XOM
- **ENI**: E
- **Snam**: SRG.MI

### Commodity
- **WTI Crude Oil**: CL=F
- **Brent Crude Oil**: BZ=F
- **Natural Gas**: NG=F

### ETF Energetici
- **Energy Select SPDR**: XLE
- **Vanguard Energy ETF**: VDE
- **iShares Global Energy ETF**: IXC

## 🔒 Sicurezza dei Dati
- Tutti i dati sono salvati localmente nel file `investments_data.json`
- Nessun dato viene inviato a server esterni (tranne le chiamate API per i prezzi)
- I tuoi investimenti rimangono completamente privati

## 🛠️ Personalizzazione
Puoi facilmente personalizzare l'applicazione modificando:
- Tipi di investimento disponibili nel codice
- Simboli predefiniti nel file `price_updater.py`
- Grafici e visualizzazioni nel file principale

## ⚠️ Note Importanti
- I prezzi sono forniti da Yahoo Finance e potrebbero avere un leggero ritardo
- Assicurati di avere una connessione internet per l'aggiornamento automatico dei prezzi
- I calcoli di ROI sono basati sui valori che inserisci manualmente

## 🆘 Risoluzione Problemi

### L'app non si avvia
1. Verifica di aver installato tutte le dipendenze: `pip install -r requirements.txt`
2. Controlla la versione di Python: `python --version`
3. Assicurati di essere nella cartella corretta: `C:\Users\nino1\curriculum-streamlit`

### I prezzi non si aggiornano
1. Verifica la connessione internet
2. Controlla che il simbolo sia corretto (usa il pulsante "Test")
3. Alcuni simboli potrebbero non essere disponibili su Yahoo Finance

### Errori di importazione
1. Assicurati che tutti i file siano nella stessa cartella
2. Reinstalla le dipendenze se necessario

## 🎉 Esempio di Utilizzo

Supponiamo tu abbia investito 5.000€ in petrolio e ora vale 10.000€ (come il tuo caso!):

1. **Aggiungi l'investimento**:
   - Nome: "Investimento Petrolio"
   - Tipo: "Olio"
   - Data: Data dell'investimento originale
   - Importo investito: 5000€
   - Valore attuale: 10000€

2. **Visualizza il risultato**:
   - ROI: 100%
   - Profitto: 5.000€
   - Grafici che mostrano la performance

3. **Aggiorna automaticamente** usando simboli come CL=F o BZ=F per monitorare l'andamento futuro

## 🔄 Aggiornamenti Futuri
- [ ] Aggiornamenti automatici programmati
- [ ] Export dei dati in Excel/PDF
- [ ] Grafici storici dell'andamento
- [ ] Notifiche per soglie di ROI
- [ ] Integrazione con API di brokers

---

**Creato con ❤️ per aiutarti a tracciare i tuoi investimenti nel settore energetico!**

## 📋 File Inclusi

- `investment_tracker.py` - Applicazione principale
- `price_updater.py` - Modulo per l'aggiornamento automatico dei prezzi
- `requirements.txt` - Dipendenze necessarie
- `INVESTMENT_TRACKER_README.md` - Questa guida

**Buon tracking dei tuoi investimenti! 🚀📈**
