# NYC Taxi Analysis

## Project Overview
This project performs exploratory data analysis on NYC taxi trip records and zone information to uncover demand and trip behavior patterns.

## Files
- `EDA_NYC_Taxi_Analysis.ipynb`: Main EDA notebook.
- `Datasets and Dictionary-NYC/Datasets and Dictionary/trip_records/`: Monthly trip parquet files.
- `Datasets and Dictionary-NYC/Datasets and Dictionary/taxi_zones/`: Taxi zone shapefile components.
- `Datasets and Dictionary-NYC/Datasets and Dictionary/data_dictionary_trip_records_yellow.pdf`: Data dictionary.

## What This Project Covers
- Data loading from parquet files
- EDA on trip patterns and usage trends
- Zone-level context for trip analysis

## How to Run
1. Create and activate a Python environment.
2. Install core libraries: pandas, numpy, matplotlib, seaborn, pyarrow, jupyter.
3. Open `EDA_NYC_Taxi_Analysis.ipynb` and run all cells.

## Notes
- Monthly parquet files are large; avoid pushing full raw data to standard GitHub repositories.
- Prefer samples in repo plus links/instructions for full dataset access.

## Data Availability
- This public project includes only sample data for demonstration and reproducibility.
- The full dataset is proprietary and is not shared in this repository.
- To run with private full data, place the original files in `data/raw/` and keep lightweight samples in `data/sample/`.
