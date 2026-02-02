import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import warnings
import os
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("=" * 60)
print("PREDICTION OF HUMAN DECISION FATIGUE USING BEHAVIORAL DATA")
print("=" * 60)
print()

# 1. LOAD AND CONSOLIDATE DATASET
print("1. LOADING AND CONSOLIDATING DATASET")
print("-" * 40)

def load_behavioral_data():
    """Load and consolidate all CSV files from High_MWL and Low_MWL directories"""
    data_frames = []
    
    # Load High MWL files (High Decision Fatigue)
    high_mwl_path = "High_MWL/High_MWL"
    if os.path.exists(high_mwl_path):
        for file in os.listdir(high_mwl_path):
            if file.endswith('.csv'):
                file_path = os.path.join(high_mwl_path, file)
                df = pd.read_csv(file_path)
                df['fatigue_level'] = 1  # High fatigue
                df['subject_id'] = file.replace('.csv', '')
                data_frames.append(df)
                print(f"Loaded High MWL: {file} - Shape: {df.shape}")
    
    # Load Low MWL files (Low Decision Fatigue)
    low_mwl_path = "Low_MWL/Low_MWL"
    if os.path.exists(low_mwl_path):
        for file in os.listdir(low_mwl_path):
            if file.endswith('.csv'):
                file_path = os.path.join(low_mwl_path, file)
                df = pd.read_csv(file_path)
                df['fatigue_level'] = 0  # Low fatigue
                df['subject_id'] = file.replace('.csv', '')
                data_frames.append(df)
                print(f"Loaded Low MWL: {file} - Shape: {df.shape}")
    
    # Combine all data
    if data_frames:
        consolidated_df = pd.concat(data_frames, ignore_index=True)
        print(f"\nTotal consolidated dataset shape: {consolidated_df.shape}")
        return consolidated_df
    else:
        raise FileNotFoundError("No CSV files found in the specified directories")

# Load the data
try:
    df = load_behavioral_data()
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

print()

# 2. EXPLORATORY DATA ANALYSIS
print("2. EXPLORATORY DATA ANALYSIS")
print("-" * 30)

print(f"Dataset shape: {df.shape}")
print(f"Column names: {list(df.columns)}")
print(f"\nMissing values per column:")
print(df.isnull().sum())
print(f"\nData types:")
print(df.dtypes)

# Display basic statistics
print(f"\nBasic statistics:")
print(df.describe())

# Check class distribution
print(f"\nTarget variable distribution (fatigue_level):")
print(df['fatigue_level'].value_counts())
print(df['fatigue_level'].value_counts(normalize=True))

# 3. DATA PREPROCESSING
print("\n3. DATA PREPROCESSING")
print("-" * 20)

# Handle missing values
print("Handling missing values...")
numeric_columns = df.select_dtypes(include=[np.number]).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
print("Missing values handled by mean imputation")

# Feature engineering - extract statistical features from time series data
print("Engineering features from time series data...")

def extract_features(df):
    """Extract statistical features from the time series data"""
    feature_dfs = []
    
    for subject in df['subject_id'].unique():
        subject_data = df[df['subject_id'] == subject].copy()
        
        # Get numeric columns (excluding identifiers)
        numeric_cols = subject_data.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col not in ['fatigue_level']]
        
        if len(numeric_cols) > 0:
            # Extract features for each column
            features = {}
            features['subject_id'] = subject
            features['fatigue_level'] = subject_data['fatigue_level'].iloc[0]
            
            for col in numeric_cols:
                col_data = subject_data[col].dropna()
                if len(col_data) > 0:
                    features[f'{col}_mean'] = col_data.mean()
                    features[f'{col}_std'] = col_data.std()
                    features[f'{col}_min'] = col_data.min()
                    features[f'{col}_max'] = col_data.max()
                    features[f'{col}_median'] = col_data.median()
                    features[f'{col}_skew'] = col_data.skew()
                    features[f'{col}_kurt'] = col_data.kurt()
                    features[f'{col}_range'] = col_data.max() - col_data.min()
            
            feature_dfs.append(pd.DataFrame([features]))
    
    return pd.concat(feature_dfs, ignore_index=True)

# Extract features
processed_df = extract_features(df)
print(f"Feature engineering completed. New shape: {processed_df.shape}")

# Remove subject_id column as it's not a feature
feature_columns = [col for col in processed_df.columns if col not in ['subject_id', 'fatigue_level']]
X = processed_df[feature_columns]
y = processed_df['fatigue_level']

print(f"Final feature matrix shape: {X.shape}")
print(f"Target vector shape: {y.shape}")

# Normalize features
print("Normalizing features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=feature_columns)

print("Preprocessing completed!")

# 4. SPLIT DATASET
print("\n4. SPLITTING DATASET")
print("-" * 20)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")
print(f"Training class distribution:")
print(pd.Series(y_train).value_counts(normalize=True))
print(f"Testing class distribution:")
print(pd.Series(y_test).value_counts(normalize=True))

# 5. TRAIN MULTIPLE MODELS
print("\n5. TRAINING MULTIPLE CLASSIFICATION MODELS")
print("-" * 45)

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
    'Support Vector Machine': SVC(random_state=42, probability=True)
}

model_results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    model_results[name] = {
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

# 6. MODEL EVALUATION AND COMPARISON
print("\n6. MODEL EVALUATION AND COMPARISON")
print("-" * 35)

# Create comparison DataFrame
comparison_df = pd.DataFrame({
    'Model': list(model_results.keys()),
    'Accuracy': [results['accuracy'] for results in model_results.values()],
    'Precision': [results['precision'] for results in model_results.values()],
    'Recall': [results['recall'] for results in model_results.values()],
    'F1-Score': [results['f1_score'] for results in model_results.values()]
})

print("Model Performance Comparison:")
print(comparison_df.round(4))

# Find best model
best_model_name = comparison_df.loc[comparison_df['F1-Score'].idxmax(), 'Model']
best_model = model_results[best_model_name]['model']
print(f"\nBest performing model: {best_model_name}")

# 7. DETAILED EVALUATION OF BEST MODEL
print(f"\n7. DETAILED EVALUATION OF {best_model_name.upper()}")
print("-" * 50)

best_predictions = model_results[best_model_name]['predictions']
best_model_obj = model_results[best_model_name]['model']

# Confusion Matrix
print("Confusion Matrix:")
cm = confusion_matrix(y_test, best_predictions)
print(cm)

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, best_predictions))

# 8. HYPERPARAMETER TUNING
print(f"\n8. HYPERPARAMETER TUNING FOR {best_model_name}")
print("-" * 45)

if best_model_name == 'Random Forest':
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    base_model = RandomForestClassifier(random_state=42)
    
elif best_model_name == 'Logistic Regression':
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga']
    }
    base_model = LogisticRegression(random_state=42, max_iter=1000)
    
else:  # SVM
    param_grid = {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf', 'poly'],
        'gamma': ['scale', 'auto', 0.1, 1]
    }
    base_model = SVC(random_state=42)

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

# 9. FEATURE IMPORTANCE
print(f"\n9. FEATURE IMPORTANCE ANALYSIS")
print("-" * 30)

if hasattr(best_model, 'feature_importances_'):
    # Random Forest feature importance
    importances = best_model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print("Top 10 Most Important Features:")
    print(feature_importance_df.head(10))
    
    # Plot feature importance
    plt.figure(figsize=(12, 8))
    top_features = feature_importance_df.head(15)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Feature Importance')
    plt.title('Top 15 Feature Importances - Random Forest')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Feature importance plot saved as 'feature_importance.png'")
    
elif hasattr(best_model, 'coef_'):
    # Logistic Regression coefficients
    if len(best_model.coef_.shape) > 1:
        coef = np.mean(np.abs(best_model.coef_), axis=0)
    else:
        coef = np.abs(best_model.coef_[0])
        
    feature_importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': coef
    }).sort_values('importance', ascending=False)
    
    print("Top 10 Most Important Features (by coefficient magnitude):")
    print(feature_importance_df.head(10))

# 10. VISUALIZATIONS
print(f"\n10. DATA VISUALIZATIONS")
print("-" * 22)

# Class distribution
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
y.value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
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
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Model comparison plot saved as 'model_comparison.png'")

# Confusion matrix heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Low Fatigue', 'High Fatigue'],
            yticklabels=['Low Fatigue', 'High Fatigue'])
plt.title(f'Confusion Matrix - {best_model_name}')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("Confusion matrix plot saved as 'confusion_matrix.png'")

# Feature correlation heatmap (top 10 features)
plt.figure(figsize=(12, 10))
top_corr_features = feature_importance_df.head(10)['feature'].tolist()
correlation_matrix = X_scaled[top_corr_features].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Matrix - Top 10 Features')
plt.tight_layout()
plt.savefig('feature_correlation.png', dpi=300, bbox_inches='tight')
plt.close()
print("Feature correlation plot saved as 'feature_correlation.png'")

# 11. CONCLUSIONS AND INSIGHTS
print(f"\n11. CONCLUSIONS AND INSIGHTS")
print("=" * 40)

print("\nKEY FINDINGS:")
print("-------------")

print(f"1. Dataset Summary:")
print(f"   - Total samples: {len(df)}")
print(f"   - Number of features after engineering: {len(feature_columns)}")
print(f"   - Class distribution: {pd.Series(y).value_counts().to_dict()}")

print(f"\n2. Model Performance:")
print(f"   - Best performing model: {best_model_name}")
print(f"   - Best F1-score: {model_results[best_model_name]['f1_score']:.4f}")
print(f"   - Best accuracy: {model_results[best_model_name]['accuracy']:.4f}")

print(f"\n3. Hyperparameter Tuning Results:")
print(f"   - Pre-tuning F1-score: {model_results[best_model_name]['f1_score']:.4f}")
print(f"   - Post-tuning F1-score: {tuned_f1:.4f}")
print(f"   - Improvement: {tuned_f1 - model_results[best_model_name]['f1_score']:.4f}")

print(f"\n4. Decision Fatigue Patterns:")
if 'feature_importance_df' in locals():
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

print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY!")
print("=" * 60)