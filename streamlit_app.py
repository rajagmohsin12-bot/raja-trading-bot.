import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import traceback

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Trading Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .buy-signal {
        background: #10b981;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
    .sell-signal {
        background: #ef4444;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
    .neutral-signal {
        background: #6b7280;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
st.sidebar.title(" Dashboard Settings")

pairs = {
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Ethereum (ETH-USD)": "ETH-USD",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "Gold (GC=F)": "GC=F"
}

selected_pair_name = st.sidebar.selectbox("Select Trading Pair", list(pairs.keys()))
selected_pair = pairs[selected_pair_name]

timeframes = {
    "5 Minutes": "5m",
    "15 Minutes": "15m",
    "1 Hour": "1h",
    "1 Day": "1d"
}

selected_timeframe_name = st.sidebar.selectbox("Select Timeframe", list(timeframes.keys()))
selected_timeframe = timeframes[selected_timeframe_name]

run_analysis = st.sidebar.button(" Run Analysis", use_container_width=True)

# ============================================================================
# DATA FETCHING FUNCTION (WITH MULTIINDEX FIX)
# ============================================================================
@st.cache_data(ttl=300)
def fetch_data(pair, interval):
    """Fetch live data from
