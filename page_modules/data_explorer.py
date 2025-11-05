"""
Data Explorer Page
Detailed data tables with filtering and export
"""

import streamlit as st
import pandas as pd
from src.ui_components import render_filters


def render(kpi_calculator, data_loader):
    """Render the Data Explorer page"""
    
    st.markdown('<div class="main-header">Data Explorer</div>', unsafe_allow_html=True)
    
    # Table selector
    st.sidebar.markdown("### Select Data Table")
    table_options = {
        "Completed Services": "completed_services",
        "Sales by Tech": "sales_by_tech",
        "Lost Sales": "lost_sales",
        "Customer Detail": "customer_detail",
        "Tech Reviews": "tech_reviews",
        "Customer Reviews": "customer_reviews",
        "Top Rep Index": "top_rep_index",
        "Financials": "financials"
    }
    
    selected_table = st.sidebar.selectbox("Choose Table", list(table_options.keys()))
    
    # Get selected table data
    table_name = table_options[selected_table]
    df = data_loader.get_data(table_name)
    
    if df.empty:
        st.warning(f"No data available for {selected_table}")
        return
    
    st.subheader(f"{selected_table} Data")
    
    # Filters
    filters = render_filters(data_loader, location="sidebar")
    
    # Apply filters
    filtered_df = df.copy()
    if filters.get('branch') and 'Branch' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Branch'] == filters['branch']]
    if filters.get('sales_rep'):
        if 'Primary Sales Rep' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Primary Sales Rep'] == filters['sales_rep']]
        elif 'Sales Rep' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Sales Rep'] == filters['sales_rep']]
    if filters.get('technician') and 'Tech Name' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Tech Name'] == filters['technician']]
    if filters.get('category') and 'Category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Category'] == filters['category']]
    
    # Search functionality
    search_cols = st.columns(3)
    with search_cols[0]:
        search_term = st.text_input("Search in data", "")
    
    if search_term:
        # Search across all text columns
        text_cols = filtered_df.select_dtypes(include=['object']).columns
        mask = pd.Series([False] * len(filtered_df))
        for col in text_cols:
            mask |= filtered_df[col].astype(str).str.contains(search_term, case=False, na=False)
        filtered_df = filtered_df[mask]
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(filtered_df))
    with col2:
        st.metric("Total Columns", len(filtered_df.columns))
    with col3:
        if len(df) > 0:
            pct_filtered = (len(filtered_df) / len(df)) * 100
            st.metric("Filtered %", f"{pct_filtered:.1f}%")
    
    st.markdown("---")
    
    # Display data table
    st.dataframe(filtered_df, use_container_width=True, height=600)
    
    # Export functionality
    st.markdown("---")
    st.subheader("Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{table_name}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Show column info
        with st.expander("Column Information"):
            st.write("**Columns:**")
            for col in filtered_df.columns:
                dtype = filtered_df[col].dtype
                non_null = filtered_df[col].notna().sum()
                null_count = filtered_df[col].isna().sum()
                st.write(f"- {col}: {dtype} ({non_null} non-null, {null_count} null)")

