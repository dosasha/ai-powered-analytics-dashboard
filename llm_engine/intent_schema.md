# Intent Schema (v1)

User questions are converted to a structured intent JSON.

## Fields
- metric: total_revenue | orders | aov | customers
- dimension: time | country | product
- period: YYYY-MM or range
- comparison: previous_period | same_period_last_year | none
- why: true | false

## Examples
Q: Why did revenue drop in 2011-03?
{
  "metric": "total_revenue",
  "dimension": "time",
  "period": "2011-03",
  "comparison": "previous_period",
  "why": true
}

Q: Which countries drive revenue?
{
  "metric": "total_revenue",
  "dimension": "country",
  "period": "all",
  "comparison": "none",
  "why": false
}
