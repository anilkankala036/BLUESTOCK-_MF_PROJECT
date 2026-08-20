# Bluestock MF Capstone Project

Mutual fund data analysis project — ETL pipeline, NAV tracking, exploratory analysis, and Power BI dashboard covering 40 Indian mutual fund schemes across 10 fund houses (2022-2025).

## Overview

This project ingests raw mutual fund data (fund details, NAV history, investor transactions, performance metrics, AUM, SIP inflows, etc.), cleans it, loads it into a SQLite star schema, runs exploratory analysis with charts, and presents the results in an interactive Power BI dashboard.

## Project Structure

```
bluestock1/
├── data/
│   ├── raw/              # original 10 CSVs
│   └── processed/        # cleaned CSVs (output of clean_data.py)
├── scripts/
│   ├── data_ingestion.py       # Day 1 - load & inspect raw CSVs
│   ├── live_nav_fetch.py       # Day 1 - fetch live NAV from mfapi.in
│   ├── fund_master_exploration.py  # Day 1 - fund master + AMFI validation
│   ├── clean_data.py           # Day 2 - clean nav_history, transactions, performance
│   ├── load_to_sqlite.py       # Day 2 - build bluestock_mf.db
│   └── run_pipeline.py         # runs the full pipeline end to end
├── sql/
│   ├── schema.sql        # star schema CREATE TABLE statements
│   └── queries.sql       # 10 analytical queries
├── notebooks/
│   └── EDA_Analysis.ipynb      # Day 3 - 10 charts, key findings
├── reports/
│   └── charts/            # exported PNG charts
├── dashboard/
│   └── bluestock_mf_dashboard.pbix  # Day 4 - Power BI dashboard
├── bluestock_mf.db         # SQLite database (built by load_to_sqlite.py)
├── requirements.txt
└── data_dictionary.md      # column-level documentation for all datasets
```

## Setup

1. Clone the repo:
```
git clone https://github.com/anilkankala036/BLUESTOCK-_MF_PROJECT.git
cd BLUESTOCK-_MF_PROJECT
```

2. Install Python dependencies:
```
pip install -r requirements.txt
```

3. Make sure the 10 raw CSVs are in `data/raw/` (see `data_dictionary.md` for what each one contains).

## Running the ETL Pipeline

Run everything end to end with one command:
```
python scripts/run_pipeline.py
```

This runs, in order:
1. `data_ingestion.py` — loads and inspects the 10 raw CSVs
2. `live_nav_fetch.py` — fetches live NAV data from mfapi.in
3. `fund_master_exploration.py` — explores fund master, validates AMFI codes
4. `clean_data.py` — cleans nav_history, investor_transactions, scheme_performance; copies the rest to `data/processed/`
5. `load_to_sqlite.py` — builds `bluestock_mf.db` from the schema and loads all cleaned data

Or run any step individually, e.g.:
```
python scripts/clean_data.py
```

## Exploring the Data

Open the EDA notebook:
```
jupyter notebook notebooks/EDA_Analysis.ipynb
```
Run all cells top to bottom. Charts are saved to `reports/charts/`.

To query the database directly:
```
sqlite3 bluestock_mf.db
```
or open it in [DB Browser for SQLite](https://sqlitebrowser.org/), and run the queries in `sql/queries.sql`.

## Opening the Dashboard

Open `dashboard/bluestock_mf_dashboard.pbix` in [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free). It has 4 pages:
1. **Industry Overview** — KPIs, AUM trend, AUM by AMC
2. **Fund Performance** — return vs risk scatter, fund scorecard, NAV vs benchmark
3. **Investor Analytics** — transactions by state, SIP/Lumpsum/Redemption split, demographics
4. **SIP & Market Trends** — SIP inflow vs NIFTY50, category inflow heatmap, top categories by inflow

## Dataset Descriptions

See `data_dictionary.md` for full column-level documentation of all 10 datasets and the SQLite star schema.

Quick summary:
- **01_fund_master.csv** — one row per fund (40 funds, 10 fund houses)
- **02_nav_history.csv** — daily NAV per fund, 2022-2025
- **03_aum_by_fund_house.csv** — AUM tracked per fund house over time
- **04_monthly_sip_inflows.csv** — industry-wide SIP inflow trends
- **05_category_inflows.csv** — net inflows by fund category
- **06_industry_folio_count.csv** — investor folio counts
- **07_scheme_performance.csv** — returns, risk metrics per fund
- **08_investor_transactions.csv** — individual investor transactions
- **09_portfolio_holdings.csv** — stock-level holdings per fund
- **10_benchmark_indices.csv** — daily closing values for benchmark indices (NIFTY50, etc.)

## Tech Stack

Python (pandas, numpy, matplotlib, seaborn, plotly), SQLite + SQLAlchemy, Jupyter, Power BI

## Author

Anil Kankala
