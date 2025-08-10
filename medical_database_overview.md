# 🏥 Nino Medical AI - Database Medico Completo

## 📋 Panoramica Database

Il database medico integrato nell'applicazione desktop contiene informazioni cliniche strutturate per supportare l'analisi dei sintomi e la raccomandazione di trattamenti.

---

## 🔍 1. SINTOMI E DIAGNOSI

### 🩸 **LIVIDI**
**Diagnosi Principali:**
- Trauma accidentale (85% probabilità)
- Disturbi coagulazione (12% probabilità)  
- Vasculite (8% probabilità)
- Piastrinopenia (5% probabilità)
- Leucemia (3% probabilità)
- Trauma non accidentale (2% probabilità)

**Sintomi Associati:**
- Dolore localizzato
- Gonfiore
- Limitazione funzionale
- Cambio colore (rosso→blu→verde→giallo)
- Petecchie
- Sanguinamenti spontanei

**Esami Diagnostici:**
- Emocromo completo
- PT/PTT/INR
- Conta piastrinica
- Fibrinogeno
- D-dimero
- Fattori coagulazione
- Ecografia tessuti molli
- Radiografia (se trauma)

**Trattamenti:**
- Riposo e immobilizzazione
- Applicazione ghiaccio (24-48h)
- Antidolorifici (paracetamolo)
- Evitare FANS se coagulopatie
- Compressione elastica
- Elevazione arto
- Fisioterapia (fase tardiva)
- Trattamento causa sottostante

**Terapie Specifiche:**
- **Coagulopatie:** Vitamina K, plasma fresco, concentrati fattori
- **Piastrinopenia:** Corticosteroidi, immunoglobuline, trasfusioni
- **Vasculite:** Corticosteroidi, immunosoppressori
- **Trauma:** PRICE (Protection, Rest, Ice, Compression, Elevation)

---

### 🌡️ **FEBBRE**
**Diagnosi Principali:**
- Infezione virale
- Infezione batterica
- Infezione fungina
- Malattie autoimmuni
- Neoplasie
- Farmaci

**Trattamenti:**
- Antipiretici (paracetamolo, ibuprofene)
- Idratazione
- Riposo
- Antibiotici (se batterica)
- Antivirali specifici

---

### 💔 **DOLORE TORACE**
**Diagnosi Principali:**
- Infarto miocardico
- Angina pectoris
- Embolia polmonare
- Pneumotorace
- Pericardite
- Reflusso gastroesofageo
- Costocondrite
- Ansia/attacchi panico

**Esami Diagnostici:**
- ECG
- Troponine
- D-dimero
- Radiografia torace
- Ecocardiogramma
- TC torace con contrasto
- Angiografia coronarica

**Trattamenti:**
- Ossigenoterapia
- Nitroglicerina
- Antiaggreganti
- Anticoagulanti
- Beta-bloccanti
- ACE-inibitori
- Riperfusione (PCI/trombolisi)
- Ansiolitici (se indicato)

---

### 😤 **DISPNEA**
**Diagnosi Principali:**
- Asma
- BPCO
- Insufficienza cardiaca
- Embolia polmonare
- Pneumonia
- Pneumotorace
- Anemia
- Ansia

**Trattamenti:**
- Broncodilatatori
- Corticosteroidi
- Ossigenoterapia
- Diuretici
- ACE-inibitori
- Antibiotici
- Ventilazione assistita

---

## 💊 2. DATABASE FARMACI

### 🩹 **ANALGESICI**
- **Paracetamolo:** 500-1000mg ogni 6-8h, max 4g/die
- **Ibuprofene:** 400-600mg ogni 8h, max 2.4g/die
- **Diclofenac:** 50mg ogni 8-12h
- **Ketoprofene:** 100mg ogni 12h

### 🦠 **ANTIBIOTICI**
- **Amoxicillina:** 500-875mg ogni 8-12h per 7-10 giorni
- **Azitromicina:** 500mg il primo giorno, poi 250mg per 4 giorni
- **Ciprofloxacina:** 500mg ogni 12h per 7-14 giorni
- **Levofloxacina:** 500mg ogni 24h per 7-10 giorni

### ❤️ **FARMACI CARDIACI**
- **Atenololo:** 50-100mg/die
- **Lisinopril:** 5-10mg/die, incrementare gradualmente
- **Amlodipina:** 5-10mg/die
- **Furosemide:** 40-80mg/die al mattino

---

## 🚨 3. PROTOCOLLI EMERGENZA

### 🔴 **CODICE ROSSO** (Priorità Massima)
- Arresto cardiaco
- Shock
- Trauma maggiore
- Ictus acuto
- Infarto STEMI
- Embolia polmonare massiva

### 🟡 **CODICE GIALLO** (Alta Priorità)
- Dolore toracico
- Dispnea severa
- Trauma minore
- Febbre alta
- Sincope

### 🟢 **CODICE VERDE** (Bassa Priorità)
- Sintomi lievi
- Follow-up
- Controlli
- Medicazioni

---

## 🔧 4. UTILIZZO NEL SISTEMA

### **Analisi Automatica:**
Il sistema riconosce automaticamente i sintomi inseriti e:
1. Mostra le diagnosi principali con probabilità calcolate
2. Suggerisce esami diagnostici appropriati
3. Raccomanda trattamenti specifici
4. Identifica criteri di allarme

### **Personalizzazione:**
- Adatta le raccomandazioni in base ai parametri del paziente
- Considera la storia medica
- Valuta l'urgenza percepita

### **Sicurezza:**
- Include sempre disclaimer medico
- Evidenzia quando consultare un medico
- Non sostituisce mai il giudizio clinico professionale

---

## ⚠️ DISCLAIMER IMPORTANTE

**Questo database è destinato esclusivamente a scopi dimostrativi ed educativi. Non deve mai essere utilizzato per diagnosi mediche reali o decisioni cliniche. Consultare sempre un medico qualificato per qualsiasi problema di salute.**

---

*Sviluppato da: Antonino Piacenza - AI Researcher & MedTech Developer*
*Email: ninomedical.ai@gmail.com*
*Data: Gennaio 2025*
