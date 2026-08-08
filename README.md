# Retail Sales Data Pipeline

<img width="1707" height="752" alt="pipline_Archticture" src="https://github.com/user-attachments/assets/7cb60099-ac40-458a-926c-0b1426a0fe41" />


## Overview
This project is an end-to-end Automated ETL (Extract, Transform, Load) Pipeline built with Python. It processes real-world retail company data, extracting it from raw CSV files, applying complex business transformations, and loading it into a structured SQL Server Datawarehouse. The primary objective of this pipeline is to prepare clean, analytical-ready datasets for future Business Intelligence (BI) and dashboarding purposes.

## Tech Stack
* Python (Core Orchestration & Logic)
* Pandas (Data Cleaning & Transformation)
* SQLAlchemy & pyodbc (Database Engine & Connections)
* SQL Server (Datawarehouse)
* SSMS (Schema Setup)

## Data Model (Star Schema)
The target data warehouse follows a dimensional modeling approach (Star Schema) to optimize query performance for BI tools. It consists of one central Fact table and three Dimension tables:

<img width="1422" height="782" alt="data_model" src="https://github.com/user-attachments/assets/0356640d-76c3-48a3-a69b-980587cb5bc2" />


## Data Transformations
The transformation phase (`transform.py`) applies several critical business rules and data standardization processes across different datasets to ensure data integrity:

### Customers Data
* Calculated the `age` of each customer by engineering a new feature from the `birthdate` column.
* Cleaned the `yearly_income` column by removing special characters (`-` and `$`), cast the data type from string to integer, and split it into two detailed columns: `min_yearly_income` and `max_yearly_income`.

### Products Data
* Engineered a new `profit_margin` column by calculating the difference between `product_retail_price` and `product_cost`.
* Handled missing data in the `recyclable` and `low_fat` indicator columns (0/1 values) by replacing all `NULL` values with `0`, strictly aligning with business logic requirements.

### Stores Data
* Standardized the `store_phone` format by stripping out dashes (`-`) to ensure clean and consistent numerical records.

### Sales Data (Fact Table)
* Calculated `time_to_sell_by_days` by finding the date difference between `transaction_date` and `stock_date`.
* Merged the `Products` dataset with the `Sales` dataset to inherit the `profit_margin` feature.
* Calculated `total_profit` for each transaction by multiplying `profit_margin` by the sold `quantity`.

### Global Standardizations
* Converted all date-related columns across all datasets from `string` to standard `datetime` objects for accurate time-series analysis in future dashboards.

## Project Structure
```text
etl-sales-pipeline/
├── data/
│   ├── raw/              # Input immutable CSV files
│   └── processed/        # Output transformed data files
├── src/
│   ├── extract.py        # Data extraction logic
│   ├── transform.py      # Cleaning and feature engineering
│   ├── load.py           # Data loading logic
│   ├── database.py       # SQLAlchemy engine and connection setup
│   └── main.py           # ETL Pipeline Orchestrator
├── schema.sql            # SQL script to create the Star Schema (DDL)
├── requirements.txt      # Project dependencies
└── README.md
```

## How to Run the Project
### 1. Prerequisites
* Python 3.x installed.
* SQL Server installed and running locally or remotely.
* ODBC Driver for SQL Server installed (e.g., ODBC Driver 17).

### 2. Database Preparation
* Before running the script, create an empty target database in your SQL Server environment named SalesDW.

### 3. Database Schema Setup (Important)
* Before executing the Python pipeline, you must build the Star Schema (Tables, Primary Keys, and Foreign Keys):
* Open SQL Server Management Studio (SSMS).
* Connect to your SQL Server and select the SalesDW database.
* Open the schema.sql file provided in this repository and click Execute. This will drop any existing tables and create the correct dimensional model.

### 4. Installation
* Clone the repository and install the required dependencies:
```
Bash
git clone <[your_repository_link_here](https://github.com/mohamed-ibrahim-data/Retail-Sales-Data-Pipeline.git)>
cd etl-sales-pipeline
pip install -r requirements.txt
```
### 5. Running the Pipeline
* Execute the main orchestrator script to trigger the full ETL workflow:
```
Bash
python src/main.py
```
