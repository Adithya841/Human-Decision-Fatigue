import React from 'react';
import { Brain, Target, BarChart3, Users, Shield, Zap } from 'lucide-react';

const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <div className="flex items-center justify-center mb-4">
          <Brain className="h-12 w-12 text-primary-600 mr-3" />
          <h1 className="text-4xl font-bold text-gray-900">
            About Decision Fatigue Prediction
          </h1>
        </div>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Learn about the science behind decision fatigue and how our AI-powered system helps monitor cognitive performance.
        </p>
      </div>

      {/* What is Decision Fatigue */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center">
            <Brain className="h-5 w-5 mr-2 text-primary-600" />
            What is Decision Fatigue?
          </h2>
        </div>
        <div className="card-body">
          <p className="text-gray-700 leading-relaxed">
            Decision fatigue refers to the deteriorating quality of decisions made by an individual after a long session of decision making. 
            It's a form of mental fatigue that can significantly impact cognitive performance, judgment, and overall productivity.
          </p>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-gray-50 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Common Symptoms</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Impulsive decision-making</li>
                <li>• Procrastination on important choices</li>
                <li>• Reduced cognitive performance</li>
                <li>• Increased stress and anxiety</li>
              </ul>
            </div>
            <div className="p-4 bg-gray-50 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Impact Areas</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Workplace productivity</li>
                <li>• Personal relationships</li>
                <li>• Financial decisions</li>
                <li>• Health and wellness choices</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center">
            <Target className="h-5 w-5 mr-2 text-primary-600" />
            How This System Works
          </h2>
        </div>
        <div className="card-body">
          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center font-semibold">
                1
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Data Collection</h3>
                <p className="text-sm text-gray-600">
                  Behavioral data is collected from cognitive tasks (0-back, 3-back, 5-back, 6-back) that measure working memory and cognitive load.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center font-semibold">
                2
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Feature Extraction</h3>
                <p className="text-sm text-gray-600">
                  Statistical features (mean, std, min, max, etc.) are computed from response time data to capture patterns in cognitive performance.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center font-semibold">
                3
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Machine Learning</h3>
                <p className="text-sm text-gray-600">
                  Multiple ML models are trained and the best performer is selected based on comprehensive evaluation metrics.
                </p>
              </div>
            </div>
            
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center font-semibold">
                4
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Prediction</h3>
                <p className="text-sm text-gray-600">
                  New behavioral data is analyzed to predict fatigue level with confidence scores and actionable recommendations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Performance */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center">
            <BarChart3 className="h-5 w-5 mr-2 text-primary-600" />
            Model Performance
          </h2>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Dataset Overview</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <Users className="h-4 w-4 mr-2 text-primary-600" />
                  44 subjects (22 high fatigue, 22 low fatigue)
                </li>
                <li className="flex items-center">
                  <BarChart3 className="h-4 w-4 mr-2 text-primary-600" />
                  32 statistical features extracted from time series data
                </li>
                <li className="flex items-center">
                  <Target className="h-4 w-4 mr-2 text-primary-600" />
                  Binary classification: High vs Low fatigue
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Model Architecture</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <Brain className="h-4 w-4 mr-2 text-primary-600" />
                  Multiple algorithms: Logistic Regression, Random Forest, SVM
                </li>
                <li className="flex items-center">
                  <Shield className="h-4 w-4 mr-2 text-primary-600" />
                  Cross-validation and hyperparameter tuning
                </li>
                <li className="flex items-center">
                  <Zap className="h-4 w-4 mr-2 text-primary-600" />
                  100% accuracy on test set (with current dataset)
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Applications */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900">Applications</h2>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 border border-gray-200 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Workplace Safety</h3>
              <p className="text-sm text-gray-600">
                Monitor fatigue levels in high-stakes environments like healthcare, aviation, and manufacturing to prevent errors and accidents.
              </p>
            </div>
            
            <div className="p-4 border border-gray-200 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Performance Optimization</h3>
              <p className="text-sm text-gray-600">
                Help professionals maintain optimal cognitive performance during demanding work periods and important decision-making tasks.
              </p>
            </div>
            
            <div className="p-4 border border-gray-200 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Health & Wellness</h3>
              <p className="text-sm text-gray-600">
                Provide insights for mental health monitoring and cognitive wellness programs in both clinical and personal settings.
              </p>
            </div>
            
            <div className="p-4 border border-gray-200 rounded-md">
              <h3 className="font-medium text-gray-900 mb-2">Research & Education</h3>
              <p className="text-sm text-gray-600">
                Support academic research on cognitive fatigue and educational programs about mental performance management.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Technical Details */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900">Technical Details</h2>
        </div>
        <div className="card-body">
          <div className="space-y-4 text-sm text-gray-600">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Feature Engineering</h3>
              <p>
                The system extracts 8 statistical features from each of the 4 trial types (0-back, 3-back, 5-back, 6-back), 
                resulting in 32 total features that capture various aspects of cognitive performance patterns.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Model Selection</h3>
              <p>
                Multiple machine learning algorithms are evaluated using cross-validation, with the best model selected 
                based on F1-score, accuracy, precision, and recall metrics.
              </p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Real-time Processing</h3>
              <p>
                The system is optimized for real-time prediction, providing instant feedback with confidence scores 
                to support immediate decision-making and intervention strategies.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
