# California Traffic Collision Data Analysis

A comprehensive big data analytics project analyzing over 900,000 California traffic collision records using PySpark, with focus on identifying patterns, risk factors, and actionable safety insights.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5.4-orange.svg)](https://spark.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Overview

This project analyzes California traffic collision data from the SWITRS (Statewide Integrated Traffic Records System) dataset to uncover patterns in collision severity, temporal trends, spatial distributions, and contributing environmental factors. Using PySpark for distributed data processing and Plotly/Matplotlib for visualization, the analysis provides data-driven recommendations for improving road safety, optimizing traffic management, and implementing evidence-based policy changes.

The project demonstrates end-to-end data engineering and analytics capabilities: from cleaning and preprocessing large-scale datasets to exploratory analysis and actionable insight generation.

---

## 📊 Dataset

**Source:** California Traffic Collision Data from SWITRS (Statewide Integrated Traffic Records System)

**Dataset Characteristics:**
- **Structure:** Four relational tables (collisions, parties, victims, case IDs)
- **Size:** 906,203 collision records after cleaning
- **Time Span:** Multiple years of historical collision data
- **Attributes:** Severity, weather conditions, lighting, temporal data, geographical location, victim demographics, and party information

**Note:** The repository contains **sample data only**. The full SWITRS dataset is available from the California Highway Patrol's official data portal.

---

## 🎯 Objectives

- **Analyze collision severity distribution** to understand the proportion of property damage vs. injury/fatality incidents
- **Examine environmental influences** (weather, lighting, road conditions) on collision frequency and severity
- **Identify demographic vulnerabilities** through victim age distribution analysis
- **Uncover temporal patterns** (weekly, monthly, hourly) to guide resource allocation
- **Map spatial distributions** at county level to identify high-risk geographical areas
- **Assess predictive risk** through severity-victim relationships and latent risk estimation
- **Generate actionable recommendations** for safety interventions and policy development

---

## 🔄 Project Workflow

### 1. Data Preparation
- Loaded four relational tables using PySpark (`collisions`, `parties`, `victims`, `case_ids`)
- Applied sampling techniques for initial data exploration
- Structured data for efficient distributed processing

### 2. Data Cleaning
- **Sparse Column Removal:** Dropped columns with >60% missing values (e.g., `caltrans_county`, `latitude`, `longitude`)
- **Missing Value Treatment:** Dropped rows missing critical identifiers (`case_id`, `collision_date`); filled numerical counts (victim counts) with 0
- **Data Type Standardization:** Converted `case_id` to long, `victim_age` to integer, date/time to Spark timestamp formats
- **Outlier Detection:** Applied IQR method to identify outliers in age-related attributes
- **Duplicate Removal:** Deduplicated based on composite keys (`case_id`, `party_number`, `id`)

### 3. Exploratory Data Analysis (EDA)

**Univariate Analysis:**
- Collision severity distribution (property damage: 60.5%, pain: 24.5%, other injury: 12.5%, severe: 2.4%)
- Weather conditions (clear: 82.47%, cloudy: 12.92%, rain: 3.43%)
- Victim age distribution with KDE smoothing

**Bivariate Analysis:**
- Collision severity vs. number of victims (box plot analysis)
- Weather conditions vs. severity (stacked bar + heatmap)
- Lighting conditions vs. severity (dual visualization)

**Temporal Analysis:**
- Weekly collision patterns (Friday peak, weekend drop)
- Monthly trends (March and October peaks)
- Hourly distribution (evening rush hour peak at 5 PM with 72,000 collisions)

**Spatial Analysis:**
- County-level collision distribution (Los Angeles: 30.49%)
- Geographical risk mapping (bubble chart with frequency + fatality rate)

### 4. Predictive Risk Assessment
- Risk heatmap (weather × severity interaction)
- Latent fatality risk analysis by severity level (severe injury: 40% estimated risk)

### 5. Insight Generation & Recommendations
- Immediate, medium-term, and long-term intervention strategies
- Implementation roadmap with success metrics

---

## 🛠️ Techniques and Concepts Applied

| Technique | Purpose | Implementation |
|-----------|---------|----------------|
| **Sparse Column Removal** | Remove columns with >60% missing values | Drop operation on columns with high null rates |
| **IQR Outlier Detection** | Identify age outliers while preserving severity-critical events | `approxQuantile` with 1.5× IQR bounds |
| **String Indexing** | Encode categorical columns for numeric operations | PySpark `StringIndexer` |
| **Time Series Analysis** | Identify hourly, daily, and monthly patterns | Temporal aggregation with Spark SQL functions |
| **Cross-Tabulation** | Analyze categorical relationships (weather × severity) | GroupBy + pivot + percentage calculation |
| **Interactive Visualization** | Enable exploration of complex patterns | Plotly (bar charts, heatmaps, scatter plots) |
| **Spatial Analysis** | Map collision patterns at county level | Geospatial visualization with dual metric encoding |
| **Risk Scoring** | Combine frequency and severity for risk prioritization | Interaction analysis with severity progression estimation |

---

## 📈 Models Used

**Primary Approach:** Exploratory Data Analysis (EDA) with descriptive statistics and visualization-based pattern identification

**Why This Approach?**
- Large dataset (N > 900,000) where even small effects are statistically significant
- Focus on **practical significance** through effect size and percentage differences
- Observational data nature requires association identification rather than causal inference
- Safety intervention decisions benefit from pattern magnitude assessment

**Statistical Methods Applied:**
- Descriptive statistics (mean, median, standard deviation, IQR)
- Frequency distributions and proportional analysis
- Comparative distribution analysis (box plots, kernel density estimation)
- Time series decomposition and seasonal pattern detection

---

## 📊 Results

### Key Analytical Findings

| Dimension | Finding | Implication |
|-----------|---------|-------------|
| **Peak Hour** | 5 PM (72,000 collisions) | Enhanced enforcement during evening traffic |
| **Urban Concentration** | Los Angeles County: 30.49% | Targeted urban safety initiatives |
| **Weather Impact** | Clear conditions: 82.47% | Focus on driver behavior factors |
| **Age Vulnerability** | 20–30 age group (31,000 victims) | Targeted education for young drivers |
| **Seasonal Pattern** | March & October peaks | Seasonal safety campaigns |
| **Lighting Impact** | Dark conditions show higher severity proportion | Infrastructure lighting upgrades |
| **Risk Escalation** | Severe injury → 40% latent fatality risk | Importance of immediate medical response |

### Severity Distribution
- Property Damage Only: **60.5%**
- Pain (Complaint of Pain): **24.5%**
- Other Injury: **12.5%**
- Severe Injury: **2.4%**

### Visual Analysis Summary
- **Weather × Severity:** Clear weather dominates volume but lower severe percentage; rain and fog show higher severity proportion per incident
- **Lighting × Severity:** Dark conditions (no street lights) show higher severity risk despite fewer total collisions
- **Victim Age:** Right-skewed distribution with peak in 20-30 age range; mean age ~34 years
- **Weekly Pattern:** Friday peak (13.5%), Sunday minimum (11.8%)

---

## 💡 Key Insights

### Business & Domain Insights

1. **Driver Behavior Dominates:** Despite intuitive assumptions, clear weather accounts for the majority of collisions (82.47%), suggesting driver behavior factors (distraction, speeding, impairment) are primary contributors rather than environmental visibility.

2. **Urban Density Impact:** Los Angeles County's 30.49% collision concentration highlights the need for urban-specific safety measures and infrastructure improvements in high-density areas.

3. **Disproportionate Risk in Adverse Conditions:** While adverse weather (rain, fog) has lower collision volume, it shows higher severe injury percentage per incident—critical for emergency response planning.

4. **Young Driver Vulnerability:** The 20-30 age group's disproportionately high victim count (31,000) supports evidence-based policies for graduated licensing and targeted education.

5. **Evening Rush Hour Risk:** Peak collision frequency at 5 PM (72,000 collisions) identifies the optimal timing for resource allocation and enforcement.

6. **Seasonal Variation:** March and October peaks suggest seasonal factors (weather transitions, daylight changes) influence collision patterns—valuable for predictive resource planning.

7. **Latent Fatality Risk:** Severe injury collisions carry an estimated 40% latent fatality risk, emphasizing the importance of immediate medical response and comprehensive follow-up care.

---

## 🧠 Key Learnings

### Technical Concepts Reinforced

1. **Data Quality Assessment:** Missing value treatment requires balancing data retention with analytical validity—sparse column removal at 60% threshold maintained ~99.5% of records while improving processing efficiency.

2. **Large Dataset Statistical Significance:** With N > 900,000, even trivial effects achieve statistical significance. Focus on **practical significance** through effect magnitude and percentage differences is more meaningful for safety decisions.

3. **Categorical Variable Relationships:** Cross-tabulation with percentage calculation (not just raw counts) reveals severity risk independent of volume—crucial for identifying disproportionate risks.

4. **Temporal Aggregation Granularity:** Hour-level analysis reveals patterns (5 PM peak) invisible at daily or monthly granularity; analytical granularity must match the decision-making context.

5. **Geographical Data Limitations:** Original coordinate limitations required county-level aggregation—understanding data quality constraints is essential before spatial analysis.

6. **Visualization Multi-Encoding:** Dual encoding (color + size, frequency + percentage) enables simultaneous assessment of multiple risk dimensions in a single visualization.

7. **Exploratory vs. Confirmatory Analysis:** For observational data with practical application goals, exploratory analysis with visualization-based pattern identification is often more appropriate than formal hypothesis testing.

---

## 📁 Repository Structure

Traffic-Data-Analysis/
├── data/
│ └── sample/
│ ├── sample_collisions.csv
│ ├── sample_parties.csv
│ ├── sample_victims.csv
│ └── sample_case_ids.csv
├── ETL_Traffic_Data_Analysis.ipynb
├── Report.pdf
└── README.md

---

## 📝 Notes

- **Full dataset excluded** due to size constraints and licensing considerations
- **Sample data provided** to demonstrate data structure and facilitate execution
- **Project completed** as part of the MSc in Machine Learning and Artificial Intelligence program
- **Analysis environment:** Google Colab Pro with PySpark 3.5.4
- **Data source:** SWITRS California Traffic Collision Dataset (publicly available from California Highway Patrol)

---

## 🔧 Technologies Used

- **Python 3.9+** – Core programming language
- **PySpark 3.5.4** – Distributed data processing for large-scale ETL
- **Pandas 2.2.2** – Data manipulation and analysis
- **NumPy** – Numerical computing
- **Plotly 5.18.0** – Interactive visualizations (bar charts, heatmaps, scatter plots)
- **Matplotlib 3.8.0** – Static visualizations
- **Seaborn 0.13.0** – Statistical visualizations
- **Google Colab Pro** – Development environment with GPU support
- **Overleaf LaTeX** – Professional report documentation
- **AWS S3** – Scalable data storage (conceptual implementation)

---

## 📄 License

This project is for academic and portfolio purposes. The SWITRS dataset is maintained by the California Highway Patrol and is subject to their data use policies.

---

## 👤 Author

**Vishwanath R Athrey**  
MSc in Machine Learning and Artificial Intelligence