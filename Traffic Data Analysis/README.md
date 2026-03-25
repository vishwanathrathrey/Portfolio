# Traffic Data Analysis (ETL)

## Project Overview
This project performs ETL and analysis on traffic collision-related datasets to prepare data for reporting and insight generation.

## Files
- `ETL_Traffic_Data_Analysis.ipynb`: Main ETL and analysis notebook.
- `Crash_Data_Analysis_Dataset/sample_case_ids.csv`: Case ID data.
- `Crash_Data_Analysis_Dataset/sample_collisions.csv`: Collision records.
- `Crash_Data_Analysis_Dataset/sample_parties.csv`: Party-level records.
- `Crash_Data_Analysis_Dataset/sample_victims.csv`: Victim-level records.

## What This Project Covers
- Data extraction and loading
- Transformations and joins across related CSV files
- Analytical outputs from prepared traffic data

## How to Run
1. Create and activate a Python environment.
2. Install core libraries: pandas, numpy, matplotlib, seaborn, jupyter.
3. Open `ETL_Traffic_Data_Analysis.ipynb` and run all cells.

## Notes
- Several CSV files are very large and may fail normal GitHub push limits.
- Use sampled data for the repository and keep full raw data outside version control.

## Data Availability
- This public project includes only sample data for demonstration and reproducibility.
- The full dataset is proprietary and is not shared in this repository.
- To run with private full data, place the original files in `data/raw/` and keep lightweight samples in `data/sample/`.
