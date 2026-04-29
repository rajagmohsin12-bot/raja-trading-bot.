import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Pro Quant Scanner", layout="wide")

# 1. CSS for Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ A-Z Ultimate Trading Dashboard")

# 2. Sidebar Configuration
st.sidebar.header("Market Control")
asset = st.sidebar.selectbox("Select Asset", ['BTC-USD', 'ETH-USD', 'EURUSD=X', 'GBPUSD=X', 'GC=F', 'SI=F'])
timeframe = st.sidebar.selectbox("Timeframe", ['15m', '1h', '1d'])

# 3. Core Engine (Mathematical Analysis)
def analyze(symbol, interval):
    df = yf.download(symbol, period='15d', interval=interval, progress=False)
    if df.empty: return None
    df.columns = df.columns.get_level_values(0)
    
    # EMAs & Momentum
    df['EMA_50'] = ta.ema(df['Close'], length=50)
    df['EMA_100'] = ta.ema(df['Close'], length=100)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['ADX'] = ta.adx(df['High'], df['Low'], df['Close'])['ADX_14']
    
    # Volatility & Momentum
    bb = ta.bbands(df['Close'], length=20)
    df = pd.concat([df, bb], axis=1)
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)
    
    # Price Action Patterns
    df['Bull_Eng'] = ((df['Close'] > df['Open']) & (df['Open'] < df['Close'].shift(1)) & (df['Close'] > df['Open'].shift(1))).astype(int)
    
    return df

# 4. Run Analysis
if st.sidebar.button('GENERATE MASTER SIGNAL'):
    df = analyze(asset, timeframe)
    if df is not None:
        last = df.iloc[-1]
        
        # PRO SCORING (1-10)
        score = 5
        reasons = []
        if last['Close'] > last['EMA_50'] > last['EMA_100']: score += 2; reasons.append("Strong Uptrend")
        if last['RSI'] < 35: score += 2; reasons.append("Oversold (RSI)")
        if last['MACD_12_26_9'] > last['MACDs_12_26_9']: score += 1; reasons.append("MACD Bullish Cross")
        if last['Bull_Eng']: score += 2; reasons.append("Bullish Engulfing Found")
        if last['ADX'] > 25: score += 1; reasons.append("Strong Trend Momentum")

        # Metrics Display
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Live Price", f"${last['Close']:.2f}")
        col2.metric("RSI", f"{last['RSI']:.1f}")
        col3.metric("ADX", f"{last['ADX']:.1f}")
        col4.metric("Quant Score", f"{score}/10")

        # Signal Alert
        if score >= 8: st.success(f"🚀 **STRONG BUY SIGNAL** | Reasoning: {', '.join(reasons)}")
        elif score <= 3: st.error(f"📉 **STRONG SELL SIGNAL**")
        else: st.warning("😐 **NEUTRAL MARKET**")

        # Pro Charting
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], name="EMA 50", line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_100'], name="EMA 100", line=dict(color='cyan')))
        st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.caption("A-Z Pro Quant Scanner | Professional Grade Mathematical Analysis")
