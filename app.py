import streamlit as st
import streamlit.components.v1 as components
import feedparser
import yfinance as yf
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. ROBUST TREND ENGINE (API error आने पर भी ऐप नहीं रुकेगा)
def get_market_trends():
    try:
        ticker = yf.Ticker("GC=F") 
        trends = {}
        intervals = {"5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h"}
        bullish_count = 0
        for label, interval in intervals.items():
            data = ticker.history(period="1d", interval=interval)
            if not data.empty and len(data) >= 2:
                trends[label] = "Bullish" if data['Close'].iloc[-1] > data['Close'].iloc[-2] else "Bearish"
                if trends[label] == "Bullish": bullish_count += 1
            else: trends[label] = "No Data"
        return trends, bullish_count
    except:
        return {"5m": "N/A", "15m": "N/A", "1h": "N/A", "4h": "N/A"}, 0

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")
col_l, col_m, col_r = st.columns([1.5, 1, 1])

with col_l:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<iframe src="https://www.tradingview.com/widgetembed/?symbol=OANDA%3AXAUUSD" width="100%" height="320" frameborder="0"></iframe>""", height=320)

with col_m:
    st.markdown("### 📊 Market Sentiment")
    # API एरर को हैंडल किया
    trends, b_count = get_market_trends()
    score = b_count * 2.5
    st.metric(label="Live Sentiment Score", value=f"{score}/10")

with col_r:
    st.markdown("### 📈 Multi-Timeframe Trend")
    cols = st.columns(4)
    for i, (tf, trend) in enumerate(trends.items()):
        with cols[i]:
            st.caption(tf)
            st.write(trend)

# 4. HEATMAP & NEWS (अगर कुछ न दिखे, तो 'Reload' बटन दें)
st.markdown("### 🗺️ Currency Strength Heatmap")
components.html("""<iframe src="https://www.tradingview.com/embed-widget/forex-heat-map/" width="100%" height="400" frameborder="0"></iframe>""", height=420)
