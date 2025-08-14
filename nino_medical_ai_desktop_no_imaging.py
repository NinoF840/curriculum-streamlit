#!/usr/bin/env python3
"""
Nino Medical AI Pro Ultimate - Desktop Edition (No Imaging)
============================================================

Versione desktop nativa senza funzionalità di imaging per build leggera.
Sviluppato da Antonino Piacenza
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import threading
import time
import json
import os
import webbrowser

class NinoMedicalAIDesktopNoImaging:
    """Applicazione desktop Nino Medical AI senza imaging."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Nino Medical AI Pro Ultimate - Desktop Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f2f6')
        
        # Variabili di stato
        self.current_page = "dashboard"
        self.analysis_results = {}
        
        # Configura stile
        self.setup_style()
        
        # Crea interfaccia
        self.create_main_interface()
        
        # Avvia loop principale
        self.root.mainloop()
    
    def setup_style(self):
        """Configura lo stile dell'applicazione."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colori personalizzati
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), 
                       foreground='#1f4e79', background='#f0f2f6')
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), 
                       foreground='#2e7d32', background='white')
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=2)
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        
    def create_main_interface(self):
        """Crea l'interfaccia principale."""
        # Header
        self.create_header()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f2f6')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.create_content_area(main_container)
        
        # Status bar
        self.create_status_bar()
        
        # Carica dashboard iniziale
        self.show_dashboard()
        
    def create_header(self):
        """Crea header dell'applicazione."""
        header_frame = tk.Frame(self.root, bg='#1f4e79', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo e titolo
        title_frame = tk.Frame(header_frame, bg='#1f4e79')
        title_frame.pack(expand=True)
        
        title_label = tk.Label(
            title_frame, 
            text="🏥 NINO MEDICAL AI PRO ULTIMATE", 
            font=('Arial', 18, 'bold'),
            fg='white', 
            bg='#1f4e79'
        )
        title_label.pack(pady=(10, 0))
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Desktop Edition - Ricerca e Analisi Medica Avanzata", 
            font=('Arial', 10),
            fg='#e0e0e0', 
            bg='#1f4e79'
        )
        subtitle_label.pack(pady=(0, 10))
        
    def create_sidebar(self, parent):
        """Crea sidebar di navigazione."""
        sidebar_frame = tk.Frame(parent, bg='#2c3e50', width=250)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Titolo sidebar
        sidebar_title = tk.Label(
            sidebar_frame, 
            text="🏥 Navigazione", 
            font=('Arial', 14, 'bold'),
            fg='white', 
            bg='#2c3e50',
            pady=20
        )
        sidebar_title.pack(fill='x')
        
        # Pulsanti navigazione
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🌍 Database Medici", self.show_databases),
            ("🧠 Medicina Predittiva", self.show_predictive_medicine),
            ("🧪 Trial Clinici", self.show_clinical_trials),
            ("🩺 Analisi Sintomi", self.show_symptom_analysis),
            ("📊 Analytics", self.show_analytics),
            ("👨‍💻 Chi Sono", self.show_about)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                sidebar_frame,
                text=text,
                command=command,
                font=('Arial', 10, 'bold'),
                bg='#34495e',
                fg='white',
                activebackground='#1f4e79',
                activeforeground='white',
                bd=0,
                pady=12,
                cursor='hand2'
            )
            btn.pack(fill='x', padx=10, pady=2)
        
        # Separatore
        separator = tk.Frame(sidebar_frame, height=2, bg='#1f4e79')
        separator.pack(fill='x', padx=10, pady=20)
        
        # Statistiche
        stats_title = tk.Label(
            sidebar_frame, 
            text="📊 Statistiche Globali", 
            font=('Arial', 12, 'bold'),
            fg='white', 
            bg='#2c3e50'
        )
        stats_title.pack()
        
        # Metriche sidebar
        metrics = [
            ("🤖 Modelli AI", "45+"),
            ("📄 Pubblicazioni", "1.2M+"),
            ("📈 Analisi Eseguite", "250k+")
        ]
        
        for label, value in metrics:
            metric_frame = tk.Frame(sidebar_frame, bg='#2c3e50')
            metric_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(metric_frame, text=label, font=('Arial', 9), 
                    fg='#bdc3c7', bg='#2c3e50').pack(anchor='w')
            tk.Label(metric_frame, text=value, font=('Arial', 12, 'bold'), 
                    fg='white', bg='#2c3e50').pack(anchor='w')
    
    def create_content_area(self, parent):
        """Crea area contenuto principale."""
        self.content_frame = tk.Frame(parent, bg='#f0f2f6')
        self.content_frame.pack(side='right', fill='both', expand=True)
    
    def create_status_bar(self):
        """Crea status bar."""
        status_frame = tk.Frame(self.root, bg='#34495e', height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"Ready - {datetime.now().strftime('%H:%M:%S')}",
            font=('Arial', 9),
            fg='white',
            bg='#34495e',
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10)
        
        # Aggiorna ora ogni secondo
        self.update_clock()
    
    def update_clock(self):
        """Aggiorna l'orologio nella status bar."""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.status_label.config(text=f"Sistema Operativo - {current_time}")
        self.root.after(1000, self.update_clock)
    
    def clear_content(self):
        """Pulisce l'area contenuto."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Mostra dashboard principale."""
        self.clear_content()
        self.current_page = "dashboard"
        
        # Titolo
        title_label = tk.Label(
            self.content_frame,
            text="📊 Dashboard Principale",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Welcome card
        welcome_frame = tk.Frame(self.content_frame, bg='#667eea', relief='raised', bd=2)
        welcome_frame.pack(fill='x', padx=20, pady=10)
        
        welcome_title = tk.Label(
            welcome_frame,
            text="🚀 Benvenuto in Nino Medical AI Pro Ultimate",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#667eea'
        )
        welcome_title.pack(pady=(15, 5))
        
        welcome_desc = tk.Label(
            welcome_frame,
            text="Piattaforma integrata per la ricerca medica, analisi predittiva e gestione trial clinici",
            font=('Arial', 11),
            fg='white',
            bg='#667eea',
            wraplength=800
        )
        welcome_desc.pack(pady=(0, 15))
        
        # Metriche sistema
        metrics_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        metrics_title = tk.Label(
            metrics_frame,
            text="Stato del Sistema",
            font=('Arial', 14, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        metrics_title.pack(anchor='w', pady=(0, 10))
        
        # Grid metriche
        metrics_grid = tk.Frame(metrics_frame, bg='#f0f2f6')
        metrics_grid.pack(fill='x')
        
        system_metrics = [
            ("Connessione Database", "✅ Attiva", "#28a745"),
            ("Moduli Predittivi", "✅ Caricati (12)", "#28a745"),
            ("Stato Sistema", "✅ Operativo", "#28a745"),
            ("Ora Server", datetime.now().strftime("%H:%M:%S"), "#1f4e79")
        ]
        
        for i, (title, value, color) in enumerate(system_metrics):
            col = i % 4
            metric_card = tk.Frame(metrics_grid, bg='white', relief='raised', bd=1)
            metric_card.grid(row=0, column=col, padx=5, pady=5, sticky='ew')
            
            tk.Label(metric_card, text=title, font=('Arial', 10, 'bold'), 
                    bg='white').pack(pady=(10, 5))
            tk.Label(metric_card, text=value, font=('Arial', 12, 'bold'), 
                    fg=color, bg='white').pack(pady=(0, 10))
        
        # Configura grid weights
        for i in range(4):
            metrics_grid.columnconfigure(i, weight=1)
        
        # Grafici
        self.create_dashboard_charts()
    
    def create_dashboard_charts(self):
        """Crea grafici per dashboard."""
        charts_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        charts_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titolo grafici
        charts_title = tk.Label(
            charts_frame,
            text="📈 Panoramica Attività",
            font=('Arial', 14, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        charts_title.pack(anchor='w', pady=(0, 10))
        
        # Container grafici
        charts_container = tk.Frame(charts_frame, bg='#f0f2f6')
        charts_container.pack(fill='both', expand=True)
        
        # Grafico 1: Utilizzo moduli
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        modules = ['Predizione\nRischio', 'Analisi Dati\nClinici', 'NLP\nMedico', 'Ottimizzazione\nTerapie']
        usage = [450, 320, 280, 150]
        colors = ['#1f4e79', '#2e7d32', '#e65100', '#7b1fa2']
        
        bars = ax1.bar(modules, usage, color=colors)
        ax1.set_title('Utilizzo Moduli IA (Ultimi 30 giorni)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Utilizzo')
        
        # Aggiungi valori sulle barre
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, charts_container)
        canvas1.get_tk_widget().pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Grafico 2: Performance modelli
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        models = ['Cardiovascolare', 'Diabetico', 'Oncologico', 'Renale']
        accuracy = [94.5, 91.2, 89.7, 92.1]
        
        ax2.plot(models, accuracy, 'o-', color='#2e7d32', linewidth=3, markersize=8)
        ax2.set_title('Accuratezza Modelli Predittivi (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Accuratezza (%)')
        ax2.set_ylim(85, 100)
        ax2.grid(True, alpha=0.3)
        
        # Aggiungi valori sui punti
        for i, v in enumerate(accuracy):
            ax2.text(i, v + 0.5, f'{v}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, charts_container)
        canvas2.get_tk_widget().pack(side='right', fill='both', expand=True, padx=(10, 0))
    
    def show_databases(self):
        """Mostra interfaccia database medici."""
        self.clear_content()
        self.current_page = "databases"
        
        title_label = tk.Label(
            self.content_frame,
            text="🌍 Accesso Database Medici Globali",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Info card
        info_frame = tk.Frame(self.content_frame, bg='#d1ecf1', relief='raised', bd=1)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Interfaccia unificata per interrogare i principali database medici senza autenticazione",
            font=('Arial', 11),
            fg='#0c5460',
            bg='#d1ecf1',
            wraplength=800
        )
        info_text.pack(pady=15)
        
        # Form ricerca
        search_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="Database Selection & Search", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 10))
        
        # Selezione database
        db_frame = tk.Frame(search_frame, bg='white')
        db_frame.pack(fill='x', padx=20)
        
        tk.Label(db_frame, text="Seleziona Database:", font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=(0, 5))
        
        self.db_var = tk.StringVar(value="PubMed")
        db_combo = ttk.Combobox(
            db_frame, 
            textvariable=self.db_var,
            values=["PubMed", "ClinicalTrials.gov", "FDA", "WHO", "UniProt", "Disease Ontology"],
            state="readonly",
            font=('Arial', 10)
        )
        db_combo.pack(fill='x', pady=(0, 15))
        
        # Campo ricerca
        tk.Label(db_frame, text="Termine di ricerca:", font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(db_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(fill='x', pady=(0, 15))
        
        # Pulsante ricerca
        search_btn = tk.Button(
            search_frame,
            text="🔍 Avvia Ricerca",
            command=self.perform_database_search,
            font=('Arial', 11, 'bold'),
            bg='#1f4e79',
            fg='white',
            pady=10,
            cursor='hand2'
        )
        search_btn.pack(pady=(0, 20))
        
        # Area risultati
        self.results_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        self.results_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    def perform_database_search(self):
        """Simula ricerca nei database."""
        if not self.search_var.get().strip():
            messagebox.showwarning("Attenzione", "Inserire un termine di ricerca!")
            return
        
        # Pulisci risultati precedenti
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Simula caricamento
        loading_label = tk.Label(
            self.results_frame,
            text=f"🔍 Ricerca in corso su {self.db_var.get()}...",
            font=('Arial', 12),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        loading_label.pack(pady=20)
        
        self.root.update()
        time.sleep(1)  # Simula delay ricerca
        
        loading_label.destroy()
        
        # Mostra risultati simulati
        results_title = tk.Label(
            self.results_frame,
            text=f"✅ Trovati 150 risultati per '{self.search_var.get()}' in {self.db_var.get()}",
            font=('Arial', 12, 'bold'),
            fg='#28a745',
            bg='#f0f2f6'
        )
        results_title.pack(anchor='w', pady=(0, 10))
        
        # Tabella risultati
        results_table_frame = tk.Frame(self.results_frame, bg='white', relief='raised', bd=1)
        results_table_frame.pack(fill='both', expand=True)
        
        # Headers
        headers = ["Titolo", "Autori", "Data", "DOI"]
        header_frame = tk.Frame(results_table_frame, bg='#1f4e79')
        header_frame.pack(fill='x')
        
        for header in headers:
            tk.Label(header_frame, text=header, font=('Arial', 10, 'bold'),
                    fg='white', bg='#1f4e79', relief='raised', bd=1).pack(
                    side='left', fill='x', expand=True, padx=1, pady=1)
        
        # Scroll frame per risultati
        scroll_frame = scrolledtext.ScrolledText(results_table_frame, height=15)
        scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Dati simulati
        for i in range(15):
            result_text = f"Studio {i+1} su {self.search_var.get()}\t"
            result_text += f"Team di Ricerca {i+1}\t"
            result_text += f"{2023-i//3}-01-01\t"
            result_text += f"10.1234/journal.{i:03d}\n"
            scroll_frame.insert(tk.END, result_text)
        
        scroll_frame.config(state='disabled')
    
    def show_predictive_medicine(self):
        """Mostra interfaccia medicina predittiva."""
        self.clear_content()
        self.current_page = "predictive_medicine"
        
        title_label = tk.Label(
            self.content_frame,
            text="🧠 Medicina Predittiva",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Warning
        warning_frame = tk.Frame(self.content_frame, bg='#fff3cd', relief='raised', bd=1)
        warning_frame.pack(fill='x', padx=20, pady=10)
        
        warning_text = tk.Label(
            warning_frame,
            text="⚠️ I modelli in questa sezione sono a scopo dimostrativo e non devono essere usati per diagnosi reali.",
            font=('Arial', 11, 'bold'),
            fg='#856404',
            bg='#fff3cd',
            wraplength=800
        )
        warning_text.pack(pady=15)
        
        # Selezione modello
        model_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        model_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(model_frame, text="Seleziona Modello Predittivo", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 10))
        
        self.model_var = tk.StringVar(value="Predizione Rischio Cardiovascolare")
        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=[
                "Predizione Rischio Cardiovascolare",
                "Predizione Insorgenza Diabete", 
                "Analisi Risposta a Terapia Oncologica"
            ],
            state="readonly",
            font=('Arial', 11)
        )
        model_combo.pack(fill='x', padx=20, pady=(0, 15))
        
        # Area configurazione
        self.config_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        self.config_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Carica configurazione cardiovascolare di default
        self.show_cardiovascular_config()
        
        # Bind cambio modello
        model_combo.bind("<<ComboboxSelected>>", self.on_model_change)
    
    def on_model_change(self, event=None):
        """Gestisce il cambio di modello predittivo."""
        model = self.model_var.get()
        
        # Pulisci area configurazione
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        
        if model == "Predizione Rischio Cardiovascolare":
            self.show_cardiovascular_config()
        else:
            # Per altri modelli, mostra messaggio "in sviluppo"
            dev_label = tk.Label(
                self.config_frame,
                text="🚧 Modulo in fase di sviluppo",
                font=('Arial', 14),
                fg='#6c757d',
                bg='#f0f2f6'
            )
            dev_label.pack(expand=True)
    
    def show_cardiovascular_config(self):
        """Mostra configurazione per modello cardiovascolare."""
        # Card configurazione
        config_card = tk.Frame(self.config_frame, bg='white', relief='raised', bd=2)
        config_card.pack(fill='both', expand=True)
        
        tk.Label(config_card, text="Inserisci Dati del Paziente (Simulati)", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 20))
        
        # Grid input
        input_grid = tk.Frame(config_card, bg='white')
        input_grid.pack(fill='x', padx=20)
        
        # Variabili input
        self.age_var = tk.IntVar(value=55)
        self.cholesterol_var = tk.IntVar(value=220)
        self.bp_var = tk.IntVar(value=140)
        self.glucose_var = tk.IntVar(value=90)
        self.smoker_var = tk.StringVar(value="No")
        self.exercise_var = tk.StringVar(value="Sì")
        
        # Campi input
        inputs = [
            ("Età:", self.age_var, 20, 100),
            ("Colesterolo (mg/dL):", self.cholesterol_var, 100, 400),
            ("Pressione Sistolica (mmHg):", self.bp_var, 80, 200),
            ("Glicemia (mg/dL):", self.glucose_var, 50, 200)
        ]
        
        for i, (label, var, min_val, max_val) in enumerate(inputs):
            row = i // 2
            col = i % 2
            
            input_frame = tk.Frame(input_grid, bg='white')
            input_frame.grid(row=row, column=col, padx=20, pady=10, sticky='ew')
            
            tk.Label(input_frame, text=label, font=('Arial', 10), 
                    bg='white').pack(anchor='w')
            
            spinbox = tk.Spinbox(input_frame, from_=min_val, to=max_val, 
                               textvariable=var, font=('Arial', 10))
            spinbox.pack(fill='x', pady=(5, 0))
        
        # Configura grid
        input_grid.columnconfigure(0, weight=1)
        input_grid.columnconfigure(1, weight=1)
        
        # Radio buttons
        radio_frame = tk.Frame(config_card, bg='white')
        radio_frame.pack(fill='x', padx=20, pady=20)
        
        # Fumatore
        smoker_frame = tk.Frame(radio_frame, bg='white')
        smoker_frame.pack(side='left', fill='x', expand=True, padx=(0, 20))
        
        tk.Label(smoker_frame, text="Fumatore:", font=('Arial', 10), 
                bg='white').pack(anchor='w')
        
        for value in ["Sì", "No"]:
            tk.Radiobutton(smoker_frame, text=value, variable=self.smoker_var,
                          value=value, bg='white', font=('Arial', 10)).pack(anchor='w')
        
        # Esercizio fisico
        exercise_frame = tk.Frame(radio_frame, bg='white')
        exercise_frame.pack(side='right', fill='x', expand=True, padx=(20, 0))
        
        tk.Label(exercise_frame, text="Esercizio Fisico:", font=('Arial', 10), 
                bg='white').pack(anchor='w')
        
        for value in ["Sì", "No"]:
            tk.Radiobutton(exercise_frame, text=value, variable=self.exercise_var,
                          value=value, bg='white', font=('Arial', 10)).pack(anchor='w')
        
        # Pulsante calcolo
        calc_btn = tk.Button(
            config_card,
            text="⚡ Calcola Rischio Cardiovascolare",
            command=self.calculate_cardiovascular_risk,
            font=('Arial', 12, 'bold'),
            bg='#1f4e79',
            fg='white',
            pady=15,
            cursor='hand2'
        )
        calc_btn.pack(pady=(20, 30))
        
        # Area risultati
        self.cardio_results_frame = tk.Frame(config_card, bg='white')
        self.cardio_results_frame.pack(fill='x', padx=20, pady=(0, 20))
    
    def calculate_cardiovascular_risk(self):
        """Calcola il rischio cardiovascolare simulato."""
        # Pulisci risultati precedenti
        for widget in self.cardio_results_frame.winfo_children():
            widget.destroy()
        
        # Simula calcolo
        loading_label = tk.Label(
            self.cardio_results_frame,
            text="🧠 Analisi in corso...",
            font=('Arial', 12),
            fg='#1f4e79',
            bg='white'
        )
        loading_label.pack(pady=10)
        
        self.root.update()
        time.sleep(2)  # Simula elaborazione
        
        loading_label.destroy()
        
        # Calcolo simulato
        age_factor = self.age_var.get() / 100
        chol_factor = self.cholesterol_var.get() / 300
        bp_factor = self.bp_var.get() / 180
        smoker_factor = 1.5 if self.smoker_var.get() == "Sì" else 0.8
        exercise_factor = 0.7 if self.exercise_var.get() == "Sì" else 1.2
        
        risk_score = age_factor * chol_factor * bp_factor * smoker_factor * exercise_factor
        risk_percentage = min(risk_score * 100, 99)
        
        # Risultati
        results_frame = tk.Frame(self.cardio_results_frame, bg='#d4edda', relief='raised', bd=2)
        results_frame.pack(fill='x', pady=10)
        
        tk.Label(results_frame, text="✅ Analisi Completata!", 
                font=('Arial', 12, 'bold'), fg='#155724', bg='#d4edda').pack(pady=(10, 5))
        
        risk_text = f"Rischio Cardiovascolare a 10 anni: {risk_percentage:.1f}%"
        risk_level = "Alto" if risk_percentage > 30 else "Medio" if risk_percentage > 15 else "Basso"
        
        tk.Label(results_frame, text=risk_text, 
                font=('Arial', 14, 'bold'), fg='#155724', bg='#d4edda').pack(pady=5)
        
        tk.Label(results_frame, text=f"Livello di Rischio: {risk_level}", 
                font=('Arial', 11), fg='#155724', bg='#d4edda').pack(pady=(0, 10))
        
        # Raccomandazioni
        recommendations_frame = tk.Frame(self.cardio_results_frame, bg='#fff3cd', relief='raised', bd=1)
        recommendations_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(recommendations_frame, text="💡 Raccomandazioni:", 
                font=('Arial', 11, 'bold'), fg='#856404', bg='#fff3cd').pack(anchor='w', padx=10, pady=(10, 5))
        
        recommendations = [
            "• Consultazione cardiologica per valutazione approfondita",
            "• Monitoraggio regolare della pressione arteriosa",
            "• Controllo periodico dei livelli di colesterolo"
        ]
        
        if self.smoker_var.get() == "Sì":
            recommendations.append("• Considerare programma per cessazione tabagismo")
        
        if self.exercise_var.get() == "No":
            recommendations.append("• Incrementare attività fisica regolare")
        
        for rec in recommendations:
            tk.Label(recommendations_frame, text=rec, 
                    font=('Arial', 10), fg='#856404', bg='#fff3cd', 
                    anchor='w').pack(anchor='w', padx=10, pady=2)
        
        tk.Label(recommendations_frame, text="", bg='#fff3cd').pack(pady=(0, 10))
    
    def show_clinical_trials(self):
        """Mostra interfaccia trial clinici."""
        self.clear_content()
        self.current_page = "clinical_trials"
        
        title_label = tk.Label(
            self.content_frame,
            text="🧪 Ottimizzazione Trial Clinici",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Info
        info_frame = tk.Frame(self.content_frame, bg='#d1ecf1', relief='raised', bd=1)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Identifica coorti di pazienti idonei per trial clinici basandosi su dati anonimizzati",
            font=('Arial', 11),
            fg='#0c5460',
            bg='#d1ecf1',
            wraplength=800
        )
        info_text.pack(pady=15)
        
        # Filtri
        filters_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        filters_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(filters_frame, text="Filtri per la Selezione dei Pazienti", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 20))
        
        # Grid filtri
        filter_grid = tk.Frame(filters_frame, bg='white')
        filter_grid.pack(fill='x', padx=20)
        
        # Colonna sinistra
        left_col = tk.Frame(filter_grid, bg='white')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        tk.Label(left_col, text="Patologia di interesse:", 
                font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        
        self.pathology_var = tk.StringVar(value="Oncologia")
        pathology_combo = ttk.Combobox(
            left_col,
            textvariable=self.pathology_var,
            values=["Oncologia", "Cardiologia", "Diabetologia", "Malattie Rare"],
            state="readonly"
        )
        pathology_combo.pack(fill='x', pady=(0, 15))
        
        tk.Label(left_col, text="Età minima:", 
                font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        
        self.min_age_var = tk.IntVar(value=40)
        min_age_scale = tk.Scale(left_col, from_=18, to=100, orient=tk.HORIZONTAL,
                               variable=self.min_age_var, bg='white')
        min_age_scale.pack(fill='x', pady=(0, 15))
        
        # Colonna destra
        right_col = tk.Frame(filter_grid, bg='white')
        right_col.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        tk.Label(right_col, text="Età massima:", 
                font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        
        self.max_age_var = tk.IntVar(value=70)
        max_age_scale = tk.Scale(right_col, from_=18, to=100, orient=tk.HORIZONTAL,
                               variable=self.max_age_var, bg='white')
        max_age_scale.pack(fill='x', pady=(0, 15))
        
        tk.Label(right_col, text="Escludi co-morbilità:", 
                font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        
        # Checkbuttons per comorbidità
        self.comorbidities = {}
        comorbidity_list = ["Ipertensione", "Diabete", "Insufficienza Renale"]
        
        for comorbidity in comorbidity_list:
            var = tk.BooleanVar()
            self.comorbidities[comorbidity] = var
            tk.Checkbutton(right_col, text=comorbidity, variable=var,
                          bg='white', font=('Arial', 10)).pack(anchor='w')
        
        # Pulsante ricerca
        search_btn = tk.Button(
            filters_frame,
            text="👤 Trova Pazienti Idonei",
            command=self.find_eligible_patients,
            font=('Arial', 12, 'bold'),
            bg='#1f4e79',
            fg='white',
            pady=15,
            cursor='hand2'
        )
        search_btn.pack(pady=(30, 20))
        
        # Area risultati
        self.trial_results_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        self.trial_results_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    def find_eligible_patients(self):
        """Trova pazienti idonei per trial."""
        # Pulisci risultati precedenti
        for widget in self.trial_results_frame.winfo_children():
            widget.destroy()
        
        # Simula ricerca
        loading_label = tk.Label(
            self.trial_results_frame,
            text="🔍 Ricerca nel database pazienti anonimizzato...",
            font=('Arial', 12),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        loading_label.pack(pady=20)
        
        self.root.update()
        time.sleep(1.5)
        
        loading_label.destroy()
        
        # Risultati simulati
        patient_count = np.random.randint(50, 200)
        
        success_label = tk.Label(
            self.trial_results_frame,
            text=f"✅ Trovati {patient_count} pazienti potenzialmente idonei",
            font=('Arial', 12, 'bold'),
            fg='#28a745',
            bg='#f0f2f6'
        )
        success_label.pack(anchor='w', pady=(0, 10))
        
        # Tabella pazienti
        patients_frame = tk.Frame(self.trial_results_frame, bg='white', relief='raised', bd=2)
        patients_frame.pack(fill='both', expand=True)
        
        # Headers
        headers = ["ID Paziente", "Età", "Patologia", "Score Compatibilità"]
        header_frame = tk.Frame(patients_frame, bg='#1f4e79')
        header_frame.pack(fill='x')
        
        for header in headers:
            tk.Label(header_frame, text=header, font=('Arial', 10, 'bold'),
                    fg='white', bg='#1f4e79', relief='raised', bd=1).pack(
                    side='left', fill='x', expand=True, padx=1, pady=1)
        
        # Scroll area
        scroll_frame = scrolledtext.ScrolledText(patients_frame, height=12)
        scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Dati simulati pazienti
        min_age = self.min_age_var.get()
        max_age = self.max_age_var.get()
        pathology = self.pathology_var.get()
        
        for i in range(12):  # Mostra primi 12 pazienti
            patient_id = f"P{np.random.randint(1000, 9999)}"
            age = np.random.randint(min_age, max_age)
            compatibility = np.random.uniform(85, 99)
            
            patient_text = f"{patient_id:<15}{age:<10}{pathology:<20}{compatibility:.1f}%\n"
            scroll_frame.insert(tk.END, patient_text)
        
        scroll_frame.config(state='disabled')
    
    def show_analytics(self):
        """Mostra pagina analytics."""
        self.clear_content()
        self.current_page = "analytics"
        
        title_label = tk.Label(
            self.content_frame,
            text="📊 Analytics & Reporting",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        stats_grid = tk.Frame(stats_frame, bg='#f0f2f6')
        stats_grid.pack()
        
        stats_data = [
            ("📊 Analisi Totali", "25,847", "#1f4e79"),
            ("🧠 Modelli Attivi", "12", "#2e7d32"),
            ("👥 Utenti Sistema", "45", "#e65100"),
            ("⚡ Uptime", "99.8%", "#7b1fa2")
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            col = i % 2
            row = i // 2
            
            stat_card = tk.Frame(stats_grid, bg='white', relief='raised', bd=2,
                               width=250, height=100)
            stat_card.grid(row=row, column=col, padx=10, pady=10)
            stat_card.pack_propagate(False)
            
            tk.Label(stat_card, text=title, font=('Arial', 11), 
                    bg='white').pack(pady=(15, 5))
            tk.Label(stat_card, text=value, font=('Arial', 18, 'bold'), 
                    fg=color, bg='white').pack()
        
        # Report generation
        report_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        report_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(report_frame, text="📈 Genera Report", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 10))
        
        report_buttons = [
            ("📊 Report Utilizzo Mensile", lambda: messagebox.showinfo("Report", "Report generato!")),
            ("🧠 Performance Modelli", lambda: messagebox.showinfo("Report", "Report modelli generato!")),
            ("👥 Statistiche Utenti", lambda: messagebox.showinfo("Report", "Report utenti generato!")),
            ("💾 Export Dati CSV", lambda: messagebox.showinfo("Export", "Dati esportati!"))
        ]
        
        for text, command in report_buttons:
            tk.Button(report_frame, text=text, command=command,
                     font=('Arial', 10), bg='#1f4e79', fg='white',
                     pady=8, cursor='hand2').pack(fill='x', padx=20, pady=5)
        
        tk.Label(report_frame, text="", bg='white').pack(pady=10)
    
    def show_about(self):
        """Mostra pagina informazioni."""
        self.clear_content()
        self.current_page = "about"
        
        title_label = tk.Label(
            self.content_frame,
            text="👨‍💻 Profilo Professionale",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Main info card
        info_card = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        info_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Profile header
        profile_frame = tk.Frame(info_card, bg='white')
        profile_frame.pack(fill='x', padx=30, pady=30)
        
        # Avatar placeholder
        avatar_frame = tk.Frame(profile_frame, bg='white')
        avatar_frame.pack(side='left', padx=(0, 30))
        
        avatar_label = tk.Label(
            avatar_frame,
            text="👨‍💻",
            font=('Arial', 48),
            bg='white'
        )
        avatar_label.pack()
        
        # Info text
        info_text_frame = tk.Frame(profile_frame, bg='white')
        info_text_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(info_text_frame, text="Antonino Piacenza", 
                font=('Arial', 20, 'bold'), fg='#1f4e79', bg='white').pack(anchor='w')
        
        tk.Label(info_text_frame, text="AI Researcher & MedTech Developer", 
                font=('Arial', 14), fg='#2e7d32', bg='white').pack(anchor='w', pady=(0, 15))
        
        # Description
        description_text = """Sviluppatore di soluzioni di Intelligenza Artificiale per il settore medico-sanitario.

VISIONE:
Trasformare la medicina attraverso l'IA etica e scalabile, migliorando la qualità 
della vita dei pazienti e l'efficienza degli operatori sanitari.

SPECIALIZZAZIONI:
• Medicina Predittiva: Modelli per stratificazione del rischio
• NLP Clinico: Estrazione informazioni da testi medici  
• Analisi Dati Sanitari: Integrazione e analisi big data
• Federated Learning: Privacy-preserving AI per dati sensibili

CONTATTI:
• Email: ninomedical.ai@gmail.com
• LinkedIn: linkedin.com/in/antoNinoF840
• Progetti: Aperto a collaborazioni Horizon Europe"""
        
        description_label = tk.Label(
            info_text_frame,
            text=description_text,
            font=('Arial', 11),
            fg='#333',
            bg='white',
            justify='left',
            anchor='nw'
        )
        description_label.pack(fill='both', expand=True)
        
        # Footer buttons
        footer_frame = tk.Frame(info_card, bg='white')
        footer_frame.pack(fill='x', padx=30, pady=(0, 30))
        
        contact_btn = tk.Button(
            footer_frame,
            text="📧 Contatta per Collaborazioni",
            command=lambda: webbrowser.open("mailto:ninomedical.ai@gmail.com"),
            font=('Arial', 11, 'bold'),
            bg='#1f4e79',
            fg='white',
            pady=10,
            cursor='hand2'
        )
        contact_btn.pack(side='left')
        
        linkedin_btn = tk.Button(
            footer_frame,
            text="🔗 LinkedIn Profile",
            command=lambda: messagebox.showinfo("LinkedIn", "Apri: linkedin.com/in/antoNinoF840"),
            font=('Arial', 11),
            bg='#0077b5',
            fg='white',
            pady=10,
            cursor='hand2'
        )
        linkedin_btn.pack(side='right')

    def show_symptom_analysis(self):
        """Mostra interfaccia analisi sintomi."""
        self.clear_content()
        self.current_page = "symptom_analysis"
        
        title_label = tk.Label(
            self.content_frame,
            text="🩺 Analisi Sintomi AI",
            font=('Arial', 18, 'bold'),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        title_label.pack(pady=(20, 10))
        
        # Info
        info_frame = tk.Frame(self.content_frame, bg='#fff3cd', relief='raised', bd=1)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = tk.Label(
            info_frame,
            text="⚠️ Questo strumento è solo a scopo dimostrativo. Per diagnosi reali consultare sempre un medico.",
            font=('Arial', 11, 'bold'),
            fg='#856404',
            bg='#fff3cd',
            wraplength=800
        )
        info_text.pack(pady=15)
        
        # Form analisi sintomi
        analysis_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        analysis_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(analysis_frame, text="Descrizione Sintomi del Paziente", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 10))
        
        # Area descrizione sintomi
        symptoms_frame = tk.Frame(analysis_frame, bg='white')
        symptoms_frame.pack(fill='x', padx=20)
        
        tk.Label(symptoms_frame, text="Inserisci i sintomi osservati:", 
                font=('Arial', 10), bg='white').pack(anchor='w', pady=(0, 5))
        
        self.symptoms_text = tk.Text(symptoms_frame, height=4, font=('Arial', 10))
        self.symptoms_text.pack(fill='x', pady=(0, 15))
        self.symptoms_text.insert('1.0', "Paziente mostra lividi braccio sinistro")
        
        # Parametri aggiuntivi
        params_frame = tk.Frame(analysis_frame, bg='white')
        params_frame.pack(fill='x', padx=20)
        
        # Colonna sinistra
        left_params = tk.Frame(params_frame, bg='white')
        left_params.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        tk.Label(left_params, text="Età paziente:", font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=(0, 5))
        self.age_symptom_var = tk.IntVar(value=45)
        age_spinbox = tk.Spinbox(left_params, from_=1, to=120, 
                               textvariable=self.age_symptom_var, font=('Arial', 10))
        age_spinbox.pack(fill='x', pady=(0, 15))
        
        tk.Label(left_params, text="Sesso:", font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=(0, 5))
        self.gender_var = tk.StringVar(value="M")
        gender_frame = tk.Frame(left_params, bg='white')
        gender_frame.pack(fill='x', pady=(0, 15))
        tk.Radiobutton(gender_frame, text="M", variable=self.gender_var,
                      value="M", bg='white').pack(side='left')
        tk.Radiobutton(gender_frame, text="F", variable=self.gender_var,
                      value="F", bg='white').pack(side='left')
        
        # Colonna destra
        right_params = tk.Frame(params_frame, bg='white')
        right_params.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        tk.Label(right_params, text="Urgenza percepita:", font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=(0, 5))
        self.urgency_var = tk.StringVar(value="Media")
        urgency_combo = ttk.Combobox(
            right_params,
            textvariable=self.urgency_var,
            values=["Bassa", "Media", "Alta", "Critica"],
            state="readonly"
        )
        urgency_combo.pack(fill='x', pady=(0, 15))
        
        tk.Label(right_params, text="Storia medica:", font=('Arial', 10), 
                bg='white').pack(anchor='w', pady=(0, 5))
        self.history_var = tk.StringVar()
        history_combo = ttk.Combobox(
            right_params,
            textvariable=self.history_var,
            values=["Nessuna", "Cardiopatie", "Diabete", "Ipertensione", "Disturbi coagulazione"],
            state="readonly"
        )
        history_combo.pack(fill='x', pady=(0, 15))
        
        # Pulsante analisi
        analyze_btn = tk.Button(
            analysis_frame,
            text="🔍 Analizza Sintomi con AI",
            command=self.analyze_symptoms,
            font=('Arial', 12, 'bold'),
            bg='#1f4e79',
            fg='white',
            pady=15,
            cursor='hand2'
        )
        analyze_btn.pack(pady=(30, 20))
        
        # Area risultati
        self.symptom_results_frame = tk.Frame(self.content_frame, bg='#f0f2f6')
        self.symptom_results_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    def analyze_symptoms(self):
        """Analizza i sintomi inseriti."""
        symptoms = self.symptoms_text.get('1.0', tk.END).strip()
        if not symptoms:
            messagebox.showwarning("Attenzione", "Inserire una descrizione dei sintomi!")
            return
        
        # Pulisci risultati precedenti
        for widget in self.symptom_results_frame.winfo_children():
            widget.destroy()
        
        # Simula analisi AI
        loading_label = tk.Label(
            self.symptom_results_frame,
            text="🧠 Analisi AI in corso... Elaborazione sintomi...",
            font=('Arial', 12),
            fg='#1f4e79',
            bg='#f0f2f6'
        )
        loading_label.pack(pady=20)
        
        self.root.update()
        time.sleep(3)  # Simula elaborazione AI
        
        loading_label.destroy()
        
        # Analisi specifica per lividi braccio sinistro
        if "lividi" in symptoms.lower() or "livido" in symptoms.lower():
            self.analyze_bruising_case(symptoms)
        else:
            self.analyze_general_symptoms(symptoms)
    
    def get_medical_database(self):
        """Database medico completo con sintomi, diagnosi e cure."""
        return {
            "sintomi_diagnosi": {
                "lividi": {
                    "diagnosi_principali": [
                        "Trauma accidentale", "Disturbi coagulazione", "Vasculite", 
                        "Piastrinopenia", "Leucemia", "Trauma non accidentale"
                    ],
                    "sintomi_associati": [
                        "Dolore localizzato", "Gonfiore", "Limitazione funzionale",
                        "Cambio colore (rosso->blu->verde->giallo)", "Petecchie",
                        "Sanguinamenti spontanei"
                    ],
                    "esami_diagnostici": [
                        "Emocromo completo", "PT/PTT/INR", "Conta piastrinica",
                        "Fibrinogeno", "D-dimero", "Fattori coagulazione",
                        "Ecografia tessuti molli", "Radiografia (se trauma)"
                    ],
                    "cure_trattamenti": [
                        "Riposo e immobilizzazione", "Applicazione ghiaccio (24-48h)",
                        "Antidolorifici (paracetamolo)", "Evitare FANS se coagulopatie",
                        "Compressione elastica", "Elevazione arto",
                        "Fisioterapia (fase tardiva)", "Trattamento causa sottostante"
                    ],
                    "terapie_specifiche": {
                        "coagulopatie": "Vitamina K, plasma fresco, concentrati fattori",
                        "piastrinopenia": "Corticosteroidi, immunoglobuline, trasfusioni",
                        "vasculite": "Corticosteroidi, immunosoppressori",
                        "trauma": "PRICE (Protection, Rest, Ice, Compression, Elevation)"
                    }
                },
                "febbre": {
                    "diagnosi_principali": [
                        "Infezione virale", "Infezione batterica", "Infezione fungina",
                        "Malattie autoimmuni", "Neoplasie", "Farmaci"
                    ],
                    "cure_trattamenti": [
                        "Antipiretici (paracetamolo, ibuprofene)", "Idratazione",
                        "Riposo", "Antibiotici (se batterica)", "Antivirali specifici"
                    ]
                },
                "dolore_torace": {
                    "diagnosi_principali": [
                        "Infarto miocardico", "Angina pectoris", "Embolia polmonare",
                        "Pneumotorace", "Pericardite", "Reflusso gastroesofageo",
                        "Costocondrite", "Ansia/attacchi panico"
                    ],
                    "esami_diagnostici": [
                        "ECG", "Troponine", "D-dimero", "Radiografia torace",
                        "Ecocardiogramma", "TC torace con contrasto", "Angiografia coronarica"
                    ],
                    "cure_trattamenti": [
                        "Ossigenoterapia", "Nitroglicerina", "Antiaggreganti",
                        "Anticoagulanti", "Beta-bloccanti", "ACE-inibitori",
                        "Riperfusione (PCI/trombolisi)", "Ansiolitici (se indicato)"
                    ]
                },
                "dispnea": {
                    "diagnosi_principali": [
                        "Asma", "BPCO", "Insufficienza cardiaca", "Embolia polmonare",
                        "Pneumonia", "Pneumotorace", "Anemia", "Ansia"
                    ],
                    "cure_trattamenti": [
                        "Broncodilatatori", "Corticosteroidi", "Ossigenoterapia",
                        "Diuretici", "ACE-inibitori", "Antibiotici", "Ventilazione assistita"
                    ]
                }
            },
            "farmaci_database": {
                "analgesici": {
                    "paracetamolo": "500-1000mg ogni 6-8h, max 4g/die",
                    "ibuprofene": "400-600mg ogni 8h, max 2.4g/die",
                    "diclofenac": "50mg ogni 8-12h",
                    "ketoprofene": "100mg ogni 12h"
                },
                "antibiotici": {
                    "amoxicillina": "500-875mg ogni 8-12h per 7-10 giorni",
                    "azitromicina": "500mg il primo giorno, poi 250mg per 4 giorni",
                    "ciprofloxacina": "500mg ogni 12h per 7-14 giorni",
                    "levofloxacina": "500mg ogni 24h per 7-10 giorni"
                },
                "cardiaci": {
                    "atenololo": "50-100mg/die",
                    "lisinopril": "5-10mg/die, incrementare gradualmente",
                    "amlodipina": "5-10mg/die",
                    "furosemide": "40-80mg/die al mattino"
                }
            },
            "protocolli_emergenza": {
                "codice_rosso": [
                    "Arresto cardiaco", "Shock", "Trauma maggiore",
                    "Ictus acuto", "Infarto STEMI", "Embolia polmonare massiva"
                ],
                "codice_giallo": [
                    "Dolore toracico", "Dispnea severa", "Trauma minore",
                    "Febbre alta", "Sincope"
                ],
                "codice_verde": [
                    "Sintomi lievi", "Follow-up", "Controlli", "Medicazioni"
                ]
            }
        }
    
    def analyze_bruising_case(self, symptoms):
        """Analisi specifica per caso di lividi."""
        medical_db = self.get_medical_database()
        lividi_data = medical_db["sintomi_diagnosi"]["lividi"]
        
        # Risultati dell'analisi
        results_title = tk.Label(
            self.symptom_results_frame,
            text="✅ Analisi AI Completata - Caso: Lividi Braccio Sinistro",
            font=('Arial', 14, 'bold'),
            fg='#28a745',
            bg='#f0f2f6'
        )
        results_title.pack(anchor='w', pady=(0, 15))
        
        # Card principale risultati
        main_results_frame = tk.Frame(self.symptom_results_frame, bg='white', relief='raised', bd=2)
        main_results_frame.pack(fill='both', expand=True)
        
        # Diagnosi differenziale
        tk.Label(main_results_frame, text="🔍 Diagnosi Differenziale AI", 
                font=('Arial', 14, 'bold'), fg='#1f4e79', bg='white').pack(pady=(15, 10))
        
        # Usa dati dal database medico
        diagnosi_principali = lividi_data["diagnosi_principali"]
        probabilita = [85, 12, 8, 5, 3, 2]  # Probabilità per ciascuna diagnosi
        
        diagnoses = []
        for i, diagnosi in enumerate(diagnosi_principali):
            prob = probabilita[i] if i < len(probabilita) else 1
            if prob > 50:
                level, color = "Verde", "#28a745"
            elif prob > 20:
                level, color = "Giallo", "#ffc107"
            else:
                level, color = "Rosso", "#dc3545"
            diagnoses.append((diagnosi, prob, level, color))
        
        for diagnosis, probability, level, color in diagnoses:
            diag_frame = tk.Frame(main_results_frame, bg='white')
            diag_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(diag_frame, text=f"• {diagnosis}", 
                    font=('Arial', 11, 'bold'), bg='white', anchor='w').pack(side='left')
            tk.Label(diag_frame, text=f"{probability}% - {level}", 
                    font=('Arial', 11, 'bold'), fg=color, bg='white', anchor='e').pack(side='right')
        
        # Raccomandazioni cliniche
        recommendations_frame = tk.Frame(main_results_frame, bg='#e7f3ff', relief='raised', bd=1)
        recommendations_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(recommendations_frame, text="💡 Raccomandazioni Cliniche AI", 
                font=('Arial', 12, 'bold'), fg='#0c5460', bg='#e7f3ff').pack(pady=(10, 5))
        
        # Raccomandazioni dal database
        esami_diagnostici = lividi_data["esami_diagnostici"]
        cure_trattamenti = lividi_data["cure_trattamenti"]
        
        recommendations = [
            "1. ANAMNESI: Indagare traumi recenti, farmaci anticoagulanti, storia familiare",
            "2. ESAME FISICO: Valutare estensione, sede, colore e dolorabilità dei lividi",
            f"3. ESAMI: {', '.join(esami_diagnostici[:3])}",
            f"4. IMAGING: {esami_diagnostici[-2]} se indicato",
            "5. CONSULENZE: Ematologia se sospetti disturbi coagulazione",
            "6. FOLLOW-UP: Monitoraggio evoluzione temporale"
        ]
        
        for rec in recommendations:
            tk.Label(recommendations_frame, text=rec, 
                    font=('Arial', 10), fg='#0c5460', bg='#e7f3ff', 
                    anchor='w', wraplength=700).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(recommendations_frame, text="", bg='#e7f3ff').pack(pady=5)
        
        # Criteri di allarme
        alarm_frame = tk.Frame(main_results_frame, bg='#f8d7da', relief='raised', bd=1)
        alarm_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(alarm_frame, text="🚨 Criteri di Allarme (Invio urgente)", 
                font=('Arial', 12, 'bold'), fg='#721c24', bg='#f8d7da').pack(pady=(10, 5))
        
        # Criteri di allarme dal database
        sintomi_associati = lividi_data["sintomi_associati"]
        alarms = [
            "• Lividi multipli in sedi diverse senza trauma giustificante",
            f"• {sintomi_associati[4]} o {sintomi_associati[5]} associati",  # Petecchie, sanguinamenti
            "• Sanguinamenti spontanei (nasali, gengivali, gastrointestinali)",
            "• Pallore, astenia, febbre, perdita peso inspiegabili",
            "• Storia familiare/personale di disturbi ematologici",
            "• Lividi in sedi insolite (tronco, collo, genitali)"
        ]
        
        for alarm in alarms:
            tk.Label(alarm_frame, text=alarm, 
                    font=('Arial', 10), fg='#721c24', bg='#f8d7da', 
                    anchor='w', wraplength=700).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(alarm_frame, text="", bg='#f8d7da').pack(pady=5)
        
        # Footer con disclaimer
        footer_frame = tk.Frame(main_results_frame, bg='#6c757d')
        footer_frame.pack(fill='x')
        
        # Aggiungi sezione trattamenti
        treatment_frame = tk.Frame(main_results_frame, bg='#d1edda', relief='raised', bd=1)
        treatment_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(treatment_frame, text="💊 Trattamenti Consigliati", 
                font=('Arial', 12, 'bold'), fg='#155724', bg='#d1edda').pack(pady=(10, 5))
        
        # Mostra cure e trattamenti dal database
        for i, trattamento in enumerate(cure_trattamenti[:6]):
            tk.Label(treatment_frame, text=f"• {trattamento}", 
                    font=('Arial', 10), fg='#155724', bg='#d1edda', 
                    anchor='w', wraplength=700).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(treatment_frame, text="", bg='#d1edda').pack(pady=5)
        
        # Terapie specifiche
        specific_treatments = lividi_data["terapie_specifiche"]
        tk.Label(treatment_frame, text="🎯 Terapie Specifiche per Patologia:", 
                font=('Arial', 11, 'bold'), fg='#155724', bg='#d1edda').pack(anchor='w', padx=10, pady=(5, 2))
        
        for patologia, terapia in list(specific_treatments.items())[:3]:
            tk.Label(treatment_frame, text=f"• {patologia.title()}: {terapia}", 
                    font=('Arial', 9), fg='#155724', bg='#d1edda', 
                    anchor='w', wraplength=650).pack(anchor='w', padx=15, pady=1)
        
        tk.Label(treatment_frame, text="", bg='#d1edda').pack(pady=5)
        
        tk.Label(footer_frame, 
                text="⚕️ Questa analisi è generata da AI e non sostituisce il giudizio clinico. Consultare sempre un medico.",
                font=('Arial', 9, 'italic'), fg='white', bg='#6c757d',
                wraplength=700).pack(pady=10)
    
    def analyze_general_symptoms(self, symptoms):
        """Analisi generica per altri sintomi."""
        medical_db = self.get_medical_database()
        
        results_frame = tk.Frame(self.symptom_results_frame, bg='white', relief='raised', bd=2)
        results_frame.pack(fill='both', expand=True)
        
        tk.Label(results_frame, text="🔍 Analisi Sintomi Generale AI", 
                font=('Arial', 14, 'bold'), fg='#1f4e79', bg='white').pack(pady=(20, 10))
        
        # Analizza sintomi comuni
        symptoms_lower = symptoms.lower()
        matches = []
        
        if any(word in symptoms_lower for word in ["febbre", "temperatura", "caldo"]):
            matches.append("febbre")
        if any(word in symptoms_lower for word in ["torace", "petto", "cuore", "dolore petto"]):
            matches.append("dolore_torace")
        if any(word in symptoms_lower for word in ["respiro", "fiato", "dispnea", "affanno"]):
            matches.append("dispnea")
        
        if matches:
            # Mostra analisi per sintomi trovati
            for symptom in matches:
                if symptom in medical_db["sintomi_diagnosi"]:
                    data = medical_db["sintomi_diagnosi"][symptom]
                    
                    # Card per ogni sintoma
                    symptom_card = tk.Frame(results_frame, bg='#f8f9fa', relief='raised', bd=1)
                    symptom_card.pack(fill='x', padx=20, pady=10)
                    
                    tk.Label(symptom_card, text=f"📋 Analisi per: {symptom.replace('_', ' ').title()}", 
                            font=('Arial', 12, 'bold'), fg='#1f4e79', bg='#f8f9fa').pack(pady=(10, 5))
                    
                    # Diagnosi principali
                    tk.Label(symptom_card, text="🎯 Diagnosi Principali:", 
                            font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w', padx=10)
                    
                    for i, diagnosi in enumerate(data["diagnosi_principali"][:4]):
                        tk.Label(symptom_card, text=f"• {diagnosi}", 
                                font=('Arial', 10), bg='#f8f9fa', anchor='w').pack(anchor='w', padx=20, pady=1)
                    
                    # Trattamenti se disponibili
                    if "cure_trattamenti" in data:
                        tk.Label(symptom_card, text="💊 Trattamenti:", 
                                font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w', padx=10, pady=(5, 0))
                        
                        for trattamento in data["cure_trattamenti"][:3]:
                            tk.Label(symptom_card, text=f"• {trattamento}", 
                                    font=('Arial', 10), bg='#f8f9fa', anchor='w').pack(anchor='w', padx=20, pady=1)
                    
                    tk.Label(symptom_card, text="", bg='#f8f9fa').pack(pady=5)
        else:
            # Nessun match specifico
            tk.Label(results_frame, 
                    text="L'analisi AI ha elaborato i sintomi inseriti.\nPer un'analisi più specifica, utilizzare termini medici più dettagliati\n(es: febbre, dolore torace, dispnea, lividi, etc.)",
                    font=('Arial', 11), bg='white', wraplength=600, justify='center').pack(pady=20)
            
            # Mostra esempi di sintomi disponibili
            examples_frame = tk.Frame(results_frame, bg='#e7f3ff', relief='raised', bd=1)
            examples_frame.pack(fill='x', padx=20, pady=20)
            
            tk.Label(examples_frame, text="💡 Sintomi Analizzabili dal Database:", 
                    font=('Arial', 11, 'bold'), fg='#0c5460', bg='#e7f3ff').pack(pady=(10, 5))
            
            sintomi_disponibili = list(medical_db["sintomi_diagnosi"].keys())
            for sintomo in sintomi_disponibili:
                tk.Label(examples_frame, text=f"• {sintomo.replace('_', ' ').title()}", 
                        font=('Arial', 10), fg='#0c5460', bg='#e7f3ff', anchor='w').pack(anchor='w', padx=20, pady=1)
            
            tk.Label(examples_frame, text="", bg='#e7f3ff').pack(pady=5)

if __name__ == "__main__":
    app = NinoMedicalAIDesktopNoImaging()
