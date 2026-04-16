import React, { useState } from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';

interface DataSimulatorProps {
  trialType: '0back' | '3back' | '5back' | '6back';
  onDataGenerated: (data: any) => void;
}

const DataSimulator: React.FC<DataSimulatorProps> = ({ trialType, onDataGenerated }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [currentTrial, setCurrentTrial] = useState('');
  const [userResponses, setUserResponses] = useState<boolean[]>([]);
  const [responseTimes, setResponseTimes] = useState<number[]>([]);
  const [correctResponses, setCorrectResponses] = useState<boolean[]>([]);
  const [stimulusHistory, setStimulusHistory] = useState<string[]>([]);
  const [feedback, setFeedback] = useState<'correct' | 'incorrect' | null>(null);
  const [currentTrialIndex, setCurrentTrialIndex] = useState(0);
  const [trialStartTime, setTrialStartTime] = useState<number>(0);

  // Handle user response
  const handleUserResponse = () => {
    if (!isRunning || !currentTrial) return;
    
    const responseTime = Date.now() - trialStartTime;
    const n = parseInt(trialType.replace('back', ''));
    
    // Check if response is correct
    let isCorrect = false;
    if (n === 0) {
      // 0-back: Click when you see X
      isCorrect = currentTrial === 'X';
    } else if (stimulusHistory.length > n) {
      // N-back: Click when current matches N steps back
      isCorrect = currentTrial === stimulusHistory[stimulusHistory.length - n - 1];
    }
    
    setUserResponses(prev => [...prev, true]);
    setCorrectResponses(prev => [...prev, isCorrect]);
    setResponseTimes(prev => [...prev, responseTime]);
    setFeedback(isCorrect ? 'correct' : 'incorrect');
    
    setTimeout(() => setFeedback(null), 1000);
  };

  // Simulate n-back task
  const simulateTask = async () => {
    let stimuli = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
    
    // For 0-back, include target letter X
    if (trialType === '0back') {
      stimuli = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'X'];
    }
    
    const responses: boolean[] = [];
    const times: number[] = [];
    
    for (let i = 0; i < 20; i++) {
      const stimulus = stimuli[Math.floor(Math.random() * stimuli.length)];
      setCurrentTrial(stimulus);
      
      // Simulate user response time
      const responseTime = 800 + Math.random() * 1200; // 800-2000ms
      const shouldRespond = Math.random() > 0.3; // 70% accuracy
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (shouldRespond) {
        responses.push(true);
        times.push(responseTime);
      } else {
        responses.push(false);
        times.push(responseTime + Math.random() * 500);
      }
    }
    
    setUserResponses(responses);
    setResponseTimes(times);
    
    // Calculate statistics
    const avgResponseTime = times.reduce((a, b) => a + b, 0) / times.length;
    const accuracy = responses.filter(r => r).length / responses.length;
    const variability = Math.sqrt(times.reduce((sq, n) => sq + Math.pow(n - avgResponseTime, 2), 0) / times.length);
    
    onDataGenerated({
      response_time: Math.round(avgResponseTime),
      accuracy: parseFloat(accuracy.toFixed(2)),
      variability: Math.round(variability)
    });
    
    setIsRunning(false);
  };

  const startSimulation = () => {
    setIsRunning(true);
    setUserResponses([]);
    setResponseTimes([]);
    simulateTask();
  };

  const resetSimulation = () => {
    setIsRunning(false);
    setCurrentTrial('');
    setUserResponses([]);
    setResponseTimes([]);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4">Interactive N-Back Task Simulator</h3>
      
      <div className="mb-4">
        <div className="text-center mb-4">
          <div 
            onClick={handleUserResponse}
            className={`text-6xl font-bold mb-2 cursor-pointer transition-all duration-200 ${
              isRunning && currentTrial 
                ? 'text-primary-600 hover:text-primary-700 hover:scale-110' 
                : 'text-gray-400'
            } ${feedback === 'correct' ? 'text-green-600' : feedback === 'incorrect' ? 'text-red-600' : ''}`}
          >
            {currentTrial || (isRunning ? '?' : '-')}
          </div>
          
          <div className="text-sm text-gray-600 mb-2">
            {isRunning ? (
              <>
                {trialType === '0back' ? 'Click if you see X!' : `Click if this matches ${trialType.replace('back', '-back')}!`}
                <div className="text-xs mt-1">
                  Pattern: {trialType === '0back' ? 'Look for letter X' : `Match with ${trialType.replace('back', '')} steps back`}
                </div>
              </>
            ) : 'Press Start to begin'}
          </div>
          
          {isRunning && currentTrial && (
            <div className="mb-2">
              <button
                onClick={handleUserResponse}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
              >
                {feedback === 'correct' ? 'Correct! +1' : feedback === 'incorrect' ? 'Wrong! -1' : 'CLICK TO RESPOND'}
              </button>
            </div>
          )}
        </div>
        
        {/* Stimulus History */}
        {stimulusHistory.length > 0 && (
          <div className="mb-4 p-3 bg-gray-50 rounded">
            <div className="text-xs text-gray-600 mb-2">Recent stimuli (newest first):</div>
            <div className="flex justify-center space-x-1">
              {stimulusHistory.slice(-8).reverse().map((stimulus, idx) => {
                const n = parseInt(trialType.replace('back', ''));
                const isMatchPosition = n === 0 ? stimulus === 'X' : idx === n - 1 && stimulusHistory.length > n;
                return (
                  <span 
                    key={idx}
                    className={`px-2 py-1 text-xs rounded ${
                      idx === 0 ? 'bg-blue-100 text-blue-800 font-bold' : 
                      isMatchPosition ? 'bg-yellow-100 text-yellow-800 border border-yellow-400' :
                      'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {stimulus}
                    {idx === n - 1 && n > 0 && <span className="ml-1">?</span>}
                  </span>
                );
              })}
            </div>
            {parseInt(trialType.replace('back', '')) > 0 && (
              <div className="text-xs text-center mt-2 text-gray-500">
                Yellow highlight = {trialType.replace('back', '')} steps back (compare with blue)
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
            <>
              <button
                onClick={handleUserResponse}
                disabled={!currentTrial}
                className="flex items-center space-x-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                <span>{currentTrial ? 'CLICK TO RESPOND' : 'Waiting...'}</span>
              </button>
              <button
                onClick={resetSimulation}
                className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                <Pause className="h-4 w-4" />
                <span>Stop</span>
              </button>
            </>
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
              <div>Trials: {responseTimes.length} | Responses: {userResponses.filter(r => r).length}</div>
              <div>Accuracy: {correctResponses.length > 0 ? ((correctResponses.filter(r => r).length / correctResponses.length) * 100).toFixed(1) : 0}%</div>
              <div>Avg Response Time: {Math.round(responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length)}ms</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataSimulator;
