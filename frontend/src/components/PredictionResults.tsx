import React from 'react';
import { AlertTriangle, CheckCircle, TrendingUp, Brain } from 'lucide-react';

interface PredictionData {
  fatigue_level: string;
  confidence: number;
}

interface PredictionResultsProps {
  prediction: PredictionData;
}

const PredictionResults: React.FC<PredictionResultsProps> = ({ prediction }) => {
  const isHighFatigue = prediction.fatigue_level.includes('High');
  const confidencePercentage = (prediction.confidence * 100).toFixed(1);

  const getRecommendations = () => {
    if (isHighFatigue) {
      return [
        'Consider taking a break from decision-making tasks',
        'Try relaxation techniques or stress reduction',
        'Stay hydrated and ensure proper nutrition',
        'Consider rest before important decisions'
      ];
    } else {
      return [
        'Current fatigue level appears manageable',
        'Continue monitoring during extended tasks',
        'Consider regular breaks to maintain performance'
      ];
    }
  };

  return (
    <div className="space-y-6">
      {/* Prediction Card */}
      <div className={`prediction-card-${isHighFatigue ? 'high' : 'low'}`}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            {isHighFatigue ? (
              <AlertTriangle className="h-8 w-8" />
            ) : (
              <CheckCircle className="h-8 w-8" />
            )}
            <h2 className="text-2xl font-bold">
              {prediction.fatigue_level}
            </h2>
          </div>
          <div className="text-right">
            <div className="text-sm opacity-90">Confidence</div>
            <div className="text-3xl font-bold">{confidencePercentage}%</div>
          </div>
        </div>
      </div>

      {/* Confidence Gauge */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2 text-primary-600" />
            Confidence Score
          </h3>
        </div>
        <div className="card-body">
          <div className="relative">
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className={`h-4 rounded-full transition-all duration-500 ${
                  prediction.confidence >= 0.8
                    ? 'bg-success-500'
                    : prediction.confidence >= 0.6
                    ? 'bg-warning-500'
                    : 'bg-danger-500'
                }`}
                style={{ width: `${prediction.confidence * 100}%` }}
              />
            </div>
            <div className="flex justify-between mt-2 text-xs text-gray-600">
              <span>0%</span>
              <span>50%</span>
              <span>80%</span>
              <span>100%</span>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-3">
            Model confidence: {confidencePercentage}% - This indicates how certain the ML model is about this prediction.
          </p>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Brain className="h-5 w-5 mr-2 text-primary-600" />
            Recommendations
          </h3>
        </div>
        <div className="card-body">
          <div className={`p-4 rounded-md ${
            isHighFatigue 
              ? 'bg-warning-50 border border-warning-200' 
              : 'bg-success-50 border border-success-200'
          }`}>
            <h4 className={`font-medium mb-3 ${
              isHighFatigue ? 'text-warning-800' : 'text-success-800'
            }`}>
              {isHighFatigue ? '⚠️ High Fatigue Detected' : '✅ Fatigue Level Manageable'}
            </h4>
            <ul className="space-y-2">
              {getRecommendations().map((recommendation, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-primary-600 mr-2 mt-1">•</span>
                  <span className="text-sm text-gray-700">{recommendation}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Model Info */}
      <div className="card">
        <div className="card-body">
          <div className="text-center text-sm text-gray-500">
            <p>This prediction was generated using machine learning models trained on behavioral data from cognitive tasks.</p>
            <p className="mt-1">The system analyzes response patterns across different difficulty levels to assess decision fatigue.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionResults;
