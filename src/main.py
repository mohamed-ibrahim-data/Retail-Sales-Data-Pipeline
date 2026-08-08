from extract import customers, products, stores, sales
from transform import transform_customers, transform_products, transform_stores, transform_sales
from load import get_db_engine, load_data

def run_etl_pipline():

    print('----Starting ETL Pipline----')

    # Extract
    print('Extracting data')

    # Transform
    print('Transform data')
    customers_clean = transform_customers(customers)
    products_clean = transform_products(products)
    stores_clean = transform_stores(stores)
    sales_clean = transform_sales(sales)

    # Loading
    print('Loading data')
    server = r'localhost\SQLEXPRESS'
    database = 'SalesDW'
    engine = get_db_engine(server, database)

    if engine:
        load_data(customers_clean, 'dim_customers', engine)
        load_data(products_clean, 'dim_products', engine)
        load_data(stores_clean, 'dim_stores', engine)
        load_data(sales_clean, 'fact_sales', engine)

    print('ETL Pipline completed')


run_etl_pipline()