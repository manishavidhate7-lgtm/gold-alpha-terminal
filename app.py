import streamlit as st
import feedparser
from google.genai import Client
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")

# --- 1. Client Setup ---
def get_client():
    try:
        return Client(api_key=st.secrets["GEMINI_API_KEY"])
    except:
        return None

client = get_client()

# --- 2. News Fetching ---
@st.cache_data(ttl=60)
def fetch_news():
    try:
        feed = feedparser.parse("https://finance.yahoo.com/rss/headline?s=GC=F")
        return feed.entries[:3]
    except:
        return []

# --- 3. Translation Helper ---
def safe_translate(text):
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text[:300])
    except:
        return text

# --- 4. Dashboard UI ---
st.title("XAU/USD Alpha Terminal")

col1, col2 = st.columns([1, 1])

# Column 1: News List (Always visible)
with col1:
    st.header("📰 News Flow")
    news = fetch_news()
    for item in news:
        with st.container(border=True):
            st.markdown(f"**{safe_translate(item.title)}**")
            st.caption(safe_translate(BeautifulSoup(item.summary, "html.parser").get_text()))

# Column 2: AI Desk (Logic)
with col2:
    st.header("🤖 AI Analysis & Bias")
    if client:
        try:
            # Full prompt for Bias and Analysis
            prompt = "Analyze XAUUSD market bias (Bullish/Bearish) and provide 3 key points based on the latest news. Answer in Hindi."
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt
            )
            st.success("Market Bias: Active")
            st.markdown(response.text)
        except Exception as e:
            st.error("AI Analysis failed. Check API Key permissions.")
    else:
        st.warning("API Key missing. Please check Streamlit Secrets.")
