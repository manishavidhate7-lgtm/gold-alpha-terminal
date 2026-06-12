import streamlit as st
import feedparser
import streamlit.components.v1 as components
import time
from groq import Groq

# 1. PAGE SETUP
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

# 2. GROQ SETUP
client = Groq(api_key="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")

# 3. AI ENGINE WITH PROMPT
def get_ai_analysis(live_spot):
    prompt = f"""
    You are an expert XAUUSD trader. Current price: {live_spot}.
    Return output EXACTLY in Hindi (Devanagari script) using this layout:

    ### 📋 Dynamic Intraday Key Levels (SMC Grid)
    - **PDH (Previous Day High):** Calculate levels based on {live_spot}
    - **PDL (Previous Day Low):** Calculate levels based on {live_spot}
    - **Resistance 1 (R1):** Calculate levels based on {live_spot}
    - **Support 1 (S1):** Calculate levels based on {live_spot}

    ### 🎯 Live Trade Setup Section (Actionable)
    - **Bias:** [BUY/SELL]
    - **Entry:** {live_spot}
    - **SL:** [Price]
    - **TP:** [Price]
    - **RR:** [Ratio]

    ### 🔍 AI News Interpreter & Market Impact Panel
    - Explain news impact in simple Hindi.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# 4. UI LAYOUT
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("### 🚀 XAU/USD Live Spot Price")
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {"symbol": "OANDA:XAUUSD", "width": "100%", "isTransparent": false, "colorTheme": "light", "locale": "en"}
      </script>
    </div>
    """, height=130)

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
    rss_url = "https://www.investing.com/rss/news_14.rss"
    for item in feedparser.parse(rss_url).entries[:5]:
        with st.container(border=True):
            st.subheader(item.title)
            st.markdown(f"[Source Link]({item.link})")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Reset & Refresh Terminal", type="primary"):
        st.rerun()
    
    with st.spinner("Analyzing Market..."):
        st.markdown(get_ai_analysis(2385.0))
