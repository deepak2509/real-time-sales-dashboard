import os
import boto3
import pandas as pd
import io

# AWS credentials (development only — secure appropriately in production)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = 'us-east-2'

# S3 settings
bucket_name = os.getenv("S3_BUCKET_NAME", "salesproject-1")
key_prefix = os.getenv("S3_KEY_PREFIX", "sales-data8")

def load_to_s3(data: list, format='parquet'):
    df = pd.DataFrame(data)

    # ✅ Keep timestamps as datetime (not strings)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    date = pd.to_datetime('now').strftime('%Y-%m-%d')
    key = f"{key_prefix}/dt={date}/sales_data.{format}"

    buffer = io.BytesIO()
    if format == 'parquet':
        # ✅ Keep timestamp in datetime64[ns] and write as Parquet
        df.to_parquet(buffer, index=False, engine='pyarrow')
    elif format == 'csv':
        df.to_csv(buffer, index=False)

    buffer.seek(0)
    s3.upload_fileobj(buffer, Bucket=bucket_name, Key=key)
    print(f"✅ Uploaded to s3://{bucket_name}/{key}")

# Example usage
if __name__ == "__main__":
    sample_data = [
        {
            "order_id": "abc123",
            "product_id": "SKU123",
            "amount": 99.99,
            "quantity": 2,
            "region": "East",
            "timestamp": "2025-05-13T12:34:56Z"
        }
    ]
    load_to_s3(sample_data)
