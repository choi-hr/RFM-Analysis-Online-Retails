# Published Tableau workbook

[Customer Intelligence & Marketing Strategy](https://public.tableau.com/app/profile/harin.choi/viz/CustomerIntelligenceMarketingStrategy/MarketingStrategyBusinessInsights#1)

Three dashboard tabs share the same 5,878-row customer export. All three were opened in the public viewer. Source worksheets are hidden from public tab navigation. The published TWBX was downloaded through Tableau Public, rather than inferred from a generated XML prototype.

## Verified views and interactions
- Customer Segmentation: eligible purchase value £17.37m; customers 5,878; distinct invoices 36,969; AOV £469.98; repeat-customer share 72.4%. Country and segment bars act as dashboard filters; clear the selection to reset.
- Selecting Champions changed the KPIs to 1,268 customers, 22,034 invoices, £11.80m and £535.32 AOV. Selecting United Kingdom changed the KPIs to 5,350 customers, 33,542 invoices and £14.39m.
- RFM Customer Analysis: customer counts, purchase value, mean R/F/M, recency-score distribution, customer-value scatterplot and country comparison. Country and segment chart selection filters the dashboard.
- Marketing Strategy & Business Insights: historical purchase value by proposed action, repeat-customer shares, country customer map and a text panel separating observed metrics from proposed experiments.

Purchase value excludes cancellations and returns; it is not net revenue. The map may not resolve historical/ambiguous country labels (for example Unspecified); the country bar chart retains the complete customer allocation. Customer value bands use historical observed spend, not predicted CLV.

## Files
- `Customer_Intelligence_Marketing_Strategy.twbx`: actual downloaded published workbook, with embedded public UCI-derived customer data.
- `customers.csv`: source customer dataset, using hashed keys in place of original IDs.
- Other CSVs: independently reproducible supplementary exports.

## QA
Compare the all-customer KPIs to `docs/audit.json` and independent SQLite results in `docs/sql_results.json`. Navigate all three tabs; test country and segment selection; clear selections. Captures in `assets/` are real browser screenshots from Tableau Public. The historical dataset does not demonstrate current campaign performance or logistics demand.
