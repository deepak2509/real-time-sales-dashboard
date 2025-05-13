import json
import uuid
import random
import time
from datetime import datetime
from faker import Faker
import os

# Initialize Faker
fake = Faker()

# Define the list of SKUs and regions
SKUs = ['SKU12345', 'SKU67890', 'SKU54321', 'SKU98765', 'SKU11223']
regions = ['North', 'South', 'East', 'West', 'Central']

# Function to generate a single sales record
def generate_sale_record():
    return {
        "order_id": str(uuid.uuid4()),
        "product_id": random.choice(SKUs),
        "amount": round(random.uniform(10.0, 200.0), 2),
        "quantity": random.randint(1, 5),
        "region": random.choice(regions),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# Stream sales data dynamically
while True:
    order = generate_sale_record()  # Generate a new sale record
    with open("data_simulation/streamed_sales.json", "a") as f:  # Open the file in append mode
        f.write(json.dumps(order) + "\n")  # Write the order as a JSON object on a new line
    print(order)  # Print the generated order for debugging purposes
    time.sleep(1)  # Simulate 1 new order per second
