import streamlit as st
import streamlit.components.v1 as components
import feedparser
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. DYNAMIC SENTIMENT ENGINE
def get_dynamic_sentiment():
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
    st.markdown("### 📊 Live Market Sentiment")
    live_score = get_dynamic_sentiment()
    sentiment_label = "Bullish" if live_score > 5 else "Bearish"
    st.metric(label="Dynamic Sentiment Score", value=f"{live_score}/10", delta=sentiment_label)
    if st.button("🔄 Refresh"): st.rerun()

with col_right:
    st.markdown("### 📅 Economic Calendar")
    components.html("""
    <div class="tradingview-widget-container">
      <iframe src="https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=1,2,3&features=datepicker,timezone&countries=25,32,37,72,5&calType=day&lang=1" width="100%" height="400" frameborder="0"></iframe>
    </div>
    """, height=420)

st.write("---")

# 4. CURRENCY HEATMAP
st.markdown("### 🗺️ Currency Strength Heatmap")
components.html("""
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>
  {
  "width": "100%",
  "height": 400,
  "currencies": ["EUR", "USD", "JPY", "GBP", "CHF", "AUD", "CAD", "NZD", "INR"],
  "isTransparent": false,
  "colorTheme": "light",
  "locale": "en"
  }
  </script>
</div>
""", height=420)

st.write("---")

# 5. NEWS SECTION
st.header("📰 Live Market News & AI Analyser")
# यहाँ अपना फीड पार्सर वाला कोड जोड़ें...
