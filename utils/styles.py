"""
Praxis Branded Styles for Databricks Job Monitor
Custom CSS with Praxis color scheme
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config


def get_custom_css():
    """Return custom CSS with Praxis branding"""
    return f"""
    <style>
        :root {{
            --praxis-black: {Config.PRAXIS_BLACK};
            --praxis-cyan: {Config.PRAXIS_CYAN};
            --praxis-blue: {Config.PRAXIS_BLUE};
            --praxis-orange: {Config.PRAXIS_ORANGE};
        }}
        
        /* ===== SIDEBAR STYLES ===== */
        [data-testid="stSidebar"] {{
            background: {Config.PRAXIS_BLACK} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {{
            color: white !important;
            font-weight: 600;
        }}
        
        /* ===== DROPDOWN FIX ===== */
        .stSelectbox {{
            color: #1f2937 !important;
        }}
        
        .stSelectbox label {{
            color: white !important;
            font-weight: 500 !important;
        }}
        
        .stSelectbox > div > div {{
            background-color: white !important;
            border: 1px solid #e2e8f0 !important;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            color: #1f2937 !important;
        }}
        
        .stSelectbox [data-baseweb="select"] > div {{
            color: #1f2937 !important;
        }}
        
        .stSelectbox input {{
            color: #1f2937 !important;
            background-color: white !important;
        }}
        
        .stSelectbox * {{
            color: #1f2937 !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox > div > div * {{
            color: #1f2937 !important;
        }}
        
        [data-baseweb="menu"] {{
            background-color: white !important;
        }}
        
        [data-baseweb="menu"] li {{
            color: #1f2937 !important;
            background-color: white !important;
        }}
        
        [data-baseweb="menu"] li:hover {{
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
        }}
        
        [data-baseweb="menu"] li * {{
            color: #1f2937 !important;
        }}
        
        .stSelectbox svg {{
            fill: #1f2937 !important;
        }}
        
        /* ===== RADIO BUTTONS ===== */
        .stRadio label {{
            color: white !important;
        }}
        
        .stRadio [role="radiogroup"] label {{
            color: white !important;
        }}
        
        /* ===== LOGO & BRANDING ===== */
        .praxis-logo-container {{
            text-align: center;
            padding: 1.5rem 1rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid rgba(255,255,255,0.2);
        }}
        
        .praxis-tagline {{
            font-size: 0.7rem;
            color: {Config.PRAXIS_CYAN};
            font-weight: 600;
            letter-spacing: 0.2em;
            margin-top: 0.5rem;
        }}
        
        .praxis-subtitle {{
            font-size: 0.8rem;
            color: rgba(255,255,255,0.75);
            font-weight: 300;
            line-height: 1.4;
            margin-top: 0.5rem;
        }}
        
        /* ===== HEADERS ===== */
        .main-header {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {Config.PRAXIS_BLUE};
            margin-bottom: 0.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid {Config.PRAXIS_CYAN};
        }}
        
        .main-subtitle {{
            color: #64748b;
            margin-bottom: 0.5rem !important;
            font-size: 1rem;
        }}
        
        .sub-header {{
            font-size: 1.3rem;
            font-weight: 600;
            color: {Config.PRAXIS_BLUE};
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        /* Compact sub-header for inside expanders */
        .sub-header-compact {{
            font-size: 1.2rem;
            font-weight: 600;
            color: {Config.PRAXIS_BLUE};
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            padding-bottom: 0.25rem;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        /* Balanced gaps in main content area */
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {{
            gap: 0.75rem !important;
        }}
        
        /* ===== JOB STATUS CARDS ===== */
        .job-card {{
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }}
        
        .job-card:hover {{
            border-color: {Config.PRAXIS_CYAN};
            box-shadow: 0 4px 12px rgba(0,206,209,0.15);
            transform: translateY(-2px);
        }}
        
        .job-card-success {{
            border-left: 4px solid {Config.STATUS_SUCCESS};
        }}
        
        .job-card-failed {{
            border-left: 4px solid {Config.STATUS_FAILED};
        }}
        
        .job-card-running {{
            border-left: 4px solid {Config.STATUS_RUNNING};
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
            100% {{ opacity: 1; }}
        }}
        
        /* ===== METRIC CARDS ===== */
        .metric-card {{
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        
        .metric-card:hover {{
            border-color: {Config.PRAXIS_CYAN};
            box-shadow: 0 4px 12px rgba(0,206,209,0.15);
            transform: translateY(-2px);
        }}
        
        .metric-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: {Config.PRAXIS_BLUE};
            margin-bottom: 0.25rem;
        }}
        
        .metric-label {{
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 500;
        }}
        
        /* ===== BUTTONS ===== */
        .stButton>button {{
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        [data-testid="stSidebar"] .stButton>button {{
            background-color: transparent;
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
            padding: 0.75rem 1rem;
        }}
        
        [data-testid="stSidebar"] .stButton>button:hover {{
            background-color: rgba(255,255,255,0.1) !important;
            border-color: {Config.PRAXIS_CYAN};
        }}
        
        [data-testid="stSidebar"] button[kind="primary"] {{
            background-color: {Config.PRAXIS_CYAN} !important;
            color: black !important;
            font-weight: 700;
            border: none;
        }}
        
        /* Primary action buttons */
        .stButton>button[kind="primary"] {{
            background-color: {Config.PRAXIS_CYAN} !important;
            color: black !important;
            font-weight: 700;
        }}
        
        /* ===== TABLES ===== */
        .dataframe {{
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px;
        }}
        
        .dataframe th {{
            background-color: {Config.PRAXIS_BLUE} !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px !important;
        }}
        
        .dataframe td {{
            padding: 10px !important;
        }}
        
        /* ===== ALERTS & INFO BOXES ===== */
        .stAlert {{
            border-radius: 8px;
            border-left: 4px solid {Config.PRAXIS_CYAN};
        }}
        
        /* ===== EXPANDERS ===== */
        .streamlit-expanderHeader {{
            background-color: #f8fafc;
            border-radius: 8px;
            font-weight: 600;
            color: {Config.PRAXIS_BLUE} !important;
        }}
        
        [data-testid="stExpander"] {{
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            margin-bottom: 1rem;
        }}
        
        [data-testid="stExpander"]:hover {{
            border-color: {Config.PRAXIS_CYAN};
        }}
        
        /* Reduce spacing inside expanders */
        [data-testid="stExpander"] [data-testid="stVerticalBlock"] {{
            gap: 0.5rem !important;
        }}
        
        [data-testid="stExpander"] .stMarkdown {{
            margin-bottom: 0 !important;
        }}
        
        [data-testid="stExpander"] [data-testid="stCaptionContainer"] {{
            margin-top: -0.5rem !important;
            margin-bottom: 0.5rem !important;
        }}
        
        /* ===== TOGGLE ===== */
        .stToggle label {{
            color: white !important;
        }}
        
        /* ===== SLIDER ===== */
        .stSlider label {{
            color: white !important;
        }}
        
        /* ===== STATUS BADGES ===== */
        .status-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
        }}
        
        .status-success {{
            background-color: #D1FAE5;
            color: #065F46;
        }}
        
        .status-failed {{
            background-color: #FEE2E2;
            color: #991B1B;
        }}
        
        .status-running {{
            background-color: #DBEAFE;
            color: #1E40AF;
        }}
        
        .status-canceled {{
            background-color: #EDE9FE;
            color: #5B21B6;
        }}
        
        /* ===== CONNECTION STATUS ===== */
        .connection-status {{
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        }}
        
        .connection-connected {{
            background-color: rgba(16, 185, 129, 0.2);
            border: 1px solid #10B981;
        }}
        
        .connection-disconnected {{
            background-color: rgba(239, 68, 68, 0.2);
            border: 1px solid #EF4444;
        }}
        
        /* ===== LAST REFRESH INFO ===== */
        .refresh-info {{
            font-size: 0.75rem;
            color: rgba(255,255,255,0.6);
            text-align: center;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
    </style>
    """

