import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

st.title("⚡ Wolf Alpha Terminal | XAU/USD")

# 2. GROQ SETUP
client = Groq(api_key="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")

# 3. AI LOGIC (Spot Price Base)
def get_ai_analysis():
    # यहाँ स्पॉट प्राइस को डायनामिक बनाने के लिए आप अपनी API का उपयोग कर सकते हैं
    spot_price = 4177.465 
    prompt = f"""
    Analyze XAUUSD current spot price: {spot_price}.
    Return output EXACTLY in Hindi (Devanagari script) with:
    1. Dynamic Intraday Key Levels (PDH, PDL, R1, S1) based on {spot_price}.
    2. Live Trade Setup (Bias, Entry, SL, TP, RR).
    3. AI News Interpreter (Simple Hindi breakdown).
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# 4. LAYOUT
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light", "locale": "en"}
      </script>
    </div>
    """, height=130)

with top_col2:
    st.markdown("### 📊 HTF Alignment Meters")
    # विजिबल मीटर सेक्शन (Inline Style के साथ)
    m_cols = st.columns(4)
    data = [("5M", "SELL", "#f23645"), ("15M", "SELL", "#f23645"), ("1H", "NEUT", "#64748b"), ("4H", "BUY", "#089981")]
    for i, (tf, status, color) in enumerate(data):
        m_cols[i].markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 8px; text-align: center; background: #fff;">
            <div style="font-size: 12px; font-weight: bold; color: #64748b;">{tf}</div>
            <div style="font-size: 16px; font-weight: 900; color: {color};">{status}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

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
