'use client';

import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { PredictionData } from '@/lib/mockData';

interface ChartsProps {
  prediction: PredictionData;
}

export default function Charts({ prediction }: ChartsProps) {
  const predictionData = [
    { name: 'Healthy', value: Math.round(prediction.prob_map[0] * 100) },
    { name: 'Wear-Out', value: Math.round(prediction.prob_map[1] * 100) },
    { name: 'Controller', value: Math.round(prediction.prob_map[4] * 100) },
  ];

  const COLORS = ['#22c55e', '#f59e0b', '#ef4444'];

  return (
    <div className="section-wrap">
      <h2 className="section-title">📊 Charts</h2>
      <p className="section-subtitle">Interactive probability distribution and class confidence visuals</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Donut Chart */}
        <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
          <h3 className="text-sm font-bold text-cyan-400 mb-4">Prediction Probability</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={predictionData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
              >
                {predictionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip formatter={(value: any) => typeof value === 'number' ? `${value.toFixed(1)}%` : value} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Bar Chart */}
        <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
          <h3 className="text-sm font-bold text-cyan-400 mb-4">Probability Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={predictionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #0ea5a0' }}
                formatter={(value) => `${value}%`}
              />
              <Bar dataKey="value" fill="#38bdf8" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-gray-300">
          <thead>
            <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
              <th className="px-4 py-2 text-left">Failure Mode</th>
              <th className="px-4 py-2 text-right">Probability %</th>
            </tr>
          </thead>
          <tbody>
            {predictionData.map((row, idx) => (
              <tr key={idx} className={idx % 2 === 0 ? 'bg-slate-800/35' : 'bg-slate-700/25'}>
                <td className="px-4 py-2">{row.name}</td>
                <td className="px-4 py-2 text-right font-bold text-cyan-400">{row.value.toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
