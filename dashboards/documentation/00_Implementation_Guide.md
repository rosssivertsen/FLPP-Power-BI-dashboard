# FLPP Power BI Dashboard - Implementation Guide

## Quick Start

This guide will walk you through implementing the FLPP Power BI Dashboard from scratch using the provided specifications and code.

## Prerequisites

- Power BI Desktop (latest version)
- Excel file: `data/FLPP_All_Data_Merged.xlsx`
- Access to all documentation files in `dashboards/documentation/`

## Implementation Steps

### Step 1: Prepare Data Source

1. Ensure the Excel file is located at: `data/FLPP_All_Data_Merged.xlsx`
2. Verify all sheets are present:
   - Completed Services
   - Sales by Tech
   - Lost Sales
   - Customer Detail
   - Tech Reviews
   - Customer Reviews
   - Top Rep Index
   - Financials

### Step 2: Create Power BI File

1. Open Power BI Desktop
2. Create a new report file
3. Save as: `FLPP_Performance_Dashboard.pbix` in the `dashboards/` folder

### Step 3: Import Data Using Power Query

1. **Get Data → Excel Workbook**
   - Navigate to `data/FLPP_All_Data_Merged.xlsx`
   - Select all sheets

2. **For Each Sheet, Apply Transformations:**

   **Completed Services:**
   - Promote headers
   - Remove columns: Unnamed: 10, 11, 12
   - Clean currency strings (Appt Amount, Invoice Amount)
   - Convert to proper data types
   - Trim text fields

   **Sales by Tech:**
   - Promote headers
   - Clean currency strings (Init Price, Reg Price, Contract Value)
   - Convert Customer Id to number
   - Trim text fields

   **Lost Sales:**
   - Promote headers
   - Remove empty columns
   - Verify data types

   **Customer Detail:**
   - Skip first row (header row)
   - Promote headers
   - Convert Auto Pay to boolean
   - Select relevant columns only

   **Tech Reviews:**
   - Skip first row
   - Promote headers
   - Standardize technician names

   **Customer Reviews:**
   - Skip first row
   - Promote headers
   - Verify date formats

   **Top Rep Index:**
   - Skip first row
   - Promote headers
   - Standardize sales rep names

   **Financials:**
   - Parse P&L structure (adjust based on actual format)
   - Create proper date/month columns

3. **Create Date Table:**
   - Use DAX: `Date = CALENDAR(MIN(CompletedServices[Service Date]), MAX(CompletedServices[Service Date]) + 365)`
   - Add calculated columns: Year, Quarter, Month, Month Name, etc.
   - Mark as Date Table

4. **Load Data:**
   - Click "Close & Apply"
   - Wait for data to load

### Step 4: Create Data Model Relationships

1. **Go to Model View** (left sidebar icon)

2. **Create Relationships:**

   - Customer Detail[Customer Id] → Completed Services[Customer Id] (1:*)
   - Customer Detail[Customer Id] → Sales by Tech[Customer Id] (1:*)
   - Customer Detail[Customer Id] → Customer Reviews[Customer Id] (1:*)
   - Completed Services[Tech Name] → Tech Reviews[Technician] (*:1)
   - Sales by Tech[Primary Sales Rep] → Top Rep Index[Sales Rep] (*:1)
   - Date[Date] → Completed Services[Service Date] (1:*)
   - Date[Date] → Sales by Tech[Sold Date] (1:*)
   - Date[Date] → Lost Sales[Sold Date] (1:*)
   - Date[Date] → Customer Reviews[Service Date] (1:*)
   - Date[Date] → Customer Reviews[Review Date] (1:*)

3. **Configure Relationships:**
   - Set cross-filter direction (typically Single for Date → Facts, Both for Customer → Facts)
   - Verify cardinality

4. **Mark Date Table:**
   - Right-click Date table → Mark as Date Table
   - Select Date column

### Step 5: Create DAX Measures

1. **Open DAX Editor** (Model view → New Measure)

2. **Copy measures from `dashboards/dax/02_DAX_Measures.dax`**

3. **Create measures in this order:**

   **Base Measures:**
   - Total Sales
   - Total Revenue
   - YTD Actual

   **Sales & Growth:**
   - Monthly Sales per Rep
   - Recurring Sales %
   - Organic Growth YoY
   - Cancellation Rate

   **Technician Performance:**
   - Completion Rate
   - Tech Review Score
   - Recurring Service Ratio
   - Service Accuracy / Callback Rate

   **Financial Metrics:**
   - Payroll % of Revenue
   - Chemical Spend %
   - EBITDA Margin
   - Revenue Growth YoY

   **Customer & Payment:**
   - Auto Pay Enrollment %
   - Avg Customer Review

   **Fleet & Safety:**
   - Total YTD Revenue
   - Avg Monthly Production per Tech

   **Status Measures:**
   - Sales Status
   - Tech Review Status
   - Auto Pay Status
   - EBITDA Status

4. **Test Each Measure:**
   - Verify calculations return expected values
   - Check for errors
   - Test with different filter contexts

### Step 6: Create KPI Targets Table

1. **Create New Table:**
   - Home → Enter Data
   - Create table with columns:
     - KPI Category
     - KPI Name
     - Target Value
     - Unit
     - Last Updated

2. **Enter Target Values:**
   - Use values from `04_KPI_Reference_Table.md`
   - Update as needed

3. **Create Relationships:**
   - Link to measures as needed (optional, for dynamic targets)

### Step 7: Build Dashboard Pages

#### Page 1: Main Dashboard (KPI Scorecard)

1. **Create Page:**
   - Right-click page → Rename to "Main Dashboard"

2. **Add Header:**
   - Insert → Text Box
   - Text: "FLPP Performance Dashboard"
   - Format: Large, bold, blue

3. **Add Slicers:**
   - Insert → Slicer
   - Add: Month, Branch, Sales Rep, Technician, Category
   - Format consistently

4. **Create KPI Cards:**
   - Insert → Card visual
   - Add measure (e.g., Monthly Sales per Rep)
   - Format:
     - Show value, target, % to target
     - Add conditional formatting for status
   - Repeat for all KPIs

5. **Organize Layout:**
   - Group by category (Sales, Technician, Financial, etc.)
   - Use grid layout
   - Add section headers

#### Page 2: Sales & Growth Detail

1. **Create Page:**
   - Rename to "Sales & Growth"

2. **Add Visuals:**
   - Monthly Sales per Rep (Clustered Column Chart)
   - Recurring Sales % (Donut Chart)
   - Organic Growth YoY (Line Chart)
   - Lost Sales Table

3. **Add Slicers:**
   - Month, Branch, Sales Rep, Category

4. **Configure Drill-down:**
   - Right-click visual → Drill-down
   - Set hierarchy: Sales Rep → Customer → Service Detail

#### Page 3: Technician Performance Detail

1. **Create Page:**
   - Rename to "Technician Performance"

2. **Add Visuals:**
   - Completion Rate Trend (Line Chart)
   - Tech Review Score (Bar Chart)
   - Recurring Service Ratio (Pie Chart)
   - Service Accuracy (Gauge)
   - Completed Services Table

3. **Add Slicers:**
   - Month, Branch, Technician, Category

#### Page 4: Financial Metrics Detail

1. **Create Page:**
   - Rename to "Financial Metrics"

2. **Add Visuals:**
   - Payroll % of Revenue (Gauge)
   - Chemical Spend % (Gauge)
   - EBITDA Margin Trend (Line Chart)
   - Revenue Growth YoY (Line Chart)
   - Monthly P&L Table

3. **Add Slicers:**
   - Month, Branch, Year

#### Page 5: Customer & Payment Detail

1. **Create Page:**
   - Rename to "Customer & Payment"

2. **Add Visuals:**
   - Auto Pay Enrollment (Donut Chart)
   - Avg Customer Review (Card + Bar Chart)
   - Customer Review Trend
   - Customer Reviews Table

3. **Add Slicers:**
   - Month, Branch, Account Type, Payment Type

#### Page 6: Data Explorer

1. **Create Page:**
   - Rename to "Data Explorer"

2. **Add Tables:**
   - Completed Services Detail
   - Sales by Tech Detail
   - Customer Detail
   - All fact tables

3. **Make Exportable:**
   - Enable export functionality
   - Format for readability

### Step 8: Apply Design Theme

1. **Set Color Palette:**
   - View → Themes → Customize current theme
   - Primary: #0078D4
   - Success: #00B050
   - Warning: #FFC000
   - Error: #FF0000

2. **Apply Consistent Formatting:**
   - Font: Segoe UI
   - Card backgrounds: White
   - Borders: Subtle gray
   - Spacing: Consistent padding

3. **Add Conditional Formatting:**
   - KPI cards: Traffic light colors based on status
   - Tables: Color-code based on thresholds

### Step 9: Configure Drill-Through

1. **Create Drill-Through Pages:**
   - Sales Rep Detail
   - Technician Detail
   - Customer Detail

2. **Set Up Drill-Through:**
   - Right-click visual → Drill-through
   - Select target page
   - Configure fields to pass

### Step 10: Test and Validate

1. **Test All Visuals:**
   - Verify data displays correctly
   - Check calculations
   - Test filters and slicers

2. **Test Navigation:**
   - Verify drill-down works
   - Test drill-through pages
   - Check breadcrumbs

3. **Performance Testing:**
   - Check load times
   - Test with full dataset
   - Optimize if needed

4. **User Acceptance:**
   - Share with stakeholders
   - Gather feedback
   - Make adjustments

### Step 11: Publish and Deploy

1. **Publish to Power BI Service:**
   - File → Publish
   - Select workspace
   - Wait for upload

2. **Configure Data Refresh:**
   - Set up data source credentials
   - Configure refresh schedule
   - Test refresh

3. **Share Dashboard:**
   - Add users/groups
   - Set permissions
   - Share links if needed

## Troubleshooting

### Common Issues

1. **Data Not Loading:**
   - Check file path
   - Verify Excel file structure
   - Review Power Query errors

2. **Measures Returning Errors:**
   - Check relationships exist
   - Verify measure syntax
   - Test with sample data

3. **Visuals Not Updating:**
   - Refresh data
   - Check filters
   - Verify measure calculations

4. **Performance Issues:**
   - Review large tables
   - Check for unnecessary calculations
   - Consider aggregations

## Next Steps

1. **Schedule Regular Reviews:**
   - Monthly KPI review
   - Quarterly target adjustment
   - Annual comprehensive review

2. **Maintain Documentation:**
   - Update as changes are made
   - Keep data dictionary current
   - Document new measures

3. **User Training:**
   - Create user guide
   - Conduct training sessions
   - Gather feedback

## Support Resources

- **Documentation:** All files in `dashboards/documentation/`
- **DAX Reference:** `dashboards/dax/02_DAX_Measures.dax`
- **Power Query:** `dashboards/power-query/01_Data_Import_Power_Query.pq`
- **KPI Reference:** `dashboards/documentation/04_KPI_Reference_Table.md`

## Checklist

- [ ] Data source prepared
- [ ] Power BI file created
- [ ] Data imported and transformed
- [ ] Relationships created
- [ ] DAX measures created
- [ ] KPI targets table created
- [ ] All dashboard pages built
- [ ] Design theme applied
- [ ] Drill-through configured
- [ ] Testing completed
- [ ] Published to Power BI Service
- [ ] Data refresh configured
- [ ] Shared with users

---

**Last Updated:** 2025-01-16
**Version:** 1.0


