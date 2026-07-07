# E-commerce Product Data Management System

## Overview

This project implements a complete data management system for an e-commerce platform, demonstrating practical skills in handling multiple file formats (CSV, JSON, TXT) through Python. The system manages three interconnected data components: product sales data (CSV), product details (JSON), and product descriptions (TXT), using Stock Keeping Unit (SKU) as the primary identifier. The workflow showcases essential data engineering concepts including file I/O operations, data serialization, directory management, and the creation of a unified CRUD (Create, Read, Update, Delete) interface.

## Recruiter Snapshot

This project demonstrates:
- **Data Engineering Fundamentals:** Competency in core data engineering tasks, including reading, parsing, and writing data in multiple formats (CSV, JSON, TXT).
- **Multi-format Data Integration:** Ability to build a unified system that integrates heterogeneous data sources using a common key (SKU).
- **CRUD Operations:** Implementation of a complete Create, Read, Update, and Delete interface for managing product data, a foundational skill for any data management system.
- **Data Persistence and Integrity:** Experience in persisting changes back to their original file formats while maintaining data structure and integrity.
- **System Design with Standard Libraries:** Proficiency in building a functional data management tool using only Python's standard libraries (`os`, `json`, `csv`), showcasing resourcefulness and a strong grasp of fundamentals.

## Dataset

- **Expected Format**: Multi-format dataset consisting of:
  - CSV: Product sales data with columns `Product_SKU`, `Day1` through `Day14`.
  - JSON: Product details (attributes like name, price, category).
  - TXT: Product descriptions as plain text files.
- **Primary Key**: SKU (Stock Keeping Unit) - 13-character unique identifier.
- **Note**: The actual dataset is not included in this repository. The notebook contains the complete implementation logic.

## Objectives

- Read and parse data from CSV, JSON, and TXT file formats using Python.
- Implement a unified data loading mechanism for heterogeneous data sources.
- Create update functions for each data type (sales, details, descriptions).
- Build an interactive update system for adding/modifying product information.
- Persist modified data back to original file formats while maintaining data integrity.
- Demonstrate file handling, directory management, and data serialization techniques.

## Project Workflow

1.  **Environment Setup:**
    - Imported required libraries: `os` (file navigation), `json` (JSON handling), `csv` (CSV operations).
2.  **Data Loading:**
    - Implemented `load_data()` function to read all data sources:
      - Parsed CSV sales data using `csv.DictReader`.
      - Loaded JSON product details using `json.load()`.
      - Read TXT product descriptions from separate files.
    - Organized data into dictionaries keyed by SKU for efficient lookup.
3.  **Data Update Operations:**
    - **Sales Data Update**: `update_sales_data()` - Updates 14-day sales quantities for a given SKU.
    - **Product Details Update**: `update_product_details()` - Updates or adds product attribute dictionary.
    - **Product Description Update**: `update_product_description()` - Updates product description text.
    - **Unified Update Interface**: `update()` function that orchestrates all three operations with interactive user input.
4.  **Data Persistence:**
    - Implemented `dump_data()` function for saving data back to disk:
      - Wrote to CSV using `csv.DictWriter` with proper headers.
      - Serialized to JSON using `json.dump()`.
      - Wrote to TXT files with clean formatting.
    - Included logic for automatic directory creation for missing folders.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Multi-format File I/O** | Reading/writing CSV, JSON, and TXT files using Python's standard libraries. |
| **CSV Parsing** | Using `csv.DictReader` and `csv.DictWriter` for structured, row-based data. |
| **JSON Serialization** | Using `json.load()` and `json.dump()` for semi-structured, nested data. |
| **File & Directory Management** | Using the `os` module for path manipulation, directory creation, and file iteration. |
| **Data Structures** | Using dictionaries as the primary in-memory data structure for efficient, key-based lookups. |
| **CRUD Interface** | Implementing Create, Read, Update, Delete logic for a complete data management cycle. |
| **Interactive Input** | Using Python's `input()` function to create a simple, interactive command-line interface. |

## Key Learnings

- **Handling Heterogeneous Data:** This project provided practical experience in designing a system that can ingest and manage data from different file formats, a common challenge in real-world data pipelines.
- **Importance of a Unified Key:** Using the SKU as a consistent primary key across all data sources was essential for successfully joining and managing the disparate datasets.
- **Idempotent Write Operations:** The `dump_data` function was designed to be idempotent, meaning it can be run multiple times without creating duplicate data, ensuring data integrity.
- **Building from Scratch:** Implementing the entire system with only standard libraries reinforced a deep understanding of fundamental data handling and serialization concepts.

## Future Work

- **Database Integration:** Replace the file-based storage with a relational database (like SQLite or PostgreSQL) to improve scalability, transactional integrity, and querying capabilities.
- **Web Interface:** Build a simple web interface using Flask or FastAPI to replace the command-line input, making the system more user-friendly.
- **Error Handling & Validation:** Implement more robust error handling and data validation (e.g., using Pydantic) to ensure data quality upon ingestion and update.

## Repository Structure

```
Ecommerce-Data-Management/
├── File_Handling.ipynb     # Jupyter Notebook with all the code
└── README.md               # This file
```

## Notes
- This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating proficiency in Python file handling, data serialization, and building practical data management systems for e-commerce applications.
