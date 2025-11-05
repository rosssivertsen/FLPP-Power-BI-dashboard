"""
Main Dashboard Page
KPI Scorecard with all key metrics
"""

import streamlit as st
from src.ui_components import render_kpi_card, render_filters


def render(kpi_calculator, data_loader):
    """Render the main dashboard page"""
    
    st.markdown('<div class="main-header">FLPP Performance Dashboard</div>', unsafe_allow_html=True)
    
    # Filters
    filters = render_filters(data_loader, location="top")
    
    st.markdown("---")
    
    # Sales & Growth Section
    st.subheader("📈 Sales & Growth")
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
    
    # Technician Performance Section
    st.subheader("🔧 Technician Performance")
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
    
    # Financial Metrics Section
    st.subheader("💰 Financial Metrics")
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
    
    # Customer & Payment Section
    st.subheader("👥 Customer & Payment")
    col1, col2 = st.columns(2)
    
    with col1:
        value, target, status, pct = kpi_calculator.auto_pay_enrollment(filters)
        render_kpi_card("Auto Pay Enrollment", value, target, status, pct, "percentage")
    
    with col2:
        value, target, status, pct = kpi_calculator.avg_customer_review(filters)
        render_kpi_card("Avg Customer Review", value, target, status, pct, "rating")
    
    st.markdown("---")
    
    # Fleet & Safety Section
    st.subheader("🚗 Fleet & Safety")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #00B050;
        ">
            <div style="font-size: 0.9rem; color: #666;">Fleet Safety Grade</div>
            <div style="font-size: 2rem; font-weight: bold; color: #00B050;">🟢 A</div>
            <div style="font-size: 0.8rem; color: #999;">Target: A</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        value, target, status, pct = kpi_calculator.total_ytd_revenue(filters)
        render_kpi_card("Total YTD Revenue", value, target, status, pct, "currency")
    
    with col3:
        value, target, status, pct = kpi_calculator.avg_monthly_production_per_tech(filters)
        render_kpi_card("Avg Monthly Production per Tech", value, target, status, pct, "currency")
    
    with col4:
        value, target, status, pct = kpi_calculator.recurring_sales_pct(filters)
        render_kpi_card("Recurring % of Sales", value, target, status, pct, "percentage")

