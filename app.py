import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

client = Groq(api_key="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")

# 2. AI NEWS INTERPRETER ENGINE
def get_ai_analysis(news_content):
    prompt = f"""
    You are an expert market analyst. Analyze ALL the following news headlines provided below and provide a structured impact report in English:
    
    NEWS HEADLINES:
    {news_content}
    
    Output Format:
    ### 📊 Market Impact Analysis
    1. **Summary:** A concise 2-3 sentence summary of the combined news.
    2. **XAU/USD Impact:** [High/Medium/Low] - Detailed reasoning based on these headlines.
    3. **Relevant Pair (USD/INR) Impact:** [High/Medium/Low] - Detailed reasoning.
    4. **Indian Market (Nifty/Sensex) Impact:** [High/Medium/Low] - Detailed reasoning.
    """
    completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Terminal | XAU/USD")

# TOP ROW: CHART & METERS
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

# BOTTOM ROW: NEWS & AI
col1, col2 = st.columns([1, 1], gap="large")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
all_news_list = [] # यहाँ सारी खबरें एक साथ जमा होंगी

with col1:
    st.header("📰 Live Market News")
    for url in sources:
        feed = feedparser.parse(url)
        for item in feed.entries[:5]: 
            all_news_list.append(item.title) # हर खबर को लिस्ट में डाल रहे हैं
            with st.container(border=True):
                st.write(item.title)
                st.markdown(f"[Read More]({item.link})")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Analyze All News Impact"):
        with st.spinner("AI analyzing all news..."):
            # अब यहाँ पूरी लिस्ट एक बड़े टेक्स्ट ब्लॉक में जा रही है
            full_news_text = "\n".join([f"- {news}" for news in all_news_list])
            st.markdown(get_ai_analysis(full_news_text))
