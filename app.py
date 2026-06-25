import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Customer Insights & Recommendation System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main{
    background:#F6F8FC;
}

.block-container{
    padding-top:1rem;
}

.metric-card{
    background:white;
    border-radius:18px;
    padding:18px;
    box-shadow:0px 4px 15px rgba(0,0,0,.08);
}

h1,h2,h3{
    color:#1f2937;
}

</style>
""",unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():

    master=pd.read_csv("reports/master_dataset.csv")
    segment=pd.read_csv("reports/customer_segments.csv")

    return master,segment

master,segment=load_data()

# ---------------- SIDEBAR ----------------

st.sidebar.image(
"https://img.icons8.com/color/96/combo-chart--v1.png",
width=80
)

st.sidebar.title("Dashboard Filters")

state=st.sidebar.selectbox(
"Customer State",
["All"]+sorted(master["customer_state"].dropna().unique())
)

payment=st.sidebar.selectbox(
"Payment Type",
["All"]+sorted(master["payment_type"].dropna().unique())
)

if state!="All":
    master=master[
        master["customer_state"]==state
    ]

if payment!="All":
    master=master[
        master["payment_type"]==payment
    ]

st.sidebar.markdown("---")

st.sidebar.success("ReadyNest Internship Project")

# ---------------- TITLE ----------------

st.title("📊 Customer Insights & Recommendation Dashboard")

st.caption(
"Advanced Analytics Dashboard using Python • Pandas • Plotly • Streamlit"
)

st.divider()

# ---------------- KPI ----------------

customers=master["customer_unique_id"].nunique()

orders=master["order_id"].nunique()

products=master["product_id"].nunique()

revenue=master["payment_value"].sum()

review=round(master["review_score"].mean(),2)

c1,c2,c3,c4,c5=st.columns(5)

c1.metric("Customers",f"{customers:,}")

c2.metric("Orders",f"{orders:,}")

c3.metric("Products",f"{products:,}")

c4.metric("Revenue",f"R$ {revenue:,.0f}")

c5.metric("Review",review)

st.divider()

# =====================================================
# ROW 1
# =====================================================

left,right = st.columns(2)

with left:

    st.subheader("💳 Payment Method Distribution")

    payment_df = (
        master["payment_type"]
        .value_counts()
        .reset_index()
    )

    payment_df.columns=["Payment Type","Orders"]

    fig = px.pie(
        payment_df,
        names="Payment Type",
        values="Orders",
        hole=.45,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("📦 Order Status")

    status = (
        master["order_status"]
        .value_counts()
        .reset_index()
    )

    status.columns=["Status","Orders"]

    fig = px.bar(
        status,
        x="Status",
        y="Orders",
        color="Status",
        text_auto=True
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# ROW 2
# =====================================================

left,right = st.columns(2)

with left:

    st.subheader("👥 Customer Segments")

    seg = (
        segment["CustomerSegment"]
        .value_counts()
        .reset_index()
    )

    seg.columns=["Segment","Customers"]

    fig = px.bar(
        seg,
        x="Segment",
        y="Customers",
        color="Segment",
        text_auto=True
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("⭐ Review Score")

    review_df = (
        master["review_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    review_df.columns=["Score","Customers"]

    fig = px.bar(
        review_df,
        x="Score",
        y="Customers",
        color="Score",
        text_auto=True
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# ROW 3
# =====================================================

left,right = st.columns(2)

with left:

    st.subheader("🏆 Top Product Categories")

    cat = (
        master["product_category_name"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
        .reset_index()
    )

    cat.columns=["Category","Orders"]

    fig = px.bar(
        cat,
        x="Orders",
        y="Category",
        orientation="h",
        color="Orders",
        text_auto=True
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🌍 Top Customer States")

    state_df = (
        master["customer_state"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    state_df.columns=["State","Customers"]

    fig = px.bar(
        state_df,
        x="State",
        y="Customers",
        color="Customers",
        text_auto=True
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# MONTHLY SALES TREND
# =====================================================

st.subheader("📈 Monthly Sales Trend")

master["order_purchase_timestamp"] = pd.to_datetime(
    master["order_purchase_timestamp"],
    errors="coerce"
)

monthly = (
    master
    .groupby(master["order_purchase_timestamp"].dt.to_period("M"))["payment_value"]
    .sum()
    .reset_index()
)

monthly["order_purchase_timestamp"] = monthly["order_purchase_timestamp"].astype(str)

fig = px.line(
    monthly,
    x="order_purchase_timestamp",
    y="payment_value",
    markers=True,
    title="Monthly Revenue"
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# REVENUE BY STATE
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("💰 Revenue by State")

    revenue_state = (
        master.groupby("customer_state")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        revenue_state,
        x="customer_state",
        y="payment_value",
        color="payment_value",
        text_auto=".2s"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("🚚 Delivery Days")
    # Create delivery_days if not present
if "delivery_days" not in master.columns:

    master["order_purchase_timestamp"] = pd.to_datetime(
        master["order_purchase_timestamp"],
        errors="coerce"
    )

    master["order_delivered_customer_date"] = pd.to_datetime(
        master["order_delivered_customer_date"],
        errors="coerce"
    )

    master["delivery_days"] = (
        master["order_delivered_customer_date"]
        - master["order_purchase_timestamp"]
    ).dt.days

    delivery = master["delivery_days"].dropna()

    fig = px.histogram(
        delivery,
        nbins=30,
        title="Delivery Time Distribution"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# PAYMENT vs REVIEW
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("⭐ Review Score vs Revenue")

    review_rev = (
        master.groupby("review_score")["payment_value"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        review_rev,
        x="review_score",
        y="payment_value",
        color="payment_value",
        text_auto=".2f"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("💳 Payment Installments")

    install = (
        master["payment_installments"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    install.columns = ["Installments", "Orders"]

    fig = px.bar(
        install,
        x="Installments",
        y="Orders",
        color="Orders",
        text_auto=True
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# CUSTOMER DATA
# =====================================================

st.subheader("📋 Customer Dataset Preview")

st.dataframe(
    master.head(50),
    use_container_width=True
)

st.divider()

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.header("🧠 AI Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### 📈 Key Insights

✅ Total Revenue : **R$ {revenue:,.2f}**

✅ Total Customers : **{customers:,}**

✅ Total Orders : **{orders:,}**

✅ Average Review : **{review} ⭐**
""")

with col2:

    top_state = master["customer_state"].mode()[0]
    top_payment = master["payment_type"].mode()[0]
    top_category = master["product_category_name"].fillna("Unknown").mode()[0]

    st.info(f"""
### 💡 Business Recommendations

⭐ Focus marketing in **{top_state}**

💳 Most customers prefer **{top_payment}**

📦 Best Selling Category:
**{top_category}**

🚀 Increase loyalty rewards for repeat customers.

🎯 Launch personalized campaigns for At Risk customers.
""")

st.divider()

# =====================================================
# DOWNLOAD SECTION
# =====================================================

st.header("📥 Download Reports")

col1, col2 = st.columns(2)

with col1:

    csv = master.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Master Dataset",
        csv,
        "master_dataset.csv",
        "text/csv"
    )

with col2:

    seg_csv = segment.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Customer Segments",
        seg_csv,
        "customer_segments.csv",
        "text/csv"
    )

st.divider()

# =====================================================
# PROJECT SUMMARY
# =====================================================

st.header("📊 Project Summary")

summary = pd.DataFrame({

"Metric":[

"Customers",

"Orders",

"Products",

"Revenue",

"Review Score"

],

"Value":[

customers,

orders,

products,

f"R$ {revenue:,.2f}",

review

]

})

st.table(summary)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
---
### 🚀 Customer Insights & Recommendation System

**Technologies Used**

- Python
- Pandas
- Plotly
- Streamlit
- Scikit-Learn
- Machine Learning
- Data Analytics

Built as an End-to-End Data Analytics Project.

Made for ReadyNest Internship 🚀
"""
)

# =====================================================
# ADVANCED ANALYTICS
# =====================================================

st.header("📈 Advanced Business Analytics")

col1, col2 = st.columns(2)

# Revenue by Month
with col1:

    monthly_sales = (
        master.groupby(
            master["order_purchase_timestamp"].dt.to_period("M")
        )["payment_value"]
        .sum()
        .reset_index()
    )

    monthly_sales["order_purchase_timestamp"] = (
        monthly_sales["order_purchase_timestamp"]
        .astype(str)
    )

    fig = px.area(
        monthly_sales,
        x="order_purchase_timestamp",
        y="payment_value",
        title="Monthly Revenue Growth"
    )

    st.plotly_chart(fig, use_container_width=True)

# Average Order Value

with col2:

    avg_order = (
        master.groupby("customer_state")["payment_value"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        avg_order,
        x="customer_state",
        y="payment_value",
        color="payment_value",
        title="Average Order Value"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# CUSTOMER INSIGHTS
# =====================================================

st.header("👥 Customer Insights")

left,right = st.columns(2)

with left:

    segment_chart = (
        segment.groupby("CustomerSegment")
        .size()
        .reset_index(name="Customers")
    )

    fig = px.treemap(
        segment_chart,
        path=["CustomerSegment"],
        values="Customers",
        color="Customers"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    state_chart = (
        master.groupby("customer_state")
        .size()
        .reset_index(name="Orders")
    )

    fig = px.scatter(
        state_chart,
        x="customer_state",
        y="Orders",
        size="Orders",
        color="Orders"
    )

    st.plotly_chart(fig,use_container_width=True)

st.divider()

st.header("🤖 Smart Recommendation Engine")

recommendations = {
    "Premium": [
        "VIP Membership",
        "Exclusive Discounts",
        "Early Product Access",
        "Premium Support"
    ],
    "Loyal": [
        "Reward Points",
        "Cross-selling",
        "Referral Bonus"
    ],
    "Regular": [
        "Bundle Offers",
        "Festival Discounts",
        "Email Marketing"
    ],
    "At Risk": [
        "Win-back Campaign",
        "High Discount Coupon",
        "Free Shipping"
    ]
}

for seg_name, recs in recommendations.items():
    with st.expander(f"📌 {seg_name} Customers"):
        for r in recs:
            st.write("✅", r)

            st.markdown("---")

st.markdown("""
## 📌 Project Information

**Project Name**
Customer Insights & Recommendation System

**Tech Stack**

- Python
- Pandas
- Plotly
- Streamlit
- Scikit-Learn
- Machine Learning

**Developed for ReadyNest Internship**

⭐ Resume Ready Portfolio Project
""")



