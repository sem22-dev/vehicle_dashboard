"""
CSS styles for the vehicle dashboard
"""

def get_dashboard_styles():
    """Return all CSS styles for the dashboard"""
    return """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styling */
        .stApp {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1e3a8a 0%, #155e75 100%);
        }
        
        /* Main container */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
            background: #ffffff;
            border-radius: 20px;
            margin: 1rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        
        /* Header styling */
        .dashboard-header {
            text-align: center;
            padding: 2.5rem 0;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 10px 30px rgba(30, 58, 138, 0.5);
        }
        
        .dashboard-title {
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
            color: #ffffff;
        }
        
        .dashboard-subtitle {
            font-size: 1.3rem;
            font-weight: 400;
            margin-top: 0.8rem;
            color: #e0f2fe;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        /* Filter styling */
        .filter-section {
            background: linear-gradient(135deg, #0f766e 0%, #155e75 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 40px rgba(15, 118, 110, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .filter-title {
            color: #ffffff;
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 2rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
        }
        
        .filter-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 0.5rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(15, 118, 110, 0.2);
            transition: transform 0.3s ease;
        }
        
        .filter-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(15, 118, 110, 0.2);
        }
        
        .filter-card-title {
            color: #0f766e;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
            border-bottom: 2px solid #0f766e;
            padding-bottom: 0.5rem;
        }
        
        /* Enhanced multiselect styling */
        .stMultiSelect > div > div {
            background-color: #ffffff;
            border: 2px solid #0f766e;
            border-radius: 10px;
            color: #0f172a;
        }
        
        .stMultiSelect > div > div:hover {
            border-color: #155e75;
            box-shadow: 0 4px 15px rgba(15, 118, 110, 0.2);
        }
        
        .stMultiSelect span[data-baseweb="tag"] {
            background-color: #0f766e !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }
        
        .stMultiSelect span[data-baseweb="tag"] > span:first-child {
            color: white !important;
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #0f766e 0%, #155e75 100%);
            padding: 1.8rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 0.3rem;
            box-shadow: 0 10px 30px rgba(15, 118, 110, 0.4);
            transition: transform 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(15, 118, 110, 0.6);
        }
        
        .metric-value {
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .metric-label {
            font-size: 1rem;
            font-weight: 600;
            margin-top: 0.8rem;
            color: #a7f3d0;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        /* Section headers */
        .section-header {
            font-size: 2rem;
            font-weight: 700;
            color: #0f172a;
            margin: 2.5rem 0 1.5rem 0;
            border-left: 5px solid #0f766e;
            padding-left: 1.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        /* Insights cards */
        .insight-card {
            background: linear-gradient(135deg, #0f766e 0%, #155e75 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: white;
            border-left: 5px solid #06b6d4;
            box-shadow: 0 8px 25px rgba(15, 118, 110, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .insight-card strong {
            color: #67e8f9;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        /* Growth explanation cards */
        .growth-explanation {
            background: #f0f9ff;
            border: 1px solid #0ea5e9;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            color: #0c4a6e;
        }
        
        .growth-explanation strong {
            color: #0369a1;
        }
        
        /* Better button styling */
        .stButton > button {
            background: linear-gradient(135deg, #0f766e 0%, #155e75 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.7rem 1.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
            box-shadow: 0 4px 15px rgba(15, 118, 110, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(15, 118, 110, 0.5);
            background: linear-gradient(135deg, #134e4a 0%, #164e63 100%);
        }
        
        /* Fix expander styling */
        .streamlit-expanderHeader {
            background-color: #f0fdfa !important;
            color: #0f766e !important;
            font-weight: 600 !important;
            border: 1px solid #0f766e !important;
            border-radius: 10px !important;
        }
        
        /* Remove streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
