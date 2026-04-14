# CMOS Battery Failure Analysis Dashboard

AI-powered predictive maintenance dashboard for hardware telemetry. The system classifies machine health into three classes using a Random Forest model:
- Healthy (0)
- Wear-Out Failure (1)
- Controller/Firmware Failure (4)

## Overview

This project provides an end-to-end workflow for CMOS and system-level failure analysis:
- ingest telemetry from CSV datasets
- preprocess and validate failure-mode labels
- train and evaluate a multi-class classifier
- visualize results in an interactive Streamlit dashboard
- generate actionable maintenance recommendations

It is designed for predictive maintenance scenarios where early detection reduces downtime and repair cost.

## Key Features

- Multi-class failure prediction (Healthy, Wear-Out, Controller/Firmware)
- Real-time inference from sidebar input controls
- Per-class probability display and risk-level scoring
- Global and class-specific feature importance (permutation-based)
- Test metrics and stratified cross-validation summary
- Confusion matrix and optional dataset analytics
- CSV upload support for custom telemetry data
- Downloadable report with predicted failure labels

## Project Structure

```text
.
├── app.py                             # Streamlit dashboard (main entry point)
├── train_model.py                     # Training, evaluation, and model serialization
├── preprocess.py                      # Raw log preprocessing utility
├── model.pkl                          # Saved RandomForest pipeline
├── CMOS_Battery_Failure_Dataset.csv   # Primary dataset
├── NVMe_Drive_Failure_Dataset.csv     # Additional dataset
└── data/
   ├── raw_logs.txt                   # Raw system logs
   └── processed_logs.csv             # Structured output from preprocess.py
```

## Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Estimators | 400 |
| Max Depth | 8 |
| Class Weighting | `balanced_subsample` |
| Missing Value Handling | `SimpleImputer(strategy="median")` |
| Validation | Stratified cross-validation |

### Input Features

- `Battery_Voltage`
- `RTC_Drift_sec_per_day`
- `Boot_Errors_Count`
- `CMOS_Warning_Flag`
- `Reset_BIOS_Flag`
- `Power_Cycle_Count`
- `System_Age_Years`
- `Ambient_Temperature_C`

### Target Classes

| Label | Meaning |
|---|---|
| `0` | Healthy |
| `1` | Wear-Out Failure |
| `4` | Controller/Firmware Failure |

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/TILAKMK/System-Failure-Prediction.git
cd System-Failure-Prediction
pip install streamlit pandas numpy scikit-learn plotly
```

### Run the Dashboard

```bash
streamlit run app.py
```

Default local URL is typically `http://localhost:8501`.

## Training and Preprocessing

### Retrain Model

```bash
python train_model.py
```

This script trains the model, prints evaluation metrics, and writes `model.pkl`.

### Preprocess Raw Logs

```bash
python preprocess.py
```

Input: `data/raw_logs.txt`  
Output: `data/processed_logs.csv`

## Using a Custom Dataset

1. Open the Streamlit app.
2. Upload a CSV from the sidebar.
3. Include the required feature columns and `Failure_Mode` values in `{0, 1, 4}`.

The app will process the uploaded dataset and run model training/evaluation for that session.

## Report Export

Use **Download Report** in the dashboard to export telemetry rows with prediction outputs, including:
- `Predicted_Failure_Mode`
- `Failure_Mode_Label`
- `Failure_Flag`

## License

This project is licensed under the MIT License.

## Author

Tilak M K  
B.E. Artificial Intelligence and Machine Learning  
The National Institute of Engineering, Mysuru
