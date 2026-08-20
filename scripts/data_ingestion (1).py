"""
data_ingestion.py

Loads the 10 raw mutual fund datasets and prints shape, dtypes, and head
for each, plus basic anomaly checks (missing values, duplicates, date
columns stored as text, duplicate codes, empty columns).

Run from the project root:
    python scripts/data_ingestion.py
"""

import pandas as pd
import os

RAW_DATA_DIR = os.path.join("data", "raw")

DATASET_FILES = [
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


def inspect_dataframe(name: str, df: pd.DataFrame) -> None:
    """Print shape, dtypes, head, and anomaly checks for a single dataframe."""
    print(f"\n{'=' * 60}\nFILE: {name}\n{'=' * 60}")
    print("\nShape:", df.shape)
    print("\nData Types:")
    print(df.dtypes)
    print("\nHead:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())

    for col in df.columns:
        if "date" in col.lower() and df[col].dtype == "object":
            print(f"Note: '{col}' looks like a date but is stored as text")

    for col in df.columns:
        if "code" in col.lower() and df[col].nunique() != len(df):
            print(f"Note: '{col}' has repeated values")


def main() -> None:
    """Load and inspect all 10 raw datasets."""
    if not os.path.isdir(RAW_DATA_DIR):
        print(f"ERROR: '{RAW_DATA_DIR}' not found. Run this from the project root.")
        return

    for filename in DATASET_FILES:
        path = os.path.join(RAW_DATA_DIR, filename)
        if not os.path.isfile(path):
            print(f"\n{filename} not found, skipping")
            continue
        df = pd.read_csv(path)
        inspect_dataframe(filename, df)

    print("\nDone loading all files")


if __name__ == "__main__":
    main()
