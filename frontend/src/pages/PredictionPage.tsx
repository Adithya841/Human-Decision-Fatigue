import React, { useState } from 'react';
import { Brain, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import BehavioralDataForm from '../components/BehavioralDataForm';
import PredictionResults from '../components/PredictionResults';
import { predictFatigue } from '../services/api';

interface PredictionData {
  fatigue_level: string;
  confidence: number;
}

const PredictionPage: React.FC = () => {
  const [isPredicting, setIsPredicting] = useState(false);
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = async (behavioralData: any) => {
    setIsPredicting(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await predictFatigue(behavioralData);
      setPrediction(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
    } finally {
      setIsPredicting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <Brain className="h-12 w-12 text-primary-600 mr-3" />
          <h1 className="text-4xl font-bold text-gray-900">
            Decision Fatigue Prediction
          </h1>
        </div>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Enter your behavioral data from cognitive tasks to get an AI-powered prediction 
          of your current decision fatigue level.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="card">
            <div className="card-header">
              <h2 className="text-xl font-semibold text-gray-900">
                Behavioral Data Input
              </h2>
            </div>
            <div className="card-body">
              <BehavioralDataForm 
                onSubmit={handlePrediction}
                isLoading={isPredicting}
              />
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {isPredicting && (
            <div className="card">
              <div className="card-body flex items-center justify-center py-12">
                <div className="text-center">
                  <Loader2 className="h-8 w-8 animate-spin text-primary-600 mx-auto mb-4" />
                  <p className="text-gray-600">Analyzing your behavioral data...</p>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="card">
              <div className="card-body">
                <div className="flex items-center p-4 bg-danger-50 border border-danger-200 rounded-md">
                  <AlertTriangle className="h-5 w-5 text-danger-600 mr-3 flex-shrink-0" />
                  <div>
                    <h3 className="text-sm font-medium text-danger-800">
                      Prediction Error
                    </h3>
                    <p className="text-sm text-danger-700 mt-1">{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {prediction && !isPredicting && (
            <PredictionResults prediction={prediction} />
          )}

          {!prediction && !isPredicting && !error && (
            <div className="card">
              <div className="card-body">
                <div className="text-center py-8">
                  <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Ready for Prediction
                  </h3>
                  <p className="text-gray-600">
                    Enter your behavioral data and click "Make Prediction" to get started.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictionPage;
