import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline


# ------------------------------
# Streamlit page setup
# ------------------------------
st.set_page_config(page_title="CMOS Failure Analysis Report", layout="wide")

def inject_dashboard_styles() -> None:
    """Apply a premium, animated SaaS visual style."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
            --surface: rgba(15, 23, 42, 0.56);
            --surface-strong: rgba(15, 23, 42, 0.74);
            --border: rgba(148, 163, 184, 0.20);
            --text: #e2e8f0;
            --muted: #94a3b8;
            --primary: #38bdf8;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
            --purple: #8b5cf6;
            --shadow: 0 14px 32px rgba(2, 6, 23, 0.34);
            --radius: 16px;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 12%, rgba(56, 189, 248, 0.09), transparent 24%),
                radial-gradient(circle at 88% 8%, rgba(139, 92, 246, 0.10), transparent 24%),
                radial-gradient(circle at 50% 96%, rgba(34, 197, 94, 0.06), transparent 22%),
                linear-gradient(160deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: var(--text);
            font-family: 'Space Grotesk', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #67e8f9;
        }

        p, li, span, .small-note {
            color: #a5b4c8;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #020617 0%, #0f172a 54%, #3b0764 100%);
            border-right: 1px solid rgba(148,163,184,0.18);
            padding-top: 0.55rem;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] .st-emotion-cache-10trblm {
            color: #67e8f9 !important;
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #cbd5e1 !important;
        }

        section[data-testid="stSidebar"] .stNumberInput input,
        section[data-testid="stSidebar"] .stSelectbox input,
        section[data-testid="stSidebar"] .stTextInput input {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        section[data-testid="stSidebar"] .streamlit-expanderHeader {
            margin-top: 0.25rem;
            margin-bottom: 0.2rem;
            color: #7dd3fc !important;
        }

        section[data-testid="stSidebar"] [data-baseweb="input"],
        section[data-testid="stSidebar"] [data-baseweb="select"] {
            transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
        }

        section[data-testid="stSidebar"] [data-baseweb="input"]:hover,
        section[data-testid="stSidebar"] [data-baseweb="select"]:hover {
            box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.50);
            transform: translateY(-1px);
        }

        section[data-testid="stSidebar"] .st-emotion-cache-1629p8f {
            gap: 0.65rem;
        }

        .hero {
            padding: 1.2rem 1.25rem;
            border-radius: 18px;
            border: 1px solid rgba(148,163,184,0.25);
            background:
                linear-gradient(120deg, rgba(3, 105, 161, 0.36), rgba(91, 33, 182, 0.34), rgba(8, 145, 178, 0.34));
            box-shadow: 0 15px 35px rgba(56, 189, 248, 0.18);
            position: relative;
            overflow: hidden;
            margin-bottom: 0.9rem;
            animation: fadeIn 0.7s ease-out;
        }

        .hero::after {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.95), transparent);
        }

        .hero-title {
            font-size: 2.55rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0;
            letter-spacing: -0.03em;
            background: linear-gradient(90deg, #e0f2fe, #38bdf8, #a78bfa, #67e8f9, #e0f2fe);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            background-size: 250% auto;
            text-shadow: 0 0 16px rgba(56, 189, 248, 0.34);
            animation: gradientShift 8s linear infinite;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.02rem;
            margin-top: 0.42rem;
        }

        .section-wrap {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.08rem 1.12rem;
            margin: 0.8rem 0 1.05rem 0;
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
            animation: fadeIn 0.55s ease-out;
        }

        .section-shell {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(12px);
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #67e8f9;
            margin: 0 0 0.2rem 0;
        }

        .section-subtitle {
            color: var(--muted);
            margin: 0 0 0.85rem 0;
            font-size: 0.92rem;
        }

        .kpi-card {
            border-radius: 14px;
            padding: 0.95rem 1rem;
            border: 1px solid transparent;
            box-shadow: 0 10px 25px rgba(2, 6, 23, 0.28);
            min-height: 118px;
            margin-bottom: 0.65rem;
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }

        .kpi-card:hover {
            transform: scale(1.05);
            box-shadow: 0 16px 34px rgba(15, 23, 42, 0.45);
        }

        .kpi-healthy {
            background: linear-gradient(135deg, rgba(34,197,94,0.45), rgba(15,23,42,0.80));
            border-color: rgba(34,197,94,0.40);
        }

        .kpi-failure {
            background: linear-gradient(135deg, rgba(239,68,68,0.46), rgba(15,23,42,0.80));
            border-color: rgba(239,68,68,0.42);
        }

        .kpi-warning {
            background: linear-gradient(135deg, rgba(245,158,11,0.45), rgba(15,23,42,0.80));
            border-color: rgba(245,158,11,0.42);
        }

        .kpi-info {
            background: linear-gradient(135deg, rgba(56,189,248,0.44), rgba(15,23,42,0.80));
            border-color: rgba(56,189,248,0.40);
        }

        .metric-label {
            font-size: 0.88rem;
            font-weight: 700;
            color: #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            font-size: 1.85rem;
            font-weight: 800;
            margin-top: 0.25rem;
            letter-spacing: -0.03em;
            color: #f8fafc;
        }

        .metric-meta {
            margin-top: 0.35rem;
            font-size: 0.92rem;
            color: #cbd5e1;
        }

        .chart-card, .download-card, .summary-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 1rem;
            height: 100%;
            backdrop-filter: blur(10px);
            animation: slideInUp 0.6s ease-out;
        }

        .summary-box {
            line-height: 1.65;
            color: #e2e8f0;
        }

        .soft-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(148,163,184,0.40), transparent);
            margin: 1rem 0;
        }

        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 0.9rem;
        }

        .small-note {
            color: var(--muted);
            font-size: 0.9rem;
        }

        /* Animations and Transitions */
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(15px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes gradientShift {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-10px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .animate-card {
            animation: slideInUp 0.6s ease-out;
        }

        .animate-text {
            animation: fadeIn 0.8s ease-out;
        }

        .stProgress > div > div {
            background: linear-gradient(90deg, #38bdf8, #22c55e) !important;
        }

        .footer-note {
            margin-top: 1rem;
            text-align: center;
            color: #9ca3af;
            font-size: 0.9rem;
            padding-bottom: 0.65rem;
        }

        @media (max-width: 900px) {
            .hero-title {
                font-size: 1.85rem;
            }

            .metric-value {
                font-size: 1.5rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label: str, value: str, meta: str = "", tone: str = "neutral", icon: str = "📊") -> str:
    return f"""
    <div class="kpi-card kpi-{tone}">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-meta">{meta}</div>
    </div>
    """


def chart_card(title: str, subtitle: str = "") -> str:
    return f"""
    <div class="chart-card">
        <div class="section-title">{title}</div>
        {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
    """


def section_open(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="section-wrap">
            <div class="section-title">{title}</div>
            {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
        """,
        unsafe_allow_html=True,
    )


def section_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def failure_label(mode: int) -> str:
    return MODE_LABELS.get(int(mode), "Unknown")


inject_dashboard_styles()
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🚀 CMOS Failure Analysis Dashboard</div>
        <div class="hero-subtitle">AI-powered predictive maintenance system</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------
# Constants
# ------------------------------
DATA_FILE = "CMOS_Battery_Failure_Dataset.csv"
SOURCE_BINARY_COLUMN = "Failure_Label"
MODE_COLUMN = "Failure_Mode"
BINARY_COLUMN = "Failure_Flag"
VALID_MODES = [0, 1, 4]
MODE_LABELS = {
    0: "Healthy",
    1: "Wear-Out Failure",
    4: "Controller/Firmware Failure",
}
IGNORE_COLUMNS = ["System_ID"]
REQUIRED_FEATURES = [
    "Battery_Voltage",
    "RTC_Drift_sec_per_day",
    "Boot_Errors_Count",
    "CMOS_Warning_Flag",
    "Reset_BIOS_Flag",
    "Power_Cycle_Count",
    "System_Age_Years",
    "Ambient_Temperature_C",
]

# Resource guardrails for Streamlit Cloud deployments.
MAX_BALANCED_SAMPLES_PER_CLASS = 2500
MAX_PERMUTATION_SAMPLE_SIZE = 800
RF_N_ESTIMATORS = 220


# ------------------------------
# Data loading
# ------------------------------
@st.cache_data
def load_dataset_from_path(file_path: str) -> pd.DataFrame:
    """Load dataset from a local CSV path."""
    return pd.read_csv(file_path)


@st.cache_data
def load_dataset_from_upload(file_bytes: bytes) -> pd.DataFrame:
    """Load dataset from uploaded CSV bytes."""
    return pd.read_csv(io.BytesIO(file_bytes))


# ------------------------------
# Data preprocessing
# ------------------------------
def _to_numeric_feature(df: pd.DataFrame, column: str, default_value: float = 0.0) -> pd.Series:
    """Safely coerce a feature to numeric with default fill for missing columns."""
    if column not in df.columns:
        return pd.Series(default_value, index=df.index, dtype=float)
    return pd.to_numeric(df[column], errors="coerce")


def ensure_failure_modes(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure dataset has multi-class failure mode labels and derived binary failure flag."""
    working_df = df.copy()

    age = _to_numeric_feature(working_df, "System_Age_Years")
    cycles = _to_numeric_feature(working_df, "Power_Cycle_Count")
    boot = _to_numeric_feature(working_df, "Boot_Errors_Count")
    rtc = _to_numeric_feature(working_df, "RTC_Drift_sec_per_day")
    temp = _to_numeric_feature(working_df, "Ambient_Temperature_C")
    volt = _to_numeric_feature(working_df, "Battery_Voltage", 3.0)
    cmos_warn = _to_numeric_feature(working_df, "CMOS_Warning_Flag")
    reset_flag = _to_numeric_feature(working_df, "Reset_BIOS_Flag")

    if MODE_COLUMN in working_df.columns:
        mode = pd.to_numeric(working_df[MODE_COLUMN], errors="coerce")
    else:
        mode = pd.Series(np.nan, index=working_df.index, dtype=float)

    # Existing binary failure labels are treated as a weak hint.
    base_failure = pd.Series(False, index=working_df.index)
    if SOURCE_BINARY_COLUMN in working_df.columns:
        base_failure = pd.to_numeric(working_df[SOURCE_BINARY_COLUMN], errors="coerce").fillna(0).astype(int) == 1

    wear_condition = (
        (age >= 7)
        & (cycles >= 1700)
        & ((rtc >= 65) | (temp >= 34) | (volt <= 2.70))
    )
    controller_condition = (
        (boot >= 5)
        | ((boot >= 3) & (age <= 4))
        | ((cmos_warn >= 1) & (boot >= 2) & (rtc >= 90))
        | ((reset_flag >= 1) & (boot >= 4))
    )

    simulated_failure = wear_condition | controller_condition
    any_failure = base_failure | simulated_failure

    # Fill only unknown/invalid mode values to preserve explicit labels from uploaded data.
    unknown_mask = ~mode.isin(VALID_MODES)
    derived_mode = pd.Series(0, index=working_df.index, dtype=int)
    derived_mode.loc[any_failure & controller_condition] = 4
    derived_mode.loc[any_failure & ~controller_condition] = 1

    # Resolve ambiguous failure rows using domain-weighted scoring.
    unresolved = any_failure & (derived_mode == 0)
    wear_score = (
        age.fillna(age.median())
        + (cycles.fillna(cycles.median()) / 350.0)
        + (rtc.fillna(rtc.median()) / 40.0)
        + (temp.fillna(temp.median()) / 18.0)
        - (volt.fillna(3.0) * 1.5)
    )
    controller_score = (
        (boot.fillna(0) * 1.8)
        + (cmos_warn.fillna(0) * 2.5)
        + (reset_flag.fillna(0) * 1.7)
        + ((rtc.fillna(0) >= 90).astype(int) * 1.4)
        + ((age.fillna(99) <= 4).astype(int) * 1.2)
    )
    derived_mode.loc[unresolved] = np.where(
        wear_score.loc[unresolved] >= controller_score.loc[unresolved],
        1,
        4,
    )

    mode.loc[unknown_mask] = derived_mode.loc[unknown_mask]
    mode = mode.fillna(0).astype(int)

    working_df[MODE_COLUMN] = mode
    working_df[BINARY_COLUMN] = (mode != 0).astype(int)

    return working_df


def preprocess_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """Prepare validated feature and failure mode dataframes."""
    working_df = ensure_failure_modes(df)

    for col in IGNORE_COLUMNS:
        if col in working_df.columns:
            working_df = working_df.drop(columns=[col])

    missing_required = [col for col in REQUIRED_FEATURES if col not in working_df.columns]
    if missing_required:
        raise ValueError(
            "Dataset is missing required telemetry columns: " + ", ".join(missing_required)
        )

    x = working_df[REQUIRED_FEATURES].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(working_df[MODE_COLUMN], errors="coerce")

    valid_target_mask = y.isin(VALID_MODES)
    x = x.loc[valid_target_mask].copy()
    y = y.loc[valid_target_mask].astype(int)
    processed_df = working_df.loc[valid_target_mask].copy()

    if y.empty:
        raise ValueError("No valid failure mode labels found after preprocessing.")

    if y.nunique() < 3:
        raise ValueError(
            "Need all three classes in Failure_Mode (0, 1, 4). Upload data with all classes or let simulation create them."
        )

    return x, y, processed_df


def balance_training_set(x_train: pd.DataFrame, y_train: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
    """Balance class distribution by oversampling minority classes in training data."""
    train_df = pd.concat([x_train.reset_index(drop=True), y_train.reset_index(drop=True).rename(MODE_COLUMN)], axis=1)
    class_counts = train_df[MODE_COLUMN].value_counts()
    max_count = int(class_counts.max())
    target_count = min(max_count, MAX_BALANCED_SAMPLES_PER_CLASS)

    balanced_parts = []
    for class_label in VALID_MODES:
        class_rows = train_df[train_df[MODE_COLUMN] == class_label]
        if class_rows.empty:
            continue
        sampled = class_rows.sample(
            n=target_count,
            replace=(len(class_rows) < target_count),
            random_state=42,
        )
        balanced_parts.append(sampled)

    balanced_df = pd.concat(balanced_parts, axis=0).sample(frac=1.0, random_state=42).reset_index(drop=True)
    x_bal = balanced_df[REQUIRED_FEATURES]
    y_bal = balanced_df[MODE_COLUMN].astype(int)
    return x_bal, y_bal


# ------------------------------
# Model training and evaluation
# ------------------------------
@st.cache_resource
def train_and_evaluate_model(x: pd.DataFrame, y: pd.Series):
    """Train multi-class model for Failure_Mode and report robust evaluation artifacts."""
    shuffled_df = pd.concat([x, y.rename(MODE_COLUMN)], axis=1).sample(frac=1.0, random_state=42).reset_index(drop=True)
    x_shuffled = shuffled_df[REQUIRED_FEATURES]
    y_shuffled = shuffled_df[MODE_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x_shuffled,
        y_shuffled,
        test_size=0.2,
        random_state=42,
        stratify=y_shuffled,
    )

    x_train_bal, y_train_bal = balance_training_set(x_train, y_train)

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=RF_N_ESTIMATORS,
                    random_state=42,
                    max_depth=8,
                    min_samples_split=12,
                    min_samples_leaf=5,
                    max_features="sqrt",
                    class_weight="balanced_subsample",
                    n_jobs=1,
                ),
            ),
        ]
    )

    pipeline.fit(x_train_bal, y_train_bal)

    y_pred = pipeline.predict(x_test)
    y_prob = pipeline.predict_proba(x_test)

    test_metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="macro", zero_division=0),
        "f1": f1_score(y_test, y_pred, average="macro", zero_division=0),
    }

    smallest_class_size = int(y_shuffled.value_counts().min())
    cv_folds = 5
    cv_note = "Using 5-fold stratified cross-validation."
    if smallest_class_size < 5:
        cv_folds = max(2, smallest_class_size)
        cv_note = (
            f"Small minority class ({smallest_class_size} rows). "
            f"Using {cv_folds}-fold CV instead of 5-fold."
        )

    skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    fold_accuracy = []
    fold_precision = []
    fold_recall = []
    fold_f1 = []

    for train_idx, valid_idx in skf.split(x_shuffled, y_shuffled):
        x_fold_train = x_shuffled.iloc[train_idx]
        y_fold_train = y_shuffled.iloc[train_idx]
        x_fold_valid = x_shuffled.iloc[valid_idx]
        y_fold_valid = y_shuffled.iloc[valid_idx]

        x_fold_train_bal, y_fold_train_bal = balance_training_set(x_fold_train, y_fold_train)
        fold_model = clone(pipeline)
        fold_model.fit(x_fold_train_bal, y_fold_train_bal)

        fold_pred = fold_model.predict(x_fold_valid)
        fold_accuracy.append(accuracy_score(y_fold_valid, fold_pred))
        fold_precision.append(precision_score(y_fold_valid, fold_pred, average="macro", zero_division=0))
        fold_recall.append(recall_score(y_fold_valid, fold_pred, average="macro", zero_division=0))
        fold_f1.append(f1_score(y_fold_valid, fold_pred, average="macro", zero_division=0))

    cv_summary = {
        "accuracy_mean": float(np.mean(fold_accuracy)),
        "accuracy_std": float(np.std(fold_accuracy)),
        "precision_mean": float(np.mean(fold_precision)),
        "precision_std": float(np.std(fold_precision)),
        "recall_mean": float(np.mean(fold_recall)),
        "recall_std": float(np.std(fold_recall)),
        "f1_mean": float(np.mean(fold_f1)),
        "f1_std": float(np.std(fold_f1)),
        "folds": cv_folds,
        "note": cv_note,
    }

    x_perm = x_test
    y_perm = y_test
    if len(x_test) > MAX_PERMUTATION_SAMPLE_SIZE:
        perm_idx = x_test.sample(n=MAX_PERMUTATION_SAMPLE_SIZE, random_state=42).index
        x_perm = x_test.loc[perm_idx]
        y_perm = y_test.loc[perm_idx]

    perm_global = permutation_importance(
        pipeline,
        x_perm,
        y_perm,
        n_repeats=6,
        random_state=42,
        scoring="f1_macro",
        n_jobs=1,
    )

    # Class-wise permutation importance to inspect wear-out vs controller drivers.
    class_importance = {}
    for mode in [1, 4]:
        y_test_binary = (y_test == mode).astype(int)

        def class_scorer(estimator, x_eval, y_eval):
            pred_mode = estimator.predict(x_eval)
            pred_binary = (pred_mode == mode).astype(int)
            y_binary = (y_eval == mode).astype(int)
            return f1_score(y_binary, pred_binary, zero_division=0)

        if y_test_binary.sum() > 0:
            perm_mode = permutation_importance(
                pipeline,
                x_perm,
                y_perm,
                n_repeats=4,
                random_state=42,
                scoring=class_scorer,
                n_jobs=1,
            )
            class_importance[mode] = perm_mode.importances_mean
        else:
            class_importance[mode] = np.zeros(len(REQUIRED_FEATURES))

    importance_df = pd.DataFrame(
        {
            "Feature": REQUIRED_FEATURES,
            "Global_Importance": perm_global.importances_mean,
            "Global_Importance_STD": perm_global.importances_std,
            "Wear_Out_Importance": class_importance[1],
            "Controller_Importance": class_importance[4],
        }
    ).sort_values("Global_Importance", ascending=False)

    conf_mat = confusion_matrix(y_test, y_pred, labels=VALID_MODES)
    conf_mat_df = pd.DataFrame(
        conf_mat,
        index=["Actual Healthy (0)", "Actual Wear-Out (1)", "Actual Controller (4)"],
        columns=["Pred Healthy (0)", "Pred Wear-Out (1)", "Pred Controller (4)"],
    )

    return {
        "pipeline": pipeline,
        "x_test": x_test,
        "y_test": y_test,
        "y_prob": y_prob,
        "test_metrics": test_metrics,
        "cv_summary": cv_summary,
        "importance_df": importance_df,
        "conf_mat_df": conf_mat_df,
    }


# ------------------------------
# Sidebar defaults
# ------------------------------
def get_default(df: pd.DataFrame, column: str, fallback: float = 0.0) -> float:
    """Provide a robust numeric default for UI widgets."""
    if column in df.columns and pd.notna(df[column]).any():
        return float(pd.to_numeric(df[column], errors="coerce").median())
    return fallback


# ------------------------------
# Analytics and reporting
# ------------------------------
def calculate_failure_distribution(y_mode: pd.Series) -> dict:
    """Calculate percentage distribution of failure modes."""
    total = len(y_mode)
    counts = y_mode.value_counts().reindex(VALID_MODES, fill_value=0)
    percentages = {
        mode: (int(counts[mode]) / total * 100) if total > 0 else 0.0
        for mode in VALID_MODES
    }
    return percentages


def generate_failure_summary(percentages: dict) -> str:
    """Generate a dynamic summary based on failure distribution."""
    healthy_pct = percentages.get(0, 0)
    wearout_pct = percentages.get(1, 0)
    controller_pct = percentages.get(4, 0)

    summary = []

    if healthy_pct >= 70:
        summary.append(f"<strong>✅ System Health:</strong> Most systems ({healthy_pct:.1f}%) are operating normally with low failure risk.")
    else:
        summary.append(f"<strong>⚠️ System Health:</strong> Only {healthy_pct:.1f}% of systems are fully healthy. Attention required.")

    if wearout_pct >= 20:
        summary.append(f"<strong>📈 Wear-Out Pattern:</strong> {wearout_pct:.1f}% of failures are wear-out related, indicating aging systems. Consider proactive maintenance and component replacement for older units.")
    elif wearout_pct > 0:
        summary.append(f"<strong>📈 Wear-Out Pattern:</strong> {wearout_pct:.1f}% of failures stem from wear-out, a gradual degradation pattern expected in mature deployments.")

    if controller_pct >= 20:
        summary.append(f"<strong>🔧 Controller Issues:</strong> {controller_pct:.1f}% of failures are controller/firmware related. These are often sudden and may require firmware updates or component replacements.")
    elif controller_pct > 0:
        summary.append(f"<strong>🔧 Controller Issues:</strong> {controller_pct:.1f}% of failures involve controller/firmware problems, typically characterized by sudden onset and requiring swift intervention.")

    if healthy_pct < 30 and wearout_pct + controller_pct > 70:
        summary.append("<strong>🚨 Critical Alert:</strong> Field failure rate exceeds 70%. Recommend immediate root cause analysis and preventive recall if necessary.")

    return "<br><br>".join(summary) if summary else "Insufficient data for analysis."


def create_export_dataset(processed_data: pd.DataFrame, y_mode: pd.Series) -> pd.DataFrame:
    """Create a comprehensive export dataset with predictions and failure flags."""
    export_df = processed_data.copy()
    export_df["Predicted_Failure_Mode"] = y_mode.values
    export_df["Failure_Mode_Label"] = y_mode.map(lambda m: MODE_LABELS.get(int(m), "Unknown"))
    export_df["Failure_Flag"] = (y_mode != 0).astype(int)
    return export_df


def _apply_plotly_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk, sans-serif", "color": "#e2e8f0"},
        margin={"l": 20, "r": 20, "t": 55, "b": 20},
        legend={"font": {"color": "#cbd5e1"}, "bgcolor": "rgba(15,23,42,0.35)"},
    )
    return fig


def create_distribution_donut_chart(distribution_data: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        distribution_data,
        values="Count",
        names="Label",
        hole=0.62,
        color="Label",
        color_discrete_map={
            "Healthy": "#22c55e",
            "Wear-Out Failure": "#f59e0b",
            "Controller/Firmware Failure": "#ef4444",
        },
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        pull=[0.015, 0.015, 0.015],
        marker={"line": {"color": "rgba(15,23,42,0.8)", "width": 2}},
        hovertemplate="<b>%{label}</b><br>Share: %{percent}<br>Count: %{value}<extra></extra>",
    )
    fig.update_layout(
        title="Dataset Failure Distribution",
        height=460,
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        legend_title_text="Failure Mode",
    )
    return _apply_plotly_theme(fig)


def create_importance_chart(importance_df: pd.DataFrame) -> go.Figure:
    """Create an interactive horizontal bar chart for feature importance."""
    top_df = importance_df.sort_values("Global_Importance", ascending=True)
    fig = px.bar(
        top_df,
        x="Global_Importance",
        y="Feature",
        orientation="h",
        color="Global_Importance",
        color_continuous_scale=["#1d4ed8", "#06b6d4", "#22c55e"],
        text=top_df["Global_Importance"].map(lambda v: f"{v:.3f}"),
    )
    fig.update_layout(
        title="Global Feature Importance",
        xaxis_title="Permutation Importance",
        yaxis_title="",
        coloraxis_showscale=False,
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.2)")
    fig.update_yaxes(showgrid=False)
    return _apply_plotly_theme(fig)


def get_risk_level(failure_probability: float) -> tuple[str, str]:
    """Map failure probability to a human-readable risk level and accent color."""
    if failure_probability < 0.25:
        return "Low", "#16a34a"
    if failure_probability < 0.60:
        return "Medium", "#f59e0b"
    return "High", "#dc2626"


def generate_prediction_summary(pred_mode: int, probability_map: dict) -> str:
    """Generate a summary based on the live model prediction."""
    healthy_pct = probability_map.get(0, 0.0) * 100
    wear_pct = probability_map.get(1, 0.0) * 100
    controller_pct = probability_map.get(4, 0.0) * 100

    if pred_mode == 0:
        return (
            f"<strong>✅ System is operating normally.</strong> "
            f"Healthy confidence is {healthy_pct:.1f}%, with lower failure probabilities for wear-out ({wear_pct:.1f}%) and controller issues ({controller_pct:.1f}%)."
        )
    if pred_mode == 1:
        return (
            f"<strong>⚠️ System shows signs of aging.</strong> "
            f"Wear-out probability is {wear_pct:.1f}%, which is higher than the healthy confidence ({healthy_pct:.1f}%)."
        )
    return (
        f"<strong>🚨 System may have firmware/controller issues.</strong> "
        f"Controller failure probability is {controller_pct:.1f}%, indicating sudden fault behavior rather than gradual wear-out."
    )


def build_probability_frame(probability_map: dict) -> pd.DataFrame:
    """Convert model probabilities to a display dataframe."""
    return pd.DataFrame(
        {
            "Failure_Mode": VALID_MODES,
            "Label": [MODE_LABELS[m] for m in VALID_MODES],
            "Probability_%": [probability_map[m] * 100 for m in VALID_MODES],
        }
    )


def create_probability_donut_chart(probability_frame: pd.DataFrame) -> go.Figure:
    """Create an interactive donut chart from live prediction probabilities."""
    fig = px.pie(
        probability_frame,
        values="Probability_%",
        names="Label",
        hole=0.60,
        color="Label",
        color_discrete_sequence=["#22c55e", "#f59e0b", "#ef4444"],
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        pull=[0.02, 0.02, 0.02],
        marker={"line": {"color": "rgba(15,23,42,0.85)", "width": 2}},
        hovertemplate="<b>%{label}</b><br>Probability: %{value:.2f}%<extra></extra>",
    )
    fig.update_layout(
        title="Prediction Probability Split",
        height=470,
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        legend_title_text="Failure Mode",
    )
    return _apply_plotly_theme(fig)


def create_probability_bar_chart(probability_frame: pd.DataFrame) -> go.Figure:
    """Create an interactive bar chart from live prediction probabilities."""
    fig = px.bar(
        probability_frame,
        x="Label",
        y="Probability_%",
        color="Label",
        color_discrete_sequence=["#22c55e", "#f59e0b", "#ef4444"],
        text=probability_frame["Probability_%"].map(lambda v: f"{v:.2f}%"),
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_color="rgba(15,23,42,0.85)",
        marker_line_width=1,
    )
    fig.update_layout(
        title="Prediction Probability Breakdown",
        yaxis_title="Probability (%)",
        xaxis_title="",
        showlegend=False,
        transition={"duration": 450, "easing": "cubic-in-out"},
    )
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.2)")
    fig.update_xaxes(showgrid=False)
    return _apply_plotly_theme(fig)


def style_table(df: pd.DataFrame, highlight_columns: list[str] | None = None):
    """Apply readable table styling with alternating rows and highlighted columns."""
    highlight_columns = highlight_columns or []

    def _alternate_rows(data: pd.DataFrame) -> pd.DataFrame:
        colors = [
            "rgba(15, 23, 42, 0.35)" if i % 2 == 0 else "rgba(30, 41, 59, 0.25)"
            for i in range(len(data))
        ]
        return pd.DataFrame(
            [[f"background-color: {color}"] * len(data.columns) for color in colors],
            index=data.index,
            columns=data.columns,
        )

    styler = (
        df.style
        .apply(_alternate_rows, axis=None)
        .set_properties(**{"color": "#e2e8f0", "padding": "0.55rem", "border-color": "rgba(148,163,184,0.22)"})
        .set_table_styles(
            [
                {"selector": "th", "props": "background-color: rgba(14, 116, 144, 0.35); color: #f8fafc; font-weight: 700;"},
                {"selector": "td", "props": "font-size: 0.92rem;"},
            ]
        )
    )

    if highlight_columns:
        styler = styler.set_properties(subset=highlight_columns, **{"font-weight": "700", "color": "#f8fafc"})

    return styler


# ------------------------------
# Recommendation Engine
# ------------------------------
def render_recommendations(pred_mode: int, user_df: pd.DataFrame) -> None:
    """Render recommendations using Streamlit components only."""
    st.subheader("🔧 Recommended Actions")

    if pred_mode == 1:
        st.warning("⚠️ Wear-Out Failure Detected")
        st.write("• Replace CMOS battery soon")
        st.write("• Schedule preventive maintenance")
        st.write("• Monitor system aging metrics")
    elif pred_mode == 4:
        st.error("🚨 Controller/Firmware Failure Detected")
        st.write("• Update BIOS/Firmware")
        st.write("• Run system diagnostics")
        st.write("• Check error logs")
    else:
        st.success("✅ System Healthy")
        st.write("• No immediate action required")

    battery_voltage = float(user_df["Battery_Voltage"].iloc[0])
    boot_errors = int(user_df["Boot_Errors_Count"].iloc[0])
    temperature = float(user_df["Ambient_Temperature_C"].iloc[0])

    if battery_voltage < 2.8:
        st.error(f"🚨 Battery voltage is critically low ({battery_voltage:.2f}V).")
    if boot_errors >= 5:
        st.warning(f"⚠️ Boot errors are high ({boot_errors}).")
    if temperature > 40:
        st.warning(f"⚠️ Ambient temperature is elevated ({temperature:.1f}°C).")


# ------------------------------
# Main app workflow
# ------------------------------
st.sidebar.header("Dataset Source")
uploaded_file = st.sidebar.file_uploader("Upload system telemetry CSV (optional)", type=["csv"])

data = None
data_source_label = ""

if uploaded_file is not None:
    try:
        data = load_dataset_from_upload(uploaded_file.getvalue())
        data_source_label = f"Uploaded file: {uploaded_file.name}"
    except Exception as exc:
        st.error(f"Could not read uploaded dataset: {exc}")
        st.stop()
else:
    try:
        data = load_dataset_from_path(DATA_FILE)
        data_source_label = f"Local file: {DATA_FILE}"
    except FileNotFoundError:
        st.error(
            "Default dataset was not found. Upload a CSV from the sidebar or place "
            "CMOS_Battery_Failure_Dataset.csv next to app.py."
        )
        st.stop()
    except Exception as exc:
        st.error(f"Could not load local dataset: {exc}")
        st.stop()

st.info(f"Using dataset source: {data_source_label}")

try:
    x, y_mode, processed_data = preprocess_data(data)
except Exception as exc:
    st.error(f"Error in preprocessing: {exc}")
    st.stop()

sample_count = len(processed_data)
mode_counts = y_mode.value_counts().reindex(VALID_MODES, fill_value=0)
minority_count = int(mode_counts.min())

try:
    artifacts = train_and_evaluate_model(x, y_mode)
except Exception as exc:
    st.error(f"Error in training/evaluation: {exc}")
    st.stop()

model = artifacts["pipeline"]
test_metrics = artifacts["test_metrics"]
cv_summary = artifacts["cv_summary"]
importance_df = artifacts["importance_df"]
conf_mat_df = artifacts["conf_mat_df"]

if model is None:
    st.warning("Model is not loaded. Please check training pipeline and dataset format.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Manual Inputs")

with st.sidebar.expander("🔋 Electrical Health", expanded=True):
    battery_voltage = st.number_input(
        "Battery Voltage",
        value=get_default(x, "Battery_Voltage", 3.0),
        format="%.3f",
        key="battery_voltage",
    )
    rtc_drift = st.number_input(
        "RTC Drift (sec/day)",
        min_value=0,
        value=int(get_default(x, "RTC_Drift_sec_per_day", 0)),
        step=1,
        key="rtc_drift",
    )

with st.sidebar.expander("📊 System Events", expanded=True):
    boot_errors = st.number_input(
        "Boot Errors",
        min_value=0,
        value=int(get_default(x, "Boot_Errors_Count", 0)),
        step=1,
        key="boot_errors",
    )
    cmos_warning = st.selectbox("CMOS Warning Flag", options=[0, 1], index=0, key="cmos_warning")
    reset_bios = st.selectbox("Reset BIOS Flag", options=[0, 1], index=0, key="reset_bios")

with st.sidebar.expander("🌡️ Environment", expanded=True):
    power_cycle = st.number_input(
        "Power Cycle Count",
        min_value=0,
        value=int(get_default(x, "Power_Cycle_Count", 0)),
        step=1,
        key="power_cycle",
    )
    system_age = st.number_input(
        "System Age (years)",
        min_value=0,
        value=int(get_default(x, "System_Age_Years", 1)),
        step=1,
        key="system_age",
    )
    temperature = st.number_input(
        "Ambient Temperature (C)",
        value=get_default(x, "Ambient_Temperature_C", 25.0),
        format="%.2f",
        key="temperature",
    )

user_df = pd.DataFrame(
    [
        {
            "Battery_Voltage": battery_voltage,
            "RTC_Drift_sec_per_day": rtc_drift,
            "Boot_Errors_Count": boot_errors,
            "CMOS_Warning_Flag": cmos_warning,
            "Reset_BIOS_Flag": reset_bios,
            "Power_Cycle_Count": power_cycle,
            "System_Age_Years": system_age,
            "Ambient_Temperature_C": temperature,
        }
    ]
).reindex(columns=REQUIRED_FEATURES)

prediction_slot = st.empty()
try:
    with st.spinner("Analyzing system..."):
        pred_mode = int(model.predict(user_df)[0])
        pred_probs = model.predict_proba(user_df)[0]
        class_order = list(model.named_steps["model"].classes_)
except Exception as exc:
    st.error(f"Prediction failed: {exc}")
    st.stop()

prob_map = {mode: 0.0 for mode in VALID_MODES}
for label, prob in zip(class_order, pred_probs):
    prob_map[int(label)] = float(prob)

pred_flag = 0 if pred_mode == 0 else 1
failure_probability = prob_map[1] + prob_map[4]
prediction_frame = build_probability_frame(prob_map)
risk_level, risk_color = get_risk_level(failure_probability)
status_label = MODE_LABELS.get(pred_mode, f"Unknown Mode ({pred_mode})")
summary_text = generate_prediction_summary(pred_mode, prob_map)
failure_flag_label = "Healthy" if pred_flag == 0 else "Failure"
confidence_pct = prob_map.get(pred_mode, 0.0) * 100

with prediction_slot.container():
    section_open("🔥 KPI Prediction Cards", "Realtime classification and confidence indicators")

    card1, card2, card3, card4 = st.columns(4)
    with card1:
        status_tone = "healthy" if pred_mode == 0 else "failure"
        st.markdown(
            stat_card("Predicted Status", failure_flag_label, "Current system health", status_tone, "✅"),
            unsafe_allow_html=True,
        )
    with card2:
        st.markdown(
            stat_card("Confidence", f"{confidence_pct:.1f}%", "Predicted-class confidence", "info", "📊"),
            unsafe_allow_html=True,
        )
    with card3:
        risk_tone = "healthy" if risk_level == "Low" else "warning" if risk_level == "Medium" else "failure"
        st.markdown(
            stat_card("Risk Level", risk_level, "Computed from failure probability", risk_tone, "⚠️"),
            unsafe_allow_html=True,
        )
    with card4:
        mode_tone = "healthy" if pred_mode == 0 else "warning" if pred_mode == 1 else "failure"
        st.markdown(
            stat_card("Failure Mode", f"{pred_mode}: {status_label}", "Multi-class mode output", mode_tone, "🚨"),
            unsafe_allow_html=True,
        )

    st.caption(f"Overall failure probability: {failure_probability * 100:.2f}%")
    st.progress(min(max(confidence_pct / 100.0, 0.0), 1.0))
    st.caption("Confidence progress for the predicted class")
    section_close()

    section_open("📊 Charts", "Interactive probability distribution and class confidence visuals")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown(chart_card("Prediction Probability", "Distribution across healthy, wear-out, and controller modes"), unsafe_allow_html=True)
        st.plotly_chart(create_probability_donut_chart(prediction_frame), use_container_width=True)
    with chart_col2:
        st.markdown(chart_card("Probability Breakdown", "Per-class confidence from current telemetry input"), unsafe_allow_html=True)
        st.plotly_chart(create_probability_bar_chart(prediction_frame), use_container_width=True)

    st.markdown("#### Summary Table")
    st.dataframe(
        style_table(prediction_frame, highlight_columns=["Probability_%"]),
        use_container_width=True,
    )
    section_close()

    section_open("🔧 Recommendations", "Actionable response based on predicted failure mode")
    try:
        render_recommendations(pred_mode, user_df)
    except Exception as exc:
        st.warning(f"Could not generate recommendations: {str(exc)[:100]}")
    section_close()

# ========================================
# GLOBAL FEATURE IMPORTANCE SECTION
# ========================================
section_open("📈 Feature Importance", "Global and mode-specific telemetry impact")

importance_col1, importance_col2 = st.columns(2)
with importance_col1:
    st.markdown(chart_card("Global Feature Impact", "Permutation importance on the test split"), unsafe_allow_html=True)
    st.plotly_chart(create_importance_chart(importance_df), use_container_width=True)
with importance_col2:
    st.markdown(chart_card("Mode-Specific Drivers", "Wear-out vs controller contributions"), unsafe_allow_html=True)
    st.dataframe(
        style_table(
            importance_df[["Feature", "Wear_Out_Importance", "Controller_Importance", "Global_Importance"]],
            highlight_columns=["Global_Importance"],
        ),
        use_container_width=True,
    )

top_wear = importance_df.sort_values("Wear_Out_Importance", ascending=False).head(3)
top_controller = importance_df.sort_values("Controller_Importance", ascending=False).head(3)

col_wear, col_ctrl = st.columns(2)
with col_wear:
    st.markdown("Top Wear-Out drivers")
    st.dataframe(style_table(top_wear[["Feature", "Wear_Out_Importance"]]), use_container_width=True)
with col_ctrl:
    st.markdown("Top Controller/Firmware drivers")
    st.dataframe(style_table(top_controller[["Feature", "Controller_Importance"]]), use_container_width=True)

if importance_df.iloc[0]["Feature"] == "Battery_Voltage":
    st.info(
        "Battery voltage remains important, but the model now uses class-balanced training and "
        "mode-specific permutation analysis so wear-out and controller patterns can emerge separately."
    )
section_close()

section_open("🧾 Summary", "Prediction digest for quick decision making")
st.markdown(f'<div class="summary-box">{summary_text}</div>', unsafe_allow_html=True)

st.caption("Prediction updates automatically whenever sidebar inputs change.")
st.dataframe(style_table(user_df), use_container_width=True)
section_close()

section_open("🎯 Model Performance", "Validation metrics and confusion matrix")
perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
with perf_col1:
    st.markdown(stat_card("Accuracy", f"{test_metrics['accuracy'] * 100:.2f}%", "Test split performance", "info", "🎯"), unsafe_allow_html=True)
with perf_col2:
    st.markdown(stat_card("Precision", f"{test_metrics['precision'] * 100:.2f}%", "Macro averaged", "warning", "📌"), unsafe_allow_html=True)
with perf_col3:
    st.markdown(stat_card("Recall", f"{test_metrics['recall'] * 100:.2f}%", "Macro averaged", "info", "🔁"), unsafe_allow_html=True)
with perf_col4:
    st.markdown(stat_card("F1-score", f"{test_metrics['f1'] * 100:.2f}%", "Balanced performance", "healthy", "⭐"), unsafe_allow_html=True)

cv_df = pd.DataFrame(
    {
        "Metric": ["Accuracy", "Precision", "Recall", "F1"],
        "CV Mean": [
            cv_summary["accuracy_mean"],
            cv_summary["precision_mean"],
            cv_summary["recall_mean"],
            cv_summary["f1_mean"],
        ],
        "CV Std": [
            cv_summary["accuracy_std"],
            cv_summary["precision_std"],
            cv_summary["recall_std"],
            cv_summary["f1_std"],
        ],
    }
)
st.caption(f"Cross-validation summary ({cv_summary['folds']}-fold stratified)")
st.caption(cv_summary["note"])
st.dataframe(style_table(cv_df, highlight_columns=["CV Mean"]), use_container_width=True)

st.markdown("### 🧩 Confusion Matrix")
st.dataframe(style_table(conf_mat_df), use_container_width=True)
section_close()

# Analytics and Reporting section
st.divider()
with st.expander("Optional: Dataset Analytics", expanded=False):
    if sample_count < 50:
        st.warning("Dataset too small, results may be inaccurate")
    if minority_count < 10:
        st.warning(
            f"One or more classes have fewer than 10 rows (min={minority_count}). "
            "Class probabilities may be unstable."
        )

    st.markdown("#### Dataset Preview")
    st.dataframe(processed_data.head(25), use_container_width=True)

    dataset_percentages = calculate_failure_distribution(y_mode)
    total_systems = len(processed_data)
    healthy_pct = dataset_percentages[0]
    failure_pct = dataset_percentages[1] + dataset_percentages[4]
    most_common_mode = int(mode_counts.idxmax())
    most_common_label = failure_label(most_common_mode)

    st.markdown("#### Dataset Overview")
    ds_col1, ds_col2, ds_col3, ds_col4 = st.columns(4)
    with ds_col1:
        st.metric("Total Systems", f"{total_systems:,}")
    with ds_col2:
        st.metric("Healthy %", f"{healthy_pct:.1f}%")
    with ds_col3:
        st.metric("Failure %", f"{failure_pct:.1f}%")
    with ds_col4:
        st.metric("Common Class", most_common_label)

    dataset_distribution = pd.DataFrame(
        {
            "Failure_Mode": VALID_MODES,
            "Label": [MODE_LABELS[m] for m in VALID_MODES],
            "Count": [int(mode_counts.loc[m]) for m in VALID_MODES],
            "Percentage": [dataset_percentages[m] for m in VALID_MODES],
        }
    )
    st.markdown("Dataset-based distribution stays available here for reference.")
    st.plotly_chart(create_distribution_donut_chart(dataset_distribution), use_container_width=True)
    st.dataframe(style_table(dataset_distribution, highlight_columns=["Count", "Percentage"]), use_container_width=True)

st.markdown("### 📥 Export Analysis")
export_data = create_export_dataset(processed_data, y_mode)

csv_buffer = io.BytesIO()
export_data.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

st.markdown(
    """
    <div class="download-card">
        <div class="section-title">Download Report</div>
        <div class="section-subtitle">Export all telemetry rows with predicted Failure_Mode and Failure_Flag.</div>
    """,
    unsafe_allow_html=True,
)
st.download_button(
    label="Download Report",
    data=csv_buffer.getvalue(),
    file_name="failure_analysis_report.csv",
    mime="text/csv",
    help="Download all predictions with Failure_Mode and Failure_Flag for further analysis.",
)
st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"Report includes {len(export_data)} systems with predicted failure modes and binary failure flags.")
st.markdown('<div class="footer-note">Built for predictive maintenance | AI-powered system</div>', unsafe_allow_html=True)
