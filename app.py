import streamlit as st
import feedparser
import streamlit.components.v1 as components
import os
import time
import urllib.request
import json
import google.genai as genai
from google.genai import types
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# =====================================================================
# 1. PAGE SETUP
# =====================================================================
st.set_page_config(page_title="XAUUSD Alpha Terminal v2", layout="wide", initial_sidebar_state="collapsed")

# CSS वही पुराना वाला (जो आपने पहले इस्तेमाल किया था) - उसे रहने दें।
st.markdown("""
<style>
    .ai-box-container { color: #1e293b !important; font-size: 14px !important; }
    .stMarkdown h3 { font-size: 15px !important; font-weight: 800 !important; color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ XAU/USD Alpha Terminal v2")

# =====================================================================
# 2. CLIENT SETUP
# =====================================================================
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def get_live_gold_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return float(json.loads(response.read().decode())['pax-gold']['usd'])
    except:
        return 2385.0

@st.cache_data(ttl=30)
def fetch_gold_news():
    rss_url = "https://finance.yahoo.com/rss/headline?s=GC=F"
    feed = feedparser.parse(rss_url)
    news_items = []
    for entry in feed.entries[:5]:
        summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()
        news_items.append({"title": entry.title, "summary": summary, "link": entry.link})
    return news_items

# =====================================================================
# 3. TRANSLATION ENGINE
# =====================================================================
def translate_to_hindi(text):
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text)
    except:
        return text

# =====================================================================
# 4. AI DESK ENGINE
# =====================================================================
def get_ai_analysis(title, content):
    prompt = f"Analyze this financial news for a trader. Title: {title}. Content: {content}. Provide output in 6 short bullet points in English."
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    
    # यहाँ से हिंदी में कन्वर्ट होकर आउटपुट निकलेगा
    raw = response.text
    return translate_to_hindi(raw)

# =====================================================================
# 5. UI LAYOUT
# =====================================================================
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.header("📰 Live Alpha News Flow")
    news = fetch_gold_news()
    for item in news:
        with st.container(border=True):
            st.markdown(f"**{item['title']}**")
            st.caption(item['summary'][:150] + "...")

with col2:
    st.header("🤖 Advanced AI Desk")
    if st.button("🔄 Refresh Analysis"):
        st.cache_data.clear()
        st.rerun()
    
    news = fetch_gold_news()
    for item in news:
        with st.spinner("हिंदी में विश्लेषण हो रहा है..."):
            analysis = get_ai_analysis(item['title'], item['summary'])
            st.markdown(f"### 🔍 {translate_to_hindi(item['title'])}")
            st.markdown(analysis)
            st.write("---")
