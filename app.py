import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

client = Groq(api_key="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")

# 2. AI NEWS ANALYST (Individual Impact)
def get_single_news_impact(news_title):
    prompt = f"""
    Analyze this news headline for market impact: "{news_title}"
    Provide output in this exact format:
    - **Impact on XAU/USD:** [High/Medium/Low]
    - **Impact on USD/INR:** [High/Medium/Low]
    - **Impact on Indian Market (Nifty/Sensex):** [High/Medium/Low]
    - **Reasoning:** Brief explanation.
    """
    completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Terminal | XAU/USD")

# Top Section (Chart & Meters)
top1, top2 = st.columns([1, 1])
with top1:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "colorTheme": "light"}</script></div>""", height=130)

with top2:
    st.markdown("### 📊 HTF Alignment Meters")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True): st.markdown("<div style='text-align:center'>5M<br><b style='color:red'>SELL</b></div>", unsafe_allow_html=True)
    with m2:
        with st.container(border=True): st.markdown("<div style='text-align:center'>15M<br><b style='color:red'>SELL</b></div>", unsafe_allow_html=True)
    with m3:
        with st.container(border=True): st.markdown("<div style='text-align:center'>1H<br><b style='color:grey'>NEUT</b></div>", unsafe_allow_html=True)
    with m4:
        with st.container(border=True): st.markdown("<div style='text-align:center'>4H<br><b style='color:green'>BUY</b></div>", unsafe_allow_html=True)

st.write("---")

# 4. NEWS & SEPARATE AI IMPACT
st.header("📰 Live Market News & AI Impact")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]

# हर खबर के लिए अलग कॉलम
for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.container(border=True):
            col_news, col_ai = st.columns([2, 1])
            with col_news:
                st.subheader(item.title)
                st.markdown(f"[Read More]({item.link})")
            with col_ai:
                # Key=item.title इसे यूनिक बटन बनाता है
                if st.button("Analyze Impact", key=item.title):
                    with st.spinner("AI analyzing..."):
                        st.markdown(get_single_news_impact(item.title))
