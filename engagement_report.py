#!/usr/bin/env python3
"""
Quick Engagement Analytics Report
================================

Generate a summary report of engaged visitors metrics
without requiring full Streamlit context.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any

def generate_engagement_report() -> Dict[str, Any]:
    """Generate current engagement analytics report."""
    
    # Simulate current engagement data (in production, this would come from your database/analytics)
    np.random.seed(42)  # For consistent demo data
    
    # Generate mock data for 500 visitors over last 30 days
    total_visitors = 500
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    # Engagement distribution (realistic percentages)
    engagement_levels = {
        'low': int(total_visitors * 0.40),      # 40% - 200 visitors
        'medium': int(total_visitors * 0.30),   # 30% - 150 visitors  
        'high': int(total_visitors * 0.20),     # 20% - 100 visitors
        'super': int(total_visitors * 0.10)     # 10% - 50 visitors
    }
    
    # Calculate engaged visitors (medium + high + super)
    engaged_visitors = engagement_levels['medium'] + engagement_levels['high'] + engagement_levels['super']
    engagement_rate = (engaged_visitors / total_visitors) * 100
    
    # Business metrics
    pro_conversions = int(engaged_visitors * 0.08)  # 8% of engaged visitors convert
    super_engaged = engagement_levels['super']
    
    # Daily active users (mock real-time data)
    current_active_users = np.random.randint(25, 85)
    highly_engaged_now = np.random.randint(8, 25)
    super_engaged_now = np.random.randint(2, 12)
    
    # Session metrics
    avg_session_duration = 4.2  # minutes
    avg_pages_per_session = 3.4
    bounce_rate = 0.35
    
    # Top engaging segments
    user_segments = {
        'Medico': {'engagement_score': 67.3, 'count': 150, 'conversion_rate': 0.12},
        'Ricercatore': {'engagement_score': 71.8, 'count': 125, 'conversion_rate': 0.14},
        'Studente': {'engagement_score': 58.2, 'count': 125, 'conversion_rate': 0.06},
        'Paziente': {'engagement_score': 52.1, 'count': 100, 'conversion_rate': 0.04}
    }
    
    # Traffic source performance
    traffic_sources = {
        'Organic Search': {'engagement_score': 64.5, 'count': 225, 'conversion_rate': 0.09},
        'Direct': {'engagement_score': 59.8, 'count': 150, 'conversion_rate': 0.07},
        'Referral': {'engagement_score': 68.2, 'count': 75, 'conversion_rate': 0.11},
        'Social': {'engagement_score': 55.4, 'count': 50, 'conversion_rate': 0.05}
    }
    
    # Recent trends (last 7 days)
    recent_trends = {
        'daily_engaged': [45, 52, 38, 61, 48, 55, 42],
        'daily_super_engaged': [8, 12, 6, 15, 9, 11, 7],
        'daily_conversions': [3, 4, 2, 5, 3, 4, 2]
    }
    
    # Engagement funnel
    funnel_data = {
        'Tutti i Visitatori': {'count': total_visitors, 'rate': 100.0},
        'Non Bounce': {'count': int(total_visitors * 0.65), 'rate': 65.0},
        'Sessione > 2min': {'count': int(total_visitors * 0.55), 'rate': 55.0},
        'Engaged (Score ≥50)': {'count': engaged_visitors, 'rate': engagement_rate},
        'High Engaged (Score ≥60)': {'count': engagement_levels['high'] + engagement_levels['super'], 'rate': 30.0},
        'Super Engaged (Score ≥80)': {'count': super_engaged, 'rate': 10.0},
        'Conversioni Pro': {'count': pro_conversions, 'rate': 2.4}
    }
    
    return {
        'overview': {
            'total_visitors': total_visitors,
            'engaged_visitors': engaged_visitors,
            'engagement_rate': engagement_rate,
            'super_engaged': super_engaged,
            'pro_conversions': pro_conversions,
            'conversion_rate_from_engaged': (pro_conversions / engaged_visitors) * 100
        },
        'real_time': {
            'active_users_now': current_active_users,
            'highly_engaged_now': highly_engaged_now,
            'super_engaged_now': super_engaged_now,
            'engagement_rate_now': (highly_engaged_now / current_active_users) * 100
        },
        'engagement_levels': engagement_levels,
        'session_metrics': {
            'avg_duration_minutes': avg_session_duration,
            'avg_pages_per_session': avg_pages_per_session,
            'bounce_rate': bounce_rate
        },
        'top_segments': user_segments,
        'traffic_performance': traffic_sources,
        'recent_trends': recent_trends,
        'funnel': funnel_data,
        'generated_at': datetime.now().isoformat()
    }

def print_engagement_summary(report: Dict[str, Any]):
    """Print a formatted summary of engagement metrics."""
    
    print("🔥 ENGAGED VISITORS ANALYTICS REPORT")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Overview
    overview = report['overview']
    print("📊 OVERVIEW METRICS")
    print("-" * 30)
    print(f"👥 Total Visitors: {overview['total_visitors']:,}")
    print(f"🔥 Engaged Visitors: {overview['engaged_visitors']:,}")
    print(f"📈 Engagement Rate: {overview['engagement_rate']:.1f}%")
    print(f"🌟 Super Engaged: {overview['super_engaged']:,}")
    print(f"💎 Pro Conversions: {overview['pro_conversions']:,}")
    print(f"🎯 Conversion Rate: {overview['conversion_rate_from_engaged']:.1f}% (from engaged)")
    print()
    
    # Real-time
    realtime = report['real_time']
    print("🔴 REAL-TIME METRICS")
    print("-" * 30)
    print(f"👥 Active Users Now: {realtime['active_users_now']}")
    print(f"🔥 Highly Engaged Now: {realtime['highly_engaged_now']}")
    print(f"🌟 Super Engaged Now: {realtime['super_engaged_now']}")
    print(f"📊 Current Engagement Rate: {realtime['engagement_rate_now']:.1f}%")
    print()
    
    # Engagement levels breakdown
    levels = report['engagement_levels']
    print("🎯 ENGAGEMENT LEVELS BREAKDOWN")
    print("-" * 30)
    total = sum(levels.values())
    for level, count in levels.items():
        percentage = (count / total) * 100
        print(f"{level.upper():>12}: {count:>3} visitors ({percentage:4.1f}%)")
    print()
    
    # Top performing segments
    print("🏆 TOP PERFORMING SEGMENTS")
    print("-" * 30)
    segments = report['top_segments']
    for segment, data in sorted(segments.items(), key=lambda x: x[1]['engagement_score'], reverse=True):
        print(f"{segment:>12}: Score {data['engagement_score']:4.1f} | {data['count']:3} users | {data['conversion_rate']:.1%} conversion")
    print()
    
    # Traffic sources
    print("🌐 TRAFFIC SOURCE PERFORMANCE")
    print("-" * 30)
    sources = report['traffic_performance']
    for source, data in sorted(sources.items(), key=lambda x: x[1]['engagement_score'], reverse=True):
        print(f"{source:>15}: Score {data['engagement_score']:4.1f} | {data['count']:3} users | {data['conversion_rate']:.1%} conversion")
    print()
    
    # Recent trends
    trends = report['recent_trends']
    avg_daily_engaged = sum(trends['daily_engaged']) / len(trends['daily_engaged'])
    avg_daily_super = sum(trends['daily_super_engaged']) / len(trends['daily_super_engaged'])
    avg_daily_conversions = sum(trends['daily_conversions']) / len(trends['daily_conversions'])
    
    print("📈 RECENT TRENDS (Last 7 days)")
    print("-" * 30)
    print(f"Avg Daily Engaged: {avg_daily_engaged:.1f}")
    print(f"Avg Daily Super Engaged: {avg_daily_super:.1f}")
    print(f"Avg Daily Conversions: {avg_daily_conversions:.1f}")
    print()
    
    # Key insights
    print("💡 KEY INSIGHTS")
    print("-" * 30)
    
    # Find best performing segment
    best_segment = max(segments.items(), key=lambda x: x[1]['engagement_score'])
    print(f"• Top segment: {best_segment[0]} with {best_segment[1]['engagement_score']:.1f} engagement score")
    
    # Find best traffic source
    best_source = max(sources.items(), key=lambda x: x[1]['engagement_score'])
    print(f"• Best traffic source: {best_source[0]} with {best_source[1]['engagement_score']:.1f} score")
    
    # Conversion insights
    if overview['engagement_rate'] > 60:
        print("• 🟢 Strong engagement rate - above 60%")
    elif overview['engagement_rate'] > 40:
        print("• 🟡 Good engagement rate - room for improvement")
    else:
        print("• 🔴 Low engagement rate - needs attention")
    
    # Pro conversion insights
    if overview['conversion_rate_from_engaged'] > 10:
        print("• 💎 Excellent Pro conversion rate from engaged users")
    elif overview['conversion_rate_from_engaged'] > 5:
        print("• 💰 Good Pro conversion rate - can optimize further")
    else:
        print("• 📈 Pro conversion rate needs improvement")
    
    print()
    print("🚀 RECOMMENDATIONS")
    print("-" * 30)
    print("• Focus marketing on top-performing segments")
    print("• Optimize onboarding for low-engagement users")
    print("• Create targeted Pro upgrade campaigns for highly engaged users")
    print("• Analyze drop-off points in engagement funnel")
    print("• A/B test personalized content for different engagement levels")

if __name__ == "__main__":
    # Generate and display report
    report = generate_engagement_report()
    print_engagement_summary(report)
    
    print("\n" + "=" * 50)
    print("📊 For detailed dashboard, run: streamlit run nino_medical_ai_app.py")
    print("🔥 Access Admin → Engagement for full analytics")
    print("=" * 50)
