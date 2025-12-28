import pandas as pd
import numpy as np

# Load raw data
borrows = pd.read_csv(r"D:\blockchain\borrows_full.csv")
repays = pd.read_csv(r"D:\blockchain\repays_full.csv")

# Ensure timestamps are ints
borrows["timestamp"] = borrows["timestamp"].astype(int)
repays["timestamp"] = repays["timestamp"].astype(int)

# -------------------------------
# Borrower-level aggregation
# -------------------------------
borrow_agg = borrows.groupby("account_id").agg(
    total_borrows_usd=("amountUSD", "sum"),
    borrow_count=("id", "count"),
    first_borrow_ts=("timestamp", "min"),
    last_borrow_ts=("timestamp", "max"),
).reset_index()

repay_agg = repays.groupby("account_id").agg(
    total_repays_usd=("amountUSD", "sum"),
    repay_count=("id", "count"),
).reset_index()

df = borrow_agg.merge(repay_agg, on="account_id", how="left").fillna(0)

# -------------------------------
# Feature engineering
# -------------------------------
df["repayment_ratio"] = df["total_repays_usd"] / df["total_borrows_usd"]
df["active_days"] = (df["last_borrow_ts"] - df["first_borrow_ts"]) / 86400
df["borrow_frequency"] = df["borrow_count"] / df["active_days"].replace(0, 1)

# Clip extremes
df["repayment_ratio"] = df["repayment_ratio"].clip(0, 1.2)
df["borrow_frequency"] = df["borrow_frequency"].clip(
    0, df["borrow_frequency"].quantile(0.99)
)

# -------------------------------
# Credit score (0–100)
# -------------------------------
def minmax(series):
    return (series - series.min()) / (series.max() - series.min())

df["repayment_norm"] = minmax(df["repayment_ratio"])
df["frequency_norm"] = 1 - minmax(df["borrow_frequency"])  # lower = safer
df["experience_norm"] = minmax(df["active_days"])

df["credit_score"] = (
    0.5 * df["repayment_norm"] +
    0.3 * df["frequency_norm"] +
    0.2 * df["experience_norm"]
) * 100

df["credit_score"] = df["credit_score"].round(2)

# -------------------------------
# Save output
# -------------------------------
OUTPUT_PATH = r"D:\blockchain\borrower_credit_scores.csv"
df[["account_id", "credit_score"]].to_csv(OUTPUT_PATH, index=False)

print("✅ Credit scores computed")
print("Saved to:", OUTPUT_PATH)
