'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ImportanceData } from '@/lib/mockData';

interface FeatureImportanceProps {
  importance: ImportanceData;
}

export default function FeatureImportance({ importance }: FeatureImportanceProps) {
  const data = importance.features.map((feature, idx) => ({
    name: feature,
    global: parseFloat(importance.global_importance[idx].toFixed(3)),
    wearout: parseFloat(importance.wear_out_importance[idx].toFixed(3)),
    controller: parseFloat(importance.controller_importance[idx].toFixed(3)),
  }));

  const topWearOut = [...data].sort((a, b) => b.wearout - a.wearout).slice(0, 3);
  const topController = [...data].sort((a, b) => b.controller - a.controller).slice(0, 3);

  return (
    <div className="section-wrap">
      <h2 className="section-title">📈 Feature Importance</h2>
      <p className="section-subtitle">Global and mode-specific telemetry impact</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Global Feature Impact */}
        <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
          <h3 className="text-sm font-bold text-cyan-400 mb-4">Global Feature Impact</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart layout="vertical" data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" />
              <XAxis type="number" stroke="#94a3b8" />
              <YAxis dataKey="name" type="category" stroke="#94a3b8" width={120} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #0ea5a0' }}
                formatter={(value: any) => typeof value === 'number' ? value.toFixed(3) : value}
              />
              <Bar dataKey="global" fill="#38bdf8" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Mode-Specific Table */}
        <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
          <h3 className="text-sm font-bold text-cyan-400 mb-4">Mode-Specific Drivers</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-gray-300">
              <thead>
                <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
                  <th className="px-2 py-2 text-left">Feature</th>
                  <th className="px-2 py-2 text-right">Wear-Out</th>
                  <th className="px-2 py-2 text-right">Controller</th>
                </tr>
              </thead>
              <tbody>
                {data.map((row, idx) => (
                  <tr key={idx} className={idx % 2 === 0 ? 'bg-slate-800/35' : 'bg-slate-700/25'}>
                    <td className="px-2 py-2">{row.name}</td>
                    <td className="px-2 py-2 text-right text-yellow-400">{row.wearout.toFixed(3)}</td>
                    <td className="px-2 py-2 text-right text-red-400">{row.controller.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Top Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
          <h4 className="text-sm font-bold text-yellow-400 mb-3">Top Wear-Out drivers</h4>
          <div className="space-y-2">
            {topWearOut.map((item, idx) => (
              <div key={idx} className="flex justify-between text-sm">
                <span className="text-gray-300">{item.name}</span>
                <span className="text-yellow-400 font-bold">{item.wearout.toFixed(3)}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
          <h4 className="text-sm font-bold text-red-400 mb-3">Top Controller/Firmware drivers</h4>
          <div className="space-y-2">
            {topController.map((item, idx) => (
              <div key={idx} className="flex justify-between text-sm">
                <span className="text-gray-300">{item.name}</span>
                <span className="text-red-400 font-bold">{item.controller.toFixed(3)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
