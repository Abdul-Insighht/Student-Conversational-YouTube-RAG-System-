#!/usr/bin/env python3
"""
AI Travel Assistant Planner - Application Launcher
This script helps launch the Streamlit application with proper configuration
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if all required files and dependencies exist"""
    print("🔍 Checking requirements...")
    
    # Check required files
    required_files = ['main.py', 'config.py', 'utils.py', 'components.py', '.env']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if virtual environment exists
    venv_path = Path('venv')
    if not venv_path.exists():
        print("⚠️  Virtual environment not found. Run setup.sh first.")
        return False
    
    # Check .env file
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY=' not in content or 'your-api-key-here' in content:
                print("⚠️  Please update your GEMINI_API_KEY in .env file")
                return False
    
    print("✅ All requirements satisfied")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def launch_app():
    """Launch the Streamlit application"""
    print("🚀 Launching AI Travel Assistant Planner...")
    
    try:
        # Set environment variables for better Streamlit experience
        env = os.environ.copy()
        env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        env['STREAMLIT_SERVER_HEADLESS'] = 'true'
        
        # Launch Streamlit
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'main.py',
            '--server.port=8501',
            '--server.address=localhost',
            '--server.headless=true',
            '--browser.gatherUsageStats=false'
        ], env=env)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        print("🌐 Opening browser...")
        webbrowser.open('http://localhost:8501')
        
        print("\n✅ Application launched successfully!")
        print("🌍 AI Travel Assistant Planner is now running at: http://localhost:8501")
        print("\n📋 Instructions:")
        print("1. The app should open automatically in your browser")
        print("2. If not, manually navigate to http://localhost:8501")
        print("3. Press Ctrl+C in this terminal to stop the application")
        print("\nHappy Travel Planning! ✈️🗺️")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down application...")
            process.terminate()
            print("👋 Goodbye!")
            
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🌍 AI Travel Assistant Planner Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('main.py').exists():
        print("❌ Please run this script from the project directory")
        return
    
    # Check requirements
    if not check_requirements():
        print("\n💡 Please run the setup script first:")
        print("   chmod +x setup.sh && ./setup.sh")
        return
    
    # Check if we need to install dependencies
    try:
        import streamlit
        import google.generativeai
        import plotly
        print("✅ Dependencies are already installed")
    except ImportError:
        print("📦 Installing missing dependencies...")
        if not install_dependencies():
            return
    
    # Launch the application
    launch_app()

if __name__ == "__main__":
    main()