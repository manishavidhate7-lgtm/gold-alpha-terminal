import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE CONFIG
st.set_page_config(page_title="Wolf Alpha Pro Terminal", layout="wide")

st.title("⚡ Wolf Alpha Pro Terminal | Live")

# 2. LAYOUT
col_l, col_r = st.columns([2, 1])

with col_l:
    st.markdown("### 🚀 Live Spot Chart")
    components.html("""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart" style="height:400px; width:100%;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
      "width": "100%", "height": 400, "symbol": "OANDA:XAUUSD", "interval": "5",
      "timezone": "Etc/UTC", "theme": "light", "style": "1", "locale": "en",
      "toolbar_bg": "#f1f3f6", "enable_publishing": false, "container_id": "tradingview_chart"
      });
      </script>
    </div>
    """, height=420)

with col_r:
    st.markdown("### 📊 Market Technical Trend")
    # यह विजेट अपने आप Bullish/Bearish बता देगा
    components.html("""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {
      "interval": "15m",
      "width": "100%",
      "isTransparent": false,
      "height": 400,
      "symbol": "OANDA:XAUUSD",
      "showIntervalTabs": true,
      "displayMode": "single",
      "locale": "en",
      "colorTheme": "light"
      }
      </script>
    </div>
    """, height=420)

# 3. HEATMAP
st.markdown("### 🗺️ Currency Strength Heatmap")
components.html("""<iframe src="https://www.tradingview.com/embed-widget/forex-heat-map/" width="100%" height="400" frameborder="0"></iframe>""", height=420)

# 4. NEWS SECTION
st.header("📰 Live Market News")
import feedparser
for item in feedparser.parse("https://www.investing.com/rss/news_14.rss").entries[:5]:
    st.write(f"• {item.title}")
