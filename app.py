import streamlit as st
import feedparser
from google.genai import Client
from deep_translator import GoogleTranslator

st.title("XAU/USD Alpha Terminal")

# 1. API Client setup
def get_client():
    try:
        # यहाँ 'GEMINI_API_KEY' वही नाम है जो आपने Streamlit Secrets में रखा है
        return Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"API Key Error: {e}")
        return None

client = get_client()

# 2. News
feed = feedparser.parse("https://finance.yahoo.com/rss/headline?s=GC=F")

# 3. Process
for item in feed.entries[:3]:
    # ट्रांसलेट हेडलाइन
    try:
        title_hi = GoogleTranslator(source='auto', target='hi').translate(item.title)
    except:
        title_hi = item.title
    
    st.subheader(title_hi)

    if client:
        try:
            # हम मॉडल को 'gemini-1.5-flash' इस्तेमाल करते हैं, यह सबसे स्टेबल है
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=f"Summarize in 2 short hindi lines: {item.title}"
            )
            st.write(response.text)
        except Exception as e:
            st.write("एआई अभी लोड नहीं हो रहा, की (Key) चेक करें।")
    st.divider()
