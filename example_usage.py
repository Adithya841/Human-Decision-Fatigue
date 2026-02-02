"""
Example script demonstrating how to use the modular components
for making predictions on new data
"""

import numpy as np
from data_loader import load_behavioral_data, extract_features
from ml_model import DecisionFatiguePredictor
from sklearn.model_selection import train_test_split

def example_usage():
    """Example of how to use the modular components"""
    
    print("=== HUMAN DECISION FATIGUE PREDICTION - EXAMPLE USAGE ===\n")
    
    # Step 1: Load and train the model (one-time setup)
    print("1. Loading and training model...")
    raw_df = load_behavioral_data()
    features_df = extract_features(raw_df)
    
    # Initialize predictor
    predictor = DecisionFatiguePredictor(random_state=42)
    
    # Prepare data
    X, y, feature_columns = predictor.prepare_data(features_df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_scaled, X_test_scaled = predictor.preprocess_data(X_train, X_test)
    
    # Train models
    model_results = predictor.train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    comparison_df = predictor.compare_models()
    
    print(f"Model trained successfully! Best model: {predictor.best_model_name}")
    
    # Step 2: Make predictions on new data
    print("\n2. Making predictions on new samples...")
    
    # Example 1: Predict using test data
    sample_1 = X_test_scaled[0]  # First test sample
    prediction_1, probability_1 = predictor.predict_single_sample(sample_1)
    actual_1 = y_test.iloc[0]
    
    print(f"\nSample 1:")
    print(f"  Actual fatigue level: {actual_1} ({'High' if actual_1 == 1 else 'Low'})")
    print(f"  Predicted fatigue level: {prediction_1} ({'High' if prediction_1 == 1 else 'Low'})")
    if probability_1 is not None:
        print(f"  Confidence: {max(probability_1):.2f}")
    
    # Example 2: Another sample
    sample_2 = X_test_scaled[3]  # Fourth test sample
    prediction_2, probability_2 = predictor.predict_single_sample(sample_2)
    actual_2 = y_test.iloc[3]
    
    print(f"\nSample 2:")
    print(f"  Actual fatigue level: {actual_2} ({'High' if actual_2 == 1 else 'Low'})")
    print(f"  Predicted fatigue level: {prediction_2} ({'High' if prediction_2 == 1 else 'Low'})")
    if probability_2 is not None:
        print(f"  Confidence: {max(probability_2):.2f}")
    
    # Step 3: Batch predictions
    print("\n3. Batch predictions example...")
    test_predictions = predictor.best_model.predict(X_test_scaled)
    accuracy = (test_predictions == y_test).mean()
    print(f"Batch prediction accuracy on test set: {accuracy:.2f}")
    
    # Step 4: Feature importance for interpretation
    print("\n4. Key features for decision fatigue prediction:")
    if hasattr(predictor.best_model, 'coef_'):
        # For Logistic Regression
        coef_importance = np.abs(predictor.best_model.coef_[0])
        feature_importance = list(zip(feature_columns, coef_importance))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        print("Top 5 most important features:")
        for i, (feature, importance) in enumerate(feature_importance[:5]):
            print(f"  {i+1}. {feature}: {importance:.4f}")

def create_new_sample_prediction():
    """Example of creating a prediction for completely new behavioral data"""
    print("\n=== CREATING PREDICTION FOR NEW BEHAVIORAL DATA ===\n")
    
    # In a real scenario, you would collect new behavioral data
    # For this example, we'll simulate new data based on the trained model
    
    print("To predict fatigue level for new behavioral data:")
    print("1. Collect time series behavioral measurements")
    print("2. Extract the same statistical features used in training:")
    print("   - Mean, std, min, max, median, skew, kurt, range")
    print("   - For each trial type (0-back, 3-back, 5-back, 6-back)")
    print("3. Pass the feature vector to the predict_single_sample method")
    print("4. Get fatigue prediction (0=Low, 1=High) with confidence score")
    
    print("\nExample feature vector format:")
    print("[mean_0back, std_0back, min_0back, max_0back, ... , range_6back]")

if __name__ == "__main__":
    # Run the examples
    example_usage()
    create_new_sample_prediction()
    
    print("\n=== END OF EXAMPLES ===")
    print("The modular components can be imported and used in your own applications!")