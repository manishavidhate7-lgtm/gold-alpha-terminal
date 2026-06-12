import streamlit as st
import feedparser
import os
import urllib.request
import json
from google.genai import Client
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# =====================================================================
# 1. फिक्स्ड क्लाइंट सेटअप (इसे ध्यान से देखें)
# =====================================================================
def get_client():
    try:
        # सीक्रेट्स से की लें
        api_key = st.secrets["GEMINI_API_KEY"]
        return Client(api_key=api_key)
    except Exception as e:
        return None

client = get_client()

# =====================================================================
# 2. अनुवाद और एआई फंक्शन
# =====================================================================
def translate_to_hindi(text):
    try:
        return GoogleTranslator(source='auto', target='hi').translate(text)
    except:
        return text

def get_ai_analysis(title, content):
    if not client:
        return "AI API Key missing or error."
    
    try:
        prompt = f"Analyze this financial news: {title}. {content}. Give 3 short points."
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return translate_to_hindi(response.text)
    except Exception as e:
        return "विश्लेषण अभी उपलब्ध नहीं है।"

# =====================================================================
# 3. बाकी कोड... (पुराना वाला ही रखें)
# =====================================================================
# यहाँ अपना फीड और लेआउट वाला कोड पेस्ट करें
