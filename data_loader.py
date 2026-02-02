import pandas as pd
import numpy as np
import os

def load_behavioral_data():
    """Load and consolidate all CSV files from High_MWL and Low_MWL directories"""
    print("Loading behavioral data from CSV files...")
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

def extract_features(df):
    """Extract statistical features from the time series data"""
    print("Engineering features from time series data...")
    
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
                    features[f'{col}_skew'] = col_data.skew() if len(col_data) > 1 else 0
                    features[f'{col}_kurt'] = col_data.kurt() if len(col_data) > 3 else 0
                    features[f'{col}_range'] = col_data.max() - col_data.min()
                else:
                    # Handle case where all values are NaN
                    features[f'{col}_mean'] = 0
                    features[f'{col}_std'] = 0
                    features[f'{col}_min'] = 0
                    features[f'{col}_max'] = 0
                    features[f'{col}_median'] = 0
                    features[f'{col}_skew'] = 0
                    features[f'{col}_kurt'] = 0
                    features[f'{col}_range'] = 0
            
            feature_dfs.append(pd.DataFrame([features]))
    
    result_df = pd.concat(feature_dfs, ignore_index=True)
    
    # Handle any remaining NaN values
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    print(f"Feature engineering completed. New shape: {result_df.shape}")
    return result_df

def get_data_summary(df):
    """Get summary statistics of the dataset"""
    summary = {
        'total_samples': len(df),
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'shape': df.shape,
        'fatigue_distribution': df['fatigue_level'].value_counts().to_dict() if 'fatigue_level' in df.columns else {}
    }
    return summary

if __name__ == "__main__":
    # Test the data loader
    try:
        df = load_behavioral_data()
        features_df = extract_features(df)
        summary = get_data_summary(features_df)
        print("\nData Loading Test Successful!")
        print(f"Loaded {summary['total_samples']} samples with {len(summary['columns'])} features")
    except Exception as e:
        print(f"Error: {e}")