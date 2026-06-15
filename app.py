import streamlit as st
import streamlit.components.v1 as components
import feedparser
import os
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")
st.title("⚡ Wolf Alpha Pro Terminal | Live")

# 2. AI ANALYZER SETUP
# सुनिश्चित करें कि स्ट्रीमलिट Secrets में GROQ_API_KEY सेट है
api_key = st.secrets.get("GROQ_API_KEY") 
client = Groq(api_key=api_key) if api_key else None

def get_single_news_impact(news_title):
    if not client:
        return "Error: API Key missing in Secrets."
    
    prompt = f"Analyze: '{news_title}'. Impact on XAU/USD (High/Med/Low) + Reasoning."
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}" # यह आपको बताएगा कि 'Rate limit' है या 'Invalid key'

# 3. LAYOUT
col_l, col_r = st.columns([2, 1])

with col_l:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""
    <iframe src="https://www.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=15&theme=light" width="100%" height="400" frameborder="0"></iframe>
    """, height=420)

with col_r:
    st.markdown("### 📊 Market Technical Trend")
    components.html("""
    <iframe src="https://www.tradingview.com/embed-widget/technical-analysis/?symbol=OANDA:XAUUSD&interval=15m&theme=light" width="100%" height="400" frameborder="0"></iframe>
    """, height=420)

# 4. NEWS SECTION
st.header("📰 Live Market News & AI Analyser")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]

for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.expander(item.title):
            if st.button("Analyze News", key=item.title):
                with st.spinner("AI analyzing..."):
                    st.markdown(get_single_news_impact(item.title))
