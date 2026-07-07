# Car Price Prediction with Regularised Linear Models

## Overview

This project develops a robust regression model to predict used car prices based on a variety of vehicle features, specifications, and condition indicators. The work focuses on a complete machine learning workflow: from exploratory data analysis and feature engineering to model development, regularisation, and evaluation.

The primary objective is to build a predictive model suitable for a reseller or marketplace platform to support price benchmarking, feature valuation, and inventory decisions. A secondary objective is to investigate feature importance and the effect of regularisation techniques (Ridge and Lasso) on a highly collinear dataset.

## Dataset

- **Source:** Provided dataset `Car_Price_data.csv`
- **Characteristics:** The dataset contains 15,915 records and 23 columns, including both numerical features (e.g., `km`, `hp_kW`) and categorical features (e.g., `make_model`, `Fuel`). The target variable for prediction is the car's `price`.
- **Note:** Only sample data is included in this repository for illustration. The full dataset is excluded.

## Objectives

The project was guided by the following objectives:

- **Price Prediction:** Develop a model to accurately predict used car prices from the provided features.
- **Market Analysis:** Explore price trends and the relationship between different features and the target variable.
- **Feature Importance:** Identify the most influential factors determining car prices.
- **Regularisation:** Apply and compare Ridge and Lasso regression to manage multicollinearity and enhance model robustness and interpretability.

## Project Workflow

1.  **Data Loading and Initial Inspection:** Loaded the dataset and performed an initial sanity check of its structure, data types, and basic statistics.
2.  **Data Cleaning & Preprocessing:**
    - Confirmed the absence of missing values.
    - Addressed class imbalances and consolidated rare categories in categorical features (e.g., consolidating `Type` into `Used` and `New/Pre-registered`).
    - Log-transformed the target variable `price` to correct for significant right-skewness, resulting in a `log_price` target.
3.  **Exploratory Data Analysis (EDA) & Visualisation:**
    - Analyzed the distribution of numerical features to identify skewness.
    - Visualized frequency distributions of categorical features to spot imbalances.
    - Used a correlation matrix to understand the relationships between numerical features and the target.
    - Employed grouped bar plots to analyze how average `log_price` varies across different categories.
4.  **Outlier Analysis & Handling:**
    - Identified outliers in numerical features using the IQR method and boxplots.
    - Capped (Winsorized) outliers instead of removing them to preserve sample size and market coverage.
5.  **Feature Engineering:**
    - Split the `make_model` column into `make` and `model` for better granularity.
    - Processed four specification columns (e.g., `Comfort_Convenience`) containing comma-separated lists into binary indicator variables.
    - Applied threshold-based pruning to retain only features present in a meaningful proportion of the data.
    - One-hot encoded categorical variables.
6.  **Data Splitting:** Split the dataset into an 80% training set and a 20% testing set.
7.  **Feature Scaling:** Applied `StandardScaler` on the training and testing sets to standardise features for regularisation.
8.  **Model Development & Evaluation:**
    - **Baseline Linear Regression:** Established a performance baseline without any regularisation.
    - **Ridge Regression:** Conducted a hyperparameter search (`alpha`) to find the optimal regularisation strength.
    - **Lasso Regression:** Conducted a hyperparameter search (`alpha`) to find the optimal regularisation strength and assess its feature-selection capability.
9.  **Final Model Comparison:** Compared the performance of Linear, Ridge, and Lasso regressions on key metrics.

## Techniques and Concepts Applied

- **Missing Value Treatment:** Checked for and identified no missing data.
- **Outlier Detection & Treatment:** Used boxplots and the IQR method to identify and cap outliers.
- **Target Transformation:** Applied a log transformation (using `np.log1p`) to the target variable `price` to improve its distribution for linear modelling.
- **Correlation Analysis:** Used a correlation matrix and heatmap to analyse relationships between numeric features and the target.
- **One-Hot Encoding:** Transformed categorical features into a machine-readable numeric format.
- **Multi-Label Feature Engineering:** Parsed comma-separated feature lists into individual binary indicators to capture rich specification data.
- **Feature Importance Analysis:** Analysed coefficients from Lasso and Ridge models to identify key price drivers.
- **Hyperparameter Tuning with `GridSearchCV`:** Used grid search to find optimal alpha values for Ridge and Lasso regressions.
- **K-Fold Cross-Validation:** Used within `GridSearchCV` for robust hyperparameter selection.
- **Winsorization (Outlier Capping):** Capped outlier values to reduce their influence without deleting data points.
- **Variance Inflation Factor (VIF) Analysis:** Calculated VIF to detect multicollinearity, justifying the use of regularised regression methods.

## Models Used

1.  **Baseline Linear Regression:** A standard OLS model was trained as a benchmark.
2.  **Ridge Regression:** L2 regularisation was applied to shrink coefficients and stabilise the model against multicollinearity.
3.  **Lasso Regression:** L1 regularisation was applied to shrink coefficients and perform feature selection by driving some coefficients to zero.

**Key Observations:** The choice of preprocessing steps (like target transformation and outlier capping) had a more significant impact on model stability and performance than the choice of regularisation. Ridge and Lasso models confirmed the baseline model's stability, demonstrating that the solution was already reasonably stable under multicollinearity. While Ridge is recommended for its coefficient stabilisation, its predictive performance was near-identical to the linear and Lasso models.

## Results

All models were evaluated on the transformed `log_price` scale.

**Key Metrics (Baseline Linear Regression):**

| Metric | Train | Test |
| :--- | :--- | :--- |
| **R²** | 0.7985 | 0.7847 |
| **RMSE** | 0.18 | 0.18 |
| **MAE** | 0.14 | 0.14 |

**Model Comparison:**

| Model | Best Alpha | Test MAE | Test R² |
| :--- | :--- | :--- | :--- |
| Baseline Linear | N/A | 0.14 | 0.7847 |
| **Ridge Regression** | **0.000800** | **0.1432** | **0.7847** |
| Lasso Regression | 0.000100 | 0.1432 | 0.7847 |

The most significant finding from the analysis was that the **log-transformation of the target variable** was the single most important modelling decision, reducing skewness from **1.236** to **-0.031**. This correction made the target much more compatible with linear models and likely contributed more to performance than the choice between linear and regularised models.

## Key Insights

- **Vehicle Power and Transmission:** Features like `hp_kW`, `Gears`, and `Displacement_cc` show a positive correlation with car price.
- **Vehicle Age and Mileage:** `age` and `km` are strong negative price signals, aligning with standard depreciation and wear-and-tear expectations.
- **Vehicle Segment:** The grouped mean-price plots demonstrated clear pricing differences across `make_model`, `body_type`, and `Type` categories. `New/Pre-registered` vehicles, for instance, were valued higher than `Used` ones.
- **Specifications:** Premium features related to upholstery (`Part/Full Leather`) and gearing (`Automatic`) were associated with higher average prices.
- **Analysis:** Regularisation was not necessary for performance gain but was vital for model validation and stability.

## Key Learnings

- **Importance of Target Transformation:** The substantial impact of the log transformation highlighted how crucial it is to address severe skewness in a target variable to fulfil the normality assumptions of linear models and improve predictive accuracy.
- **The Role of Preprocessing:** The analysis demonstrated that comprehensive data cleaning and feature engineering steps (like category consolidation and outlier capping) can be more impactful than simply choosing a more advanced model.
- **Understanding Feature Signals:** The exploratory analysis and correlation study helped confirm real-world relationships, such as the negative impact of age and mileage and the positive premium for performance and luxury features.
- **Model Sufficiency:** While linear models (regularised or not) offer a good baseline and can explain a substantial portion of price variation (≈78%), the residual analysis indicated that the linearity assumption is approximate, suggesting potential value in exploring more complex models.
- **Residual Analysis for Validation:** Checking residual plots against fitted values and normality assumptions was essential to validate that the model was well-behaved and to understand its limitations.

## Repository Structure

Car-Price-Prediction/
├── data/
│ └── sample/ # Sample data (full dataset excluded)
├── CarPricePrediction.ipynb # Main analysis notebook
├── report.pdf # Full project report
└── README.md # This file


## Notes

- The full dataset is excluded from this repository due to its size. Only sample data is provided.
- This project was completed as part of my MSc in Machine Learning and Artificial Intelligence.
- The focus of this portfolio piece is on data processing, analytical reasoning, model evaluation, and understanding core machine learning concepts, rather than on production-level deployment.