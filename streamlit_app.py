import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(page_title="Pro Trading Dashboard", layout="wide")
st.title("📊 A-Z Master Market Scanner")

# Sidebar
asset = st.sidebar.selectbox("Select Asset", ['BTC-USD', 'ETH-USD', 'EURUSD=X', 'GBPUSD=X', 'GC=F'])
timeframe = st.sidebar.selectbox("Timeframe", ['15m', '1h', '1d'])

if st.sidebar.button('Run Analysis'):
    try:
        # Data fetch
        df = yf.download(asset, period='15d', interval=timeframe, progress=False)
        
        if df.empty:
            st.error("No data found!")
        else:
            # Fix for new yfinance format
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Indicators
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_50'] = ta.ema(df['Close'], length=50)
            
            last_price = float(df['Close'].iloc[-1])
            last_rsi = float(df['RSI'].iloc[-1])
            
            # Display
            st.metric(f"Current Price ({asset})", f"${last_price:.2f}")
            st.write(f"**RSI (14):** {last_rsi:.2f}")
            
            # Signal Logic
            if last_rsi < 35: st.success("🚀 SIGNAL: BUY (Oversold)")
            elif last_rsi > 65: st.error("📉 SIGNAL: SELL (Overbought)")
            else: st.info("😐 Status: Neutral")
            
            # Chart
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Technical Error: {e}")
