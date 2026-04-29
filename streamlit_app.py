import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# 1. Page Title
st.title("🛡️ A-Z Pro Trading Dashboard")

# 2. Simple Inputs
symbol = st.selectbox("Select Asset", ['BTC-USD', 'ETH-USD', 'EURUSD=X', 'GBPUSD=X', 'GC=F'])
timeframe = st.selectbox("Timeframe", ['15m', '1h', '1d'])

# 3. Analyze Button
if st.button('🚀 RUN ANALYSIS'):
    try:
        # Fetch Data
        df = yf.download(symbol, period='15d', interval=timeframe, progress=False)
        
        if df.empty:
            st.error("No data found! Check your internet or symbol.")
        else:
            # Fix Multi-index Columns
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            
            # Basic Calculations
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_50'] = ta.ema(df['Close'], length=50)
            
            # Latest Values
            last_price = df['Close'].iloc[-1]
            last_rsi = df['RSI'].iloc[-1]
            
            # Show Metrics
            st.metric("Live Price", f"{last_price:.2f}")
            st.write(f"**RSI (14):** {last_rsi:.2f}")
            
            # Logic
            if last_rsi < 35: st.success("🚀 SIGNAL: BUY")
            elif last_rsi > 65: st.error("📉 SIGNAL: SELL")
            else: st.info("😐 Status: Neutral")

            # Chart
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error Details: {e}")
