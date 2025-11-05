# FLPP Power BI Dashboard - Source to Visual Mapping

## Overview

This document provides a comprehensive mapping of data sources to dashboard visuals, including all transformations, measures, and relationships used. This serves as a complete reference for understanding how data flows from the Excel source to the final dashboard visuals.

## Data Source Mapping

### Excel File: `FLPP_All_Data_Merged.xlsx`

| Sheet Name | Power BI Table | Primary Key | Row Count | Key Fields |
|------------|----------------|-------------|-----------|------------|
| Completed Services | CompletedServices | (Index) | 2,364 | Customer Id, Tech Name, Service Date |
| Sales by Tech | SalesByTech | (Index) | 224 | Customer Id, Primary Sales Rep, Sold Date |
| Lost Sales | LostSales | (Index) | 34 | Sales Rep, Acct #, Sold Date |
| Customer Detail | CustomerDetail | Customer Id | Variable | Customer Id, Auto Pay, Status |
| Tech Reviews | TechReviews | (Index) | Variable | Technician, Average Star Rating |
| Customer Reviews | CustomerReviews | (Index) | Variable | Customer Id, Review Date, Rating |
| Top Rep Index | TopRepIndex | (Index) | Variable | Sales Rep, Rank, Index |
| Financials | Financials | (Index) | Variable | Month, Branch, Revenue, Payroll, EBITDA |

## Visual Mapping by Dashboard Page

### Page 1: Main Dashboard (KPI Scorecard)

#### Visual: Monthly Sales per Rep (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | SalesByTech | Average of monthly sales per rep | `Monthly Sales per Rep` |
| **Target** | KPI Targets Table | Static target value | `Sales Target` = $50,000 |
| **% to Target** | Calculated | (Actual / Target) | `% to Target` |
| **Status** | Calculated | Traffic light logic | `Sales Status` |
| **Data Source** | SalesByTech[Contract Value] | Aggregated by Sales Rep | SUM('Sales by Tech'[Contract Value]) |

**DAX Measure:**
```dax
Monthly Sales per Rep = 
AVERAGEX(
    VALUES('Sales by Tech'[Primary Sales Rep]),
    CALCULATE(SUM('Sales by Tech'[Contract Value]))
)
```

#### Visual: Recurring Sales % (KPI Card + Donut Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | SalesByTech | % of recurring sales | `Recurring Sales %` |
| **Target** | KPI Targets Table | Static target value | `Recurring Sales Target` = 60% |
| **Categories** | SalesByTech[Category] | Filtered by "Recurring", "Monthly", "Bi-Monthly", "Quarterly" | Category field |
| **Data Source** | SalesByTech[Contract Value] | Filtered by category | SUM('Sales by Tech'[Contract Value]) |

**DAX Measure:**
```dax
Recurring Sales % = 
VAR TotalSales = [Total Sales]
VAR RecurringSales = 
    CALCULATE(
        [Total Sales],
        FILTER(
            'Sales by Tech',
            CONTAINSSTRING('Sales by Tech'[Category], "Recurring") ||
            CONTAINSSTRING('Sales by Tech'[Category], "Monthly") ||
            CONTAINSSTRING('Sales by Tech'[Category], "Bi-Monthly") ||
            CONTAINSSTRING('Sales by Tech'[Category], "Quarterly")
        )
    )
RETURN
    DIVIDE(RecurringSales, TotalSales, 0)
```

#### Visual: Organic Growth YoY (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | SalesByTech + Date Table | YoY comparison | `Organic Growth YoY` |
| **Target** | KPI Targets Table | Static target value | `Growth Target` = 15% |
| **Time Period** | Date Table | Current Year vs Previous Year | Date[Year] |
| **Data Source** | SalesByTech[Contract Value] | Grouped by Year | TOTALYTD(SUM(...)) |

#### Visual: Cancellation Rate (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | LostSales + SalesByTech | Lost / (Sales + Lost) | `Cancellation Rate` |
| **Target** | KPI Targets Table | Static target value | `Cancellation Target` = 5% |
| **Data Sources** | LostSales[Contract Value], SalesByTech[Contract Value] | Combined calculation | SUM(Lost Sales) / SUM(Total Sales + Lost Sales) |

**DAX Measure:**
```dax
Cancellation Rate = 
VAR TotalSales = [Total Sales]
VAR LostSales = SUM('Lost Sales'[Contract Value])
RETURN
    DIVIDE(LostSales, TotalSales + LostSales, 0)
```

#### Visual: Completion Rate (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CompletedServices | Completed / Assigned | `Completion Rate` |
| **Target** | KPI Targets Table | Static target value | `Completion Target` = 95% |
| **Data Source** | CompletedServices | Count of rows | COUNTROWS('Completed Services') |
| **Note** | Assumes all rows are completed services | Adjust if assigned services data exists | |

#### Visual: Tech Review Score (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | TechReviews | Average rating | `Tech Review Score` |
| **Target** | KPI Targets Table | Static target value | `Tech Review Target` = 4.5 |
| **Data Source** | TechReviews[Average Star Rating] | Average across all techs | AVERAGE('Tech Reviews'[Average Star Rating]) |

#### Visual: Recurring Service Ratio (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CompletedServices + CustomerDetail | Recurring customers / Total | `Recurring Service Ratio` |
| **Target** | KPI Targets Table | Static target value | `Recurring Service Target` = 70% |
| **Data Source** | CustomerDetail[Auto Pay Flag] | Filtered by Auto Pay = TRUE | DISTINCTCOUNT('Completed Services'[Customer Id]) |

#### Visual: Service Accuracy / Callbacks (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CompletedServices | Callbacks / Total Services | `Callback Rate` |
| **Target** | KPI Targets Table | Static target value | `Callback Target` = 3% |
| **Data Source** | CompletedServices[Type], [Name], [Category] | Filtered by "Callback" | COUNTROWS filtered by callback indicator |

**DAX Measure:**
```dax
Service Accuracy = 1 - [Callback Rate]
```

#### Visual: Payroll % of Revenue (Gauge)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials | Payroll / Revenue | `Payroll % of Revenue` |
| **Target** | KPI Targets Table | Static target value | `Payroll Target` = 40% |
| **Data Sources** | Financials[Payroll], Financials[Revenue] | Division | DIVIDE(SUM(Payroll), SUM(Revenue)) |

#### Visual: Chemical Spend % (Gauge)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials | Chemical / Revenue | `Chemical Spend %` |
| **Target** | KPI Targets Table | Static target value | `Chemical Target` = 8% |
| **Data Sources** | Financials[Chemical Spend], Financials[Revenue] | Division | DIVIDE(SUM(Chemical), SUM(Revenue)) |

#### Visual: EBITDA Margin (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials | EBITDA / Revenue | `EBITDA Margin` |
| **Target** | KPI Targets Table | Static target value | `EBITDA Target` = 20% |
| **Data Sources** | Financials[EBITDA], Financials[Revenue] | Division | DIVIDE(SUM(EBITDA), SUM(Revenue)) |

#### Visual: Revenue Growth YoY (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials + Date Table | (Current Year - Previous Year) / Previous Year | `Revenue Growth YoY` |
| **Target** | KPI Targets Table | Static target value | `Growth Target` = 15% |
| **Data Source** | Financials[Revenue] | Grouped by Year | TOTALYTD(SUM(Revenue)) |

#### Visual: Auto Pay Enrollment (Donut Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CustomerDetail | Auto Pay customers / Total | `Auto Pay Enrollment %` |
| **Target** | KPI Targets Table | Static target value | `Auto Pay Target` = 80% |
| **Data Source** | CustomerDetail[Auto Pay Flag] | Count TRUE vs FALSE | COUNTROWS filtered by Auto Pay Flag |

**DAX Measure:**
```dax
Auto Pay Enrollment % = 
VAR TotalCustomers = COUNTROWS('Customer Detail')
VAR AutoPayCustomers = 
    CALCULATE(
        COUNTROWS('Customer Detail'),
        'Customer Detail'[Auto Pay Flag] = TRUE
    )
RETURN
    DIVIDE(AutoPayCustomers, TotalCustomers, 0)
```

#### Visual: Avg Customer Review (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CustomerReviews | Average rating | `Avg Customer Review` |
| **Target** | KPI Targets Table | Static target value | `Review Target` = 4.5 |
| **Data Source** | CustomerReviews[Overall Star Rating] | Average | AVERAGE('Customer Reviews'[Overall Star Rating]) |

#### Visual: Fleet Safety Grade (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Manual/External | Manual input or calculated | `Fleet Safety Grade` |
| **Target** | KPI Targets Table | Static target value | `Safety Target` = A |
| **Data Source** | TBD - To be implemented | Placeholder | |

#### Visual: Total YTD Revenue (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials + Date Table | Year-to-date total | `Total YTD Revenue` |
| **Target** | KPI Targets Table | Static target value | `YTD Revenue Target` = $10M |
| **Data Source** | Financials[Revenue] | Cumulative YTD | TOTALYTD(SUM(Revenue), Date[Date]) |

#### Visual: Avg Monthly Production per Tech (KPI Card)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CompletedServices | Revenue / Months / Techs | `Avg Monthly Production per Tech` |
| **Target** | KPI Targets Table | Static target value | `Production Target` = $15,000 |
| **Data Sources** | CompletedServices[Invoice Amount], [Tech Name], Date Table | Complex calculation | DIVIDE(Total Revenue / Months, Distinct Techs) |

### Page 2: Sales & Growth Detail

#### Visual: Monthly Sales per Rep (Clustered Column Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **X-Axis** | SalesByTech | Sales Rep | 'Sales by Tech'[Primary Sales Rep] |
| **Y-Axis** | SalesByTech | Sales Amount | SUM('Sales by Tech'[Contract Value]) |
| **Drill-down** | SalesByTech → CustomerDetail | Customer level | Customer Name, Contract Value |

#### Visual: Recurring Sales % (Donut Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Categories** | SalesByTech | Recurring vs One-time | Filtered by Category |
| **Values** | SalesByTech | Sales Amount | SUM('Sales by Tech'[Contract Value]) |

#### Visual: Organic Growth YoY (Line Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **X-Axis** | Date Table | Month | Date[Year Month] |
| **Y-Axis** | SalesByTech | Sales Amount | SUM('Sales by Tech'[Contract Value]) |
| **Series** | Date Table | Current Year vs Previous Year | Date[Year] |

#### Visual: Lost Sales Table

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Columns** | LostSales | All columns | Sales Rep, Customer Name, Date, Category, Contract Value |
| **Filtering** | LostSales | By filters | All slicers apply |

### Page 3: Technician Performance Detail

#### Visual: Completion Rate Trend (Line Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **X-Axis** | Date Table | Date | Date[Date] |
| **Y-Axis** | CompletedServices | Completion Rate | `Completion Rate` (calculated over time) |

#### Visual: Tech Review Score (Bar Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **X-Axis** | TechReviews | Technician | 'Tech Reviews'[Technician] |
| **Y-Axis** | TechReviews | Rating | 'Tech Reviews'[Average Star Rating] |
| **Drill-down** | TechReviews → CustomerReviews | Review comments | Individual reviews |

#### Visual: Recurring Service Ratio (Pie Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Categories** | CompletedServices + CustomerDetail | Recurring vs One-time | Filtered by Auto Pay Flag |
| **Values** | CompletedServices | Count of services | COUNTROWS('Completed Services') |

#### Visual: Service Accuracy (Gauge)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | CompletedServices | 1 - Callback Rate | `Service Accuracy` |
| **Target** | KPI Targets Table | 97% | `Service Accuracy Target` |

### Page 4: Financial Metrics Detail

#### Visual: Payroll % of Revenue (Gauge)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials | Payroll / Revenue | `Payroll % of Revenue` |
| **Target** | KPI Targets Table | 40% | `Payroll Target` |

#### Visual: Chemical Spend % (Gauge)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Value** | Financials | Chemical / Revenue | `Chemical Spend %` |
| **Target** | KPI Targets Table | 8% | `Chemical Target` |

#### Visual: EBITDA Margin Trend (Line Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **X-Axis** | Date Table | Month | Date[Year Month] |
| **Y-Axis** | Financials | EBITDA Margin | `EBITDA Margin` |

#### Visual: Revenue Growth YoY (Line Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **X-Axis** | Date Table | Month | Date[Year Month] |
| **Y-Axis** | Financials | Revenue | Financials[Revenue] |
| **Series** | Date Table | Current Year vs Previous Year | Date[Year] |

### Page 5: Customer & Payment Detail

#### Visual: Auto Pay Enrollment (Donut Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Categories** | CustomerDetail | Enrolled vs Not Enrolled | Customer Detail[Auto Pay Flag] |
| **Values** | CustomerDetail | Count of customers | COUNTROWS('Customer Detail') |

#### Visual: Avg Customer Review (Card + Bar Chart)

| Component | Source | Calculation | Measure/Column |
|-----------|--------|-------------|----------------|
| **Card Value** | CustomerReviews | Average rating | `Avg Customer Review` |
| **Bar Chart** | CustomerReviews + Date Table | Trend over time | AVERAGE grouped by Month |

## Transformation Summary

### Power Query Transformations

| Table | Key Transformations |
|-------|---------------------|
| **CompletedServices** | Remove empty columns, clean currency strings, convert to numbers, trim text fields |
| **SalesByTech** | Clean currency strings, convert Customer Id to number, standardize names |
| **LostSales** | Remove empty columns, standardize date formats |
| **CustomerDetail** | Promote headers from first row, convert Auto Pay to boolean flag, trim text |
| **TechReviews** | Promote headers from first row, standardize technician names |
| **CustomerReviews** | Promote headers from first row, standardize dates and names |
| **TopRepIndex** | Promote headers from first row, standardize sales rep names |
| **Financials** | Parse P&L structure (adjust based on actual format) |
| **Date Table** | Create from date range, add year, quarter, month attributes |

## Relationship Mapping

| Relationship | From Table | To Table | Key Field | Purpose |
|--------------|------------|----------|-----------|---------|
| Customer ↔ Services | CustomerDetail | CompletedServices | Customer Id | Link services to customers |
| Customer ↔ Sales | CustomerDetail | SalesByTech | Customer Id | Link sales to customers |
| Customer ↔ Reviews | CustomerDetail | CustomerReviews | Customer Id | Link reviews to customers |
| Tech ↔ Services | TechReviews | CompletedServices | Tech Name → Technician | Correlate quality with volume |
| Sales Rep ↔ Sales | TopRepIndex | SalesByTech | Sales Rep → Primary Sales Rep | Compare performance |
| Date ↔ All Facts | Date Table | All Fact Tables | Date → Various Date Fields | Time intelligence |

## Measure Dependencies

### Base Measures (Used by Other Measures)

1. **Total Sales** - Used by: Recurring Sales %, Cancellation Rate, Organic Growth
2. **Total Revenue** - Used by: Payroll %, Chemical %, EBITDA Margin, Revenue Growth
3. **YTD Actual** - Used by: % to Target calculations

### Compound Measures (Depend on Other Measures)

1. **Recurring Sales %** - Uses: Total Sales
2. **Cancellation Rate** - Uses: Total Sales, Lost Sales Amount
3. **Organic Growth YoY** - Uses: Total Sales, Date calculations
4. **Service Accuracy** - Uses: Callback Rate

## Filter Propagation

### Global Filters (Apply to All Pages)

- **Month/Date** - Filters all time-based visuals
- **Branch** - Filters all branch-specific data
- **Year** - Filters all year-based comparisons

### Page-Specific Filters

- **Sales Rep** - Sales & Growth page
- **Technician** - Technician Performance page
- **Category** - All pages (context-dependent)
- **Account Type** - Customer & Payment page

## Data Refresh Requirements

### Refresh Schedule

- **Daily:** Sales by Tech, Completed Services, Lost Sales
- **Weekly:** Customer Detail, Tech Reviews, Customer Reviews
- **Monthly:** Financials, Top Rep Index

### Data Source Location

- **Excel File:** `data/FLPP_All_Data_Merged.xlsx`
- **Path:** Relative to Power BI file location
- **Update Method:** Replace entire file or use Power BI Gateway for scheduled refresh

## Performance Considerations

### Large Tables

- **CompletedServices:** 2,364 rows - Consider aggregating for summary visuals
- **SalesByTech:** 224 rows - Manageable size
- **CustomerDetail:** Variable - Index Customer Id for faster joins

### Optimization Tips

1. **Use Aggregations:** Pre-aggregate data where possible
2. **Index Keys:** Ensure all relationship keys are indexed
3. **Limit Columns:** Only load necessary columns in Power Query
4. **Date Table:** Use built-in date table for better performance
5. **Measure Optimization:** Use SUMX sparingly, prefer SUM where possible

## Troubleshooting Guide

### Common Issues

1. **Measure Returns Blank:**
   - Check relationship exists and is active
   - Verify filter context
   - Check for null values in key fields

2. **Visual Not Updating:**
   - Verify data refresh completed
   - Check filter selections
   - Review measure calculations

3. **Relationship Errors:**
   - Verify data types match (number vs text)
   - Check for null values in key columns
   - Ensure names match exactly (case-sensitive)

4. **Performance Slow:**
   - Review large tables
   - Check for unnecessary calculations
   - Consider using aggregations


