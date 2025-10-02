# Avalanche Risk Prediction Web Application

A real-time avalanche risk assessment web application for Colorado backcountry zones, built with machine learning models trained on historical climate, snow, and avalanche data.

## 🌐 Live Demo

Visit the deployed application at: [Your Vercel URL]

## 🏔️ Features

- **Interactive Map**: Real-time visualization of avalanche risk levels across 10 Colorado backcountry zones
- **Risk Assessment**: Color-coded zones showing current avalanche risk (Low, Moderate, Considerable, High, Extreme)
- **Model Metrics**: Display of model performance (Accuracy: 92%, Precision: 86%, Recall: 88%)
- **Zone Details**: Click on any zone to see detailed risk information and probabilities
- **Responsive Design**: Clean, modern interface optimized for all devices
- **Real-time Updates**: Automatic refresh of risk assessments every 30 seconds

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Mapping**: Leaflet.js with OpenStreetMap
- **Backend**: Python Flask API
- **ML Models**: Gradient Boosting Classifier (Scikit-learn)
- **Deployment**: Vercel
- **Styling**: Custom CSS with gradient backgrounds

## 📊 Model Information

- **Algorithm**: Gradient Boosting Classifier
- **Training Data**: 2011-2016 winters (6 seasons)
- **Validation**: 2016-2017 winter season
- **Target**: D2+ destructive avalanches
- **Features**: Weather, snowpack, temperature, wind data
- **Zones**: 10 Colorado backcountry zones

## 🚀 Deployment on Vercel

### Prerequisites
- Node.js and npm installed
- Vercel CLI installed (`npm i -g vercel`)

### Deployment Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd avalanche-prediction/web-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

4. **Configure environment variables** (if needed)
   ```bash
   vercel env add VARIABLE_NAME
   ```

### File Structure
```
web-app/
├── index.html          # Main HTML file
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
├── api/
│   └── index.py        # Flask API endpoints
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies
└── README.md           # This file
```

## 🔧 API Endpoints

- `GET /api/risk-assessment` - Get current risk assessment for all zones
- `GET /api/zone/<zone_id>` - Get detailed information for a specific zone
- `GET /api/model-metrics` - Get model performance metrics
- `GET /api/health` - Health check endpoint

## 🎨 Design Features

The interface follows a clean, modern design similar to your web scraper project with:
- Gradient backgrounds (purple to blue)
- Card-based layout
- Smooth animations and hover effects
- Responsive grid system
- Professional color scheme
- Clear typography and spacing

## ⚠️ Important Disclaimer

**This tool is for educational and research purposes only.**

This information is NOT intended to be used as an operational avalanche risk forecast. Please refer to professional avalanche forecasts for actual backcountry travel decisions:

[Colorado Avalanche Information Center](http://avalanche.state.co.us)

## 🔄 Real-time Updates

The application automatically updates risk assessments every 30 seconds and includes:
- Live timestamp display
- Refresh button for manual updates
- Keyboard shortcut (R key) for quick refresh
- Loading animations during updates

## 📱 Mobile Responsive

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🎯 Future Enhancements

- Integration with real weather APIs
- Historical risk trend visualization
- User authentication and preferences
- Push notifications for high-risk alerts
- Detailed forecast charts
- Social sharing features

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Created by Prashant

---

**Remember**: Always check with professional avalanche forecasters before making backcountry travel decisions!
