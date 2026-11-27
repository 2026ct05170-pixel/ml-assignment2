from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, roc_auc_score, precision_score, recall_score,
                             f1_score, matthews_corrcoef)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

SEED = 42
OUT = Path(__file__).resolve().parent.parent


def main():
    bunch = load_breast_cancer(as_frame=True)
    data = bunch.frame.rename(columns={"target": "target"}).drop_duplicates().reset_index(drop=True)
    # sklearn encodes 0=malignant and 1=benign in this dataset.
    # Preserve the documented mapping; the positive class for binary metrics is benign (1).
    data.to_csv(OUT / "breast_cancer_wisconsin.csv", index=False)
    X, y = data.drop(columns="target"), data["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=SEED
    )
    test = X_test.copy()
    test["target"] = y_test
    test.to_csv(OUT / "test_data.csv", index=False)

    models = {
        "Logistic Regression": Pipeline([("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()), ("model", LogisticRegression(max_iter=5000, random_state=SEED))]),
        "Decision Tree": Pipeline([("impute", SimpleImputer(strategy="median")),
            ("model", DecisionTreeClassifier(random_state=SEED, class_weight="balanced"))]),
        "K-Nearest Neighbors": Pipeline([("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()), ("model", KNeighborsClassifier(n_neighbors=5))]),
        "Gaussian Naive Bayes": Pipeline([("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()), ("model", GaussianNB())]),
        "Random Forest": Pipeline([("impute", SimpleImputer(strategy="median")),
            ("model", RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                              random_state=SEED, n_jobs=-1))]),
        # The assignment's comparison template mentions six models, while the required list names five.
        "RBF Support Vector Machine (additional)": Pipeline([("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()), ("model", SVC(kernel="rbf", probability=True,
                                                           class_weight="balanced", random_state=SEED))]),
    }
    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        prob = model.predict_proba(X_test)[:, 1]
        rows.append({"Model": name,
            "Accuracy": accuracy_score(y_test, pred),
            "AUC": roc_auc_score(y_test, prob),
            "Precision": precision_score(y_test, pred, zero_division=0),
            "Recall": recall_score(y_test, pred, zero_division=0),
            "F1": f1_score(y_test, pred, zero_division=0),
            "MCC": matthews_corrcoef(y_test, pred)})
    results = pd.DataFrame(rows)
    results.to_csv(OUT / "model_metrics.csv", index=False, float_format="%.4f")
    ax = results.set_index("Model")[["Accuracy", "AUC", "Precision", "Recall", "F1"]].plot(
        kind="bar", figsize=(13, 6), ylim=(0, 1.05), rot=20, width=0.8)
    ax.set_ylabel("Score"); ax.set_title("Wisconsin Breast Cancer Model Comparison")
    ax.legend(loc="lower right", ncol=3); ax.grid(axis="y", alpha=.25)
    plt.tight_layout(); plt.savefig(OUT / "metric_comparison.png", dpi=180); plt.close()
    ax = results.set_index("Model")["MCC"].plot(kind="bar", figsize=(12, 5), ylim=(0, 1.05), color="#4776a8")
    ax.set_ylabel("Matthews correlation coefficient"); ax.set_title("MCC by classifier"); ax.grid(axis="y", alpha=.25)
    plt.tight_layout(); plt.savefig(OUT / "mcc_comparison.png", dpi=180); plt.close()
    print("Class distribution (0=malignant, 1=benign):")
    print(data.target.value_counts().sort_index().to_string())
    print("\nTest split metrics:")
    print(results.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nWrote breast_cancer_wisconsin.csv, test_data.csv, model_metrics.csv, metric_comparison.png, mcc_comparison.png")

if __name__ == "__main__":
    main()




