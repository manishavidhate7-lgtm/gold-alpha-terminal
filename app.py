import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

# 2. GROQ SETUP
client = Groq(api_key="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")

# AI FUNCTION: XAUUSD स्पॉट प्राइस को बेस मानकर लेवल्स
def get_ai_analysis():
    # XAUUSD Spot Price (इसे लाइव करने के लिए आप API से रिप्लेस कर सकते हैं)
    spot_price = 2385.0 
    prompt = f"""
    Analyze XAUUSD current spot price: {spot_price}.
    Return output in Hindi (Devanagari script) with:
    1. Dynamic Intraday Key Levels (PDH, PDL, R1, S1) calculated based on {spot_price}.
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

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Terminal | XAU/USD")

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
    # विजिबल मीटर फिक्स
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("5M", "SELL")
    with m2: st.metric("15M", "SELL")
    with m3: st.metric("1H", "NEUT")
    with m4: st.metric("4H", "BUY")
    # कलर फिक्स
    st.markdown("""<style>
        [data-testid='stMetricValue'] { font-size: 18px !important; }
        [data-testid='stMetricValue']:nth-child(1) { color: red; }
    </style>""", unsafe_allow_html=True)

st.write("---")

# 4. NEWS & AI DESK
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📰 Live Market News")
    sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
    for url in sources:
        for item in feedparser.parse(url).entries[:3]:
            with st.container(border=True):
                st.subheader(item.title)
                st.markdown(f"[Read More]({item.link})")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Analyze Market Bias"):
        with st.spinner("Analyzing with Spot Price..."):
            st.markdown(get_ai_analysis())
