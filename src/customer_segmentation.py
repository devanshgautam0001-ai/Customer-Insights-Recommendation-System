import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("="*60)
print("CUSTOMER SEGMENTATION STARTED")
print("="*60)

df = pd.read_csv("reports/feature_engineered_dataset.csv")

print("Dataset Loaded")
print(df.shape)

# ==========================
# RFM TABLE
# ==========================

rfm = df.groupby("customer_unique_id").agg(
{
    "order_purchase_timestamp":"max",
    "order_id":"nunique",
    "payment_value":"sum"
})

rfm.columns=[
    "LastPurchase",
    "Frequency",
    "Monetary"
]

rfm.reset_index(inplace=True)

rfm["LastPurchase"]=pd.to_datetime(rfm["LastPurchase"])

latest_date=rfm["LastPurchase"].max()

rfm["Recency"]=(latest_date-rfm["LastPurchase"]).dt.days

rfm=rfm[["customer_unique_id","Recency","Frequency","Monetary"]]

print(rfm.head())

print("\nCustomers :",len(rfm))

# ==========================
# Scaling
# ==========================

X=rfm[["Recency","Frequency","Monetary"]]

scaler=StandardScaler()

X_scaled=scaler.fit_transform(X)

print("Scaling Completed")

# ==========================
# KMeans
# ==========================

kmeans=KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["Cluster"]=kmeans.fit_predict(X_scaled)

print("KMeans Completed")

# ==========================
# Cluster Names
# ==========================

mapping={
0:"Premium",
1:"Loyal",
2:"Regular",
3:"At Risk"
}

rfm["CustomerSegment"]=rfm["Cluster"].map(mapping)

print(rfm["CustomerSegment"].value_counts())

rfm.to_csv(
"reports/customer_segments.csv",
index=False
)

print("="*60)
print("SEGMENTATION COMPLETED")
print("Saved -> reports/customer_segments.csv")
print("="*60)