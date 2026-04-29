import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import time

# Page Setup
st.set_page_config(page_title="A-Z Pro Quant Scanner", layout="wide")
st.title("💎 A-Z Professional Market Analyzer")

# 1. SIDEBAR CONFIG
asset_list = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'EURUSD=X', 'GBPUSD=X', 'GC=F']
symbol = st.sidebar.selectbox("Select Asset", asset_list)
timeframe = st.sidebar.selectbox("Timeframe", ['15m', '1h', '1d'])

# 2. ANALYSIS ENGINE
if st.sidebar.button('🚀 RUN MASTER ANALYSIS'):
    try:
        # Fetching Data
        data = yf.download(symbol, period='20d', interval=timeframe, progress=False)
        
        if data.empty:
            st.error("No data found! Check internet or symbol.")
        else:
            # FIX: Yahoo Finance Multi-index issue
            df = data.copy()
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # --- MATHEMATICS (A to Z) ---
            df['EMA_50'] = ta.ema(df['Close'], length=50)
            df['EMA_100'] = ta.ema(df['Close'], length=100)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['ADX'] = ta.adx(df['High'], df['Low'], df['Close'])['ADX_14']
            
            macd = ta.macd(df['Close'])
            df = pd.concat([df, macd], axis=1)
            
            bb = ta.bbands(df['Close'], length=20)
            df = pd.concat([df, bb], axis=1)
            
            # Support/Resistance & Price Action
            df['Sup'] = df['Low'].rolling(20).min()
            df['Res'] = df['High'].rolling(20).max()
            df['Bull_Eng'] = ((df['Close'] > df['Open']) & (df['Open'] < df['Close'].shift(1)) & (df['Close'] > df['Open'].shift(1))).astype(int)

            last = df.iloc[-1]
            
            # --- SCORING SYSTEM (1-10) ---
            score = 5
            reasons = []
            
            if last['Close'] > last['EMA_50'] > last['EMA_100']: score += 2; reasons.append("Strong Uptrend (EMAs)")
            if last['RSI'] < 35: score += 2; reasons.append("Oversold (RSI)")
            if last['MACD_12_26_9'] > last['MACDs_12_26_9']: score += 1; reasons.append("MACD Bullish Cross")
            if last['Bull_Eng'] == 1: score += 2; reasons.append("Bullish Engulfing Pattern")
            if last['Close'] <= last['Sup']: score += 1; reasons.append("Price at Support")

            # Final Score Normalization
            final_score = max(1, min(10, score))

            # --- DISPLAY ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Live Price", f"${float(last['Close']):.2f}")
            c2.metric("RSI", f"{float(last['RSI']):.1f}")
            c3.metric("ADX (Strength)", f"{float(last['ADX']):.1f}")
            c4.metric("Confluence Score", f"{final_score}/10")

            if final_score >= 8: st.success(f"🚀 **STRONG BUY SIGNAL** | Reasoning: {', '.join(reasons)}")
            elif final_score <= 3: st.error(f"📉 **STRONG SELL SIGNAL**")
            else: st.warning("😐 **NEUTRAL MARKET / WAIT**")

            # Charting
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], name="EMA 50", line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA_100'], name="EMA 100", line=dict(color='cyan')))
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Technical Error: {e}")
