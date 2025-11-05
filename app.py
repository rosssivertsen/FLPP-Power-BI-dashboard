"""
FLPP Performance Dashboard - Streamlit Web Application
Main entry point for the dashboard
"""

import streamlit as st
import sys
import os

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import DataLoader
from src.kpi_calculator import KPICalculator
import page_modules.main_dashboard as main_dashboard
import page_modules.sales_growth as sales_growth
import page_modules.technician_performance as technician_performance
import page_modules.financial_metrics as financial_metrics
import page_modules.customer_payment as customer_payment
import page_modules.data_explorer as data_explorer

# Page configuration
st.set_page_config(
    page_title="FLPP Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = None
if 'kpi_calculator' not in st.session_state:
    st.session_state.kpi_calculator = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0078D4;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #0078D4;
    }
    .status-green {
        color: #00B050;
        font-weight: bold;
    }
    .status-yellow {
        color: #FFC000;
        font-weight: bold;
    }
    .status-red {
        color: #FF0000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📊 FLPP Dashboard")
    st.markdown("---")
    
    # Data loading
    if not st.session_state.data_loaded:
        st.info("📁 Load data to begin")
        if st.button("Load Data", type="primary"):
            with st.spinner("Loading data..."):
                try:
                    data_loader = DataLoader("data/FLPP_All_Data_Merged.xlsx")
                    data_loader.load_all_data()
                    st.session_state.data_loader = data_loader
                    st.session_state.kpi_calculator = KPICalculator(data_loader)
                    st.session_state.data_loaded = True
                    st.success("Data loaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
    else:
        st.success("✅ Data loaded")
        if st.button("Reload Data"):
            st.session_state.data_loaded = False
            st.session_state.data_loader = None
            st.session_state.kpi_calculator = None
            st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.subheader("Navigation")
    page = st.radio(
        "Select Page",
        [
            "🏠 Main Dashboard",
            "📈 Sales & Growth",
            "🔧 Technician Performance",
            "💰 Financial Metrics",
            "👥 Customer & Payment",
            "📋 Data Explorer"
        ]
    )

# Main content area
if not st.session_state.data_loaded:
    st.markdown('<div class="main-header">FLPP Performance Dashboard</div>', unsafe_allow_html=True)
    st.info("👈 Please load data from the sidebar to begin")
    st.markdown("""
    ### Welcome to the FLPP Performance Dashboard
    
    This dashboard provides comprehensive insights into:
    - Sales & Growth metrics
    - Technician Performance
    - Financial Metrics
    - Customer Satisfaction
    - Fleet & Safety
    
    **Getting Started:**
    1. Click "Load Data" in the sidebar
    2. Wait for data to process
    3. Navigate through the different pages
    """)
else:
    # Route to appropriate page
    try:
        if page == "🏠 Main Dashboard":
            main_dashboard.render(st.session_state.kpi_calculator, st.session_state.data_loader)
        elif page == "📈 Sales & Growth":
            sales_growth.render(st.session_state.kpi_calculator, st.session_state.data_loader)
        elif page == "🔧 Technician Performance":
            technician_performance.render(st.session_state.kpi_calculator, st.session_state.data_loader)
        elif page == "💰 Financial Metrics":
            financial_metrics.render(st.session_state.kpi_calculator, st.session_state.data_loader)
        elif page == "👥 Customer & Payment":
            customer_payment.render(st.session_state.kpi_calculator, st.session_state.data_loader)
        elif page == "📋 Data Explorer":
            data_explorer.render(st.session_state.kpi_calculator, st.session_state.data_loader)
    except Exception as e:
        st.error(f"Error rendering page: {str(e)}")
        st.exception(e)

