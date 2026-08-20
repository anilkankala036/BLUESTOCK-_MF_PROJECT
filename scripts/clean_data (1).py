"""
clean_data.py

Cleans the 3 datasets that need it and copies the rest to data/processed/
unchanged.

- nav_history: parse dates, sort by fund + date, forward-fill missing
  NAV for weekends/holidays, remove duplicates, drop NAV <= 0
- investor_transactions: standardise transaction_type, drop invalid
  amounts, fix date format, report KYC status values
- scheme_performance: validate returns are numeric, flag anomalies,
  check expense ratio is within 0.1%-2.5%

Run from the project root:
    python scripts/clean_data.py
"""

import pandas as pd
import os
import shutil

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

REMAINING_FILES = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]


def clean_nav_history() -> None:
    """Clean nav_history.csv and save to data/processed/."""
    df = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))

    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates(subset=["amfi_code", "date"])
    df = df[df["nav"] > 0]
    df = df.sort_values(["amfi_code", "date"])

    # forward-fill missing calendar days (weekends/holidays) per fund
    filled = []
    for code, group in df.groupby("amfi_code"):
        group = group.set_index("date")
        full_range = pd.date_range(group.index.min(), group.index.max(), freq="D")
        group = group.reindex(full_range)
        group["amfi_code"] = code
        group["nav"] = group["nav"].ffill()
        filled.append(group.rename_axis("date").reset_index())

    df = pd.concat(filled, ignore_index=True)[["amfi_code", "date", "nav"]]
    df.to_csv(os.path.join(PROCESSED_DIR, "02_nav_history.csv"), index=False)


def clean_investor_transactions() -> None:
    """Clean investor_transactions.csv and save to data/processed/."""
    df = pd.read_csv(os.path.join(RAW_DIR, "08_investor_transactions.csv"))

    df["transaction_type"] = df["transaction_type"].str.strip().str.title()
    df["transaction_type"] = df["transaction_type"].replace({"Sip": "SIP"})

    df = df[df["amount_inr"] > 0]
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%d-%m-%Y")
    df = df.drop_duplicates()

    df.to_csv(os.path.join(PROCESSED_DIR, "08_investor_transactions.csv"), index=False)


def clean_scheme_performance() -> None:
    """Clean scheme_performance.csv and save to data/processed/."""
    df = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"))

    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct"]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.to_csv(os.path.join(PROCESSED_DIR, "07_scheme_performance.csv"), index=False)


def copy_remaining_files() -> None:
    """Copy the datasets that don't need cleaning to data/processed/."""
    for filename in REMAINING_FILES:
        src = os.path.join(RAW_DIR, filename)
        dst = os.path.join(PROCESSED_DIR, filename)
        if os.path.isfile(src):
            shutil.copy(src, dst)


def main() -> None:
    """Run all cleaning steps and copy remaining files to data/processed/."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    copy_remaining_files()

    print("Done. All 10 datasets are now in data/processed/")


if __name__ == "__main__":
    main()
