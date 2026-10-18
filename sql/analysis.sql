-- Eligible purchase KPIs, GBP. Integer pence avoid floating point reconciliation drift.
SELECT COUNT(*) eligible_lines, COUNT(DISTINCT customer_key) customers, COUNT(DISTINCT invoice) orders, SUM(revenue_pence)/100.0 revenue_gbp, SUM(revenue_pence)/100.0/COUNT(DISTINCT invoice) aov_gbp FROM transactions;
-- Independent customer aggregation uses invoice identifiers, never timestamps.
SELECT customer_key, COUNT(DISTINCT invoice) frequency, SUM(revenue_pence)/100.0 monetary_gbp, MAX(date) last_purchase FROM transactions GROUP BY customer_key ORDER BY monetary_gbp DESC LIMIT 10;
SELECT segment, COUNT(*) customers, SUM(frequency) orders, SUM(monetary_pence)/100.0 revenue_gbp, AVG(recency_days) mean_recency, AVG(frequency) mean_frequency, AVG(monetary_pence)/100.0 mean_monetary_gbp FROM customers GROUP BY segment ORDER BY revenue_gbp DESC;
SELECT country, COUNT(*) customers, SUM(monetary_pence)/100.0 revenue_gbp, AVG(repeat_customer) repeat_share FROM customers GROUP BY country ORDER BY revenue_gbp DESC;
SELECT R,F,COUNT(*) customers,SUM(monetary_pence)/100.0 revenue_gbp FROM customers GROUP BY R,F;
