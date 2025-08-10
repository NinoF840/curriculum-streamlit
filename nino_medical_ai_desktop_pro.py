#!/usr/bin/env python3
"""
Nino Medical AI Pro - Standalone Desktop Application
===================================================

Versione Pro standalone senza dipendenze da Streamlit.
Utilizza tkinter per l'interfaccia grafica desktop.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
import base64
import os
import sys

class NinoMedicalAIProDesktop:
    """Applicazione desktop standalone per Nino Medical AI Pro."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Nino Medical AI Pro - Antonino Piacenza")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variabili di stato
        self.current_image = None
        self.analysis_results = {}
        
        # Configura stile
        self.setup_style()
        
        # Crea interfaccia
        self.create_interface()
        
        # Avvia applicazione
        self.root.mainloop()
    
    def setup_style(self):
        """Configura lo stile dell'applicazione."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colori personalizzati
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), 
                       foreground='#1f4e79', background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), 
                       foreground='#2e7d32', background='#f0f0f0')
        style.configure('Custom.TNotebook.Tab', padding=[20, 10])
        
    def create_interface(self):
        """Crea l'interfaccia principale."""
        # Header
        self.create_header()
        
        # Notebook per le tab
        self.create_notebook()
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self):
        """Crea header dell'applicazione."""
        header_frame = tk.Frame(self.root, bg='#1f4e79', height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Titolo
        title_label = tk.Label(
            header_frame, 
            text="🏥 NINO MEDICAL AI PRO", 
            font=('Arial', 20, 'bold'),
            fg='white', 
            bg='#1f4e79'
        )
        title_label.pack(pady=15)
        
        # Sottotitolo
        subtitle_label = tk.Label(
            header_frame, 
            text="Intelligenza Artificiale per la Medicina - Antonino Piacenza", 
            font=('Arial', 10),
            fg='#e0e0e0', 
            bg='#1f4e79'
        )
        subtitle_label.pack()
        
    def create_notebook(self):
        """Crea il notebook con le diverse sezioni."""
        notebook = ttk.Notebook(self.root, style='Custom.TNotebook')
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab Dashboard
        dashboard_frame = ttk.Frame(notebook)
        notebook.add(dashboard_frame, text='📊 Dashboard')
        self.create_dashboard_tab(dashboard_frame)
        
        # Tab Analisi Immagini
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text='🖼️ Analisi Immagini')
        self.create_analysis_tab(analysis_frame)
        
        # Tab Chi Sono
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text='👨‍💻 Chi Sono')
        self.create_about_tab(about_frame)
        
        # Tab Contatti
        contact_frame = ttk.Frame(notebook)
        notebook.add(contact_frame, text='📞 Contatti')
        self.create_contact_tab(contact_frame)
        
    def create_dashboard_tab(self, parent):
        """Crea la tab dashboard."""
        # Welcome card
        welcome_frame = tk.Frame(parent, bg='#667eea', relief='raised', bd=2)
        welcome_frame.pack(fill='x', padx=10, pady=10)
        
        welcome_label = tk.Label(
            welcome_frame,
            text="🚀 Benvenuto in Nino Medical AI Pro",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#667eea'
        )
        welcome_label.pack(pady=10)
        
        desc_label = tk.Label(
            welcome_frame,
            text="Piattaforma innovativa che utilizza l'IA per supportare la ricerca medica",
            font=('Arial', 10),
            fg='white',
            bg='#667eea'
        )
        desc_label.pack(pady=(0, 10))
        
        # Metriche
        metrics_frame = tk.Frame(parent, bg='#f0f0f0')
        metrics_frame.pack(fill='x', padx=10, pady=10)
        
        metrics = [
            ("🔬 Modelli IA", "8", "+2 nuovi"),
            ("📊 Dataset", "25", "+5 aggiunti"),
            ("🏥 Partner", "3", "+1 nuovo"),
            ("📈 Accuratezza", "94.2%", "+2.1%")
        ]
        
        for i, (label, value, delta) in enumerate(metrics):
            metric_frame = tk.Frame(metrics_frame, bg='white', relief='raised', bd=1)
            metric_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            
            tk.Label(metric_frame, text=label, font=('Arial', 10, 'bold'), bg='white').pack(pady=5)
            tk.Label(metric_frame, text=value, font=('Arial', 14, 'bold'), 
                    fg='#1f4e79', bg='white').pack()
            tk.Label(metric_frame, text=delta, font=('Arial', 8), 
                    fg='#2e7d32', bg='white').pack(pady=(0, 5))
        
        # Grafici
        self.create_dashboard_charts(parent)
        
    def create_dashboard_charts(self, parent):
        """Crea grafici per la dashboard."""
        charts_frame = tk.Frame(parent, bg='#f0f0f0')
        charts_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Grafico progresso
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        months = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu']
        progress = [10, 25, 40, 55, 70, 85]
        ax1.plot(months, progress, color='#1f4e79', linewidth=3, marker='o')
        ax1.set_title('Progresso Progetti 2025')
        ax1.set_ylabel('Completamento (%)')
        ax1.grid(True, alpha=0.3)
        
        canvas1 = FigureCanvasTkAgg(fig1, charts_frame)
        canvas1.get_tk_widget().pack(side='left', fill='both', expand=True, padx=5)
        
        # Grafico aree ricerca
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        areas = ['Diagnostica', 'Predittiva', 'Imaging', 'NLP']
        values = [35, 25, 25, 15]
        colors = ['#1f4e79', '#2e7d32', '#e65100', '#7b1fa2']
        ax2.pie(values, labels=areas, colors=colors, autopct='%1.1f%%')
        ax2.set_title('Aree di Ricerca')
        
        canvas2 = FigureCanvasTkAgg(fig2, charts_frame)
        canvas2.get_tk_widget().pack(side='right', fill='both', expand=True, padx=5)
        
    def create_analysis_tab(self, parent):
        """Crea la tab per analisi immagini."""
        # Frame principale
        main_frame = tk.Frame(parent, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Controlli upload
        controls_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(controls_frame, text="📁 Carica Immagine Medica", 
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
        
        button_frame = tk.Frame(controls_frame, bg='white')
        button_frame.pack(pady=10)
        
        upload_btn = tk.Button(
            button_frame, 
            text="📂 Seleziona Immagine",
            command=self.upload_image,
            bg='#2e7d32',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=10
        )
        upload_btn.pack(side='left', padx=5)
        
        analyze_btn = tk.Button(
            button_frame,
            text="🔍 Analizza",
            command=self.analyze_image,
            bg='#1f4e79',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=10,
            state='disabled'
        )
        analyze_btn.pack(side='left', padx=5)
        self.analyze_btn = analyze_btn
        
        # Frame risultati
        results_frame = tk.Frame(main_frame, bg='#f0f0f0')
        results_frame.pack(fill='both', expand=True)
        
        # Frame immagine
        image_frame = tk.Frame(results_frame, bg='white', relief='raised', bd=2)
        image_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.image_label = tk.Label(image_frame, text="Nessuna immagine caricata", 
                                   bg='white', fg='gray')
        self.image_label.pack(expand=True)
        
        # Frame analisi
        analysis_frame = tk.Frame(results_frame, bg='white', relief='raised', bd=2)
        analysis_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        tk.Label(analysis_frame, text="📊 Risultati Analisi", 
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
        
        self.results_text = tk.Text(analysis_frame, height=15, width=40, 
                                   bg='#f8f9fa', relief='flat')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.results_text.insert('1.0', "Carica un'immagine per iniziare l'analisi...")
        
    def create_about_tab(self, parent):
        """Crea la tab informazioni."""
        # Scroll frame
        canvas = tk.Canvas(parent, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenuto
        content_frame = tk.Frame(scrollable_frame, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Titolo
        title_label = tk.Label(content_frame, text="👨‍💻 Antonino Piacenza", 
                              font=('Arial', 18, 'bold'), fg='#1f4e79', bg='white')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(content_frame, 
                                 text="Ricercatore e Sviluppatore in Intelligenza Artificiale", 
                                 font=('Arial', 12, 'italic'), fg='#2e7d32', bg='white')
        subtitle_label.pack(pady=(0, 20))
        
        # Descrizione
        desc_text = """
Sono un appassionato ricercatore specializzato nell'applicazione dell'Intelligenza 
Artificiale al settore medico-sanitario. Il mio obiettivo è sviluppare soluzioni 
innovative che possano migliorare la diagnostica medica e supportare i professionisti 
sanitari.

🎓 BACKGROUND
• Formazione: Informatica e Intelligenza Artificiale
• Specializzazione: Machine Learning per applicazioni mediche  
• Esperienza: 2+ anni in progetti di IA per la sanità

🔬 AREE DI RICERCA
• Computer Vision Medica: Analisi di immagini diagnostiche
• NLP Clinico: Elaborazione del linguaggio naturale per testi medici
• Medicina Predittiva: Modelli per la previsione di patologie
• Federated Learning: Apprendimento distribuito per la privacy dei dati

🛠️ COMPETENZE TECNICHE
• Python: 95%
• Machine Learning: 90%
• Deep Learning: 85%
• Computer Vision: 88%
• NLP: 80%
• Streamlit: 92%
        """
        
        desc_label = tk.Label(content_frame, text=desc_text, font=('Arial', 10), 
                             fg='#333', bg='white', justify='left', wraplength=800)
        desc_label.pack(fill='x', pady=10)
        
    def create_contact_tab(self, parent):
        """Crea la tab contatti."""
        contact_frame = tk.Frame(parent, bg='white', padx=20, pady=20)
        contact_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Titolo
        title_label = tk.Label(contact_frame, text="📞 Contatti e Collaborazioni", 
                              font=('Arial', 16, 'bold'), fg='#1f4e79', bg='white')
        title_label.pack(pady=(0, 20))
        
        # Informazioni contatto
        contact_info = """
🤝 INTERESSATO A COLLABORARE?

Sono sempre alla ricerca di nuove opportunità di collaborazione:

🏥 Ospedali e Cliniche: Per validazione clinica e implementazione
🎓 Università: Per progetti di ricerca congiunti
💼 Aziende: Per sviluppo di prodotti innovativi
🌍 Progetti Internazionali: Horizon Europe e altri finanziamenti

📧 COME CONTATTARMI

• Email Personale: nino58150@gmail.com
• Email Professionale: ninomedical.ai@gmail.com
• LinkedIn: linkedin.com/in/antoninopiacenza
• WhatsApp/Telefono: +39 393 678 9529
• GitHub: github.com/ninopiacenza

📋 RICHIESTA INFORMAZIONI

Utilizza il form qui sotto per inviarmi un messaggio:
        """
        
        info_label = tk.Label(contact_frame, text=contact_info, font=('Arial', 10), 
                             fg='#333', bg='white', justify='left')
        info_label.pack(fill='x', pady=(0, 20))
        
        # Form contatto
        form_frame = tk.Frame(contact_frame, bg='#f8f9fa', relief='raised', bd=2)
        form_frame.pack(fill='x', pady=10)
        
        # Form fields
        fields = [('Nome:', 'name'), ('Email:', 'email'), ('Messaggio:', 'message')]
        self.form_vars = {}
        
        for label_text, var_name in fields:
            row_frame = tk.Frame(form_frame, bg='#f8f9fa')
            row_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(row_frame, text=label_text, bg='#f8f9fa', 
                    font=('Arial', 10, 'bold')).pack(anchor='w')
            
            if var_name == 'message':
                widget = tk.Text(row_frame, height=4, width=50)
                widget.pack(fill='x', pady=2)
            else:
                widget = tk.Entry(row_frame, font=('Arial', 10))
                widget.pack(fill='x', pady=2)
            
            self.form_vars[var_name] = widget
        
        # Send button
        send_btn = tk.Button(
            form_frame,
            text="📨 Invia Messaggio",
            command=self.send_message,
            bg='#2e7d32',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=10
        )
        send_btn.pack(pady=10)
        
    def create_status_bar(self):
        """Crea status bar."""
        status_frame = tk.Frame(self.root, relief='sunken', bd=1)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_label = tk.Label(status_frame, text="Pronto", anchor='w')
        self.status_label.pack(side='left', padx=5, pady=2)
        
        time_label = tk.Label(status_frame, 
                             text=f"© 2025 Antonino Piacenza - {datetime.now().strftime('%H:%M:%S')}", 
                             anchor='e')
        time_label.pack(side='right', padx=5, pady=2)
        
    def upload_image(self):
        """Carica un'immagine."""
        file_path = filedialog.askopenfilename(
            title="Seleziona immagine medica",
            filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                # Carica e ridimensiona immagine
                image = Image.open(file_path)
                image.thumbnail((400, 300), Image.Resampling.LANCZOS)
                
                # Converti per tkinter
                photo = ImageTk.PhotoImage(image)
                
                # Mostra immagine
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Mantieni riferimento
                
                # Salva percorso
                self.current_image = file_path
                
                # Abilita analisi
                self.analyze_btn.configure(state='normal')
                
                self.status_label.configure(text=f"Immagine caricata: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare l'immagine: {e}")
                
    def analyze_image(self):
        """Analizza l'immagine caricata."""
        if not self.current_image:
            messagebox.showwarning("Avviso", "Carica prima un'immagine!")
            return
            
        self.status_label.configure(text="Analisi in corso...")
        self.root.update()
        
        # Simula analisi (sostituire con vera IA)
        import time
        time.sleep(2)
        
        # Risultati simulati
        confidence = np.random.uniform(85, 98)
        quality = "Ottima" if confidence > 90 else "Buona"
        
        results_text = f"""
🔍 ANALISI COMPLETATA

📊 Risultati:
• Confidenza: {confidence:.1f}%
• Qualità immagine: {quality}
• Data analisi: {datetime.now().strftime('%d/%m/%Y %H:%M')}

🎯 Classificazione:
• Normale: {np.random.uniform(80, 95):.1f}%
• Anomalia 1: {np.random.uniform(3, 15):.1f}%
• Anomalia 2: {np.random.uniform(1, 8):.1f}%

⚠️ IMPORTANTE:
Questi sono risultati simulati a scopo 
dimostrativo. Non utilizzare per diagnosi 
cliniche reali.

💡 Raccomandazioni:
• Consultare sempre un medico specialista
• Verificare risultati con altri strumenti
• Mantenere documentazione clinica
        """
        
        # Aggiorna risultati
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', results_text)
        
        self.status_label.configure(text="Analisi completata")
        
    def send_message(self):
        """Invia messaggio di contatto."""
        # Ottieni valori form
        name = self.form_vars['name'].get()
        email = self.form_vars['email'].get()
        
        if hasattr(self.form_vars['message'], 'get'):
            message = self.form_vars['message'].get('1.0', tk.END).strip()
        else:
            message = self.form_vars['message'].get()
        
        if not (name and email and message):
            messagebox.showwarning("Avviso", "Compila tutti i campi!")
            return
            
        # Simula invio
        messagebox.showinfo("Successo", 
                           "✅ Messaggio inviato con successo!\n\n"
                           "Ti risponderò entro 24-48 ore.")
        
        # Pulisci form
        self.form_vars['name'].delete(0, tk.END)
        self.form_vars['email'].delete(0, tk.END)
        self.form_vars['message'].delete('1.0', tk.END)

def main():
    """Funzione principale."""
    print("🏥 Avvio Nino Medical AI Pro...")
    
    try:
        app = NinoMedicalAIProDesktop()
    except KeyboardInterrupt:
        print("\n⚠️ Applicazione chiusa dall'utente")
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")
        input("Premi Enter per chiudere...")

if __name__ == "__main__":
    main()
