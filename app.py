import streamlit as st
import feedparser
from groq import Groq
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="Wolf Alpha Terminal", layout="wide")

# Groq क्लाइंट सेटअप - हमने की को यहाँ फिक्स कर दिया है
client = Groq(api_key="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")

# अनुवाद फ़ंक्शन
def translate_to_hindi(text):
    if not text: return ""
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text[:500])
    except:
        return text

# न्यूज़ फ़ेचिंग
@st.cache_data(ttl=60)
def get_news():
    try:
        feed = feedparser.parse("https://finance.yahoo.com/rss/headline?s=GC=F")
        return feed.entries[:3]
    except:
        return []

# यूआई लेआउट
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
        with st.spinner("Analyzing..."):
            try:
                # सीधे Groq को कॉल करें
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": "Analyze XAUUSD news. Give Bullish/Bearish bias and 3 bullet points for intraday in Hindi."}
                    ],
                    model="llama3-8b-8192",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.success("Wolf Terminal v2.0 Online")
