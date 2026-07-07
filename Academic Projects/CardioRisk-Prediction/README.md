# CardioRisk Prediction: CVD Risk Modelling

## Overview

This project develops a machine learning pipeline to predict the risk of cardiovascular disease (CVD) using routine patient health data. The primary objective is to support healthcare providers by creating an effective pre-screening tool that prioritizes high-risk individuals, thereby optimizing consultation time and enabling timely preventative care. The analysis follows a complete data science workflow, from initial data cleaning and exploratory data analysis (EDA) to feature engineering, model building, hyperparameter tuning, and final model selection.

## Recruiter Snapshot

This project demonstrates:
- **End-to-End Classification Workflow:** Building a complete pipeline for a binary classification problem, including data cleaning, feature engineering, model training, and evaluation.
- **Healthcare Data Handling:** Experience with cleaning and preprocessing real-world health data, including identifying and removing physiologically implausible data points.
- **Feature Engineering for Health Metrics:** Creating clinically relevant features like Body Mass Index (BMI) and performing unit conversions for interpretability.
- **Model Comparison and Selection:** Training and evaluating multiple classification algorithms (SVM, Decision Tree, Random Forest) to select the best-performing model based on relevant metrics.
- **Performance Optimization for Clinical Utility:** Optimizing a model for high sensitivity (recall) by adjusting the classification threshold, a critical step for medical screening tools to minimize false negatives.

## Dataset

- **Source:** `health_data.csv`
- **Size:** The raw dataset contains 70,000 patient records with 14 features.
- **Key Features:** The dataset includes metrics such as `age`, `gender`, `height`, `weight`, systolic (`ap_hi`) and diastolic (`ap_lo`) blood pressure, `cholesterol`, `glucose` (`gluc`), and lifestyle indicators (`smoke`, `alco`, `active`).
- **Target Variable:** `cardio` (0 = No Disease, 1 = Disease).
- **Note:** Only a sample of the data is included in this repository. The full dataset is excluded due to size or sensitivity.

## Objectives

- **Predict CVD Risk:** Accurately identify individuals at risk for cardiovascular disease using their health data.
- **Support Preventative Care:** Provide a model that assists in patient triage, allowing doctors to prioritize high-risk patients.
- **Evaluate Multiple Models:** Compare the performance of a linear SVM, a decision tree, and a random forest classifier.
- **Optimize the Model:** Use hyperparameter tuning and cutoff selection to maximize clinically relevant metrics, specifically prioritizing sensitivity (recall).

## Project Workflow

1.  **Data Understanding & Cleaning:**
    - Loaded the dataset and removed non-predictive identifier columns.
    - Identified and removed records with illogical physiological values (e.g., negative weight, diastolic > systolic pressure).
    - Modified the representation of `age` (from days to years) and `height` (from cm to m) for better interpretability.
2.  **Exploratory Data Analysis (EDA):**
    - Performed univariate analysis on numerical and categorical features.
    - Visualized correlations between numerical features using a heatmap.
    - Conducted bivariate analysis to understand the relationship between features and the target variable.
3.  **Feature Engineering:**
    - Created a new feature, `BMI` (Body Mass Index), from `weight` and `height`.
    - Dropped original `height` and `weight` columns to reduce redundancy.
    - One-hot encoded categorical features and scaled all numerical features using `MinMaxScaler`.
4.  **Model Development & Evaluation:**
    - **Trained a Linear SVM:** Established a strong, interpretable baseline.
    - **Trained a Decision Tree Classifier:** Built a simple, transparent model.
    - **Trained a Random Forest Classifier:** Used an ensemble method to improve predictive power and control overfitting.
    - **Hyperparameter Tuning:** Optimized the Random Forest model using `GridSearchCV`.
    - **Threshold Optimization:** Adjusted the classification threshold of the final model to achieve a target sensitivity of at least 80%.
    - **Model Comparison:** Final models were evaluated on their generalization performance.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Data Cleaning** | Identifying and removing illogical physiological values based on domain knowledge. |
| **Exploratory Data Analysis (EDA)** | Histograms, count plots, correlation heatmaps to understand data distributions and relationships. |
| **Feature Engineering** | Creating `BMI` as a composite feature, one-hot encoding categorical variables. |
| **Feature Scaling** | `MinMaxScaler` to normalize numerical features for distance-sensitive algorithms like SVM. |
| **Classification Models** | Linear SVM, Decision Tree, Random Forest. |
| **Hyperparameter Tuning** | `GridSearchCV` to find the optimal parameters for the Random Forest model. |
| **Performance Metrics** | Accuracy, Precision, Recall (Sensitivity), F1-Score, ROC-AUC. |
| **Threshold-Moving** | Adjusting the decision threshold to optimize for high recall, minimizing false negatives. |

## Models Used

- **Linear Support Vector Machine (SVM)**
- **Decision Tree Classifier**
- **Random Forest Classifier (Final Model)**

## Results

| Model | Accuracy | Precision | Recall (Sensitivity) | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| Linear SVM | 0.72 | 0.74 | 0.68 | 0.71 | 0.78 |
| Decision Tree | 0.63 | 0.62 | 0.65 | 0.63 | 0.63 |
| **Random Forest (Tuned)** | **0.72** | **0.72** | **0.72** | **0.72** | **0.79** |

After optimizing the Random Forest cutoff to prioritize sensitivity, the final model achieved **81% recall** on the test set, successfully meeting the clinical requirement.

## Key Insights

- **Key Risk Factors:** Age, cholesterol levels, and high blood pressure were the most significant predictors of cardiovascular disease.
- **Model Suitability:** The Random Forest classifier provided the best balance of performance and robustness, outperforming both the linear SVM and the single Decision Tree.
- **Importance of Optimization:** Standard model performance was insufficient for a clinical setting. By tuning the classification threshold, the model's utility was significantly increased by ensuring most at-risk patients were correctly identified.

## Key Learnings

- **Domain-Specific Data Cleaning:** Real-world data, especially in healthcare, requires domain knowledge to identify and handle errors that are not just statistical outliers but physiologically impossible.
- **Metric Selection is Context-Dependent:** For a medical screening tool, recall (sensitivity) is often more critical than accuracy or precision. A false negative (missing a sick patient) is far more costly than a false positive (flagging a healthy patient for review).
- **The Power of Ensembles:** Random Forest's ability to reduce the variance of individual decision trees led to a more stable and accurate model.

## Future Work

- **Advanced Models:** Experiment with Gradient Boosting models (XGBoost, LightGBM) which often perform best on tabular data.
- **Explainability:** Apply SHAP (SHapley Additive exPlanations) to the final model to better understand the drivers of individual predictions.
- **Cross-Validation Strategy:** Implement a more robust cross-validation strategy, such as stratified k-fold, to ensure stable evaluation, especially with imbalanced datasets.

## Repository Structure

```
CardioRisk-Prediction/
├── CardioRisk_Prediction.ipynb # Jupyter Notebook with the complete analysis
├── README.md                   # Project summary (this file)
└── data/
    └── health_data.csv         # Sample dataset
```

## Notes
- This project was completed as part of an MSc in Machine Learning and Artificial Intelligence. It emphasizes the development of a practical machine learning solution for healthcare, focusing on conceptual understanding, analytical reasoning, and the complete modelling lifecycle rather than deployment.
