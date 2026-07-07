# NYC Taxi Data Analysis: 2023 Trip Patterns

## Overview

This project performs an exploratory data analysis (EDA) on New York City taxi trip data for 2023. The analysis examines over 1.87 million sampled trips to uncover temporal usage patterns, revenue trends, and geographic demand distribution. The goal is to identify actionable insights for fleet management, driver scheduling, and urban mobility planning.

## Dataset

- **Source:** NYC Taxi & Limousine Commission (TLC) — 2023 trip records
- **Format:** 12 monthly Parquet files
- **Sampling:** A 5% stratified sample was used to reduce computational load while preserving temporal and geographic patterns
- **Size:** The final cleaned dataset contains **1,870,893** trips
- **Features:** Pick-up/drop-off times, locations, fare amounts, trip distances, passenger counts, and payment types
- **Note:** The full dataset is not included in this repository. Only a sample is provided to illustrate the data structure.

## Objectives

- Analyze temporal patterns to determine peak hours and days for taxi demand
- Understand revenue distribution and identify the most lucrative months
- Identify geographic hotspots and pinpoint the busiest taxi zones in NYC
- Provide data-driven recommendations for operational efficiency and resource allocation

## Project Workflow

### 1. Data Collection & Validation
- Mounted Google Drive to access the dataset
- Validated the presence of all 12 monthly Parquet files and the `taxi_zones.shp` shapefile

### 2. Data Sampling & Preparation
- Implemented a **nested sampling strategy** (5% per hour and date) to create a representative subset of the 2023 data
- Extracted temporal features (`pickup_hour`, `pickup_day`, `pickup_month`) for analysis

### 3. Data Cleaning & Feature Engineering
- Lowercased column names for consistency
- Calculated `trip_duration` (minutes) and `trip_speed_mph`
- Removed invalid trips (e.g., negative duration)
- Handled outliers using predefined, business-logic-driven bounds for `fare_amount`, `trip_distance`, `trip_duration`, and `trip_speed_mph`

### 4. Exploratory Data Analysis (EDA)
- **Temporal Analysis:** Analyzed the distribution of pickups by hour to identify rush-hour patterns
- **Financial Analysis:** Aggregated revenue by month to uncover seasonal trends
- **Geographic Analysis:** Mapped pickup density by taxi zone using `geopandas` to identify hotspots

## Techniques and Concepts Applied

| Technique | Application |
|-----------|-------------|
| **Stratified Sampling** | Reduced data size while maintaining distribution integrity |
| **Feature Engineering** | Created temporal features (hour, month) and trip metrics (duration, speed) |
| **Outlier Detection** | Used business logic and domain knowledge to filter unrealistic values |
| **Temporal Analysis** | Analyzed hourly and monthly patterns to identify peak periods |
| **Financial Analysis** | Aggregated and visualized revenue trends to uncover seasonality |
| **Geographic Analysis** | Used shapefiles and `geopandas` to visualize spatial demand distribution |
| **Data Visualization** | Created clear, informative plots using `matplotlib` and `seaborn` |

## Results

### Key Metrics

| Metric | Value | Insight |
|--------|-------|---------|
| **Peak Hour** | 18:00 (6 PM) | Evening commute is the busiest period |
| **Quietest Hour** | 04:00 (4 AM) | Very low demand during early morning hours |
| **Peak Month** | October | Highest revenue month of the year ($2.48M) |
| **Busiest Zone** | JFK Airport | 93,544 pickups (5.1% of total) |
| **Total Annual Revenue** | $36.2 Million | Average monthly revenue of ~$3M |

### Key Comparisons

- **Hourly vs. Monthly Patterns:** The hourly distribution shows a clear bi-modal peak (morning and evening rush), while the monthly distribution reveals a seasonal cycle with a fall peak
- **Revenue vs. Volume:** While May is a high-volume month, October generates the highest revenue, indicating a possible difference in average fare or trip distance
- **Core vs. Outer Boroughs:** The geographic analysis highlights the extreme concentration of pickups in Manhattan compared to other boroughs

### Key Findings

- **Evening Rush Dominates:** The period from 4-7 PM accounts for **22.3%** of all daily trips
- **October is the Peak Revenue Month:** Revenue is **9.3%** higher than the annual average in October
- **Manhattan is the Epicenter:** The top 5 busiest zones are all in Manhattan and account for **11.5%** of all pickups

## Key Insights

### Operational Efficiency
The data provides clear guidance for dynamic fleet deployment. Increasing vehicle availability during evening rush hours (4-7 PM) and reducing it during early mornings (4-5 AM) would significantly improve efficiency.

### Seasonal Planning
The clear revenue peak in October suggests that maintenance and vehicle acquisition can be strategically scheduled for the low season (February).

### Urban Mobility
The concentration of pickups in Manhattan, particularly near transportation hubs (JFK, Penn Station) and tourist areas, provides crucial data for city planning and infrastructure decisions.

## Key Learnings

### 1. Data Quality is Paramount
The initial steps of sampling and cleaning were essential. A significant number of unrealistic trips (1.1% of the sample) were removed, which would have skewed the analysis.

### 2. The Power of Visualization
A simple bar chart or heatmap can instantly communicate complex patterns that are difficult to see in raw data.

### 3. Strategic Data Sampling
The nested sampling strategy allowed for deep analysis of a very large dataset without requiring massive computational resources.

### 4. Domain Knowledge
Understanding the business context (e.g., what constitutes a reasonable trip fare or duration) is critical for effective data cleaning and generating actionable insights.

## Repository Structure

```
NYC-Taxi-Data-Analysis/
├── data/
│ └── sample/ # Sample parquet files (full data excluded)
├── NYC_Taxi_Analysis.ipynb # Main analysis notebook
├── report.pdf # Comprehensive project report
└── README.md # Project overview
```


## Notes

- Full dataset is excluded from this repository due to size constraints
- Sample data is provided to illustrate the data structure
- The notebook can be run with the full dataset for complete results
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**

## Future Work

- Build predictive models for demand forecasting
- Incorporate weather data to analyze weather impact on taxi demand
- Analyze impact of major events on taxi demand patterns
- Compare trends across different years (2022 vs. 2023)
- Develop an interactive dashboard for real-time monitoring

## References

- NYC Taxi & Limousine Commission. (2023). *Trip Record Data*. https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- NYC Department of City Planning. (2023). *Taxi Zones Shapefile*.
- McKinsey & Company. (2020). *The Future of Mobility in New York City*.