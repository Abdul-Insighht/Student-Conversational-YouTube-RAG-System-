"""
Configuration settings for AI Travel Assistant Planner
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-2.0-flash-exp'
    
    # App Configuration
    APP_NAME = os.getenv('APP_NAME', 'AI Travel Assistant Planner')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # UI Configuration
    PAGE_TITLE = "🌍 AI Travel Assistant Planner"
    PAGE_ICON = "✈️"
    LAYOUT = "wide"
    
    # Travel Configuration
    MIN_BUDGET = 100
    MAX_BUDGET = 50000
    MIN_DURATION = 1
    MAX_DURATION = 30
    
    # Supported Travel Styles
    TRAVEL_STYLES = ["Budget", "Mid-range", "Luxury"]
    
    # Food Preferences
    FOOD_PREFERENCES = [
        "No restrictions", "Vegetarian", "Halal", 
        "Vegan", "Gluten-free", "Kosher"
    ]
    
    # Travel Companions
    COMPANION_OPTIONS = ["Solo", "Couple", "Family (2-4)", "Group (5+)"]
    
    # Priority Options
    PRIORITY_OPTIONS = [
        "Historical Sites", "Museums", "Nature/Hiking", "Beaches", 
        "Shopping", "Nightlife", "Food Tours", "Adventure Sports", 
        "Photography", "Local Culture", "Architecture", "Wildlife"
    ]
    
    # Currency Symbols
    CURRENCY_SYMBOLS = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
        'CAD': 'C$', 'AUD': 'A$', 'INR': '₹'
    }
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        return True