import streamlit as st
import feedparser
import json
import urllib.request
from bs4 import BeautifulSoup
from google.genai import Client
from deep_translator import GoogleTranslator

st.set_page_config(layout="wide")
st.title("XAU/USD Alpha Terminal")

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

# --- 3. Simple Safe Translation ---
def safe_translate(text):
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text[:500])
    except:
        return text

# --- 4. Main UI ---
news = fetch_news()

if not news:
    st.write("अभी कोई न्यूज़ लोड नहीं हो पाई है।")
else:
    for item in news:
        st.subheader(safe_translate(item.title))
        
        # एआई एनालिसिस के लिए सेफ कॉल
        if client:
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=f"Summarize: {item.title}"
                )
                st.write(safe_translate(response.text))
            except Exception as e:
                st.write("एआई विश्लेषण में तकनीकी समस्या।")
        else:
            st.write("API Key नहीं मिली।")
        st.divider()
