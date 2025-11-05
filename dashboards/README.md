# FLPP Power BI Dashboard

## Overview

This folder contains all components for the FLPP Performance Dashboard, including Power Query scripts, DAX measures, and comprehensive documentation.

## Folder Structure

```
dashboards/
├── README.md                           # This file
├── power-query/
│   └── 01_Data_Import_Power_Query.pq  # Power Query M scripts for data import
├── dax/
│   └── 02_DAX_Measures.dax            # All DAX measure definitions
└── documentation/
    ├── 00_Implementation_Guide.md      # Step-by-step implementation guide
    ├── 03_Data_Model_Relationships.md  # Data model and relationship documentation
    ├── 04_KPI_Reference_Table.md      # KPI definitions, targets, and calculations
    ├── 05_Dashboard_Structure_Layout.md # Dashboard layout and design specifications
    └── 06_Source_to_Visual_Mapping.md  # Complete source-to-visual mapping
```

## Quick Start

1. **Read the Implementation Guide:**
   - Start with `documentation/00_Implementation_Guide.md`
   - Follow the step-by-step instructions

2. **Import Data:**
   - Use Power Query scripts from `power-query/01_Data_Import_Power_Query.pq`
   - Adjust paths and transformations as needed

3. **Create Measures:**
   - Copy DAX measures from `dax/02_DAX_Measures.dax`
   - Paste into Power BI Desktop

4. **Build Dashboard:**
   - Follow layout specifications in `05_Dashboard_Structure_Layout.md`
   - Reference KPI definitions in `04_KPI_Reference_Table.md`

## Documentation Guide

### For Implementation
- **Start Here:** `00_Implementation_Guide.md` - Complete step-by-step guide
- **Data Model:** `03_Data_Model_Relationships.md` - Understand table relationships
- **KPIs:** `04_KPI_Reference_Table.md` - All KPI definitions and targets

### For Development
- **Power Query:** `power-query/01_Data_Import_Power_Query.pq` - Data transformation scripts
- **DAX Measures:** `dax/02_DAX_Measures.dax` - All measure definitions
- **Mapping:** `06_Source_to_Visual_Mapping.md` - Complete data flow documentation

### For Design
- **Layout:** `05_Dashboard_Structure_Layout.md` - Visual layout and design specifications
- **KPIs:** `04_KPI_Reference_Table.md` - KPI visual specifications

## Key Features

- **15+ KPIs** across 5 categories (Sales, Technician, Financial, Customer, Fleet)
- **Traffic Light Status** indicators (Green/Yellow/Red)
- **Drill-Down Capability** from summary to detail
- **Time Intelligence** with YTD, YoY, and MoM calculations
- **Interactive Filters** for Month, Branch, Sales Rep, Technician, Category
- **Comprehensive Documentation** for maintenance and updates

## Data Source

- **File:** `data/FLPP_All_Data_Merged.xlsx`
- **Sheets:** 8 sheets (Completed Services, Sales by Tech, Lost Sales, Customer Detail, Tech Reviews, Customer Reviews, Top Rep Index, Financials)

## Dashboard Pages

1. **Main Dashboard** - KPI Scorecard with all key metrics
2. **Sales & Growth** - Sales performance and growth metrics
3. **Technician Performance** - Technician productivity and quality
4. **Financial Metrics** - Profitability and cost efficiency
5. **Customer & Payment** - Customer satisfaction and payment metrics
6. **Data Explorer** - Detailed data tables for analysis

## Status Indicators

- 🟢 **Green:** On target (≥ 100% of goal)
- 🟡 **Yellow:** At risk (90-99% of goal)
- 🔴 **Red:** Below target (< 90% of goal)

## Maintenance

### Regular Updates

- **Monthly:** Review KPI performance against targets
- **Quarterly:** Evaluate and adjust target values
- **Annually:** Comprehensive review of all KPIs and targets

### Data Refresh

- Configure Power BI Gateway for scheduled refresh
- Update Excel file location if moved
- Verify all data sources are accessible

## Support

For questions or issues:
1. Review the implementation guide
2. Check the source-to-visual mapping document
3. Verify data model relationships
4. Test DAX measures individually

## Version History

- **v1.0** (2025-01-16) - Initial implementation based on specification


