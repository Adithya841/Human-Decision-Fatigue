"""
Main script for Human Decision Fatigue Prediction
Modular approach with separate input, processing, and output components
"""

# Import the modular components
from data_loader import load_behavioral_data, extract_features, get_data_summary
from ml_model import DecisionFatiguePredictor
from output_generator import OutputGenerator
from sklearn.model_selection import train_test_split

def main():
    # Initialize components
    output_gen = OutputGenerator()
    ml_predictor = DecisionFatiguePredictor(random_state=42)
    
    # Print header
    output_gen.print_header()
    
    # 1. LOAD DATA (Input Component)
    try:
        print("1. LOADING DATASET")
        print("-" * 20)
        raw_df = load_behavioral_data()
        features_df = extract_features(raw_df)
        data_summary = get_data_summary(features_df)
        output_gen.print_data_summary(data_summary)
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # 2. PREPARE DATA FOR MODELING
    try:
        print("\n2. PREPARING DATA FOR MODELING")
        print("-" * 30)
        X, y, feature_columns = ml_predictor.prepare_data(features_df)
        output_gen.print_preprocessing_info(X.shape, y.shape)
    except Exception as e:
        print(f"Error preparing data: {e}")
        return
    
    # 3. SPLIT DATASET
    print("\n3. SPLITTING DATASET")
    print("-" * 20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # 4. PREPROCESS DATA
    X_train_scaled, X_test_scaled = ml_predictor.preprocess_data(X_train, X_test)
    
    # 5. TRAIN MODELS (Processing Component)
    try:
        model_results = ml_predictor.train_models(X_train_scaled, X_test_scaled, y_train, y_test)
        comparison_df = ml_predictor.compare_models()
        output_gen.print_model_results(model_results, comparison_df)
        output_gen.print_best_model_info(ml_predictor.best_model_name, 
                                       model_results[ml_predictor.best_model_name])
    except Exception as e:
        print(f"Error training models: {e}")
        return
    
    # 6. DETAILED EVALUATION
    try:
        cm, feature_importance = ml_predictor.detailed_evaluation(y_test, feature_columns)
        # For demonstration, we'll recreate the classification report string
        from sklearn.metrics import classification_report
        classification_report_str = classification_report(y_test, model_results[ml_predictor.best_model_name]['predictions'])
        output_gen.print_detailed_evaluation(cm, classification_report_str)
    except Exception as e:
        print(f"Error in detailed evaluation: {e}")
        return
    
    # 7. HYPERPARAMETER TUNING
    try:
        tuned_model, tuned_accuracy, tuned_f1, best_params = ml_predictor.hyperparameter_tuning(
            X_train_scaled, y_train, X_test_scaled, y_test
        )
        pre_tuning_f1 = model_results[ml_predictor.best_model_name]['f1_score']
        tuning_results = {
            'best_params': best_params,
            'post_tuning_f1': tuned_f1,
            'pre_tuning_f1': pre_tuning_f1
        }
        output_gen.print_tuning_results(best_params, pre_tuning_f1, tuned_f1)
    except Exception as e:
        print(f"Error in hyperparameter tuning: {e}")
        tuning_results = None
    
    # 8. FEATURE IMPORTANCE
    if feature_importance is not None:
        output_gen.print_feature_importance(feature_importance)
    
    # 9. GENERATE OUTPUTS (Output Component)
    try:
        print("\n9. GENERATING VISUALIZATIONS")
        print("-" * 28)
        output_gen.save_model_comparison_plot(y, model_results)
        output_gen.save_confusion_matrix_plot(cm, ml_predictor.best_model_name)
        output_gen.save_feature_importance_plot(feature_importance)
        output_gen.save_feature_correlation_plot(X_test_scaled, feature_importance)
    except Exception as e:
        print(f"Error generating visualizations: {e}")
    
    # 10. PRINT CONCLUSIONS
    output_gen.print_conclusions(
        data_summary, 
        model_results, 
        ml_predictor.best_model_name, 
        feature_importance,
        tuning_results
    )
    
    # 11. COMPLETION
    output_gen.print_completion_message()
    
    # Return results for potential further use
    return {
        'data_summary': data_summary,
        'model_results': model_results,
        'best_model': ml_predictor.best_model,
        'feature_importance': feature_importance,
        'tuning_results': tuning_results
    }

# Example usage function for external calls
def predict_fatigue_level(sample_data, trained_model_results=None):
    """
    Predict fatigue level for new sample data
    
    Args:
        sample_data: Dictionary or array of feature values
        trained_model_results: Results from main() function
    
    Returns:
        prediction: 0 (low fatigue) or 1 (high fatigue)
        probability: Confidence scores
    """
    if trained_model_results is None:
        # Train model first if not provided
        results = main()
        ml_predictor = DecisionFatiguePredictor()
    else:
        ml_predictor = DecisionFatiguePredictor()
        ml_predictor.best_model = trained_model_results['best_model']
    
    # Make prediction
    prediction, probability = ml_predictor.predict_single_sample(sample_data)
    return prediction, probability

if __name__ == "__main__":
    # Run the complete pipeline
    results = main()
    
    # Example of how to use for new predictions (uncomment to test)
    # sample_prediction = predict_fatigue_level(your_sample_data, results)
    # print(f"Predicted fatigue level: {sample_prediction[0]}")