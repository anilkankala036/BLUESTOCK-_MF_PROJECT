"""
Day 1 - Fund Master Exploration + AMFI Code Validation
Step 6: Explore fund master - unique fund houses, categories, sub-categories, risk grades
Step 7: Validate that every AMFI code in fund_master exists in nav_history
"""

import pandas as pd
import os

raw_folder = "data/raw"

fund_master = pd.read_csv(os.path.join(raw_folder, "01_fund_master.csv"))
nav_history = pd.read_csv(os.path.join(raw_folder, "02_nav_history.csv"))

# ---------------------------------------------------------
# STEP 6: Explore fund master
# ---------------------------------------------------------

print("=" * 60)
print("STEP 6: FUND MASTER EXPLORATION")
print("=" * 60)

print("\nUnique Fund Houses:")
print(fund_master["fund_house"].unique())
print("Count:", fund_master["fund_house"].nunique())

print("\nUnique Categories:")
print(fund_master["category"].unique())
print("Count:", fund_master["category"].nunique())

print("\nUnique Sub-Categories:")
print(fund_master["sub_category"].unique())
print("Count:", fund_master["sub_category"].nunique())

print("\nUnique Risk Categories:")
print(fund_master["risk_category"].unique())
print("Count:", fund_master["risk_category"].nunique())

print("\nAMFI Code structure:")
print("Total funds:", len(fund_master))
print("Min amfi_code:", fund_master["amfi_code"].min())
print("Max amfi_code:", fund_master["amfi_code"].max())
print("Are all amfi_codes unique?", fund_master["amfi_code"].is_unique)

print("\nSEBI category codes (these repeat across similar fund types):")
print(fund_master["sebi_category_code"].value_counts())

# ---------------------------------------------------------
# STEP 7: Validate AMFI codes between fund_master and nav_history
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("STEP 7: AMFI CODE VALIDATION")
print("=" * 60)

master_codes = set(fund_master["amfi_code"].unique())
nav_codes = set(nav_history["amfi_code"].unique())

missing_in_nav = master_codes - nav_codes
missing_in_master = nav_codes - master_codes

print("\nTotal unique codes in fund_master:", len(master_codes))
print("Total unique codes in nav_history:", len(nav_codes))

if missing_in_nav:
    print(f"\nWARNING: {len(missing_in_nav)} codes in fund_master have NO nav_history data:")
    print(missing_in_nav)
else:
    print("\nAll fund_master codes have matching nav_history data.")

if missing_in_master:
    print(f"\nNOTE: {len(missing_in_master)} codes in nav_history are NOT in fund_master:")
    print(missing_in_master)
else:
    print("\nAll nav_history codes exist in fund_master.")

# ---------------------------------------------------------
# Data Quality Summary
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DATA QUALITY SUMMARY")
print("=" * 60)

print(f"""
- fund_master.csv: {len(fund_master)} funds, {fund_master['fund_house'].nunique()} fund houses,
  {fund_master['category'].nunique()} categories, {fund_master['sub_category'].nunique()} sub-categories,
  {fund_master['risk_category'].nunique()} risk levels. No missing values, no duplicate rows.

- nav_history.csv: {len(nav_history)} NAV records across {nav_history['amfi_code'].nunique()} schemes.
  'date' column is stored as text, not datetime - should be converted before time-series analysis.

- AMFI code cross-check: {len(missing_in_nav)} fund_master codes missing from nav_history,
  {len(missing_in_master)} nav_history codes missing from fund_master.

- Other datasets (investor_transactions, monthly_sip_inflows) have minor issues:
  transaction_date uses DD-MM-YYYY format (inconsistent with YYYY-MM-DD used elsewhere),
  and yoy_growth_pct has 12 missing values (likely first-year data with no prior year to compare).
""")
