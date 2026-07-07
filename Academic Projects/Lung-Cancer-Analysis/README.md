# Lung Cancer Patient Data Analysis with PySpark

## Overview

This project performs a comprehensive analysis of lung cancer patient data using Apache PySpark, examining treatment patterns, survival rates, and geographical variations in cancer staging. The analysis addresses key healthcare questions: treatment duration by therapy type, smoking status impact on survival, regional differences in advanced-stage diagnoses, and high-risk patient characteristics.

The workflow demonstrates practical big data processing capabilities using PySpark's distributed computing framework, including data cleaning, transformation, aggregation, and analytical querying on a healthcare dataset.

## Dataset

- **Source**: Synthetic lung cancer patient dataset
- **Format**: CSV file with patient medical records
- **Size**: 890,000 patient records after cleaning
- **Key Features**:
  - `id`: Patient identifier
  - `age`: Patient age
  - `gender`: Male/Female
  - `country`: Patient country of residence
  - `diagnosis_date`: Date of cancer diagnosis
  - `cancer_stage`: Stage I through IV
  - `family_history`: Yes/No indicator
  - `smoking_status`: Current, Former, Never Smoked
  - `bmi`: Body Mass Index
  - `cholesterol_level`: Blood cholesterol
  - `hypertension`: 0/1 indicator
  - `asthma`: 0/1 indicator
  - `cirrhosis`: 0/1 indicator
  - `other_cancer`: 0/1 indicator
  - `treatment_type`: Radiation, Chemotherapy, Combined, Surgery
  - `end_treatment_date`: Date treatment concluded
  - `survived`: Survival indicator (0/1)
- **Note**: Full dataset is excluded; sample data is provided for reference

## Objectives

- Perform comprehensive data cleaning and standardization on healthcare dataset using PySpark
- Analyze treatment duration patterns across different therapy types
- Identify smoking status with the highest survival rate
- Determine countries with highest percentage of Stage IV (advanced) cancer diagnoses
- Analyze characteristics of high-risk patients (male, advanced stage, family history, current smokers, high BMI)
- Demonstrate PySpark DataFrame operations for healthcare analytics

## Project Workflow

### 1. Environment Setup
- Initialized PySpark session with appropriate application name
- Imported required libraries: `SparkSession`, DataFrame functions (`F`), and data types (`IntegerType`, `DoubleType`, `DateType`)
- Configured Google Colab for file upload

### 2. Data Loading
- Uploaded lung cancer dataset CSV file through Google Colab interface
- Loaded data into PySpark DataFrame with header and schema inference
- Displayed schema structure and record count for verification

### 3. Data Cleaning & Standardization
- **Removed duplicate records** to ensure data quality
- **Standardized binary columns** (`family_history`, `hypertension`, `asthma`, `cirrhosis`, `other_cancer`):
  - Converted "Yes"/"No" strings to 1/0 integers
  - Maintained existing numeric values
- **Cast columns to appropriate types**:
  - `age`: IntegerType
  - `bmi`: DoubleType
  - `cholesterol_level`: DoubleType
  - `survived`: IntegerType
- **Converted date columns** using `to_date()`:
  - `diagnosis_date`
  - `end_treatment_date`
- **Trimmed string columns** to remove whitespace:
  - `smoking_status`
  - `treatment_type`

### 4. Treatment Duration Analysis
- Filtered patients with valid diagnosis and end treatment dates
- Calculated treatment duration in days using `datediff()`
- Grouped by `treatment_type` to find average treatment duration per therapy

### 5. Smoking Status and Survival Analysis
- Grouped patients by `smoking_status`
- Calculated average survival rate for each category
- Identified smoking status with highest survival rate

### 6. Geographical Analysis of Advanced Cancer
- Calculated total patient count per country
- Counted Stage IV diagnoses per country
- Computed Stage IV percentage per country
- Identified top 3 countries with highest percentage of advanced-stage diagnoses

### 7. High-Risk Patient Profile Analysis
- Filtered patients meeting high-risk criteria:
  - Gender: Male
  - Cancer Stage: Stage III or Stage IV
  - Family History: Yes (1)
  - Smoking Status: Current
  - BMI: > 30
  - Survived: Yes (1)
- Calculated average age and hypertension percentage for this cohort

## Techniques and Concepts Applied

| Technique | Application |
|-----------|-------------|
| **Apache PySpark** | Distributed data processing framework |
| **DataFrame Operations** | Filtering, grouping, aggregation, and joining |
| **Duplicate Removal** | `dropDuplicates()` for data quality |
| **String Standardization** | Converting "Yes"/"No" to binary values |
| **Date Operations** | `to_date()` and `datediff()` for temporal analysis |
| **Data Type Casting** | Converting columns to appropriate numeric types |
| **String Trimming** | `trim()` for whitespace removal |
| **GroupBy Aggregation** | `groupBy()` + `agg()` with `avg()`, `count()` |
| **Conditional Filtering** | Complex boolean logic using `&` operators |
| **Joins** | DataFrame joining for country-level analysis |
| **Column Renaming** | `alias()` and `withColumnRenamed()` |

## Results

### Data Cleaning Summary
- **Total rows after cleaning**: 890,000 patient records
- Successfully standardized binary columns (Yes/No to 1/0)
- All date columns properly converted to DateType
- String columns trimmed for consistency

### Treatment Duration Analysis

| Treatment Type | Average Duration (Days) |
|----------------|------------------------|
| Radiation | 458.40 |
| Chemotherapy | 458.40 |
| Combined | 457.82 |
| Surgery | 457.74 |

**Key Finding**: All treatment types show remarkably similar average durations (~458 days), suggesting standardized treatment protocols across therapies.

### Smoking Status and Survival

| Smoking Status | Survival Rate |
|----------------|---------------|
| Never Smoked | 22.09% |

**Key Finding**: "Never Smoked" patients demonstrate the highest survival rate at approximately 22.09%, indicating the significant impact of smoking on cancer outcomes.

### Geographical Analysis

| Country | Stage IV Percentage |
|---------|---------------------|
| Greece | 25.50% |
| Croatia | 25.43% |
| Czech Republic | 25.29% |

**Key Finding**: European countries show the highest percentages of Stage IV diagnoses, ranging from 25.29% to 25.50%.

### High-Risk Patient Analysis
- **Result**: No records met all high-risk criteria simultaneously
- **Insight**: The combination of high-risk factors (male, advanced stage, family history, current smoker, high BMI, and survival) is exceptionally rare in the dataset

## Key Insights

### Treatment Patterns
- All four treatment types (Radiation, Chemotherapy, Combined, Surgery) show nearly identical average durations (~458 days)
- This consistency suggests standardized treatment protocols across different therapeutic approaches
- No significant treatment type is associated with substantially longer or shorter treatment periods

### Smoking Impact
- "Never Smoked" patients have the highest survival rate at 22.09%
- This finding underscores the protective effect of never smoking against cancer mortality
- Even among those who develop lung cancer, smoking history significantly impacts survival outcomes

### Geographical Variation
- Greece, Croatia, and Czech Republic have the highest Stage IV diagnosis percentages (25.29-25.50%)
- These percentages represent the proportion of patients diagnosed at the most advanced cancer stage
- Factors may include: screening practices, healthcare access, environmental exposures, or population demographics

### High-Risk Cohort
- The combination of risk factors (male, advanced stage, family history, current smoker, high BMI, survival) appears extremely rare
- No patients simultaneously meeting all high-risk criteria were found
- This may indicate protective factors among this demographic or data characteristics

## Key Learnings

### 1. PySpark for Healthcare Analytics
PySpark's distributed processing capabilities enable efficient analysis of large healthcare datasets (890,000 records). The platform handles complex transformations, aggregations, and joins at scale, making it suitable for population health studies.

### 2. Data Cleaning in Healthcare Context
Healthcare data requires careful standardization:
- Converting categorical variables (Yes/No) to binary (1/0)
- Ensuring consistent date formats for temporal calculations
- Trimming string fields to prevent analysis errors
- Removing duplicate records to prevent counting artifacts

### 3. Date Operations
PySpark's `datediff()` function is essential for calculating treatment durations and other temporal metrics. Proper date conversion using `to_date()` ensures accurate calculations.

### 4. Aggregation and Grouping
Grouping by categorical variables (`treatment_type`, `smoking_status`, `country`) enables meaningful comparisons of healthcare outcomes and patterns.

### 5. Complex Filtering
Analyzing high-risk cohorts requires combining multiple conditions using logical operators. The filter logic demonstrates how to identify specific patient subpopulations for targeted analysis.

### 6. Limitations of Synthetic Data
The dataset's synthetic nature is evident in the perfect consistency of treatment durations and the absence of high-risk survivors. Real-world healthcare data would show more variation and complexity.

## Repository Structure
```
Lung-Cancer-Analysis/
├── data/
│ └── sample/
│ └── lung_cancer_sample.csv
├── Lung_Cancer_Mini_Assignment_1.ipynb
└── README.md
```

## Getting Started

1. **Prepare your data**: Place your lung cancer dataset CSV file in the appropriate directory
2. **Run the notebook**: Execute cells sequentially in Google Colab or Jupyter
3. **Upload file**: Use the file upload widget when prompted
4. **View results**: Analysis outputs will be displayed for each task

## Notes

- Full dataset is excluded from this repository; sample data is provided for reference
- The notebook is designed to work with any lung cancer dataset following the specified schema
- PySpark session must be configured with appropriate resources for large datasets
- All analysis functions are modular and can be extended for additional metrics
- The dataset is synthetic and should not be used for real clinical decision-making

This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating proficiency in big data processing with PySpark and analytical problem-solving in the healthcare domain.