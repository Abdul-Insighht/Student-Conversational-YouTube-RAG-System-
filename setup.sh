#!/bin/bash

# AI Travel Assistant Planner Setup Script
echo "🌍 Setting up AI Travel Assistant Planner..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first"
    exit 1
fi

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [ "$(echo "$python_version >= 3.8" | bc)" -eq 0 ]; then
    echo "❌ Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env .env
    echo "⚠️  Please update your GEMINI_API_KEY in .env file"
else
    echo "✅ .env file already exists"
fi

# Check if all required files exist
files=("main.py" "config.py" "utils.py" "components.py" "requirements.txt")
missing_files=()

for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All required files are present"
else
    echo "❌ Missing files: ${missing_files[*]}"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update your GEMINI_API_KEY in the .env file"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run main.py"
echo ""
echo "🌐 The app will open in your browser at http://localhost:8501"
echo ""echo "🚀 Enjoy planning your travels with AI!"
