def clean_record(record):
    required_keys = {"order_id", "product_id", "amount", "quantity", "region", "timestamp"}
    if not all(key in record for key in required_keys):
        return None
    if not isinstance(record["amount"], (int, float)) or record["amount"] < 0:
        return None
    if not isinstance(record["quantity"], int) or record["quantity"] <= 0:
        return None
    return record

def transform_sales_data(raw_records):
    return [clean_record(rec) for rec in raw_records if clean_record(rec)]
