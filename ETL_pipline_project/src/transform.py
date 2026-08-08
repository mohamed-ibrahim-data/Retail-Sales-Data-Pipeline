import pandas as pd
import numpy as np
from datetime import datetime
from extract import customers, products, stores, sales


def transform_customers(customers):
    if customers is None:
        return None

    cleaned_customers = customers.copy()
    cleaned_customers = cleaned_customers.dropna()

    # concatenate first_name and last_name into a new column called full_name
    cleaned_customers['full_name'] = cleaned_customers['first_name'] + ' ' + cleaned_customers['last_name']
    cleaned_customers.drop(columns=['first_name', 'last_name'], inplace=True)

    # convert birthdate to datetime and calculate age
    cleaned_customers['birthdate'] = pd.to_datetime(cleaned_customers['birthdate'], errors='coerce')
    cleaned_customers['age'] = datetime.now().year - cleaned_customers['birthdate'].dt.year

    # marital_status: convert 'M' to 1 and 'S' to 0
    cleaned_customers['marital_status'] = cleaned_customers['marital_status'].map({'M': 1, 'S': 0})

    # yearly_income: remove '$', 'K', and '+' characters, split into min and max income,
    # convert to float and multiply by 1000 and drop the original column
    cleaned_customers['yearly_income'] = cleaned_customers['yearly_income'].str.replace(r'[\$,K +]', '', regex=True)
    cleaned_customers[['min_yearly_income','max_yearly_income']] = cleaned_customers['yearly_income'].str.split('-', expand=True)
    cleaned_customers['min_yearly_income'] = cleaned_customers['min_yearly_income'].astype(float) * 1000
    cleaned_customers['max_yearly_income'] = cleaned_customers['max_yearly_income'].astype(float) * 1000
    cleaned_customers.drop(columns='yearly_income', inplace=True)

    # acct_open_date: convert to datetime
    cleaned_customers['acct_open_date'] = pd.to_datetime(cleaned_customers['acct_open_date'], errors = 'coerce')

    # homeowner: convert 'Y' to 1 and 'N' to 0
    cleaned_customers['homeowner'] = cleaned_customers['homeowner'].map({'Y': 1, 'N': 0})

    # select the final columns for the cleaned customers data
    cleaned_customers = cleaned_customers[['customer_id','full_name', 'customer_acct_num', 'customer_address', 'customer_city',
       'customer_state_province', 'customer_postal_code', 'customer_country',
       'birthdate', 'age', 'marital_status', 'gender', 'total_children',
       'num_children_at_home', 'education', 'acct_open_date', 'member_card',
       'min_yearly_income', 'max_yearly_income', 'occupation', 'homeowner']]

    return cleaned_customers


customers_cleaned = transform_customers(customers)
# print(customers_cleaned['customer_acct_num'])

def transform_products(products):
    if products is None:
        return None

    cleaned_products = products.copy()

    # calculate profit margin as product_retail_price - product_cost
    cleaned_products['profit_margin'] = cleaned_products['product_retail_price'] - cleaned_products['product_cost']

    # fill missing values in recyclable and low_fat columns with '0' and convert to integer
    cleaned_products['recyclable'] = cleaned_products['recyclable'].fillna('0').astype(int)
    cleaned_products['low_fat'] = cleaned_products['low_fat'].fillna('0').astype(int)

    # select the final columns for the cleaned products data
    cleaned_products = cleaned_products[['product_id', 'product_brand', 'product_name', 'product_sku',
       'product_retail_price', 'product_cost', 'profit_margin', 'product_weight', 'recyclable',
       'low_fat']]

    return cleaned_products


products_cleaned = transform_products(products)
# print(products_cleaned.info())   

def transform_stores(stores):
    if stores is None:
        return None

    cleaned_stores = stores.copy()

    # remove dashes from store_phone
    cleaned_stores['store_phone'] = cleaned_stores['store_phone'].str.replace('-', '')

    # convert first_opened_date and last_remodel_date to datetime, coerce errors to NaT
    cleaned_stores['first_opened_date'] = pd.to_datetime(cleaned_stores['first_opened_date'], errors='coerce')
    cleaned_stores['last_remodel_date'] = pd.to_datetime(cleaned_stores['last_remodel_date'], errors='coerce')

    return cleaned_stores


stores_cleaned = transform_stores(stores)
# print(stores_cleaned.info())


def transform_sales(sales):
    if sales is None:
        return None

    cleaned_sales = sales.copy()

    # convert transaction_date and stock_date to datetime, coerce errors to NaT
    cleaned_sales['transaction_date'] = pd.to_datetime(cleaned_sales['transaction_date'], errors='coerce')
    cleaned_sales['stock_date'] = pd.to_datetime(cleaned_sales['stock_date'], errors='coerce')

    # calculate time_to_sell as the difference in days between transaction_date and stock_date
    cleaned_sales['time_to_sell_by_days'] = (cleaned_sales['transaction_date'] - cleaned_sales['stock_date']).dt.days

    # merge cleaned_sales with products_cleaned to include profit_margin
    cleaned_sales = pd.merge(products_cleaned[['profit_margin','product_id']], cleaned_sales, on=['product_id'], how='left')

    # calculate total_profit as profit_margin * quantity
    cleaned_sales['total_profit']  = cleaned_sales['profit_margin'] * cleaned_sales['quantity']

    # convert columns to appropriate data types
    cleaned_sales['time_to_sell_by_days'] = cleaned_sales['time_to_sell_by_days'].astype('Int64')
    cleaned_sales['customer_id'] = cleaned_sales['customer_id'].astype('Int64')
    cleaned_sales['store_id'] = cleaned_sales['store_id'].astype('Int64')
    cleaned_sales['quantity'] = cleaned_sales['quantity'].astype('Int64')

    # select the final columns for the cleaned sales data
    cleaned_sales = cleaned_sales[['transaction_date', 'stock_date', 'time_to_sell_by_days', 'customer_id', 'product_id', 'store_id', 'quantity','profit_margin','total_profit']]

    return cleaned_sales


sales_cleaned = transform_sales(sales)
# print(sales_cleaned.info())
