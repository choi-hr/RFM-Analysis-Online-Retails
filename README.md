# RFM Customer Analysis

Turn historical purchase records into transparent customer priorities for retention, reactivation and relationship development. A reproducible Python pipeline and independent SQL checks connect customer behavior to testable marketing actions.

**Tableau status:** new combined workbook **not published**. Editable [TWBX draft](tableau/Customer_Intelligence_DRAFT.twbx), [source CSV](tableau/customers.csv), and [publication / QA instructions](tableau/PUBLISHING.md) are available. No customer Tableau screenshot or live URL is claimed.

## Business problem
Which customers generate observed purchase value, which show historical inactivity, and where should a commercial team investigate before investing in outreach?

## Analytical questions
- How are customers, orders and purchase value distributed by country and segment?
- Which RFM groups merit retention, development or reactivation tests?
- Which observed co-purchases warrant a cross-sell hypothesis?

## Dataset and provenance
Chen, D. (2012), UCI Online Retail II, [DOI](https://doi.org/10.24432/C5CG6D), CC BY 4.0. Both sheets cover 1 Dec 2009–9 Dec 2011; 1,067,371 source rows. The transformed data excludes unknown customers, cancellations, returns, nonpositive prices and exact duplicates. See [methodology](docs/methodology.md) and [audit](docs/audit.json).

## Python and SQL
[src/build.py](src/build.py) prepares data and scores customers; [sql/analysis.sql](sql/analysis.sql) executes real SQLite customer, country, segment and KPI aggregations. Independent SQL customer counts and integer purchase values match pandas exactly. [SQL results](docs/sql_results.json) record the executed queries.

## KPIs and validated findings
| Metric | Value |
|---|---:|
| Eligible customers | 5,878 |
| Distinct eligible invoices | 36,969 |
| Eligible purchase value | £17,374,804.25 |
| Average order value | £469.98 |
| Customers with 2+ invoices | 72.39% |

Champions represent 21.6% of customers and 67.9% of observed purchase value. At Risk contains 478 customers with £1.50m historical purchase value. These are descriptive results, not campaign outcomes.

## Business implications
Prioritize relationship-care tests for Champions and investigate purchase-cycle and service explanations for At Risk. Evaluate outreach against randomized holdouts. [Findings and actions](docs/findings.md) separate measured observations from proposed tests, including country considerations and a product-pair cross-sell hypothesis.

## Reproduce
```bash
python -m pip install -r requirements.txt
# Download the original Excel workbook from the UCI source below and keep it local.
python src/build.py --input /path/to/online_retail_II.xlsx --output .
python src/build_workbook.py
```
[Official input](https://archive.ics.uci.edu/dataset/502/online+retail+ii). Outputs include ignored private transactions, customer and RFM tables, local SQLite database, Tableau CSVs and audit documentation. No raw workbook or DataCo customer records are committed. Exported customer keys are pseudonymous, not original customer identifiers. Workbook generation validates XML structure only; render and publish through Tableau before claiming completion.

## Original work and limitations
The preserved `RFM.ipynb` originally used UCI Online Retail II in two separate annual sheets. It counted unique InvoiceDate values as frequency; the rebuilt pipeline counts distinct invoice IDs. The notebook is preserved unchanged as historical work, and is superseded by `src/build.py` for reproducible calculations.

The rebuilt combined analysis changes eligibility, currency rounding, observation date and scoring. It is not numerically interchangeable with original annual results. Recency is relative to 10 Dec 2011. Ties receive equal scores; segments follow documented ordered rules. Purchase value excludes returns and is neither net revenue, profit nor CLV. Geography allocates full customer histories to their latest country. Historical retailer patterns do not establish current logistics demand. See [limitations and definitions](docs/methodology.md).

## Technologies
Python · pandas · NumPy · SQLite / SQL · Tableau-ready CSV · editable Tableau XML draft.

## Explore related work
[Customer Segmentation](https://github.com/choi-hr/Customer-segmentation) · [Commercial Logistics Intelligence](https://github.com/choi-hr/commercial-logistics-intelligence) · [Tableau profile](https://public.tableau.com/app/profile/harin.choi/vizzes)
