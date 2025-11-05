"""
Customer & Payment Page
Customer satisfaction and payment metrics
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from src.ui_components import render_kpi_card, render_filters


def render(kpi_calculator, data_loader):
    """Render the Customer & Payment page"""
    
    st.markdown('<div class="main-header">Customer & Payment Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    filters = render_filters(data_loader, location="top")
    
    st.markdown("---")
    
    # KPI Cards
    col1, col2 = st.columns(2)
    
    with col1:
        value, target, status, pct = kpi_calculator.auto_pay_enrollment(filters)
        render_kpi_card("Auto Pay Enrollment", value, target, status, pct, "percentage")
    
    with col2:
        value, target, status, pct = kpi_calculator.avg_customer_review(filters)
        render_kpi_card("Avg Customer Review", value, target, status, pct, "rating")
    
    st.markdown("---")
    
    # Auto Pay Enrollment Chart
    customer_df = data_loader.get_data('customer_detail')
    
    if not customer_df.empty and 'Auto Pay Flag' in customer_df.columns:
        # Apply filters
        filtered_customers = customer_df.copy()
        if filters.get('branch') and 'Branch' in filtered_customers.columns:
            filtered_customers = filtered_customers[filtered_customers['Branch'] == filters['branch']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Auto Pay Enrollment")
            auto_pay_counts = filtered_customers['Auto Pay Flag'].value_counts()
            auto_pay_df = pd.DataFrame({
                'Status': ['Enrolled', 'Not Enrolled'],
                'Count': [auto_pay_counts.get(True, 0), auto_pay_counts.get(False, 0)]
            })
            
            fig = px.pie(
                auto_pay_df,
                values='Count',
                names='Status',
                title="Auto Pay Enrollment Distribution",
                color='Status',
                color_discrete_map={'Enrolled': '#00B050', 'Not Enrolled': '#FFC000'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Customer Review Trend")
            reviews_df = data_loader.get_data('customer_reviews')
            
            if not reviews_df.empty and 'Review Date' in reviews_df.columns and 'Overall Star Rating' in reviews_df.columns:
                # Apply filters
                filtered_reviews = reviews_df.copy()
                
                filtered_reviews['Year Month'] = pd.to_datetime(filtered_reviews['Review Date']).dt.to_period('M')
                monthly_avg = filtered_reviews.groupby('Year Month')['Overall Star Rating'].mean().reset_index()
                monthly_avg['Year Month'] = monthly_avg['Year Month'].astype(str)
                
                fig = px.bar(
                    monthly_avg,
                    x='Year Month',
                    y='Overall Star Rating',
                    title="Average Customer Review Score Over Time",
                    labels={'Overall Star Rating': 'Average Rating', 'Year Month': 'Month'}
                )
                fig.add_hline(y=4.5, line_dash="dash", line_color="green", annotation_text="Target: 4.5")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # Customer Reviews Table
    st.subheader("Customer Reviews Detail")
    reviews_df = data_loader.get_data('customer_reviews')
    
    if not reviews_df.empty:
        # Apply filters
        filtered_reviews = reviews_df.copy()
        
        display_cols = ['Customer', 'Review Date', 'Overall Star Rating', 'Technician Star Rating', 
                       'Comments', 'Service Category', 'Technician']
        available_cols = [col for col in display_cols if col in filtered_reviews.columns]
        
        # Add search functionality
        search_term = st.text_input("Search reviews", "")
        if search_term:
            if 'Comments' in filtered_reviews.columns:
                filtered_reviews = filtered_reviews[
                    filtered_reviews['Comments'].astype(str).str.contains(search_term, case=False, na=False)
                ]
        
        st.dataframe(filtered_reviews[available_cols].head(100), use_container_width=True)
        
        # Customer Detail Table
        st.subheader("Customer Detail")
        if not customer_df.empty:
            display_cols = ['Customer Id', 'Status', 'Branch', 'Auto Pay', 'Payment Type', 
                          'City', 'State', 'Account Type']
            available_cols = [col for col in display_cols if col in customer_df.columns]
            st.dataframe(filtered_customers[available_cols].head(100), use_container_width=True)

