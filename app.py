import streamlit as st
import streamlit.components.v1 as components
import feedparser
import yfinance as yf
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. TREND ENGINE (Multi-Timeframe)
def get_market_trends():
    ticker = yf.Ticker("GC=F") 
    trends = {}
    intervals = {"5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h"}
    bullish_count = 0
    
    for label, interval in intervals.items():
        data = ticker.history(period="1d", interval=interval)
        if not data.empty and len(data) >= 2:
            trends[label] = "Bullish" if data['Close'].iloc[-1] > data['Close'].iloc[-2] else "Bearish"
            if trends[label] == "Bullish": bullish_count += 1
        else:
            trends[label] = "Neutral"
    return trends, bullish_count

# 3. AI ANALYZER
client = Groq(api_key="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")

def get_single_news_impact(news_title):
    try:
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": f"Analyze: '{news_title}'. Format: Impact (High/Med/Low) + Reasoning."}])
        return completion.choices[0].message.content
    except: return "Analysis unavailable."

# 4. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")

# Top Row
col_l, col_m, col_r = st.columns([1.5, 1, 1])

with col_l:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "height": 300, "colorTheme": "light"}</script></div>""", height=320)

with col_m:
    st.markdown("### 📊 Market Sentiment")
    trends, b_count = get_market_trends()
    score = b_count * 2.5
    sentiment_label = "Bullish" if score >= 5 else "Bearish"
    st.metric(label="Live Sentiment Score", value=f"{score}/10", delta=sentiment_label)

with col_r:
    st.markdown("### 📈 Multi-Timeframe Trend")
    cols = st.columns(4)
    for i, (tf, trend) in enumerate(trends.items()):
        with cols[i]:
            st.caption(tf)
            st.write(trend)

# 5. HEATMAP & NEWS
st.markdown("### 🗺️ Currency Strength Heatmap")
components.html("""<iframe src="https://www.tradingview.com/embed-widget/forex-heat-map/?locale=en#%7B%22width%22%3A%22100%25%22%2C%22height%22%3A400%2C%22currencies%22%3A%5B%22EUR%22%2C%22USD%22%2C%22JPY%22%2C%22GBP%22%2C%22CHF%22%2C%22AUD%22%2C%22CAD%22%2C%22NZD%22%2C%22INR%22%5D%2C%22isTransparent%22%3Afalse%2C%22colorTheme%22%3A%22light%22%7D" width="100%" height="400" frameborder="0"></iframe>""", height=420)

st.header("📰 Live Market News & AI Analyser")
for url in ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]:
    for item in feedparser.parse(url).entries[:5]:
        with st.expander(item.title):
            if st.button("Analyze News", key=item.title):
                with st.spinner("AI analyzing..."): st.markdown(get_single_news_impact(item.title))
