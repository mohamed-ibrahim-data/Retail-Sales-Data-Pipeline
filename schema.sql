-- =======================================================
-- Retail Sales Datawarehouse Schema (SQL Server)
-- =======================================================
USE SalesDW

DROP TABLE IF EXISTS fact_sales
DROP TABLE IF EXISTS dim_customers
DROP TABLE IF EXISTS dim_products
DROP TABLE IF EXISTS dim_stores
GO

CREATE TABLE dim_customers(
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(70),
    customer_acct_num BIGINT,
    customer_address VARCHAR(70),
    customer_city VARCHAR(50),
    customer_state_province VARCHAR(70),
    customer_postal_code INT,
    customer_country VARCHAR(50),
    birthdate DATETIME2,
    age INT,
    marital_status INT,
    gender VARCHAR(5),
    total_children INT,
    num_children_at_home INT,
    education VARCHAR(70),
    acct_open_date DATETIME2,
    member_card VARCHAR(20),
    min_yearly_income DECIMAL(10,2),
    max_yearly_income DECIMAL(10,2),
    occupation VARCHAR(70),
    homeowner INT
);

CREATE TABLE dim_products(
    product_id INT PRIMARY KEY,
    product_brand VARCHAR(70),
    product_name VARCHAR(70),
    product_sku BIGINT,
    product_retail_price DECIMAL(10,2),
    product_cost DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    product_weight DECIMAL(10,2),
    recyclable INT DEFAULT 0,
    low_fat INT DEFAULT 0
);

CREATE TABLE dim_stores(
    store_id INT PRIMARY KEY,
    region_id INT,
    store_type VARCHAR(60),
    store_name VARCHAR(60),
    store_street_address VARCHAR(60),
    store_city VARCHAR(50),
    store_state VARCHAR(50),
    store_country VARCHAR(50),
    store_phone VARCHAR(20),
    first_opened_date DATETIME2,
    last_remodel_date DATETIME2,
    total_sqft INT,
    grocery_sqft INT,
);

CREATE TABLE fact_sales(
    transaction_date DATETIME2,
    stock_date DATETIME2,
    time_to_sell_by_days INT,
    customer_id INT,
    product_id INT,
    store_id INT,
    quantity INT,
    profit_margin DECIMAL(10,2),
    total_profit DECIMAL(10,2)


    CONSTRAINT fk_sales_customers FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    CONSTRAINT fk_sales_products FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
    CONSTRAINT fk_sales_stores FOREIGN KEY (store_id) REFERENCES dim_stores(store_id)
);
GO
