import streamlit as st
import streamlit.components.v1 as components
import feedparser
import time
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. AI ANALYZER SETUP
client = Groq(api_key="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")

def get_single_news_impact(news_title):
    prompt = f"Analyze: '{news_title}'. Format: Impact on XAU/USD, USD/INR, Nifty (High/Med/Low) + Reasoning."
    try:
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        return completion.choices[0].message.content
    except Exception as e: 
        return f"Analysis unavailable: {str(e)}"

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")

# (Charts, Calendar, Heatmap यहाँ पहले वाले कोड की तरह ही रखें...)

# 4. FIXED NEWS SECTION WITH ANALYSER
st.header("📰 Live Market News & AI Analyser")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]

for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.container(border=True):
            col_n, col_a = st.columns([3, 1])
            with col_n: 
                st.write(item.title)
            with col_a:
                if st.button("Analyze", key=item.title):
                    with st.spinner("AI analyzing..."): 
                        analysis = get_single_news_impact(item.title)
                        st.markdown(analysis)
