"""
Financial Metrics Page
Financial performance metrics with drill-down
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.ui_components import render_kpi_card, render_filters


def render(kpi_calculator, data_loader):
    """Render the Financial Metrics page"""
    
    st.markdown('<div class="main-header">Financial Metrics Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    filters = render_filters(data_loader, location="top")
    
    st.markdown("---")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        value, target, status, pct = kpi_calculator.payroll_pct_revenue(filters)
        render_kpi_card("Payroll % of Revenue", value, target, status, pct, "percentage")
    
    with col2:
        value, target, status, pct = kpi_calculator.chemical_spend_pct(filters)
        render_kpi_card("Chemical Spend %", value, target, status, pct, "percentage")
    
    with col3:
        value, target, status, pct = kpi_calculator.ebitda_margin(filters)
        render_kpi_card("EBITDA Margin", value, target, status, pct, "percentage")
    
    with col4:
        value, target, status, pct = kpi_calculator.revenue_growth_yoy(filters)
        render_kpi_card("Revenue Growth YoY", value, target, status, pct, "percentage")
    
    st.markdown("---")
    
    # Calculate revenue from completed services
    services_df = data_loader.get_data('completed_services')
    
    if not services_df.empty and 'Invoice Amount' in services_df.columns:
        # Apply filters
        filtered_services = services_df.copy()
        if filters.get('branch') and 'Branch' in filtered_services.columns:
            filtered_services = filtered_services[filtered_services['Branch'] == filters['branch']]
        
        # Payroll % Gauge
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Payroll % of Revenue")
            payroll_pct = 38.0  # Placeholder - would come from Financials table
            target = 40.0
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = payroll_pct,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Payroll % of Revenue"},
                gauge = {
                    'axis': {'range': [None, 50]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 45], 'color': "yellow"},
                        {'range': [45, 50], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 40
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Chemical Spend % of Revenue")
            chemical_pct = 7.2  # Placeholder
            target = 8.0
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = chemical_pct,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Chemical Spend % of Revenue"},
                gauge = {
                    'axis': {'range': [None, 15]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 8], 'color': "lightgreen"},
                        {'range': [8, 10], 'color': "yellow"},
                        {'range': [10, 15], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 8
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # EBITDA Margin Trend
        st.subheader("EBITDA Margin Trend")
        if 'Service Date' in filtered_services.columns:
            filtered_services['Year Month'] = pd.to_datetime(filtered_services['Service Date']).dt.to_period('M')
            monthly_revenue = filtered_services.groupby('Year Month')['Invoice Amount'].sum().reset_index()
            monthly_revenue['Year Month'] = monthly_revenue['Year Month'].astype(str)
            
            # Placeholder EBITDA calculation (would come from Financials)
            monthly_revenue['EBITDA'] = monthly_revenue['Invoice Amount'] * 0.22  # 22% margin
            monthly_revenue['EBITDA Margin'] = (monthly_revenue['EBITDA'] / monthly_revenue['Invoice Amount']) * 100
            
            fig = px.line(
                monthly_revenue,
                x='Year Month',
                y='EBITDA Margin',
                title="EBITDA Margin Over Time",
                markers=True,
                labels={'EBITDA Margin': 'EBITDA Margin (%)', 'Year Month': 'Month'}
            )
            fig.add_hline(y=20, line_dash="dash", line_color="green", annotation_text="Target: 20%")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Revenue Growth YoY
        st.subheader("Revenue Growth YoY")
        if 'Service Date' in filtered_services.columns:
            filtered_services['Year'] = pd.to_datetime(filtered_services['Service Date']).dt.year
            yearly_revenue = filtered_services.groupby('Year')['Invoice Amount'].sum().reset_index()
            yearly_revenue = yearly_revenue.sort_values('Year')
            
            fig = px.line(
                yearly_revenue,
                x='Year',
                y='Invoice Amount',
                title="Year-over-Year Revenue Growth",
                markers=True,
                labels={'Invoice Amount': 'Revenue ($)', 'Year': 'Year'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate growth rate
            if len(yearly_revenue) >= 2:
                current_year = yearly_revenue.iloc[-1]['Invoice Amount']
                previous_year = yearly_revenue.iloc[-2]['Invoice Amount']
                growth_rate = ((current_year - previous_year) / previous_year) * 100 if previous_year > 0 else 0
                st.metric("YoY Growth Rate", f"{growth_rate:.1f}%")

