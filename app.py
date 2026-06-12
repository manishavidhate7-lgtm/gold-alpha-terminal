import streamlit as st
import feedparser
import streamlit.components.v1 as components
from groq import Groq

# 1. PAGE SETUP
st.set_page_config(page_title="Wolf Alpha Terminal | XAU/USD", layout="wide", initial_sidebar_state="collapsed")

client = Groq(api_key="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")

# 2. AI LOGIC (News Analysis Engine)
def get_ai_analysis(news_content):
    prompt = f"""
    You are a professional Market Analyst. Analyze the following news and provide a structured impact report in English:
    
    NEWS DATA: {news_content}
    
    Provide the output in this EXACT format:
    
    ### 📊 Market Impact Analysis
    1. **Summary:** Brief 2-line summary of the news.
    2. **XAU/USD Impact:** [High/Medium/Low] - Explanation.
    3. **Relevant Pair Impact (e.g., USD/INR or EUR/USD):** [High/Medium/Low] - Explanation.
    4. **Indian Market (Nifty/Sensex) Impact:** [High/Medium/Low] - Explanation.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Terminal | XAU/USD")

# News Fetching Logic
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
news_data = ""
for url in sources:
    for item in feedparser.parse(url).entries[:3]:
        news_data += f"- {item.title}\n"

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📰 Live Market News")
    st.text(news_data) # ये न्यूज़ डेटा हमने वेरिएबल में ले लिया

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Analyze Live News Impact"):
        with st.spinner("Processing news impact..."):
            analysis = get_ai_analysis(news_data)
            st.markdown(analysis)
