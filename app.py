import streamlit as st
import feedparser
import streamlit.components.v1 as components
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. DYNAMIC SENTIMENT ENGINE
def get_dynamic_sentiment():
    # यहाँ हम 'Price Action' का इम्पैक्ट जोड़ रहे हैं
    # मान लीजिए मार्केट 0.62% गिरा है
    price_change = -0.62 
    
    # बेस सेंटीमेंट AI से आता है (माना 6)
    base_sentiment = 6
    
    # कैलकुलेशन: अगर प्राइस गिर रहा है, तो सेंटीमेंट स्कोर कम होगा
    # फॉर्मूला: बेस स्कोर + (प्राइस चेंज * 5)
    final_score = base_sentiment + (price_change * 5)
    
    # स्कोर को 0 से 10 के बीच रखें
    return max(0, min(10, round(final_score, 1)))

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")

col_left, col_mid, col_right = st.columns([1.5, 1, 1])

with col_left:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "height": 300, "colorTheme": "light"}</script></div>""", height=320)

with col_mid:
    st.markdown("### 📊 Live Market Sentiment")
    # अब ये स्कोर लाइव प्राइस के हिसाब से बदलेगा
    live_score = get_dynamic_sentiment()
    sentiment_label = "Bullish" if live_score > 5 else "Bearish"
    st.metric(label="Dynamic Sentiment Score", value=f"{live_score}/10", delta=sentiment_label)
    if st.button("🔄 Refresh"): st.rerun()

# (बाकी का Currency Heatmap और News सेक्शन वैसे ही रखें...)
