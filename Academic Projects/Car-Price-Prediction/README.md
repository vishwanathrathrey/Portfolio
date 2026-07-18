# Car Price Prediction with Regularised Linear Models

## Overview

This project develops a robust regression model to predict used car prices based on a variety of vehicle features, specifications, and condition indicators. The work focuses on a complete machine learning workflow: from exploratory data analysis and feature engineering to model development, regularisation, and evaluation. The primary objective is to build a predictive model suitable for a reseller or marketplace platform to support price benchmarking and feature valuation.

## Recruiter Snapshot

This project demonstrates:
- **End-to-End Regression Workflow:** Execution of a full machine learning pipeline, from data cleaning and EDA to model training and evaluation.
- **Feature Engineering & Preprocessing:** Competency in transforming raw data into model-ready features, including handling skewed data, outlier capping, and one-hot encoding.
- **Regularization Techniques:** Practical application and comparison of Ridge (L2) and Lasso (L1) regularization to manage multicollinearity and improve model generalization.
- **Hyperparameter Optimization:** Use of cross-validation to systematically tune model hyperparameters (`alpha`) for optimal performance.
- **Data-Driven Interpretation:** Analysis of model coefficients to identify key drivers of car prices and provide actionable business insights.

## Dataset

- **Source:** Provided dataset `Car_Price_data.csv`
- **Characteristics:** The dataset contains 15,915 records and 23 columns, including both numerical features (e.g., `km`, `hp_kW`) and categorical features (e.g., `make_model`, `Fuel`). The target variable for prediction is the car's `price`.
- **Note:** Only sample data is included in this repository for illustration. The full dataset is excluded.

## Objectives

- **Price Prediction:** Develop a model to accurately predict used car prices from the provided features.
- **Market Analysis:** Explore price trends and the relationship between different features and the target variable.
- **Feature Importance:** Identify the most influential factors determining car prices.
- **Regularisation:** Apply and compare Ridge and Lasso regression to manage multicollinearity and enhance model robustness and interpretability.

## Project Workflow

1.  **Data Loading and Initial Inspection:** Loaded the dataset and performed an initial sanity check of its structure, data types, and basic statistics.
2.  **Data Cleaning & Preprocessing:**
    - Confirmed the absence of missing values.
    - Log-transformed the target variable `price` to correct for significant right-skewness, resulting in a `log_price` target.
3.  **Exploratory Data Analysis (EDA) & Visualisation:**
    - Analyzed the distribution of numerical features to identify skewness.
    - Visualized relationships between key features and `log_price` using scatter plots and heatmaps.
    - Employed grouped bar plots to analyze how average `log_price` varies across different categories.
4.  **Outlier Analysis & Handling:**
    - Identified outliers in numerical features using the IQR method and boxplots.
    - Capped (Winsorized) outliers instead of removing them to preserve sample size and market coverage.
5.  **Feature Engineering:**
    - Split the `make_model` column into `make` and `model` for better granularity.
    - Created a `car_age` feature from the `year` column.
    - One-hot encoded categorical variables.
6.  **Data Splitting:** Split the dataset into an 80% training set and a 20% testing set.
7.  **Feature Scaling:** Applied `StandardScaler` on the training and testing sets to standardise features for regularisation.
8.  **Model Development & Evaluation:**
    - **Baseline Linear Regression:** Established a performance baseline without any regularisation.
    - **Ridge Regression:** Implemented Ridge with cross-validation to find the optimal `alpha` for L2 regularization.
    - **Lasso Regression:** Conducted a hyperparameter search (`alpha`) to find the optimal regularisation strength and assess its feature-selection capability.
9.  **Final Model Comparison:** Compared the performance of Linear, Ridge, and Lasso regressions on key metrics.

## Techniques Applied

| Technique | Application |
|---|---|
| **Data Preprocessing** | Log transformation for skewed data, outlier capping (Winsorization) |
| **Feature Engineering** | Creating new features (`car_age`), splitting columns (`make`, `model`) |
| **Encoding & Scaling** | One-hot encoding for categorical data, `StandardScaler` for numerical data |
| **Regression Modeling** | Linear Regression, Ridge Regression (L2), Lasso Regression (L1) |
| **Regularization** | Managing multicollinearity and preventing overfitting |
| **Hyperparameter Tuning** | Using cross-validation to find the optimal `alpha` for Ridge and Lasso |
| **Model Evaluation** | R-squared, Mean Absolute Error (MAE), Root Mean Squared Error (RMSE) |

## Models Used

- **Linear Regression (Baseline)**
- **Ridge Regression**
- **Lasso Regression**

## Results

| Model | R-squared (Test Set) | MAE (Test Set) | RMSE (Test Set) | Key Finding |
|---|---|---|---|---|
| **Linear Regression** | 0.7847 | 0.1432 | 0.1800 | Strong baseline but susceptible to multicollinearity. |
| **Ridge Regression** | 0.7847 | 0.1432 | 0.1800 | Performed similarly to linear regression, effectively shrinking coefficients. |
| **Lasso Regression** | 0.7847 | 0.1432 | 0.1800 | Achieved comparable performance while performing automatic feature selection. |

## Key Insights

- **Top Price Influencers:** `car_age`, `hp_kW` (horsepower), and `make` were consistently the most significant predictors of price.
- **Minimal Regularization Impact on Performance:** The performance metrics for all three models are nearly identical because the optimal regularization strength (`alpha`) found during hyperparameter tuning was extremely close to zero. This indicates that for this dataset, the baseline linear model was not significantly overfitting, and the regularization penalty was too small to cause a noticeable change in predictive accuracy.
- **Feature Selection:** Lasso regression successfully zeroed out coefficients of less important features, demonstrating its utility for creating more interpretable and simpler models even when performance metrics don't change.
- **Model Stability:** Both Ridge and Lasso produced more stable models by penalizing large coefficient values, making them robust to collinear features, which was their primary benefit in this analysis.

## Key Learnings

- The importance of handling skewed target variables (like price) through transformations to meet the assumptions of linear models.
- The practical difference between Ridge and Lasso: Ridge shrinks coefficients towards zero, while Lasso can eliminate them entirely, performing implicit feature selection.
- A systematic approach to the machine learning workflow, from data inspection to model comparison, is crucial for building reliable predictive models.

## Future Work

- **Advanced Models:** Explore non-linear models like Gradient Boosting (e.g., XGBoost, LightGBM) or neural networks to potentially capture more complex relationships and improve accuracy.
- **Expanded Feature Engineering:** Incorporate external data, such as macroeconomic indicators or regional demand data, to enhance predictive power.
- **Deployment:** Package the final model into a simple API (e.g., using Flask or FastAPI) to serve predictions.

## Repository Structure

```
Car-Price-Prediction/
├── CarPricePrediction.ipynb    # Jupyter Notebook with the complete analysis
├── README.md                   # Project summary (this file)
└── data/
    └── sample/                 # Directory for sample data
```

## Notes

- The focus of this portfolio piece is on data processing, analytical reasoning, model evaluation, and understanding core machine learning concepts, rather than on production-level deployment.
- This project was completed as part of an MSc in Machine Learning and Artificial Intelligence.
