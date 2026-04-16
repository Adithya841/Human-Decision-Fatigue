import React, { useState, useEffect, useCallback } from 'react';
import { Play, Pause, RotateCcw, MousePointer, Timer } from 'lucide-react';

interface InteractiveNBackSimulatorProps {
  trialType: '0back' | '3back' | '5back' | '6back';
  onDataGenerated: (data: { response_time: number; accuracy: number; variability: number }) => void;
}

const InteractiveNBackSimulator: React.FC<InteractiveNBackSimulatorProps> = ({ 
  trialType, 
  onDataGenerated 
}) => {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStimulus, setCurrentStimulus] = useState('');
  const [stimulusHistory, setStimulusHistory] = useState<string[]>([]);
  const [userResponses, setUserResponses] = useState<boolean[]>([]);
  const [correctResponses, setCorrectResponses] = useState<boolean[]>([]);
  const [responseTimes, setResponseTimes] = useState<number[]>([]);
  const [currentTrialIndex, setCurrentTrialIndex] = useState(0);
  const [showFeedback, setShowFeedback] = useState<'correct' | 'incorrect' | null>(null);
  const [timeRemaining, setTimeRemaining] = useState(1000);
  const [totalTrials, setTotalTrials] = useState(20);

  const stimuli = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
  const n = parseInt(trialType.replace('back', ''));

  const generateStimulus = useCallback(() => {
    return stimuli[Math.floor(Math.random() * stimuli.length)];
  }, []);

  const shouldRespond = useCallback((history: string[], currentIndex: number) => {
    if (n === 0) {
      return history[currentIndex] === 'X'; // 0-back: respond to 'X'
    }
    if (currentIndex < n) return false;
    return history[currentIndex] === history[currentIndex - n]; // n-back: check n steps back
  }, [n]);

  const handleUserClick = useCallback(() => {
    if (!isRunning || currentTrialIndex === 0) return;

    const shouldHaveResponded = shouldRespond(stimulusHistory, currentTrialIndex - 1);
    const responseTime = 1000 - timeRemaining; // Time since stimulus appeared
    
    setUserResponses(prev => [...prev, true]);
    setCorrectResponses(prev => [...prev, shouldHaveResponded]);
    setResponseTimes(prev => [...prev, responseTime]);
    
    setShowFeedback(shouldHaveResponded ? 'correct' : 'incorrect');
    setTimeout(() => setShowFeedback(null), 500);
  }, [isRunning, currentTrialIndex, stimulusHistory, shouldRespond, timeRemaining]);

  const startSimulation = () => {
    setIsRunning(true);
    setCurrentTrialIndex(0);
    setStimulusHistory([]);
    setUserResponses([]);
    setCorrectResponses([]);
    setResponseTimes([]);
    setCurrentStimulus('');
    setTimeRemaining(1000);
  };

  const resetSimulation = () => {
    setIsRunning(false);
    setCurrentTrialIndex(0);
    setStimulusHistory([]);
    setUserResponses([]);
    setCorrectResponses([]);
    setResponseTimes([]);
    setCurrentStimulus('');
    setShowFeedback(null);
    setTimeRemaining(1000);
  };

  // Timer for stimulus display
  useEffect(() => {
    if (!isRunning) return;

    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 100) {
          return 1000; // Reset for next stimulus
        }
        return prev - 100;
      });
    }, 100);

    return () => clearInterval(timer);
  }, [isRunning]);

  // Handle stimulus progression
  useEffect(() => {
    if (!isRunning) return;
    if (timeRemaining !== 1000) return; // Only change stimulus at the start of each trial

    if (currentTrialIndex >= totalTrials) {
      // Simulation complete - calculate results
      const avgResponseTime = responseTimes.length > 0 
        ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length 
        : 1500;
      
      const accuracy = correctResponses.length > 0
        ? correctResponses.filter(r => r).length / correctResponses.length
        : 0.5;
      
      const variability = responseTimes.length > 1
        ? Math.sqrt(responseTimes.reduce((sq, n) => sq + Math.pow(n - avgResponseTime, 2), 0) / responseTimes.length)
        : 200;

      onDataGenerated({
        response_time: Math.round(avgResponseTime),
        accuracy: parseFloat(accuracy.toFixed(2)),
        variability: Math.round(variability)
      });

      setIsRunning(false);
      return;
    }

    // Generate new stimulus
    const newStimulus = n === 0 && currentTrialIndex > 0 && Math.random() > 0.8 
      ? 'X' // 0-back: occasionally show target
      : generateStimulus();

    const newHistory = [...stimulusHistory, newStimulus];
    setStimulusHistory(newHistory);
    setCurrentStimulus(newStimulus);
    setCurrentTrialIndex(prev => prev + 1);

    // Auto-handle no-response cases
    if (currentTrialIndex > 0) {
      const shouldHaveResponded = shouldRespond(newHistory, currentTrialIndex - 1);
      if (shouldHaveResponded) {
        // User should have clicked but didn't
        setUserResponses(prev => [...prev, false]);
        setCorrectResponses(prev => [...prev, false]);
        setResponseTimes(prev => [...prev, 1000]); // Max time for missed response
      }
    }

  }, [isRunning, timeRemaining, currentTrialIndex, totalTrials, stimulusHistory, generateStimulus, shouldRespond, n, responseTimes, onDataGenerated]);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4">Interactive N-Back Task Simulator</h3>
      
      <div className="mb-4">
        <div className="text-center mb-4">
          <div className={`text-6xl font-bold mb-2 transition-all duration-200 ${
            showFeedback === 'correct' ? 'text-green-600' : 
            showFeedback === 'incorrect' ? 'text-red-600' : 
            'text-primary-600'
          }`}>
            {currentStimulus || '-'}
          </div>
          
          <div className="text-sm text-gray-600 mb-2">
            {trialType.toUpperCase()} - Click if this matches {n === 0 ? 'the letter X' : `the letter from ${n} steps back`}
          </div>
          
          <div className="flex items-center justify-center space-x-2 mb-2">
            <Timer className="h-4 w-4 text-gray-500" />
            <div className="text-sm font-mono">
              Time: {(timeRemaining / 1000).toFixed(1)}s
            </div>
          </div>
          
          <div className="text-xs text-gray-500">
            Trial {currentTrialIndex} / {totalTrials}
          </div>
        </div>

        {/* Stimulus History */}
        {stimulusHistory.length > 0 && (
          <div className="mb-4 p-3 bg-gray-50 rounded">
            <div className="text-xs text-gray-600 mb-1">History (newest first):</div>
            <div className="flex flex-wrap gap-1 justify-center">
              {stimulusHistory.slice(-10).reverse().map((stimulus, idx) => (
                <span 
                  key={idx}
                  className={`px-2 py-1 text-xs rounded ${
                    idx === 0 ? 'bg-blue-100 text-blue-800 font-bold' : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {stimulus}
                </span>
              ))}
            </div>
            {n > 0 && stimulusHistory.length > n && (
              <div className="text-xs text-center mt-1 text-gray-500">
                Compare current (blue) with position {n} back
              </div>
            )}
          </div>
        )}
        
        <div className="flex justify-center space-x-4 mb-4">
          {!isRunning ? (
            <button
              onClick={startSimulation}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              <Play className="h-4 w-4" />
              <span>Start Simulation</span>
            </button>
          ) : (
            <button
              onClick={handleUserClick}
              disabled={currentTrialIndex === 0}
              className="flex items-center space-x-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              <MousePointer className="h-5 w-5" />
              <span>CLICK TO RESPOND</span>
            </button>
          )}
          
          <button
            onClick={resetSimulation}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
          >
            <RotateCcw className="h-4 w-4" />
            <span>Reset</span>
          </button>
        </div>
        
        {responseTimes.length > 0 && (
          <div className="mt-4 p-4 bg-gray-50 rounded">
            <div className="text-sm text-gray-600">
              <div>Responses: {userResponses.filter(r => r).length} / {correctResponses.length}</div>
              <div>Accuracy: {correctResponses.length > 0 
                ? ((correctResponses.filter(r => r).length / correctResponses.length) * 100).toFixed(1) 
                : 0}%</div>
              <div>Avg Response Time: {responseTimes.length > 0 
                ? Math.round(responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length) 
                : 0}ms</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractiveNBackSimulator;
