import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sales_data(num_orders=1000):
    # Set seed for reproducibility
    np.random.seed(42)
    
    # Core data components
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = {
        'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Tablet', 'Smartwatch'],
        'Furniture': ['Chair', 'Table', 'Sofa', 'Bookshelf', 'Desk'],
        'Office Supplies': ['Pen', 'Paper', 'Binder', 'Folder', 'Stapler']
    }
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(1, num_orders + 1):
        order_id = f'ORD-{1000 + i}'
        date = start_date + timedelta(days=np.random.randint(0, 425)) # ~14 months
        region = np.random.choice(regions)
        category = np.random.choice(list(categories.keys()))
        product = np.random.choice(categories[category])
        
        # Sales and Quantity logic
        quantity = np.random.randint(1, 11)
        base_price = {
            'Electronics': 200,
            'Furniture': 150,
            'Office Supplies': 20
        }[category]
        
        sales = round(base_price * quantity * np.random.uniform(0.8, 1.2), 2)
        # Profit standard margin roughly 15-30%
        profit = round(sales * np.random.uniform(0.1, 0.35), 2)
        
        data.append([order_id, date, region, product, category, sales, quantity, profit])

    df = pd.DataFrame(data, columns=['Order ID', 'Date', 'Region', 'Product', 'Category', 'Sales', 'Quantity', 'Profit'])
    
    # Introduce some "dirty" data for cleaning practice
    # 1. Duplicates
    df = pd.concat([df, df.head(10)], ignore_index=True)
    
    return df

def clean_data(df):
    # 1. Remove duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_len - len(df)} duplicates.")
    
    # 2. Ensure Date format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 3. Create Calculated Columns
    df['Profit Margin'] = (df['Profit'] / df['Sales']).round(4)
    df['Month-Year'] = df['Date'].dt.strftime('%b-%Y')
    
    return df

if __name__ == "__main__":
    output_dir = "d:/data analysis/Sales_Dashboard_Project/data"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating raw data...")
    raw_df = generate_sales_data()
    
    print("Cleaning data...")
    cleaned_df = clean_data(raw_df)
    
    output_path = os.path.join(output_dir, "sales_data.csv")
    cleaned_df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
