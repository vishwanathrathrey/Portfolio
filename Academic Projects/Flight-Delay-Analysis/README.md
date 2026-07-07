# Domestic Flight Delay Analysis with PySpark

## Overview

This project performs a comprehensive analysis of domestic flight data using Apache PySpark, focusing on delay patterns and operational metrics. The analysis addresses key questions about flight performance: early arrivals, departure time patterns for long-haul flights, proportion of significant delays, average airtime for early morning departures, and the relationship between departure and arrival delays.

The workflow demonstrates practical big data processing capabilities using PySpark's distributed computing framework, including data ingestion, cleaning, transformation, and aggregation operations on flight datasets.

## Dataset

- **Source**: Domestic Flight Dataset (US flights)
- **Format**: CSV file with flight operation metrics
- **Key Features**:
  - `FL_DATE`: Flight date
  - `DEP_DELAY`: Departure delay in minutes
  - `ARR_DELAY`: Arrival delay in minutes
  - `AIR_TIME`: Actual flight time in minutes
  - `DISTANCE`: Flight distance in miles
  - `DEP_TIME`: Scheduled departure time (decimal hours)
  - `ARR_TIME`: Scheduled arrival time (decimal hours)
- **Note**: Full dataset is excluded; sample data is provided for reference

## Objectives

- Perform data cleaning and standardization on flight dataset using PySpark
- Analyze flight delay patterns and operational efficiency
- Calculate key performance metrics including early arrivals, delay proportions, and average airtime
- Identify patterns in long-haul flight departure times
- Investigate the relationship between departure and arrival delays
- Demonstrate PySpark DataFrame operations and aggregation functions

## Project Workflow

### 1. Environment Setup
- Initialized PySpark session with appropriate application name
- Imported required libraries: `SparkSession`, DataFrame functions (`col`, `avg`, `round`, `max`), and data types (`FloatType`)
- Configured Google Colab for file upload

### 2. Data Loading
- Uploaded flight dataset CSV file through Google Colab interface
- Loaded data into PySpark DataFrame with schema inference
- Displayed schema structure and sample records for verification

### 3. Data Cleaning & Standardization
- Converted numeric columns to `FloatType` for consistent data types:
  - `DEP_DELAY`, `ARR_DELAY`, `AIR_TIME`, `DISTANCE`, `DEP_TIME`, `ARR_TIME`
- Removed rows with null values in numeric columns
- Ensured data quality for subsequent analysis

### 4. Analysis Tasks

**Task 1: Early Arrivals Analysis**
- Counted flights that arrived earlier than expected (ARR_DELAY < 0)
- Result: 534,655 flights arrived early

**Task 2: Long-Haul Flight Departure Patterns**
- Filtered flights with distance > 2000 miles
- Calculated average departure time rounded to 2 decimal places
- Result: Average departure time of 13.97 (approximately 1:58 PM)

**Task 3: Significant Delay Analysis**
- Calculated proportion of flights with arrival delays > 60 minutes
- Result: 5.31% of flights experienced significant delays

**Task 4: Early Morning Flight Analysis**
- Filtered flights departing before 9:00 AM
- Calculated average airtime
- Result: Average airtime of 111.36 minutes

**Task 5: Delay Relationship Analysis**
- Filtered flights with no departure delay (DEP_DELAY <= 0)
- Found maximum arrival delay among these flights
- Result: Maximum arrival delay of 701.0 minutes

## Techniques and Concepts Applied

| Technique | Application |
|-----------|-------------|
| **Apache PySpark** | Distributed data processing framework |
| **DataFrame Operations** | Filtering, aggregation, and transformation |
| **Schema Inference** | Automatic data type detection from CSV |
| **Data Type Casting** | Converting columns to appropriate numeric types |
| **Missing Value Treatment** | Dropping rows with null values |
| **Column Operations** | Using `col()` function for column references |
| **Aggregation Functions** | `avg()`, `max()`, `count()` for summary statistics |
| **Filtering** | Conditional row selection using boolean expressions |
| **Rounding** | Formatting numeric results with `round()` function |
| **Spark Session Management** | Initializing and managing Spark context |

## Models Used

This project focuses on **data analysis and aggregation** rather than machine learning modeling. The following analytical operations were performed using PySpark:

| Operation Type | Function | Purpose |
|----------------|----------|---------|
| **Count Aggregation** | `count()` | Counting early arrivals and total flights |
| **Average Calculation** | `avg()` + `round()` | Computing mean departure times and airtime |
| **Proportion Calculation** | Conditional counting + division | Determining percentage of delayed flights |
| **Maximum Value** | `max()` | Finding maximum arrival delay |

## Results

### Early Arrivals
- **534,655 flights** arrived earlier than expected
- Indicates significant operational efficiency in the dataset

### Long-Haul Departure Patterns
- **Average departure time**: 13.97 (approximately 1:58 PM)
- Suggests long-haul flights tend to depart in the afternoon

### Significant Delays
- **5.31%** of flights experienced arrival delays exceeding 60 minutes
- Provides insights into on-time performance reliability

### Early Morning Flights
- **Average airtime**: 111.36 minutes for flights departing before 9:00 AM
- Demonstrates typical flight duration for early morning operations

### Delay Correlation
- **Maximum arrival delay of 701.0 minutes** occurred despite zero departure delay
- Highlights that arrival delays can originate from factors other than departure delays
- Suggests significant external factors (weather, air traffic, etc.) impact arrival times

## Key Insights

### Delay Patterns
- Early arrivals are common (534,655 instances), indicating conservative scheduling or operational efficiency
- Only 5.31% of flights experience significant delays (>60 minutes), suggesting relatively reliable operations
- Maximum arrival delay of 701 minutes despite on-time departure indicates complex delay propagation mechanisms

### Operational Patterns
- Long-haul flights (>2000 miles) typically depart around 2:00 PM
- Early morning flights (<9:00 AM) average approximately 1 hour 51 minutes of airtime
- Distance and departure time show patterns that could inform scheduling optimization

### Data Quality Observations
- Schema inference correctly identified data types
- Missing values were present and required handling
- Float type conversion ensured numeric precision for calculations

## Key Learnings

### 1. PySpark for Data Analysis
PySpark's DataFrame API provides efficient, scalable operations for large datasets. The project demonstrated how to perform complex aggregations and transformations using distributed computing, making it suitable for big data scenarios where pandas would face memory limitations.

### 2. Data Cleaning in Distributed Environments
Type casting and null value handling are critical steps in PySpark workflows. Converting columns to appropriate types (FloatType) and handling missing values ensures analytical accuracy and prevents runtime errors.

### 3. Analytical Workflow Design
Breaking analysis into discrete tasks with clear functions improves code modularity and reusability. Each task can be independently validated and modified without affecting other analyses.

### 4. Delay Analysis Complexity
Flight delays are influenced by multiple factors beyond departure delays. The finding of 701-minute arrival delays despite zero departure delays indicates that:
- Weather conditions at destination airports
- Air traffic congestion
- Connection/crew issues
- Aircraft maintenance problems

These factors can cause significant delays independently of departure timing.

### 5. Big Data Tool Proficiency
This project demonstrates practical PySpark skills including session management, DataFrame operations, column transformations, and aggregation functions - all essential for data engineering roles.

## Repository Structure
```
Flight-Delay-Analysis/
├── data/
│ └── sample/
│ └── flight_data_sample.csv
├── Flight_Data_Mini_Assignment_2.ipynb
└── README.md
```

## Getting Started

1. **Prepare your data**: Place your flight dataset CSV file in the appropriate directory
2. **Run the notebook**: Execute cells sequentially in Google Colab or Jupyter
3. **Upload file**: Use the file upload widget when prompted
4. **View results**: Analysis outputs will be displayed for each task

## Notes

- Full dataset is excluded from this repository; sample data is provided for reference
- The notebook is designed to work with any flight dataset following the specified schema
- PySpark session must be configured with appropriate resources for large datasets
- All analysis functions are modular and can be extended for additional metrics

This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating proficiency in big data processing with PySpark and analytical problem-solving in the aviation domain.