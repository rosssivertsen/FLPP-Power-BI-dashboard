"""
Data Loader Module
Handles loading and preprocessing of Excel data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
import warnings


class DataLoader:
    """Loads and preprocesses data from Excel file"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        
    def clean_currency(self, value):
        """Clean currency string and convert to float"""
        if pd.isna(value) or value == '':
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        # Remove $, commas, and spaces
        cleaned = str(value).replace('$', '').replace(',', '').strip()
        try:
            return float(cleaned)
        except:
            return 0.0
    
    def clean_numeric_id(self, value):
        """Clean and convert to numeric ID"""
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return int(value) if not pd.isna(value) else None
        # Try to extract number from string
        cleaned = str(value).strip()
        try:
            return int(float(cleaned))
        except:
            return None
    
    def load_completed_services(self):
        """Load and clean Completed Services sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Completed Services')
        
        # Remove empty columns
        df = df.dropna(axis=1, how='all')
        
        # Clean currency columns
        if 'Appt Amount' in df.columns:
            df['Appt Amount'] = df['Appt Amount'].apply(self.clean_currency)
        if 'Invoice Amount' in df.columns:
            df['Invoice Amount'] = df['Invoice Amount'].apply(self.clean_currency)
        
        # Clean date column
        if 'Service Date' in df.columns:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df['Service Date'] = pd.to_datetime(df['Service Date'], errors='coerce')
        
        # Clean text columns
        text_cols = ['Branch', 'Category', 'Type', 'Name', 'Customer Name', 'Tech Name']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # Clean Customer Id
        if 'Customer Id' in df.columns:
            df['Customer Id'] = df['Customer Id'].apply(self.clean_numeric_id)
            df = df[df['Customer Id'].notna()]
        
        return df
    
    def load_sales_by_tech(self):
        """Load and clean Sales by Tech sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Sales by Tech')
        
        # Clean currency columns
        currency_cols = ['Init Price', 'Reg Price', 'Contract Value']
        for col in currency_cols:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_currency)
        
        # Clean date column
        if 'Sold Date' in df.columns:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df['Sold Date'] = pd.to_datetime(df['Sold Date'], errors='coerce')
        
        # Clean Customer Id
        if 'Customer Id' in df.columns:
            df['Customer Id'] = df['Customer Id'].apply(self.clean_numeric_id)
            df = df[df['Customer Id'].notna()]
        
        # Clean text columns
        text_cols = ['Customer Name', 'Service Status', 'Category']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def load_lost_sales(self):
        """Load and clean Lost Sales sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Lost Sales')
        
        # Remove empty columns
        df = df.dropna(axis=1, how='all')
        
        # Clean date column
        if 'Sold Date' in df.columns:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df['Sold Date'] = pd.to_datetime(df['Sold Date'], errors='coerce')
        
        # Clean text columns
        text_cols = ['Sales Rep', 'Customer Name', 'Service Category']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def load_customer_detail(self):
        """Load and clean Customer Detail sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Customer Detail')
        
        # First row contains headers - use it
        if df.shape[0] > 0:
            # Get first row as headers
            first_row = df.iloc[0]
            df.columns = first_row.values
            df = df.iloc[1:].reset_index(drop=True)
            
            # Clean Customer Id
            if 'Customer Id' in df.columns:
                df['Customer Id'] = df['Customer Id'].apply(self.clean_numeric_id)
                df = df[df['Customer Id'].notna()]
            
            # Convert Auto Pay to boolean
            if 'Auto Pay' in df.columns:
                df['Auto Pay Flag'] = df['Auto Pay'].astype(str).str.upper().isin(['YES', 'Y', 'TRUE', '1'])
            
            # Clean numeric columns
            numeric_cols = ['Balance', 'Overdue Balance', 'Days Late']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Clean text columns
            text_cols = ['Status', 'Branch', 'Payment Type', 'City', 'State', 'Account Type']
            for col in text_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def load_tech_reviews(self):
        """Load and clean Tech Reviews sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Tech Reviews')
        
        # Skip first row if it's a header
        if df.shape[0] > 0:
            first_row = df.iloc[0]
            if 'Technician' in str(first_row.values):
                df.columns = first_row.values
                df = df.iloc[1:].reset_index(drop=True)
            
            # Clean text columns
            if 'Technician' in df.columns:
                df['Technician'] = df['Technician'].astype(str).str.strip()
            if 'Account Type' in df.columns:
                df['Account Type'] = df['Account Type'].astype(str).str.strip()
            
            # Clean numeric columns
            if 'Average Star Rating' in df.columns:
                df['Average Star Rating'] = pd.to_numeric(df['Average Star Rating'], errors='coerce')
            if 'Total Ratings' in df.columns:
                df['Total Ratings'] = pd.to_numeric(df['Total Ratings'], errors='coerce').fillna(0).astype(int)
        
        return df
    
    def load_customer_reviews(self):
        """Load and clean Customer Reviews sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Customer Reviews')
        
        # Skip first row if it's a header
        if df.shape[0] > 0:
            first_row = df.iloc[0]
            if 'Overall Star Rating' in str(first_row.values):
                df.columns = first_row.values
                df = df.iloc[1:].reset_index(drop=True)
            
            # Clean date columns
            date_cols = ['Service Date', 'Review Date']
            for col in date_cols:
                if col in df.columns:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Clean Customer Id
            if 'Customer Id' in df.columns:
                df['Customer Id'] = df['Customer Id'].apply(self.clean_numeric_id)
                df = df[df['Customer Id'].notna()]
            
            # Clean text columns
            text_cols = ['Technician', 'Service Category', 'Appointment Type', 'Customer', 'Account Type']
            for col in text_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
            
            # Clean numeric columns
            if 'Overall Star Rating' in df.columns:
                df['Overall Star Rating'] = pd.to_numeric(df['Overall Star Rating'], errors='coerce')
            if 'Technician Star Rating' in df.columns:
                df['Technician Star Rating'] = pd.to_numeric(df['Technician Star Rating'], errors='coerce')
        
        return df
    
    def load_top_rep_index(self):
        """Load and clean Top Rep Index sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Top Rep Index')
        
        # Skip first row if it's a header
        if df.shape[0] > 0:
            first_row = df.iloc[0]
            if 'Rank' in str(first_row.values):
                df.columns = first_row.values
                df = df.iloc[1:].reset_index(drop=True)
            
            # Clean text columns
            if 'Sales Rep' in df.columns:
                df['Sales Rep'] = df['Sales Rep'].astype(str).str.strip()
            if 'Sales Office' in df.columns:
                df['Sales Office'] = df['Sales Office'].astype(str).str.strip()
            
            # Clean numeric columns
            numeric_cols = ['Rank', 'Active', 'Auto Pay%', 'Auto Pay Rank', 'Avg Contract Val', 
                          'Avg Cont Val Rank', 'Index', 'Scratch', 'Avg Initial Amt Price',
                          'Avg Regular Amt', 'Avg Contract Length']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def load_financials(self):
        """Load and clean Financials sheet"""
        df = pd.read_excel(self.file_path, sheet_name='Financials')
        
        # Financials structure may vary - basic cleaning
        # Remove header rows
        if df.shape[0] > 0:
            # Look for rows with company name and skip
            df = df[~df.iloc[:, 0].astype(str).str.contains('FL Pest Pros', case=False, na=False)]
        
        return df
    
    def load_all_data(self):
        """Load all sheets"""
        try:
            self.data['completed_services'] = self.load_completed_services()
            self.data['sales_by_tech'] = self.load_sales_by_tech()
            self.data['lost_sales'] = self.load_lost_sales()
            self.data['customer_detail'] = self.load_customer_detail()
            self.data['tech_reviews'] = self.load_tech_reviews()
            self.data['customer_reviews'] = self.load_customer_reviews()
            self.data['top_rep_index'] = self.load_top_rep_index()
            self.data['financials'] = self.load_financials()
            
            # Create date range for date table
            self._create_date_table()
            
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
    
    def _create_date_table(self):
        """Create a date table for time intelligence"""
        # Get date range from completed services
        if 'completed_services' in self.data and 'Service Date' in self.data['completed_services'].columns:
            dates = self.data['completed_services']['Service Date'].dropna()
            if len(dates) > 0:
                min_date = dates.min()
                max_date = dates.max()
                
                # Create date range
                date_range = pd.date_range(start=min_date, end=max_date + pd.Timedelta(days=365), freq='D')
                date_df = pd.DataFrame({'Date': date_range})
                
                # Add date attributes
                date_df['Year'] = date_df['Date'].dt.year
                date_df['Quarter'] = date_df['Date'].dt.quarter
                date_df['Month'] = date_df['Date'].dt.month
                date_df['Month Name'] = date_df['Date'].dt.strftime('%B')
                date_df['Year Month'] = date_df['Date'].dt.strftime('%Y-%m')
                date_df['Day of Week'] = date_df['Date'].dt.day_name()
                date_df['Day of Week Number'] = date_df['Date'].dt.dayofweek
                
                self.data['date_table'] = date_df
    
    def get_data(self, table_name):
        """Get specific data table"""
        return self.data.get(table_name, pd.DataFrame())
    
    def get_all_data(self):
        """Get all loaded data"""
        return self.data

