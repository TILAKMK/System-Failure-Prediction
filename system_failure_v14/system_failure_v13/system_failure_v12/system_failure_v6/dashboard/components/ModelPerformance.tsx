'use client';

import { ModelMetrics } from '@/lib/mockData';

interface ModelPerformanceProps {
  metrics: ModelMetrics;
}

export default function ModelPerformance({ metrics }: ModelPerformanceProps) {
  const StatCard = ({ label, value, meta }: any) => (
    <div className="bg-gradient-to-br from-cyan-500/45 to-slate-900/80 border border-cyan-500/40 rounded-lg p-4 min-h-[100px]">
      <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider">📊 {label}</div>
      <div className="text-2xl font-bold text-white mt-1">{(value * 100).toFixed(2)}%</div>
      <div className="text-xs text-gray-400 mt-2">{meta}</div>
    </div>
  );

  const cvMetrics = [
    { label: 'Accuracy', value: metrics.cv_summary.accuracy_mean, std: metrics.cv_summary.accuracy_std },
    { label: 'Precision', value: metrics.cv_summary.precision_mean, std: metrics.cv_summary.precision_std },
    { label: 'Recall', value: metrics.cv_summary.recall_mean, std: metrics.cv_summary.recall_std },
    { label: 'F1-score', value: metrics.cv_summary.f1_mean, std: metrics.cv_summary.f1_std },
  ];

  const confusionMatrix = [
    { actual: 'Healthy (0)', healthy: metrics.confusion_matrix[0][0], wearout: metrics.confusion_matrix[0][1], controller: metrics.confusion_matrix[0][2] },
    { actual: 'Wear-Out (1)', healthy: metrics.confusion_matrix[1][0], wearout: metrics.confusion_matrix[1][1], controller: metrics.confusion_matrix[1][2] },
    { actual: 'Controller (4)', healthy: metrics.confusion_matrix[2][0], wearout: metrics.confusion_matrix[2][1], controller: metrics.confusion_matrix[2][2] },
  ];

  return (
    <div className="section-wrap">
      <h2 className="section-title">🎯 Model Performance</h2>
      <p className="section-subtitle">Validation metrics and confusion matrix</p>

      {/* Test Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Accuracy" value={metrics.accuracy} meta="Test split performance" />
        <StatCard label="Precision" value={metrics.precision} meta="Macro averaged" />
        <StatCard label="Recall" value={metrics.recall} meta="Macro averaged" />
        <StatCard label="F1-score" value={metrics.f1} meta="Balanced performance" />
      </div>

      {/* Cross-Validation Summary */}
      <div className="mb-6">
        <p className="text-sm text-gray-400 mb-2">
          Cross-validation summary ({metrics.cv_summary.folds}-fold stratified)
        </p>
        <p className="text-sm text-gray-400 mb-4">{metrics.cv_summary.note}</p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-gray-300">
            <thead>
              <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
                <th className="px-4 py-2 text-left">Metric</th>
                <th className="px-4 py-2 text-right">CV Mean</th>
                <th className="px-4 py-2 text-right">CV Std</th>
              </tr>
            </thead>
            <tbody>
              {cvMetrics.map((row, idx) => (
                <tr key={idx} className={idx % 2 === 0 ? 'bg-slate-800/35' : 'bg-slate-700/25'}>
                  <td className="px-4 py-2">{row.label}</td>
                  <td className="px-4 py-2 text-right font-bold text-cyan-400">{(row.value * 100).toFixed(2)}%</td>
                  <td className="px-4 py-2 text-right text-gray-400">{(row.std * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Confusion Matrix */}
      <div>
        <h3 className="text-sm font-bold text-cyan-400 mb-3">🧩 Confusion Matrix</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-gray-300">
            <thead>
              <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
                <th className="px-4 py-2 text-left">Actual / Predicted</th>
                <th className="px-4 py-2 text-right">Healthy (0)</th>
                <th className="px-4 py-2 text-right">Wear-Out (1)</th>
                <th className="px-4 py-2 text-right">Controller (4)</th>
              </tr>
            </thead>
            <tbody>
              {confusionMatrix.map((row, idx) => (
                <tr key={idx} className={idx % 2 === 0 ? 'bg-slate-800/35' : 'bg-slate-700/25'}>
                  <td className="px-4 py-2 font-bold">{row.actual}</td>
                  <td className="px-4 py-2 text-right text-green-400">{row.healthy}</td>
                  <td className="px-4 py-2 text-right text-yellow-400">{row.wearout}</td>
                  <td className="px-4 py-2 text-right text-red-400">{row.controller}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
