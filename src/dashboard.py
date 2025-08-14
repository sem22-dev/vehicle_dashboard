"""
Main dashboard application - now much cleaner and modular!
"""
import streamlit as st
import pandas as pd
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database import DatabaseManager
from src.data_processor import DataProcessor
from src.components.styles import get_dashboard_styles
from src.components.metrics import MetricsComponent
from src.components.filters import FilterComponent
from src.components.charts import ChartComponent
from src.components.insights import InsightsComponent
from src.utils.growth_calculator import GrowthCalculator

# Configure page
st.set_page_config(
    page_title="Vehicle Registration Analytics Platform",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styles
st.markdown(get_dashboard_styles(), unsafe_allow_html=True)

class VehicleDashboard:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.data_processor = DataProcessor()
        self.growth_calculator = GrowthCalculator()
    
    def load_data(self):
        """Load data from database"""
        try:
            query = """
            SELECT 
                registration_date,
                vehicle_category,
                manufacturer,
                state,
                district,
                SUM(registrations_count) as total_registrations
            FROM vehicle_registrations 
            GROUP BY registration_date, vehicle_category, manufacturer, state, district
            ORDER BY registration_date DESC
            """
            return self.db_manager.fetch_data(query)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def display_header(self):
        """Display dashboard header"""
        st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">🏎️ Vehicle Analytics Platform</h1>
            <p class="dashboard-subtitle">Advanced Registration Insights & Market Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_growth_analysis(self, df_filtered, selected_years):
        """Display comprehensive growth analysis section"""
        if len(selected_years) <= 1:
            st.info("💡 **Select multiple years** in the filter above to unlock comprehensive growth analysis including YoY and QoQ metrics")
            return
        
        st.markdown('<h2 class="section-header">📊 Comprehensive Growth Intelligence</h2>', unsafe_allow_html=True)
        
        # Calculate enhanced growth metrics
        yearly_growth, quarterly_growth, manufacturer_growth = self.growth_calculator.calculate_enhanced_growth_metrics(df_filtered)
        
        # Growth Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["📈 Year-over-Year (YoY)", "📊 Quarter-over-Quarter (QoQ)", "🏭 Manufacturer Growth"])
        
        with tab1:
            self._display_yoy_analysis(yearly_growth)
        
        with tab2:
            self._display_qoq_analysis(quarterly_growth)
        
        with tab3:
            self._display_manufacturer_growth_analysis(manufacturer_growth, df_filtered)
    
    def _display_yoy_analysis(self, yearly_growth):
        """Display YoY growth analysis"""
        st.markdown("### Year-over-Year Growth Analysis")
        
        InsightsComponent.create_growth_explanation_card(
            "Understanding YoY Growth:",
            "Year-over-Year growth compares the same period in consecutive years. Positive values indicate growth, negative values indicate decline. This metric helps identify long-term trends and business cycles."
        )
        
        if not yearly_growth.empty and not yearly_growth['yoy_growth'].isna().all():
            yoy_clean = yearly_growth.dropna(subset=['yoy_growth'])
            if not yoy_clean.empty:
                fig_yoy = ChartComponent.create_enhanced_chart(
                    yoy_clean, 'bar',
                    x='year', y='yoy_growth', color='vehicle_category',
                    title="📈 Year-over-Year Growth Rates by Category",
                    color_discrete_sequence=['#0f766e', '#155e75', '#0891b2'],
                    labels={'yoy_growth': 'YoY Growth (%)', 'year': 'Year'}
                )
                if fig_yoy:
                    fig_yoy.add_hline(y=0, line_dash="dash", line_color="red", 
                                    annotation_text="Break-even Point", annotation_position="top left")
                    st.plotly_chart(fig_yoy, use_container_width=True)
                
                # YoY Summary
                avg_growth = yoy_clean['yoy_growth'].mean()
                if avg_growth > 0:
                    st.success(f"📈 **Average YoY Growth**: +{avg_growth:.1f}% - Market showing positive growth trend")
                else:
                    st.warning(f"📉 **Average YoY Growth**: {avg_growth:.1f}% - Market showing decline trend")
        else:
            st.info("📊 Insufficient data for YoY growth analysis. Need at least 2 years of data.")
    
    def _display_qoq_analysis(self, quarterly_growth):
        """Display QoQ growth analysis"""
        st.markdown("### Quarter-over-Quarter Growth Analysis")
        
        InsightsComponent.create_growth_explanation_card(
            "Understanding QoQ Growth:",
            "Quarter-over-Quarter growth compares consecutive 3-month periods. This metric reveals short-term trends, seasonal patterns, and immediate market responses. It's more sensitive to recent changes than YoY metrics."
        )
        
        if not quarterly_growth.empty and not quarterly_growth['qoq_growth'].isna().all():
            qoq_clean = quarterly_growth.dropna(subset=['qoq_growth'])
            if not qoq_clean.empty:
                fig_qoq = ChartComponent.create_enhanced_chart(
                    qoq_clean, 'line',
                    x='year_quarter', y='qoq_growth', color='vehicle_category',
                    title="📊 Quarter-over-Quarter Growth Trends",
                    color_discrete_sequence=['#0f766e', '#155e75', '#0891b2'],
                    labels={'qoq_growth': 'QoQ Growth (%)', 'year_quarter': 'Quarter'}
                )
                if fig_qoq:
                    fig_qoq.add_hline(y=0, line_dash="dash", line_color="red",
                                    annotation_text="No Growth Line", annotation_position="top left")
                    fig_qoq.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_qoq, use_container_width=True)
                
                # QoQ Insights
                latest_quarter = qoq_clean.iloc[-3:]
                if not latest_quarter.empty:
                    recent_avg = latest_quarter['qoq_growth'].mean()
                    if recent_avg > 5:
                        st.success(f"🚀 **Recent QoQ Trend**: +{recent_avg:.1f}% - Strong quarterly momentum")
                    elif recent_avg > 0:
                        st.info(f"📈 **Recent QoQ Trend**: +{recent_avg:.1f}% - Moderate quarterly growth")
                    else:
                        st.warning(f"📉 **Recent QoQ Trend**: {recent_avg:.1f}% - Quarterly decline observed")
        else:
            st.info("📊 QoQ analysis based on distributed annual data. For precise quarterly analysis, quarterly registration data would be needed.")
    
    def _display_manufacturer_growth_analysis(self, manufacturer_growth, df_filtered):
        """Display manufacturer growth analysis"""
        st.markdown("### Top Manufacturer/Vehicle Type Growth")
        
        InsightsComponent.create_growth_explanation_card(
            "Manufacturer Growth Analysis:",
            "This section shows year-over-year growth for individual vehicle types/manufacturers. It helps identify market winners and losers, emerging trends, and investment opportunities."
        )
        
        if not manufacturer_growth.empty:
            top_manufacturers = df_filtered.groupby('manufacturer')['total_registrations'].sum().sort_values(ascending=False).head(10).index
            mfg_clean = manufacturer_growth[
                (manufacturer_growth['manufacturer'].isin(top_manufacturers)) &
                (manufacturer_growth['yoy_growth'].notna())
            ]
            
            if not mfg_clean.empty:
                latest_year = mfg_clean['year'].max()
                latest_growth = mfg_clean[mfg_clean['year'] == latest_year].sort_values('yoy_growth', ascending=True)
                
                if not latest_growth.empty:
                    fig_mfg = ChartComponent.create_enhanced_chart(
                        latest_growth, 'horizontal_bar',
                        x='yoy_growth', y='manufacturer',
                        title=f"🏭 Top Vehicle Types YoY Growth ({latest_year})",
                        color='yoy_growth',
                        color_continuous_scale=['#dc2626', '#f59e0b', '#10b981'],
                        labels={'yoy_growth': 'YoY Growth (%)', 'manufacturer': 'Vehicle Type'}
                    )
                    if fig_mfg:
                        fig_mfg.add_vline(x=0, line_dash="dash", line_color="black",
                                        annotation_text="Break-even", annotation_position="top")
                        fig_mfg.update_layout(height=500)
                        st.plotly_chart(fig_mfg, use_container_width=True)
                    
                    # Growth winners and losers
                    if len(latest_growth) > 0:
                        winner = latest_growth.iloc[-1]
                        loser = latest_growth.iloc[0]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success(f"🏆 **Growth Winner**: {winner['manufacturer']} (+{winner['yoy_growth']:.1f}%)")
                        with col2:
                            st.error(f"📉 **Needs Attention**: {loser['manufacturer']} ({loser['yoy_growth']:.1f}%)")
    
    def display_data_explorer(self, df_filtered):
        """Display data explorer section"""
        with st.expander("🔍 Data Explorer - Detailed View", expanded=False):
            if not df_filtered.empty:
                st.markdown("### Summary Statistics")
                summary_stats = df_filtered.groupby('vehicle_category')['total_registrations'].agg([
                    'sum', 'mean', 'std', 'min', 'max', 'count'
                ]).round(2)
                st.dataframe(summary_stats, use_container_width=True)
                
                st.markdown("### Complete Dataset")
                display_df = df_filtered.copy()
                display_df['registration_date'] = display_df['registration_date'].dt.strftime('%Y-%m-%d')
                st.dataframe(
                    display_df.sort_values('total_registrations', ascending=False),
                    use_container_width=True
                )
            else:
                st.info("No data available for selected filters")
    
    def run_dashboard(self):
        """Main dashboard function - now much cleaner!"""
        
        # Display header
        self.display_header()
        
        # Load data
        with st.spinner("🔄 Loading market data..."):
            df = self.load_data()
        
        if df.empty:
            st.error("📊 No data available. Please check your database connection.")
            return
        
        # Ensure registration_date is datetime
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        
        # Display filters and get selections
        selected_years, categories, manufacturers = FilterComponent.create_custom_filter_section(df)
        
        # Filter data
        if selected_years:
            df_filtered = df[
                (df['registration_date'].dt.year.isin(selected_years)) &
                (df['vehicle_category'].isin(categories)) &
                (df['manufacturer'].isin(manufacturers))
            ]
        else:
            df_filtered = df[
                (df['vehicle_category'].isin(categories)) &
                (df['manufacturer'].isin(manufacturers))
            ]
        
        if df_filtered.empty:
            st.warning("🔍 No data matches your filters. Try adjusting your selection.")
            return
        
        # Display all sections using modular components
        MetricsComponent.display_kpi_section(df_filtered)
        ChartComponent.display_market_trends_section(df_filtered)
        ChartComponent.display_vehicle_performance_section(df_filtered)
        self.display_growth_analysis(df_filtered, selected_years)
        InsightsComponent.display_insights_section(df_filtered, selected_years)
        self.display_data_explorer(df_filtered)

# Initialize and run dashboard
if __name__ == "__main__":
    dashboard = VehicleDashboard()
    dashboard.run_dashboard()
