"""
fund_master_exploration.py

Explores the fund master dataset (unique fund houses, categories,
sub-categories, risk levels) and validates that every AMFI code in
fund_master has matching data in nav_history, and vice versa.
Prints a short data quality summary.

Run from the project root:
    python scripts/fund_master_exploration.py
"""

import pandas as pd
import os

RAW_DATA_DIR = os.path.join("data", "raw")


def explore_fund_master(fund_master: pd.DataFrame) -> None:
    """Print unique fund houses, categories, sub-categories, and risk levels."""
    print("Unique Fund Houses:", fund_master["fund_house"].unique())
    print("Unique Categories:", fund_master["category"].unique())
    print("Unique Sub-Categories:", fund_master["sub_category"].unique())
    print("Unique Risk Categories:", fund_master["risk_category"].unique())
    print("\nAMFI code range:", fund_master["amfi_code"].min(), "-", fund_master["amfi_code"].max())
    print("All amfi_codes unique:", fund_master["amfi_code"].is_unique)


def validate_amfi_codes(fund_master: pd.DataFrame, nav_history: pd.DataFrame) -> tuple:
    """Cross-check AMFI codes between fund_master and nav_history."""
    master_codes = set(fund_master["amfi_code"].unique())
    nav_codes = set(nav_history["amfi_code"].unique())

    missing_in_nav = master_codes - nav_codes
    missing_in_master = nav_codes - master_codes

    print("Codes in fund_master with no nav_history:", len(missing_in_nav))
    print("Codes in nav_history with no fund_master entry:", len(missing_in_master))

    return missing_in_nav, missing_in_master


def main() -> None:
    """Run fund master exploration and AMFI code validation."""
    fund_master = pd.read_csv(os.path.join(RAW_DATA_DIR, "01_fund_master.csv"))
    nav_history = pd.read_csv(os.path.join(RAW_DATA_DIR, "02_nav_history.csv"))

    print("=" * 60)
    print("FUND MASTER EXPLORATION")
    print("=" * 60)
    explore_fund_master(fund_master)

    print("\n" + "=" * 60)
    print("AMFI CODE VALIDATION")
    print("=" * 60)
    missing_in_nav, missing_in_master = validate_amfi_codes(fund_master, nav_history)

    print("\n" + "=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)
    print(f"""
- fund_master.csv: {len(fund_master)} funds, {fund_master['fund_house'].nunique()} fund houses,
  {fund_master['category'].nunique()} categories, {fund_master['sub_category'].nunique()} sub-categories.
- nav_history.csv: {len(nav_history)} NAV records across {nav_history['amfi_code'].nunique()} schemes.
- AMFI cross-check: {len(missing_in_nav)} unmatched fund_master codes,
  {len(missing_in_master)} unmatched nav_history codes.
""")


if __name__ == "__main__":
    main()
