# FLPP Power BI Dashboard - KPI Reference Table

## Overview

This document defines all Key Performance Indicators (KPIs) for the FLPP Power BI Dashboard, including goals, targets, calculation methods, and status thresholds.

## KPI Categories

### 1. Sales & Growth

| KPI Name | Description | Goal/Target | Calculation | Status Logic | Priority |
|----------|-------------|-------------|-------------|--------------|----------|
| **Monthly Sales per Rep** | Average or total monthly sales per rep | $50,000/month | `AVERAGEX(Reps, SUM(Sales[Contract Value]))` | Green: ≥$50k, Yellow: $45k-$49k, Red: <$45k | High |
| **Recurring Sales %** | Percentage of sales from recurring customers | 60% | `DIVIDE(Recurring Sales, Total Sales)` | Green: ≥60%, Yellow: 50-59%, Red: <50% | High |
| **Organic Growth** | Year-over-year net new sales growth | 15% YoY | `(Current Year - Previous Year) / Previous Year` | Green: ≥15%, Yellow: 10-14%, Red: <10% | High |
| **Cancellation Rate** | Lost sales as percentage of total opportunities | <5% | `DIVIDE(Lost Sales, Total Sales + Lost Sales)` | Green: <5%, Yellow: 5-7%, Red: >7% | Medium |

### 2. Technician Performance

| KPI Name | Description | Goal/Target | Calculation | Status Logic | Priority |
|----------|-------------|-------------|-------------|--------------|----------|
| **Completion Rate** | Services completed vs. assigned | 95% | `DIVIDE(Completed, Assigned)` | Green: ≥95%, Yellow: 90-94%, Red: <90% | High |
| **Tech Review Score** | Average technician rating | 4.5/5.0 | `AVERAGE(Tech Reviews[Rating])` | Green: ≥4.5, Yellow: 4.0-4.4, Red: <4.0 | High |
| **Recurring Service Ratio** | % of recurring customers per tech | 70% | `DIVIDE(Recurring Customers, Total Customers)` | Green: ≥70%, Yellow: 60-69%, Red: <60% | Medium |
| **Service Accuracy / Callbacks** | % of callback jobs vs. total | <3% | `DIVIDE(Callbacks, Total Services)` | Green: <3%, Yellow: 3-5%, Red: >5% | High |

### 3. Financial Metrics

| KPI Name | Description | Goal/Target | Calculation | Status Logic | Priority |
|----------|-------------|-------------|-------------|--------------|----------|
| **Payroll % of Revenue** | Payroll costs as percentage of revenue | <40% | `DIVIDE(Payroll, Revenue)` | Green: <40%, Yellow: 40-45%, Red: >45% | High |
| **Chemical Spend %** | Chemical costs as percentage of revenue | <8% | `DIVIDE(Chemical Spend, Revenue)` | Green: <8%, Yellow: 8-10%, Red: >10% | Medium |
| **EBITDA Margin** | Operating margin percentage | 20% | `DIVIDE(EBITDA, Revenue)` | Green: ≥20%, Yellow: 15-19%, Red: <15% | High |
| **Revenue Growth YoY** | Year-over-year revenue growth | 15% | `(Current Year - Previous Year) / Previous Year` | Green: ≥15%, Yellow: 10-14%, Red: <10% | High |

### 4. Customer & Payment

| KPI Name | Description | Goal/Target | Calculation | Status Logic | Priority |
|----------|-------------|-------------|-------------|--------------|----------|
| **Auto Pay Enrollment** | Percentage of customers enrolled in auto-pay | 80% | `DIVIDE(Auto Pay Customers, Total Customers)` | Green: ≥80%, Yellow: 70-79%, Red: <70% | Medium |
| **Avg Customer Review** | Average customer review score | 4.5/5.0 | `AVERAGE(Customer Reviews[Rating])` | Green: ≥4.5, Yellow: 4.0-4.4, Red: <4.0 | High |

### 5. Fleet & Safety

| KPI Name | Description | Goal/Target | Calculation | Status Logic | Priority |
|----------|-------------|-------------|-------------|--------------|----------|
| **Fleet Safety Grade** | Safety rating (manual or external source) | A | Manual input or calculated from incidents | Green: A, Yellow: B, Red: C or below | Medium |
| **Total YTD Revenue** | Cumulative year-to-date revenue | $10M | `TOTALYTD(SUM(Revenue), Date[Date])` | Green: ≥$10M, Yellow: $9M-$9.9M, Red: <$9M | High |
| **Avg Monthly Production per Tech** | Total service revenue ÷ number of techs | $15,000/month | `DIVIDE(Total Revenue / Months, Distinct Techs)` | Green: ≥$15k, Yellow: $12k-$14k, Red: <$12k | Medium |
| **Recurring % of Sales** | Portion of sales from recurring customers | 60% | Same as Recurring Sales % | Green: ≥60%, Yellow: 50-59%, Red: <50% | High |

## Status Color Coding

### Traffic Light System

- **🟢 Green (On Target):** KPI meets or exceeds target threshold
- **🟡 Yellow (At Risk):** KPI is within warning range (90-99% of target)
- **🔴 Red (Below Target):** KPI is below acceptable threshold

### Status Calculation Logic

```dax
Status = 
VAR PctToTarget = DIVIDE(Actual, Target, 0)
RETURN
    SWITCH(
        TRUE(),
        PctToTarget >= 1.0, "Green",      // ≥ 100% of target
        PctToTarget >= 0.90, "Yellow",    // 90-99% of target
        "Red"                              // < 90% of target
    )
```

## KPI Target Values Table (Power BI)

Create a KPI Targets table in Power BI for dynamic target management:

| KPI Category | KPI Name | Target Value | Unit | Last Updated | Notes |
|--------------|----------|--------------|------|--------------|-------|
| Sales & Growth | Monthly Sales per Rep | 50000 | USD | 2025-01-01 | Per rep monthly average |
| Sales & Growth | Recurring Sales % | 0.60 | Percentage | 2025-01-01 | 60% target |
| Sales & Growth | Organic Growth | 0.15 | Percentage | 2025-01-01 | 15% YoY growth |
| Sales & Growth | Cancellation Rate | 0.05 | Percentage | 2025-01-01 | <5% target |
| Technician Performance | Completion Rate | 0.95 | Percentage | 2025-01-01 | 95% target |
| Technician Performance | Tech Review Score | 4.5 | Rating | 2025-01-01 | Out of 5.0 |
| Technician Performance | Recurring Service Ratio | 0.70 | Percentage | 2025-01-01 | 70% target |
| Technician Performance | Service Accuracy | 0.97 | Percentage | 2025-01-01 | <3% callbacks |
| Financial Metrics | Payroll % of Revenue | 0.40 | Percentage | 2025-01-01 | <40% target |
| Financial Metrics | Chemical Spend % | 0.08 | Percentage | 2025-01-01 | <8% target |
| Financial Metrics | EBITDA Margin | 0.20 | Percentage | 2025-01-01 | 20% target |
| Financial Metrics | Revenue Growth YoY | 0.15 | Percentage | 2025-01-01 | 15% YoY |
| Customer & Payment | Auto Pay Enrollment | 0.80 | Percentage | 2025-01-01 | 80% target |
| Customer & Payment | Avg Customer Review | 4.5 | Rating | 2025-01-01 | Out of 5.0 |
| Fleet & Safety | Total YTD Revenue | 10000000 | USD | 2025-01-01 | $10M target |
| Fleet & Safety | Avg Monthly Production per Tech | 15000 | USD | 2025-01-01 | $15k/month |

## DAX Measure for Dynamic Targets

```dax
// KPI Target Lookup
KPI Target = 
VAR CurrentKPI = SELECTEDVALUE('KPI Targets'[KPI Name])
VAR TargetValue = 
    CALCULATE(
        MAX('KPI Targets'[Target Value]),
        'KPI Targets'[KPI Name] = CurrentKPI
    )
RETURN
    TargetValue

// % to Target (Generic)
% to Target = 
VAR Actual = [Current KPI Measure]  // Replace with specific measure
VAR Target = [KPI Target]
RETURN
    DIVIDE(Actual, Target, 0)
```

## Implementation in Power BI

### Step 1: Create KPI Targets Table

1. In Power BI, create a new table with the structure above
2. Import or manually enter target values
3. Create relationships to filter context if needed

### Step 2: Create Status Measures

For each KPI, create a status measure:
```dax
[KPI Name] Status = 
VAR Actual = [KPI Actual Measure]
VAR Target = [KPI Target]
VAR PctToTarget = DIVIDE(Actual, Target, 0)
RETURN
    SWITCH(
        TRUE(),
        PctToTarget >= 1.0, "Green",
        PctToTarget >= 0.90, "Yellow",
        "Red"
    )
```

### Step 3: Create Conditional Formatting

1. Select KPI card visual
2. Format → Conditional formatting
3. Choose "Field value" or "Rules"
4. Set up rules based on status values

### Step 4: Create KPI Scorecard Visual

1. Create KPI cards for each KPI
2. Add status indicator (traffic light icon or color)
3. Display Actual, Target, and % to Target
4. Group by category on separate pages or sections

## Notes and Considerations

1. **Target Updates:** Review and update targets quarterly or as business goals change
2. **Historical Context:** Consider showing targets vs. actuals over time
3. **Benchmarking:** Compare actuals to industry benchmarks where available
4. **Flexibility:** Allow users to adjust targets via parameters if needed
5. **Documentation:** Keep this document updated when targets change

## Review Schedule

- **Monthly:** Review KPI performance against targets
- **Quarterly:** Evaluate and adjust target values
- **Annually:** Comprehensive review of all KPIs and targets


