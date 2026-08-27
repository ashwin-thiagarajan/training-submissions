import numpy as np
import pandas as pd

def calculate_avg_sales(sales):
    return np.mean(sales)
def calculate_min_sales(sales):
    return np.min(sales)
def calculate_max_sales(sales):
    return np.max(sales)

def create_sales_df():
    data = {'product': ['A', 'B'], 'quantity': [10, 2], 'price': [100, 5],'region':['North America','Europe']}
    return pd.DataFrame(data)

def filter_high_selling_products(df,threshold = 5):
    return df[df['quantity'] > threshold]

def group_revenue_by_region(df):
    return df.groupby('region')['quantity'].sum().reset_index()

def main():
    sales_df = create_sales_df()
    print(filter_high_selling_products(sales_df))
    print(group_revenue_by_region(sales_df))
    print(calculate_avg_sales([2,1,3,5,4]))
    print(calculate_min_sales([2,1,3,5,4]))
    print(calculate_max_sales([2,1,3,5,4]))

if __name__ == '__main__':
    main()