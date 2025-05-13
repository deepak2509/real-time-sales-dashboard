# etl_scripts/transform_sales.py
import pandas as pd

def transform_sales_data(records):
    df = pd.DataFrame(records)
    df = df.dropna()  # Drop nulls
    df['amount'] = df['amount'].astype(float)
    df['quantity'] = df['quantity'].astype(int)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df
