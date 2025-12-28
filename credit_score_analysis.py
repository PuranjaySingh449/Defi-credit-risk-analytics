import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# PATHS
# ===============================
CREDIT_SCORES_PATH = r"D:\blockchain\borrower_credit_scores.csv"
BORROWS_PATH = r"D:\blockchain\borrows_full.csv"
OUTPUT_PATH = r"D:\blockchain\borrower_credit_scores_with_risk.csv"

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv(CREDIT_SCORES_PATH)
borrows = pd.read_csv(BORROWS_PATH)

print("✅ Data loaded")
print("Borrowers:", len(df))

# ===============================
# OPTION A — RISK TIERING
# ===============================
low_cutoff = df["credit_score"].quantile(0.30)
high_cutoff = df["credit_score"].quantile(0.70)

def assign_risk(score):
    if score <= low_cutoff:
        return "High Risk"
    elif score <= high_cutoff:
        return "Medium Risk"
    else:
        return "Low Risk"

df["risk_tier"] = df["credit_score"].apply(assign_risk)

print("\n📊 Risk tier distribution:")
print(df["risk_tier"].value_counts())

# ===============================
# OPTION B — SCORE DISTRIBUTION
# ===============================
print("\n📈 Credit score statistics:")
print(df["credit_score"].describe())

print("\n📌 Credit score percentiles:")
print(df["credit_score"].quantile([0.1, 0.3, 0.5, 0.7, 0.9]))

# Histogram (paper-ready)
plt.figure()
plt.hist(df["credit_score"], bins=30)
plt.xlabel("Credit Score")
plt.ylabel("Number of Borrowers")
plt.title("Distribution of DeFi Credit Scores")
plt.tight_layout()
plt.show()

# ===============================
# OPTION C — BEHAVIORAL VALIDATION
# ===============================

# Aggregate borrow behavior
borrow_agg = borrows.groupby("account_id").agg(
    total_borrows_usd=("amountUSD", "sum"),
    borrow_count=("id", "count")
).reset_index()

# Merge with scores
full = df.merge(borrow_agg, on="account_id", how="left").fillna(0)

validation = full.groupby("risk_tier").agg(
    avg_credit_score=("credit_score", "mean"),
    avg_total_borrowed_usd=("total_borrows_usd", "mean"),
    avg_borrow_count=("borrow_count", "mean"),
    users=("account_id", "count")
)

print("\n🧠 Behavioral validation by risk tier:")
print(validation)

# ===============================
# SAVE FINAL OUTPUT
# ===============================
df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ Final file saved:")
print(OUTPUT_PATH)
