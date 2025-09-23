"""
UI Components for AI Travel Assistant Planner
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
from utils import format_currency, get_priority_emoji, get_meal_emoji, get_transport_emoji

def render_custom_css():
    """Render custom CSS styles"""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .budget-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
            transition: transform 0.3s ease;
        }
        
        .budget-card:hover {
            transform: translateY(-5px);
        }
        
        .day-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
        }
        
        .attraction-card {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            color: white;
            box-shadow: 0 5px 15px rgba(67, 233, 123, 0.3);
            transition: transform 0.2s ease;
        }
        
        .attraction-card:hover {
            transform: scale(1.02);
        }
        
        .expense-card {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            color: white;
            box-shadow: 0 5px 15px rgba(250, 112, 154, 0.3);
        }
        
        .stats-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            text-align: center;
            color: #333;
            box-shadow: 0 5px 15px rgba(168, 237, 234, 0.3);
        }
        
        .recommendation-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            color: #333;
            box-shadow: 0 5px 15px rgba(255, 236, 210, 0.3);
        }
        
        .alert-success {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .alert-warning {
            background: linear-gradient(135deg, #f7b733 0%, #fc4a1a 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .stSelectbox > div > div {
            background-color: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        
        .stTextInput > div > div > input {
            background-color: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 25px;
            border: none;
            padding: 0.75rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .sidebar-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 1rem 0;
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render beautiful animated header"""
    st.markdown("""
    <div class="main-header">
        <h1>🌍 AI Travel Assistant Planner</h1>
        <p>Your Personal Travel Expert - Optimizing Every Journey Within Your Budget</p>
        <small>✨ Powered by Advanced AI • 🎯 Personalized Recommendations • 💰 Budget Optimization</small>
    </div>
    """, unsafe_allow_html=True)

def render_budget_overview(itinerary: Dict, preferences):
    """Render comprehensive budget overview with visualizations"""
    st.markdown("## 💰 Budget Analysis & Breakdown")
    
    cost_breakdown = itinerary['summary']['cost_breakdown']
    total_cost = itinerary['summary']['total_estimated_cost']
    planned_budget = preferences.budget
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #667eea;">💵 Total Cost</h3>
            <h2>{format_currency(total_cost)}</h2>
            <small>{itinerary['summary']['currency']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        daily_avg = total_cost / preferences.duration
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #f093fb;">📊 Daily Average</h3>
            <h2>{format_currency(daily_avg)}</h2>
            <small>Per day</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        budget_diff = planned_budget - total_cost
        color = "#43e97b" if budget_diff >= 0 else "#fc4a1a"
        status = "Under Budget" if budget_diff >= 0 else "Over Budget"
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: {color};">🎯 Budget Status</h3>
            <h2 style="color: {color};">{format_currency(abs(budget_diff))}</h2>
            <small>{status}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        savings_rate = (budget_diff / planned_budget * 100) if planned_budget > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #4facfe;">📈 Efficiency</h3>
            <h2 style="color: #4facfe;">{savings_rate:.1f}%</h2>
            <small>Budget efficiency</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Visual breakdown
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Enhanced pie chart
        labels = [k.replace('_', ' ').title() for k in cost_breakdown.keys()]
        values = list(cost_breakdown.values())
        
        fig = px.pie(
            values=values, 
            names=labels, 
            title="💸 Expense Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
        )
        fig.update_layout(
            showlegend=True,
            height=400,
            title_font_size=16,
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget comparison bar chart
        comparison_df = pd.DataFrame({
            'Category': ['Planned Budget', 'Estimated Cost'],
            'Amount': [planned_budget, total_cost],
            'Color': ['#667eea', '#f093fb' if total_cost <= planned_budget else '#fc4a1a']
        })
        
        fig = px.bar(
            comparison_df, 
            x='Category', 
            y='Amount',
            title='💰 Budget vs Actual',
            color='Color',
            color_discrete_map={'#667eea': '#667eea', '#f093fb': '#f093fb', '#fc4a1a': '#fc4a1a'}
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown table
    st.markdown("### 📋 Detailed Cost Breakdown")
    breakdown_data = []
    for category, amount in cost_breakdown.items():
        percentage = (amount / total_cost * 100) if total_cost > 0 else 0
        breakdown_data.append({
            "Category": category.replace('_', ' ').title(),
            "Amount": format_currency(amount),
            "Percentage": f"{percentage:.1f}%",
            "Daily Average": format_currency(amount / preferences.duration)
        })
    
    breakdown_df = pd.DataFrame(breakdown_data)
    st.dataframe(breakdown_df, use_container_width=True)

def render_daily_itinerary(itinerary: Dict):
    """Render enhanced daily itinerary with better visuals"""
    st.markdown("## 📅 Your Complete Itinerary")
    
    # Summary timeline
    total_days = len(itinerary['daily_itinerary'])
    st.markdown(f"### 🗓 {total_days}-Day Adventure Overview")
    
    # Create day selector
    day_tabs = st.tabs([f"Day {day['day']}" for day in itinerary['daily_itinerary']])
    
    for i, (tab, day_plan) in enumerate(zip(day_tabs, itinerary['daily_itinerary'])):
        with tab:
            # Day header
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"## 🎯 {day_plan['theme']}")
                st.markdown(f"📅 **{day_plan['date']}**")
            
            with col2:
                st.markdown(f"""
                <div class="stats-card">
                    <h4>💰 Daily Budget</h4>
                    <h3>{format_currency(day_plan['daily_total'])}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                activity_count = len(day_plan['activities'])
                meal_count = len(day_plan['meals'])
                st.markdown(f"""
                <div class="stats-card">
                    <h4>📊 Activities</h4>
                    <h3>{activity_count + meal_count}</h3>
                    <small>{activity_count} tours • {meal_count} meals</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Main content
            left_col, right_col = st.columns([2, 1])
            
            with left_col:
                # Activities timeline
                st.markdown("### 🎯 Activities & Attractions")
                
                for activity in day_plan['activities']:
                    priority_emoji = get_priority_emoji(activity['priority'])
                    st.markdown(f"""
                    <div class="attraction-card">
                        <h4>{priority_emoji} {activity['time']} - {activity['activity']}</h4>
                        <p>📍 <strong>{activity['location']}</strong></p>
                        <p>💰 {format_currency(activity['cost'])} | ⏱ {activity['duration']}</p>
                        <p>💡 <em>{activity['tips']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Meals
                st.markdown("### 🍽 Dining Experiences")
                
                for meal in day_plan['meals']:
                    meal_emoji = get_meal_emoji(meal['meal'])
                    stars = "⭐" * int(meal['rating'])
                    st.markdown(f"""
                    <div class="expense-card">
                        <h4>{meal_emoji} {meal['meal'].title()} - {meal['restaurant']}</h4>
                        <p>🍜 <strong>{meal['cuisine']} Cuisine</strong></p>
                        <p>📍 {meal['location']} | 💰 {format_currency(meal['cost'])}</p>
                        <p>{stars} ({meal['rating']}/5.0)</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with right_col:
                # Accommodation info
                st.markdown("### 🏨 Accommodation")
                acc = day_plan['accommodation']
                stars = "⭐" * int(acc['rating'])
                
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>{acc['name']}</h4>
                    <p><strong>{acc['type'].title()}</strong></p>
                    <p>📍 {acc['location']}</p>
                    <p>💰 {format_currency(acc['cost_per_night'])}/night</p>
                    <p>{stars} ({acc['rating']}/5.0)</p>
                    <p><strong>Amenities:</strong><br>{', '.join(acc['amenities'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Transportation
                st.markdown("### 🚗 Transportation")
                
                for transport in day_plan['transport']:
                    transport_emoji = get_transport_emoji(transport['method'])
                    st.markdown(f"""
                    <div class="stats-card">
                        <h4>{transport_emoji} {transport['method'].title()}</h4>
                        <p><strong>{transport['from']}</strong><br>↓<br><strong>{transport['to']}</strong></p>
                        <p>💰 {format_currency(transport['cost'])}</p>
                        <p>⏱ {transport['duration']}</p>
                    </div>
                    """, unsafe_allow_html=True)

def render_recommendations(itinerary: Dict):
    """Render enhanced recommendations with better organization"""
    st.markdown("## 🎯 Expert Recommendations & Insider Tips")
    
    recs = itinerary['recommendations']
    
    # Create recommendation tabs
    rec_tabs = st.tabs(["🏆 Must-Visit", "💎 Hidden Gems", "💰 Money Tips", "🌍 Local Insights", "🛡 Safety"])
    
    with rec_tabs[0]:
        st.markdown("### 🏆 Must-Visit Attractions")
        for i, item in enumerate(recs['must_visit'], 1):
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>#{i} {item}</h4>
            </div>
            """, unsafe_allow_html=True)
    
    with rec_tabs[1]:
        st.markdown("### 💎 Hidden Gems & Local Favorites")
        for item in recs['hidden_gems']:
            st.markdown(f"""
            <div class="recommendation-card">
                <p>💎 {item}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with rec_tabs[2]:
        st.markdown("### 💰 Money-Saving Strategies")
        for tip in recs['money_saving_tips']:
            st.markdown(f"""
            <div class="alert-success">
                <p>💡 {tip}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with rec_tabs[3]:
        st.markdown("### 🌍 Local Culture & Tips")
        for tip in recs['local_tips']:
            st.markdown(f"""
            <div class="recommendation-card">
                <p>🌍 {tip}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with rec_tabs[4]:
        st.markdown("### 🛡 Safety & Health Tips")
        for tip in recs['safety_tips']:
            st.markdown(f"""
            <div class="alert-warning">
                <p>🛡 {tip}</p>
            </div>
            """, unsafe_allow_html=True)

def render_alternatives_and_adjustments(itinerary: Dict):
    """Render budget alternatives and dynamic adjustments"""
    st.markdown("## 🔄 Smart Alternatives & Adjustments")
    
    alts = itinerary['alternatives']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💸 Budget-Friendly Options")
        st.markdown(f"""
        <div class="alert-success">
            <h4>🎯 Cost-Saving Strategy</h4>
            <p>{alts['budget_friendly']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💎 Luxury Upgrades")
        st.markdown(f"""
        <div class="recommendation-card">
            <h4>✨ Premium Experience</h4>
            <p>{alts['luxury_upgrades']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🌧 Weather Backup Plans")
        st.markdown("#### Indoor Alternatives:")
        for item in alts['weather_backup']:
            st.markdown(f"""
            <div class="stats-card">
                <p>🏢 {item}</p>
            </div>
            """, unsafe_allow_html=True)

def render_export_options(itinerary: Dict):
    """Render export and sharing options"""
    st.markdown("## 📤 Export & Share Your Itinerary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as PDF"):
            st.info("PDF export functionality would be implemented here")
    
    with col2:
        if st.button("📊 Download CSV"):
            from utils import export_itinerary_to_csv
            csv_data = export_itinerary_to_csv(itinerary)
            st.download_button(
                label="📥 Download",
                data=csv_data.to_csv(index=False),
                file_name="travel_itinerary.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📱 Share Itinerary"):
            st.info("Sharing functionality would be implemented here")