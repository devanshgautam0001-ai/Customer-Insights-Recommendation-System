import pandas as pd
import os

# ============================
# Load Datasets
# ============================

DATASET_PATH = "dataset"

customers = pd.read_csv(os.path.join(DATASET_PATH, "olist_customers_dataset.csv"))
orders = pd.read_csv(os.path.join(DATASET_PATH, "olist_orders_dataset.csv"))
items = pd.read_csv(os.path.join(DATASET_PATH, "olist_order_items_dataset.csv"))
products = pd.read_csv(os.path.join(DATASET_PATH, "olist_products_dataset.csv"))
payments = pd.read_csv(os.path.join(DATASET_PATH, "olist_order_payments_dataset.csv"))
reviews = pd.read_csv(os.path.join(DATASET_PATH, "olist_order_reviews_dataset.csv"))

print("=" * 60)
print("DATASETS LOADED SUCCESSFULLY")
print("=" * 60)

print("Customers :", customers.shape)
print("Orders    :", orders.shape)
print("Items     :", items.shape)
print("Products  :", products.shape)
print("Payments  :", payments.shape)
print("Reviews   :", reviews.shape)

# ============================
# Merge Customers + Orders
# ============================

master = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="left"
)

print("\nAfter Orders + Customers :", master.shape)

# ============================
# Merge Order Items
# ============================

master = pd.merge(
    master,
    items,
    on="order_id",
    how="left"
)

print("After Order Items        :", master.shape)

# ============================
# Merge Products
# ============================

master = pd.merge(
    master,
    products,
    on="product_id",
    how="left"
)

print("After Products           :", master.shape)

# ============================
# Merge Payments
# ============================

master = pd.merge(
    master,
    payments,
    on="order_id",
    how="left"
)

print("After Payments           :", master.shape)

# ============================
# Merge Reviews
# ============================

master = pd.merge(
    master,
    reviews,
    on="order_id",
    how="left"
)

print("After Reviews            :", master.shape)

# ============================
# Remove Duplicate Columns
# ============================

master = master.loc[:, ~master.columns.duplicated()]

# ============================
# Missing Values
# ============================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = master.isnull().sum()
missing = missing[missing > 0]

if len(missing) == 0:
    print("No Missing Values")
else:
    print(missing)

# ============================
# Duplicate Rows
# ============================

print("\nDuplicate Rows :", master.duplicated().sum())

# ============================
# Final Shape
# ============================

print("\nFinal Dataset Shape :", master.shape)

# ============================
# Save Dataset
# ============================

os.makedirs("reports", exist_ok=True)

master.to_csv(
    "reports/master_dataset.csv",
    index=False
)

print("\nMaster Dataset Created Successfully")
print("Saved at : reports/master_dataset.csv")
print("=" * 60)