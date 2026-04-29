import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Pro Quant Scanner", layout="wide")

st.title("🛡️ A-Z Ultimate Trading Dashboard")

# Asset List
asset_list = ['BTC-USD', 'ETH-USD', 'EURUSD=X', 'GBPUSD=X', 'GC=F']
symbol = st.sidebar.selectbox("Select Asset", asset_list)
timeframe = st.sidebar.selectbox("Timeframe", ['15m', '1h', '1d'])

if st.sidebar.button('🚀 GENERATE MASTER SIGNAL'):
    try:
        # Data Fetching
        df = yf.download(symbol, period='15d', interval=timeframe, progress=False)
        
        if not df.empty:
            # Multi-Index columns fix
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Math Indicators
            df['EMA_50'] = ta.ema(df['Close'], length=50)
            df['EMA_100'] = ta.ema(df['Close'], length=100)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            
            last = df.iloc[-1]
            
            # Display Results
            c1, c2 = st.columns(2)
            c1.metric("Current Price", f"{last['Close']:.4f}")
            c2.metric("RSI", f"{last['RSI']:.2f}")

            # Chart
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Market data not found.")
    except Exception as e:
        st.error(f"Error: {e}")
