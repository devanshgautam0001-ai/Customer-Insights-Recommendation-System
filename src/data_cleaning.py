import pandas as pd
import os

# Dataset folder path
DATASET_PATH = "dataset"

# CSV files to load
files = [
    "olist_customers_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
    "olist_geolocation_dataset.csv"
]

print("=" * 60)
print("DATA CLEANING STARTED")
print("=" * 60)

for file in files:
    path = os.path.join(DATASET_PATH, file)

    df = pd.read_csv(path)

    print(f"\n📄 {file}")
    print("-" * 60)

    print(f"Rows : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())

print("\n✅ Data Cleaning Completed")