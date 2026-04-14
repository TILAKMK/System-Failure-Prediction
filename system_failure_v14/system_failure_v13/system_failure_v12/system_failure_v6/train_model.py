import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline

DATA_FILE = "CMOS_Battery_Failure_Dataset.csv"
TARGET_COLUMN = "Failure_Mode"
FEATURES = [
    "Battery_Voltage",
    "RTC_Drift_sec_per_day",
    "Boot_Errors_Count",
    "CMOS_Warning_Flag",
    "Reset_BIOS_Flag",
    "Power_Cycle_Count",
    "System_Age_Years",
    "Ambient_Temperature_C",
]


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_FILE)

    missing_features = [c for c in FEATURES if c not in df.columns]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    x = df[FEATURES].apply(pd.to_numeric, errors="coerce")
    y = pd.to_numeric(df[TARGET_COLUMN], errors="coerce")

    valid = y.isin([0, 1, 4])
    x = x.loc[valid].copy()
    y = y.loc[valid].astype(int)

    shuffled = pd.concat([x, y.rename(TARGET_COLUMN)], axis=1).sample(frac=1.0, random_state=42)
    x = shuffled[FEATURES]
    y = shuffled[TARGET_COLUMN]
    return x, y


def main() -> None:
    x, y = load_data()

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=400,
                    random_state=42,
                    max_depth=8,
                    min_samples_split=12,
                    min_samples_leaf=5,
                    class_weight="balanced_subsample",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)
    pred = pipeline.predict(x_test)

    print("Model trained")
    print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")
    print(f"Accuracy:  {accuracy_score(y_test, pred):.4f}")
    print(f"Precision: {precision_score(y_test, pred, average='macro', zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_test, pred, average='macro', zero_division=0):.4f}")
    print(f"F1-score:  {f1_score(y_test, pred, average='macro', zero_division=0):.4f}")

    print("\nClassification report:")
    print(classification_report(y_test, pred, labels=[0, 1, 4], target_names=["Healthy", "Wear-Out", "Controller/Firmware"], zero_division=0))

    cm = confusion_matrix(y_test, pred, labels=[0, 1, 4])
    print("Confusion matrix (rows=actual, cols=pred):")
    print(cm)

    class_counts = y.value_counts().sort_index()
    min_class = int(class_counts.min())
    cv_folds = 5 if min_class >= 5 else max(2, min_class)
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

    cv_results = cross_validate(
        pipeline,
        x,
        y,
        cv=cv,
        scoring={
            "accuracy": "accuracy",
            "precision": "precision_macro",
            "recall": "recall_macro",
            "f1": "f1_macro",
        },
        n_jobs=-1,
    )

    print(f"\nCross-validation ({cv_folds}-fold)")
    print(f"Accuracy : {np.mean(cv_results['test_accuracy']):.4f} +/- {np.std(cv_results['test_accuracy']):.4f}")
    print(f"Precision: {np.mean(cv_results['test_precision']):.4f} +/- {np.std(cv_results['test_precision']):.4f}")
    print(f"Recall   : {np.mean(cv_results['test_recall']):.4f} +/- {np.std(cv_results['test_recall']):.4f}")
    print(f"F1       : {np.mean(cv_results['test_f1']):.4f} +/- {np.std(cv_results['test_f1']):.4f}")

    with open("model.pkl", "wb") as f:
        pickle.dump(pipeline, f)

    print("Saved model.pkl")


if __name__ == "__main__":
    main()
