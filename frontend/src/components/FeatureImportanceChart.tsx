import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface FeatureImportanceChartProps {
  data: Array<{
    feature: string;
    importance: number;
  }>;
}

const FeatureImportanceChart: React.FC<FeatureImportanceChartProps> = ({ data }) => {
  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="horizontal"
          margin={{
            top: 20,
            right: 30,
            left: 120,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="feature" type="category" width={100} />
          <Tooltip 
            formatter={(value: number) => value.toFixed(4)}
            labelStyle={{ color: '#000' }}
          />
          <Bar dataKey="importance" fill="#3b82f6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default FeatureImportanceChart;
