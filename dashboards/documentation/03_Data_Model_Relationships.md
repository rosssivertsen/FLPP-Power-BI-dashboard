# FLPP Power BI Dashboard - Data Model Relationships

## Overview

This document describes the data model relationships for the FLPP Power BI Dashboard. The model follows a star schema design with fact and dimension tables.

## Table Relationships

### Primary Relationships

```
Customer Detail (Dimension)
    ├── Customer Id (Primary Key)
    │
    ├── Completed Services (Fact)
    │   └── Customer Id (Foreign Key) → Many-to-One
    │
    ├── Sales by Tech (Fact)
    │   └── Customer Id (Foreign Key) → Many-to-One
    │
    └── Customer Reviews (Fact)
        └── Customer Id (Foreign Key) → Many-to-One
```

### Relationship Details

#### 1. Customer Detail ↔ Completed Services
- **Type:** One-to-Many (One customer, many services)
- **From:** Customer Detail[Customer Id]
- **To:** Completed Services[Customer Id]
- **Cardinality:** 1:*
- **Cross Filter Direction:** Both
- **Purpose:** Link services to customer details for segmentation and auto-pay analysis

#### 2. Customer Detail ↔ Sales by Tech
- **Type:** One-to-Many (One customer, many sales)
- **From:** Customer Detail[Customer Id]
- **To:** Sales by Tech[Customer Id]
- **Cardinality:** 1:*
- **Cross Filter Direction:** Both
- **Purpose:** Link sales to customer details for recurring sales analysis

#### 3. Customer Detail ↔ Customer Reviews
- **Type:** One-to-Many (One customer, many reviews)
- **From:** Customer Detail[Customer Id]
- **To:** Customer Reviews[Customer Id]
- **Cardinality:** 1:*
- **Cross Filter Direction:** Both
- **Purpose:** Link reviews to customer details for satisfaction analysis

#### 4. Completed Services ↔ Tech Reviews
- **Type:** Many-to-One (Many services, one tech rating)
- **From:** Completed Services[Tech Name]
- **To:** Tech Reviews[Technician]
- **Cardinality:** *:1
- **Cross Filter Direction:** Single (Tech Reviews → Completed Services)
- **Purpose:** Correlate service volume with technician quality ratings

#### 5. Sales by Tech ↔ Top Rep Index
- **Type:** Many-to-One (Many sales, one rep ranking)
- **From:** Sales by Tech[Primary Sales Rep]
- **To:** Top Rep Index[Sales Rep]
- **Cardinality:** *:1
- **Cross Filter Direction:** Single (Top Rep Index → Sales by Tech)
- **Purpose:** Compare sales performance against top rep benchmarks

#### 6. Sales by Tech ↔ Lost Sales
- **Type:** Many-to-Many (via Sales Rep)
- **From:** Sales by Tech[Primary Sales Rep]
- **To:** Lost Sales[Sales Rep]
- **Cardinality:** *:*
- **Cross Filter Direction:** Both
- **Purpose:** Calculate conversion rates and cancellation analysis

#### 7. Date Table ↔ All Fact Tables
- **Type:** One-to-Many
- **From:** Date[Date]
- **To:** Completed Services[Service Date]
- **To:** Sales by Tech[Sold Date]
- **To:** Lost Sales[Sold Date]
- **To:** Customer Reviews[Service Date]
- **To:** Customer Reviews[Review Date]
- **Cardinality:** 1:*
- **Cross Filter Direction:** Single (Date → Fact Tables)
- **Purpose:** Enable time-based calculations (YTD, YoY, MoM) and filtering

#### 8. Financials ↔ Date Table
- **Type:** Many-to-One (if Financials has Month/Date column)
- **From:** Financials[Month] (or Date column)
- **To:** Date[Date]
- **Cardinality:** *:1
- **Cross Filter Direction:** Both
- **Purpose:** Link financial metrics to time periods

## Relationship Matrix

| From Table | To Table | Relationship Type | Key Field | Notes |
|------------|----------|-------------------|-----------|-------|
| Customer Detail | Completed Services | 1:* | Customer Id | Primary relationship |
| Customer Detail | Sales by Tech | 1:* | Customer Id | Primary relationship |
| Customer Detail | Customer Reviews | 1:* | Customer Id | Primary relationship |
| Completed Services | Tech Reviews | *:1 | Tech Name → Technician | Name matching |
| Sales by Tech | Top Rep Index | *:1 | Primary Sales Rep → Sales Rep | Name matching |
| Sales by Tech | Lost Sales | *:* | Primary Sales Rep → Sales Rep | Many-to-many |
| Date | Completed Services | 1:* | Date → Service Date | Time intelligence |
| Date | Sales by Tech | 1:* | Date → Sold Date | Time intelligence |
| Date | Lost Sales | 1:* | Date → Sold Date | Time intelligence |
| Date | Customer Reviews | 1:* | Date → Service Date | Time intelligence |
| Date | Customer Reviews | 1:* | Date → Review Date | Time intelligence |
| Date | Financials | 1:* | Date → Month | Time intelligence |

## Implementation Notes

### 1. Name-Based Relationships
Some relationships (Tech Reviews, Top Rep Index) are based on name matching rather than IDs. Ensure:
- Consistent name formatting (trimmed, standardized)
- Consider creating lookup tables if names are inconsistent
- Use calculated columns or Power Query transformations to standardize names

### 2. Many-to-Many Relationships
The Sales by Tech ↔ Lost Sales relationship is many-to-many. Consider:
- Creating an intermediate bridge table
- Using DAX measures with CROSSFILTER() for accurate calculations
- Testing filter propagation carefully

### 3. Date Table
The Date table is critical for time intelligence:
- Mark as Date Table in Power BI
- Ensure continuous date range covers all fact table dates
- Add calculated columns for fiscal periods if needed

### 4. Inactive Relationships
If multiple date relationships exist (e.g., Service Date and Review Date), mark inactive relationships and use USERELATIONSHIP() in DAX when needed.

## Data Model Diagram (Conceptual)

```
                        ┌─────────────┐
                        │    Date     │
                        │  (Dimension)│
                        └──────┬──────┘
                               │
                               │ 1:*
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        │                      │                      │
┌───────▼────────┐   ┌─────────▼────────┐   ┌────────▼─────────┐
│   Completed    │   │   Sales by Tech  │   │  Customer Reviews│
│   Services     │   │     (Fact)       │   │     (Fact)       │
│    (Fact)      │   └─────────┬────────┘   └────────┬─────────┘
└───────┬────────┘             │                     │
        │                      │                     │
        │ *:1                  │ *:1                 │ *:1
        │                      │                     │
        └──────────┬───────────┴──────────┬──────────┘
                   │                      │
                   │ Customer Id          │
                   │                      │
           ┌───────▼──────────────┐      │
           │   Customer Detail    │◄─────┘
           │    (Dimension)       │
           └──────────────────────┘

        ┌──────────────┐      ┌──────────────┐
        │ Tech Reviews │      │ Top Rep Index│
        │  (Dimension) │      │  (Dimension) │
        └──────┬───────┘      └──────┬───────┘
               │                     │
               │ Tech Name           │ Sales Rep
               │                     │
        ┌──────▼──────────────┐      │
        │  Completed Services │      │
        └─────────────────────┘      │
                                     │
                             ┌───────▼─────────┐
                             │  Sales by Tech  │
                             └─────────────────┘
```

## Relationship Configuration in Power BI

### Steps to Create Relationships:

1. **Open Power BI Desktop**
2. **Go to Model View** (icon on left sidebar)
3. **Drag and drop** to create relationships:
   - Drag `Customer Id` from Customer Detail to Completed Services
   - Drag `Customer Id` from Customer Detail to Sales by Tech
   - Drag `Customer Id` from Customer Detail to Customer Reviews
   - Drag `Tech Name` from Completed Services to `Technician` in Tech Reviews
   - Drag `Primary Sales Rep` from Sales by Tech to `Sales Rep` in Top Rep Index
   - Drag `Date` from Date table to date columns in fact tables

4. **Configure each relationship:**
   - Right-click → Edit Relationship
   - Verify cardinality (1:* or *:1)
   - Set cross-filter direction
   - Enable/disable referential integrity as needed

5. **Mark Date Table:**
   - Right-click Date table → Mark as Date Table
   - Select Date column

## Best Practices

1. **Avoid Circular Dependencies:** Ensure filter propagation is logical and doesn't create circular references
2. **Use Single Direction Filters:** For dimension-to-fact relationships, typically use single direction (dimension → fact)
3. **Test Filter Behavior:** Verify that slicers and filters work as expected across all visuals
4. **Optimize Performance:** 
   - Use integer keys where possible (faster than text)
   - Minimize many-to-many relationships
   - Consider materializing calculated columns instead of measures for frequently used filters

## Troubleshooting

### Common Issues:

1. **Relationship not working:**
   - Check data types match (number vs text)
   - Verify no null values in key columns
   - Ensure names/values are exactly matching

2. **Filters not propagating:**
   - Check cross-filter direction
   - Verify cardinality is correct
   - Use DAX CROSSFILTER() if needed

3. **Performance issues:**
   - Review relationship cardinality (many-to-many can be slow)
   - Consider materializing relationships with calculated columns
   - Use DirectQuery vs Import mode appropriately


