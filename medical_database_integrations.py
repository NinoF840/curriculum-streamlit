"""
Nino Medical AI - Integrazioni Database Medici Mondiali
======================================================

Modulo per l'integrazione con database medici pubblici senza autenticazione.
Supporta varie fonti di dati medici globali per ricerca e sviluppo IA.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import requests
import pandas as pd
import json
import streamlit as st
from typing import Dict, List, Optional, Any
import xml.etree.ElementTree as ET
from datetime import datetime
import time


class MedicalDatabaseIntegrator:
    """Classe principale per l'integrazione con database medici mondiali."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Nino-Medical-AI/1.0 (ninomedical.ai@gmail.com)'
        })
    
    def get_pubmed_articles(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Ricerca articoli su PubMed tramite API pubblica.
        
        Args:
            query: Termine di ricerca
            max_results: Numero massimo di risultati
            
        Returns:
            Lista di articoli con metadati
        """
        try:
            # PubMed E-utilities API (gratuita, senza autenticazione)
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'retmode': 'json'
            }
            
            response = self.session.get(search_url, params=search_params)
            search_data = response.json()
            
            if 'esearchresult' not in search_data:
                return []
                
            pmids = search_data['esearchresult'].get('idlist', [])
            
            if not pmids:
                return []
            
            # Recupera dettagli degli articoli
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'xml'
            }
            
            response = self.session.get(fetch_url, params=fetch_params)
            
            # Parse XML response
            root = ET.fromstring(response.content)
            articles = []
            
            for article in root.findall('.//PubmedArticle'):
                try:
                    title_elem = article.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else "N/A"
                    
                    abstract_elem = article.find('.//AbstractText')
                    abstract = abstract_elem.text if abstract_elem is not None else "N/A"
                    
                    authors = []
                    for author in article.findall('.//Author'):
                        lastname = author.find('LastName')
                        forename = author.find('ForeName')
                        if lastname is not None and forename is not None:
                            authors.append(f"{forename.text} {lastname.text}")
                    
                    pmid_elem = article.find('.//PMID')
                    pmid = pmid_elem.text if pmid_elem is not None else "N/A"
                    
                    articles.append({
                        'pmid': pmid,
                        'title': title,
                        'abstract': abstract[:500] + "..." if len(abstract) > 500 else abstract,
                        'authors': authors[:3],  # Prime 3 autori
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
                except Exception as e:
                    continue
            
            return articles
            
        except Exception as e:
            st.error(f"Errore nella ricerca PubMed: {str(e)}")
            return []
    
    def get_who_data(self, indicator: str = "MDG_0000000001") -> Dict:
        """
        Recupera dati sanitari globali dall'API WHO.
        
        Args:
            indicator: Codice indicatore WHO
            
        Returns:
            Dati dell'indicatore WHO
        """
        try:
            # WHO Global Health Observatory API (gratuita)
            url = f"https://ghoapi.azureedge.net/api/{indicator}"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'indicator': indicator,
                    'data': data.get('value', [])[:10],  # Prime 10 entries
                    'source': 'WHO Global Health Observatory'
                }
            else:
                return {'error': f"Status code: {response.status_code}"}
                
        except Exception as e:
            return {'error': str(e)}
    
    def get_fda_drug_info(self, drug_name: str) -> List[Dict]:
        """
        Ricerca informazioni sui farmaci tramite API FDA.
        
        Args:
            drug_name: Nome del farmaco
            
        Returns:
            Lista di informazioni sui farmaci
        """
        try:
            # FDA openFDA API (gratuita)
            url = "https://api.fda.gov/drug/label.json"
            params = {
                'search': f'openfda.generic_name:"{drug_name}"',
                'limit': 5
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for result in data.get('results', []):
                    openfda = result.get('openfda', {})
                    results.append({
                        'brand_name': openfda.get('brand_name', ['N/A'])[0],
                        'generic_name': openfda.get('generic_name', ['N/A'])[0],
                        'manufacturer_name': openfda.get('manufacturer_name', ['N/A'])[0],
                        'indications_and_usage': result.get('indications_and_usage', ['N/A'])[0][:200] + "...",
                        'warnings': result.get('warnings', ['N/A'])[0][:200] + "..." if result.get('warnings') else "N/A"
                    })
                
                return results
            else:
                return []
                
        except Exception as e:
            st.error(f"Errore nella ricerca FDA: {str(e)}")
            return []
    
    def get_disease_ontology(self, term: str) -> List[Dict]:
        """
        Ricerca termini nell'Ontologia delle Malattie (Disease Ontology).
        
        Args:
            term: Termine di ricerca
            
        Returns:
            Lista di termini trovati
        """
        try:
            # OLS (Ontology Lookup Service) API - gratuita
            url = "https://www.ebi.ac.uk/ols/api/search"
            params = {
                'q': term,
                'ontology': 'doid',  # Disease Ontology
                'rows': 10
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for doc in data.get('response', {}).get('docs', []):
                    results.append({
                        'id': doc.get('id', 'N/A'),
                        'label': doc.get('label', 'N/A'),
                        'description': doc.get('description', ['N/A'])[0] if doc.get('description') else 'N/A',
                        'synonyms': doc.get('synonym', [])[:3],  # Prime 3 sinonimi
                        'url': f"https://disease-ontology.org/?id={doc.get('short_form', '')}"
                    })
                
                return results
            else:
                return []
                
        except Exception as e:
            st.error(f"Errore nella ricerca Disease Ontology: {str(e)}")
            return []
    
    def get_clinical_trials(self, condition: str, max_results: int = 10) -> List[Dict]:
        """
        Ricerca studi clinici tramite ClinicalTrials.gov API.
        
        Args:
            condition: Condizione medica
            max_results: Numero massimo di risultati
            
        Returns:
            Lista di studi clinici
        """
        try:
            # ClinicalTrials.gov API (gratuita)
            url = "https://clinicaltrials.gov/api/query/study_fields"
            params = {
                'expr': condition,
                'fields': 'NCTId,BriefTitle,Condition,Phase,StudyType,StartDate,CompletionDate',
                'min_rnk': 1,
                'max_rnk': max_results,
                'fmt': 'json'
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                studies = []
                
                study_fields = data.get('StudyFieldsResponse', {}).get('StudyFields', [])
                
                for study in study_fields:
                    fields = study.get('Field', [])
                    if len(fields) >= 7:
                        studies.append({
                            'nct_id': fields[0],
                            'title': fields[1],
                            'condition': fields[2],
                            'phase': fields[3],
                            'study_type': fields[4],
                            'start_date': fields[5],
                            'completion_date': fields[6],
                            'url': f"https://clinicaltrials.gov/ct2/show/{fields[0]}"
                        })
                
                return studies
            else:
                return []
                
        except Exception as e:
            st.error(f"Errore nella ricerca Clinical Trials: {str(e)}")
            return []
    
    def get_uniprot_protein_info(self, protein_name: str) -> List[Dict]:
        """
        Ricerca informazioni sulle proteine tramite UniProt API.
        
        Args:
            protein_name: Nome della proteina
            
        Returns:
            Lista di informazioni sulle proteine
        """
        try:
            # UniProt API (gratuita)
            url = "https://rest.uniprot.org/uniprotkb/search"
            params = {
                'query': f'gene:{protein_name} AND reviewed:true',
                'format': 'json',
                'size': 5
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                proteins = []
                
                for result in data.get('results', []):
                    proteins.append({
                        'accession': result.get('primaryAccession', 'N/A'),
                        'protein_name': result.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'N/A'),
                        'gene_name': result.get('genes', [{}])[0].get('geneName', {}).get('value', 'N/A') if result.get('genes') else 'N/A',
                        'organism': result.get('organism', {}).get('scientificName', 'N/A'),
                        'function': result.get('comments', [{}])[0].get('texts', [{}])[0].get('value', 'N/A')[:200] + "..." if result.get('comments') else 'N/A',
                        'url': f"https://www.uniprot.org/uniprotkb/{result.get('primaryAccession', '')}"
                    })
                
                return proteins
            else:
                return []
                
        except Exception as e:
            st.error(f"Errore nella ricerca UniProt: {str(e)}")
            return []


def render_database_integrations_page():
    """Renderizza la pagina delle integrazioni database medici."""
    
    st.markdown('<h2 class="section-header">🌍 Integrazioni Database Medici Mondiali</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    **Nino Medical AI** si integra con i principali database medici mondiali per fornire accesso 
    a informazioni scientifiche aggiornate e dataset di ricerca di alta qualità.
    """)
    
    # Inizializza l'integratore
    integrator = MedicalDatabaseIntegrator()
    
    # Tabs per diverse integrazioni
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📚 PubMed", "🌍 WHO", "💊 FDA", 
        "🔬 Disease Ontology", "🏥 Clinical Trials", "🧬 UniProt"
    ])
    
    with tab1:
        st.subheader("📚 Ricerca Letteratura Scientifica - PubMed")
        st.markdown("Accesso alla più grande collezione di letteratura biomedica al mondo.")
        
        pubmed_query = st.text_input("Termine di ricerca PubMed:", value="artificial intelligence medical imaging")
        pubmed_results = st.slider("Numero risultati:", 1, 20, 10)
        
        if st.button("Cerca su PubMed", key="pubmed_search"):
            with st.spinner("Ricerca in corso su PubMed..."):
                articles = integrator.get_pubmed_articles(pubmed_query, pubmed_results)
                
                if articles:
                    for article in articles:
                        with st.expander(f"PMID: {article['pmid']} - {article['title'][:100]}..."):
                            st.write(f"**Autori:** {', '.join(article['authors'])}")
                            st.write(f"**Abstract:** {article['abstract']}")
                            st.markdown(f"[Visualizza su PubMed]({article['url']})")
                else:
                    st.warning("Nessun articolo trovato per questa ricerca.")
    
    with tab2:
        st.subheader("🌍 Dati Sanitari Globali - WHO")
        st.markdown("Statistiche sanitarie globali dall'Organizzazione Mondiale della Sanità.")
        
        who_indicators = {
            "MDG_0000000001": "Mortalità materna",
            "WHS4_100": "Aspettativa di vita",
            "WHS4_544": "Medici per 10.000 abitanti",
            "SA_0000001688": "Copertura vaccinazione DTP3"
        }
        
        selected_indicator = st.selectbox("Seleziona indicatore WHO:", 
                                        list(who_indicators.keys()),
                                        format_func=lambda x: who_indicators[x])
        
        if st.button("Ottieni dati WHO", key="who_data"):
            with st.spinner("Recupero dati WHO..."):
                who_data = integrator.get_who_data(selected_indicator)
                
                if 'error' not in who_data:
                    st.success(f"Dati recuperati per: {who_indicators[selected_indicator]}")
                    if who_data['data']:
                        df = pd.DataFrame(who_data['data'])
                        st.dataframe(df.head(10))
                else:
                    st.error(f"Errore: {who_data['error']}")
    
    with tab3:
        st.subheader("💊 Informazioni Farmaci - FDA")
        st.markdown("Database dei farmaci approvati dalla FDA americana.")
        
        drug_name = st.text_input("Nome farmaco:", value="aspirin")
        
        if st.button("Cerca farmaco FDA", key="fda_search"):
            with st.spinner("Ricerca nel database FDA..."):
                drugs = integrator.get_fda_drug_info(drug_name)
                
                if drugs:
                    for drug in drugs:
                        with st.expander(f"{drug['brand_name']} ({drug['generic_name']})"):
                            st.write(f"**Produttore:** {drug['manufacturer_name']}")
                            st.write(f"**Indicazioni:** {drug['indications_and_usage']}")
                            st.write(f"**Avvertenze:** {drug['warnings']}")
                else:
                    st.warning("Nessun farmaco trovato con questo nome.")
    
    with tab4:
        st.subheader("🔬 Ontologia delle Malattie")
        st.markdown("Classificazione standardizzata delle malattie e condizioni mediche.")
        
        disease_term = st.text_input("Termine malattia:", value="diabetes")
        
        if st.button("Cerca malattia", key="disease_search"):
            with st.spinner("Ricerca nell'ontologia delle malattie..."):
                diseases = integrator.get_disease_ontology(disease_term)
                
                if diseases:
                    for disease in diseases:
                        with st.expander(f"{disease['label']} ({disease['id']})"):
                            st.write(f"**Descrizione:** {disease['description']}")
                            if disease['synonyms']:
                                st.write(f"**Sinonimi:** {', '.join(disease['synonyms'])}")
                            st.markdown(f"[Maggiori info]({disease['url']})")
                else:
                    st.warning("Nessuna malattia trovata con questo termine.")
    
    with tab5:
        st.subheader("🏥 Studi Clinici - ClinicalTrials.gov")
        st.markdown("Database degli studi clinici registrati a livello mondiale.")
        
        condition = st.text_input("Condizione medica:", value="cancer")
        trials_count = st.slider("Numero studi:", 1, 20, 10)
        
        if st.button("Cerca studi clinici", key="trials_search"):
            with st.spinner("Ricerca studi clinici..."):
                trials = integrator.get_clinical_trials(condition, trials_count)
                
                if trials:
                    for trial in trials:
                        with st.expander(f"{trial['nct_id']} - {trial['title'][:100]}..."):
                            st.write(f"**Condizione:** {trial['condition']}")
                            st.write(f"**Fase:** {trial['phase']}")
                            st.write(f"**Tipo Studio:** {trial['study_type']}")
                            st.write(f"**Data Inizio:** {trial['start_date']}")
                            st.write(f"**Data Completamento:** {trial['completion_date']}")
                            st.markdown(f"[Visualizza studio]({trial['url']})")
                else:
                    st.warning("Nessuno studio clinico trovato per questa condizione.")
    
    with tab6:
        st.subheader("🧬 Informazioni Proteine - UniProt")
        st.markdown("Database delle sequenze proteiche e informazioni funzionali.")
        
        protein_name = st.text_input("Nome proteina/gene:", value="p53")
        
        if st.button("Cerca proteina", key="protein_search"):
            with st.spinner("Ricerca nel database UniProt..."):
                proteins = integrator.get_uniprot_protein_info(protein_name)
                
                if proteins:
                    for protein in proteins:
                        with st.expander(f"{protein['protein_name']} ({protein['accession']})"):
                            st.write(f"**Gene:** {protein['gene_name']}")
                            st.write(f"**Organismo:** {protein['organism']}")
                            st.write(f"**Funzione:** {protein['function']}")
                            st.markdown(f"[Visualizza su UniProt]({protein['url']})")
                else:
                    st.warning("Nessuna proteina trovata con questo nome.")
    
    # Sezione statistiche
    st.markdown('<h3 class="section-header">📊 Statistiche Integrazioni</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Database Integrati", "6")
    with col2:
        st.metric("API Pubbliche", "6")
    with col3:
        st.metric("Senza Autenticazione", "100%")
    with col4:
        st.metric("Aggiornamento", "Real-time")


if __name__ == "__main__":
    # Test delle integrazioni
    integrator = MedicalDatabaseIntegrator()
    
    print("Testing PubMed integration...")
    articles = integrator.get_pubmed_articles("AI medical imaging", 3)
    print(f"Found {len(articles)} articles")
    
    print("\nTesting WHO integration...")
    who_data = integrator.get_who_data()
    print(f"WHO data keys: {who_data.keys()}")
    
    print("\nTesting FDA integration...")
    drugs = integrator.get_fda_drug_info("aspirin")
    print(f"Found {len(drugs)} drugs")
