import streamlit as st
import feedparser
import streamlit.components.v1 as components
import time

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Master Terminal", layout="wide")

# 2. UI LAYOUT
st.title("⚡ Wolf Alpha Master Terminal | Live")

# Top Section: Chart, Sentiment, and Calendar
# Layout को 3 बराबर हिस्सों में बांटते हैं
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light"}</script></div>""", height=250)

with col2:
    st.markdown("### 📊 Global Sentiment")
    # एक ही डिब्बा रखेंगे ताकि कंफ्यूजन न हो
    with st.container(border=True):
        st.markdown("<div style='text-align:center; font-size:20px'>🟢 Bullish (+6)</div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh"):
        st.rerun()

with col3:
    st.markdown("### 📅 Economic Calendar")
    # Calendar विजेट फिक्स किया
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s.tradingview.com/external-embedding/embed-widget-events.js" async>{"width": "100%", "height": "400", "colorTheme": "light", "importanceFilter": "0,1"}</script></div>""", height=400)

st.write("---")

# 4. NEWS SECTION
st.header("📰 Live Market News")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.container(border=True):
            st.markdown(f"**{item.title}**")

# 5. AUTO-REFRESH
st.sidebar.warning("Auto-refreshing every 60s.")
time.sleep(60)
st.rerun()
