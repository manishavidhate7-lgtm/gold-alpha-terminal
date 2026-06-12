import streamlit as st
import feedparser
from groq import Groq
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# Page Config
st.set_page_config(page_title="Wolf Terminal Pro", layout="wide")

# --- 1. Client Setup ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key missing in Secrets. Please configure!")
    st.stop()

# --- 2. Translation Engine ---
def translate_to_hindi(text):
    if not text: return ""
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text[:500])
    except:
        return text

# --- 3. News Fetching ---
@st.cache_data(ttl=60)
def get_news():
    try:
        feed = feedparser.parse("https://finance.yahoo.com/rss/headline?s=GC=F")
        return feed.entries[:3]
    except:
        return []

# --- 4. Main Dashboard UI ---
st.title("⚡ Wolf Alpha Terminal | XAU/USD")
st.write("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📰 Live Market News")
    for item in get_news():
        with st.container(border=True):
            st.markdown(f"**{translate_to_hindi(item.title)}**")
            st.caption(translate_to_hindi(BeautifulSoup(item.summary, "html.parser").get_text()))

with col2:
    st.header("🤖 AI Market Intelligence")
    if st.button("🚀 Analyze Market Bias"):
        with st.spinner("Analyzing with Groq Llama 3..."):
            try:
                # Prompting for high-impact trading analysis
                prompt = "Analyze XAUUSD current market news and provide a Bullish/Bearish bias. Give 3 key points for intraday trading. Keep it professional and short."
                
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                raw_response = completion.choices[0].message.content
                st.markdown(translate_to_hindi(raw_response))
                
            except Exception as e:
                st.error("AI engine could not process request.")

st.sidebar.success("Wolf Terminal v2.0 Online")
