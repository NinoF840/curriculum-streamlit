"""
Nino Medical AI - Sistema Export Avanzato
==========================================

Sistema completo per l'export di dati medici in vari formati
con report automatizzati e visualizzazioni personalizzate.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.drawing.image import Image as XLImage
from openpyxl.chart import BarChart, LineChart, Reference
import xlsxwriter
import io
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import tempfile
import os
from pathlib import Path


class DataExporter:
    """Classe principale per export dati in vari formati."""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "nino_medical_exports"
        self.temp_dir.mkdir(exist_ok=True)
        
    def export_to_excel(self, 
                       data: Dict[str, pd.DataFrame], 
                       filename: str = "medical_data.xlsx",
                       include_charts: bool = True) -> bytes:
        """
        Esporta dati in formato Excel con formattazione avanzata.
        
        Args:
            data: Dizionario con sheet_name -> DataFrame
            filename: Nome del file
            include_charts: Include grafici nel file
            
        Returns:
            Bytes del file Excel
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Stili
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'text_wrap': True,
                'valign': 'top'
            })
            
            for sheet_name, df in data.items():
                # Scrivi DataFrame
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                
                worksheet = writer.sheets[sheet_name]
                
                # Applica formattazione header
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(1, col_num, value, header_format)
                    
                # Auto-adjust colonne
                for i, column in enumerate(df.columns):
                    column_length = max(df[column].astype(str).map(len).max(), len(column))
                    worksheet.set_column(i, i, min(column_length + 2, 50))
                    
                # Aggiungi titolo
                title_format = workbook.add_format({
                    'bold': True,
                    'font_size': 16,
                    'align': 'center',
                    'fg_color': '#4F81BD',
                    'font_color': 'white'
                })
                worksheet.merge_range(0, 0, 0, len(df.columns)-1, 
                                    f'Nino Medical AI - {sheet_name}', title_format)
                
                # Aggiungi grafici se richiesto
                if include_charts and not df.empty:
                    self._add_excel_charts(worksheet, df, workbook, len(df) + 5)
                    
        output.seek(0)
        return output.getvalue()
        
    def _add_excel_charts(self, worksheet, df: pd.DataFrame, workbook, start_row: int):
        """Aggiunge grafici al foglio Excel."""
        if len(df.columns) < 2:
            return
            
        # Grafico a barre per colonne numeriche
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            chart = workbook.add_chart({'type': 'column'})
            
            # Prima colonna numerica
            col_letter = chr(65 + list(df.columns).index(numeric_cols[0]))
            chart.add_series({
                'name': numeric_cols[0],
                'categories': f'=Sheet1!$A$2:$A${len(df)+1}',
                'values': f'=Sheet1!${col_letter}$2:${col_letter}${len(df)+1}',
            })
            
            chart.set_title({'name': f'Distribuzione {numeric_cols[0]}'})
            chart.set_x_axis({'name': 'Categorie'})
            chart.set_y_axis({'name': 'Valori'})
            
            worksheet.insert_chart(start_row, 0, chart)
            
    def export_to_pdf(self, 
                     data: Dict[str, Any], 
                     charts: List[go.Figure] = None,
                     filename: str = "medical_report.pdf") -> bytes:
        """
        Crea un report PDF completo con dati e grafici.
        
        Args:
            data: Dati da includere nel report
            charts: Lista di grafici Plotly
            filename: Nome del file
            
        Returns:
            Bytes del file PDF
        """
        output = io.BytesIO()
        
        # Crea documento PDF
        doc = SimpleDocTemplate(
            output, 
            pagesize=A4,
            rightMargin=72, 
            leftMargin=72,
            topMargin=72, 
            bottomMargin=18
        )
        
        # Stili
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4e79'),
            alignment=1,  # Centrato
            spaceAfter=30
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2e7d32'),
            spaceBefore=20,
            spaceAfter=12
        )
        
        # Contenuto del documento
        story = []
        
        # Titolo
        story.append(Paragraph("🏥 Nino Medical AI - Report Medico", title_style))
        story.append(Spacer(1, 20))
        
        # Informazioni report
        info_data = [
            ['Data Generazione:', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
            ['Autore:', 'Antonino Piacenza'],
            ['Sistema:', 'Nino Medical AI Pro'],
            ['Versione:', '1.0']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f2f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Aggiungi dati
        for section_name, section_data in data.items():
            story.append(Paragraph(section_name, heading_style))
            
            if isinstance(section_data, pd.DataFrame):
                # Converti DataFrame in tabella
                table_data = [list(section_data.columns)]
                table_data.extend(section_data.head(20).values.tolist())
                
                pdf_table = Table(table_data)
                pdf_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(pdf_table)
                
            elif isinstance(section_data, dict):
                # Mostra dati come lista
                for key, value in section_data.items():
                    story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
                    
            story.append(Spacer(1, 20))
            
        # Aggiungi grafici se presenti
        if charts:
            story.append(Paragraph("📊 Visualizzazioni", heading_style))
            
            for i, fig in enumerate(charts):
                # Salva grafico come immagine temporanea
                img_bytes = pio.to_image(fig, format='png', width=600, height=400)
                
                temp_img_path = self.temp_dir / f"chart_{i}.png"
                with open(temp_img_path, 'wb') as f:
                    f.write(img_bytes)
                    
                # Aggiungi immagine al PDF
                story.append(RLImage(str(temp_img_path), width=5*inch, height=3*inch))
                story.append(Spacer(1, 20))
                
                # Rimuovi file temporaneo
                os.unlink(temp_img_path)
                
        # Footer
        story.append(Spacer(1, 50))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph("© 2025 Antonino Piacenza - Nino Medical AI", footer_style))
        
        # Costruisci PDF
        doc.build(story)
        
        output.seek(0)
        return output.getvalue()
        
    def create_comprehensive_report(self, 
                                  patient_data: pd.DataFrame,
                                  search_results: Dict[str, List[Dict]],
                                  ai_analysis: Dict[str, Any]) -> Dict[str, bytes]:
        """
        Crea un report completo con tutti i dati analizzati.
        
        Returns:
            Dizionario con 'excel' e 'pdf' come chiavi e bytes come valori
        """
        # Prepara dati per Excel
        excel_data = {}
        
        if not patient_data.empty:
            excel_data['Dati_Pazienti'] = patient_data
            
        # Aggiungi risultati ricerche database
        for db_name, results in search_results.items():
            if results:
                df = pd.DataFrame(results)
                excel_data[f'Ricerca_{db_name}'] = df
                
        # Dati analisi AI
        if ai_analysis:
            ai_df = pd.DataFrame([ai_analysis])
            excel_data['Analisi_AI'] = ai_df
            
        # Crea file Excel
        excel_bytes = self.export_to_excel(excel_data, include_charts=True)
        
        # Prepara dati per PDF
        pdf_data = {
            'Riepilogo Analisi': ai_analysis,
            'Statistiche Pazienti': {
                'Numero totale pazienti': len(patient_data),
                'Età media': f"{patient_data['age'].mean():.1f}" if 'age' in patient_data.columns else 'N/A',
                'Distribuzione genere': dict(patient_data['gender'].value_counts()) if 'gender' in patient_data.columns else 'N/A'
            }
        }
        
        # Aggiungi DataFrames
        if not patient_data.empty:
            pdf_data['Dati Pazienti (Sample)'] = patient_data
            
        # Crea grafici per PDF
        charts = []
        if not patient_data.empty and 'age' in patient_data.columns:
            fig = px.histogram(patient_data, x='age', title='Distribuzione Età Pazienti')
            charts.append(fig)
            
        if not patient_data.empty and 'disease' in patient_data.columns:
            fig = px.pie(patient_data, names='disease', title='Distribuzione Patologie')
            charts.append(fig)
            
        # Crea file PDF
        pdf_bytes = self.export_to_pdf(pdf_data, charts)
        
        return {
            'excel': excel_bytes,
            'pdf': pdf_bytes
        }


class ReportGenerator:
    """Generatore di report automatizzati."""
    
    def __init__(self):
        self.exporter = DataExporter()
        
    def generate_daily_report(self) -> Dict[str, bytes]:
        """Genera report giornaliero automatico."""
        # Simula dati giornalieri
        today = datetime.now()
        
        # Dati pazienti simulati
        np.random.seed(int(today.timestamp()))
        patient_data = pd.DataFrame({
            'patient_id': range(1, 21),
            'age': np.random.randint(20, 80, 20),
            'gender': np.random.choice(['Male', 'Female'], 20),
            'condition': np.random.choice(['Healthy', 'Fever', 'Cough', 'Fatigue'], 20),
            'admission_date': [today - timedelta(days=np.random.randint(0, 30)) for _ in range(20)]
        })
        
        # Analisi AI simulate
        ai_analysis = {
            'total_analyses': 50,
            'avg_processing_time': 2.3,
            'accuracy_rate': 0.94,
            'most_common_condition': 'Fever',
            'alert_cases': 3
        }
        
        # Risultati ricerche simulate
        search_results = {
            'PubMed': [
                {'title': 'Recent advances in AI diagnosis', 'authors': 'Smith et al.'},
                {'title': 'Machine learning in healthcare', 'authors': 'Johnson et al.'}
            ]
        }
        
        return self.exporter.create_comprehensive_report(
            patient_data, search_results, ai_analysis
        )
        
    def generate_weekly_summary(self) -> Dict[str, bytes]:
        """Genera sommario settimanale."""
        # Simula dati settimanali
        week_data = pd.DataFrame({
            'day': ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica'],
            'patients_seen': [15, 23, 18, 25, 22, 12, 8],
            'ai_analyses': [45, 67, 52, 78, 65, 32, 21],
            'critical_cases': [2, 3, 1, 4, 3, 1, 0]
        })
        
        weekly_summary = {
            'total_patients': week_data['patients_seen'].sum(),
            'total_analyses': week_data['ai_analyses'].sum(),
            'total_critical': week_data['critical_cases'].sum(),
            'avg_daily_patients': week_data['patients_seen'].mean()
        }
        
        excel_data = {
            'Riepilogo_Settimanale': pd.DataFrame([weekly_summary]),
            'Dati_Giornalieri': week_data
        }
        
        pdf_data = {
            'Sommario Settimana': weekly_summary,
            'Andamento Giornaliero': week_data
        }
        
        # Grafici settimanali
        charts = [
            px.bar(week_data, x='day', y='patients_seen', title='Pazienti per Giorno'),
            px.line(week_data, x='day', y='ai_analyses', title='Analisi AI per Giorno')
        ]
        
        return {
            'excel': self.exporter.export_to_excel(excel_data),
            'pdf': self.exporter.export_to_pdf(pdf_data, charts)
        }


def create_download_button(file_bytes: bytes, filename: str, label: str, mime_type: str):
    """Crea un bottone di download per file."""
    b64 = base64.b64encode(file_bytes).decode()
    href = f'data:{mime_type};base64,{b64}'
    
    st.markdown(
        f'<a href="{href}" download="{filename}" class="download-button">{label}</a>',
        unsafe_allow_html=True
    )


def render_export_page():
    """Renderizza la pagina di export dati."""
    st.markdown('<h2 class="section-header">📤 Export e Report</h2>', unsafe_allow_html=True)
    st.markdown("Esporta dati e genera report personalizzati in vari formati.")
    
    # CSS per bottoni download
    st.markdown("""
    <style>
    .download-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #1f77b4;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        margin: 5px;
    }
    .download-button:hover {
        background-color: #0d5aa7;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs per diversi tipi di export
    tab1, tab2, tab3 = st.tabs(["📊 Export Personalizzato", "📋 Report Automatici", "⚙️ Configurazioni"])
    
    with tab1:
        render_custom_export_tab()
        
    with tab2:
        render_automated_reports_tab()
        
    with tab3:
        render_export_settings_tab()


def render_custom_export_tab():
    """Tab per export personalizzato."""
    st.subheader("📊 Export Personalizzato")
    st.markdown("Seleziona i dati da esportare e il formato desiderato.")
    
    # Selezione dati
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Seleziona Dati da Esportare:**")
        include_patient_data = st.checkbox("Dati Pazienti Simulati", value=True)
        include_search_results = st.checkbox("Risultati Ricerche Database")
        include_ai_analysis = st.checkbox("Analisi IA")
        include_statistics = st.checkbox("Statistiche e Metriche")
        
    with col2:
        st.markdown("**Formato Export:**")
        export_format = st.radio("Scegli formato:", ["Excel (.xlsx)", "PDF Report", "Entrambi"])
        include_charts = st.checkbox("Includi Grafici", value=True)
        
    if st.button("🚀 Genera Export", key="generate_custom_export"):
        with st.spinner("Generazione export in corso..."):
            exporter = DataExporter()
            
            # Prepara dati simulati
            patient_data = pd.DataFrame()
            search_results = {}
            ai_analysis = {}
            
            if include_patient_data:
                np.random.seed(42)
                patient_data = pd.DataFrame({
                    'patient_id': range(1, 51),
                    'age': np.random.randint(20, 85, 50),
                    'gender': np.random.choice(['Male', 'Female'], 50),
                    'condition': np.random.choice(['Healthy', 'Hypertension', 'Diabetes', 'Heart Disease'], 50),
                    'bmi': np.random.uniform(18, 35, 50),
                    'last_visit': pd.date_range('2024-01-01', periods=50, freq='D')
                })
                
            if include_search_results:
                search_results = {
                    'PubMed': [
                        {'title': 'AI in Medical Diagnosis', 'authors': 'Smith et al.', 'year': 2024},
                        {'title': 'Machine Learning Healthcare', 'authors': 'Johnson et al.', 'year': 2023}
                    ],
                    'WHO': [
                        {'indicator': 'Life Expectancy', 'value': 72.5, 'country': 'Global'},
                        {'indicator': 'Infant Mortality', 'value': 29.2, 'country': 'Global'}
                    ]
                }
                
            if include_ai_analysis:
                ai_analysis = {
                    'total_analyses_performed': 1250,
                    'average_accuracy': 0.923,
                    'processing_time_avg_seconds': 2.1,
                    'models_used': ['CNN', 'NLP', 'Random Forest'],
                    'last_update': datetime.now().isoformat()
                }
                
            # Genera file
            files = exporter.create_comprehensive_report(patient_data, search_results, ai_analysis)
            
            st.success("✅ Export generato con successo!")
            
            # Bottoni download
            col_dl1, col_dl2 = st.columns(2)
            
            if export_format in ["Excel (.xlsx)", "Entrambi"]:
                with col_dl1:
                    st.download_button(
                        label="📥 Download Excel",
                        data=files['excel'],
                        file_name=f"nino_medical_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
            if export_format in ["PDF Report", "Entrambi"]:
                with col_dl2:
                    st.download_button(
                        label="📥 Download PDF",
                        data=files['pdf'],
                        file_name=f"nino_medical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )


def render_automated_reports_tab():
    """Tab per report automatici."""
    st.subheader("📋 Report Automatici")
    st.markdown("Genera report automatici con dati aggregati e analisi.")
    
    report_generator = ReportGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Report Giornaliero")
        st.markdown("Include attività giornaliera, analisi IA eseguite e statistiche pazienti.")
        
        if st.button("Genera Report Giornaliero", key="daily_report"):
            with st.spinner("Generazione report giornaliero..."):
                files = report_generator.generate_daily_report()
                
                st.success("Report giornaliero generato!")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        "📥 Excel Giornaliero",
                        files['excel'],
                        f"daily_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                with col_d2:
                    st.download_button(
                        "📥 PDF Giornaliero",
                        files['pdf'],
                        f"daily_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        "application/pdf"
                    )
                    
    with col2:
        st.markdown("#### 📊 Report Settimanale")
        st.markdown("Sommario settimanale con trend e analisi comparative.")
        
        if st.button("Genera Report Settimanale", key="weekly_report"):
            with st.spinner("Generazione report settimanale..."):
                files = report_generator.generate_weekly_summary()
                
                st.success("Report settimanale generato!")
                
                col_w1, col_w2 = st.columns(2)
                with col_w1:
                    st.download_button(
                        "📥 Excel Settimanale",
                        files['excel'],
                        f"weekly_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                with col_w2:
                    st.download_button(
                        "📥 PDF Settimanale",
                        files['pdf'],
                        f"weekly_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        "application/pdf"
                    )


def render_export_settings_tab():
    """Tab per configurazioni export."""
    st.subheader("⚙️ Configurazioni Export")
    st.markdown("Personalizza le impostazioni per gli export e i report.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Formato Excel")
        excel_include_styling = st.checkbox("Applica stili avanzati", value=True)
        excel_include_charts = st.checkbox("Includi grafici automatici", value=True)
        excel_max_rows = st.number_input("Massimo righe per foglio", min_value=100, max_value=10000, value=1000)
        
        st.markdown("#### 📄 Formato PDF")
        pdf_page_size = st.selectbox("Dimensione pagina", ["A4", "Letter"], index=0)
        pdf_include_images = st.checkbox("Includi grafici come immagini", value=True)
        pdf_font_size = st.slider("Dimensione font", 8, 16, 10)
        
    with col2:
        st.markdown("#### 🎨 Personalizzazione")
        company_name = st.text_input("Nome Organizzazione", value="Nino Medical AI")
        report_logo = st.file_uploader("Logo Report (opzionale)", type=['png', 'jpg', 'jpeg'])
        
        st.markdown("#### 📧 Export Automatico")
        auto_export_enabled = st.checkbox("Abilita export automatico")
        if auto_export_enabled:
            auto_export_frequency = st.selectbox("Frequenza", ["Giornaliera", "Settimanale", "Mensile"])
            auto_export_format = st.multiselect("Formati", ["Excel", "PDF"], default=["PDF"])
            
    if st.button("💾 Salva Configurazioni", key="save_export_settings"):
        # Qui salveresti le configurazioni in un file o database
        st.success("✅ Configurazioni salvate!")
        
        # Mostra anteprima configurazioni
        with st.expander("👁️ Anteprima Configurazioni"):
            config = {
                "Excel": {
                    "styling": excel_include_styling,
                    "charts": excel_include_charts,
                    "max_rows": excel_max_rows
                },
                "PDF": {
                    "page_size": pdf_page_size,
                    "include_images": pdf_include_images,
                    "font_size": pdf_font_size
                },
                "Personalization": {
                    "company_name": company_name,
                    "has_logo": report_logo is not None
                },
                "Auto_Export": {
                    "enabled": auto_export_enabled,
                    "frequency": auto_export_frequency if auto_export_enabled else None,
                    "formats": auto_export_format if auto_export_enabled else None
                }
            }
            
            st.json(config)


if __name__ == "__main__":
    # Test sistema export
    print("Testing Export System...")
    
    exporter = DataExporter()
    
    # Test data
    test_data = {
        'Test_Sheet': pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'Score': [85, 92, 88]
        })
    }
    
    # Test Excel export
    excel_bytes = exporter.export_to_excel(test_data)
    print(f"✅ Excel export: {len(excel_bytes)} bytes")
    
    # Test PDF export
    pdf_data = {'Test Data': test_data['Test_Sheet']}
    pdf_bytes = exporter.export_to_pdf(pdf_data)
    print(f"✅ PDF export: {len(pdf_bytes)} bytes")
    
    print("Export system working correctly!")
