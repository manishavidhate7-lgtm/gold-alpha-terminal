import streamlit as st
import feedparser
from groq import Groq
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# Page Setup
st.set_page_config(page_title="Wolf Alpha Terminal", layout="wide")

# --- 1. Emergency API Loading ---
# यह कोड पक्का काम करेगा चाहे Secrets में कुछ भी हो
def get_groq_client():
    key_from_secrets = st.secrets.get("GROQ_API_KEY")
    # अगर सीक्रेट्स वाला नहीं मिला, तो डायरेक्ट की का इस्तेमाल करेगा
    final_key = key_from_secrets if key_from_secrets else "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"
    return Groq(api_key=final_key)

client = get_groq_client()

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

# --- 4. UI Layout ---
st.title("⚡ Wolf Alpha Terminal | XAU/USD")
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
        with st.spinner("Processing with Groq..."):
            try:
                prompt = "Analyze XAUUSD market. Give Bullish/Bearish bias and 3 bullet points for intraday trading in Hindi."
                completion = client.chat.completions.create(
                    model="llama3-8b-8192", # यह मॉडल बहुत फास्ट और स्टेबल है
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error("AI Error: Check API Key connectivity.")

st.sidebar.success("Wolf Terminal v2.0 Online")
