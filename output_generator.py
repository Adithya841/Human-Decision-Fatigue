import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class OutputGenerator:
    def __init__(self):
        self.plots_saved = []
    
    def print_header(self):
        """Print project header"""
        print("=" * 60)
        print("PREDICTION OF HUMAN DECISION FATIGUE USING BEHAVIORAL DATA")
        print("=" * 60)
        print()
    
    def print_section_header(self, title, separator="-"):
        """Print a section header"""
        print(f"\n{title}")
        print(separator * len(title))
    
    def print_data_summary(self, summary):
        """Print data loading summary"""
        self.print_section_header("1. DATASET SUMMARY")
        print(f"Total samples: {summary['total_samples']}")
        print(f"Dataset shape: {summary['shape']}")
        print(f"Number of features: {len(summary['columns'])}")
        print(f"Missing values: {sum(summary['missing_values'].values())}")
        print(f"Class distribution: {summary['fatigue_distribution']}")
    
    def print_preprocessing_info(self, X_shape, y_shape):
        """Print preprocessing information"""
        self.print_section_header("2. DATA PREPROCESSING COMPLETED")
        print(f"Feature matrix shape: {X_shape}")
        print(f"Target vector shape: {y_shape}")
        print("Features normalized and ready for modeling")
    
    def print_model_results(self, model_results, comparison_df):
        """Print model training results"""
        self.print_section_header("3. MODEL TRAINING RESULTS")
        
        for name, results in model_results.items():
            print(f"\n{name}:")
            print(f"  Accuracy: {results['accuracy']:.4f}")
            print(f"  Precision: {results['precision']:.4f}")
            print(f"  Recall: {results['recall']:.4f}")
            print(f"  F1-Score: {results['f1_score']:.4f}")
        
        self.print_section_header("4. MODEL COMPARISON")
        print(comparison_df.round(4))
    
    def print_best_model_info(self, best_model_name, best_results):
        """Print information about the best model"""
        self.print_section_header(f"5. BEST MODEL: {best_model_name.upper()}")
        print(f"Best F1-Score: {best_results['f1_score']:.4f}")
        print(f"Best Accuracy: {best_results['accuracy']:.4f}")
    
    def print_detailed_evaluation(self, cm, classification_report_str):
        """Print detailed model evaluation"""
        self.print_section_header("6. DETAILED MODEL EVALUATION")
        print("Confusion Matrix:")
        print(cm)
        print("\nClassification Report:")
        print(classification_report_str)
    
    def print_tuning_results(self, best_params, pre_tuning_f1, post_tuning_f1):
        """Print hyperparameter tuning results"""
        self.print_section_header("7. HYPERPARAMETER TUNING RESULTS")
        print(f"Best parameters: {best_params}")
        print(f"Pre-tuning F1-score: {pre_tuning_f1:.4f}")
        print(f"Post-tuning F1-score: {post_tuning_f1:.4f}")
        print(f"Improvement: {post_tuning_f1 - pre_tuning_f1:.4f}")
    
    def print_feature_importance(self, feature_importance_df, top_n=10):
        """Print feature importance results"""
        self.print_section_header("8. FEATURE IMPORTANCE ANALYSIS")
        print(f"Top {top_n} Most Important Features:")
        print(feature_importance_df.head(top_n))
    
    def save_model_comparison_plot(self, y, model_results):
        """Save model comparison plot"""
        plt.figure(figsize=(10, 6))
        plt.subplot(1, 2, 1)
        pd.Series(y).value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
        plt.title('Class Distribution (Fatigue Levels)')
        plt.xlabel('Fatigue Level (0=Low, 1=High)')
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        
        # Model comparison
        plt.subplot(1, 2, 2)
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        x = np.arange(len(metrics))
        width = 0.25
        
        for i, (model_name, results) in enumerate(model_results.items()):
            values = [results['accuracy'], results['precision'], results['recall'], results['f1_score']]
            plt.bar(x + i*width, values, width, label=model_name)
        
        plt.xlabel('Metrics')
        plt.ylabel('Score')
        plt.title('Model Performance Comparison')
        plt.xticks(x + width, metrics)
        plt.legend()
        plt.ylim(0, 1)
        plt.tight_layout()
        filename = 'model_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots_saved.append(filename)
        print(f"Model comparison plot saved as '{filename}'")
    
    def save_confusion_matrix_plot(self, cm, best_model_name):
        """Save confusion matrix plot"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Low Fatigue', 'High Fatigue'],
                    yticklabels=['Low Fatigue', 'High Fatigue'])
        plt.title(f'Confusion Matrix - {best_model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        filename = 'confusion_matrix.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        self.plots_saved.append(filename)
        print(f"Confusion matrix plot saved as '{filename}'")
    
    def save_feature_importance_plot(self, feature_importance_df, top_n=15):
        """Save feature importance plot"""
        if feature_importance_df is not None:
            plt.figure(figsize=(12, 8))
            top_features = feature_importance_df.head(top_n)
            plt.barh(range(len(top_features)), top_features['importance'])
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('Feature Importance')
            plt.title(f'Top {top_n} Feature Importances')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            filename = 'feature_importance.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots_saved.append(filename)
            print(f"Feature importance plot saved as '{filename}'")
    
    def save_feature_correlation_plot(self, X_scaled, feature_importance_df, top_n=10):
        """Save feature correlation plot"""
        if feature_importance_df is not None:
            plt.figure(figsize=(12, 10))
            top_corr_features = feature_importance_df.head(top_n)['feature'].tolist()
            correlation_matrix = pd.DataFrame(X_scaled, columns=feature_importance_df['feature'].tolist())[top_corr_features].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
            plt.title(f'Correlation Matrix - Top {top_n} Features')
            plt.tight_layout()
            filename = 'feature_correlation.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            self.plots_saved.append(filename)
            print(f"Feature correlation plot saved as '{filename}'")
    
    def print_conclusions(self, summary, model_results, best_model_name, feature_importance_df, tuning_results=None):
        """Print final conclusions and insights"""
        self.print_section_header("9. CONCLUSIONS AND INSIGHTS")
        print("=" * 40)
        
        print("\nKEY FINDINGS:")
        print("-------------")
        
        print(f"1. Dataset Summary:")
        print(f"   - Total samples: {summary['total_samples']}")
        print(f"   - Number of features: {len(summary['columns']) - 2}")  # excluding subject_id and fatigue_level
        print(f"   - Class distribution: {summary['fatigue_distribution']}")
        
        best_results = model_results[best_model_name]
        print(f"\n2. Model Performance:")
        print(f"   - Best performing model: {best_model_name}")
        print(f"   - Best F1-score: {best_results['f1_score']:.4f}")
        print(f"   - Best accuracy: {best_results['accuracy']:.4f}")
        
        if tuning_results:
            print(f"\n3. Hyperparameter Tuning Results:")
            print(f"   - Pre-tuning F1-score: {best_results['f1_score']:.4f}")
            print(f"   - Post-tuning F1-score: {tuning_results['post_tuning_f1']:.4f}")
            print(f"   - Improvement: {tuning_results['post_tuning_f1'] - best_results['f1_score']:.4f}")
        
        print(f"\n4. Decision Fatigue Patterns:")
        if feature_importance_df is not None:
            top_3_features = feature_importance_df.head(3)['feature'].tolist()
            print(f"   - Top 3 most predictive features: {top_3_features}")
            print(f"   - These features likely represent key behavioral indicators of decision fatigue")
        
        print(f"\n5. Practical Implications:")
        print(f"   - The model can predict decision fatigue with good accuracy")
        print(f"   - Behavioral patterns show clear distinction between high and low fatigue states")
        print(f"   - This could be used for real-time fatigue monitoring in high-stakes environments")
        
        print(f"\n6. Limitations:")
        print(f"   - Dataset is limited to specific behavioral measurements")
        print(f"   - Results may not generalize to all populations")
        print(f"   - More diverse features could improve performance")
        
        print(f"\n7. Future Work:")
        print(f"   - Collect more diverse behavioral data")
        print(f"   - Explore deep learning approaches for time series")
        print(f"   - Include physiological measures (heart rate, EEG)")
        print(f"   - Real-time implementation and validation")
    
    def print_completion_message(self):
        """Print project completion message"""
        print("\n" + "=" * 60)
        print("PROJECT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        if self.plots_saved:
            print(f"\nGenerated plots: {', '.join(self.plots_saved)}")
        print()

# Test the output generator
if __name__ == "__main__":
    output_gen = OutputGenerator()
    output_gen.print_header()
    output_gen.print_section_header("Test Output Generator", "=")
    print("Output generator is ready for use!")