# FLPP Power BI Dashboard

Power BI dashboard project for FLPP (Financial Leadership Performance Program).

## Overview

This repository contains a comprehensive Power BI Performance Dashboard for FLPP, including all data transformation scripts, DAX measures, and detailed documentation. The dashboard provides executive visibility and operational insights across sales, technician performance, financial metrics, customer satisfaction, and fleet safety.

## Project Structure

```
.
├── README.md                        # This file
├── README_WEB_APP.md               # Web application documentation
├── requirements.txt                 # Python dependencies
├── app.py                          # Streamlit web application entry point
├── .gitignore
├── data/
│   └── FLPP_All_Data_Merged.xlsx    # Source data file
├── src/
│   ├── data_loader.py              # Data loading and preprocessing
│   ├── kpi_calculator.py           # KPI calculation logic
│   └── ui_components.py            # Reusable UI components
├── pages/
│   ├── main_dashboard.py           # Main KPI scorecard page
│   ├── sales_growth.py             # Sales metrics page
│   ├── technician_performance.py   # Tech metrics page
│   ├── financial_metrics.py        # Financial metrics page
│   ├── customer_payment.py         # Customer metrics page
│   └── data_explorer.py            # Data exploration page
├── dashboards/
│   ├── README.md                   # Power BI dashboard documentation
│   ├── power-query/
│   │   └── 01_Data_Import_Power_Query.pq  # Power Query M scripts
│   ├── dax/
│   │   └── 02_DAX_Measures.dax     # All DAX measure definitions
│   └── documentation/
│       ├── 00_Implementation_Guide.md      # Step-by-step implementation
│       ├── 03_Data_Model_Relationships.md  # Data model documentation
│       ├── 04_KPI_Reference_Table.md      # KPI definitions and targets
│       ├── 05_Dashboard_Structure_Layout.md # Layout specifications
│       └── 06_Source_to_Visual_Mapping.md  # Source-to-visual mapping
└── docs/
    └── flpp_dashboard_plan.md       # Original requirements specification
```

## Key Features

- **15+ KPIs** across 5 categories (Sales & Growth, Technician Performance, Financial Metrics, Customer & Payment, Fleet & Safety)
- **Traffic Light Status** indicators (Green/Yellow/Red) for quick performance assessment
- **Drill-Down Capability** from high-level KPIs to detailed data exploration
- **Time Intelligence** with YTD, YoY, and MoM calculations
- **Interactive Filters** for Month, Branch, Sales Rep, Technician, and Category
- **Comprehensive Documentation** for implementation and maintenance

## Getting Started

### Option 1: Web Application (Recommended for Quick Start)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

3. **Access Dashboard:**
   - Open browser to `http://localhost:8501`
   - Click "Load Data" in the sidebar
   - Navigate through pages using sidebar menu

For detailed web app instructions, see [README_WEB_APP.md](README_WEB_APP.md)

### Option 2: Power BI Dashboard

1. **Read the Implementation Guide:**
   - Start with `dashboards/documentation/00_Implementation_Guide.md`
   - This provides step-by-step instructions for building the dashboard

2. **Prepare Your Environment:**
   - Install Power BI Desktop (latest version)
   - Ensure Excel file is located at `data/FLPP_All_Data_Merged.xlsx`

3. **Build the Dashboard:**
   - Follow the implementation guide
   - Use Power Query scripts from `dashboards/power-query/`
   - Copy DAX measures from `dashboards/dax/`

### Documentation Guide

- **Implementation:** `dashboards/documentation/00_Implementation_Guide.md`
- **Data Model:** `dashboards/documentation/03_Data_Model_Relationships.md`
- **KPIs:** `dashboards/documentation/04_KPI_Reference_Table.md`
- **Layout:** `dashboards/documentation/05_Dashboard_Structure_Layout.md`
- **Data Flow:** `dashboards/documentation/06_Source_to_Visual_Mapping.md`

## Dashboard Pages

1. **Main Dashboard** - KPI Scorecard with all key metrics
2. **Sales & Growth** - Sales performance and growth metrics
3. **Technician Performance** - Technician productivity and quality
4. **Financial Metrics** - Profitability and cost efficiency
5. **Customer & Payment** - Customer satisfaction and payment metrics
6. **Data Explorer** - Detailed data tables for analysis

## Requirements

### For Power BI Dashboard
- Power BI Desktop (latest version recommended)
- Excel file: `data/FLPP_All_Data_Merged.xlsx`
- Access to Power BI Service (for publishing and sharing)

### For Web Application
- Python 3.8 or higher
- pip (Python package manager)
- See `requirements.txt` for Python dependencies
- Excel file: `data/FLPP_All_Data_Merged.xlsx`

## Data Source

The dashboard uses data from `FLPP_All_Data_Merged.xlsx` which contains 8 sheets:
- Completed Services
- Sales by Tech
- Lost Sales
- Customer Detail
- Tech Reviews
- Customer Reviews
- Top Rep Index
- Financials

## Contributing

1. Ensure all Power BI files are saved in the `dashboards/` directory
2. Update documentation when making changes
3. Test all measures and visuals before committing
4. Follow the existing code structure and naming conventions

## Maintenance

- **Monthly:** Review KPI performance against targets
- **Quarterly:** Evaluate and adjust target values
- **Annually:** Comprehensive review of all KPIs and targets

## Repository

- **GitHub:** https://github.com/rosssivertsen/FLPP-Power-BI-dashboard
- **Status:** Active Development

## License

[Add your license information here]

