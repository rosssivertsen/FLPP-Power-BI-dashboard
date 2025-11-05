"""
Technician Performance Page
Detailed technician metrics with drill-down
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.ui_components import render_kpi_card, render_filters


def render(kpi_calculator, data_loader):
    """Render the Technician Performance page"""
    
    st.markdown('<div class="main-header">Technician Performance Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    filters = render_filters(data_loader, location="top")
    
    st.markdown("---")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        value, target, status, pct = kpi_calculator.completion_rate(filters)
        render_kpi_card("Completion Rate", value, target, status, pct, "percentage")
    
    with col2:
        value, target, status, pct = kpi_calculator.tech_review_score(filters)
        render_kpi_card("Tech Review Score", value, target, status, pct, "rating")
    
    with col3:
        value, target, status, pct = kpi_calculator.recurring_service_ratio(filters)
        render_kpi_card("Recurring Service Ratio", value, target, status, pct, "percentage")
    
    with col4:
        value, target, status, pct = kpi_calculator.service_accuracy(filters)
        render_kpi_card("Service Accuracy", value, target, status, pct, "percentage")
    
    st.markdown("---")
    
    # Visualizations
    services_df = data_loader.get_data('completed_services')
    tech_reviews_df = data_loader.get_data('tech_reviews')
    customer_df = data_loader.get_data('customer_detail')
    
    if not services_df.empty:
        # Apply filters
        filtered_services = services_df.copy()
        if filters.get('branch') and 'Branch' in filtered_services.columns:
            filtered_services = filtered_services[filtered_services['Branch'] == filters['branch']]
        if filters.get('technician') and 'Tech Name' in filtered_services.columns:
            filtered_services = filtered_services[filtered_services['Tech Name'] == filters['technician']]
        if filters.get('category') and 'Category' in filtered_services.columns:
            filtered_services = filtered_services[filtered_services['Category'] == filters['category']]
        
        # Completion Rate Trend
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Completion Rate Trend")
            if 'Service Date' in filtered_services.columns and 'Tech Name' in filtered_services.columns:
                filtered_services['Year Month'] = pd.to_datetime(filtered_services['Service Date']).dt.to_period('M')
                monthly_completions = filtered_services.groupby('Year Month').size().reset_index(name='Completed')
                monthly_completions['Year Month'] = monthly_completions['Year Month'].astype(str)
                
                fig = px.line(
                    monthly_completions,
                    x='Year Month',
                    y='Completed',
                    title="Services Completed Over Time",
                    markers=True,
                    labels={'Completed': 'Number of Services', 'Year Month': 'Month'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Tech Review Score")
            if not tech_reviews_df.empty and 'Technician' in tech_reviews_df.columns:
                tech_reviews_display = tech_reviews_df[['Technician', 'Average Star Rating', 'Total Ratings']].copy()
                tech_reviews_display = tech_reviews_display.sort_values('Average Star Rating', ascending=False)
                
                fig = px.bar(
                    tech_reviews_display.head(20),
                    x='Technician',
                    y='Average Star Rating',
                    title="Technician Review Scores",
                    labels={'Average Star Rating': 'Rating (out of 5)', 'Technician': 'Technician'}
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Drill-down selector
                selected_tech = st.selectbox(
                    "Select Technician to View Details",
                    ["None"] + tech_reviews_display['Technician'].tolist()
                )
                
                if selected_tech != "None":
                    tech_services = filtered_services[filtered_services['Tech Name'] == selected_tech]
                    st.subheader(f"Services for {selected_tech}")
                    display_cols = ['Customer Name', 'Service Date', 'Category', 'Type', 'Invoice Amount']
                    available_cols = [col for col in display_cols if col in tech_services.columns]
                    st.dataframe(tech_services[available_cols].head(20), use_container_width=True)
        
        # Recurring Service Ratio
        st.subheader("Recurring Service Ratio by Technician")
        if 'Tech Name' in filtered_services.columns and 'Customer Id' in filtered_services.columns:
            # Merge with customer detail for auto pay
            if not customer_df.empty and 'Customer Id' in customer_df.columns:
                merged = filtered_services.merge(
                    customer_df[['Customer Id', 'Auto Pay Flag']],
                    on='Customer Id',
                    how='left'
                )
                
                tech_recurring = merged.groupby('Tech Name').agg({
                    'Customer Id': 'nunique',
                    'Auto Pay Flag': lambda x: (x == True).sum()
                }).reset_index()
                tech_recurring.columns = ['Tech Name', 'Total Customers', 'Recurring Customers']
                tech_recurring['Recurring Ratio'] = tech_recurring['Recurring Customers'] / tech_recurring['Total Customers']
                tech_recurring = tech_recurring.sort_values('Recurring Ratio', ascending=False)
                
                fig = px.bar(
                    tech_recurring.head(20),
                    x='Tech Name',
                    y='Recurring Ratio',
                    title="Recurring Service Ratio by Technician",
                    labels={'Recurring Ratio': 'Recurring Ratio (%)', 'Tech Name': 'Technician'}
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Service Accuracy Gauge
        st.subheader("Service Accuracy")
        callback_keywords = ['Callback', 'Call-back']
        callback_mask = (
            filtered_services['Type'].astype(str).str.contains('|'.join(callback_keywords), case=False, na=False) |
            filtered_services['Name'].astype(str).str.contains('|'.join(callback_keywords), case=False, na=False)
        )
        total_services = len(filtered_services)
        callback_services = callback_mask.sum()
        accuracy = (total_services - callback_services) / total_services if total_services > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = accuracy * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Service Accuracy (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 97], 'color': "lightgray"},
                    {'range': [97, 100], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 97
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Completed Services Table
        st.subheader("Completed Services Detail")
        display_cols = ['Tech Name', 'Customer Name', 'Service Date', 'Category', 'Type', 'Invoice Amount']
        available_cols = [col for col in display_cols if col in filtered_services.columns]
        st.dataframe(filtered_services[available_cols].head(100), use_container_width=True)

