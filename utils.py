"""
Utility functions for AI Travel Assistant Planner
"""

import json
import datetime
from typing import Dict, List, Optional, Tuple
import streamlit as st
import pandas as pd
from config import Config

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency with appropriate symbol"""
    symbol = Config.CURRENCY_SYMBOLS.get(currency, '$')
    return f"{symbol}{amount:,.2f}"

def calculate_daily_budget(total_budget: float, duration: int) -> float:
    """Calculate daily budget from total budget and duration"""
    return total_budget / duration if duration > 0 else 0

def validate_travel_preferences(preferences: Dict) -> Tuple[bool, List[str]]:
    """Validate travel preferences and return errors if any"""
    errors = []
    
    if not preferences.get('destination'):
        errors.append("Destination is required")
    
    if preferences.get('budget', 0) < Config.MIN_BUDGET:
        errors.append(f"Budget must be at least ${Config.MIN_BUDGET}")
    
    if preferences.get('duration', 0) < Config.MIN_DURATION:
        errors.append(f"Duration must be at least {Config.MIN_DURATION} day(s)")
    
    if not preferences.get('priorities'):
        errors.append("Please select at least one priority")
    
    return len(errors) == 0, errors

def parse_gemini_response(response_text: str) -> Optional[Dict]:
    """Parse Gemini AI response and extract JSON"""
    try:
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove code block markers if present
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:-3]
        elif cleaned_text.startswith('```'):
            cleaned_text = cleaned_text[3:-3]
        
        # Parse JSON
        return json.loads(cleaned_text)
    
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse AI response: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error parsing response: {str(e)}")
        return None

def generate_date_range(start_date: str, duration: int) -> List[str]:
    """Generate list of dates for the trip"""
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    return [(start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(duration)]

def calculate_budget_variance(planned: float, actual: float) -> Dict[str, float]:
    """Calculate budget variance metrics"""
    variance = actual - planned
    variance_percent = (variance / planned * 100) if planned > 0 else 0
    
    return {
        'variance': variance,
        'variance_percent': variance_percent,
        'is_over_budget': variance > 0,
        'savings': abs(variance) if variance < 0 else 0
    }

def get_priority_emoji(priority: str) -> str:
    """Get emoji for activity priority"""
    priority_map = {
        'high': '🔥',
        'medium': '⭐',
        'low': '💡'
    }
    return priority_map.get(priority.lower(), '💡')

def get_meal_emoji(meal_type: str) -> str:
    """Get emoji for meal types"""
    meal_map = {
        'breakfast': '🍳',
        'lunch': '🍽',
        'dinner': '🍷',
        'snack': '🥨'
    }
    return meal_map.get(meal_type.lower(), '🍽')

def get_transport_emoji(transport_method: str) -> str:
    """Get emoji for transport methods"""
    transport_map = {
        'flight': '✈️',
        'train': '🚂',
        'bus': '🚌',
        'taxi': '🚕',
        'uber': '🚗',
        'walking': '🚶',
        'metro': '🚇',
        'boat': '⛵',
        'bicycle': '🚲'
    }
    return transport_map.get(transport_method.lower(), '🚗')

def create_expense_dataframe(itinerary: Dict) -> pd.DataFrame:
    """Create a detailed expense breakdown DataFrame"""
    expenses = []
    
    for day in itinerary.get('daily_itinerary', []):
        day_num = day.get('day', 0)
        date = day.get('date', '')
        
        # Activities
        for activity in day.get('activities', []):
            expenses.append({
                'Day': day_num,
                'Date': date,
                'Category': 'Activity',
                'Item': activity.get('activity', ''),
                'Cost': activity.get('cost', 0),
                'Location': activity.get('location', ''),
                'Priority': activity.get('priority', 'medium')
            })
        
        # Meals
        for meal in day.get('meals', []):
            expenses.append({
                'Day': day_num,
                'Date': date,
                'Category': 'Food',
                'Item': f"{meal.get('meal', '').title()} at {meal.get('restaurant', '')}",
                'Cost': meal.get('cost', 0),
                'Location': meal.get('location', ''),
                'Priority': 'high'
            })
        
        # Accommodation
        acc = day.get('accommodation', {})
        if acc:
            expenses.append({
                'Day': day_num,
                'Date': date,
                'Category': 'Accommodation',
                'Item': acc.get('name', ''),
                'Cost': acc.get('cost_per_night', 0),
                'Location': acc.get('location', ''),
                'Priority': 'high'
            })
        
        # Transport
        for transport in day.get('transport', []):
            expenses.append({
                'Day': day_num,
                'Date': date,
                'Category': 'Transport',
                'Item': f"{transport.get('from', '')} to {transport.get('to', '')}",
                'Cost': transport.get('cost', 0),
                'Location': transport.get('method', ''),
                'Priority': 'medium'
            })
    
    return pd.DataFrame(expenses)

def generate_packing_list(destination: str, duration: int, travel_style: str, priorities: List[str]) -> Dict[str, List[str]]:
    """Generate a smart packing list based on trip details"""
    
    base_items = {
        'Documents': [
            'Passport/ID', 'Travel insurance', 'Flight tickets', 
            'Hotel confirmations', 'Driver\'s license', 'Emergency contacts'
        ],
        'Electronics': [
            'Phone charger', 'Power adapter', 'Camera', 
            'Portable battery', 'Headphones'
        ],
        'Clothing': [
            'Underwear', 'Socks', 'Comfortable shoes', 
            'Casual clothes', 'Sleepwear'
        ],
        'Health & Hygiene': [
            'Toothbrush', 'Toothpaste', 'Medications', 
            'First aid kit', 'Sunscreen', 'Hand sanitizer'
        ]
    }
    
    # Add items based on travel style
    if travel_style.lower() == 'luxury':
        base_items['Clothing'].extend(['Formal wear', 'Dress shoes', 'Nice accessories'])
    elif travel_style.lower() == 'budget':
        base_items['General'].append('Reusable water bottle')
        base_items['General'].append('Travel towel')
    
    # Add items based on priorities
    if 'Beaches' in priorities:
        base_items['Beach'] = ['Swimwear', 'Beach towel', 'Flip-flops', 'Waterproof bag']
    
    if 'Nature/Hiking' in priorities:
        base_items['Outdoor'] = ['Hiking boots', 'Backpack', 'Weather jacket', 'Hat']
    
    if 'Photography' in priorities:
        base_items['Photography'] = ['Camera batteries', 'Memory cards', 'Tripod', 'Lens cleaning kit']
    
    # Adjust quantities based on duration
    if duration > 7:
        base_items['Health & Hygiene'].append('Laundry detergent')
    
    return base_items

def get_weather_recommendations(destination: str, month: int) -> Dict[str, str]:
    """Get basic weather recommendations (simplified version)"""
    # This is a simplified version - in production, you'd integrate with weather APIs
    
    general_advice = {
        'clothing': 'Check weather forecast before packing',
        'activities': 'Have indoor backup plans ready',
        'health': 'Pack according to season and climate'
    }
    
    # Basic seasonal advice for Northern Hemisphere
    if month in [12, 1, 2]:  # Winter
        general_advice['clothing'] = 'Pack warm clothes, layers, waterproof jacket'
        general_advice['activities'] = 'Consider indoor attractions, museums'
    elif month in [6, 7, 8]:  # Summer
        general_advice['clothing'] = 'Light clothes, sun protection, comfortable shoes'
        general_advice['activities'] = 'Early morning or evening outdoor activities'
    
    return general_advice

def export_itinerary_to_csv(itinerary: Dict) -> pd.DataFrame:
    """Export itinerary to CSV format"""
    csv_data = []
    
    for day in itinerary.get('daily_itinerary', []):
        base_row = {
            'Day': day.get('day'),
            'Date': day.get('date'),
            'Theme': day.get('theme'),
            'Daily_Total': day.get('daily_total', 0)
        }
        
        # Activities
        for i, activity in enumerate(day.get('activities', [])):
            row = base_row.copy()
            row.update({
                'Type': 'Activity',
                'Time': activity.get('time'),
                'Item': activity.get('activity'),
                'Location': activity.get('location'),
                'Cost': activity.get('cost', 0),
                'Duration': activity.get('duration'),
                'Priority': activity.get('priority'),
                'Tips': activity.get('tips')
            })
            csv_data.append(row)
        
        # Meals
        for meal in day.get('meals', []):
            row = base_row.copy()
            row.update({
                'Type': 'Meal',
                'Item': f"{meal.get('meal')} at {meal.get('restaurant')}",
                'Location': meal.get('location'),
                'Cost': meal.get('cost', 0),
                'Cuisine': meal.get('cuisine'),
                'Rating': meal.get('rating')
            })
            csv_data.append(row)
    
    return pd.DataFrame(csv_data)