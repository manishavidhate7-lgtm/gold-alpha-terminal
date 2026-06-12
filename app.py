import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

# 2. PRO-STYLE CSS FOR METERS & LAYOUT
st.markdown("""
<style>
    .metric-card { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #e2e8f0; 
        text-align: center; 
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05); 
    }
    .timeframe-title { font-size: 12px; font-weight: bold; color: #64748b; margin-bottom: 5px; }
    .status-box { font-weight: 900; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Wolf Alpha Terminal | XAU/USD")

# 3. GROQ CLIENT SETUP
client = Groq(api_key="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")

def get_ai_analysis():
    prompt = """
    Analyze XAUUSD market news. Provide output in Hindi (Devanagari script) with:
    1. Dynamic Intraday Key Levels (PDH, PDL, R1, S1).
    2. Live Trade Setup (Bias, Entry, SL, TP, RR).
    3. AI News Interpreter with Bullish/Bearish impact.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# 4. TOP ROW: CHART & METERS
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light", "locale": "en"}
      </script>
    </div>
    """, height=130)

with top_col2:
    st.markdown("### 📊 HTF Alignment Meters")
    tf_data = [("5M", "SELL", "#f23645"), ("15M", "SELL", "#f23645"), ("1H", "NEUT", "#64748b"), ("4H", "BUY", "#089981")]
    cols = st.columns(4)
    for i, (tf, status, color) in enumerate(tf_data):
        cols[i].markdown(f'''
        <div class="metric-card">
            <div class="timeframe-title">{tf}</div>
            <div class="status-box" style="color: {color};">{status}</div>
        </div>
        ''', unsafe_allow_html=True)

st.write("---")

# 5. BOTTOM ROW: NEWS & AI DESK
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📰 Live Market News (Investing & FXStreet)")
    sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
    for url in sources:
        for item in feedparser.parse(url).entries[:3]:
            with st.container(border=True):
                st.subheader(item.title)
                st.markdown(f"[Read More]({item.link})")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Analyze Market Bias"):
        with st.spinner("AI analyzing..."):
            st.markdown(get_ai_analysis())
