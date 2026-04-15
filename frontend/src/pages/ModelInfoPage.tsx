import React, { useState, useEffect } from 'react';
import { Brain, BarChart3, Target, TrendingUp, Loader2 } from 'lucide-react';
import { getModelInfo, getModelMetrics, getFeatureImportance } from '../services/api';
import ModelPerformanceChart from '../components/ModelPerformanceChart';
import FeatureImportanceChart from '../components/FeatureImportanceChart';

interface ModelInfo {
  best_model: string;
  test_accuracy: number;
  feature_count: number;
  target: string;
}

interface ModelMetrics {
  model_comparison: Array<{
    Model: string;
    Accuracy: number;
    Precision: number;
    Recall: number;
    'F1-Score': number;
  }>;
}

interface FeatureData {
  features: Array<{
    feature: string;
    importance: number;
  }>;
}

const ModelInfoPage: React.FC = () => {
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [modelMetrics, setModelMetrics] = useState<ModelMetrics | null>(null);
  const [featureData, setFeatureData] = useState<FeatureData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [info, metrics, features] = await Promise.all([
          getModelInfo(),
          getModelMetrics(),
          getFeatureImportance()
        ]);
        
        setModelInfo(info);
        setModelMetrics(metrics);
        setFeatureData(features);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load model information');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading model information...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="card-body">
          <div className="p-4 bg-danger-50 border border-danger-200 rounded-md">
            <p className="text-danger-800">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <Brain className="h-12 w-12 text-primary-600 mr-3" />
          <h1 className="text-4xl font-bold text-gray-900">
            Model Information
          </h1>
        </div>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Detailed information about the machine learning models used for decision fatigue prediction.
        </p>
      </div>

      {/* Key Metrics */}
      {modelInfo && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Best Model</p>
                <p className="text-2xl font-bold text-gray-900">{modelInfo.best_model}</p>
              </div>
              <Brain className="h-8 w-8 text-primary-600" />
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Test Accuracy</p>
                <p className="text-2xl font-bold text-gray-900">{(modelInfo.test_accuracy * 100).toFixed(1)}%</p>
              </div>
              <Target className="h-8 w-8 text-success-600" />
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Features</p>
                <p className="text-2xl font-bold text-gray-900">{modelInfo.feature_count}</p>
              </div>
              <BarChart3 className="h-8 w-8 text-warning-600" />
            </div>
          </div>
          
          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Target</p>
                <p className="text-2xl font-bold text-gray-900">{modelInfo.target}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-primary-600" />
            </div>
          </div>
        </div>
      )}

      {/* Model Performance Comparison */}
      {modelMetrics && (
        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <BarChart3 className="h-5 w-5 mr-2 text-primary-600" />
              Model Performance Comparison
            </h2>
          </div>
          <div className="card-body">
            <ModelPerformanceChart data={modelMetrics.model_comparison} />
          </div>
        </div>
      )}

      {/* Feature Importance */}
      {featureData && (
        <div className="card">
          <div className="card-header">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-primary-600" />
              Top 10 Most Important Features
            </h2>
          </div>
          <div className="card-body">
            <FeatureImportanceChart data={featureData.features} />
          </div>
        </div>
      )}

      {/* Model Details */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900">Model Details</h2>
        </div>
        <div className="card-body space-y-4">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Dataset Information</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• <strong>Dataset:</strong> 44 subjects (22 high fatigue, 22 low fatigue)</li>
              <li>• <strong>Features:</strong> 32 statistical features extracted from time series data</li>
              <li>• <strong>Models:</strong> Logistic Regression, Random Forest, Support Vector Machine</li>
              <li>• <strong>Validation:</strong> 80/20 train-test split with stratified sampling</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Feature Engineering</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• <strong>Response Time Features:</strong> Mean, std, min, max, median, skewness, kurtosis, range</li>
              <li>• <strong>Trial Types:</strong> 0-back, 3-back, 5-back, 6-back cognitive tasks</li>
              <li>• <strong>Statistical Features:</strong> 8 features per trial type × 4 trials = 32 total features</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Model Selection</h3>
            <p className="text-sm text-gray-600">
              The best performing model is selected based on F1-score weighted average. 
              All models are trained with standardized features and hyperparameter tuning to ensure optimal performance.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelInfoPage;
