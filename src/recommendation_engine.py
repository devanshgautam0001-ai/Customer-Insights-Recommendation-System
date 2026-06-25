import pandas as pd
import os

print("=" * 60)
print("RECOMMENDATION ENGINE STARTED")
print("=" * 60)

# Create reports folder
os.makedirs("reports", exist_ok=True)

# Load customer segments
df = pd.read_csv("reports/customer_segments.csv")

print("\nCustomer Segments Loaded Successfully!")
print(df.head())

recommendations = []

for segment in df["CustomerSegment"].unique():

    if segment == "Premium":
        rec = """
==========================
PREMIUM CUSTOMERS
==========================
• Offer VIP Membership
• Early Access to New Products
• Premium Customer Support
• Exclusive Discounts
• Personalized Recommendations
"""

    elif segment == "Loyal":
        rec = """
==========================
LOYAL CUSTOMERS
==========================
• Reward Loyalty Points
• Cross Sell Related Products
• Referral Bonus
• Exclusive Coupons
• Encourage Product Reviews
"""

    elif segment == "Regular":
        rec = """
==========================
REGULAR CUSTOMERS
==========================
• Bundle Offers
• Email Marketing Campaigns
• Festival Discounts
• Personalized Product Suggestions
"""

    elif segment == "At Risk":
        rec = """
==========================
AT RISK CUSTOMERS
==========================
• Win-back Campaign
• High Discount Coupons
• Personalized Emails
• Free Shipping
• Customer Feedback Survey
"""

    recommendations.append(rec)

# Remove duplicates
recommendations = list(dict.fromkeys(recommendations))

# Save report
with open("reports/recommendations.txt", "w", encoding="utf-8") as f:

    f.write("CUSTOMER RECOMMENDATION REPORT\n")
    f.write("=" * 60 + "\n\n")

    for rec in recommendations:
        f.write(rec)
        f.write("\n")

print("\nRecommendations Generated Successfully!\n")

for rec in recommendations:
    print(rec)

print("=" * 60)
print("Recommendation Report Saved")
print("Location : reports/recommendations.txt")
print("=" * 60)