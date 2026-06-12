import streamlit as st
import feedparser
import streamlit.components.v1 as components
import time
import urllib.request
import json
from groq import Groq

# =====================================================================
# 1. PAGE SETUP
# =====================================================================
st.set_page_config(page_title="XAUUSD Alpha Terminal v2", layout="wide", initial_sidebar_state="collapsed")

# CSS Styling
st.markdown("""
<style>
    .metric-card { background-color: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0px 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 8px; }
    .timeframe-title { font-size: 13px; font-weight: bold; color: #64748b; margin-bottom: 3px; }
    .buy-text { color: #089981; font-weight: 800; font-size: 16px; }
    .sell-text { color: #f23645; font-weight: 800; font-size: 16px; }
    .neutral-text { color: #64748b; font-weight: 800; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ XAU/USD Alpha Terminal v2")

# =====================================================================
# 2. GROQ CLIENT SETUP
# =====================================================================
# यहाँ अपनी असली API Key डालें या Secrets का उपयोग करें
client = Groq(api_key="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")

# =====================================================================
# 3. DATA FUNCTIONS
# =====================================================================
def get_live_gold_price():
    return 2385.0 # आप इसे अपनी लाइव API से रिप्लेस कर सकते हैं

@st.cache_data(ttl=60)
def fetch_gold_news():
    rss_url = "https://www.investing.com/rss/news_14.rss"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5]

# =====================================================================
# 4. AI ENGINE (GROQ VERSION)
# =====================================================================
def get_ai_analysis(live_spot):
    prompt = f"""
    You are an expert XAUUSD trader. Current price: {live_spot}. 
    Provide response in Hindi (Devanagari script).
    1. Dynamic Intraday Key Levels (PDH, PDL, R1, S1).
    2. Live Trade Setup (Bias, Entry, SL, TP, RR).
    3. AI News Interpreter with impact on Gold/Indian Market.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# =====================================================================
# 5. UI LAYOUT
# =====================================================================
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("### 🚀 XAU/USD Live Spot Price")
    # TradingView Ticker Here
    st.info("Live Chart Placeholder") 

with top_col2:
    st.markdown("### 📊 HTF Alignment")
    cols = st.columns(4)
    cols[0].markdown('<div class="metric-card"><div class="timeframe-title">5M</div><span class="sell-text">🔴 SELL</span></div>', unsafe_allow_html=True)
    cols[1].markdown('<div class="metric-card"><div class="timeframe-title">15M</div><span class="sell-text">🔴 SELL</span></div>', unsafe_allow_html=True)
    cols[2].markdown('<div class="metric-card"><div class="timeframe-title">1H</div><span class="neutral-text">⚪ NEUT</span></div>', unsafe_allow_html=True)
    cols[3].markdown('<div class="metric-card"><div class="timeframe-title">4H</div><span class="buy-text">🟢 BUY</span></div>', unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📰 Live Alpha News Flow")
    for item in fetch_gold_news():
        with st.container(border=True):
            st.subheader(item.title)
            st.markdown(f"[Source Link]({item.link})")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Reset & Refresh Terminal", type="primary"):
        st.rerun()
    
    with st.spinner("Groq Llama-3.3 Analyzing..."):
        analysis = get_ai_analysis(get_live_gold_price())
        st.markdown(analysis)
