import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ModelPerformanceChartProps {
  data: Array<{
    Model: string;
    Accuracy: number;
    Precision: number;
    Recall: number;
    'F1-Score': number;
  }>;
}

const ModelPerformanceChart: React.FC<ModelPerformanceChartProps> = ({ data }) => {
  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Model" />
          <YAxis domain={[0, 1]} />
          <Tooltip 
            formatter={(value: number) => (value * 100).toFixed(1) + '%'}
            labelStyle={{ color: '#000' }}
          />
          <Legend 
            formatter={(value) => value}
          />
          <Bar dataKey="Accuracy" fill="#3b82f6" />
          <Bar dataKey="Precision" fill="#10b981" />
          <Bar dataKey="Recall" fill="#f59e0b" />
          <Bar dataKey="F1-Score" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ModelPerformanceChart;
