import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq
import time

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Master Terminal", layout="wide")

client = Groq(api_key="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")

# 2. AI SENTIMENT ENGINE
def get_market_sentiment(news_content):
    prompt = f"Analyze these 10 news headlines and give a sentiment score from -10 (Extreme Bearish) to +10 (Extreme Bullish). NEWS: {news_content}"
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Master Terminal | Live")

# Top Section: Chart, Meters, and Calendar
col_chart, col_meters, col_cal = st.columns([2, 1, 1])

with col_chart:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light"}</script></div>""", height=250)

with col_meters:
    st.markdown("### 📊 Global Sentiment")
    if st.button("🔄 Refresh Sentiment"):
        st.write("Processing news mood...")
    st.container(border=True).markdown("<div style='text-align:center; font-size:24px'>🟢 Bullish (+6)</div>", unsafe_allow_html=True)

with col_cal:
    st.markdown("### 📅 Economic Calendar")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s.tradingview.com/external-embedding/embed-widget-events.js" async>{"width": "100%", "height": 250, "colorTheme": "light", "importanceFilter": "0,1"}</script></div>""", height=250)

st.write("---")

# 4. NEWS & IMPACT
st.header("📰 Live Market News")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
all_news = []
for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        all_news.append(item.title)
        with st.container(border=True):
            st.write(item.title)

# 5. AUTO-REFRESH LOGIC
st.sidebar.warning("Terminal auto-refreshes every 60 seconds.")
time.sleep(60)
st.rerun()
