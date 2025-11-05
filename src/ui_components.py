"""
UI Components Module
Reusable UI components for the dashboard
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_kpi_card(title, value, target, status, pct_to_target, format_type="number"):
    """Render a KPI card with traffic light status"""
    
    # Format value
    if format_type == "currency":
        value_str = f"${value:,.0f}"
        target_str = f"Target: ${target:,.0f}"
    elif format_type == "percentage":
        value_str = f"{value*100:.1f}%"
        target_str = f"Target: {target*100:.1f}%"
    elif format_type == "rating":
        value_str = f"{value:.1f}/5.0"
        target_str = f"Target: {target:.1f}/5.0"
    else:
        value_str = f"{value:,.0f}"
        target_str = f"Target: {target:,.0f}"
    
    # Status color
    status_colors = {
        "Green": "#00B050",
        "Yellow": "#FFC000",
        "Red": "#FF0000",
        "Gray": "#808080"
    }
    status_icons = {
        "Green": "🟢",
        "Yellow": "🟡",
        "Red": "🔴",
        "Gray": "⚪"
    }
    
    color = status_colors.get(status, "#808080")
    icon = status_icons.get(status, "⚪")
    
    # Card HTML
    card_html = f"""
    <div style="
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {color};
        margin-bottom: 1rem;
    ">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 2rem; font-weight: bold; color: {color}; margin-bottom: 0.5rem;">
            {icon} {value_str}
        </div>
        <div style="font-size: 0.8rem; color: #999;">{target_str}</div>
        <div style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
            {pct_to_target*100:.1f}% of target
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def get_filters(data_loader):
    """Get filter options from data"""
    filters = {}
    
    # Branch filter
    branches = []
    for table_name in ['completed_services', 'sales_by_tech', 'customer_detail']:
        df = data_loader.get_data(table_name)
        if 'Branch' in df.columns:
            branches.extend(df['Branch'].dropna().unique().tolist())
    filters['branches'] = sorted(list(set(branches))) if branches else []
    
    # Sales Rep filter
    sales_reps = []
    sales_df = data_loader.get_data('sales_by_tech')
    if 'Primary Sales Rep' in sales_df.columns:
        sales_reps.extend(sales_df['Primary Sales Rep'].dropna().unique().tolist())
    lost_df = data_loader.get_data('lost_sales')
    if 'Sales Rep' in lost_df.columns:
        sales_reps.extend(lost_df['Sales Rep'].dropna().unique().tolist())
    filters['sales_reps'] = sorted(list(set(sales_reps))) if sales_reps else []
    
    # Technician filter
    techs = []
    services_df = data_loader.get_data('completed_services')
    if 'Tech Name' in services_df.columns:
        techs.extend(services_df['Tech Name'].dropna().unique().tolist())
    filters['technicians'] = sorted(list(set(techs))) if techs else []
    
    # Category filter
    categories = []
    for table_name in ['completed_services', 'sales_by_tech']:
        df = data_loader.get_data(table_name)
        if 'Category' in df.columns:
            categories.extend(df['Category'].dropna().unique().tolist())
    filters['categories'] = sorted(list(set(categories))) if categories else []
    
    # Month filter
    months = []
    services_df = data_loader.get_data('completed_services')
    if not services_df.empty and 'Service Date' in services_df.columns:
        try:
            services_df_copy = services_df.copy()
            services_df_copy['Year Month'] = pd.to_datetime(services_df_copy['Service Date'], errors='coerce').dt.to_period('M')
            months = sorted(services_df_copy['Year Month'].dropna().unique().tolist())
        except Exception:
            months = []
    filters['months'] = months
    
    return filters


def render_filters(data_loader, location="sidebar"):
    """Render filter controls"""
    try:
        filter_options = get_filters(data_loader)
    except Exception as e:
        st.warning(f"Error loading filters: {str(e)}")
        filter_options = {'branches': [], 'sales_reps': [], 'technicians': [], 'categories': [], 'months': []}
    
    filters = {}
    
    if location == "sidebar":
        container = st.sidebar
    else:
        # For top location, use regular columns
        cols = st.columns(5)
        col_idx = 0
    
    if location == "sidebar":
        st.sidebar.markdown("### Filters")
        if filter_options['branches']:
            filters['branch'] = st.sidebar.selectbox("Branch", ["All"] + filter_options['branches'])
            if filters['branch'] == "All":
                filters['branch'] = None
        
        if filter_options['sales_reps']:
            filters['sales_rep'] = st.sidebar.selectbox("Sales Rep", ["All"] + filter_options['sales_reps'])
            if filters['sales_rep'] == "All":
                filters['sales_rep'] = None
        
        if filter_options['technicians']:
            filters['technician'] = st.sidebar.selectbox("Technician", ["All"] + filter_options['technicians'])
            if filters['technician'] == "All":
                filters['technician'] = None
        
        if filter_options['categories']:
            filters['category'] = st.sidebar.selectbox("Category", ["All"] + filter_options['categories'])
            if filters['category'] == "All":
                filters['category'] = None
        
        if filter_options['months']:
            filters['month'] = st.sidebar.selectbox("Month", ["All"] + [str(m) for m in filter_options['months']])
            if filters['month'] == "All":
                filters['month'] = None
            else:
                filters['month'] = pd.Period(filters['month'])
    else:
        # Horizontal filters
        if filter_options['branches']:
            filters['branch'] = cols[col_idx].selectbox("Branch", ["All"] + filter_options['branches'])
            if filters['branch'] == "All":
                filters['branch'] = None
            col_idx += 1
        
        if filter_options['sales_reps']:
            filters['sales_rep'] = cols[col_idx].selectbox("Sales Rep", ["All"] + filter_options['sales_reps'])
            if filters['sales_rep'] == "All":
                filters['sales_rep'] = None
            col_idx += 1
        
        if filter_options['technicians']:
            filters['technician'] = cols[col_idx].selectbox("Technician", ["All"] + filter_options['technicians'])
            if filters['technician'] == "All":
                filters['technician'] = None
            col_idx += 1
        
        if filter_options['categories']:
            filters['category'] = cols[col_idx].selectbox("Category", ["All"] + filter_options['categories'])
            if filters['category'] == "All":
                filters['category'] = None
            col_idx += 1
        
        if filter_options['months']:
            filters['month'] = cols[col_idx].selectbox("Month", ["All"] + [str(m) for m in filter_options['months']])
            if filters['month'] == "All":
                filters['month'] = None
            else:
                filters['month'] = pd.Period(filters['month'])
    
    return filters


def create_drilldown_table(df, selected_item, item_column, detail_columns):
    """Create a drill-down table for selected item"""
    if selected_item and item_column in df.columns:
        filtered_df = df[df[item_column] == selected_item]
        if detail_columns:
            display_cols = [col for col in detail_columns if col in filtered_df.columns]
            return filtered_df[display_cols]
    return pd.DataFrame()

