# CardioRisk Prediction: CVD Risk Modelling

## Overview

This project develops a machine learning pipeline to predict the risk of cardiovascular disease (CVD) using routine patient health data. The primary objective is to support healthcare providers by creating an effective pre-screening tool that prioritizes high-risk individuals, thereby optimizing consultation time and enabling timely preventative care. The analysis follows a complete data science workflow, from initial data cleaning and exploratory data analysis (EDA) to feature engineering, model building, hyperparameter tuning, and final model selection.

## Dataset

- **Source:** `health_data.csv`
- **Size:** The raw dataset contains 70,000 patient records with 14 features.
- **Key Features:** The dataset includes metrics such as `age`, `gender`, `height`, `weight`, systolic (`ap_hi`) and diastolic (`ap_lo`) blood pressure, `cholesterol`, `glucose` (`gluc`), and lifestyle indicators (`smoke`, `alco`, `active`).
- **Target Variable:** `cardio` (0 = No Disease, 1 = Disease).
- **Note:** Only a sample of the data is included in this repository. The full dataset is excluded due to size or sensitivity.

## Objectives

- **Predict CVD Risk:** Accurately identify individuals at risk for cardiovascular disease using their health data.
- **Support Preventative Care:** Provide a model that assists CardioCare in patient triage, allowing doctors to prioritize high-risk patients and optimize consultation time.
- **Evaluate Multiple Models:** Compare the performance of a linear SVM, a decision tree, and a random forest classifier.
- **Optimize the Model:** Use hyperparameter tuning and cutoff selection to maximize clinically relevant metrics, specifically prioritizing sensitivity (recall) to minimize false negatives.

## Project Workflow

1.  **Data Understanding & Cleaning:**
    - Loaded the dataset and removed non-predictive identifier columns (`Unnamed: 0`, `id`).
    - Addressed invalid physiological values by filtering out records where blood pressure, height, or weight fell outside reasonable limits, and removed cases where systolic pressure was lower than diastolic pressure.
    - Modified the representation of `age` (from days to years) and `height` (from cm to m) for better interpretability.

2.  **Exploratory Data Analysis (EDA):**
    - Performed univariate analysis on numerical and categorical features.
    - Analyzed correlations between numerical features using a heatmap, revealing relationships that justified the creation of a new feature.
    - Conducted bivariate analysis to understand the relationship between features and the target variable, including analyzing the proportion of `cardio=1` across categories and comparing distributions.

3.  **Feature Engineering:**
    - Created a new feature, `BMI` (Body Mass Index), from `weight` and `height` as a standard and interpretable health metric.
    - Consolidated low-frequency categories in `cholesterol` and `gluc` (merging level 3 into level 2) to reduce sparsity.
    - One-hot encoded categorical features and scaled all numerical features using `MinMaxScaler` to prepare the data for modelling.

4.  **Model Development & Evaluation:**
    - **Trained a Linear SVM:** Established a strong, interpretable baseline for tabular data.
    - **Trained a Decision Tree:** Developed a model with built-in feature importance and high interpretability.
    - **Trained a Random Forest:** Included as a third model to compare against simpler algorithms.
    - **Cutoff Selection:** For the SVM and Decision Tree, we went beyond the default 0.5 threshold. The optimal cutoff was determined by analyzing the trade-off between sensitivity (recall) and specificity, with the business goal of prioritizing the identification of high-risk individuals (minimizing false negatives).
    - **Hyperparameter Tuning:** Used `GridSearchCV` on the decision tree, optimizing for recall, to find the best configuration and mitigate overfitting.
    - **Model Comparison:** Final models were evaluated on their generalization performance.

## Techniques and Concepts Applied

- **Data Cleaning:** Identifying and removing illogical physiological values.
- **Exploratory Data Analysis (EDA):** Histograms, count plots, and correlation heatmaps.
- **Bivariate Analysis:** Grouped analysis of categorical features and box plots for numerical features vs. target.
- **Feature Engineering:** Deriving `BMI` and consolidating categories to reduce data sparsity.
- **Feature Encoding:** One-hot encoding (`pd.get_dummies`).
- **Feature Scaling:** `MinMaxScaler`.
- **Model Interpretability:** Analyzed Decision Tree feature importance scores.
- **Model Selection & Tuning:** GridSearchCV for hyperparameter tuning.
- **Threshold Optimization:** ROC-AUC analysis, sensitivity-specificity analysis, and precision-recall curves to select an optimal classification cutoff, prioritizing recall.
- **Model Evaluation:** Accuracy, Precision, and Recall metrics.

## Models Used

| Model | Purpose & Reasoning |
| :--- | :--- |
| **Linear SVM** | A strong, fast, and stable baseline model for tabular data. It showed the best balance of generalization and performance. |
| **Decision Tree** | A highly interpretable model that provides feature importance scores. The model was tuned using `GridSearchCV`. |
| **Random Forest**| An ensemble method included for comparison. It overfit heavily despite its high training performance. |

## Results

### Model Performance (Test Set)

| Model | Accuracy | Precision | Recall |
| :--- | :--- | :--- | :--- |
| **Linear SVM** (Selected) | **0.7268** | **0.7442** | **0.6824** |
| **Tuned Decision Tree** | 0.7282 | 0.7520 | 0.6724 |
| **Random Forest** | 0.7116 | 0.7131 | 0.6977 |

**Summary of Findings:**
- The **Linear SVM** was selected as the final model. It provides the best combination of stable generalization and clinically useful recall, avoiding the severe overfitting observed in the random forest model.
- The **Tuned Decision Tree** achieved comparable accuracy to the SVM but had a slightly lower recall. Tuning the tree (`criterion='gini', max_depth=5, min_samples_leaf=4, min_samples_split=2`) successfully controlled overfitting.
- The **Random Forest** model severely overfit the training data (achieving near-perfect scores), which resulted in significantly lower performance on the test set, making it unsuitable for deployment without stronger regularization.

## Key Insights

- **Strongest Predictors:** EDA and feature importance analysis confirmed medical intuition: age, blood pressure, `BMI`, cholesterol, and glucose are the strongest indicators of cardiovascular disease risk.
- **Importance of Threshold Tuning:** The project demonstrated that selecting an optimal probability cutoff (0.43) based on the business goal (prioritizing recall) is as important as model selection. This allowed us to reduce the number of false negatives compared to using the default threshold of 0.5.
- **Feature Engineering:** Creating `BMI` proved to be a valuable step, providing a consolidated and interpretable health metric that contributed to the model's predictive power.
- **Overfitting:** The random forest's performance highlights the risk of using highly complex models on this data without heavy regularization. The simpler and more interpretable SVM was ultimately more robust and reliable.

## Key Learnings

- **Data Quality is Foundational:** The initial step of cleaning illogical physiological data (`ap_hi`, `ap_lo`, `height`, `weight`) was crucial for building a reliable model.
- **Model Interpretability:** While the random forest had the highest recall, the SVM's balance and the Decision Tree's interpretability (from feature importance) proved to be significant advantages for a healthcare application.
- **Real-World Constraints:** Prioritizing recall over a simple accuracy metric is a common and essential practice in medical risk screening. The project highlighted that model selection and tuning should always be driven by the specific business objective.
- **`GridSearchCV`:** Using a grid search with a recall scoring metric was key to finding a decision tree configuration that minimized false negatives and didn't overfit.

## Repository Structure
CardioRisk-Prediction/
├── data/
│ └── health_data.csv # Sample data
├── CardioRisk_Prediction.ipynb # Full Jupyter Notebook
├── report.pdf # Comprehensive project report
└── README.md # Project overview


## Notes

- **Data:** The full `health_data.csv` is excluded from this repository. The provided data is a sample to demonstrate the structure of the dataset.
- **Academic Project:** This work was completed as part of an MSc in Machine Learning and Artificial Intelligence. It emphasizes the development of a practical machine learning solution for healthcare, focusing on conceptual understanding, analytical reasoning, and the complete modelling lifecycle rather than deployment.