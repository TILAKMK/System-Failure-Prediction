'use client';

import { PredictionData } from '@/lib/mockData';

interface PredictionCardsProps {
  prediction: PredictionData;
}

export default function PredictionCards({ prediction }: PredictionCardsProps) {
  const StatCard = ({ icon, label, value, meta, tone }: any) => {
    const toneClasses = {
      healthy: 'bg-gradient-to-br from-green-500/45 to-slate-900/80 border-green-500/40',
      failure: 'bg-gradient-to-br from-red-500/45 to-slate-900/80 border-red-500/40',
      warning: 'bg-gradient-to-br from-yellow-500/45 to-slate-900/80 border-yellow-500/40',
      info: 'bg-gradient-to-br from-cyan-500/45 to-slate-900/80 border-cyan-500/40',
    };

    return (
      <div className={`kpi-card border rounded-lg p-4 min-h-[120px] transition-transform hover:scale-105 ${toneClasses[tone as keyof typeof toneClasses]}`}>
        <div className="metric-label">{icon} {label}</div>
        <div className="metric-value">{value}</div>
        <div className="metric-meta">{meta}</div>
      </div>
    );
  };

  const statusTone = prediction.pred_mode === 0 ? 'healthy' : 'failure';
  const riskTone = prediction.risk_level === 'Low' ? 'healthy' : prediction.risk_level === 'Medium' ? 'warning' : 'failure';
  const modeTone = prediction.pred_mode === 0 ? 'healthy' : prediction.pred_mode === 1 ? 'warning' : 'failure';

  return (
    <div className="section-wrap">
      <h2 className="section-title">🔥 KPI Prediction Cards</h2>
      <p className="section-subtitle">Realtime classification and confidence indicators</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
        <StatCard
          icon="✅"
          label="Predicted Status"
          value={prediction.pred_flag === 0 ? 'Healthy' : 'Failure'}
          meta="Current system health"
          tone={statusTone}
        />
        <StatCard
          icon="📊"
          label="Confidence"
          value={`${prediction.confidence_pct.toFixed(1)}%`}
          meta="Predicted-class confidence"
          tone="info"
        />
        <StatCard
          icon="⚠️"
          label="Risk Level"
          value={prediction.risk_level}
          meta="Computed from failure probability"
          tone={riskTone}
        />
        <StatCard
          icon="🚨"
          label="Failure Mode"
          value={`${prediction.pred_mode}: ${prediction.status_label}`}
          meta="Multi-class mode output"
          tone={modeTone}
        />
      </div>

      <p className="text-sm text-gray-400 mb-2">
        Overall failure probability: <span className="font-bold text-cyan-400">{(prediction.failure_probability * 100).toFixed(2)}%</span>
      </p>
      <div className="w-full bg-slate-700 rounded-full h-2">
        <div
          className="bg-gradient-to-r from-cyan-500 to-green-500 h-2 rounded-full transition-all"
          style={{ width: `${Math.min(Math.max(prediction.confidence_pct, 0), 100)}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 mt-2">Confidence progress for the predicted class</p>
    </div>
  );
}
