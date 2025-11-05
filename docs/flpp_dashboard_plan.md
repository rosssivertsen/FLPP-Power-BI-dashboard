# **FLPP Performance Dashboard – Power BI / Power Query Development Plan**

---

## 💾 **Workbook Evaluation**

| **Tab Name** | **Description** |
|---------------|----------------|
| **Completed Services** | Contains detailed service completion data by technician and customer, including branch, category, service type, service and invoice amounts, and dates. Useful for tracking *technician performance*, *completion rate*, *callbacks*, and *recurring service ratios*. |
| **Sales by Tech** | Tracks individual sales performance for each rep or technician, including customer info, sold date, service category, and contract value. Ideal for *Monthly Sales per Rep*, *Recurring Sales %*, and *Organic Growth* KPIs. |
| **Lost Sales** | Lists unclosed or lost opportunities with sales rep name, customer, and contract value. Helps calculate *Cancellation Rate* and provide insights on *Sales Conversion* or missed revenue opportunities. |
| **Customer Detail** | Appears to be a raw export of customer master data (partially unstructured). Likely includes attributes such as customer type, region, service category, enrollment in auto-pay, etc. Good for *Auto Pay Enrollment* and *Customer Segmentation* analysis. |
| **Tech Reviews** | Summarized technician review data—likely average scores or ratings over time. Directly supports *Tech Review Score* KPI. |
| **Customer Reviews** | Customer feedback dataset with ratings and review text; helps compute *Avg Customer Review Score* and sentiment insights. |
| **Top Rep Index** | Ranking export of top-performing sales representatives, possibly with metrics like sales volume, conversion rate, and recurring % of sales. Useful for *Sales Leaderboards* and *Performance Benchmarks*. |
| **Financials** | Monthly P&L-type summary—contains revenue, payroll, chemical spend, and EBITDA data. Supports *Payroll % of Revenue*, *Chemical % of Revenue*, *EBITDA Margin*, and *Revenue Growth YoY*. |

---

## 🎯 **Dashboard Concept**

A unified **Performance Management Dashboard** built in **Power BI** (or **Excel Power Query**) with **drill-down capability** to underlying detail.

### **Structure**
- **Top Level:** KPI Scorecard (Cards + Traffic Light Status)
- **Second Level:** Category View (Sales, Technicians, Financials, etc.)
- **Third Level:** Data Explorer (record-level filtering by region, tech, customer)

---

## 🧩 **Data Model Design**

| **Table** | **Key Fields** | **Relationships / Purpose** |
|------------|----------------|-----------------------------|
| **Completed Services** | Customer Id, Tech Name, Service Date | Links to *Customer Detail* and *Tech Reviews* for service quality and frequency analysis. |
| **Sales by Tech** | Customer Id, Primary Sales Rep | Links to *Customer Detail* and *Top Rep Index* to analyze sales performance and recurring % of sales. |
| **Lost Sales** | Sales Rep, Customer Name | Joins with *Sales by Tech* for conversion and cancellation analysis. |
| **Financials** | Month, Branch | Used for all profitability, cost, and efficiency metrics. |
| **Customer Reviews** | Customer Id, Review Date | Joins to *Customer Detail* to calculate customer satisfaction and NPS-style metrics. |
| **Tech Reviews** | Tech Name, Review Date | Joins to *Completed Services* to correlate quality with productivity. |
| **Customer Detail** | Customer Id | Central master reference table. |
| **Top Rep Index** | Sales Rep | Used for leaderboard comparisons and % to Target KPIs. |

---

## ⚙️ **Key KPIs & Drilldowns**

### **1. Sales & Growth**

| KPI | Description | Visualization | Drilldown Level |
|------|--------------|----------------|----------------|
| Monthly Sales per Rep | Average or total monthly sales per rep | Clustered Column Chart | Customer and contract level |
| Recurring Sales % | Recurring vs. one-time sales | Donut Chart | Sales by category |
| Organic Growth | Net new sales YoY | Line Chart | Region / branch |
| Cancellation Rate | Lost sales as % of total | KPI Card + Table | Lost Sales table |

---

### **2. Technician Performance**

| KPI | Description | Visualization | Drilldown Level |
|------|--------------|----------------|----------------|
| Completion Rate | Services completed vs. assigned | KPI Card + Line Trend | Completed Services by tech |
| Tech Review Score | Average technician rating | Bar Chart | Individual review comments |
| Recurring Service Ratio | % of recurring customers per tech | Pie Chart | Customer Detail |
| Service Accuracy / Callbacks | % of callback jobs vs. total | Gauge | Completed Services records |

---

### **3. Financial Metrics**

| KPI | Description | Visualization | Drilldown Level |
|------|--------------|----------------|----------------|
| Payroll % of Revenue | Payroll costs / total revenue | Gauge | Monthly financials |
| Chemical Spend % | Chemical costs / total revenue | Gauge | Expense category analysis |
| EBITDA Margin | Operating margin % | KPI Card + Line Trend | Monthly P&L |
| Revenue Growth YoY | Year-over-year growth by month | Line Chart | Branch or service category |

---

### **4. Customer & Payment**

| KPI | Description | Visualization | Drilldown Level |
|------|--------------|----------------|----------------|
| Auto Pay Enrollment | % of customers enrolled | Donut Chart | Customer Detail |
| Avg Customer Review | Average customer review score | Card + Bar Trend | Review comments |

---

### **5. Fleet & Safety**

| KPI | Description | Visualization | Drilldown Level |
|------|--------------|----------------|----------------|
| Fleet Safety Grade | Safety rating (manual or external source) | Card + Color Status | Incident data |
| Total YTD Revenue | Cumulative year-to-date revenue | KPI Card | Monthly trend |
| Avg Monthly Production per Tech | Total service revenue ÷ number of techs | Column Chart | Tech level |
| Recurring % of Sales | Portion of sales from recurring customers | Donut Chart | Sales detail |

---

## 🧮 **Calculated Measures (DAX Examples)**

| **Measure** | **Formula Example** | **Notes** |
|--------------|---------------------|-----------|
| `% to Target` | `DIVIDE([YTD Actual], [Goal / Target], 0)` | Used for all goal-based KPIs |
| `YTD Actual` | `TOTALYTD(SUM(Sales[Contract Value]), 'Date'[Date])` | Used for cumulative performance |
| `Recurring Sales %` | `DIVIDE(SUM(Sales[Recurring Sales]), SUM(Sales[Total Sales]))` | Based on category or type flag |
| `Payroll % of Revenue` | `DIVIDE(SUM(Financials[Payroll]), SUM(Financials[Revenue]))` | Cost efficiency metric |
| `Revenue Growth YoY` | `([Revenue This Year] - [Revenue Last Year]) / [Revenue Last Year]` | Trend measure |

---

## 🦯 **Drill-Down Navigation**

- **Main Dashboard → Category → Detail**
  - Example: Click “Technician Performance” → view *Tech Review Score* → drill into service records for that tech.
- Hierarchy levels:
  - *Region → Branch → Tech → Customer → Service Record*

---

## 🎨 **Design & Usability**

- **KPI Cards:** Traffic light status  
  - Green: ≥ 100% target  
  - Yellow: 90–99% target  
  - Red: < 90% target  
- **Interactive Slicers:** Month, Branch, Sales Rep, Technician, Category  
- **Tooltips:** Show Goal vs. Actual vs. % to Target  
- **Color Palette:** Company brand or clean blues/greens for operational themes  
- **Layout:**  
  1. **Header:** Global filters + company name  
  2. **Main Panel:** KPI cards by category  
  3. **Detail Panel:** Drillthrough data tables and visuals  

---

## 📦 **Deliverables for GPT-5 Codex**

| **Component** | **Description** |
|----------------|----------------|
| **Power Query Setup** | Import and transform data from all tabs (`Completed Services`, `Sales by Tech`, etc.), ensuring date and currency fields are properly typed. |
| **Data Model** | Relationships per above; enforce referential integrity. |
| **Calculated Measures** | DAX definitions for all KPIs and derived metrics. |
| **Visual Layout Template** | Power BI `.PBIT` or JSON visual structure reflecting section hierarchy. |
| **KPI Reference Table** | Define: Category, KPI Name, Goal / Target, YTD Actual, % to Target, Status, Notes / Insights. |
| **Documentation** | Include source-to-visual mapping and measure logic notes. |

---

## 🗂️ **Optional Enhancements**

- **Automated Refresh:** Power BI Gateway or Excel Power Query refresh scheduled weekly.
- **AI Insights:** Use Power BI Q&A or Copilot to query “Why did sales dip in March?”.
- **Drillthrough Pages:** For “Technician Detail” and “Customer Feedback”.
- **PowerPoint Export Template:** Summary slides of KPIs auto-generated from Power BI.

---

## 📘 **Summary**

This plan establishes a structured, drillable **Performance Dashboard** connecting **sales**, **technician performance**, **financial efficiency**, and **customer satisfaction** into one Power BI model.  
It balances **executive visibility** with **operational insight** — enabling leadership to track goal alignment, identify underperformance early, and make data-driven course corrections.

