"""
load_to_sqlite.py

Builds bluestock_mf.db from sql/schema.sql and loads all cleaned
datasets into the star schema (dim_fund, dim_date, fact_nav,
fact_transactions, fact_performance, fact_aum).

Run from the project root:
    python scripts/load_to_sqlite.py
"""

import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

PROCESSED_DIR = "data/processed"
DB_PATH = "bluestock_mf.db"
SCHEMA_PATH = "sql/schema.sql"


def build_schema() -> None:
    """Drop any existing db and create fresh tables from schema.sql."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(open(SCHEMA_PATH).read())
    conn.close()


def load_data(engine) -> None:
    """Load all cleaned CSVs into their corresponding tables."""
    fund_master = pd.read_csv(f"{PROCESSED_DIR}/01_fund_master.csv")
    fund_master = fund_master.drop(columns=["expense_ratio_pct"], errors="ignore")
    fund_master.to_sql("dim_fund", engine, if_exists="append", index=False)
    print("dim_fund:", len(fund_master))

    nav = pd.read_csv(f"{PROCESSED_DIR}/02_nav_history.csv")
    nav.to_sql("fact_nav", engine, if_exists="append", index=False)
    print("fact_nav:", len(nav))

    tx = pd.read_csv(f"{PROCESSED_DIR}/08_investor_transactions.csv")
    tx = tx.rename(columns={"transaction_date": "date"})
    tx.to_sql("fact_transactions", engine, if_exists="append", index=False)
    print("fact_transactions:", len(tx))

    perf = pd.read_csv(f"{PROCESSED_DIR}/07_scheme_performance.csv")
    perf = perf.drop(columns=["scheme_name", "fund_house", "category", "plan"], errors="ignore")
    perf.to_sql("fact_performance", engine, if_exists="append", index=False)
    print("fact_performance:", len(perf))

    aum = pd.read_csv(f"{PROCESSED_DIR}/03_aum_by_fund_house.csv")
    aum.to_sql("fact_aum", engine, if_exists="append", index=False)
    print("fact_aum:", len(aum))

    dim_date = build_dim_date(nav, tx, aum)
    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
    print("dim_date:", len(dim_date))


def build_dim_date(nav: pd.DataFrame, tx: pd.DataFrame, aum: pd.DataFrame) -> pd.DataFrame:
    """Build a calendar dimension from every date used across the fact tables."""
    dates = pd.concat([
        pd.to_datetime(nav["date"]),
        pd.to_datetime(tx["date"]),
        pd.to_datetime(aum["date"]),
    ]).drop_duplicates().sort_values()

    dim_date = pd.DataFrame({"date": dates})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["weekday"] = dim_date["date"].dt.day_name()
    dim_date["date"] = dim_date["date"].dt.strftime("%Y-%m-%d")

    return dim_date


def main() -> None:
    """Build the schema and load all data into bluestock_mf.db."""
    build_schema()
    engine = create_engine(f"sqlite:///{DB_PATH}")
    load_data(engine)
    print("Done - bluestock_mf.db ready")


if __name__ == "__main__":
    main()
