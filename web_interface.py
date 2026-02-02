"""
Web-based Decision Fatigue Prediction System using Streamlit
Provides a user-friendly web interface for inputting behavioral data and getting predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from data_loader import load_behavioral_data, extract_features
from ml_model import DecisionFatiguePredictor
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Decision Fatigue Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitDecisionFatigueUI:
    def __init__(self):
        self.predictor = None
        self.feature_columns = None
        self.model_trained = False
        
    def initialize_model(self):
        """Initialize and train the ML model"""
        try:
            # Load and prepare data
            raw_df = load_behavioral_data()
            features_df = extract_features(raw_df)
            
            # Initialize predictor
            self.predictor = DecisionFatiguePredictor(random_state=42)
            
            # Prepare data
            X, y, self.feature_columns = self.predictor.prepare_data(features_df)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_train_scaled, X_test_scaled = self.predictor.preprocess_data(X_train, X_test)
            
            # Train models
            model_results = self.predictor.train_models(X_train_scaled, X_test_scaled, y_train, y_test)
            comparison_df = self.predictor.compare_models()
            
            # Store model info
            self.model_comparison = comparison_df
            self.test_accuracy = self.predictor.model_results[self.predictor.best_model_name]['accuracy']
            
            self.model_trained = True
            return True
            
        except Exception as e:
            st.error(f"Error initializing model: {e}")
            return False
    
    def get_user_input(self):
        """Get behavioral data input from user via Streamlit widgets"""
        st.markdown("### 📝 Enter Behavioral Data")
        st.markdown("Please enter the following behavioral measurements from cognitive tasks:")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        user_data = {}
        trial_types = ['0back', '3back', '5back', '6back']
        
        for i, trial in enumerate(trial_types):
            with col1 if i % 2 == 0 else col2:
                st.markdown(f"#### {trial.upper()} Trial")
                
                with st.expander(f"📊 {trial} Measurements", expanded=True):
                    # Input validation
                    response_time = st.number_input(
                        f"Average response time (ms)",
                        min_value=100.0,
                        max_value=5000.0,
                        value=1000.0,
                        step=50.0,
                        key=f"{trial}_response_time"
                    )
                    
                    accuracy = st.number_input(
                        f"Accuracy (0-1)",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.8,
                        step=0.01,
                        key=f"{trial}_accuracy"
                    )
                    
                    variability = st.number_input(
                        f"Response variability (std dev)",
                        min_value=0.0,
                        max_value=1000.0,
                        value=200.0,
                        step=10.0,
                        key=f"{trial}_variability"
                    )
                    
                    # Calculate derived features
                    user_data[f'{trial}_mean'] = response_time
                    user_data[f'{trial}_std'] = variability
                    user_data[f'{trial}_min'] = max(0, response_time - (variability * 2))
                    user_data[f'{trial}_max'] = response_time + (variability * 2)
                    user_data[f'{trial}_median'] = response_time
                    user_data[f'{trial}_skew'] = 0.0
                    user_data[f'{trial}_kurt'] = 0.0
                    user_data[f'{trial}_range'] = user_data[f'{trial}_max'] - user_data[f'{trial}_min']
        
        return user_data
    
    def create_feature_vector(self, user_data):
        """Create feature vector matching the trained model's expected format"""
        if not self.feature_columns:
            return None
        
        feature_vector = []
        for feature_name in self.feature_columns:
            if feature_name in user_data:
                feature_vector.append(user_data[feature_name])
            else:
                feature_vector.append(0.0)
        
        return np.array(feature_vector)
    
    def make_prediction(self, feature_vector):
        """Make prediction using the trained model"""
        if not self.model_trained or not self.predictor:
            return None, None
        
        try:
            prediction, probability = self.predictor.predict_single_sample(feature_vector)
            fatigue_level = "High Decision Fatigue" if prediction == 1 else "Low Decision Fatigue"
            confidence = max(probability) if probability is not None else None
            return fatigue_level, confidence
        except Exception as e:
            st.error(f"Error making prediction: {e}")
            return None, None
    
    def display_results(self, fatigue_level, confidence):
        """Display prediction results with visualizations"""
        st.markdown("---")
        st.markdown("### 🎯 Prediction Results")
        
        # Create prediction card
        if "High" in fatigue_level:
            st.markdown(f"""
            <div class="prediction-card">
                <h2>⚠️ {fatigue_level}</h2>
                <p>Confidence: {confidence:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="prediction-card" style="background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);">
                <h2>✅ {fatigue_level}</h2>
                <p>Confidence: {confidence:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Confidence gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = confidence * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Score (%)"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("### 📋 Recommendations")
        
        if "High" in fatigue_level:
            st.markdown("""
            <div class="warning-box">
                <h4>⚠️ High Fatigue Detected</h4>
                <ul>
                    <li>Consider taking a break from decision-making tasks</li>
                    <li>Try relaxation techniques or stress reduction</li>
                    <li>Stay hydrated and ensure proper nutrition</li>
                    <li>Consider rest before important decisions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-box">
                <h4>✅ Fatigue Level Manageable</h4>
                <ul>
                    <li>Current fatigue level appears manageable</li>
                    <li>Continue monitoring during extended tasks</li>
                    <li>Consider regular breaks to maintain performance</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def display_model_info(self):
        """Display model information and statistics"""
        st.markdown("### 🤖 Model Information")
        
        if not self.model_trained:
            st.warning("Model not trained yet.")
            return
        
        # Model performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Best Model", self.predictor.best_model_name)
        
        with col2:
            st.metric("Test Accuracy", f"{self.test_accuracy:.4f}")
        
        with col3:
            st.metric("Features", len(self.feature_columns))
        
        with col4:
            st.metric("Target", "Fatigue Level")
        
        # Model comparison chart
        st.markdown("#### 📊 Model Performance Comparison")
        
        fig = px.bar(
            self.model_comparison,
            x='Model',
            y=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            title="Model Performance Metrics",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance
        if hasattr(self.predictor.best_model, 'coef_'):
            st.markdown("#### 🔍 Top Features")
            
            coef = np.abs(self.predictor.best_model.coef_[0])
            feature_importance = list(zip(self.feature_columns, coef))
            feature_importance.sort(key=lambda x: x[1], reverse=True)
            
            # Create feature importance dataframe
            feature_df = pd.DataFrame(feature_importance[:10], columns=['Feature', 'Importance'])
            
            fig = px.bar(
                feature_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title="Top 10 Most Important Features"
            )
            st.plotly_chart(fig, use_container_width=True)

def main():
    """Main Streamlit application"""
    st.markdown('<h1 class="main-header">🧠 Decision Fatigue Prediction System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This system predicts human decision fatigue based on behavioral data from cognitive tasks.
    Enter your behavioral measurements below to get a fatigue prediction with confidence score.
    """)
    
    # Initialize the UI system
    if 'ui_system' not in st.session_state:
        st.session_state.ui_system = StreamlitDecisionFatigueUI()
    
    ui_system = st.session_state.ui_system
    
    # Initialize model (show progress)
    if not ui_system.model_trained:
        with st.spinner("🤖 Training ML models... This may take a moment..."):
            if ui_system.initialize_model():
                st.success("✅ Models trained successfully!")
            else:
                st.error("❌ Failed to train models. Please check your data.")
                return
    
    # Sidebar navigation
    st.sidebar.title("🎮 Navigation")
    page = st.sidebar.radio("Choose a page:", ["📊 Prediction", "🤖 Model Info", "📚 About"])
    
    if page == "📊 Prediction":
        # Get user input
        user_data = ui_system.get_user_input()
        
        # Prediction button
        if st.button("🎯 Make Prediction", type="primary", use_container_width=True):
            if user_data:
                with st.spinner("🔄 Analyzing data..."):
                    # Create feature vector
                    feature_vector = ui_system.create_feature_vector(user_data)
                    
                    if feature_vector is not None:
                        # Make prediction
                        fatigue_level, confidence = ui_system.make_prediction(feature_vector)
                        
                        if fatigue_level is not None:
                            ui_system.display_results(fatigue_level, confidence)
    
    elif page == "🤖 Model Info":
        ui_system.display_model_info()
    
    elif page == "📚 About":
        st.markdown("### 📚 About This System")
        st.markdown("""
        #### 🧠 What is Decision Fatigue?
        Decision fatigue refers to the deteriorating quality of decisions made by an individual after a long session of decision making.
        
        #### 🔬 How This System Works
        1. **Data Collection**: Behavioral data from cognitive tasks (0-back, 3-back, 5-back, 6-back)
        2. **Feature Extraction**: Statistical features (mean, std, min, max, etc.) are computed
        3. **Machine Learning**: Multiple ML models are trained and the best performer is selected
        4. **Prediction**: New behavioral data is analyzed to predict fatigue level
        
        #### 📊 Model Performance
        - **Dataset**: 44 subjects (22 high fatigue, 22 low fatigue)
        - **Features**: 32 statistical features extracted from time series data
        - **Models**: Logistic Regression, Random Forest, Support Vector Machine
        - **Best Performance**: 100% accuracy on test set
        
        #### 🎯 Applications
        - Real-time fatigue monitoring in high-stakes environments
        - Non-invasive behavioral assessment
        - Decision support systems
        - Workplace safety and productivity optimization
        """)
        
        st.markdown("---")
        st.markdown("### 📞 Contact & Support")
        st.markdown("""
        For questions about this system or to report issues, please refer to the project documentation.
        """)

if __name__ == "__main__":
    main()
