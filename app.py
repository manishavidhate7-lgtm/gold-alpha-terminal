import streamlit as st
import streamlit.components.v1 as components
import feedparser
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. DYNAMIC SENTIMENT ENGINE
def get_dynamic_sentiment():
    # यहाँ PRICE CHANGE डायनामिक हो सकता है, अभी के लिए इसे फिक्स रखा है ताकि कोड एरर न दे
    price_change = -0.62 
    base_sentiment = 6
    final_score = base_sentiment + (price_change * 5)
    return max(0, min(10, round(final_score, 1)))

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")

col_left, col_mid, col_right = st.columns([1.5, 1, 1])

with col_left:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "height": 300, "colorTheme": "light"}</script></div>""", height=320)

with col_mid:
    st.markdown("### 📊 Market Sentiment")
    live_score = get_dynamic_sentiment()
    sentiment_label = "Bullish" if live_score > 5 else "Bearish"
    st.metric(label="Dynamic Sentiment Score", value=f"{live_score}/10", delta=sentiment_label)
    if st.button("🔄 Refresh"): st.rerun()

with col_right:
    st.markdown("### 📅 Economic Calendar")
    # Iframe तरीका ताकि यह हमेशा लोड हो
    components.html("""
    <iframe src="https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=1,2,3&features=datepicker,timezone&countries=25,32,37,72,5&calType=day&lang=1" width="100%" height="300" frameborder="0"></iframe>
    """, height=320)

st.write("---")

# 4. CURRENCY HEATMAP (Iframe फिक्स)
st.markdown("### 🗺️ Currency Strength Heatmap")
components.html("""
<iframe src="https://www.tradingview.com/embed-widget/forex-heat-map/?locale=en#%7B%22width%22%3A%22100%25%22%2C%22height%22%3A400%2C%22currencies%22%3A%5B%22EUR%22%2C%22USD%22%2C%22JPY%22%2C%22GBP%22%2C%22CHF%22%2C%22AUD%22%2C%22CAD%22%2C%22NZD%22%2C%22INR%22%5D%2C%22isTransparent%22%3Afalse%2C%22colorTheme%22%3A%22light%22%7D" width="100%" height="400" frameborder="0"></iframe>
""", height=420)

st.write("---")

# 5. NEWS SECTION
st.header("📰 Live Market News & AI Analyser")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.container(border=True):
            st.write(item.title)
            if st.button("Analyze", key=item.title):
                st.write("AI Analysis placeholder...")

# 6. AUTO-REFRESH
time.sleep(60)
st.rerun()
