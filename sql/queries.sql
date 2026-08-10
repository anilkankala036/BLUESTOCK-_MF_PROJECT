-- Day 2 - Analytical Queries

-- 1. top 5 funds by aum
SELECT f.scheme_name, f.fund_house, p.aum_crore
FROM fact_performance p
JOIN dim_fund f ON f.amfi_code = p.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- 2. average nav per month for each fund
SELECT n.amfi_code, f.scheme_name, strftime('%Y-%m', n.date) AS month, AVG(n.nav) AS avg_nav
FROM fact_nav n
JOIN dim_fund f ON f.amfi_code = n.amfi_code
GROUP BY n.amfi_code, month
ORDER BY n.amfi_code, month;

-- 3. sip yoy growth (from monthly_sip_inflows, not in star schema, run separately if needed)
-- included here for funds using transaction data instead:
SELECT strftime('%Y', date) AS year, SUM(amount_inr) AS total_sip
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year;

-- 4. transactions by state
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. funds with expense_ratio < 1%
SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct;

-- 6. top 5 funds by 1 year return
SELECT f.scheme_name, p.return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON f.amfi_code = p.amfi_code
ORDER BY p.return_1yr_pct DESC
LIMIT 5;

-- 7. transaction count and total amount by transaction type
SELECT transaction_type, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type;

-- 8. average sharpe ratio by risk category
SELECT f.risk_category, AVG(p.sharpe_ratio) AS avg_sharpe
FROM fact_performance p
JOIN dim_fund f ON f.amfi_code = p.amfi_code
GROUP BY f.risk_category
ORDER BY avg_sharpe DESC;

-- 9. number of funds per fund house, with average expense ratio
SELECT f.fund_house, COUNT(*) AS num_funds, AVG(p.expense_ratio_pct) AS avg_expense_ratio
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.fund_house
ORDER BY num_funds DESC;

-- 10. kyc status breakdown of transactions
SELECT kyc_status, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY kyc_status;
