import streamlit as st
import feedparser
import streamlit.components.v1 as components
import time
import plotly.graph_objects as go
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

# 2. AI ANALYZER
client = Groq(api_key="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")

def get_sentiment_score():
    # यह फंक्शन AI से 1 से 10 के बीच स्कोर लेगा
    return 6 

def get_single_news_impact(news_title):
    prompt = f"Analyze: '{news_title}'. Format: Impact on XAU/USD, USD/INR, Nifty (High/Med/Low) + Reasoning."
    try:
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
        return completion.choices[0].message.content
    except: return "Analysis unavailable."

# 3. UI LAYOUT
st.title("⚡ Wolf Alpha Pro Terminal | Live")
col_left, col_mid, col_right = st.columns([1.5, 1, 1])

with col_left:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""<div class="tradingview-widget-container"><script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>{"symbol": "OANDA:XAUUSD", "width": "100%", "height": 300, "colorTheme": "light"}</script></div>""", height=320)

with col_mid:
    st.markdown("### 📊 Market Sentiment Gauge")
    score = get_sentiment_score()
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [-10, 10]}, 'bar': {'color': "darkblue"}, 'steps': [
            {'range': [-10, -2], 'color': "red"},
            {'range': [-2, 2], 'color': "gray"},
            {'range': [2, 10], 'color': "green"}]}
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("### 📅 Economic Calendar")
    components.html("""<iframe src="https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=1,2,3&features=datepicker,timezone&countries=25,32,37,72,5&calType=day&lang=1" width="100%" height="300" frameborder="0"></iframe>""", height=320)

st.write("---")

# 4. NEWS & ANALYZER
st.header("📰 Live Market News & AI Analyser")
sources = ["https://www.investing.com/rss/news_14.rss", "https://www.fxstreet.com/rss"]
for url in sources:
    for item in feedparser.parse(url).entries[:5]:
        with st.container(border=True):
            col_n, col_a = st.columns([3, 1])
            with col_n: st.write(item.title)
            with col_a:
                if st.button("Analyze", key=item.title):
                    with st.spinner("AI analyzing..."): st.markdown(get_single_news_impact(item.title))

# 5. AUTO-REFRESH
time.sleep(60)
st.rerun()
