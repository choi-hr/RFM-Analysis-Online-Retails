# Methodology and KPI dictionary

## Provenance
Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D . CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ . Source: https://archive.ics.uci.edu/dataset/502/online+retail+ii . Both original Excel sheets are concatenated; this is a new combined analysis, not a reproduction of either original year's reported results. Source hash, row counts, missingness and exclusions are in audit.json.

## Eligibility and cleaning
Remove exact duplicates across all source columns before analysis. This conservative rule may remove legitimate identical lines; the source has no line ID, so this uncertainty is retained. Keep only identified customers, present invoice/date, positive quantity and price, and invoices not beginning C. Missing descriptions alone do not exclude a valid purchase. No cancellation-to-sale matching is attempted. Negative quantities and cancellations are excluded, not subtracted. Purchase value therefore measures eligible positive purchases, not net revenue, profit, CLV or realized campaign value. Positive non-merchandise codes are retained, including charges; this is not exclusively merchandise sales. Values are in GBP, with each eligible line rounded to integer pence (nearest, ties-to-even) before summation. No FX conversion.

Missing customer IDs affect 243,007 raw rows. Those purchases are excluded from all shared customer KPIs rather than counted in a different denominator. Raw audit flags overlap; their counts are not additive. Customer IDs are replaced with deterministic opaque keys; original IDs, invoices and source records stay in ignored private outputs. Hashing is pseudonymization, not proof of formal anonymization. This source is already a public historical dataset, with no names, emails or street addresses in released customer exports. DataCo customer records and access logs are never published.

## Grain and formulas
| Metric | Definition |
|---|---|
| Customer | One distinct identified eligible customer across both sheets |
| Order | One distinct eligible invoice; invoice-to-customer uniqueness asserted |
| Purchase value | Sum of rounded eligible line values in GBP |
| AOV | Total purchase value / distinct invoices |
| Frequency | Distinct eligible invoices per customer, not unique timestamps |
| Recency | Whole calendar days between latest eligible purchase date and 2011-12-10 |
| Monetary | Eligible purchase value per customer |
| Repeat share | Customers with at least two eligible invoices / eligible customers |
| Country | Most recent eligible country per customer; date/invoice/country sort breaks ties deterministically |
| Cross-sell support | Invoices containing both item codes / all eligible invoices |

Thirteen customers have multiple countries. Country customer metrics allocate the customer's entire purchase history to their most recent country so customers and purchase value remain additive; they are not a shipment-destination analysis. Monthly active-customer counts are nonadditive. Segment exports sum customer invoice frequencies only after invoice ownership uniqueness is checked. No joins to monthly or pair exports are needed for customer dashboards.

## Scoring and segments
For each metric, compute the 20th/40th/60th/80th percentile cutpoints with pandas' linear interpolation. Assign 1 + number of cutpoints strictly below the value; reverse recency (6 minus score). Values equal to a cutpoint stay in the lower ascending bin. Equal observations always receive equal scores, even when bin sizes differ. Cutpoints are in audit.json. F=1,2,3,4,5 corresponds respectively to 1, 2, 3–4, 5–8, and at least 9 invoices in this run. R=5 corresponds to at most 20 days; R=1 is over 411 days.

Apply the following rules in this exact order:
1. Champions: R>=4, F>=4 and M>=4.
2. At Risk: R<=2 and (F>=4 or M>=4).
3. Loyal Customers: R>=3 and F>=4.
4. Potential Loyalists: R>=4 and F>=2.
5. New / Recent: R>=4 and F=1.
6. Hibernating: R<=2 and F<=2.
7. Needs Attention: all remaining customers.

These are descriptive operational rules, not trained clusters, churn predictions or validated future-value models. No inference of customer intent is made. RFM snapshot is frozen; filtering a country in Tableau must not silently recompute the scores.

## Validation
Python checks integer currency reconciliation, invoice ownership, one segment per customer, segment totals and score bounds. SQLite independently recalculates every customer's distinct invoices and spend and checks exact equality to pandas. All five SQL statements execute against generated local tables; results are recorded in sql_results.json. Quantile and eligibility decisions explain why totals differ from the preserved notebooks. Source data spans 2009-12-01 through 2011-12-09, including incomplete edge months. No current market recommendation is inferred.
