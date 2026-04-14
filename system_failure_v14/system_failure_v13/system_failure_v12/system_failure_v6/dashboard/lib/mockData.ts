export interface PredictionData {
  pred_mode: number;
  pred_flag: number;
  confidence_pct: number;
  risk_level: string;
  risk_color: string;
  failure_probability: number;
  status_label: string;
  summary_text: string;
  prob_map: {
    0: number;
    1: number;
    4: number;
  };
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  cv_summary: {
    accuracy_mean: number;
    accuracy_std: number;
    precision_mean: number;
    precision_std: number;
    recall_mean: number;
    recall_std: number;
    f1_mean: number;
    f1_std: number;
    folds: number;
    note: string;
  };
  confusion_matrix: number[][];
}

export interface ImportanceData {
  features: string[];
  global_importance: number[];
  wear_out_importance: number[];
  controller_importance: number[];
}

export const mockPrediction: PredictionData = {
  pred_mode: 0,
  pred_flag: 0,
  confidence_pct: 89.5,
  risk_level: 'Low',
  risk_color: '#16a34a',
  failure_probability: 0.105,
  status_label: 'Healthy',
  summary_text: '✅ System is operating normally. Healthy confidence is 89.5%, with lower failure probabilities for wear-out (8.2%) and controller issues (2.3%).',
  prob_map: {
    0: 0.895,
    1: 0.082,
    4: 0.023,
  },
};

export const mockModelMetrics: ModelMetrics = {
  accuracy: 0.876,
  precision: 0.834,
  recall: 0.821,
  f1: 0.827,
  cv_summary: {
    accuracy_mean: 0.868,
    accuracy_std: 0.032,
    precision_mean: 0.821,
    precision_std: 0.041,
    recall_mean: 0.813,
    recall_std: 0.038,
    f1_mean: 0.817,
    f1_std: 0.035,
    folds: 5,
    note: 'Using 5-fold stratified cross-validation.',
  },
  confusion_matrix: [
    [654, 38, 12],
    [42, 182, 16],
    [18, 14, 95],
  ],
};

export const mockImportance = {
  features: [
    'Battery_Voltage',
    'RTC_Drift_sec_per_day',
    'Boot_Errors_Count',
    'System_Age_Years',
    'Power_Cycle_Count',
    'Ambient_Temperature_C',
    'CMOS_Warning_Flag',
    'Reset_BIOS_Flag',
  ],
  global_importance: [0.285, 0.241, 0.198, 0.156, 0.082, 0.021, 0.012, 0.005],
  wear_out_importance: [0.312, 0.267, 0.145, 0.189, 0.065, 0.018, 0.003, 0.001],
  controller_importance: [0.241, 0.198, 0.289, 0.084, 0.123, 0.031, 0.028, 0.006],
};

export const datasetDistribution = {
  labels: ['Healthy', 'Wear-Out Failure', 'Controller/Firmware Failure'],
  counts: [1425, 342, 233],
  percentages: [70.2, 16.9, 11.5],
};
