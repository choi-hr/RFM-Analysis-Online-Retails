# Findings and proposed business actions

## Validated observations
- Invoice counts and unique purchase timestamps differ for 171 customers in the rebuilt two-year eligible dataset (36,969 customer-invoices versus 36,851 customer-timestamps in total). This confirms that the legacy timestamp definition is not interchangeable with invoice frequency.
- 5,878 customers, 36,969 orders and £17,374,804.25 eligible purchase value; AOV £469.98.
- Champions: 1,268 customers (21.6%) account for £11,795,212.16 (67.9%) of observed purchase value.
- At Risk: 478 customers account for £1,501,699.67 in historical purchases. This is historical exposure, not revenue recoverable by a campaign.
- Repeat customers: 72.4%. This describes repeated orders in the observation window, not cohort retention or future retention.
- Customers allocated to the UK account for 82.8% of eligible purchase value, under the latest-country attribution rule.
- Hibernating: 1,565 customers and 3.0% of purchase value.
- Most frequent pair among 30 shortlisted products: 22386 + 85099B appears in 1,064 invoices, support 2.88%. Candidate search is restricted to 30 most widely purchased product codes; this is not an exhaustive association-rule analysis.

## Proposed actions and evaluation
| Priority | Hypothesis / action | Evidence | Evaluation before rollout |
|---|---|---|---|
| Retain | Assign account-care and early-access tests to Champions | High historical value concentration | Randomized customer holdout; next-order rate and incremental gross profit where cost data exists |
| Reactivate | Investigate contactability, service issues and purchase cycle for At Risk | Low recency scores combined with high frequency or monetary scores | Consent and margin eligibility; randomized outreach vs holdout; measure incremental orders and unsubscribe rate |
| Develop | Test second-purchase onboarding for New / Recent and Potential Loyalists | Transparent recent-purchase segment criteria | Fixed cohort window; baseline-balanced experiment; avoid selection bias |
| Cross-sell | Test a contextual bundle for 22386 and 85099B | Co-purchase count and support above | First review product descriptions, availability and economics; compare randomized offer against holdout |
| Geographic | Start UK messaging research, then compare overseas fulfillment constraints | UK concentration in this historical retailer | Validate current customer geography, language, consent and delivery economics |

No campaign conversion, uplift, ROI, attribution or causal effect is observed. These recommendations concern the historical retailer; applying them to B2B logistics would require shipment/customer-account data and validation.
