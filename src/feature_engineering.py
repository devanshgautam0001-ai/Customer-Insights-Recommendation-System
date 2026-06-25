import pandas as pd
import numpy as np

print("=" * 60)
print("FEATURE ENGINEERING STARTED")
print("=" * 60)

# Load Master Dataset
df = pd.read_csv("reports/master_dataset.csv")

print("\nMaster Dataset Loaded Successfully")
print("Shape :", df.shape)

# Convert Date Columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

print("\nDate Columns Converted Successfully")

print("\nDataset Columns:\n")
for column in df.columns:
    print(column)

print("\nTotal Columns :", len(df.columns))

print("\nPreview:\n")
print(df.head())

print("\n" + "=" * 60)
print("STEP 1 COMPLETED")
print("=" * 60)

# ============================================================
# FEATURE ENGINEERING
# ============================================================

print("\nCreating New Features...\n")

# Total Order Value
df["total_order_value"] = (
    df["price"].fillna(0) +
    df["freight_value"].fillna(0)
)

# Delivery Time
df["delivery_days"] = (
    df["order_delivered_customer_date"] -
    df["order_purchase_timestamp"]
).dt.days

# Approval Time
df["approval_days"] = (
    df["order_approved_at"] -
    df["order_purchase_timestamp"]
).dt.days

# Estimated Delay
df["estimated_delay"] = (
    df["order_delivered_customer_date"] -
    df["order_estimated_delivery_date"]
).dt.days

# Review Missing Flag
df["has_review"] = df["review_score"].notna().astype(int)

# High Value Order
median_value = df["total_order_value"].median()

df["high_value_order"] = (
    df["total_order_value"] > median_value
).astype(int)

# Free Shipping
df["free_shipping"] = (
    df["freight_value"] == 0
).astype(int)

print("New Features Created Successfully")

print("\nNew Dataset Shape :", df.shape)

print("\nNew Columns Added :")

new_cols = [
    "total_order_value",
    "delivery_days",
    "approval_days",
    "estimated_delay",
    "has_review",
    "high_value_order",
    "free_shipping"
]

for col in new_cols:
    print("✔", col)

# Save
df.to_csv("reports/feature_engineered_dataset.csv", index=False)

print("\nDataset Saved Successfully")
print("reports/feature_engineered_dataset.csv")

print("\nFEATURE ENGINEERING COMPLETED")
print("=" * 60)