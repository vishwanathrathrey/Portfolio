# California Traffic Collision Data Analysis with PySpark

## Overview

This project conducts a large-scale analysis of over 900,000 California traffic collision records from the SWITRS dataset using PySpark. The analysis aims to identify key patterns, risk factors, and actionable insights related to collision severity, environmental conditions, and temporal trends. The workflow demonstrates an end-to-end big data analytics pipeline, from data cleaning and preprocessing to exploratory data analysis and the generation of data-driven safety recommendations.

## Recruiter Snapshot

This project demonstrates:
- **Big Data Processing with PySpark:** Proficiency in using Apache PySpark to perform large-scale data ingestion, cleaning, and analysis on a distributed computing framework, essential for handling massive datasets.
- **End-to-End Data Analytics Pipeline:** Competency in the complete data analytics lifecycle, including data cleaning, feature engineering, multi-dimensional exploratory data analysis (temporal, spatial, environmental), and insight generation.
- **Advanced Data Cleaning at Scale:** Skill in applying robust data cleaning techniques—such as sparse column removal, outlier detection (IQR method), and data type standardization—on a large, real-world dataset.
- **Actionable Insight Generation:** Ability to translate complex analytical findings into clear, actionable recommendations for business or policy decisions, such as targeted safety interventions and resource allocation.
- **Data Visualization for Impact:** Experience in using visualization libraries like Plotly and Matplotlib to effectively communicate complex patterns and insights from large datasets.

## Dataset

- **Source:** California Traffic Collision Data from SWITRS (Statewide Integrated Traffic Records System)
- **Size:** 906,203 collision records after cleaning.
- **Key Features:** Collision severity, weather conditions, lighting, temporal data, geographical location, victim demographics.
- **Note:** The repository contains sample data only.

## Objectives

- Analyze collision severity distribution to understand the proportion of different incident types.
- Examine the influence of environmental factors (weather, lighting) on collision frequency and severity.
- Identify temporal patterns (hourly, weekly, monthly) to guide resource allocation.
- Map spatial distributions at the county level to identify high-risk geographical areas.
- Generate actionable recommendations for improving road safety and traffic management.

## Project Workflow

1.  **Data Cleaning and Preprocessing:**
    - Loaded four relational tables (`collisions`, `parties`, `victims`, `case_ids`) using PySpark.
    - Performed extensive data cleaning, including removing sparse columns, handling missing values, standardizing data types, and removing duplicates.
    - Applied the IQR method to detect and handle outliers in age-related attributes.
2.  **Exploratory Data Analysis (EDA):**
    - **Univariate Analysis:** Analyzed the distribution of key variables like collision severity and weather conditions.
    - **Bivariate Analysis:** Investigated relationships between variables, such as collision severity vs. number of victims and weather vs. severity.
    - **Temporal Analysis:** Uncovered weekly, monthly, and hourly collision patterns, identifying peak times like the 5 PM evening rush hour.
    - **Spatial Analysis:** Mapped collision distribution at the county level, highlighting hotspots like Los Angeles County.
3.  **Insight Generation:**
    - Synthesized findings from the EDA to generate actionable recommendations for immediate, medium-term, and long-term safety interventions.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **PySpark** | Distributed data processing for large-scale ETL and analysis. |
| **Advanced Data Cleaning** | Using techniques like sparse column removal and IQR outlier detection at scale. |
| **Time-Series Analysis** | Identifying hourly, daily, and monthly patterns through temporal aggregation. |
| **Cross-Tabulation** | Analyzing relationships between categorical variables (e.g., weather vs. severity). |
| **Interactive Visualization** | Using Plotly to create interactive charts for exploring complex data patterns. |

## Results

| Dimension | Finding | Implication |
|---|---|---|
| **Peak Hour** | 5 PM (72,000 collisions) | Points to the need for enhanced enforcement during the evening commute. |
| **Urban Concentration** | Los Angeles County: 30.49% of collisions | Highlights the need for targeted urban safety initiatives. |
| **Weather Impact** | Clear conditions account for 82.5% of collisions | Suggests that driver behavior, not just environment, is a primary factor. |
| **Age Vulnerability** | Peak victims in the 20-30 age group | Supports targeted education campaigns for young drivers. |

## Key Learnings

- **Driver Behavior is a Dominant Factor:** The fact that most collisions occur in clear weather underscores the importance of addressing driver behavior (e.g., distraction, speeding) in safety campaigns.
- **Practical vs. Statistical Significance:** With a massive dataset, focusing on the practical significance (i.e., the magnitude of the effect) is more valuable for decision-making than just statistical significance.
- **Granularity in Temporal Analysis:** Analyzing data at an hourly level revealed a sharp peak at 5 PM that would be missed in a daily or monthly view, demonstrating the importance of choosing the right analytical granularity.

## Future Work

- **Predictive Modeling:** Develop a machine learning model to predict collision severity based on weather, time, and location data.
- **Geospatial Deep Dive:** Use more advanced geospatial techniques to analyze specific road segments or intersections.
- **Real-time Dashboard:** Create a real-time dashboard to monitor collision trends and provide live insights to traffic management authorities.

## Repository Structure

```
Traffic-Data-Analysis/
├── ETL_Traffic_Data_Analysis.ipynb     # Jupyter Notebook with PySpark code
├── README.md                           # This file
└── data/
    └── sample/                         # Directory for sample data
```

## Notes
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, showcasing my ability to manage and analyze large-scale datasets to produce actionable insights.
