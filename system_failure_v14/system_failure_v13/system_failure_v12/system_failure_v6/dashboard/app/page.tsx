'use client';

import { useMemo, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import Sidebar from '@/components/Sidebar';
import PredictionCards from '@/components/PredictionCards';
import Charts from '@/components/Charts';
import FeatureImportance from '@/components/FeatureImportance';
import ModelPerformance from '@/components/ModelPerformance';
import ExportSection from '@/components/ExportSection';
import { mockPrediction, mockModelMetrics, mockImportance, datasetDistribution } from '@/lib/mockData';

const MODE_LABELS: Record<number, string> = {
  0: 'Healthy',
  1: 'Wear-Out Failure',
  4: 'Controller/Firmware Failure',
};

function computeDashboardPrediction(inputs: {
  battery_voltage: number;
  rtc_drift: number;
  boot_errors: number;
  cmos_warning: number;
  reset_bios: number;
  power_cycle: number;
  system_age: number;
  temperature: number;
}) {
  const wearSignal =
    (inputs.system_age >= 7 ? 0.28 : 0) +
    (inputs.power_cycle >= 1700 ? 0.24 : 0) +
    (inputs.rtc_drift >= 65 ? 0.2 : 0) +
    (inputs.temperature >= 34 ? 0.14 : 0) +
    (inputs.battery_voltage <= 2.7 ? 0.22 : 0);

  const controllerSignal =
    (inputs.boot_errors >= 5 ? 0.32 : 0) +
    (inputs.boot_errors >= 3 && inputs.system_age <= 4 ? 0.2 : 0) +
    (inputs.cmos_warning >= 1 && inputs.boot_errors >= 2 && inputs.rtc_drift >= 90 ? 0.22 : 0) +
    (inputs.reset_bios >= 1 && inputs.boot_errors >= 4 ? 0.2 : 0);

  const wearProb = Math.min(0.92, Math.max(0.03, wearSignal));
  const controllerProb = Math.min(0.92, Math.max(0.02, controllerSignal));
  let healthyProb = 1 - wearProb - controllerProb;

  if (healthyProb < 0.05) {
    const total = wearProb + controllerProb;
    healthyProb = 0.05;
    const scale = 0.95 / total;
    const scaledWear = wearProb * scale;
    const scaledController = controllerProb * scale;
    const predMode = scaledWear >= scaledController ? 1 : 4;
    const confidence = predMode === 1 ? scaledWear : scaledController;
    return {
      ...mockPrediction,
      pred_mode: predMode,
      pred_flag: 1,
      confidence_pct: confidence * 100,
      risk_level: 'High',
      risk_color: '#dc2626',
      failure_probability: scaledWear + scaledController,
      status_label: MODE_LABELS[predMode],
      prob_map: {
        0: healthyProb,
        1: scaledWear,
        4: scaledController,
      } as const,
    };
  }

  const predMode = healthyProb >= wearProb && healthyProb >= controllerProb ? 0 : wearProb >= controllerProb ? 1 : 4;
  const risk = wearProb + controllerProb;
  const confidence = predMode === 0 ? healthyProb : predMode === 1 ? wearProb : controllerProb;
  const riskLevel = risk < 0.25 ? 'Low' : risk < 0.6 ? 'Medium' : 'High';

  const summaryText =
    predMode === 0
      ? `<strong>✅ System is operating normally.</strong> Healthy confidence is ${(healthyProb * 100).toFixed(1)}%, with lower failure probabilities for wear-out (${(wearProb * 100).toFixed(1)}%) and controller issues (${(controllerProb * 100).toFixed(1)}%).`
      : predMode === 1
        ? `<strong>⚠️ System shows signs of aging.</strong> Wear-out probability is ${(wearProb * 100).toFixed(1)}%, which is higher than the healthy confidence (${(healthyProb * 100).toFixed(1)}%).`
        : `<strong>🚨 System may have firmware/controller issues.</strong> Controller failure probability is ${(controllerProb * 100).toFixed(1)}%, indicating sudden fault behavior rather than gradual wear-out.`;

  return {
    ...mockPrediction,
    pred_mode: predMode,
    pred_flag: predMode === 0 ? 0 : 1,
    confidence_pct: confidence * 100,
    risk_level: riskLevel,
    risk_color: riskLevel === 'Low' ? '#16a34a' : riskLevel === 'Medium' ? '#f59e0b' : '#dc2626',
    failure_probability: risk,
    status_label: MODE_LABELS[predMode],
    summary_text: summaryText,
    prob_map: {
      0: healthyProb,
      1: wearProb,
      4: controllerProb,
    } as const,
  };
}

export default function Home() {
  const [inputs, setInputs] = useState({
    battery_voltage: 3.0,
    rtc_drift: 0,
    boot_errors: 0,
    cmos_warning: 0,
    reset_bios: 0,
    power_cycle: 0,
    system_age: 1,
    temperature: 25.0,
  });

  const prediction = useMemo(() => computeDashboardPrediction(inputs), [inputs]);

  const recommendations = useMemo(() => {
    const result: string[] = [];
    if (prediction.pred_mode === 1) {
      result.push('⚠️ Wear-Out Failure Detected');
      result.push('Replace CMOS battery soon');
      result.push('Schedule preventive maintenance');
      result.push('Monitor system aging metrics');
    } else if (prediction.pred_mode === 4) {
      result.push('🚨 Controller/Firmware Failure Detected');
      result.push('Update BIOS/Firmware');
      result.push('Run system diagnostics');
      result.push('Check error logs');
    } else {
      result.push('✅ System Healthy');
      result.push('No immediate action required');
    }

    if (inputs.battery_voltage < 2.8) {
      result.push(`🚨 Battery voltage is critically low (${inputs.battery_voltage.toFixed(2)}V).`);
    }
    if (inputs.boot_errors >= 5) {
      result.push(`⚠️ Boot errors are high (${inputs.boot_errors}).`);
    }
    if (inputs.temperature > 40) {
      result.push(`⚠️ Ambient temperature is elevated (${inputs.temperature.toFixed(1)}°C).`);
    }
    return result;
  }, [inputs, prediction.pred_mode]);

  const datasetStats = {
    total: 2000,
    healthyPct: 70.2,
    failurePct: 29.8,
    commonClass: 'Healthy',
  };

  const datasetRows = [
    {
      Battery_Voltage: 2.74,
      RTC_Drift_sec_per_day: 78,
      Boot_Errors_Count: 4,
      CMOS_Warning_Flag: 1,
      Reset_BIOS_Flag: 1,
      Power_Cycle_Count: 1812,
      System_Age_Years: 8,
      Ambient_Temperature_C: 36.2,
      Failure_Mode: 1,
      Failure_Flag: 1,
    },
    {
      Battery_Voltage: 3.02,
      RTC_Drift_sec_per_day: 14,
      Boot_Errors_Count: 0,
      CMOS_Warning_Flag: 0,
      Reset_BIOS_Flag: 0,
      Power_Cycle_Count: 412,
      System_Age_Years: 2,
      Ambient_Temperature_C: 26.1,
      Failure_Mode: 0,
      Failure_Flag: 0,
    },
    {
      Battery_Voltage: 2.86,
      RTC_Drift_sec_per_day: 98,
      Boot_Errors_Count: 6,
      CMOS_Warning_Flag: 1,
      Reset_BIOS_Flag: 1,
      Power_Cycle_Count: 940,
      System_Age_Years: 3,
      Ambient_Temperature_C: 33.8,
      Failure_Mode: 4,
      Failure_Flag: 1,
    },
  ];

  const analyticsDist = datasetDistribution.labels.map((label, idx) => ({
    label,
    count: datasetDistribution.counts[idx],
    pct: datasetDistribution.percentages[idx],
  }));
  const analyticsColors = ['#22c55e', '#f59e0b', '#ef4444'];

  return (
    <div className="min-h-screen">
      <div className="dashboard-shell max-w-[1400px] mx-auto px-4 py-6">
        <aside className="dashboard-sidebar">
          <Sidebar inputs={inputs} setInputs={setInputs} />
        </aside>

        <main className="dashboard-main">
          <div className="hero">
            <h1 className="hero-title">🚀 CMOS Failure Analysis Dashboard</h1>
            <p className="hero-subtitle">AI-powered predictive maintenance system</p>
          </div>

          <div className="section-wrap" style={{ marginTop: 0 }}>
            <p className="section-subtitle" style={{ margin: 0 }}>
              Using dataset source: Local file: CMOS_Battery_Failure_Dataset.csv
            </p>
          </div>

          <PredictionCards prediction={prediction} />

          <Charts prediction={prediction} />

          <div className="section-wrap">
            <div className="section-title">🔧 Recommendations</div>
            <div className="section-subtitle">Actionable response based on predicted failure mode</div>
            <div className="summary-box">
              {recommendations.map((item) => (
                <p key={item} style={{ marginBottom: '0.45rem' }}>• {item}</p>
              ))}
            </div>
          </div>

          <FeatureImportance importance={mockImportance} />

          <div className="section-wrap">
            <div className="section-title">🧾 Summary</div>
            <div className="section-subtitle">Prediction digest for quick decision making</div>
            <div className="summary-box" dangerouslySetInnerHTML={{ __html: prediction.summary_text }} />
            <p className="section-subtitle" style={{ marginTop: '0.75rem', marginBottom: '0.5rem' }}>
              Prediction updates automatically whenever sidebar inputs change.
            </p>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-gray-300">
                <thead>
                  <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
                    <th className="px-4 py-2 text-left">Feature</th>
                    <th className="px-4 py-2 text-right">Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="bg-slate-800/35"><td className="px-4 py-2">Battery_Voltage</td><td className="px-4 py-2 text-right">{inputs.battery_voltage}</td></tr>
                  <tr className="bg-slate-700/25"><td className="px-4 py-2">RTC_Drift_sec_per_day</td><td className="px-4 py-2 text-right">{inputs.rtc_drift}</td></tr>
                  <tr className="bg-slate-800/35"><td className="px-4 py-2">Boot_Errors_Count</td><td className="px-4 py-2 text-right">{inputs.boot_errors}</td></tr>
                  <tr className="bg-slate-700/25"><td className="px-4 py-2">CMOS_Warning_Flag</td><td className="px-4 py-2 text-right">{inputs.cmos_warning}</td></tr>
                  <tr className="bg-slate-800/35"><td className="px-4 py-2">Reset_BIOS_Flag</td><td className="px-4 py-2 text-right">{inputs.reset_bios}</td></tr>
                  <tr className="bg-slate-700/25"><td className="px-4 py-2">Power_Cycle_Count</td><td className="px-4 py-2 text-right">{inputs.power_cycle}</td></tr>
                  <tr className="bg-slate-800/35"><td className="px-4 py-2">System_Age_Years</td><td className="px-4 py-2 text-right">{inputs.system_age}</td></tr>
                  <tr className="bg-slate-700/25"><td className="px-4 py-2">Ambient_Temperature_C</td><td className="px-4 py-2 text-right">{inputs.temperature}</td></tr>
                </tbody>
              </table>
            </div>
          </div>

          <ModelPerformance metrics={mockModelMetrics} />

          <details className="section-wrap">
            <summary className="section-title" style={{ cursor: 'pointer' }}>Optional: Dataset Analytics</summary>
            <div style={{ marginTop: '0.9rem' }}>
              <p className="section-subtitle" style={{ marginBottom: '0.5rem' }}>Dataset Preview</p>
              <div className="overflow-x-auto" style={{ marginBottom: '1rem' }}>
                <table className="w-full text-sm text-gray-300">
                  <thead>
                    <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
                      <th className="px-3 py-2 text-left">Battery_Voltage</th>
                      <th className="px-3 py-2 text-right">RTC_Drift_sec_per_day</th>
                      <th className="px-3 py-2 text-right">Boot_Errors_Count</th>
                      <th className="px-3 py-2 text-right">Failure_Mode</th>
                    </tr>
                  </thead>
                  <tbody>
                    {datasetRows.map((row, idx) => (
                      <tr key={idx} className={idx % 2 === 0 ? 'bg-slate-800/35' : 'bg-slate-700/25'}>
                        <td className="px-3 py-2">{row.Battery_Voltage.toFixed(2)}</td>
                        <td className="px-3 py-2 text-right">{row.RTC_Drift_sec_per_day}</td>
                        <td className="px-3 py-2 text-right">{row.Boot_Errors_Count}</td>
                        <td className="px-3 py-2 text-right">{row.Failure_Mode}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <p className="section-subtitle" style={{ marginBottom: '0.5rem' }}>Dataset Overview</p>
              <div className="card-grid">
                <div className="kpi-card kpi-info">
                  <div className="metric-label">Total Systems</div>
                  <div className="metric-value">{datasetStats.total}</div>
                </div>
                <div className="kpi-card kpi-healthy">
                  <div className="metric-label">Healthy %</div>
                  <div className="metric-value">{datasetStats.healthyPct}%</div>
                </div>
                <div className="kpi-card kpi-warning">
                  <div className="metric-label">Failure %</div>
                  <div className="metric-value">{datasetStats.failurePct}%</div>
                </div>
                <div className="kpi-card kpi-info">
                  <div className="metric-label">Common Class</div>
                  <div className="metric-value">{datasetStats.commonClass}</div>
                </div>
              </div>

              <p className="section-subtitle" style={{ marginTop: '1rem', marginBottom: '0.5rem' }}>
                Dataset-based distribution stays available here for reference.
              </p>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div className="chart-card">
                  <div className="section-title">Dataset Failure Distribution</div>
                  <ResponsiveContainer width="100%" height={320}>
                    <PieChart>
                      <Pie data={analyticsDist} dataKey="count" nameKey="label" innerRadius={58} outerRadius={105}>
                        {analyticsDist.map((_, idx) => (
                          <Cell key={idx} fill={analyticsColors[idx]} />
                        ))}
                      </Pie>
                      <RechartsTooltip formatter={(value: number) => `${value}`} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="chart-card">
                  <div className="section-title">Distribution Table</div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm text-gray-300">
                      <thead>
                        <tr className="bg-cyan-600/30 text-cyan-300 font-bold">
                          <th className="px-3 py-2 text-left">Failure_Mode</th>
                          <th className="px-3 py-2 text-left">Label</th>
                          <th className="px-3 py-2 text-right">Count</th>
                          <th className="px-3 py-2 text-right">Percentage</th>
                        </tr>
                      </thead>
                      <tbody>
                        {[0, 1, 4].map((mode, idx) => (
                          <tr key={mode} className={idx % 2 === 0 ? 'bg-slate-800/35' : 'bg-slate-700/25'}>
                            <td className="px-3 py-2">{mode}</td>
                            <td className="px-3 py-2">{analyticsDist[idx].label}</td>
                            <td className="px-3 py-2 text-right">{analyticsDist[idx].count}</td>
                            <td className="px-3 py-2 text-right">{analyticsDist[idx].pct.toFixed(1)}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </details>

          <ExportSection rowCount={datasetStats.total} />

          <div className="footer-note">Built for predictive maintenance | AI-powered system</div>
        </main>
      </div>
    </div>
  );
}
