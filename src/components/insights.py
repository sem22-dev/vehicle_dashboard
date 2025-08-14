"""
Insights components for the dashboard
"""
import streamlit as st
import pandas as pd

class InsightsComponent:
    
    @staticmethod
    def create_growth_explanation_card(title, explanation):
        """Create explanation cards for growth metrics"""
        st.markdown(f"""
        <div class="growth-explanation">
            <strong>{title}</strong><br>
            {explanation}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def generate_enhanced_insights(df, selected_years):
        """Generate enhanced investment insights"""
        insights = []
        
        try:
            if df.empty:
                return ["📊 **No insights available** - Please adjust your filters"]
                
            # Market dominance analysis
            manufacturer_totals = df.groupby('manufacturer')['total_registrations'].sum()
            if not manufacturer_totals.empty:
                top_type = manufacturer_totals.idxmax()
                top_registrations = manufacturer_totals.max()
                market_share = (top_registrations / df['total_registrations'].sum()) * 100
                insights.append(f"🏆 **Market Leader**: {top_type} commands {market_share:.1f}% market share with {top_registrations:,.0f} registrations")
            
            # Category performance
            category_totals = df.groupby('vehicle_category')['total_registrations'].sum()
            if not category_totals.empty:
                category_leader = category_totals.idxmax()
                category_dominance = (category_totals.max() / df['total_registrations'].sum()) * 100
                insights.append(f"🎯 **Segment Dominance**: {category_leader} vehicles control {category_dominance:.1f}% of the total market")
            
            # Electric mobility trend
            ev_keywords = ['E-RICKSHAW', 'ELECTRIC', 'EV']
            ev_data = df[df['manufacturer'].str.contains('|'.join(ev_keywords), case=False, na=False)]
            if not ev_data.empty:
                ev_share = (ev_data['total_registrations'].sum() / df['total_registrations'].sum()) * 100
                insights.append(f"⚡ **EV Revolution**: Electric vehicles represent {ev_share:.1f}% of registrations, indicating strong sustainability adoption")
            
            # Market concentration
            if len(manufacturer_totals) >= 3:
                top_3_share = (manufacturer_totals.sort_values(ascending=False).head(3).sum() / df['total_registrations'].sum()) * 100
                insights.append(f"🎪 **Market Concentration**: Top 3 vehicle types account for {top_3_share:.1f}% of total registrations")
            
            # Investment recommendation
            if len(selected_years) > 1:
                yearly_totals = df.groupby(df['registration_date'].dt.year)['total_registrations'].sum()
                if len(yearly_totals) > 1:
                    latest_growth = ((yearly_totals.iloc[-1] - yearly_totals.iloc[-2]) / yearly_totals.iloc[-2]) * 100
                    trend_emoji = "📈" if latest_growth > 0 else "📉"
                    insights.append(f"{trend_emoji} **Growth Trajectory**: {latest_growth:+.1f}% year-over-year growth in the latest period - {'Strong investment signal' if latest_growth > 5 else 'Cautious growth' if latest_growth > 0 else 'Market correction phase'}")
            
        except Exception as e:
            insights.append("📊 **Analytics Processing**: Market intelligence compilation in progress...")
        
        return insights if insights else ["📊 **Processing**: Advanced insights will be available with expanded data"]
    
    @staticmethod
    def display_insights_section(df_filtered, selected_years):
        """Display the investment insights section"""
        st.markdown('<h2 class="section-header">💡 Investment Intelligence</h2>', unsafe_allow_html=True)
        
        insights = InsightsComponent.generate_enhanced_insights(df_filtered, selected_years)
        for insight in insights:
            st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
