import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(page_title="A-Z Pro Analyzer", layout="wide")
st.title("📊 A-Z Professional Market Scanner")

# Sidebar
symbol = st.sidebar.selectbox("Select Pair", ['BTC-USD', 'ETH-USD', 'EURUSD=X', 'GBPUSD=X', 'GC=F'])
timeframe = st.sidebar.selectbox("Interval", ['15m', '1h', '1d'])

if st.sidebar.button('🚀 RUN ANALYSIS'):
    try:
        # Data fetch
        df = yf.download(symbol, period='20d', interval=timeframe, progress=False)
        
        if not df.empty:
            # Fix for MultiIndex
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Indicators
            df['EMA_50'] = ta.ema(df['Close'], length=50)
            df['EMA_100'] = ta.ema(df['Close'], length=100)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['ADX'] = ta.adx(df['High'], df['Low'], df['Close'])['ADX_14']
            
            last = df.iloc[-1]
            
            # Display Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Live Price", f"{float(last['Close']):.2f}")
            c2.metric("RSI", f"{float(last['RSI']):.1f}")
            c3.metric("ADX", f"{float(last['ADX']):.1f}")
            
            # Simple Logic
            if float(last['RSI']) < 35: st.success("🚀 SIGNAL: BUY")
            elif float(last['RSI']) > 65: st.error("📉 SIGNAL: SELL")
            else: st.info("😐 Status: Neutral")

            # Chart
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Market data not found!")
    except Exception as e:
        st.error(f"Technical Error: {e}")
