"""
FastAPI Backend for Decision Fatigue Prediction System
Provides REST API endpoints for ML model predictions and information
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional, Union
import numpy as np
import pandas as pd
import sys
import os

# Add parent directory to path to import ML modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model import DecisionFatiguePredictor
from data_loader import load_behavioral_data, extract_features

# Initialize FastAPI app
app = FastAPI(
    title="Decision Fatigue Prediction API",
    description="API for predicting decision fatigue based on behavioral data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
predictor = None
feature_columns = None
model_trained = False

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    behavioral_data: Dict[str, float]

class PredictionResponse(BaseModel):
    fatigue_level: str
    confidence: float

class ModelInfoResponse(BaseModel):
    best_model: str
    test_accuracy: float
    feature_count: int
    target: str

class ModelMetricsResponse(BaseModel):
    model_comparison: List[Dict[str, Union[float, str]]]

class FeatureImportanceResponse(BaseModel):
    features: List[Dict[str, Union[float, str]]]

@app.on_event("startup")
async def startup_event():
    """Initialize the ML model on startup"""
    global predictor, feature_columns, model_trained
    
    try:
        print("Initializing ML model...")
        
        # Try to load real data first
        try:
            raw_df = load_behavioral_data()
            features_df = extract_features(raw_df)
            print("Loaded real behavioral data")
        except Exception as data_error:
            print(f"Could not load real data: {data_error}")
            print("Creating sample data for demonstration...")
            # Create sample data for demonstration
            import numpy as np
            np.random.seed(42)
            
            # Generate sample features (32 features for 44 subjects)
            n_samples = 44
            n_features = 32
            feature_names = []
            for trial in ['0back', '3back', '5back', '6back']:
                for stat in ['mean', 'std', 'min', 'max', 'median', 'skew', 'kurt', 'range']:
                    feature_names.append(f'{trial}_{stat}')
            
            sample_data = np.random.randn(n_samples, n_features)
            sample_data[:, 0] = np.random.normal(1000, 200, n_samples)  # 0back_mean
            sample_data[:, 8] = np.random.normal(1200, 250, n_samples)  # 3back_mean
            sample_data[:, 16] = np.random.normal(1400, 300, n_samples) # 5back_mean
            sample_data[:, 24] = np.random.normal(1600, 350, n_samples) # 6back_mean
            
            features_df = pd.DataFrame(sample_data, columns=feature_names)
            # Create realistic fatigue labels based on response times
            # Slower response times = higher fatigue
            fatigue_scores = []
            for i in range(n_samples):
                # Extract response time means (columns 0, 8, 16, 24)
                response_means = [sample_data[i, 0], sample_data[i, 8], sample_data[i, 16], sample_data[i, 24]]
                avg_response_time = np.mean(response_means)
                
                # Assign fatigue based on response time (slower = more fatigued)
                if avg_response_time < 1200:  # Fast responses = low fatigue
                    fatigue_level = 0
                elif avg_response_time < 1600:  # Medium responses = moderate fatigue
                    fatigue_level = np.random.choice([0, 1], p=[0.7, 0.3])  # 70% chance low fatigue
                else:  # Slow responses = high fatigue
                    fatigue_level = 1
                    
                fatigue_scores.append(fatigue_level)
            
            features_df['fatigue_level'] = fatigue_scores
            print(f"Created sample data with {n_samples} samples and {n_features} features")
        
        # Initialize predictor
        predictor = DecisionFatiguePredictor(random_state=42)
        print("Predictor initialized")
        
        # Prepare data
        print("Preparing data...")
        X, y, feature_columns = predictor.prepare_data(features_df)
        print(f"Data prepared: X shape={X.shape}, y shape={y.shape}, features={len(feature_columns)}")
        
        # Train models (using a subset for faster startup)
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"Data split: train={X_train.shape}, test={X_test.shape}")
        
        X_train_scaled, X_test_scaled = predictor.preprocess_data(X_train, X_test)
        print("Data preprocessing completed")
        
        # Train models
        print("Training models...")
        model_results = predictor.train_models(X_train_scaled, X_test_scaled, y_train, y_test)
        comparison_df = predictor.compare_models()
        print("Model training completed")
        
        model_trained = True
        print("Model initialization completed successfully!")
        print(f"Best model: {predictor.best_model_name}")
        print(f"Features: {len(feature_columns)}")
        
    except Exception as e:
        print(f"Error initializing model: {e}")
        import traceback
        traceback.print_exc()
        model_trained = False

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Decision Fatigue Prediction API",
        "version": "1.0.0",
        "status": "active" if model_trained else "model_not_loaded"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_fatigue(request: PredictionRequest):
    """Predict decision fatigue based on behavioral data"""
    
    if not model_trained or predictor is None:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # Create feature vector matching the trained model's expected format
        feature_vector = []
        for feature_name in feature_columns:
            if feature_name in request.behavioral_data:
                feature_vector.append(request.behavioral_data[feature_name])
            else:
                feature_vector.append(0.0)
        
        feature_vector = np.array(feature_vector)
        
        # Make prediction
        prediction, probability = predictor.predict_single_sample(feature_vector)
        
        # Convert prediction to human-readable format
        fatigue_level = "High Decision Fatigue" if prediction == 1 else "Low Decision Fatigue"
        confidence = max(probability) if probability is not None else 0.0
        
        return PredictionResponse(
            fatigue_level=fatigue_level,
            confidence=float(confidence)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get information about the trained model"""
    
    if not model_trained or predictor is None:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # Get model comparison results
        comparison_df = predictor.compare_models()
        
        return ModelInfoResponse(
            best_model=predictor.best_model_name,
            test_accuracy=float(predictor.model_results[predictor.best_model_name]['accuracy']),
            feature_count=len(feature_columns),
            target="Fatigue Level"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model info: {str(e)}")

@app.get("/model-metrics", response_model=ModelMetricsResponse)
async def get_model_metrics():
    """Get detailed model performance metrics"""
    
    if not model_trained or predictor is None:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # Get model comparison results
        comparison_df = predictor.compare_models()
        
        # Convert to list of dictionaries
        model_comparison = []
        for _, row in comparison_df.iterrows():
            model_comparison.append({
                "Model": row["Model"],
                "Accuracy": float(row["Accuracy"]),
                "Precision": float(row["Precision"]),
                "Recall": float(row["Recall"]),
                "F1-Score": float(row["F1-Score"])
            })
        
        return ModelMetricsResponse(model_comparison=model_comparison)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model metrics: {str(e)}")

@app.get("/feature-importance", response_model=FeatureImportanceResponse)
async def get_feature_importance():
    """Get feature importance from the best model"""
    
    if not model_trained or predictor is None:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # Get feature importance
        feature_importance = []
        
        if hasattr(predictor.best_model, 'coef_'):
            # For linear models
            coef = np.abs(predictor.best_model.coef_[0])
            for i, feature in enumerate(feature_columns):
                feature_importance.append({
                    "feature": feature,
                    "importance": float(coef[i])
                })
        elif hasattr(predictor.best_model, 'feature_importances_'):
            # For tree-based models
            importances = predictor.best_model.feature_importances_
            for i, feature in enumerate(feature_columns):
                feature_importance.append({
                    "feature": feature,
                    "importance": float(importances[i])
                })
        
        # Sort by importance and take top 10
        feature_importance.sort(key=lambda x: x["importance"], reverse=True)
        feature_importance = feature_importance[:10]
        
        return FeatureImportanceResponse(features=feature_importance)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feature importance: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_trained
    }

# Mount static files for frontend (optional)
if os.path.exists("../frontend/build"):
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
    
    @app.get("/ui")
    async def serve_frontend():
        """Serve the React frontend"""
        from fastapi.responses import FileResponse
        return FileResponse("../frontend/build/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
