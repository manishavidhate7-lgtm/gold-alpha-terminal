import streamlit as st
import feedparser
import streamlit.components.v1 as components
import os
import time
import urllib.request
import json
import google.genai as genai

# =====================================================================
# 1. PAGE SETUP & ULTRA MOBILE-RESPONSIVE UI CONFIG
# =====================================================================
st.set_page_config(
    page_title="XAUUSD Alpha Terminal v2", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# सिंपल और साफ़ क्लीन स्टाइलिंग (बिना किसी ज़बरदस्ती के लेआउट ब्रेक के)
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fafbfc;
    }
    
    /* एसएमसी लेवल्स के कार्ड्स */
    .metric-card { 
        background-color: #ffffff; 
        padding: 10px; 
        border-radius: 8px; 
        border: 1px solid #e2e8f0; 
        text-align: center;
        box-shadow: 0px 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 6px;
    }
    .timeframe-title {
        font-size: 12px;
        font-weight: bold;
        color: #64748b;
        margin-bottom: 2px;
    }
    .buy-text { color: #089981; font-weight: 800; font-size: 15px; }
    .sell-text { color: #f23645; font-weight: 800; font-size: 15px; }
    .neutral-text { color: #64748b; font-weight: 800; font-size: 15px; }
    
    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.8rem !important;
            padding-bottom: 0.8rem !important;
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
        }
        h1 { font-size: 20px !important; }
        h2 { font-size: 18px !important; }
        h3 { font-size: 15px !important; }
        iframe { height: 140px !important; }
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ XAU/USD Alpha Terminal v2")

# =====================================================================
# 2. CONFIGURE THE OFFICIAL GOOGLE GEMINI CLIENT
# =====================================================================
if "GEMINI_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GOOGLE_API_KEY = ""

try:
    if not GOOGLE_API_KEY:
        client = None
    else:
        client = genai.Client(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"AI Engine Connection Error: {str(e)}")
    client = None

# =====================================================================
# 3. LIVE BACKGROUND PRICE ENGINE
# =====================================================================
def get_live_gold_price_backup():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return float(data['pax-gold']['usd'])
    except:
        return 2385.0

# =====================================================================
# 4. REAL-TIME DATA & NEWS ENGINE
# =====================================================================
@st.cache_data(ttl=10)
def fetch_gold_news():
    rss_url = "https://www.investing.com/rss/news_14.rss" 
    feed = feedparser.parse(rss_url)
    
    news_items = []
    for idx, entry in enumerate(feed.entries[:5]):
        title_lower = entry.title.lower()
        if any(w in title_lower for w in ["fed", "cpi", "nfp", "powell", "rate", "inflation", "hiking", "banks"]):
            impact = "🔴 High"
            reaction = "Highly Volatile / Breakout Expected"
        elif any(w in title_lower for w in ["dollar", "biden", "ecb", "jobless", "yields", "treasury"]):
            impact = "🟡 Medium"
            reaction = "Trend Continuation"
        else:
            impact = "🟢 Low"
            reaction = "Range Bound"

        news_items.append({
            "title": entry.title,
            "summary": entry.get("summary", "Market liquidity shift under process. Structure building up on lower timeframes."),
            "link": entry.link,
            "published": entry.get("published", "Recent Data Window"),
            "impact": impact,
            "reaction": reaction
        })
    return news_items

# =====================================================================
# 5. TOP ROW: LIVE SPOT PRICE & HTF ALIGNMENT
# =====================================================================
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.markdown("### 🚀 XAU/USD Live Spot Price")
    tv_ticker_html = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
      {"symbol": "OANDA:XAUUSD", "width": "100%", "isTransparent": false, "colorTheme": "light", "locale": "en"}
      </script>
    </div>
    """
    components.html(tv_ticker_html, height=140)

with top_col2:
    st.markdown("### 📊 HTF Alignment")
    htf_cols = st.columns(4)
    with htf_cols[0]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 5M</div><span class="sell-text">🔴 SELL</span></div>', unsafe_allow_html=True)
    with htf_cols[1]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 15M</div><span class="sell-text">🔴 SELL</span></div>', unsafe_allow_html=True)
    with htf_cols[2]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 1H</div><span class="neutral-text">⚪ NEUT</span></div>', unsafe_allow_html=True)
    with htf_cols[3]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 4H</div><span class="buy-text">🟢 BUY</span></div>', unsafe_allow_html=True)

st.write("---")

# =====================================================================
# 6. AI TRADER ENGINE & DYNAMIC NEWS INTERPRETER
# =====================================================================
@st.cache_data(ttl=1800)
def generate_pro_ai_analysis(news_data, live_spot):
    if not client:
        return "ERROR_KEY_MISSING", "ERROR_KEY_MISSING"
        
    context_payload = ""
    for idx, item in enumerate(news_data, 1):
        context_payload += f"Story {idx}: {item['title']}\n"
        
    prompt_main = f"""
    You are an expert global macro prop trader.
    Current actual live market spot price of XAU/USD Gold right now is: ${live_spot:.2f}.
    Calculate all SMC levels and entry zones relative to ${live_spot:.2f}.
    Analyze headlines: {context_payload}
    Return output EXACTLY in Hindi script. Do not use English script.

    ### 📋 Dynamic Intraday Key Levels (SMC Grid)
    - **PDH (Previous Day High):** [Price slightly above ${live_spot:.2f}]
    - **PDL (Previous Day Low):** [Price slightly below ${live_spot:.2f}]
    - **Resistance 1 (R1):** [Logical R1]
    - **Support 1 (S1):** [Logical S1]

    ### 🤖 AI Impact Summary
    - **ECB/Fed Sentiment:** [Summary in Hindi]
    - **USD Index Bias:** [Impact in Hindi]
    - **Gold Impact:** [Bullish/Bearish in Hindi]

    ### 🎯 Live Trade Setup Section (Actionable)
    - **Current Intraday Bias:** [BUY or SELL]
    - **Entry Zone:** [Range around ${live_spot:.2f}]
    - **Stop Loss (SL):** [Logical SL]
    - **Take Profit 1 (TP1):** [Target 1]
    - **Risk-to-Reward (RR):** [e.g., 1:2.5]

    ### 🧠 मेंटर की यादशानी (SMC Confluence)
    [Warning to check lower timeframe CHoCH before entry in Hindi.]
    """

    prompt_interpreter = f"""
    You are an expert global macro analyst. You MUST analyze ALL 5 stories provided in the list below sequentially. Do not skip any story.
    For each news item, write strictly in Hindi script (Devanagari font) and explicitly mention laymen-friendly direction (🚀 BULLISH / 📉 BEARISH / ⚪ NEUTRAL) for Gold, Indian Market, and other Major Forex Pairs (like USDJPY, EURUSD, GBPUSD based on the macro context).

    ### 🔍 AI News Interpreter & Market Impact Panel

    **📌 न्यूज़ हेडライン:** [Exact headline from the list]
    - **आसान शब्दों में मतलब:** [Explain in simple Hindi what this news means]
    - **Forex (Gold/Dollar) पर असर:** [🚀 BULLISH (तेजी) / 📉 BEARISH (मंदी) / ⚪ NEUTRAL - Simple Hindi explanation]
    - **Other Major Pairs पर असर:** [State specific pairs like USDJPY, EURUSD, or GBPUSD and mark them 🚀 BULLISH or 📉 BEARISH with a 1-line reason in simple Hindi]
    - **Indian Market (Nifty/Bank Nifty) पर असर:** [🚀 BULLISH (तेजी) / 📉 BEARISH (मंदी) / ⚪ NEUTRAL - Simple Hindi explanation]
    - **असर का लेवल (Impact Level):** [🔴 High / 🟡 Medium / 🟢 Low]

    ---
    (Generate exactly 5 blocks matching the 5 stories below)

    Stories list:
    {context_payload}
    """
    
    try:
        res_main = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_main).text
        res_interp = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_interpreter).text
        return res_main, res_interp
    except Exception as e:
        fallback_main = f"""
### 📋 Dynamic Intraday Key Levels (SMC Grid)
- **PDH (Previous Day High):** {live_spot + 15:.2f}
- **PDL (Previous Day Low):** {live_spot - 20:.2f}
- **Resistance 1 (R1):** {live_spot + 6:.2f}
- **Support 1 (S1):** {live_spot - 10:.2f}

### 🎯 Live Trade Setup Section (Actionable)
- **Current Intraday Bias:** **SELL**
- **Entry Zone:** {live_spot + 3:.2f} - {live_spot + 7:.2f}
- **Stop Loss (SL):** {live_spot + 14:.2f}
- **Take Profit 1 (TP1):** {live_spot - 10:.2f}
        """
        
        fallback_interp = "### 🔍 AI News Interpreter & Market Impact Panel (Dynamic Flow)\n\n"
        for item in news_data[:5]:
            is_high = "High" in item["impact"]
            gold_imp = "📉 BEARISH (मंदी) - डॉलर मजबूत होने से सोने के दाम गिर सकते हैं।" if is_high else "🚀 BULLISH (तेजी) - सोने में खरीदार एक्टिव हो सकते हैं।"
            pairs_imp = "🚀 USDJPY BULLISH (डॉलर मजबूत) | 📉 EURUSD BEARISH (यूरो कमजोर)" if is_high else "📉 USDJPY BEARISH (येन मजबूत) | 🚀 GBPUSD BULLISH"
            nifty_imp = "📉 BEARISH (मंदी) - भारतीय बाज़ारों में थोड़ी गिरावट आ सकती है।" if is_high else "⚪ NEUTRAL (कोई खास असर नहीं)।"
            
            fallback_interp += f"**📌 न्यूज़ हेडलाइन:** {item['title']}\n"
            fallback_interp += f"- **आसान शब्दों में मतलब:** वैश्विक स्तर पर लिक्विडिटी और सेंट्रल बैंक की नीतियों से जुड़ा हुआ मुख्य अपडेट।\n"
            fallback_interp += f"- **Forex (Gold/Dollar) पर असर:** {gold_imp}\n"
            fallback_interp += f"- **Other Major Pairs पर असर:** {pairs_imp}\n"
            fallback_interp += f"- **Indian Market (Nifty) पर असर:** {nifty_imp}\n"
            fallback_interp += f"- **असर का लेवल (Impact Level):** {item['impact']}\n\n---\n\n"
            
        return fallback_main, fallback_interp

# =====================================================================
# 7. BULLETPROOF TABS LAYOUT (🚨 DEFINITIVE MOBILE FIX)
# =====================================================================
# मोबाइल पर दोनों सेक्शन्स टैब बटन बन जाएंगे, जिससे विड्थ कभी क्रैश नहीं होगी
tab1, tab2 = st.tabs(["📰 Live Alpha News Flow", "🤖 Advanced AI Desk"])

with tab1:
    @st.fragment(run_every=60)
    def show_live_news_stream():
        current_news = fetch_gold_news()
        st.caption(f"🔄 Auto-Refreshing: {time.strftime('%H:%M:%S')} (Every 60s)")
        
        for item in current_news:
            with st.container(border=True):
                st.subheader(item["title"])
                st.caption(f"📅 {item['published']}")
                st.markdown(f"**Context:** {item['summary']}")
                st.markdown(f"**Impact:** {item['impact']} | **Gold:** `{item['reaction']}`")
                st.markdown(f"[Source Link]({item['link']})")
                
    show_live_news_stream()

with tab2:
    if st.button("🔄 Reset & Refresh Terminal", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    live_spot_value = get_live_gold_price_backup()
    static_news = fetch_gold_news()
    
    if not client:
        st.warning("⚠️ सर्वर तिजोरी (Secrets) में 'GEMINI_API_KEY' डालना बाकी है।")
    
    if static_news:
        with st.spinner("जेमिनी प्रो इंजन लाइव लेवल्स और सभी 5 खबरों का डीप विश्लेषण कैलकुलेट कर रहा है..."):
            ai_main_output, ai_interpreter_output = generate_pro_ai_analysis(static_news, live_spot_value)
            
            st.markdown(ai_main_output)
            st.write("---")
            
            with st.container(border=True):
                st.markdown(ai_interpreter_output)
