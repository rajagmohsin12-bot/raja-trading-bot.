import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Trading Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    .buy-signal {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        border-left: 5px solid #047857;
    }
    .sell-signal {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        border-left: 5px solid #b91c1c;
    }
    .neutral-signal {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        border-left: 5px solid #374151;
    }
    .metric-container {
        background: #f3f4f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
st.sidebar.title(" Dashboard Settings")
st.sidebar.markdown("---")

pairs = {
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Ethereum (ETH-USD)": "ETH-USD",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "Gold (GC=F)": "GC=F"
}

selected_pair_name = st.sidebar.selectbox(
    " Select Trading Pair",
    list(pairs.keys()),
