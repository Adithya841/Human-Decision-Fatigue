"""
Interactive Decision Fatigue Prediction System
User interface for inputting behavioral data and getting predictions from trained ML model
"""

import pandas as pd
import numpy as np
import pickle
import os
from data_loader import load_behavioral_data, extract_features
from ml_model import DecisionFatiguePredictor
from sklearn.model_selection import train_test_split

class DecisionFatigueUI:
    def __init__(self):
        self.predictor = None
        self.feature_columns = None
        self.model_trained = False
        
    def initialize_model(self):
        """Initialize and train the ML model"""
        print("🚀 Initializing Decision Fatigue Prediction System...")
        print("=" * 60)
        
        try:
            # Load and prepare data
            print("📊 Loading behavioral data...")
            raw_df = load_behavioral_data()
            features_df = extract_features(raw_df)
            
            # Initialize predictor
            self.predictor = DecisionFatiguePredictor(random_state=42)
            
            # Prepare data
            X, y, self.feature_columns = self.predictor.prepare_data(features_df)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_train_scaled, X_test_scaled = self.predictor.preprocess_data(X_train, X_test)
            
            # Train models
            print("🤖 Training ML models...")
            model_results = self.predictor.train_models(X_train_scaled, X_test_scaled, y_train, y_test)
            comparison_df = self.predictor.compare_models()
            
            # Detailed evaluation
            self.predictor.detailed_evaluation(y_test, self.feature_columns)
            
            self.model_trained = True
            print(f"\n✅ Model trained successfully! Best model: {self.predictor.best_model_name}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing model: {e}")
            return False
    
    def get_user_input(self):
        """Get behavioral data input from user"""
        print("\n" + "=" * 60)
        print("📝 ENTER BEHAVIORAL DATA FOR FATIGUE PREDICTION")
        print("=" * 60)
        print("\nPlease enter the following behavioral measurements:")
        print("(These represent time series data from cognitive tasks)")
        
        # Define the expected features based on your data structure
        # These correspond to the trial types in your dataset
        trial_types = ['0back', '3back', '5back', '6back']
        
        user_data = {}
        
        for trial in trial_types:
            print(f"\n--- {trial.upper()} Trial Data ---")
            print(f"Enter behavioral measurements for {trial} cognitive task:")
            
            try:
                # Get basic statistics for each trial type
                response_time = float(input(f"  Average response time (ms): "))
                accuracy = float(input(f"  Accuracy (0-1): "))
                variability = float(input(f"  Response variability (std dev): "))
                
                user_data[f'{trial}_mean'] = response_time
                user_data[f'{trial}_std'] = variability
                user_data[f'{trial}_min'] = response_time - (variability * 2)
                user_data[f'{trial}_max'] = response_time + (variability * 2)
                user_data[f'{trial}_median'] = response_time
                user_data[f'{trial}_skew'] = 0.0  # Default
                user_data[f'{trial}_kurt'] = 0.0  # Default
                user_data[f'{trial}_range'] = user_data[f'{trial}_max'] - user_data[f'{trial}_min']
                
            except ValueError:
                print("❌ Invalid input. Please enter numeric values.")
                return None
        
        return user_data
    
    def create_feature_vector(self, user_data):
        """Create feature vector matching the trained model's expected format"""
        if not self.feature_columns:
            print("❌ Model not initialized. Feature columns unknown.")
            return None
        
        # Create feature vector with all expected features
        feature_vector = []
        
        for feature_name in self.feature_columns:
            if feature_name in user_data:
                feature_vector.append(user_data[feature_name])
            else:
                # Use default values for missing features
                feature_vector.append(0.0)
        
        return np.array(feature_vector)
    
    def make_prediction(self, feature_vector):
        """Make prediction using the trained model"""
        if not self.model_trained or not self.predictor:
            print("❌ Model not trained. Please initialize first.")
            return None, None
        
        try:
            prediction, probability = self.predictor.predict_single_sample(feature_vector)
            
            # Interpret results
            fatigue_level = "High Decision Fatigue" if prediction == 1 else "Low Decision Fatigue"
            confidence = max(probability) if probability is not None else "N/A"
            
            return fatigue_level, confidence
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return None, None
    
    def display_results(self, fatigue_level, confidence):
        """Display prediction results"""
        print("\n" + "=" * 60)
        print("🎯 PREDICTION RESULTS")
        print("=" * 60)
        
        print(f"\n📊 Predicted Fatigue Level: {fatigue_level}")
        
        if confidence != "N/A":
            print(f"🎯 Confidence Score: {confidence:.2f}")
            
            # Provide interpretation
            if confidence >= 0.9:
                print("💡 Very High Confidence - Model is very certain about this prediction")
            elif confidence >= 0.7:
                print("💡 High Confidence - Model is reasonably certain")
            elif confidence >= 0.5:
                print("💡 Moderate Confidence - Model is somewhat uncertain")
            else:
                print("⚠️  Low Confidence - Model prediction should be verified")
        
        # Provide recommendations based on fatigue level
        print(f"\n📋 RECOMMENDATIONS:")
        if "High" in fatigue_level:
            print("  ⚠️  Consider taking a break from decision-making tasks")
            print("  🧘 Try relaxation techniques or stress reduction")
            print("  💧 Stay hydrated and ensure proper nutrition")
            print("  😴 Consider rest before important decisions")
        else:
            print("  ✅ Current fatigue level appears manageable")
            print("  🎯 Continue monitoring during extended tasks")
            print("  📝 Consider regular breaks to maintain performance")
        
        print("=" * 60)
    
    def run_interactive_session(self):
        """Run the complete interactive prediction session"""
        print("🧠 HUMAN DECISION FATIGUE PREDICTION SYSTEM")
        print("=" * 60)
        print("This system predicts decision fatigue based on behavioral data")
        print("from cognitive tasks (0-back, 3-back, 5-back, 6-back trials)")
        
        # Initialize model
        if not self.initialize_model():
            return
        
        while True:
            print("\n" + "=" * 60)
            print("🎮 MAIN MENU")
            print("=" * 60)
            print("1. Make new prediction")
            print("2. View model information")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                # Get user input
                user_data = self.get_user_input()
                if user_data is None:
                    continue
                
                # Create feature vector
                feature_vector = self.create_feature_vector(user_data)
                if feature_vector is None:
                    continue
                
                # Make prediction
                fatigue_level, confidence = self.make_prediction(feature_vector)
                if fatigue_level is not None:
                    self.display_results(fatigue_level, confidence)
                
            elif choice == '2':
                self.display_model_info()
                
            elif choice == '3':
                print("\n👋 Thank you for using the Decision Fatigue Prediction System!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    def display_model_info(self):
        """Display information about the trained model"""
        print("\n" + "=" * 60)
        print("🤖 MODEL INFORMATION")
        print("=" * 60)
        
        if not self.model_trained:
            print("❌ Model not trained yet.")
            return
        
        print(f"🎯 Best Model: {self.predictor.best_model_name}")
        print(f"📊 Model Type: Classification")
        print(f"🎯 Target: Decision Fatigue Level (0=Low, 1=High)")
        print(f"📈 Number of Features: {len(self.feature_columns)}")
        
        print(f"\n🔍 Top Features Used:")
        if hasattr(self.predictor.best_model, 'coef_'):
            # For Logistic Regression
            coef = np.abs(self.predictor.best_model.coef_[0])
            feature_importance = list(zip(self.feature_columns, coef))
            feature_importance.sort(key=lambda x: x[1], reverse=True)
            
            for i, (feature, importance) in enumerate(feature_importance[:5]):
                print(f"  {i+1}. {feature}: {importance:.4f}")
        
        print(f"\n📝 How it works:")
        print(f"  1. Behavioral data from cognitive tasks is collected")
        print(f"  2. Statistical features are extracted (mean, std, min, max, etc.)")
        print(f"  3. Features are normalized and fed to the trained ML model")
        print(f"  4. Model predicts fatigue level with confidence score")
        
        print("=" * 60)

def main():
    """Main function to run the interactive system"""
    ui_system = DecisionFatigueUI()
    ui_system.run_interactive_session()

if __name__ == "__main__":
    main()
