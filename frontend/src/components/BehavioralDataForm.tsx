import React, { useState } from 'react';
import { BarChart3, Loader2, Brain } from 'lucide-react';
import DataSimulator from './DataSimulator';

interface TrialData {
  response_time: number;
  accuracy: number;
  variability: number;
}

interface BehavioralData {
  '0back': TrialData;
  '3back': TrialData;
  '5back': TrialData;
  '6back': TrialData;
}

interface BehavioralDataFormProps {
  onSubmit: (data: any) => void;
  isLoading: boolean;
}

const BehavioralDataForm: React.FC<BehavioralDataFormProps> = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState<BehavioralData>({
    '0back': { response_time: 1000, accuracy: 0.85, variability: 150 },
    '3back': { response_time: 1200, accuracy: 0.80, variability: 200 },
    '5back': { response_time: 1400, accuracy: 0.75, variability: 250 },
    '6back': { response_time: 1600, accuracy: 0.70, variability: 300 },
  });
  
  const [showSimulator, setShowSimulator] = useState(false);
  const [currentSimulatorTrial, setCurrentSimulatorTrial] = useState<'0back' | '3back' | '5back' | '6back'>('0back');

  // Handle data from simulator
  const handleSimulatorData = (trial: '0back' | '3back' | '5back' | '6back') => (data: { response_time: number; accuracy: number; variability: number }) => {
    setFormData(prev => ({
      ...prev,
      [trial]: data
    }));
  };

  // Generate realistic data for all trials
  const generateRealisticData = (fatigueLevel: 'low' | 'high') => {
    const baseData = {
      low: {
        '0back': { response_time: 850, accuracy: 0.92, variability: 120 },
        '3back': { response_time: 1100, accuracy: 0.85, variability: 180 },
        '5back': { response_time: 1400, accuracy: 0.78, variability: 250 },
        '6back': { response_time: 1800, accuracy: 0.70, variability: 320 },
      },
      high: {
        '0back': { response_time: 1200, accuracy: 0.80, variability: 250 },
        '3back': { response_time: 1600, accuracy: 0.65, variability: 350 },
        '5back': { response_time: 2100, accuracy: 0.55, variability: 450 },
        '6back': { response_time: 2800, accuracy: 0.40, variability: 600 },
      }
    };

    // Add some random variation
    const addVariation = (data: any) => {
      return Object.keys(data).reduce((acc, key) => {
        const trial = key as keyof BehavioralData;
        acc[trial] = {
          response_time: Math.round(data[trial].response_time + (Math.random() - 0.5) * 200),
          accuracy: Math.max(0.1, Math.min(1.0, data[trial].accuracy + (Math.random() - 0.5) * 0.1)),
          variability: Math.round(data[trial].variability + (Math.random() - 0.5) * 50)
        };
        return acc;
      }, {} as BehavioralData);
    };

    setFormData(addVariation(baseData[fatigueLevel]));
  };

  const trialTypes = ['0back', '3back', '5back', '6back'] as const;

  const handleInputChange = (trial: keyof BehavioralData, field: keyof TrialData, value: string) => {
    const numValue = parseFloat(value);
    if (!isNaN(numValue)) {
      setFormData(prev => ({
        ...prev,
        [trial]: {
          ...prev[trial],
          [field]: numValue
        }
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Transform data to match backend expectations (32 features)
    const transformedData = {
      behavioral_data: {
        // 0-back features
        '0back_mean': formData['0back'].response_time,
        '0back_std': formData['0back'].variability,
        '0back_min': Math.max(0, formData['0back'].response_time - (formData['0back'].variability * 2)),
        '0back_max': formData['0back'].response_time + (formData['0back'].variability * 2),
        '0back_median': formData['0back'].response_time,
        '0back_skew': 0.0,
        '0back_kurt': 0.0,
        '0back_range': formData['0back'].response_time + (formData['0back'].variability * 2) - Math.max(0, formData['0back'].response_time - (formData['0back'].variability * 2)),
        
        // 3-back features
        '3back_mean': formData['3back'].response_time,
        '3back_std': formData['3back'].variability,
        '3back_min': Math.max(0, formData['3back'].response_time - (formData['3back'].variability * 2)),
        '3back_max': formData['3back'].response_time + (formData['3back'].variability * 2),
        '3back_median': formData['3back'].response_time,
        '3back_skew': 0.0,
        '3back_kurt': 0.0,
        '3back_range': formData['3back'].response_time + (formData['3back'].variability * 2) - Math.max(0, formData['3back'].response_time - (formData['3back'].variability * 2)),
        
        // 5-back features
        '5back_mean': formData['5back'].response_time,
        '5back_std': formData['5back'].variability,
        '5back_min': Math.max(0, formData['5back'].response_time - (formData['5back'].variability * 2)),
        '5back_max': formData['5back'].response_time + (formData['5back'].variability * 2),
        '5back_median': formData['5back'].response_time,
        '5back_skew': 0.0,
        '5back_kurt': 0.0,
        '5back_range': formData['5back'].response_time + (formData['5back'].variability * 2) - Math.max(0, formData['5back'].response_time - (formData['5back'].variability * 2)),
        
        // 6-back features
        '6back_mean': formData['6back'].response_time,
        '6back_std': formData['6back'].variability,
        '6back_min': Math.max(0, formData['6back'].response_time - (formData['6back'].variability * 2)),
        '6back_max': formData['6back'].response_time + (formData['6back'].variability * 2),
        '6back_median': formData['6back'].response_time,
        '6back_skew': 0.0,
        '6back_kurt': 0.0,
        '6back_range': formData['6back'].response_time + (formData['6back'].variability * 2) - Math.max(0, formData['6back'].response_time - (formData['6back'].variability * 2)),
      }
    };
    
    console.log('Sending data:', transformedData);
    onSubmit(transformedData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Data Generation Section */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Brain className="h-5 w-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Data Generation</h3>
          </div>
          <button
            type="button"
            onClick={() => setShowSimulator(!showSimulator)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            {showSimulator ? 'Hide Simulator' : 'Show Simulator'}
          </button>
        </div>
        
        <div className="flex flex-wrap gap-3 mb-4">
          <button
            type="button"
            onClick={() => generateRealisticData('low')}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
          >
            Generate Low Fatigue Data
          </button>
          <button
            type="button"
            onClick={() => generateRealisticData('high')}
            className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 text-sm"
          >
            Generate High Fatigue Data
          </button>
          <button
            type="button"
            onClick={() => setShowSimulator(!showSimulator)}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
          >
            Interactive Simulator
          </button>
        </div>
        
        <div className="text-sm text-gray-600">
          <p>Quickly generate realistic behavioral data or use the interactive simulator to run cognitive tasks.</p>
        </div>
      </div>

      {/* Interactive Simulator */}
      {showSimulator && (
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Trial Type for Simulation
            </label>
            <div className="flex space-x-2">
              {(['0back', '3back', '5back', '6back'] as const).map((trial) => (
                <button
                  key={trial}
                  type="button"
                  onClick={() => setCurrentSimulatorTrial(trial)}
                  className={`px-3 py-1 rounded-lg text-sm ${
                    currentSimulatorTrial === trial
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {trial}
                </button>
              ))}
            </div>
          </div>
          
          <DataSimulator 
            trialType={currentSimulatorTrial}
            onDataGenerated={handleSimulatorData(currentSimulatorTrial)} 
          />
        </div>
      )}

      {/* Manual Input Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {trialTypes.map((trial) => (
          <div key={trial} className="space-y-4">
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-primary-600" />
              <h3 className="text-lg font-semibold text-gray-900">
                {trial.toUpperCase()} Trial
              </h3>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Accuracy (0-1)
              </label>
              <input
                type="number"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., 0.8"
                value={formData[trial].accuracy}
                onChange={(e) => handleInputChange(trial, 'accuracy', e.target.value)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Response Variability (std dev)
              </label>
              <input
                type="number"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., 200"
                value={formData[trial].variability}
                onChange={(e) => handleInputChange(trial, 'variability', e.target.value)}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-center pt-6 border-t border-gray-200">
        <button
          type="submit"
          disabled={isLoading}
          className="btn btn-primary w-full py-3 text-lg font-medium flex items-center justify-center space-x-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <BarChart3 className="h-5 w-5" />
              <span>Make Prediction</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default BehavioralDataForm;
