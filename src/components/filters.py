"""
Filter components for the dashboard
"""
import streamlit as st

class FilterComponent:
    
    @staticmethod
    def create_custom_filter_section(df):
        """Create enhanced filter section with card-based design"""
        st.markdown("""
        <div class="filter-section">
            <h3 class="filter-title">🎛️ Advanced Analytics Filters</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create three columns for filter cards
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            st.markdown("""
            <div class="filter-card">
                <div class="filter-card-title">📅 Time Period</div>
            </div>
            """, unsafe_allow_html=True)
            
            available_years = sorted(df['registration_date'].dt.year.unique())
            selected_years = st.multiselect(
                "Select Years",
                options=available_years,
                default=available_years,
                help="Select years for temporal analysis",
                key="years_filter",
                label_visibility="collapsed"
            )
        
        with filter_col2:
            st.markdown("""
            <div class="filter-card">
                <div class="filter-card-title">🚗 Vehicle Segments</div>
            </div>
            """, unsafe_allow_html=True)
            
            categories = st.multiselect(
                "Select Vehicle Categories",
                options=df['vehicle_category'].unique(),
                default=df['vehicle_category'].unique(),
                help="Choose vehicle category segments",
                key="category_filter",
                label_visibility="collapsed"
            )
        
        with filter_col3:
            st.markdown("""
            <div class="filter-card">
                <div class="filter-card-title">🏭 Vehicle Classifications</div>
            </div>
            """, unsafe_allow_html=True)
            
            top_manufacturers = df.groupby('manufacturer')['total_registrations'].sum().sort_values(ascending=False).head(15).index.tolist()
            manufacturers = st.multiselect(
                "Select Vehicle Types",
                options=sorted(df['manufacturer'].unique()),
                default=top_manufacturers,
                help="Select specific vehicle classifications",
                key="manufacturer_filter",
                label_visibility="collapsed"
            )
        
        return selected_years, categories, manufacturers
