# NYC Taxi Data Analysis: 2023 Trip Patterns

## Overview

This project performs an exploratory data analysis (EDA) on a large dataset of New York City taxi trips from 2023, analyzing over 1.87 million sampled records. The analysis uncovers key temporal, financial, and geographic patterns to provide data-driven insights for operational efficiency and urban mobility planning. The workflow demonstrates an end-to-end data analysis pipeline, from strategic sampling and cleaning to insightful visualization.

## Recruiter Snapshot

This project demonstrates:
- **Large-Scale Data Handling:** Proficiency in handling large datasets (millions of records) using efficient sampling techniques (stratified sampling) and libraries like Pandas.
- **End-to-End EDA:** Competency in the complete exploratory data analysis lifecycle, including data cleaning, feature engineering, multi-dimensional analysis (temporal, financial, geographic), and visualization.
- **Feature Engineering:** Skill in creating meaningful features from raw data, such as `trip_duration` and `trip_speed_mph`, and extracting temporal components to enable deeper analysis.
- **Geospatial Analysis:** Experience with `geopandas` to perform geographic analysis, such as mapping pickup densities to identify spatial hotspots.
- **Actionable Insight Generation:** Ability to translate complex data patterns into clear, actionable business recommendations for fleet management, driver scheduling, and strategic planning.

## Dataset

- **Source:** NYC Taxi & Limousine Commission (TLC) — 2023 trip records
- **Format:** 12 monthly Parquet files
- **Sampling:** A 5% stratified sample was used, resulting in **1,870,893** trips for analysis.
- **Key Features:** Pick-up/drop-off times, locations, fare amounts, trip distances, passenger counts.
- **Note:** The full dataset is not included in this repository.

## Objectives

- Analyze temporal patterns to determine peak hours and days for taxi demand.
- Understand revenue distribution to identify the most lucrative months.
- Identify geographic hotspots and pinpoint the busiest taxi zones in NYC.
- Provide data-driven recommendations for operational efficiency and resource allocation.

## Project Workflow

1.  **Data Sampling & Preparation:**
    - Implemented a **nested stratified sampling strategy** (5% per hour and date) to create a representative subset of the 2023 data.
    - Extracted temporal features (`pickup_hour`, `pickup_day`, `pickup_month`).
2.  **Data Cleaning & Feature Engineering:**
    - Calculated `trip_duration` and `trip_speed_mph`.
    - Removed invalid trips (e.g., negative duration) and handled outliers using business-logic-driven bounds.
3.  **Exploratory Data Analysis (EDA):**
    - **Temporal Analysis:** Analyzed the distribution of pickups by hour to identify rush-hour patterns.
    - **Financial Analysis:** Aggregated revenue by month to uncover seasonal trends.
    - **Geographic Analysis:** Mapped pickup density by taxi zone using `geopandas` to identify hotspots.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Stratified Sampling** | Reducing data size while preserving temporal and geographic distribution integrity. |
| **Feature Engineering** | Creating temporal features and trip metrics (duration, speed) to enrich the dataset. |
| **Outlier Detection** | Using domain knowledge to define and filter unrealistic data points. |
| **Geospatial Analysis** | Using shapefiles and `geopandas` to visualize spatial demand distribution. |
| **Data Visualization** | Creating clear, informative plots using `matplotlib` and `seaborn` to communicate findings. |

## Results

| Metric | Value | Insight |
|---|---|---|
| **Peak Hour** | 18:00 (6 PM) | The evening commute is the busiest period for taxi demand. |
| **Peak Month** | October | October is the highest revenue-generating month of the year. |
| **Busiest Zone** | JFK Airport | JFK Airport is the single busiest pickup location in NYC. |
| **Key Finding** | Evening rush (4-7 PM) accounts for 22.3% of all daily trips. | Highlights a critical window for maximizing fleet availability. |

## Key Learnings

- **Strategic Sampling is Effective:** The nested sampling strategy proved highly effective for analyzing a massive dataset on standard hardware without losing analytical integrity.
- **Domain Knowledge is Crucial for Cleaning:** Applying business context (e.g., reasonable fare amounts, trip durations) was essential for effective outlier detection and data cleaning.
- **Visualization Drives Insights:** Geographic and temporal visualizations were key to quickly identifying and communicating complex patterns like rush hours and demand hotspots.

## Future Work

- **Predictive Modeling:** Build a time-series model to forecast taxi demand by zone and hour.
- **Weather Integration:** Incorporate weather data to analyze its impact on taxi demand and trip patterns.
- **Interactive Dashboard:** Develop an interactive dashboard (e.g., with Dash or Streamlit) for real-time monitoring of taxi operations.

## Repository Structure

```
NYC-Taxi-Data-Analysis/
├── Datasets and Dictionary-NYC/
│   └── Datasets and Dictionary/
├── EDA_NYC_Taxi_Analysis.ipynb     # Jupyter Notebook with analysis
├── README.md                       # This file
└── data/
    └── sample/                     # Directory for sample data
```

## Notes
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating my ability to conduct a large-scale data analysis project from start to finish, yielding actionable business insights.
