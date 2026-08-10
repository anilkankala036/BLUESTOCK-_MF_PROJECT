import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

processed_folder = "data/processed"
db_path = "bluestock_mf.db"
schema_path = "sql/schema.sql"

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
conn.executescript(open(schema_path).read())
conn.close()

engine = create_engine(f"sqlite:///{db_path}")

fund_master = pd.read_csv(processed_folder + "/01_fund_master.csv")
fund_master = fund_master.drop(columns=["expense_ratio_pct"], errors="ignore")
fund_master.to_sql("dim_fund", engine, if_exists="append", index=False)
print("dim_fund:", len(fund_master))

nav = pd.read_csv(processed_folder + "/02_nav_history.csv")
nav.to_sql("fact_nav", engine, if_exists="append", index=False)
print("fact_nav:", len(nav))

tx = pd.read_csv(processed_folder + "/08_investor_transactions.csv")
tx = tx.rename(columns={"transaction_date": "date"})
tx.to_sql("fact_transactions", engine, if_exists="append", index=False)
print("fact_transactions:", len(tx))

perf = pd.read_csv(processed_folder + "/07_scheme_performance.csv")
perf = perf.drop(columns=["scheme_name", "fund_house", "category", "plan"], errors="ignore")
perf.to_sql("fact_performance", engine, if_exists="append", index=False)
print("fact_performance:", len(perf))

aum = pd.read_csv(processed_folder + "/03_aum_by_fund_house.csv")
aum.to_sql("fact_aum", engine, if_exists="append", index=False)
print("fact_aum:", len(aum))

# calendar table - just grab every date used anywhere
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
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
print("dim_date:", len(dim_date))

print("done - bluestock_mf.db ready")
