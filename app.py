import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal v2", layout="wide", initial_sidebar_state="collapsed")

# CSS Styling (HTF Meters)
st.markdown("""
<style>
    .metric-card { background-color: #ffffff; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; box-shadow: 0px 2px 4px rgba(0,0,0,0.1); }
    .timeframe-title { font-size: 12px; font-weight: bold; color: #64748b; }
    .status-box { font-weight: 800; font-size: 14px; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Wolf Alpha Terminal | XAU/USD")

# 2. GROQ & DATA SETUP
client = Groq(api_key="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")

def get_meter_color(status):
    if "BUY" in status: return "color: #089981;"
    if "SELL" in status: return "color: #f23645;"
    return "color: #64748b;"

# 3. UI LAYOUT: TOP SECTION (Chart + Meters)
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light", "locale": "en"}
      </script>
    </div>
    """, height=120)

with top_col2:
    st.markdown("### 📊 HTF Alignment Meters")
    # यहाँ आप अपनी मैन्युअल या API आधारित मीटर वैल्यू डाल सकते हैं
    tf_data = [("5M", "SELL"), ("15M", "SELL"), ("1H", "NEUT"), ("4H", "BUY")]
    cols = st.columns(4)
    for i, (tf, status) in enumerate(tf_data):
        cols[i].markdown(f'''
        <div class="metric-card">
            <div class="timeframe-title">{tf}</div>
            <div class="status-box" style="{get_meter_color(status)}">{status}</div>
        </div>
        ''', unsafe_allow_html=True)

st.write("---")

# 4. NEWS ENGINE (Investing.com & FXStreet)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📰 Live Market News (Investing & FXStreet)")
    # मल्टीपल सोर्सेज से डेटा फेंचिंग
    news_sources = [
        "https://www.investing.com/rss/news_14.rss",
        "https://www.fxstreet.com/rss"
    ]
    for url in news_sources:
        feed = feedparser.parse(url)
        for item in feed.entries[:3]: # हर सोर्स से 3 खबरें
            with st.container(border=True):
                st.subheader(item.title)
                st.markdown(f"[Read More]({item.link})")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Analyze Market Bias"):
        with st.spinner("Groq Analyzing..."):
            # प्रॉम्प्ट में Investing/FXStreet का डेटा पास किया जा सकता है
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "Analyze XAUUSD news. Provide Hindi analysis with SMC levels and Actionable Trade Setup."}]
            )
            st.markdown(completion.choices[0].message.content)
