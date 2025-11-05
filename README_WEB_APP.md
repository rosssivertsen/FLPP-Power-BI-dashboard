# FLPP Performance Dashboard - Web Application

## Overview

This is a Streamlit-based web application that provides an interactive dashboard for FLPP performance metrics. The application replaces the Power BI dashboard with a fully functional web-based visualization tool with drill-down capabilities.

## Features

- **Interactive Dashboard**: Real-time KPI visualization with traffic light status indicators
- **Drill-Down Functionality**: Click through from high-level metrics to detailed data
- **Multiple Pages**: 
  - Main Dashboard (KPI Scorecard)
  - Sales & Growth
  - Technician Performance
  - Financial Metrics
  - Customer & Payment
  - Data Explorer
- **Interactive Filters**: Filter by Branch, Sales Rep, Technician, Category, and Month
- **Export Capabilities**: Download filtered data as CSV
- **Responsive Design**: Works on desktop and tablet devices

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/rosssivertsen/FLPP-Power-BI-dashboard.git
   cd PowerBI-FLPP-Test
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data file location**:
   - Ensure `data/FLPP_All_Data_Merged.xlsx` exists
   - The file should contain all required sheets (see data structure below)

## Running the Application

### Start the Dashboard

```bash
streamlit run app.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`

### Access from Network

To allow access from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other devices using your computer's IP address: `http://YOUR_IP:8501`

## Usage

### Getting Started

1. **Load Data**: 
   - Click "Load Data" in the sidebar
   - Wait for data processing to complete
   - You'll see a success message when ready

2. **Navigate Pages**:
   - Use the radio buttons in the sidebar to switch between pages
   - Each page focuses on a specific category of metrics

3. **Apply Filters**:
   - Use the filter controls at the top of each page
   - Filters apply to all visualizations on that page
   - Select "All" to clear a filter

4. **Drill Down**:
   - Click on charts or select items from dropdown menus
   - View detailed data tables for selected items
   - Export data as needed

### Pages Overview

#### Main Dashboard
- Overview of all KPIs with traffic light status
- Quick view of performance across all categories
- Status indicators: 🟢 Green (On Target), 🟡 Yellow (At Risk), 🔴 Red (Below Target)

#### Sales & Growth
- Monthly sales per rep visualization
- Recurring vs one-time sales breakdown
- Year-over-year growth trends
- Lost sales detail table
- Drill-down to individual rep and customer level

#### Technician Performance
- Completion rate trends
- Tech review scores
- Recurring service ratios
- Service accuracy metrics
- Drill-down to individual technician service records

#### Financial Metrics
- Payroll and chemical spend percentages
- EBITDA margin trends
- Revenue growth year-over-year
- Gauge charts for cost efficiency metrics

#### Customer & Payment
- Auto pay enrollment distribution
- Customer review trends
- Review detail table with search
- Customer detail table

#### Data Explorer
- Access to all raw data tables
- Advanced filtering and search
- Export to CSV functionality
- Column information and statistics

## Data Structure

The application expects an Excel file with the following sheets:

1. **Completed Services** - Service completion data
2. **Sales by Tech** - Sales performance data
3. **Lost Sales** - Lost opportunity data
4. **Customer Detail** - Customer master data
5. **Tech Reviews** - Technician review scores
6. **Customer Reviews** - Customer feedback
7. **Top Rep Index** - Sales rep rankings
8. **Financials** - Financial P&L data

## KPI Targets

The application uses predefined targets for each KPI:

- **Monthly Sales per Rep**: $50,000
- **Recurring Sales %**: 60%
- **Organic Growth YoY**: 15%
- **Cancellation Rate**: <5%
- **Completion Rate**: 95%
- **Tech Review Score**: 4.5/5.0
- **Recurring Service Ratio**: 70%
- **Service Accuracy**: 97%
- **Payroll % of Revenue**: <40%
- **Chemical Spend %**: <8%
- **EBITDA Margin**: 20%
- **Auto Pay Enrollment**: 80%
- **Avg Customer Review**: 4.5/5.0
- **Total YTD Revenue**: $10M
- **Avg Monthly Production per Tech**: $15,000

## Troubleshooting

### Data Not Loading

- **Check file path**: Ensure `data/FLPP_All_Data_Merged.xlsx` exists
- **Check file format**: Verify Excel file is not corrupted
- **Check sheet names**: Ensure all required sheets are present
- **Check console**: Look for error messages in the terminal

### Performance Issues

- **Large datasets**: Consider filtering data before loading
- **Memory issues**: Close other applications to free up memory
- **Slow rendering**: Use filters to reduce data size

### Visualizations Not Displaying

- **Check data**: Ensure data is loaded successfully
- **Check filters**: Verify filters aren't excluding all data
- **Check browser**: Try refreshing the page or using a different browser

## Development

### Project Structure

```
.
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── src/
│   ├── data_loader.py       # Data loading and preprocessing
│   ├── kpi_calculator.py    # KPI calculation logic
│   └── ui_components.py     # Reusable UI components
├── pages/
│   ├── main_dashboard.py    # Main KPI scorecard
│   ├── sales_growth.py      # Sales metrics page
│   ├── technician_performance.py  # Tech metrics page
│   ├── financial_metrics.py # Financial metrics page
│   ├── customer_payment.py  # Customer metrics page
│   └── data_explorer.py     # Data exploration page
└── data/
    └── FLPP_All_Data_Merged.xlsx  # Source data
```

### Adding New KPIs

1. Add calculation method to `src/kpi_calculator.py`
2. Add target value to `TARGETS` dictionary
3. Add visualization to appropriate page in `pages/`
4. Update main dashboard if needed

### Customizing Targets

Edit the `TARGETS` dictionary in `src/kpi_calculator.py`:

```python
TARGETS = {
    'monthly_sales_per_rep': 50000,  # Update value here
    # ... other targets
}
```

## Deployment

### Local Deployment

Simply run `streamlit run app.py` as described above.

### Cloud Deployment

#### Streamlit Cloud

1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repository
4. Deploy

#### Other Platforms

- **Heroku**: Use Procfile and requirements.txt
- **AWS/GCP/Azure**: Use container services
- **Docker**: Create Dockerfile and deploy container

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in console
3. Verify data file structure
4. Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)

## License

[Add your license information here]

