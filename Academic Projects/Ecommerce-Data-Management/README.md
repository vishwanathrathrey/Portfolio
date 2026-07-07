# E-commerce Product Data Management System

## Overview

This project implements a complete data management system for an e-commerce platform, demonstrating practical skills in handling multiple file formats (CSV, JSON, TXT) through Python. The system manages three interconnected data components: product sales data (CSV), product details (JSON), and product descriptions (TXT), using Stock Keeping Unit (SKU) as the primary identifier.

The workflow showcases essential data engineering concepts including file I/O operations, data serialization, directory management, and the creation of a unified CRUD (Create, Read, Update, Delete) interface for product information management.

## Dataset

- **Expected Format**: Multi-format dataset consisting of:
  - CSV: Product sales data with columns Product_SKU, Day1 through Day14
  - JSON: Product details with attributes like product_name, brand, model, specifications, price, availability
  - TXT: Product descriptions as plain text files
- **Primary Key**: SKU (Stock Keeping Unit) - 13-character unique identifier
- **Note**: The actual dataset is not included in this repository. The notebook contains the complete implementation logic and can be adapted to work with any dataset following the specified format.

## Objectives

- Read and parse data from CSV, JSON, and TXT file formats using Python
- Implement a unified data loading mechanism for heterogeneous data sources
- Create update functions for each data type (sales, details, descriptions)
- Build an interactive update system for adding/modifying product information
- Persist modified data back to original file formats while maintaining data integrity
- Demonstrate file handling, directory management, and data serialization techniques

## Project Workflow

### 1. Environment Setup
- Imported required libraries: `os` (file navigation), `json` (JSON handling), `csv` (CSV operations), `pandas` (data manipulation)
- Configured Google Colab environment for file upload and extraction (optional)

### 2. Data Loading
- Implemented `load_data()` function to read all data sources:
  - Parsed CSV sales data using `csv.DictReader`
  - Loaded JSON product details from individual files
  - Read TXT product descriptions from separate files
- Organized data into dictionaries keyed by SKU for efficient lookup

### 3. Data Update Operations
- **Sales Data Update**: `update_sales_data()` - Updates 14-day sales quantities for a given SKU
- **Product Details Update**: `update_product_details()` - Updates or adds product attribute dictionary
- **Product Description Update**: `update_product_description()` - Updates product description text
- **Unified Update Interface**: `update()` function that orchestrates all three operations with interactive user input

### 4. Data Persistence
- Implemented `dump_data()` function for saving data back to disk:
  - CSV writing using `csv.DictWriter` with proper headers
  - JSON serialization with indentation for readability
  - TXT file writing with clean formatting
- Automatic directory creation for missing folders
- Preserved file naming conventions and directory structure

## Techniques and Concepts Applied

| Technique | Application |
|-----------|-------------|
| **Multi-format File I/O** | Reading/writing CSV, JSON, and TXT files |
| **CSV Parsing** | Using `csv.DictReader` and `csv.DictWriter` for structured data |
| **JSON Serialization** | `json.load()` and `json.dump()` for product details |
| **Text File Operations** | `read()` and `write()` for product descriptions |
| **Directory Management** | `os.path` operations and dynamic directory creation |
| **Dictionary-based Data Storage** | SKU-keyed dictionaries for fast lookups |
| **Input Validation** | SKU length validation, sales data format verification |
| **Interactive Data Entry** | User prompts for product information collection |
| **Data Persistence** | Maintaining data across sessions through file storage |
| **Error Handling** | Validation checks and exception handling for user inputs |

## Results

### Data Loading Success
- Successfully loads data from three different file formats into Python data structures
- Creates three dictionaries:
  - `sales_data`: Dictionary mapping SKUs to 14-day sales arrays
  - `product_details`: Dictionary with product attribute dictionaries
  - `product_descriptions`: Dictionary mapping SKUs to description text

### Update Operations Demonstrated
- Successfully adds new products to all three data components
- Updates existing product information when SKU already exists
- Validates input data before processing (SKU format, sales data completeness)

### Data Persistence Verification
- Successfully saves all data back to respective file formats
- Maintains file naming conventions: `details_{SKU}.json`, `description_{SKU}.txt`
- Appends new rows to existing CSV without overwriting existing data
- Maintains data integrity across all file formats

## Key Insights

### Data Organization Patterns
- Using SKU as the primary key across multiple file formats enables consistent data linking
- Dictionary-based data structures in Python provide O(1) lookup time for product operations
- Separating data into different file formats (structured vs. unstructured) follows data engineering best practices

### File Format Selection
- **CSV**: Optimal for tabular sales data with consistent column structure
- **JSON**: Suitable for hierarchical product attributes with varying structures
- **TXT**: Ideal for long-form, unstructured product descriptions

### Input Validation Importance
- SKU length validation prevents incorrect identifier formats
- Sales data validation ensures exactly 14 days of data are provided
- Type validation (integer for sales, float for price) maintains data consistency

### Automation Benefits
- The unified `update()` function reduces manual data entry errors
- Automated directory creation prevents file path errors
- Batch processing capability demonstrated by handling multiple file types simultaneously

## Key Learnings

### 1. Multi-format Data Integration
Working with heterogeneous data sources requires careful handling of different file formats, each with its own parsing requirements and serialization methods. The project demonstrated how to create a unified interface while respecting format-specific considerations.

### 2. Data Persistence Patterns
The complete CRUD cycle (Create → Update → Persist) is essential for practical data management systems. Understanding how to read from and write to various file formats while maintaining data integrity is a fundamental data engineering skill.

### 3. Directory Management
Dynamic directory creation and path manipulation using `os.path` is critical for robust file operations. Ensuring directories exist before writing files prevents runtime errors in production systems.

### 4. Input Validation and Error Handling
User-facing data entry functions require thorough input validation. The project incorporated SKU format validation, sales data count validation, and type checking to prevent corrupted data entries.

### 5. Scalable Data Structures
Using dictionaries keyed by unique identifiers (SKU) allows for efficient data retrieval and updates, demonstrating how in-memory data structures can mirror database-like functionality for small to medium datasets.

## Repository Structure
```
Ecommerce-Data-Management/
├── File_Handling.ipynb # Complete implementation
└── README.md
```

## Getting Started

1. **Prepare your data**: Organize your product data following the expected format:
   - Create a sales CSV file with columns: `Product_SKU, Day1, Day2, ..., Day14`
   - Place product detail JSON files in a `product_details/` directory
   - Place product description TXT files in a `product_descriptions/` directory

2. **Update the path**: Modify the `main_folder_address` variable in the notebook to point to your data directory

3. **Run the notebook**: Execute cells sequentially to load, update, and save your product data

4. **Interact with the system**: Use the `update()` function to add or modify products interactively

## Notes

- The actual dataset is not included in this repository; the notebook is designed to work with any dataset following the specified format
- All file operations are performed using Python's standard library (os, json, csv)
- No external dependencies are required beyond Python's standard library
- The update function (`update()`) includes comprehensive input validation and error checking
- The system expects SKUs to be exactly 13 characters long

This project was completed as part of my **MSc in Machine Learning and Artificial Intelligence**, demonstrating proficiency in Python file handling, data serialization, and building practical data management systems for e-commerce applications.