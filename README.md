# 🌍 AI Travel Assistant Planner

An intelligent travel planning application that creates personalized itineraries based on your budget, preferences, and travel style. Powered by Google's Gemini 2.0 Flash AI and built with Streamlit for a beautiful, interactive user experience.

![Travel Planner](https://img.shields.io/badge/AI-Travel%20Planner-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Gemini AI](https://img.shields.io/badge/Gemini-2.0%20Flash-purple)

## ✨ Features

### 🎯 Smart Personalization
- **Budget Optimization**: Plans trips within your exact budget with smart allocation
- **Travel Style Matching**: Luxury, mid-range, or budget travel options
- **Dietary Preferences**: Accommodates all dietary restrictions and preferences
- **Group Dynamics**: Optimized for solo, couple, family, or group travel

### 🤖 AI-Powered Planning
- **Dynamic Itinerary Generation**: Day-by-day detailed planning with activities, meals, and transport
- **Real-time Adjustments**: Adapt plans based on budget changes, weather, or preferences
- **Local Insights**: Hidden gems, money-saving tips, and cultural recommendations
- **Smart Routing**: Optimized travel routes to minimize time and costs

### 💰 Budget Intelligence
- **Cost Breakdown**: Detailed expense analysis with visual charts
- **Budget Tracking**: Real-time monitoring of planned vs actual costs
- **Savings Optimization**: Suggestions for budget-friendly alternatives
- **Flexible Adjustments**: Easy budget modification with instant plan updates

### 🎨 Beautiful User Interface
- **Modern Design**: Gradient backgrounds and smooth animations
- **Interactive Charts**: Plotly visualizations for budget analysis
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Intuitive Navigation**: Easy-to-use tabbed interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google AI Studio API key (Gemini 2.0)
- Internet connection

### Installation

1. **Clone or Download** the project files
```bash
# If using git
git clone <repository-url>
cd ai-travel-planner

# Or download and extract the ZIP file
```

2. **Run Setup Script** (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

3. **Manual Setup** (Windows/Alternative)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

4. **Configure API Key**
   - Open `.env` file
   - Replace `your-api-key-here` with your actual Gemini API key
   - Save the file

5. **Launch Application**
```bash
streamlit run main.py
```

6. **Open in Browser**
   - Navigate to `http://localhost:8501`
   - Start planning your dream trip!

## 📁 Project Structure

```
ai-travel-planner/
├── main.py              # Main Streamlit application
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── components.py        # UI components
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── setup.sh            # Installation script
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Required: Your Gemini API key
GEMINI_API_KEY=your-api-key-here

# Optional: Application settings
APP_NAME=AI Travel Assistant Planner
DEBUG=False
LOG_LEVEL=INFO
```

### Getting Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## 🎮 How to Use

### 1. Trip Planning
1. **Enter Budget**: Set your total trip budget
2. **Choose Destination**: Enter any city or country
3. **Select Dates**: Pick duration and start date
4. **Set Preferences**: Choose travel style and interests
5. **Generate Plan**: Click "Plan My Trip!"

### 2. Review Itinerary
- **Budget Overview**: See cost breakdown and analysis
- **Daily Plans**: Detailed day-by-day activities
- **Recommendations**: Expert tips and local insights
- **Alternatives**: Budget and luxury options

### 3. Dynamic Adjustments
- **Budget Changes**: Use sidebar to modify budget
- **Weather Backup**: Get indoor alternatives
- **Regenerate**: Create new plans instantly

## 🛠 Advanced Features

### Budget Intelligence
- **Smart Allocation**: Automatically distributes budget across categories
- **Variance Analysis**: Shows budget performance vs plan
- **Optimization Tips**: Suggests ways to save money
- **Flexible Planning**: Adjusts to budget changes

### Personalization Engine
- **Activity Matching**: Recommends based on your interests
- **Dietary Accommodation**: Finds suitable restaurants
- **Group Optimization**: Adjusts for travel companions
- **Style Preferences**: Matches luxury, mid-range, or budget

### Data Export
- **CSV Export**: Download detailed itinerary
- **Budget Reports**: Comprehensive cost analysis
- **Sharing Options**: Easy trip sharing (future feature)

## 🎨 UI Components

### Visual Design
- **Gradient Cards**: Beautiful color-coded sections
- **Interactive Charts**: Plotly-powered visualizations
- **Responsive Layout**: Works on all screen sizes
- **Smooth Animations**: Hover effects and transitions

### Navigation
- **Tabbed Interface**: Easy day-by-day browsing
- **Sidebar Controls**: Dynamic adjustment panel
- **Progress Indicators**: Clear planning steps
- **Quick Actions**: One-click regeneration

## 📊 Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS/HTML
- **Backend**: Python with Google Gemini AI
- **Data Processing**: Pandas for analysis
- **Visualization**: Plotly for charts
- **State Management**: Streamlit session state

### AI Integration
- **Model**: Gemini 2.0 Flash Experimental
- **Prompt Engineering**: Structured JSON responses
- **Error Handling**: Fallback itineraries
- **Response Parsing**: Robust JSON extraction

### Performance
- **Caching**: Streamlit caching for API calls
- **Optimization**: Efficient data processing
- **Responsiveness**: Fast UI updates
- **Error Recovery**: Graceful failure handling

## 🔒 Security & Privacy

### Data Protection
- **API Keys**: Stored securely in environment variables
- **Local Processing**: No user data sent to third parties
- **Session Management**: Temporary storage only
- **Privacy First**: No data collection or tracking

### Best Practices
- **Environment Variables**: Sensitive data protection
- **Input Validation**: Prevents malicious inputs
- **Error Handling**: Secure error messages
- **Dependencies**: Regularly updated packages

## 🚨 Troubleshooting

### Common Issues

#### API Key Errors
```
Error: GEMINI_API_KEY not found
Solution: Check your .env file and API key
```

#### Installation Problems
```
Error: Module not found
Solution: Ensure virtual environment is activated
```

#### Performance Issues
```
Problem: Slow response times
Solution: Check internet connection and API limits
```

### Debug Mode
Enable debug mode in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 📈 Roadmap

### Version 2.0 (Planned)
- [ ] Real-time flight booking integration
- [ ] Weather API integration
- [ ] Multi-language support
- [ ] Offline map downloads
- [ ] Social sharing features

### Version 1.5 (Next Release)
- [ ] PDF export functionality
- [ ] Calendar integration
- [ ] Budget alerts and notifications
- [ ] Historical trip tracking
- [ ] User profiles and preferences

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Use GitHub issues
2. **Suggest Features**: Share your ideas
3. **Code Contributions**: Fork and submit PRs
4. **Documentation**: Improve guides and docs
5. **Testing**: Help test new features

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd ai-travel-planner

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Start development server
streamlit run main.py --server.runOnSave true
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI Studio** for Gemini API access
- **Streamlit** for the amazing framework
- **Plotly** for beautiful visualizations
- **Open Source Community** for inspiration and tools

## 📞 Support

### Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [Gemini AI Docs](https://ai.google.dev/docs)
- [Plotly Docs](https://plotly.com/python/)

### Community
- Join our [Discord](https://discord.gg/travel-planner) (if available)
- Follow us on [Twitter](https://twitter.com/travel-planner) (if available)
- Star us on [GitHub](https://github.com/your-repo) (if available)

### Contact
- **Email**: your-email@example.com
- **Issues**: GitHub Issues page
- **Discussions**: GitHub Discussions page

---

**Made with ❤️ and AI** | **Happy Travels! 🌍✈️**