#!/usr/bin/env python3
"""
Script per analizzare i visitatori che hanno mostrato interesse per l'upgrade Pro
===============================================================================

Estrae statistiche sui visitatori che hanno "aggiunto l'app al carrello",
ovvero che hanno mostrato interesse per le funzionalità Pro.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from engagement_tracker import EngagedVisitorsAnalyzer

def analyze_cart_visitors():
    """Analizza i visitatori interessati all'upgrade Pro."""
    print("=== NINO MEDICAL AI - ANALISI VISITATORI CARRELLO ===\n")
    
    # Inizializza l'analyzer
    analyzer = EngagedVisitorsAnalyzer()
    analysis = analyzer.analyze_engagement_patterns()
    
    # Estrai dati sui visitatori
    df = analyzer.mock_data
    
    # Definisci visitatori "carrello" - quelli che hanno visualizzato upgrade
    cart_visitors = df[df['upgrade_views'] > 0].copy()
    high_intent_visitors = df[(df['upgrade_views'] > 0) & (df['engagement_score'] >= 60)].copy()
    converted_visitors = df[df['converted_to_pro'] == 1].copy()
    
    print("📊 STATISTICHE GENERALI:")
    print(f"├─ Visitatori totali: {len(df):,}")
    print(f"├─ Visitatori engaged (≥50): {len(df[df['engagement_score'] >= 50]):,}")
    print(f"├─ Highly engaged (≥60): {len(df[df['engagement_score'] >= 60]):,}")
    print(f"└─ Super engaged (≥80): {len(df[df['engagement_score'] >= 80]):,}")
    
    print("\n🛒 VISITATORI CHE HANNO AGGIUNTO APP AL CARRELLO:")
    print(f"├─ Visitatori con interesse Pro: {len(cart_visitors):,}")
    print(f"├─ % sul totale: {len(cart_visitors)/len(df)*100:.1f}%")
    print(f"├─ Con alto engagement (≥60): {len(high_intent_visitors):,}")
    print(f"└─ Effettivamente convertiti: {len(converted_visitors):,}")
    
    print("\n💰 TASSI DI CONVERSIONE:")
    total_conversion_rate = len(converted_visitors) / len(df) * 100
    cart_conversion_rate = len(converted_visitors) / len(cart_visitors) * 100 if len(cart_visitors) > 0 else 0
    high_intent_conversion = len(converted_visitors) / len(high_intent_visitors) * 100 if len(high_intent_visitors) > 0 else 0
    
    print(f"├─ Conversione generale: {total_conversion_rate:.2f}%")
    print(f"├─ Conversione da interesse: {cart_conversion_rate:.1f}%")
    print(f"└─ Conversione high-intent: {high_intent_conversion:.1f}%")
    
    # Analisi dettagliata visitatori carrello
    print("\n📈 PROFILO VISITATORI INTERESSATI:")
    if len(cart_visitors) > 0:
        avg_engagement = cart_visitors['engagement_score'].mean()
        avg_session_duration = cart_visitors['session_duration'].mean()
        avg_pages = cart_visitors['pages_visited'].mean()
        avg_interactions = cart_visitors['total_interactions'].mean()
        
        print(f"├─ Score engagement medio: {avg_engagement:.1f}/100")
        print(f"├─ Durata sessione media: {avg_session_duration:.1f} min")
        print(f"├─ Pagine visitate: {avg_pages:.1f}")
        print(f"└─ Interazioni medie: {avg_interactions:.1f}")
    
    # Segmentazione per tipo utente
    print("\n👥 SEGMENTAZIONE VISITATORI CARRELLO:")
    cart_by_user_type = cart_visitors['user_type'].value_counts()
    for user_type, count in cart_by_user_type.items():
        percentage = count / len(cart_visitors) * 100
        print(f"├─ {user_type}: {count} visitatori ({percentage:.1f}%)")
    
    # Canali di traffico più efficaci
    print("\n🌐 CANALI TRAFFICO PIÙ EFFICACI:")
    cart_by_traffic = cart_visitors['traffic_source'].value_counts()
    for source, count in cart_by_traffic.items():
        percentage = count / len(cart_visitors) * 100
        print(f"├─ {source}: {count} visitatori ({percentage:.1f}%)")
    
    # Analisi temporale (ultimi 30 giorni)
    print("\n📅 TREND TEMPORALE (ultimi 7 giorni):")
    recent_cart = cart_visitors[cart_visitors['visit_date'] >= datetime.now() - timedelta(days=7)]
    print(f"├─ Visitatori carrello recenti: {len(recent_cart)}")
    print(f"├─ Conversioni recenti: {len(recent_cart[recent_cart['converted_to_pro'] == 1])}")
    
    # Insight e raccomandazioni
    print("\n💡 INSIGHTS E RACCOMANDAZIONI:")
    
    # Identifica il segmento più promettente
    cart_conversion_by_type = cart_visitors.groupby('user_type')['converted_to_pro'].mean()
    best_segment = cart_conversion_by_type.idxmax()
    best_rate = cart_conversion_by_type.max()
    
    print(f"├─ Segmento più convertente: {best_segment} ({best_rate:.1%})")
    
    # Analisi device
    cart_by_device = cart_visitors['device'].value_counts()
    main_device = cart_by_device.index[0]
    print(f"├─ Device principale: {main_device}")
    
    # Engagement level dei visitatori carrello
    engagement_dist = cart_visitors['engagement_level'].value_counts()
    print(f"├─ Livello engagement più comune: {engagement_dist.index[0]}")
    
    print("\n🎯 AZIONI CONSIGLIATE:")
    print(f"├─ Targetizza campagne su {best_segment} (conversione più alta)")
    print(f"├─ Ottimizza esperienza per {main_device}")
    print(f"├─ Focus su traffico {cart_by_traffic.index[0]} (volume maggiore)")
    print(f"└─ Implementa retargeting per {len(cart_visitors) - len(converted_visitors)} prospect caldi")
    
    # Calcola valore potenziale
    print("\n💰 POTENZIALE REVENUE:")
    avg_pro_price = 49.99  # Prezzo ipotetico Pro
    potential_revenue = (len(cart_visitors) - len(converted_visitors)) * avg_pro_price
    if cart_conversion_rate > 0:
        expected_conversions = (len(cart_visitors) - len(converted_visitors)) * (cart_conversion_rate / 100)
        expected_revenue = expected_conversions * avg_pro_price
        print(f"├─ Prospect nel carrello: {len(cart_visitors) - len(converted_visitors)}")
        print(f"├─ Revenue potenziale: €{potential_revenue:,.2f}")
        print(f"├─ Conversioni attese: {expected_conversions:.1f}")
        print(f"└─ Revenue prevista: €{expected_revenue:,.2f}")
    
    return {
        'total_visitors': len(df),
        'cart_visitors': len(cart_visitors),
        'converted_visitors': len(converted_visitors),
        'cart_conversion_rate': cart_conversion_rate,
        'potential_revenue': potential_revenue if 'potential_revenue' in locals() else 0,
        'best_segment': best_segment if 'best_segment' in locals() else 'N/A',
        'main_traffic_source': cart_by_traffic.index[0] if len(cart_by_traffic) > 0 else 'N/A'
    }

def show_detailed_cart_analysis():
    """Mostra analisi dettagliata con tabelle."""
    analyzer = EngagedVisitorsAnalyzer()
    df = analyzer.mock_data
    cart_visitors = df[df['upgrade_views'] > 0].copy()
    
    print("\n📋 DETTAGLIO VISITATORI CARRELLO:")
    print("="*80)
    
    # Top 10 visitatori per engagement
    top_cart = cart_visitors.nlargest(10, 'engagement_score')
    
    print("🏆 TOP 10 VISITATORI PIÙ ENGAGED:")
    for i, (_, visitor) in enumerate(top_cart.iterrows(), 1):
        status = "✅ CONVERTITO" if visitor['converted_to_pro'] else "🔄 IN ATTESA"
        print(f"{i:2d}. Score: {visitor['engagement_score']:5.1f} | "
              f"Durata: {visitor['session_duration']:4.1f}m | "
              f"Tipo: {visitor['user_type']:12s} | "
              f"Device: {visitor['device']:7s} | {status}")
    
    # Analisi per fasce di engagement
    print(f"\n📊 DISTRIBUZIONE PER FASCE DI ENGAGEMENT:")
    engagement_ranges = [
        (80, 100, "🌟 Super Engaged"),
        (60, 79, "🔥 Highly Engaged"), 
        (40, 59, "👍 Medium Engaged"),
        (0, 39, "😐 Low Engaged")
    ]
    
    for min_score, max_score, label in engagement_ranges:
        count = len(cart_visitors[(cart_visitors['engagement_score'] >= min_score) & 
                                  (cart_visitors['engagement_score'] <= max_score)])
        if count > 0:
            converted = len(cart_visitors[(cart_visitors['engagement_score'] >= min_score) & 
                                        (cart_visitors['engagement_score'] <= max_score) &
                                        (cart_visitors['converted_to_pro'] == 1)])
            conv_rate = converted / count * 100 if count > 0 else 0
            print(f"{label}: {count:3d} visitatori | Conversioni: {converted:2d} ({conv_rate:4.1f}%)")

if __name__ == "__main__":
    # Analisi principale
    stats = analyze_cart_visitors()
    
    # Analisi dettagliata
    show_detailed_cart_analysis()
    
    print(f"\n{'='*80}")
    print("🎉 Analisi completata! I dati mostrano il comportamento dei visitatori")
    print("   interessati alle funzionalità Pro di Nino Medical AI.")
    print(f"{'='*80}")
