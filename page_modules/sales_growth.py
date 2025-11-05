"""
Sales & Growth Page
Detailed sales performance metrics with drill-down
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.ui_components import render_kpi_card, render_filters, create_drilldown_table


def render(kpi_calculator, data_loader):
    """Render the Sales & Growth page"""
    
    st.markdown('<div class="main-header">Sales & Growth Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    filters = render_filters(data_loader, location="top")
    
    st.markdown("---")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        value, target, status, pct = kpi_calculator.monthly_sales_per_rep(filters)
        render_kpi_card("Monthly Sales per Rep", value, target, status, pct, "currency")
    
    with col2:
        value, target, status, pct = kpi_calculator.recurring_sales_pct(filters)
        render_kpi_card("Recurring Sales %", value, target, status, pct, "percentage")
    
    with col3:
        value, target, status, pct = kpi_calculator.organic_growth_yoy(filters)
        render_kpi_card("Organic Growth YoY", value, target, status, pct, "percentage")
    
    with col4:
        value, target, status, pct = kpi_calculator.cancellation_rate(filters)
        render_kpi_card("Cancellation Rate", value, target, status, pct, "percentage")
    
    st.markdown("---")
    
    # Visualizations
    sales_df = data_loader.get_data('sales_by_tech')
    
    if not sales_df.empty and 'Contract Value' in sales_df.columns:
        # Apply filters
        filtered_df = sales_df.copy()
        if filters.get('branch') and 'Branch' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Branch'] == filters['branch']]
        if filters.get('sales_rep') and 'Primary Sales Rep' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Primary Sales Rep'] == filters['sales_rep']]
        if filters.get('category') and 'Category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Category'] == filters['category']]
        
        # Monthly Sales per Rep Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Monthly Sales per Rep")
            if 'Primary Sales Rep' in filtered_df.columns and 'Sold Date' in filtered_df.columns:
                filtered_df['Year Month'] = pd.to_datetime(filtered_df['Sold Date']).dt.to_period('M')
                monthly_sales = filtered_df.groupby(['Primary Sales Rep', 'Year Month'])['Contract Value'].sum().reset_index()
                monthly_avg = monthly_sales.groupby('Primary Sales Rep')['Contract Value'].mean().reset_index()
                monthly_avg = monthly_avg.sort_values('Contract Value', ascending=False)
                
                fig = px.bar(
                    monthly_avg,
                    x='Primary Sales Rep',
                    y='Contract Value',
                    title="Average Monthly Sales per Rep",
                    labels={'Contract Value': 'Sales Amount ($)', 'Primary Sales Rep': 'Sales Rep'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Drill-down selector
                selected_rep = st.selectbox(
                    "Select Rep to Drill Down",
                    ["None"] + monthly_avg['Primary Sales Rep'].tolist()
                )
                
                if selected_rep != "None":
                    rep_sales = filtered_df[filtered_df['Primary Sales Rep'] == selected_rep]
                    st.subheader(f"Sales Detail for {selected_rep}")
                    display_cols = ['Customer Name', 'Sold Date', 'Category', 'Contract Value', 'Service Status']
                    available_cols = [col for col in display_cols if col in rep_sales.columns]
                    st.dataframe(rep_sales[available_cols], use_container_width=True)
        
        with col2:
            st.subheader("Recurring Sales %")
            if 'Category' in filtered_df.columns:
                # Categorize as recurring or one-time
                recurring_keywords = ['Monthly', 'Bi-Monthly', 'Quarterly', 'Recurring']
                filtered_df['Sales Type'] = filtered_df['Category'].apply(
                    lambda x: 'Recurring' if any(keyword in str(x) for keyword in recurring_keywords) else 'One-time'
                )
                
                sales_by_type = filtered_df.groupby('Sales Type')['Contract Value'].sum().reset_index()
                
                fig = px.pie(
                    sales_by_type,
                    values='Contract Value',
                    names='Sales Type',
                    title="Recurring vs One-time Sales",
                    color='Sales Type',
                    color_discrete_map={'Recurring': '#00B050', 'One-time': '#FFC000'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Drill-down by category
                category_sales = filtered_df.groupby('Category')['Contract Value'].sum().reset_index()
                category_sales = category_sales.sort_values('Contract Value', ascending=False)
                st.subheader("Sales by Category")
                st.dataframe(category_sales, use_container_width=True)
        
        # Organic Growth Chart
        st.subheader("Organic Growth YoY")
        if 'Sold Date' in filtered_df.columns:
            filtered_df['Year'] = pd.to_datetime(filtered_df['Sold Date']).dt.year
            yearly_sales = filtered_df.groupby('Year')['Contract Value'].sum().reset_index()
            yearly_sales = yearly_sales.sort_values('Year')
            
            fig = px.line(
                yearly_sales,
                x='Year',
                y='Contract Value',
                title="Year-over-Year Sales Growth",
                markers=True,
                labels={'Contract Value': 'Sales Amount ($)', 'Year': 'Year'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Lost Sales Table
        st.subheader("Lost Sales Detail")
        lost_df = data_loader.get_data('lost_sales')
        if not lost_df.empty:
            # Apply filters
            if filters.get('sales_rep') and 'Sales Rep' in lost_df.columns:
                lost_df = lost_df[lost_df['Sales Rep'] == filters['sales_rep']]
            
            display_cols = ['Sales Rep', 'Customer Name', 'Sold Date', 'Service Category', 'Contract Value']
            available_cols = [col for col in display_cols if col in lost_df.columns]
            st.dataframe(lost_df[available_cols], use_container_width=True)

