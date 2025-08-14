"""
Components package for the vehicle dashboard
"""
from .styles import get_dashboard_styles
from .metrics import MetricsComponent
from .filters import FilterComponent
from .charts import ChartComponent
from .insights import InsightsComponent

__all__ = [
    'get_dashboard_styles',
    'MetricsComponent', 
    'FilterComponent',
    'ChartComponent',
    'InsightsComponent'
]
