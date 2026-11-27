# Classification Model Comparison for Breast Cancer Diagnosis

## Problem statement
Compare the five required classifiers for predicting whether a breast mass is malignant or benign using the Wisconsin Diagnostic Breast Cancer dataset. The assignment's comparison table says six models, so an RBF Support Vector Machine is included as a clearly labelled additional model.

## Dataset description
The Wisconsin Diagnostic Breast Cancer dataset contains 569 observations and 30 numeric measurements from digitized fine needle aspirate images. The target is `target`: `0` is malignant and `1` is benign. The dataset has 212 malignant (37.3%) and 357 benign (62.7%) observations. The predictors are continuous numeric features; no categorical encoding is needed. Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic). The experiment used scikit-learn's bundled copy of this dataset.

## GitHub Repository Link
[https://github.com/2026ct05170-pixel/ml-assignment2](https://github.com/2026ct05170-pixel/ml-assignment2)

## Preprocessing
The source dataset has no missing values or duplicate rows. The code removes duplicate rows if any occur and uses a median imputer fitted inside each model pipeline. The 80:20 train-test split is stratified and uses `random_state=42`. Scaling is applied inside pipelines for Logistic Regression, KNN, Gaussian Naive Bayes, and SVM; tree models do not require scaling. Preprocessing is fit only on training data. For the listed Precision, Recall, F1, and AUC metrics, benign (label 1) is the positive class. Malignant-class recall should also be considered because false negatives for malignant cases are important.

## Models used and results
All models were evaluated on the same held-out test split in the BITS Virtual Lab. Scores are rounded to four decimal places. The comparisons are shown below.

| Model | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9825 | 0.9954 | 0.9861 | 0.9861 | 0.9861 | 0.9623 |
| Decision Tree | 0.9298 | 0.9296 | 0.9571 | 0.9306 | 0.9437 | 0.8513 |
| K-Nearest Neighbors | 0.9561 | 0.9788 | 0.9589 | 0.9722 | 0.9655 | 0.9054 |
| Gaussian Naive Bayes | 0.9298 | 0.9868 | 0.9444 | 0.9444 | 0.9444 | 0.8492 |
| Random Forest | 0.9474 | 0.9937 | 0.9583 | 0.9583 | 0.9583 | 0.8869 |
| RBF Support Vector Machine (additional) | 0.9649 | 0.9940 | 0.9857 | 0.9583 | 0.9718 | 0.9260 |

![Grouped metric comparison](figures/metric_comparison.svg)

![Matthews correlation comparison](figures/mcc_comparison.svg)

### Observations
Logistic Regression performed best on this fixed split, with the highest accuracy (0.9825), AUC (0.9954), F1 (0.9861), and MCC (0.9623). The RBF SVM was close, with 0.9649 accuracy, 0.9940 AUC, and 0.9260 MCC. KNN had the highest benign-class recall (0.9722) among the tested models. The Decision Tree and Gaussian Naive Bayes had the lowest MCC values (0.8513 and 0.8492). These results compare one stratified split only; repeated cross-validation would provide a more stable estimate of performance.

## Model configurations and execution

| Model | Configuration |
|---|---|
| Logistic Regression | Standard scaling, max_iter=5000, seed=42 |
| Decision Tree | Balanced class weights, seed=42 |
| K-Nearest Neighbors | k=5, standard scaling |
| Gaussian Naive Bayes | Standard scaling |
| Random Forest | 300 trees, balanced class weights, seed=42 |
| RBF Support Vector Machine (additional) | RBF kernel, balanced class weights, standard scaling, seed=42 |

In the project directory, install dependencies with `python -m pip install -r requirements.txt`, then run `python model/model_comparison.py`. The script writes the complete dataset CSV, the held-out `test_data.csv`, `model_metrics.csv`, and two graph PNG files into the project directory. The score table above was produced by running the same model logic in the BITS Virtual Lab; the local `model_metrics.csv` records those values.

## Screenshot

![BITS Virtual Lab model execution](bits_virtual_lab_execution.png)
The genuine BITS Virtual Lab screenshot shows the class counts and all six model results. It is included in the final report.




