import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

class DecisionFatiguePredictor:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.model_results = {}
        self.best_model = None
        self.best_model_name = None
        
    def prepare_data(self, df):
        """Prepare data for modeling"""
        # Remove identifier columns
        feature_columns = [col for col in df.columns if col not in ['subject_id', 'fatigue_level']]
        X = df[feature_columns]
        y = df['fatigue_level']
        
        print(f"Feature matrix shape: {X.shape}")
        print(f"Target vector shape: {y.shape}")
        
        return X, y, feature_columns
    
    def preprocess_data(self, X_train, X_test):
        """Scale/normalize the features"""
        print("Normalizing features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def train_models(self, X_train, X_test, y_train, y_test):
        """Train multiple classification models"""
        print("Training multiple classification models...")
        
        models = {
            'Logistic Regression': LogisticRegression(random_state=self.random_state, max_iter=1000),
            'Random Forest': RandomForestClassifier(random_state=self.random_state, n_estimators=100),
            'Support Vector Machine': SVC(random_state=self.random_state, probability=True)
        }
        
        self.model_results = {}
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            self.model_results[name] = {
                'model': model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'predictions': y_pred
            }
            
            print(f"Accuracy: {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall: {recall:.4f}")
            print(f"F1-Score: {f1:.4f}")
        
        return self.model_results
    
    def compare_models(self):
        """Compare all trained models and select the best one"""
        print("\nModel Performance Comparison:")
        comparison_df = pd.DataFrame({
            'Model': list(self.model_results.keys()),
            'Accuracy': [results['accuracy'] for results in self.model_results.values()],
            'Precision': [results['precision'] for results in self.model_results.values()],
            'Recall': [results['recall'] for results in self.model_results.values()],
            'F1-Score': [results['f1_score'] for results in self.model_results.values()]
        })
        
        print(comparison_df.round(4))
        
        # Find best model based on F1-score
        self.best_model_name = comparison_df.loc[comparison_df['F1-Score'].idxmax(), 'Model']
        self.best_model = self.model_results[self.best_model_name]['model']
        print(f"\nBest performing model: {self.best_model_name}")
        
        return comparison_df
    
    def detailed_evaluation(self, y_test, feature_columns):
        """Perform detailed evaluation of the best model"""
        print(f"\nDetailed Evaluation of {self.best_model_name.upper()}:")
        print("-" * 50)
        
        best_predictions = self.model_results[self.best_model_name]['predictions']
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, best_predictions)
        print("Confusion Matrix:")
        print(cm)
        
        # Classification Report
        print("\nClassification Report:")
        print(classification_report(y_test, best_predictions))
        
        # Feature Importance (if available)
        feature_importance = None
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            feature_importance = pd.DataFrame({
                'feature': feature_columns,
                'importance': importances
            }).sort_values('importance', ascending=False)
            print("\nTop 10 Most Important Features:")
            print(feature_importance.head(10))
            
        elif hasattr(self.best_model, 'coef_'):
            if len(self.best_model.coef_.shape) > 1:
                coef = np.mean(np.abs(self.best_model.coef_), axis=0)
            else:
                coef = np.abs(self.best_model.coef_[0])
                
            feature_importance = pd.DataFrame({
                'feature': feature_columns,
                'importance': coef
            }).sort_values('importance', ascending=False)
            print("\nTop 10 Most Important Features (by coefficient magnitude):")
            print(feature_importance.head(10))
        
        return cm, feature_importance
    
    def hyperparameter_tuning(self, X_train, y_train, X_test, y_test):
        """Perform hyperparameter tuning on the best model"""
        print(f"\nHyperparameter Tuning for {self.best_model_name}:")
        print("-" * 45)
        
        if self.best_model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            base_model = RandomForestClassifier(random_state=self.random_state)
            
        elif self.best_model_name == 'Logistic Regression':
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'saga']
            }
            base_model = LogisticRegression(random_state=self.random_state, max_iter=1000)
            
        else:  # SVM
            param_grid = {
                'C': [0.1, 1, 10],
                'kernel': ['linear', 'rbf', 'poly'],
                'gamma': ['scale', 'auto', 0.1, 1]
            }
            base_model = SVC(random_state=self.random_state)
        
        print("Performing grid search...")
        grid_search = GridSearchCV(
            base_model, 
            param_grid, 
            cv=5, 
            scoring='f1_weighted',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        
        # Evaluate tuned model
        tuned_model = grid_search.best_estimator_
        tuned_predictions = tuned_model.predict(X_test)
        
        tuned_accuracy = accuracy_score(y_test, tuned_predictions)
        tuned_f1 = f1_score(y_test, tuned_predictions, average='weighted')
        
        print(f"Tuned model accuracy: {tuned_accuracy:.4f}")
        print(f"Tuned model F1-score: {tuned_f1:.4f}")
        
        return tuned_model, tuned_accuracy, tuned_f1, grid_search.best_params_

    def predict_single_sample(self, sample_features):
        """Predict fatigue level for a single sample"""
        if self.best_model is None:
            raise ValueError("No trained model available. Train models first.")
        
        # Scale the sample
        sample_scaled = self.scaler.transform([sample_features])
        prediction = self.best_model.predict(sample_scaled)[0]
        probability = self.best_model.predict_proba(sample_scaled)[0] if hasattr(self.best_model, 'predict_proba') else None
        
        return prediction, probability

if __name__ == "__main__":
    # This would be used for testing the ML class
    print("ML Model class ready for use!")