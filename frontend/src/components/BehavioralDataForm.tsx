import React, { useState } from 'react';
import { Loader2, BarChart3 } from 'lucide-react';

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
    '0back': { response_time: 1000, accuracy: 0.8, variability: 200 },
    '3back': { response_time: 1200, accuracy: 0.75, variability: 250 },
    '5back': { response_time: 1500, accuracy: 0.7, variability: 300 },
    '6back': { response_time: 1800, accuracy: 0.65, variability: 350 }
  });

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
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {trialTypes.map((trial) => (
          <div key={trial} className="space-y-4">
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5 text-primary-600" />
              <h3 className="text-lg font-semibold text-gray-900">
                {trial.toUpperCase()} Trial
              </h3>
            </div>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Average Response Time (ms)
                </label>
                <input
                  type="number"
                  min="100"
                  max="5000"
                  step="50"
                  value={formData[trial].response_time}
                  onChange={(e) => handleInputChange(trial, 'response_time', e.target.value)}
                  className="input-field"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Accuracy (0-1)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  value={formData[trial].accuracy}
                  onChange={(e) => handleInputChange(trial, 'accuracy', e.target.value)}
                  className="input-field"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Response Variability (std dev)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1000"
                  step="10"
                  value={formData[trial].variability}
                  onChange={(e) => handleInputChange(trial, 'variability', e.target.value)}
                  className="input-field"
                  required
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="pt-6 border-t border-gray-200">
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
