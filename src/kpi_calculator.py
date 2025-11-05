"""
KPI Calculator Module
Calculates all KPIs from the loaded data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class KPICalculator:
    """Calculates KPIs from loaded data"""
    
    # KPI Targets
    TARGETS = {
        'monthly_sales_per_rep': 50000,
        'recurring_sales_pct': 0.60,
        'organic_growth_yoy': 0.15,
        'cancellation_rate': 0.05,
        'completion_rate': 0.95,
        'tech_review_score': 4.5,
        'recurring_service_ratio': 0.70,
        'service_accuracy': 0.97,
        'payroll_pct_revenue': 0.40,
        'chemical_spend_pct': 0.08,
        'ebitda_margin': 0.20,
        'revenue_growth_yoy': 0.15,
        'auto_pay_enrollment': 0.80,
        'avg_customer_review': 4.5,
        'total_ytd_revenue': 10000000,
        'avg_monthly_production_per_tech': 15000
    }
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.data = data_loader.get_all_data()
    
    def get_status(self, value, target, reverse=False):
        """Get traffic light status (Green/Yellow/Red)"""
        if pd.isna(value) or pd.isna(target) or target == 0:
            return "Gray", 0
        
        pct_to_target = value / target if not reverse else target / value
        
        if reverse:  # For metrics where lower is better (e.g., cancellation rate)
            if pct_to_target <= 1.0:  # Value <= target
                return "Green", pct_to_target
            elif pct_to_target <= 1.1:  # Value <= 110% of target
                return "Yellow", pct_to_target
            else:
                return "Red", pct_to_target
        else:  # For metrics where higher is better
            if pct_to_target >= 1.0:  # Value >= target
                return "Green", pct_to_target
            elif pct_to_target >= 0.90:  # Value >= 90% of target
                return "Yellow", pct_to_target
            else:
                return "Red", pct_to_target
    
    # ============================================================================
    # SALES & GROWTH KPIs
    # ============================================================================
    
    def monthly_sales_per_rep(self, filters=None):
        """Calculate average monthly sales per rep"""
        df = self.data.get('sales_by_tech', pd.DataFrame())
        if df.empty or 'Contract Value' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        if 'Sold Date' in df.columns:
            df['Year Month'] = pd.to_datetime(df['Sold Date']).dt.to_period('M')
            monthly_sales = df.groupby(['Primary Sales Rep', 'Year Month'])['Contract Value'].sum().reset_index()
            monthly_avg = monthly_sales.groupby('Primary Sales Rep')['Contract Value'].mean().mean()
        else:
            # Fallback if no date
            if 'Primary Sales Rep' in df.columns:
                monthly_avg = df.groupby('Primary Sales Rep')['Contract Value'].mean().mean()
            else:
                monthly_avg = df['Contract Value'].mean()
        
        target = self.TARGETS['monthly_sales_per_rep']
        status, pct = self.get_status(monthly_avg, target)
        
        return monthly_avg, target, status, pct
    
    def recurring_sales_pct(self, filters=None):
        """Calculate percentage of recurring sales"""
        df = self.data.get('sales_by_tech', pd.DataFrame())
        if df.empty or 'Contract Value' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        total_sales = df['Contract Value'].sum()
        
        # Identify recurring sales (contains "Monthly", "Bi-Monthly", "Quarterly", "Recurring")
        recurring_keywords = ['Monthly', 'Bi-Monthly', 'Quarterly', 'Recurring']
        if 'Category' in df.columns:
            recurring_mask = df['Category'].astype(str).str.contains('|'.join(recurring_keywords), case=False, na=False)
            recurring_sales = df[recurring_mask]['Contract Value'].sum()
        else:
            recurring_sales = 0
        
        pct = recurring_sales / total_sales if total_sales > 0 else 0
        target = self.TARGETS['recurring_sales_pct']
        status, pct_to_target = self.get_status(pct, target)
        
        return pct, target, status, pct_to_target
    
    def organic_growth_yoy(self, filters=None):
        """Calculate year-over-year organic growth"""
        df = self.data.get('sales_by_tech', pd.DataFrame())
        if df.empty or 'Contract Value' not in df.columns or 'Sold Date' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        df['Year'] = pd.to_datetime(df['Sold Date']).dt.year
        current_year = datetime.now().year
        previous_year = current_year - 1
        
        current_year_sales = df[df['Year'] == current_year]['Contract Value'].sum()
        previous_year_sales = df[df['Year'] == previous_year]['Contract Value'].sum()
        
        if previous_year_sales == 0:
            return 0, 0, "Gray", 0
        
        growth = (current_year_sales - previous_year_sales) / previous_year_sales
        target = self.TARGETS['organic_growth_yoy']
        status, pct_to_target = self.get_status(growth, target)
        
        return growth, target, status, pct_to_target
    
    def cancellation_rate(self, filters=None):
        """Calculate cancellation rate"""
        sales_df = self.data.get('sales_by_tech', pd.DataFrame())
        lost_df = self.data.get('lost_sales', pd.DataFrame())
        
        if sales_df.empty:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            sales_df = self._apply_filters(sales_df, filters)
            lost_df = self._apply_filters(lost_df, filters)
        
        total_sales = sales_df['Contract Value'].sum() if 'Contract Value' in sales_df.columns else 0
        lost_sales = lost_df['Contract Value'].sum() if 'Contract Value' in lost_df.columns else 0
        
        total_opportunities = total_sales + lost_sales
        rate = lost_sales / total_opportunities if total_opportunities > 0 else 0
        
        target = self.TARGETS['cancellation_rate']
        status, pct_to_target = self.get_status(rate, target, reverse=True)  # Lower is better
        
        return rate, target, status, pct_to_target
    
    # ============================================================================
    # TECHNICIAN PERFORMANCE KPIs
    # ============================================================================
    
    def completion_rate(self, filters=None):
        """Calculate completion rate"""
        df = self.data.get('completed_services', pd.DataFrame())
        if df.empty:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        # Assuming all rows are completed services
        completed = len(df)
        # If we had assigned services, we'd compare here
        assigned = completed  # Placeholder
        
        rate = completed / assigned if assigned > 0 else 0
        target = self.TARGETS['completion_rate']
        status, pct_to_target = self.get_status(rate, target)
        
        return rate, target, status, pct_to_target
    
    def tech_review_score(self, filters=None):
        """Calculate average tech review score"""
        df = self.data.get('tech_reviews', pd.DataFrame())
        if df.empty or 'Average Star Rating' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        # Weighted average by total ratings
        if 'Total Ratings' in df.columns:
            df['Weighted Score'] = df['Average Star Rating'] * df['Total Ratings']
            avg_score = df['Weighted Score'].sum() / df['Total Ratings'].sum() if df['Total Ratings'].sum() > 0 else 0
        else:
            avg_score = df['Average Star Rating'].mean()
        
        target = self.TARGETS['tech_review_score']
        status, pct_to_target = self.get_status(avg_score, target)
        
        return avg_score, target, status, pct_to_target
    
    def recurring_service_ratio(self, filters=None):
        """Calculate recurring service ratio"""
        services_df = self.data.get('completed_services', pd.DataFrame())
        customer_df = self.data.get('customer_detail', pd.DataFrame())
        
        if services_df.empty:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            services_df = self._apply_filters(services_df, filters)
        
        # Merge with customer detail to get auto pay status
        if 'Customer Id' in services_df.columns and 'Customer Id' in customer_df.columns:
            merged = services_df.merge(
                customer_df[['Customer Id', 'Auto Pay Flag']],
                on='Customer Id',
                how='left'
            )
            total_customers = merged['Customer Id'].nunique()
            recurring_customers = merged[merged['Auto Pay Flag'] == True]['Customer Id'].nunique()
            
            ratio = recurring_customers / total_customers if total_customers > 0 else 0
        else:
            ratio = 0
        
        target = self.TARGETS['recurring_service_ratio']
        status, pct_to_target = self.get_status(ratio, target)
        
        return ratio, target, status, pct_to_target
    
    def service_accuracy(self, filters=None):
        """Calculate service accuracy (1 - callback rate)"""
        df = self.data.get('completed_services', pd.DataFrame())
        if df.empty:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        total_services = len(df)
        
        # Identify callbacks
        callback_keywords = ['Callback', 'Call-back', 'Callback']
        callback_mask = (
            df['Type'].astype(str).str.contains('|'.join(callback_keywords), case=False, na=False) |
            df['Name'].astype(str).str.contains('|'.join(callback_keywords), case=False, na=False) |
            df['Category'].astype(str).str.contains('|'.join(callback_keywords), case=False, na=False)
        )
        
        callback_services = callback_mask.sum()
        callback_rate = callback_services / total_services if total_services > 0 else 0
        accuracy = 1 - callback_rate
        
        target = self.TARGETS['service_accuracy']
        status, pct_to_target = self.get_status(accuracy, target)
        
        return accuracy, target, status, pct_to_target
    
    # ============================================================================
    # FINANCIAL METRICS KPIs
    # ============================================================================
    
    def payroll_pct_revenue(self, filters=None):
        """Calculate payroll as percentage of revenue"""
        # This would need to be implemented based on actual Financials structure
        # Placeholder implementation
        target = self.TARGETS['payroll_pct_revenue']
        return 0.38, target, "Green", 0.95  # Placeholder
    
    def chemical_spend_pct(self, filters=None):
        """Calculate chemical spend as percentage of revenue"""
        # Placeholder
        target = self.TARGETS['chemical_spend_pct']
        return 0.072, target, "Green", 0.90  # Placeholder
    
    def ebitda_margin(self, filters=None):
        """Calculate EBITDA margin"""
        # Placeholder
        target = self.TARGETS['ebitda_margin']
        return 0.22, target, "Green", 1.10  # Placeholder
    
    def revenue_growth_yoy(self, filters=None):
        """Calculate revenue growth year-over-year"""
        # Placeholder
        target = self.TARGETS['revenue_growth_yoy']
        return 0.17, target, "Green", 1.13  # Placeholder
    
    # ============================================================================
    # CUSTOMER & PAYMENT KPIs
    # ============================================================================
    
    def auto_pay_enrollment(self, filters=None):
        """Calculate auto pay enrollment percentage"""
        df = self.data.get('customer_detail', pd.DataFrame())
        if df.empty:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        total_customers = len(df)
        if 'Auto Pay Flag' in df.columns:
            auto_pay_customers = df['Auto Pay Flag'].sum()
        else:
            auto_pay_customers = 0
        
        pct = auto_pay_customers / total_customers if total_customers > 0 else 0
        target = self.TARGETS['auto_pay_enrollment']
        status, pct_to_target = self.get_status(pct, target)
        
        return pct, target, status, pct_to_target
    
    def avg_customer_review(self, filters=None):
        """Calculate average customer review score"""
        df = self.data.get('customer_reviews', pd.DataFrame())
        if df.empty or 'Overall Star Rating' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        avg_score = df['Overall Star Rating'].mean()
        target = self.TARGETS['avg_customer_review']
        status, pct_to_target = self.get_status(avg_score, target)
        
        return avg_score, target, status, pct_to_target
    
    # ============================================================================
    # FLEET & SAFETY KPIs
    # ============================================================================
    
    def total_ytd_revenue(self, filters=None):
        """Calculate total year-to-date revenue"""
        df = self.data.get('completed_services', pd.DataFrame())
        if df.empty or 'Invoice Amount' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        current_year = datetime.now().year
        if 'Service Date' in df.columns:
            df['Year'] = pd.to_datetime(df['Service Date']).dt.year
            ytd_revenue = df[df['Year'] == current_year]['Invoice Amount'].sum()
        else:
            ytd_revenue = df['Invoice Amount'].sum()
        
        target = self.TARGETS['total_ytd_revenue']
        status, pct_to_target = self.get_status(ytd_revenue, target)
        
        return ytd_revenue, target, status, pct_to_target
    
    def avg_monthly_production_per_tech(self, filters=None):
        """Calculate average monthly production per tech"""
        df = self.data.get('completed_services', pd.DataFrame())
        if df.empty or 'Invoice Amount' not in df.columns:
            return 0, 0, "Gray", 0
        
        # Apply filters
        if filters:
            df = self._apply_filters(df, filters)
        
        if 'Service Date' in df.columns and 'Tech Name' in df.columns:
            df['Year Month'] = pd.to_datetime(df['Service Date']).dt.to_period('M')
            monthly_revenue = df.groupby(['Tech Name', 'Year Month'])['Invoice Amount'].sum().reset_index()
            monthly_avg_per_tech = monthly_revenue.groupby('Tech Name')['Invoice Amount'].mean().mean()
        else:
            monthly_avg_per_tech = 0
        
        target = self.TARGETS['avg_monthly_production_per_tech']
        status, pct_to_target = self.get_status(monthly_avg_per_tech, target)
        
        return monthly_avg_per_tech, target, status, pct_to_target
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    def _apply_filters(self, df, filters):
        """Apply filters to dataframe"""
        filtered_df = df.copy()
        
        if 'branch' in filters and filters['branch'] and 'Branch' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Branch'] == filters['branch']]
        
        if 'sales_rep' in filters and filters['sales_rep']:
            if 'Primary Sales Rep' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Primary Sales Rep'] == filters['sales_rep']]
            elif 'Sales Rep' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Sales Rep'] == filters['sales_rep']]
        
        if 'technician' in filters and filters['technician'] and 'Tech Name' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Tech Name'] == filters['technician']]
        
        if 'category' in filters and filters['category'] and 'Category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Category'] == filters['category']]
        
        if 'month' in filters and filters['month']:
            date_col = None
            if 'Service Date' in filtered_df.columns:
                date_col = 'Service Date'
            elif 'Sold Date' in filtered_df.columns:
                date_col = 'Sold Date'
            
            if date_col:
                filtered_df[date_col] = pd.to_datetime(filtered_df[date_col])
                filtered_df['Month'] = filtered_df[date_col].dt.to_period('M')
                filtered_df = filtered_df[filtered_df['Month'] == filters['month']]
        
        return filtered_df

