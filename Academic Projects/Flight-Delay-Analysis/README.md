# Domestic Flight Delay Analysis with PySpark

## Overview

This project performs a comprehensive analysis of domestic flight data using Apache PySpark, focusing on delay patterns and operational metrics. The analysis addresses key questions about flight performance: early arrivals, departure time patterns for long-haul flights, proportion of significant delays, average airtime for early morning departures, and the relationship between departure and arrival delays. The workflow demonstrates practical big data processing capabilities using PySpark's distributed computing framework.

## Recruiter Snapshot

This project demonstrates:
- **Big Data Processing with PySpark:** Proficiency in using Apache PySpark to perform large-scale data ingestion, cleaning, and analysis on a distributed computing framework.
- **Data Cleaning and Standardization:** Ability to handle real-world data quality issues, including casting data types and handling null values in a big data context.
- **Analytical Querying and Aggregation:** Competency in translating business questions into analytical queries using PySpark DataFrame operations, including filtering, aggregation (`avg`, `count`), and grouping.
- **Performance Metrics Calculation:** Experience in calculating key operational metrics from raw data, such as delay proportions and average airtime.
- **Actionable Insight Generation:** Ability to derive meaningful insights from large datasets to answer specific business questions about operational performance.

## Dataset

- **Source**: Domestic Flight Dataset (US flights)
- **Format**: CSV file with flight operation metrics
- **Key Features**: `FL_DATE`, `DEP_DELAY`, `ARR_DELAY`, `AIR_TIME`, `DISTANCE`, `DEP_TIME`, `ARR_TIME`
- **Note**: Full dataset is excluded; sample data is provided for reference.

## Objectives

- Perform data cleaning and standardization on a flight dataset using PySpark.
- Analyze flight delay patterns and operational efficiency.
- Calculate key performance metrics including early arrivals, delay proportions, and average airtime.
- Identify patterns in long-haul flight departure times.
- Investigate the relationship between departure and arrival delays.
- Demonstrate PySpark DataFrame operations and aggregation functions.

## Project Workflow

1.  **Environment Setup:**
    - Initialized a `SparkSession`.
    - Imported required PySpark functions (`col`, `avg`, `round`, `max`) and data types.
2.  **Data Loading:**
    - Loaded the flight dataset CSV into a PySpark DataFrame, inferring the schema.
3.  **Data Cleaning & Standardization:**
    - Converted key numeric columns (`DEP_DELAY`, `ARR_DELAY`, `AIR_TIME`, etc.) to `FloatType` for consistent calculations.
    - Removed rows with null values in critical numeric columns to ensure data quality.
4.  **Analysis Tasks:**
    - **Task 1: Early Arrivals Analysis:** Counted flights where `ARR_DELAY < 0`.
    - **Task 2: Long-Haul Flight Departure Patterns:** Filtered for flights with `DISTANCE > 2000` miles and calculated the average departure time.
    - **Task 3: Significant Delay Analysis:** Calculated the proportion of flights with `ARR_DELAY > 60` minutes.
    - **Task 4: Early Morning Flight Analysis:** Filtered for flights departing before 9:00 AM and calculated the average airtime.
    - **Task 5: Delay Relationship Analysis:** Filtered for flights with no departure delay (`DEP_DELAY <= 0`) and found the maximum arrival delay.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Apache PySpark** | End-to-end use of the distributed data processing framework for big data analysis. |
| **DataFrame Operations** | Extensive use of `filter()`, `withColumn()`, `groupBy()`, and `agg()` for data manipulation and analysis. |
| **Data Cleaning** | Type casting columns to appropriate data types and handling null values using `na.drop()`. |
| **Aggregation Functions** | Use of `count()`, `avg()`, `max()`, and `round()` to compute summary statistics. |
| **Analytical Querying** | Translating specific business questions into a sequence of PySpark transformations and actions. |

## Results

| Analysis Task | Result | Insight |
|---|---|---|
| **Early Arrivals** | 534,655 flights | A significant number of flights arrive ahead of schedule. |
| **Long-Haul Departures** | Avg. departure time: 13.97 (1:58 PM) | Long-haul flights tend to depart in the early afternoon. |
| **Significant Delays** | 5.31% of flights | A small but notable fraction of flights experience major arrival delays. |
| **Early Morning Airtime** | Avg. airtime: 111.36 minutes | Early morning flights have a consistent average flight duration. |
| **Delay Relationship** | Max arrival delay of 701 min | Even flights that depart on time can experience severe arrival delays due to in-flight or landing issues. |

## Key Learnings

- **PySpark for Scalable Analysis:** PySpark provides a powerful and scalable way to perform complex aggregations and transformations on large datasets that would be inefficient with single-node tools like Pandas.
- **The Importance of Data Cleaning:** Ensuring correct data types and handling nulls is a critical first step in any data analysis pipeline to prevent errors and ensure accurate results.
- **Translating Questions to Code:** This project provided extensive practice in breaking down analytical questions into a series of logical steps that can be executed with the PySpark DataFrame API.

## Future Work

- **Deeper Delay Cause Analysis:** Join the flight data with other datasets (e.g., weather data, airport operational data) to investigate the root causes of delays.
- **Predictive Modeling:** Build a machine learning model to predict the likelihood of a flight being delayed based on its characteristics (e.g., airline, origin, destination, time of day).
- **Visualization:** Use a library like `pyspark_dist_explore` or convert aggregated results to Pandas to create visualizations of the findings.

## Repository Structure

```
Flight-Delay-Analysis/
├── Flight_Data_Mini_Assignment_2.ipynb     # Jupyter Notebook with PySpark code
├── README.md                               # This file
└── data/
    └── sample/                             # Directory for sample data
```

## Notes
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating proficiency in big data processing with PySpark and analytical problem-solving in the aviation domain.
