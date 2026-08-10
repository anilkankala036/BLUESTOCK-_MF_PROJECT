import pandas as pd
import os
import shutil

raw_folder = "data/raw"
processed_folder = "data/processed"

os.makedirs(processed_folder, exist_ok=True)

# ---- nav history ----
print("cleaning nav_history...")
df = pd.read_csv(os.path.join(raw_folder, "02_nav_history.csv"))
before = len(df)

df["date"] = pd.to_datetime(df["date"])
df = df.drop_duplicates(subset=["amfi_code", "date"])

bad_nav = df[df["nav"] <= 0]
if len(bad_nav) > 0:
    print("dropping", len(bad_nav), "rows with nav <= 0")
df = df[df["nav"] > 0]

df = df.sort_values(["amfi_code", "date"])

# fill missing days per fund (weekends/holidays) using last known nav
filled = []
for code, group in df.groupby("amfi_code"):
    group = group.set_index("date")
    full_range = pd.date_range(group.index.min(), group.index.max(), freq="D")
    group = group.reindex(full_range)
    group["amfi_code"] = code
    group["nav"] = group["nav"].ffill()
    group = group.rename_axis("date").reset_index()
    filled.append(group)

df = pd.concat(filled, ignore_index=True)
df = df[["amfi_code", "date", "nav"]]
df.to_csv(os.path.join(processed_folder, "02_nav_history.csv"), index=False)
print("nav_history:", before, "->", len(df), "rows after filling gaps\n")


# ---- investor transactions ----
print("cleaning investor_transactions...")
df2 = pd.read_csv(os.path.join(raw_folder, "08_investor_transactions.csv"))
before2 = len(df2)

df2["transaction_type"] = df2["transaction_type"].str.strip().str.title()
df2["transaction_type"] = df2["transaction_type"].replace({"Sip": "SIP"})

weird_types = set(df2["transaction_type"].unique()) - {"SIP", "Lumpsum", "Redemption"}
if weird_types:
    print("hmm found unexpected transaction types:", weird_types)

bad_amt = df2[df2["amount_inr"] <= 0]
if len(bad_amt) > 0:
    print("dropping", len(bad_amt), "rows with amount <= 0")
df2 = df2[df2["amount_inr"] > 0]

df2["transaction_date"] = pd.to_datetime(df2["transaction_date"], format="%d-%m-%Y")

print("kyc status values:", df2["kyc_status"].unique())

df2 = df2.drop_duplicates()
df2.to_csv(os.path.join(processed_folder, "08_investor_transactions.csv"), index=False)
print("investor_transactions:", before2, "->", len(df2), "rows\n")


# ---- scheme performance ----
print("cleaning scheme_performance...")
df3 = pd.read_csv(os.path.join(raw_folder, "07_scheme_performance.csv"))

return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct"]
for col in return_cols:
    not_numeric = pd.to_numeric(df3[col], errors="coerce").isna() & df3[col].notna()
    if not_numeric.any():
        print("non-numeric values in", col)
    df3[col] = pd.to_numeric(df3[col], errors="coerce")

    weird = df3[(df3[col] < -100) | (df3[col] > 200)]
    if len(weird) > 0:
        print(len(weird), "anomalous values in", col)

out_range = df3[(df3["expense_ratio_pct"] < 0.1) | (df3["expense_ratio_pct"] > 2.5)]
if len(out_range) > 0:
    print(len(out_range), "funds have expense ratio outside 0.1-2.5% range")
    print(out_range[["amfi_code", "scheme_name", "expense_ratio_pct"]])
else:
    print("expense ratios all look fine")

df3.to_csv(os.path.join(processed_folder, "07_scheme_performance.csv"), index=False)


# ---- rest of the files, just copy as is ----
print("\ncopying the rest of the files over...")
remaining = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]
for f in remaining:
    src = os.path.join(raw_folder, f)
    dst = os.path.join(processed_folder, f)
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        print(f, "missing from raw folder")

print("done, check data/processed/")
