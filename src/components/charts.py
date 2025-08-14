"""
Chart components for the dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import logging

logger = logging.getLogger(__name__)

class ChartComponent:
    
    @staticmethod
    def create_enhanced_chart(data, chart_type, **kwargs):
        """Create enhanced charts with updated color scheme"""
        if data.empty:
            return None
            
        if chart_type == 'line':
            fig = px.line(data, **kwargs)
            fig.update_traces(line=dict(width=4))
        elif chart_type == 'bar':
            fig = px.bar(data, **kwargs)
        elif chart_type == 'horizontal_bar':
            fig = px.bar(data, orientation='h', **kwargs)
        elif chart_type == 'pie':
            fig = px.pie(data, **kwargs)
        else:
            fig = px.scatter(data, **kwargs)
        
        # Enhanced styling with teal/navy color scheme
        fig.update_layout(
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Inter, sans-serif", size=13, color="#0f172a"),
            title_font=dict(size=18, color="#0f172a", family="Inter", weight=600),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(255,255,255,0.95)",
                bordercolor="rgba(15,118,110,0.2)",
                borderwidth=1,
                font=dict(color="#0f172a", size=12)
            ),
            margin=dict(l=50, r=50, t=70, b=50),
            height=380
        )
        
        # Better grid styling
        fig.update_xaxes(
            gridcolor='rgba(15,118,110,0.15)',
            linecolor='rgba(15,118,110,0.3)',
            tickfont=dict(color="#0f172a", size=11),
            showgrid=True,
            title_font=dict(color="#0f172a", size=13)
        )
        fig.update_yaxes(
            gridcolor='rgba(15,118,110,0.15)',
            linecolor='rgba(15,118,110,0.3)',
            tickfont=dict(color="#0f172a", size=11),
            showgrid=True,
            title_font=dict(color="#0f172a", size=13)
        )
        
        return fig
    
    @staticmethod
    def display_market_trends_section(df_filtered):
        """Display market trends analysis section"""
        st.markdown('<h2 class="section-header">📈 Market Trends Analysis</h2>', unsafe_allow_html=True)
        
        # Two column layout
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            yearly_data = df_filtered.groupby([df_filtered['registration_date'].dt.year, 'vehicle_category'])['total_registrations'].sum().reset_index()
            yearly_data.columns = ['Year', 'Category', 'Registrations']
            
            if not yearly_data.empty:
                fig_trend = ChartComponent.create_enhanced_chart(
                    yearly_data, 'line',
                    x='Year', y='Registrations', color='Category',
                    title="📈 Registration Volume Trends by Category",
                    color_discrete_sequence=['#0f766e', '#155e75', '#0891b2', '#0369a1', '#1e40af']
                )
                if fig_trend:
                    st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("📊 No trend data available for selected filters")
        
        with chart_col2:
            category_share = df_filtered.groupby('vehicle_category')['total_registrations'].sum()
            
            if not category_share.empty:
                fig_pie = ChartComponent.create_enhanced_chart(
                    pd.DataFrame({'Category': category_share.index, 'Share': category_share.values}),
                    'pie',
                    values='Share', names='Category',
                    title="🥧 Market Share Distribution",
                    color_discrete_sequence=['#0f766e', '#155e75', '#0891b2', '#0369a1', '#1e40af']
                )
                if fig_pie:
                    st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("📊 No market share data available")
    
    @staticmethod
    def display_vehicle_performance_section(df_filtered):
        """Display vehicle type performance section"""
        st.markdown('<h2 class="section-header">🏭 Vehicle Type Performance</h2>', unsafe_allow_html=True)
        
        top_15_types = df_filtered.groupby('manufacturer')['total_registrations'].sum().sort_values(ascending=False).head(15)
        
        if not top_15_types.empty:
            fig_top_types = ChartComponent.create_enhanced_chart(
                pd.DataFrame({'Vehicle Type': top_15_types.index, 'Registrations': top_15_types.values}),
                'horizontal_bar',
                x='Registrations', y='Vehicle Type',
                title="🚀 Top 15 Vehicle Types by Registration Volume",
                color='Registrations',
                color_continuous_scale=['#a7f3d0', '#67e8f9', '#0891b2', '#155e75', '#0f766e']
            )
            if fig_top_types:
                fig_top_types.update_layout(height=520)
                st.plotly_chart(fig_top_types, use_container_width=True)
        else:
            st.info("📊 No vehicle type data available for selected filters")
