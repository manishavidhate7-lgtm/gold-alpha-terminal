import streamlit as st
import feedparser
import streamlit.components.v1 as components
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. AI ANALYZER
client = Groq(api_key="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")

def get_single_news_impact(news_title):
    prompt = f"Analyze: '{news_title}'. Format: Impact on XAU/USD, USD/INR, Nifty (High/Med/Low) + Reasoning."
    try:
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        return completion.choices[0].message.content
    except: return "Analysis unavailable."

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")

# Row 1: Chart, Sentiment, and Calendar
col_left, col_mid, col_right = st.columns([1.5, 1, 1])

with col_left:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "height": 300, "colorTheme": "light"}</script></div>""", height=320)

with col_mid:
    st.markdown("### 📊 Market Sentiment")
    st.metric(label="Sentiment Score", value="6/10", delta="Bullish")
    if st.button("🔄 Refresh"): st.rerun()

with col_right:
    st.markdown("### 📅 Economic Calendar")
    components.html("""<iframe src="https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=1,2,3&features=datepicker,timezone&countries=25,32,37,72,5&calType=day&lang=1" width="100%" height="300" frameborder="0"></iframe>""", height=320)

st.write("---")

# Row 2: Currency Heatmap
st.markdown("### 🗺️ Currency Strength Heatmap")
components.html("""
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
  {"width": "100%", "height": 400, "currencies": ["EUR", "USD", "JPY", "GBP", "CHF", "AUD", "CAD", "NZD", "INR"], "isTransparent": false, "colorTheme": "light"}
  </script>
</div>
""", height=420)

st.write("---")

# Row 3: News
st.header("📰 Live Market News & AI Analyser")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.container(border=True):
            col_n, col_a = st.columns([3, 1])
            with col_n: st.write(item.title)
            with col_a:
                if st.button("Analyze", key=item.title):
                    with st.spinner("AI analyzing..."): st.markdown(get_single_news_impact(item.title))

# 4. AUTO-REFRESH
time.sleep(60)
st.rerun()
