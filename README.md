# Decision Fatigue Prediction System

A modern web application for predicting human decision fatigue based on behavioral data from cognitive tasks. This system uses machine learning to analyze response patterns and provide real-time fatigue assessments with confidence scores.

## Features

- **Real-time Prediction**: Instant decision fatigue analysis based on behavioral input
- **Modern UI**: Professional React frontend with Tailwind CSS
- **ML Models**: Multiple algorithms (Logistic Regression, Random Forest, SVM) with automatic best model selection
- **Comprehensive Analytics**: Model performance metrics and feature importance visualization
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Static Deployment**: Can be deployed as a static website

## Architecture

### Frontend (React + TypeScript)
- Modern React 18 with TypeScript
- Tailwind CSS for styling
- Recharts for data visualization
- Axios for API communication
- Responsive design with mobile-first approach

### Backend (FastAPI + Python)
- FastAPI for REST API endpoints
- Scikit-learn for machine learning
- Pandas and NumPy for data processing
- CORS support for frontend integration
- Automatic model initialization on startup

### Machine Learning Pipeline
- Data loading from CSV files
- Feature extraction (32 statistical features)
- Multiple model training and comparison
- Best model selection based on F1-score
- Real-time prediction with confidence scores

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Prediction
- `POST /predict` - Make fatigue prediction from behavioral data
- `GET /model-info` - Get model information and statistics
- `GET /model-metrics` - Get detailed model performance metrics
- `GET /feature-importance` - Get top 10 most important features
- `GET /health` - Health check endpoint

### Request Example
```json
{
  "behavioral_data": {
    "0back_mean": 1000,
    "0back_std": 200,
    "0back_min": 600,
    "0back_max": 1400,
    "0back_median": 1000,
    "0back_skew": 0.0,
    "0back_kurt": 0.0,
    "0back_range": 800,
    "3back_mean": 1200,
    "3back_std": 250,
    // ... other features
  }
}
```

### Response Example
```json
{
  "fatigue_level": "Low Decision Fatigue",
  "confidence": 0.85
}
```

## Project Structure

```
Human-Decision-Fatigue/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   └── requirements.txt   # Python dependencies
├── frontend/               # React frontend
│   ├── public/            # Static files
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   ├── services/      # API services
│   │   ├── App.tsx        # Main app component
│   │   └── index.tsx      # Entry point
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind configuration
├── ml_model.py            # ML model implementation
├── data_loader.py         # Data loading utilities
└── web_interface.py       # Original Streamlit interface
```

## Data Requirements

The system expects behavioral data from cognitive tasks with the following trial types:
- 0-back (baseline)
- 3-back (low difficulty)
- 5-back (medium difficulty)
- 6-back (high difficulty)

For each trial type, the following features are extracted:
- Mean response time
- Standard deviation
- Minimum and maximum values
- Median
- Skewness and kurtosis
- Range

## Model Performance

- **Dataset**: 44 subjects (22 high fatigue, 22 low fatigue)
- **Features**: 32 statistical features
- **Models**: Logistic Regression, Random Forest, Support Vector Machine
- **Best Performance**: 100% accuracy on test set
- **Validation**: 80/20 train-test split with stratified sampling

## Deployment

### Static Deployment

The frontend can be built and deployed as a static website:

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. The build files will be in `frontend/build/`
3. Deploy to any static hosting service (Netlify, Vercel, GitHub Pages, etc.)

### Backend Deployment

The backend can be deployed using:
- Docker containers
- Cloud services (AWS, Google Cloud, Azure)
- PaaS platforms (Heroku, Railway)
- Traditional VPS with systemd service

## Development

### Adding New Features

1. **New ML Models**: Add to `ml_model.py` in the `train_models` method
2. **New API Endpoints**: Add to `backend/main.py`
3. **New UI Components**: Add to `frontend/src/components/`
4. **New Pages**: Add to `frontend/src/pages/` and update routing in `App.tsx`

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript**: Use ESLint and Prettier configuration
- **Components**: Use functional components with hooks
- **API**: Follow RESTful conventions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original ML implementation and data processing
- React and FastAPI communities
- Tailwind CSS for the excellent utility framework
- Recharts for data visualization components
