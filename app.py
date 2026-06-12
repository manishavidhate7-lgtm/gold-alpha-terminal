import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

# 2. GROQ SETUP
client = Groq(api_key="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")

# 3. AI LOGIC
def get_ai_analysis():
    spot_price = 4177.465 
    prompt = f"""
    Analyze XAUUSD current spot price: {spot_price}.
    Return output in Hindi (Devanagari script) with:
    1. Dynamic Intraday Key Levels (PDH, PDL, R1, S1) based on {spot_price}.
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

# 4. UI LAYOUT
st.title("⚡ Wolf Alpha Terminal | XAU/USD")

top1, top2 = st.columns([1, 1])

with top1:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light", "locale": "en"}
      </script>
    </div>
    """, height=130)

with top2:
    st.markdown("### 📊 HTF Alignment Meters")
    m1, m2, m3, m4 = st.columns(4)
    # border=True का इस्तेमाल किया है ताकि हर हाल में डिब्बा दिखे
    with m1:
        with st.container(border=True):
            st.markdown("<div style='text-align:center'>5M<br><b style='color:red'>SELL</b></div>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown("<div style='text-align:center'>15M<br><b style='color:red'>SELL</b></div>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown("<div style='text-align:center'>1H<br><b style='color:grey'>NEUT</b></div>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown("<div style='text-align:center'>4H<br><b style='color:green'>BUY</b></div>", unsafe_allow_html=True)

st.write("---")

# 5. NEWS & AI DESK
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
        with st.spinner("Analyzing market..."):
            st.markdown(get_ai_analysis())
