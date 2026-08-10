# Data Dictionary — Bluestock MF Project

Documents all source datasets and the SQLite star schema built from them.

---

## Source Datasets (data/raw/, cleaned versions in data/processed/)

### 01_fund_master.csv
One row per mutual fund scheme.

| Column | Type | Description |
|---|---|---|
| amfi_code | int | Unique AMFI scheme code, primary identifier for a fund |
| fund_house | text | AMC managing the fund (e.g. SBI Mutual Fund) |
| scheme_name | text | Full name of the scheme |
| category | text | Broad category — Equity or Debt |
| sub_category | text | Sub-category — Large Cap, Mid Cap, Gilt, Flexi Cap, etc. |
| plan | text | Regular or Direct plan |
| launch_date | text | Date the scheme was launched |
| benchmark | text | Index the fund is benchmarked against |
| expense_ratio_pct | float | Annual expense ratio charged, in percent |
| exit_load_pct | float | Exit load charged on early redemption, in percent |
| min_sip_amount | int | Minimum SIP investment amount (INR) |
| min_lumpsum_amount | int | Minimum lumpsum investment amount (INR) |
| fund_manager | text | Name of the fund manager |
| risk_category | text | Risk level — Low, Moderate, High, Very High, Moderately High |
| sebi_category_code | text | SEBI classification code for the scheme |

### 02_nav_history.csv
Daily NAV (Net Asset Value) per fund.

| Column | Type | Description |
|---|---|---|
| amfi_code | int | Links to fund_master |
| date | date | NAV date |
| nav | float | Net Asset Value per unit on that date (INR) |

Note: cleaned version forward-fills NAV for weekends/holidays so every fund has one row per calendar day.

### 03_aum_by_fund_house.csv
AUM (Assets Under Management) tracked per fund house over time.

| Column | Type | Description |
|---|---|---|
| date | date | Reporting date (quarterly snapshots) |
| fund_house | text | AMC name |
| aum_lakh_crore | float | AUM in lakh crore INR |
| aum_crore | int | AUM in crore INR |
| num_schemes | int | Number of schemes run by that fund house on that date |

### 04_monthly_sip_inflows.csv
Industry-wide SIP inflow trends, monthly.

| Column | Type | Description |
|---|---|---|
| month | text | Month (YYYY-MM) |
| sip_inflow_crore | int | Total SIP inflow that month, crore INR |
| active_sip_accounts_crore | float | Active SIP accounts, in crore |
| new_sip_accounts_lakh | float | New SIP accounts opened that month, in lakh |
| sip_aum_lakh_crore | float | Total SIP AUM, lakh crore INR |
| yoy_growth_pct | float | Year-over-year growth in SIP inflow, percent (blank for months with no prior year to compare) |

### 05_category_inflows.csv
Net inflows by fund category, monthly.

| Column | Type | Description |
|---|---|---|
| month | text | Month (YYYY-MM) |
| category | text | Fund category (Large Cap, Mid Cap, Small Cap, Flexi Cap, etc.) |
| net_inflow_crore | float | Net inflow that month, crore INR |

### 06_industry_folio_count.csv
Investor folio counts across the industry, quarterly.

| Column | Type | Description |
|---|---|---|
| month | text | Period (quarterly) |
| total_folios_crore | float | Total investor folios, in crore |
| equity_folios_crore | float | Folios in equity schemes |
| debt_folios_crore | float | Folios in debt schemes |
| hybrid_folios_crore | float | Folios in hybrid schemes |
| others_folios_crore | float | Folios in other scheme types |

### 07_scheme_performance.csv
Performance and risk metrics per fund.

| Column | Type | Description |
|---|---|---|
| amfi_code | int | Links to fund_master |
| scheme_name | text | Full scheme name |
| fund_house | text | AMC name |
| category | text | Fund category |
| plan | text | Regular or Direct |
| return_1yr_pct | float | 1-year return, percent |
| return_3yr_pct | float | 3-year annualised return, percent |
| return_5yr_pct | float | 5-year annualised return, percent |
| benchmark_3yr_pct | float | Benchmark's 3-year return, percent |
| alpha | float | Excess return vs benchmark |
| beta | float | Volatility relative to benchmark |
| sharpe_ratio | float | Risk-adjusted return measure |
| sortino_ratio | float | Downside risk-adjusted return measure |
| std_dev_ann_pct | float | Annualised standard deviation, percent |
| max_drawdown_pct | float | Maximum observed drawdown, percent |
| aum_crore | int | Fund's AUM, crore INR |
| expense_ratio_pct | float | Annual expense ratio, percent |
| morningstar_rating | int | Morningstar star rating (1-5) |
| risk_grade | text | Risk classification |

### 08_investor_transactions.csv
Individual investor transactions.

| Column | Type | Description |
|---|---|---|
| investor_id | text | Unique investor identifier |
| transaction_date | date | Date of transaction |
| amfi_code | int | Fund the transaction relates to |
| transaction_type | text | SIP, Lumpsum, or Redemption |
| amount_inr | int | Transaction amount, INR |
| state | text | Investor's state |
| city | text | Investor's city |
| city_tier | text | City tier classification (1, 2, 3) |
| age_group | text | Investor's age bracket |
| gender | text | Investor's gender |
| annual_income_lakh | float | Investor's annual income, lakh INR |
| payment_mode | text | UPI, Cheque, Mandate, Net Banking, etc. |
| kyc_status | text | Verified or Pending |

### 09_portfolio_holdings.csv
Stock-level portfolio holdings per fund.

| Column | Type | Description |
|---|---|---|
| amfi_code | int | Fund holding the stock |
| stock_symbol | text | Stock ticker symbol |
| stock_name | text | Company name |
| sector | text | Sector the stock belongs to |
| weight_pct | float | Weight of the holding in the portfolio, percent |
| market_value_cr | float | Market value of the holding, crore INR |
| current_price_inr | float | Current stock price, INR |
| portfolio_date | date | Date of the portfolio snapshot |

### 10_benchmark_indices.csv
Daily closing values for benchmark indices.

| Column | Type | Description |
|---|---|---|
| date | date | Trading date |
| index_name | text | Index name (e.g. NIFTY50) |
| close_value | float | Closing value of the index |

---

## SQLite Star Schema (bluestock_mf.db)

### dim_fund
Dimension table, one row per fund. Same columns as fund_master minus expense_ratio_pct (that lives in fact_performance instead, since it can change over time). Primary key: `amfi_code`.

### dim_date
Calendar dimension built from every date seen across fact_nav, fact_transactions, and fact_aum. Primary key: `date`. Includes year, month, day, quarter, weekday for easy time-based grouping.

### fact_nav
Daily NAV per fund. Foreign keys: `amfi_code` → dim_fund, `date` → dim_date.

### fact_transactions
Every investor transaction. Foreign keys: `amfi_code` → dim_fund, `date` → dim_date.

### fact_performance
One row per fund with performance/risk metrics. Primary key and foreign key: `amfi_code` → dim_fund.

### fact_aum
AUM by fund house over time. Foreign key: `date` → dim_date.

---

## Source References
All 10 raw CSVs were provided as part of the Day 1 task assignment (shared via GitHub / Google Sheets by the team). Live NAV data for HDFC Top 100 Direct and 5 key schemes was fetched directly from the mfapi.in public API.
