#!/usr/bin/env python3
"""
Advanced Engagement Tracking for Nino Medical AI
================================================

Sistema avanzato per tracciare e analizzare engaged visitors:
- Definizione metriche di engagement
- Tracking comportamenti utente
- Classificazione automatica visitatori
- Analytics engagement specifiche

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum

class EngagementLevel(Enum):
    """Livelli di engagement dei visitatori."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SUPER = "super"

@dataclass
class UserEngagementMetrics:
    """Metriche di engagement per un utente."""
    user_id: str
    session_id: str
    visit_start: datetime
    last_activity: datetime
    
    # Metriche temporali
    session_duration: float = 0.0  # in minuti
    time_on_page: Dict[str, float] = None  # tempo per pagina
    
    # Metriche di navigazione
    pages_visited: int = 0
    unique_pages: int = 0
    page_sequence: List[str] = None
    
    # Metriche di interazione
    clicks_count: int = 0
    form_submissions: int = 0
    searches_performed: int = 0
    ai_analyses_run: int = 0
    exports_made: int = 0
    
    # Metriche business
    upgrade_views: int = 0
    demo_interactions: int = 0
    pro_features_accessed: int = 0
    
    # Metriche di qualità
    bounce: bool = False
    scroll_depth_avg: float = 0.0
    return_visitor: bool = False
    
    # Calcolato
    engagement_score: float = 0.0
    engagement_level: EngagementLevel = EngagementLevel.LOW
    
    def __post_init__(self):
        if self.time_on_page is None:
            self.time_on_page = {}
        if self.page_sequence is None:
            self.page_sequence = []

class EngagementTracker:
    """Sistema principale per il tracking dell'engagement."""
    
    def __init__(self):
        self.session_key = "engagement_metrics"
        self.init_session_metrics()
    
    def init_session_metrics(self):
        """Inizializza le metriche di engagement per la sessione corrente."""
        if self.session_key not in st.session_state:
            user_id = st.session_state.get('user_id', 'anonymous')
            session_id = st.session_state.get('session_id', str(int(time.time())))
            
            st.session_state[self.session_key] = UserEngagementMetrics(
                user_id=user_id,
                session_id=session_id,
                visit_start=datetime.now(),
                last_activity=datetime.now()
            )
    
    def update_page_visit(self, page_name: str, time_spent: Optional[float] = None):
        """Aggiorna metriche per visita pagina."""
        metrics = st.session_state[self.session_key]
        metrics.last_activity = datetime.now()
        
        # Aggiorna contatori
        metrics.pages_visited += 1
        if page_name not in metrics.page_sequence:
            metrics.unique_pages += 1
        
        metrics.page_sequence.append(page_name)
        
        # Tempo sulla pagina
        if time_spent:
            metrics.time_on_page[page_name] = metrics.time_on_page.get(page_name, 0) + time_spent
        
        # Calcola durata sessione
        metrics.session_duration = (metrics.last_activity - metrics.visit_start).total_seconds() / 60
        
        # Aggiorna bounce
        metrics.bounce = metrics.pages_visited == 1 and metrics.session_duration < 0.5
        
        self._calculate_engagement_score()
    
    def track_interaction(self, interaction_type: str, details: Dict[str, Any] = None):
        """Traccia interazioni specifiche dell'utente."""
        metrics = st.session_state[self.session_key]
        metrics.last_activity = datetime.now()
        details = details or {}
        
        # Aggiorna contatori specifici
        if interaction_type == "click":
            metrics.clicks_count += 1
        elif interaction_type == "form_submit":
            metrics.form_submissions += 1
        elif interaction_type == "search":
            metrics.searches_performed += 1
        elif interaction_type == "ai_analysis":
            metrics.ai_analyses_run += 1
        elif interaction_type == "export":
            metrics.exports_made += 1
        elif interaction_type == "upgrade_view":
            metrics.upgrade_views += 1
        elif interaction_type == "demo_interaction":
            metrics.demo_interactions += 1
        elif interaction_type == "pro_feature":
            metrics.pro_features_accessed += 1
        
        # Tracking scroll depth se fornito
        if "scroll_depth" in details:
            current_avg = metrics.scroll_depth_avg
            new_depth = details["scroll_depth"]
            total_pages = metrics.pages_visited
            metrics.scroll_depth_avg = (current_avg * (total_pages - 1) + new_depth) / total_pages
        
        self._calculate_engagement_score()
        
        # Invia a Google Analytics se disponibile
        self._send_engagement_event(interaction_type, details)
    
    def _calculate_engagement_score(self):
        """Calcola punteggio di engagement basato su multiple metriche."""
        metrics = st.session_state[self.session_key]
        score = 0.0
        
        # Fattori temporali (peso 25%)
        if metrics.session_duration > 5:  # 5+ minuti
            score += 25
        elif metrics.session_duration > 2:  # 2-5 minuti
            score += 15
        elif metrics.session_duration > 1:  # 1-2 minuti
            score += 10
        
        # Navigazione (peso 20%)
        if metrics.unique_pages >= 5:
            score += 20
        elif metrics.unique_pages >= 3:
            score += 15
        elif metrics.unique_pages >= 2:
            score += 10
        
        # Interazioni (peso 30%)
        interaction_score = min(30, (
            metrics.clicks_count * 1 +
            metrics.form_submissions * 8 +
            metrics.searches_performed * 5 +
            metrics.ai_analyses_run * 10 +
            metrics.exports_made * 12 +
            metrics.demo_interactions * 3
        ))
        score += interaction_score
        
        # Business engagement (peso 20%)
        business_score = min(20, (
            metrics.upgrade_views * 8 +
            metrics.pro_features_accessed * 6
        ))
        score += business_score
        
        # Qualità engagement (peso 5%)
        if not metrics.bounce:
            score += 3
        if metrics.scroll_depth_avg > 0.7:  # 70%+ scroll
            score += 2
        
        metrics.engagement_score = min(100.0, score)
        
        # Determina livello di engagement
        if metrics.engagement_score >= 80:
            metrics.engagement_level = EngagementLevel.SUPER
        elif metrics.engagement_score >= 60:
            metrics.engagement_level = EngagementLevel.HIGH
        elif metrics.engagement_score >= 35:
            metrics.engagement_level = EngagementLevel.MEDIUM
        else:
            metrics.engagement_level = EngagementLevel.LOW
    
    def _send_engagement_event(self, interaction_type: str, details: Dict[str, Any]):
        """Invia evento di engagement a Google Analytics."""
        try:
            from google_analytics import get_analytics
            analytics = get_analytics()
            
            metrics = st.session_state[self.session_key]
            
            # Prepara parametri evento
            event_params = {
                'interaction_type': interaction_type,
                'engagement_score': metrics.engagement_score,
                'engagement_level': metrics.engagement_level.value,
                'session_duration': metrics.session_duration,
                'pages_visited': metrics.pages_visited,
                'unique_pages': metrics.unique_pages,
                **details
            }
            
            analytics.track_event('user_engagement', event_params)
            
        except ImportError:
            pass  # Google Analytics non disponibile
    
    def get_current_metrics(self) -> UserEngagementMetrics:
        """Ottiene le metriche correnti dell'utente."""
        return st.session_state[self.session_key]
    
    def is_engaged_visitor(self, threshold: float = 50.0) -> bool:
        """Determina se l'utente corrente è un visitatore engaged."""
        metrics = st.session_state[self.session_key]
        return metrics.engagement_score >= threshold
    
    def get_engagement_insights(self) -> Dict[str, Any]:
        """Genera insights sull'engagement dell'utente corrente."""
        metrics = st.session_state[self.session_key]
        
        insights = {
            'level': metrics.engagement_level.value,
            'score': metrics.engagement_score,
            'session_quality': 'high' if metrics.session_duration > 3 and not metrics.bounce else 'standard',
            'interaction_patterns': [],
            'recommendations': []
        }
        
        # Analizza patterns di interazione
        if metrics.searches_performed > 2:
            insights['interaction_patterns'].append('active_researcher')
        if metrics.ai_analyses_run > 1:
            insights['interaction_patterns'].append('ai_power_user')
        if metrics.upgrade_views > 0:
            insights['interaction_patterns'].append('potential_customer')
        if metrics.exports_made > 0:
            insights['interaction_patterns'].append('data_exporter')
        
        # Genera raccomandazioni
        if metrics.engagement_level == EngagementLevel.HIGH and metrics.upgrade_views == 0:
            insights['recommendations'].append('show_pro_features')
        if metrics.searches_performed > 3 and metrics.pro_features_accessed == 0:
            insights['recommendations'].append('highlight_advanced_search')
        if metrics.session_duration > 5 and metrics.form_submissions == 0:
            insights['recommendations'].append('request_feedback')
        
        return insights

class EngagedVisitorsAnalyzer:
    """Analizzatore per insights sui visitatori engaged."""
    
    def __init__(self):
        self.mock_data = self._generate_engaged_visitors_data()
    
    def _generate_engaged_visitors_data(self) -> pd.DataFrame:
        """Genera dati mock per analisi visitatori engaged."""
        np.random.seed(42)
        n_visitors = 500
        
        # Genera visitatori con diversi livelli di engagement
        visitors = []
        
        for i in range(n_visitors):
            engagement_level = np.random.choice([
                EngagementLevel.LOW, EngagementLevel.MEDIUM, 
                EngagementLevel.HIGH, EngagementLevel.SUPER
            ], p=[0.4, 0.3, 0.2, 0.1])
            
            # Genera metriche basate sul livello
            if engagement_level == EngagementLevel.SUPER:
                session_duration = np.random.uniform(8, 25)
                pages_visited = np.random.randint(8, 20)
                interactions = np.random.randint(15, 50)
                score = np.random.uniform(80, 100)
            elif engagement_level == EngagementLevel.HIGH:
                session_duration = np.random.uniform(4, 12)
                pages_visited = np.random.randint(4, 12)
                interactions = np.random.randint(8, 25)
                score = np.random.uniform(60, 85)
            elif engagement_level == EngagementLevel.MEDIUM:
                session_duration = np.random.uniform(1.5, 6)
                pages_visited = np.random.randint(2, 8)
                interactions = np.random.randint(3, 15)
                score = np.random.uniform(35, 65)
            else:  # LOW
                session_duration = np.random.uniform(0.2, 3)
                pages_visited = np.random.randint(1, 4)
                interactions = np.random.randint(0, 8)
                score = np.random.uniform(0, 40)
            
            visitor = {
                'visitor_id': f'visitor_{i+1}',
                'engagement_level': engagement_level.value,
                'engagement_score': score,
                'session_duration': session_duration,
                'pages_visited': pages_visited,
                'unique_pages': min(pages_visited, np.random.randint(1, pages_visited+1)),
                'total_interactions': interactions,
                'searches_performed': max(0, int(interactions * np.random.uniform(0.1, 0.4))),
                'ai_analyses': max(0, int(interactions * np.random.uniform(0.05, 0.2))),
                'exports_made': max(0, int(interactions * np.random.uniform(0.02, 0.1))),
                'upgrade_views': 1 if np.random.random() > 0.7 else 0,
                'converted_to_pro': 1 if engagement_level in [EngagementLevel.HIGH, EngagementLevel.SUPER] and np.random.random() > 0.85 else 0,
                'user_type': np.random.choice(['Medico', 'Ricercatore', 'Studente', 'Paziente'], p=[0.3, 0.25, 0.25, 0.2]),
                'device': np.random.choice(['Desktop', 'Mobile', 'Tablet'], p=[0.65, 0.3, 0.05]),
                'traffic_source': np.random.choice(['Organic', 'Direct', 'Referral', 'Social'], p=[0.45, 0.3, 0.15, 0.1]),
                'visit_date': datetime.now() - timedelta(days=np.random.randint(0, 30))
            }
            
            visitors.append(visitor)
        
        return pd.DataFrame(visitors)
    
    def analyze_engagement_patterns(self) -> Dict[str, Any]:
        """Analizza i pattern di engagement dei visitatori."""
        df = self.mock_data
        
        analysis = {
            'overview': {
                'total_visitors': len(df),
                'engaged_visitors': len(df[df['engagement_score'] >= 50]),
                'super_engaged': len(df[df['engagement_level'] == 'super']),
                'engagement_rate': len(df[df['engagement_score'] >= 50]) / len(df) * 100
            },
            'by_level': df['engagement_level'].value_counts().to_dict(),
            'avg_metrics_by_level': df.groupby('engagement_level').agg({
                'engagement_score': 'mean',
                'session_duration': 'mean',
                'pages_visited': 'mean',
                'total_interactions': 'mean',
                'converted_to_pro': 'mean'
            }).to_dict(),
            'conversion_by_engagement': df.groupby('engagement_level')['converted_to_pro'].mean().to_dict(),
            'top_engaging_segments': self._identify_top_segments(df)
        }
        
        return analysis
    
    def _identify_top_segments(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identifica i segmenti di utenti più engaged."""
        segments = []
        
        # Segmento per tipo utente
        user_type_engagement = df.groupby('user_type').agg({
            'engagement_score': 'mean',
            'converted_to_pro': 'mean',
            'visitor_id': 'count'
        }).rename(columns={'visitor_id': 'count'})
        
        for user_type in user_type_engagement.index:
            row = user_type_engagement.loc[user_type]
            segments.append({
                'segment_type': 'user_type',
                'segment_name': user_type,
                'avg_engagement': row['engagement_score'],
                'conversion_rate': row['converted_to_pro'],
                'visitor_count': row['count']
            })
        
        # Segmento per sorgente traffico
        traffic_engagement = df.groupby('traffic_source').agg({
            'engagement_score': 'mean',
            'converted_to_pro': 'mean',
            'visitor_id': 'count'
        }).rename(columns={'visitor_id': 'count'})
        
        for source in traffic_engagement.index:
            row = traffic_engagement.loc[source]
            segments.append({
                'segment_type': 'traffic_source',
                'segment_name': source,
                'avg_engagement': row['engagement_score'],
                'conversion_rate': row['converted_to_pro'],
                'visitor_count': row['count']
            })
        
        return sorted(segments, key=lambda x: x['avg_engagement'], reverse=True)
    
    def get_engagement_funnel(self) -> pd.DataFrame:
        """Crea funnel di engagement per analisi."""
        df = self.mock_data
        
        funnel_stages = [
            {'stage': 'Tutti i Visitatori', 'visitors': len(df), 'rate': 100.0},
            {'stage': 'Bounce < 50%', 'visitors': len(df[df['pages_visited'] > 1]), 'rate': 0},
            {'stage': 'Sessione > 2min', 'visitors': len(df[df['session_duration'] > 2]), 'rate': 0},
            {'stage': 'Engaged (Score ≥50)', 'visitors': len(df[df['engagement_score'] >= 50]), 'rate': 0},
            {'stage': 'High Engaged (Score ≥60)', 'visitors': len(df[df['engagement_score'] >= 60]), 'rate': 0},
            {'stage': 'Super Engaged (Score ≥80)', 'visitors': len(df[df['engagement_score'] >= 80]), 'rate': 0},
            {'stage': 'Conversioni Pro', 'visitors': len(df[df['converted_to_pro'] == 1]), 'rate': 0}
        ]
        
        # Calcola percentuali
        total = funnel_stages[0]['visitors']
        for stage in funnel_stages:
            stage['rate'] = (stage['visitors'] / total) * 100
        
        return pd.DataFrame(funnel_stages)

# Istanza globale per il tracking
_engagement_tracker = None

def get_engagement_tracker() -> EngagementTracker:
    """Ottiene l'istanza globale del tracker."""
    global _engagement_tracker
    if _engagement_tracker is None:
        _engagement_tracker = EngagementTracker()
    return _engagement_tracker

# Decorators per tracking automatico
def track_page_engagement(page_name: str):
    """Decorator per tracciare automaticamente l'engagement della pagina."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracker = get_engagement_tracker()
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            time_spent = (end_time - start_time) / 60  # in minuti
            tracker.update_page_visit(page_name, time_spent)
            
            return result
        return wrapper
    return decorator

def track_interaction(interaction_type: str, details: Dict[str, Any] = None):
    """Decorator per tracciare interazioni."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracker = get_engagement_tracker()
            result = func(*args, **kwargs)
            tracker.track_interaction(interaction_type, details or {})
            return result
        return wrapper
    return decorator

# Funzioni di utilità
def is_current_user_engaged(threshold: float = 50.0) -> bool:
    """Controlla se l'utente corrente è engaged."""
    tracker = get_engagement_tracker()
    return tracker.is_engaged_visitor(threshold)

def get_current_engagement_level() -> EngagementLevel:
    """Ottiene il livello di engagement corrente."""
    tracker = get_engagement_tracker()
    metrics = tracker.get_current_metrics()
    return metrics.engagement_level

def show_engagement_badge():
    """Mostra badge di engagement nell'interfaccia."""
    if is_current_user_engaged():
        level = get_current_engagement_level()
        tracker = get_engagement_tracker()
        score = tracker.get_current_metrics().engagement_score
        
        if level == EngagementLevel.SUPER:
            st.sidebar.success(f"🌟 Super Engaged User! (Score: {score:.0f})")
        elif level == EngagementLevel.HIGH:
            st.sidebar.info(f"🔥 Highly Engaged! (Score: {score:.0f})")
        elif level == EngagementLevel.MEDIUM:
            st.sidebar.info(f"👍 Good Engagement (Score: {score:.0f})")

if __name__ == "__main__":
    # Test del modulo
    print("Testing Engagement Tracker...")
    
    tracker = EngagementTracker()
    
    # Simula alcune interazioni
    tracker.update_page_visit("dashboard")
    tracker.track_interaction("search", {"query": "cancer research"})
    tracker.track_interaction("ai_analysis")
    tracker.update_page_visit("predictive")
    
    metrics = tracker.get_current_metrics()
    print(f"Engagement Score: {metrics.engagement_score}")
    print(f"Engagement Level: {metrics.engagement_level.value}")
    print(f"Is Engaged: {tracker.is_engaged_visitor()}")
    
    insights = tracker.get_engagement_insights()
    print(f"Insights: {insights}")
