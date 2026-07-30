"""
Day 1 - Data Ingestion Script
Loads all 10 provided CSV datasets, prints shape/dtypes/head, and checks for anomalies.
"""

import pandas as pd
import os

raw_folder = "data/raw"

files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

for file in files:
    path = os.path.join(raw_folder, file)

    if not os.path.isfile(path):
        print(f"\n{file} not found, skipping")
        continue

    df = pd.read_csv(path)

    print("\n" + "=" * 60)
    print("FILE:", file)
    print("=" * 60)

    print("\nShape:", df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nHead:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())

    # check date columns that are still stored as text
    for col in df.columns:
        if "date" in col.lower() and df[col].dtype == "object":
            print(f"Note: '{col}' looks like a date but is stored as text")

    # check code columns for duplicates
    for col in df.columns:
        if "code" in col.lower():
            if df[col].nunique() != len(df):
                print(f"Note: '{col}' has repeated values")

print("\nDone loading all files")
