import pandas as pd
from sqlalchemy import create_engine
import urllib

def get_db_engine(server, database):

    driver = 'ODBC Driver 17 for SQL Server'

    raw_con_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    encoded_con_str = urllib.parse.quote_plus(raw_con_str)

    db_url = f'mssql+pyodbc:///?odbc_connect={encoded_con_str}'

    try:
        print(f'Attempting to connect to the database: {database} on server: {server}')
        engine = create_engine(db_url)

        with engine.connect() as connection:
            print(f'Successfully connected to the database: {database} on server: {server}')
            return engine

    except Exception as e:
        print(f'Failed to connect to the database: {database} on server: {server}.')
        print(f'Error Details: {e}')
        return None


# server = r'localhost\SQLEXPRESS'
# database = 'SalesDW'
# engine = get_db_engine(server, database)

def load_data(df, table_name, engine):

    if df is not None and not df.empty:
        try:
            print(f'Loading data into table: {table_name}')

            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f'Successfully loaded data into table: {table_name}')

        except Exception as e:
            print(f'Failed to load data into table: {table_name}.')
            print(f'Error Details: {e}')
    else:
        print(f'Warning: No data available to load into table {table_name}.')
           