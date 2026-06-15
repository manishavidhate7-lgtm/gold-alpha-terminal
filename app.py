import streamlit as st
import streamlit.components.v1 as components
import feedparser
import yfinance as yf
import time
from groq import Groq

# 1. CACHING DATA to avoid Rate Limit Errors
@st.cache_data(ttl=300) # डेटा 5 मिनट तक कैश रहेगा
def get_market_trends():
    ticker = yf.Ticker("GC=F") 
    trends = {}
    intervals = {"5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h"}
    bullish_count = 0
    
    for label, interval in intervals.items():
        # हर रिक्वेस्ट के बीच थोड़ा ब्रेक लें
        time.sleep(1) 
        data = ticker.history(period="1d", interval=interval)
        if not data.empty and len(data) >= 2:
            trends[label] = "Bullish" if data['Close'].iloc[-1] > data['Close'].iloc[-2] else "Bearish"
            if trends[label] == "Bullish": bullish_count += 1
        else:
            trends[label] = "Neutral"
    return trends, bullish_count

# --- बाकी का स्ट्रक्चर वही रहेगा ---
