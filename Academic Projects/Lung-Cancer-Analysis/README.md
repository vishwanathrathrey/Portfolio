# Lung Cancer Patient Data Analysis with PySpark

## Overview

This project performs a comprehensive analysis of a large-scale lung cancer patient dataset (890,000 records) using Apache PySpark. The analysis focuses on uncovering patterns related to treatment duration, survival rates, geographical variations in cancer staging, and the characteristics of high-risk patient cohorts. The workflow demonstrates a practical application of big data technologies for healthcare analytics, translating key medical questions into scalable data processing queries.

## Recruiter Snapshot

This project demonstrates:
- **Big Data Processing with PySpark:** Proficiency in using Apache PySpark for large-scale data ingestion, cleaning, and analysis on a distributed computing framework, essential for handling healthcare data at scale.
- **Healthcare Data Analytics:** Competency in performing targeted analyses on medical data, including treatment effectiveness (duration), survival rate calculation, and geographical pattern detection.
- **Advanced Data Cleaning:** Skill in handling real-world data quality issues in a big data context, including duplicate removal, data type casting, date transformations, and string standardization.
- **Complex Analytical Querying:** Ability to construct complex analytical queries with multiple filtering conditions and joins to identify and analyze specific, high-risk patient subpopulations.
- **Actionable Insight Generation:** Experience in deriving meaningful insights from large datasets to answer specific questions about treatment protocols, patient outcomes, and public health trends.

## Dataset

- **Source**: Synthetic lung cancer patient dataset
- **Format**: CSV
- **Size**: 890,000 patient records after cleaning
- **Key Features**: `age`, `gender`, `country`, `diagnosis_date`, `cancer_stage`, `family_history`, `smoking_status`, `treatment_type`, `end_treatment_date`, `survived`
- **Note**: Full dataset is excluded; sample data is provided for reference.

## Objectives

- Perform comprehensive data cleaning and standardization on a large healthcare dataset using PySpark.
- Analyze treatment duration patterns across different therapy types.
- Identify the impact of smoking status on survival rates.
- Determine countries with the highest percentage of Stage IV (advanced) cancer diagnoses.
- Analyze the characteristics of a predefined high-risk patient cohort.
- Demonstrate advanced PySpark DataFrame operations for healthcare analytics.

## Project Workflow

1.  **Environment Setup & Data Loading:**
    - Initialized a `SparkSession`.
    - Loaded the 890,000-record dataset into a PySpark DataFrame.
2.  **Data Cleaning and Standardization:**
    - Removed duplicate records.
    - Standardized binary string columns (e.g., 'Yes'/'No') to integer format (1/0).
    - Cast columns to appropriate data types (`IntegerType`, `DoubleType`, `DateType`).
    - Converted string dates to `DateType` using `to_date()`.
    - Trimmed whitespace from all string columns.
3.  **Treatment Duration Analysis:**
    - Calculated treatment duration in days using `datediff()` between `end_treatment_date` and `diagnosis_date`.
    - Grouped by `treatment_type` to find the average treatment duration for each therapy.
4.  **Smoking Status and Survival Analysis:**
    - Grouped patients by `smoking_status`.
    - Calculated the average survival rate for each category to identify the group with the best outcomes.
5.  **Geographical Analysis of Advanced Cancer:**
    - Calculated the total patient count per country.
    - Counted Stage IV diagnoses per country.
    - Computed the percentage of Stage IV cases for each country and identified the top 3.
6.  **High-Risk Patient Profile Analysis:**
    - Filtered for a specific high-risk cohort: Male, Stage III/IV, family history, current smoker, and BMI > 30 who survived.
    - Analyzed the characteristics (e.g., average age, hypertension rate) of this specific subpopulation.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Apache PySpark** | End-to-end use of the distributed data processing framework for big data analytics. |
| **Large-Scale Data Cleaning** | `dropDuplicates()`, type casting, string standardization, and date conversion on a large dataset. |
| **Temporal Analysis** | Using `datediff()` and `to_date()` to calculate and analyze time-based metrics like treatment duration. |
| **GroupBy Aggregations** | Extensive use of `groupBy()` and `agg()` with `avg()` and `count()` for statistical analysis. |
| **Complex Filtering** | Combining multiple boolean conditions to isolate and analyze specific high-risk patient cohorts. |
| **DataFrame Joins** | Joining aggregated DataFrames to perform multi-level analysis (e.g., calculating percentages by country). |

## Results

| Analysis Task | Result | Insight |
|---|---|---|
| **Treatment Duration** | ~458 days for all therapies | Suggests highly standardized treatment protocols, regardless of type (Chemotherapy, Radiation, etc.). |
| **Smoking & Survival** | "Never Smoked" had the highest survival rate (22.09%) | Reinforces the strong negative correlation between smoking and patient survival outcomes. |
| **Geographical Hotspots** | Greece, Croatia, Czech Republic had the highest % of Stage IV cases | Identifies potential regions for targeted public health screening programs or further research. |
| **High-Risk Cohort** | No patients met all criteria | The specific combination of multiple high-risk factors was found to be exceptionally rare in this dataset. |

## Key Learnings

- **PySpark for Healthcare Analytics:** This project confirms PySpark's suitability for large-scale healthcare data analysis, efficiently handling nearly a million records to derive population-level insights.
- **Data Standardization is Key:** The rigorous cleaning process was critical for ensuring the accuracy of subsequent analyses, especially for temporal and categorical data.
- **Insights from Synthetic Data:** While the dataset is synthetic (as suggested by the uniform treatment durations), the analytical workflow itself is a robust template for analyzing real-world medical data to uncover trends in treatment efficacy, survival factors, and geographical health disparities.

## Future Work

- **Predictive Modeling:** Build a survival prediction model (e.g., using Logistic Regression or Gradient-Boosted Trees in `spark.ml`) to predict patient outcomes.
- **Advanced Visualization:** Export aggregated data to a visualization tool (like Tableau) or library (like Matplotlib/Seaborn) to create more intuitive dashboards of the findings.
- **Root Cause Analysis:** Integrate external datasets (e.g., demographic, environmental) to explore potential reasons for the geographical variations in advanced cancer diagnoses.

## Repository Structure

```
Lung-Cancer-Analysis/
├── Lung_Cancer_Mini_Assignment_1.ipynb     # Jupyter Notebook with PySpark code
├── README.md                               # This file
└── data/
    └── sample/                             # Directory for sample data
```

## Notes
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating proficiency in big data processing with PySpark and its application to large-scale healthcare data analysis.
