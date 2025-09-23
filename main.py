import streamlit as st
import google.generativeai as genai
import json
import datetime
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="🌍 AI Travel Assistant Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .budget-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .day-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .attraction-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .expense-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .stSelectbox > div > div {
        background-color: #667eea;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background-color: #667eea;
        border-radius: 10px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class TravelPreferences:
    budget: float
    destination: str
    duration: int
    travel_style: str
    food_preference: str
    priorities: List[str]
    companions: str
    flexible_budget: bool
    start_date: str

class AITravelAssistant:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def generate_itinerary(self, preferences: TravelPreferences) -> Dict:
        """Generate comprehensive travel itinerary using Gemini AI"""
        prompt = f"""
        Create a detailed travel itinerary for:
        
        🎯 TRIP DETAILS:
        - Destination: {preferences.destination}
        - Budget: ${preferences.budget} ({'flexible' if preferences.flexible_budget else 'fixed'})
        - Duration: {preferences.duration} days
        - Travel Style: {preferences.travel_style}
        - Food Preference: {preferences.food_preference}
        - Priorities: {', '.join(preferences.priorities)}
        - Travel Group: {preferences.companions}
        - Start Date: {preferences.start_date}
        
        Please provide a comprehensive JSON response with the following structure:
        
        {{
            "summary": {{
                "total_estimated_cost": float,
                "cost_breakdown": {{
                    "flights": float,
                    "accommodation": float,
                    "food": float,
                    "attractions": float,
                    "local_transport": float,
                    "miscellaneous": float
                }},
                "best_time_to_visit": "string",
                "currency": "string",
                "weather_forecast": "string"
            }},
            "daily_itinerary": [
                {{
                    "day": int,
                    "date": "YYYY-MM-DD",
                    "theme": "string",
                    "activities": [
                        {{
                            "time": "HH:MM",
                            "activity": "string",
                            "location": "string",
                            "cost": float,
                            "duration": "string",
                            "tips": "string",
                            "priority": "high/medium/low"
                        }}
                    ],
                    "meals": [
                        {{
                            "meal": "breakfast/lunch/dinner",
                            "restaurant": "string",
                            "cuisine": "string",
                            "cost": float,
                            "location": "string",
                            "rating": float
                        }}
                    ],
                    "accommodation": {{
                        "name": "string",
                        "type": "hotel/hostel/airbnb",
                        "location": "string",
                        "cost_per_night": float,
                        "rating": float,
                        "amenities": ["string"]
                    }},
                    "transport": [
                        {{
                            "from": "string",
                            "to": "string",
                            "method": "string",
                            "cost": float,
                            "duration": "string"
                        }}
                    ],
                    "daily_total": float
                }}
            ],
            "recommendations": {{
                "must_visit": ["string"],
                "hidden_gems": ["string"],
                "local_tips": ["string"],
                "money_saving_tips": ["string"],
                "safety_tips": ["string"]
            }},
            "alternatives": {{
                "budget_friendly": "suggestions if budget needs to be reduced",
                "luxury_upgrades": "suggestions if budget can be increased",
                "weather_backup": ["indoor alternatives"]
            }}
        }}
        
        Make sure all costs are realistic and sum up correctly. Include specific restaurant names, attractions, and locations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response text to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            return json.loads(response_text)
        except Exception as e:
            st.error(f"Error generating itinerary: {str(e)}")
            return self._get_fallback_itinerary(preferences)
    
    def _get_fallback_itinerary(self, preferences: TravelPreferences) -> Dict:
        """Provide a basic fallback itinerary if API fails"""
        return {
            "summary": {
                "total_estimated_cost": preferences.budget * 0.9,
                "cost_breakdown": {
                    "flights": preferences.budget * 0.3,
                    "accommodation": preferences.budget * 0.25,
                    "food": preferences.budget * 0.2,
                    "attractions": preferences.budget * 0.15,
                    "local_transport": preferences.budget * 0.05,
                    "miscellaneous": preferences.budget * 0.05
                },
                "best_time_to_visit": "Year-round",
                "currency": "USD",
                "weather_forecast": "Please check local weather"
            },
            "daily_itinerary": [
                {
                    "day": 1,
                    "date": preferences.start_date,
                    "theme": "Arrival & Exploration",
                    "activities": [
                        {
                            "time": "10:00",
                            "activity": "City Walking Tour",
                            "location": "Downtown",
                            "cost": 25.0,
                            "duration": "3 hours",
                            "tips": "Wear comfortable shoes",
                            "priority": "high"
                        }
                    ],
                    "meals": [
                        {
                            "meal": "lunch",
                            "restaurant": "Local Favorite",
                            "cuisine": "Local",
                            "cost": 15.0,
                            "location": "City Center",
                            "rating": 4.5
                        }
                    ],
                    "accommodation": {
                        "name": "Recommended Hotel",
                        "type": "hotel",
                        "location": "City Center",
                        "cost_per_night": preferences.budget * 0.25 / preferences.duration,
                        "rating": 4.0,
                        "amenities": ["WiFi", "Breakfast"]
                    },
                    "transport": [
                        {
                            "from": "Airport",
                            "to": "Hotel",
                            "method": "Taxi",
                            "cost": 20.0,
                            "duration": "30 minutes"
                        }
                    ],
                    "daily_total": preferences.budget / preferences.duration
                }
            ],
            "recommendations": {
                "must_visit": ["Main attractions in " + preferences.destination],
                "hidden_gems": ["Local markets", "Scenic viewpoints"],
                "local_tips": ["Learn basic local phrases", "Try street food"],
                "money_saving_tips": ["Use public transport", "Eat at local places"],
                "safety_tips": ["Keep copies of documents", "Stay aware of surroundings"]
            },
            "alternatives": {
                "budget_friendly": "Consider hostels and street food",
                "luxury_upgrades": "Premium hotels and fine dining",
                "weather_backup": ["Museums", "Shopping centers", "Indoor entertainment"]
            }
        }

def initialize_session_state():
    """Initialize session state variables"""
    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = None
    if 'preferences' not in st.session_state:
        st.session_state.preferences = None
    if 'ai_assistant' not in st.session_state:
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            st.session_state.ai_assistant = AITravelAssistant(api_key)
        else:
            st.error("Please set GEMINI_API_KEY in your .env file")
            st.stop()

def render_header():
    """Render beautiful header"""
    st.markdown("""
    <div class="main-header">
        <h1>🌍 AI Travel Assistant Planner</h1>
        <p>Your Personal Travel Expert - Optimizing Every Journey Within Your Budget</p>
    </div>
    """, unsafe_allow_html=True)

def render_preferences_form():
    """Render the travel preferences form"""
    st.markdown("## 🎯 Tell Us About Your Dream Trip")
    
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.number_input("💰 Total Budget ($)", min_value=100, value=2000, step=100)
        flexible_budget = st.checkbox("🔄 Flexible Budget?", value=False)
        
        destination = st.text_input("📍 Destination", placeholder="e.g., Paris, France")
        
        duration = st.slider("📅 Trip Duration (days)", min_value=1, max_value=30, value=7)
        
        start_date = st.date_input("📅 Start Date", datetime.date.today() + datetime.timedelta(days=30))
    
    with col2:
        travel_style = st.selectbox("🏨 Travel Style", 
            ["Budget", "Mid-range", "Luxury"])
        
        food_preference = st.selectbox("🍽 Food Preferences", 
            ["No restrictions", "Vegetarian", "Halal", "Vegan", "Gluten-free"])
        
        companions = st.selectbox("👥 Travel Companions", 
            ["Solo", "Couple", "Family (2-4)", "Group (5+)"])
        
        priorities = st.multiselect("🎯 What interests you most?", 
            ["Historical Sites", "Museums", "Nature/Hiking", "Beaches", "Shopping", 
             "Nightlife", "Food Tours", "Adventure Sports", "Photography", "Local Culture"])
    
    if st.button("🚀 Plan My Trip!", type="primary"):
        if destination and priorities:
            preferences = TravelPreferences(
                budget=budget,
                destination=destination,
                duration=duration,
                travel_style=travel_style.lower(),
                food_preference=food_preference.lower(),
                priorities=priorities,
                companions=companions.lower(),
                flexible_budget=flexible_budget,
                start_date=start_date.strftime("%Y-%m-%d")
            )
            
            with st.spinner("🤖 AI is crafting your perfect itinerary..."):
                itinerary = st.session_state.ai_assistant.generate_itinerary(preferences)
                st.session_state.itinerary = itinerary
                st.session_state.preferences = preferences
                st.rerun()
        else:
            st.warning("Please fill in destination and select at least one priority!")

def render_budget_overview(itinerary: Dict):
    """Render budget breakdown with beautiful visualization"""
    st.markdown("## 💰 Budget Breakdown")
    
    cost_breakdown = itinerary['summary']['cost_breakdown']
    total_cost = itinerary['summary']['total_estimated_cost']
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Create pie chart
        labels = list(cost_breakdown.keys())
        values = list(cost_breakdown.values())
        
        fig = px.pie(values=values, names=labels, title="Cost Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="budget-card">
            <h3>💵 Total Cost</h3>
            <h2>${total_cost:,.2f}</h2>
            <p>Currency: {itinerary['summary']['currency']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="budget-card">
            <h3>📊 Daily Average</h3>
            <h2>${total_cost/st.session_state.preferences.duration:,.2f}</h2>
            <p>Per day spending</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("### 📋 Detailed Breakdown")
    breakdown_df = pd.DataFrame([
        {"Category": k.replace('_', ' ').title(), 
         "Amount": f"${v:,.2f}", 
         "Percentage": f"{(v/total_cost)*100:.1f}%"} 
        for k, v in cost_breakdown.items()
    ])
    st.dataframe(breakdown_df, use_container_width=True)

def render_daily_itinerary(itinerary: Dict):
    """Render day-by-day itinerary"""
    st.markdown("## 📅 Daily Itinerary")
    
    for day_plan in itinerary['daily_itinerary']:
        with st.expander(f"🗓 Day {day_plan['day']} - {day_plan['theme']} ({day_plan['date']})", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Activities")
                for activity in day_plan['activities']:
                    priority_emoji = "🔥" if activity['priority'] == 'high' else "⭐" if activity['priority'] == 'medium' else "💡"
                    st.markdown(f"""
                    <div class="attraction-card">
                        <h4>{priority_emoji} {activity['time']} - {activity['activity']}</h4>
                        <p>📍 <strong>{activity['location']}</strong> | 💰 ${activity['cost']} | ⏱ {activity['duration']}</p>
                        <p>💡 {activity['tips']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("### 🍽 Meals")
                for meal in day_plan['meals']:
                    st.markdown(f"""
                    <div class="expense-card">
                        <h4>🍽 {meal['meal'].title()} at {meal['restaurant']}</h4>
                        <p>🍜 {meal['cuisine']} | 💰 ${meal['cost']} | ⭐ {meal['rating']}/5</p>
                        <p>📍 {meal['location']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 🏨 Accommodation")
                acc = day_plan['accommodation']
                st.markdown(f"""
                **{acc['name']}** ({acc['type'].title()})
                - 📍 {acc['location']}
                - 💰 ${acc['cost_per_night']}/night
                - ⭐ {acc['rating']}/5
                - 🏷 {', '.join(acc['amenities'])}
                """)
                
                st.markdown("### 🚗 Transport")
                for transport in day_plan['transport']:
                    st.markdown(f"""
                    **{transport['from']} → {transport['to']}**
                    - 🚗 {transport['method']}
                    - 💰 ${transport['cost']}
                    - ⏱ {transport['duration']}
                    """)
                
                st.markdown(f"""
                <div class="day-card">
                    <h4>💰 Daily Total: ${day_plan['daily_total']:.2f}</h4>
                </div>
                """, unsafe_allow_html=True)

def render_recommendations(itinerary: Dict):
    """Render recommendations and tips"""
    st.markdown("## 🎯 Recommendations & Tips")
    
    recs = itinerary['recommendations']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Must-Visit Places")
        for item in recs['must_visit']:
            st.markdown(f"• {item}")
        
        st.markdown("### 💎 Hidden Gems")
        for item in recs['hidden_gems']:
            st.markdown(f"• {item}")
        
        st.markdown("### 💰 Money-Saving Tips")
        for item in recs['money_saving_tips']:
            st.markdown(f"• {item}")
    
    with col2:
        st.markdown("### 🌍 Local Tips")
        for item in recs['local_tips']:
            st.markdown(f"• {item}")
        
        st.markdown("### 🛡 Safety Tips")
        for item in recs['safety_tips']:
            st.markdown(f"• {item}")

def render_alternatives(itinerary: Dict):
    """Render budget alternatives"""
    st.markdown("## 🔄 Budget Alternatives")
    
    alts = itinerary['alternatives']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💸 Budget-Friendly Options")
        st.info(alts['budget_friendly'])
    
    with col2:
        st.markdown("### 💎 Luxury Upgrades")
        st.success(alts['luxury_upgrades'])
    
    with col3:
        st.markdown("### 🌧 Weather Backup Plans")
        for item in alts['weather_backup']:
            st.markdown(f"• {item}")

def main():
    """Main application function"""
    initialize_session_state()
    render_header()
    
    # Sidebar for adjustments
    with st.sidebar:
        st.markdown("## 🎛 Dynamic Adjustments")
        
        if st.session_state.itinerary:
            st.markdown("### 💰 Budget Modifier")
            budget_multiplier = st.slider("Budget Adjustment", 0.5, 2.0, 1.0, 0.1)
            
            if budget_multiplier != 1.0:
                st.info(f"Budget adjusted by {budget_multiplier:.1f}x")
            
            st.markdown("### 🌤 Weather Considerations")
            weather_backup = st.checkbox("Show weather alternatives")
            
            if st.button("🔄 Regenerate Plan"):
                with st.spinner("Updating your itinerary..."):
                    # Update preferences with new budget
                    updated_preferences = st.session_state.preferences
                    updated_preferences.budget *= budget_multiplier
                    
                    # Regenerate itinerary
                    new_itinerary = st.session_state.ai_assistant.generate_itinerary(updated_preferences)
                    st.session_state.itinerary = new_itinerary
                    st.rerun()
        else:
            st.info("Complete the form to see adjustment options")
    
    # Main content
    if st.session_state.itinerary is None:
        render_preferences_form()
    else:
        # Display itinerary
        render_budget_overview(st.session_state.itinerary)
        render_daily_itinerary(st.session_state.itinerary)
        render_recommendations(st.session_state.itinerary)
        render_alternatives(st.session_state.itinerary)
        
        # Option to plan another trip
        st.markdown("---")
        if st.button("🗺 Plan Another Trip"):
            st.session_state.itinerary = None
            st.session_state.preferences = None
            st.rerun()

if __name__ == "__main__":
    main()