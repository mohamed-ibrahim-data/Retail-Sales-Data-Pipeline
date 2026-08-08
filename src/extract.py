import pandas as pd

def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

# Extract data from CSV files
customers = extract(r'e-commerce_data\Customers.csv')
products = extract(r'e-commerce_data\Products.csv')
stores = extract(r'e-commerce_data\Stores.csv')
sales = extract(r'e-commerce_data\Sales.csv')
