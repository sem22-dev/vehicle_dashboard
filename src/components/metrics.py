"""
Metric card components for the dashboard
"""
import streamlit as st

class MetricsComponent:
    
    @staticmethod
    def create_metric_card(value, label, col):
        """Create custom metric cards"""
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def display_kpi_section(df_filtered):
        """Display the KPI metrics section"""
        st.markdown('<h2 class="section-header">📊 Key Performance Indicators</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_registrations = df_filtered['total_registrations'].sum()
        total_vehicle_types = df_filtered['manufacturer'].nunique()
        total_categories = df_filtered['vehicle_category'].nunique()
        avg_registrations = df_filtered['total_registrations'].mean()
        
        MetricsComponent.create_metric_card(f"{total_registrations:,.0f}", "Total Registrations", col1)
        MetricsComponent.create_metric_card(f"{total_vehicle_types}", "Vehicle Types", col2)
        MetricsComponent.create_metric_card(f"{total_categories}", "Categories", col3)
        MetricsComponent.create_metric_card(f"{avg_registrations:,.0f}", "Avg per Type", col4)
