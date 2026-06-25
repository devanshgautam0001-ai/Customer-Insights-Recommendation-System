import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------
# Load Master Dataset
# ----------------------------

df = pd.read_csv("reports/master_dataset.csv")

print("=" * 60)
print("EDA STARTED")
print("=" * 60)

print("Dataset Shape:", df.shape)
print(df.head())

# Create assets folder
os.makedirs("assets", exist_ok=True)

sns.set_style("whitegrid")

# ----------------------------
# Order Status Distribution
# ----------------------------

plt.figure(figsize=(8,5))
sns.countplot(data=df, x="order_status", order=df["order_status"].value_counts().index)
plt.xticks(rotation=30)
plt.title("Order Status Distribution")
plt.tight_layout()
plt.savefig("assets/order_status.png")
plt.close()

# ----------------------------
# Payment Type
# ----------------------------

plt.figure(figsize=(8,5))
sns.countplot(data=df, x="payment_type", order=df["payment_type"].value_counts().index)
plt.xticks(rotation=30)
plt.title("Payment Type")
plt.tight_layout()
plt.savefig("assets/payment_type.png")
plt.close()

# ----------------------------
# Review Score
# ----------------------------

plt.figure(figsize=(8,5))
sns.countplot(data=df, x="review_score")
plt.title("Review Score Distribution")
plt.tight_layout()
plt.savefig("assets/review_score.png")
plt.close()

# ----------------------------
# Top States
# ----------------------------

top_states = df["customer_state"].value_counts().head(10)

plt.figure(figsize=(9,5))
sns.barplot(x=top_states.values, y=top_states.index)
plt.title("Top Customer States")
plt.tight_layout()
plt.savefig("assets/customer_states.png")
plt.close()

# ----------------------------
# Top Product Categories
# ----------------------------

top_cat = df["product_category_name"].value_counts().head(10)

plt.figure(figsize=(10,5))
sns.barplot(x=top_cat.values, y=top_cat.index)
plt.title("Top Product Categories")
plt.tight_layout()
plt.savefig("assets/top_categories.png")
plt.close()

# ----------------------------
# Monthly Orders
# ----------------------------

df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

monthly = (
    df.groupby(df["order_purchase_timestamp"].dt.to_period("M"))
    .size()
)

monthly.index = monthly.index.astype(str)

plt.figure(figsize=(12,5))
monthly.plot(marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Orders")
plt.tight_layout()
plt.savefig("assets/monthly_orders.png")
plt.close()

# ----------------------------
# Correlation Heatmap
# ----------------------------

numeric = df.select_dtypes(include="number")

plt.figure(figsize=(10,8))
sns.heatmap(numeric.corr(), cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("assets/correlation_heatmap.png")
plt.close()

# ----------------------------
# Business Insights
# ----------------------------

report = f"""
==============================
EDA REPORT
==============================

Total Customers : {df['customer_unique_id'].nunique()}

Total Orders : {df['order_id'].nunique()}

Total Products : {df['product_id'].nunique()}

Average Review Score :
{df['review_score'].mean():.2f}

Most Used Payment Method :
{df['payment_type'].mode()[0]}

Most Common Order Status :
{df['order_status'].mode()[0]}

Top Customer State :
{df['customer_state'].mode()[0]}

Top Product Category :
{df['product_category_name'].mode()[0]}

"""

with open("reports/eda_report.txt", "w") as f:
    f.write(report)

print(report)

print("=" * 60)
print("EDA COMPLETED")
print("Charts Saved in assets/")
print("Report Saved in reports/")
print("=" * 60)