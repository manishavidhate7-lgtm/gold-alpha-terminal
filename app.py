import streamlit as st
import feedparser
import streamlit.components.v1 as components
import os
import time
import urllib.request
import json
import google.genai as genai

# =====================================================================
# 1. PAGE SETUP & COMPLETE TEXT COLOR + HEADINGS SIZE FIX
# =====================================================================
st.set_page_config(
    page_title="XAUUSD Alpha Terminal v2", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# गैप्स और टेक्स्ट फॉर्मेटिंग का CSS
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fafbfc !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 98% !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.4rem !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0.6rem !important;
    }
    
    /* टेक्स्ट कलर और लाइन स्पेसिंग */
    [data-testid="stContentBlock"] h1, 
    [data-testid="stContentBlock"] h2, 
    [data-testid="stContentBlock"] h3, 
    [data-testid="stContentBlock"] p,
    .stMarkdown p, .stMarkdown h3 {
        color: #1e293b !important;
        line-height: 1.5 !important;
    }
    
    .ai-box-container {
        color: #1e293b !important;
        font-size: 14px !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .ai-box-container h1, .ai-box-container h2, .ai-box-container h3 {
        font-size: 15px !important;
        font-weight: 800 !important;
        margin-top: 10px !important;
        margin-bottom: 5px !important;
        color: #1e293b !important;
    }
    
    /* मीटर्स की स्टाइल */
    .meter-card { 
        background-color: #ffffff; 
        padding: 8px 10px; 
        border-radius: 6px; 
        border: 1px solid #e2e8f0; 
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.03);
    }
    .timeframe-title {
        font-size: 12px;
        font-weight: 700;
        color: #475569;
        margin-bottom: 4px;
    }
    .meter-bar-bg {
        background-color: #e2e8f0;
        border-radius: 4px;
        height: 6px;
        width: 100%;
        overflow: hidden;
        margin-top: 5px;
    }
    .meter-fill-sell { background-color: #f23645; height: 100%; width: 85%; }
    .meter-fill-buy { background-color: #089981; height: 100%; width: 90%; }
    .meter-fill-neut { background-color: #94a3b8; height: 100%; width: 50%; }
    
    .buy-text { color: #089981; font-weight: 800; font-size: 13px; }
    .sell-text { color: #f23645; font-weight: 800; font-size: 13px; }
    .neutral-text { color: #64748b; font-weight: 800; font-size: 13px; }
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
    components.html(tv_ticker_html, height=130)

with top_col2:
    st.markdown("### 📊 HTF Alignment Meters")
    htf_cols = st.columns(4)
    with htf_cols[0]: st.markdown('<div class="meter-card"><div class="timeframe-title">⏳ 5M</div><span class="sell-text">🔴 STRONG SELL</span><div class="meter-bar-bg"><div class="meter-fill-sell"></div></div></div>', unsafe_allow_html=True)
    with htf_cols[1]: st.markdown('<div class="meter-card"><div class="timeframe-title">⏳ 15M</div><span class="sell-text">🔴 SELL</span><div class="meter-bar-bg"><div class="meter-fill-sell" style="width:65%;"></div></div></div>', unsafe_allow_html=True)
    with htf_cols[2]: st.markdown('<div class="meter-card"><div class="timeframe-title">⏳ 1H</div><span class="neutral-text">⚪ NEUTRAL</span><div class="meter-bar-bg"><div class="meter-fill-neut"></div></div></div>', unsafe_allow_html=True)
    with htf_cols[3]: st.markdown('<div class="meter-card"><div class="timeframe-title">⏳ 4H</div><span class="buy-text">🟢 BUY</span><div class="meter-bar-bg"><div class="meter-fill-buy"></div></div></div>', unsafe_allow_html=True)

st.write("---")

# =====================================================================
# 6. AI TRADER ENGINE & DYNAMIC NEWS INTERPRETER (LINE BREAK FIXED)
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

    # 🚨 जेमिनी को साफ़ हिदायत कि हर पॉइंट के अंत में नई लाइन (\n\n) का उपयोग करे
    prompt_interpreter = f"""
    You are an expert global macro analyst. You MUST analyze ALL 5 stories provided in the list below sequentially. Do not skip any story.
    For each news item, write strictly in Hindi script (Devanagari font). 
    CRITICAL: Write each impact point on a completely new line. Do not combine them into a single paragraph.

    ### 🔍 AI News Interpreter & Market Impact Panel

    **📌 न्यूज़ हेडライン:** [Exact headline from the list]

    आसान शब्दों में मतलब: [Explain in simple Hindi what this news means]

    Forex (Gold/Dollar) पर असर: [🚀 BULLISH (तेजी) / 📉 BEARISH (मंदी) / ⚪ NEUTRAL - Simple Hindi explanation]

    Other Major Pairs पर असर: [State specific pairs like USDJPY, EURUSD, or GBPUSD and mark them 🚀 BULLISH or 📉 BEARISH with a 1-line reason in simple Hindi]

    Indian Market (Nifty/Bank Nifty) पर असर: [🚀 BULLISH (तेजी) / 📉 BEARISH (मंदी) / ⚪ NEUTRAL - Simple Hindi explanation]

    असर का लेवल (Impact Level): [🔴 High / 🟡 Medium / 🟢 Low]

    ---
    (Generate exactly 5 blocks matching the 5 stories below, leaving empty lines between every impact criteria)

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
        
        # 🚨 फॉलबैक ब्लॉक के अंदर डबल न्यू-लाइन (\n\n) देकर एक के नीचे एक आना पक्का किया
        fallback_blocks = []
        for item in news_data[:5]:
            is_high = "High" in item["impact"]
            gold_imp = "📉 BEARISH (मंदी) - डॉलर मजबूत होने से सोने के दाम गिर सकते हैं।" if is_high else "🚀 BULLISH (तेजी) - सोने में खरीदार एक्टिव हो सकते हैं।"
            pairs_imp = "🚀 USDJPY BULLISH (डॉलर मजबूत) | 📉 EURUSD BEARISH (यूरो कमजोर)" if is_high else "📉 USDJPY BEARISH (येन मजबूत) | 🚀 GBPUSD BULLISH"
            nifty_imp = "📉 BEARISH (मंदी) - भारतीय बाज़ारों में थोड़ी गिरावट आ सकती है।" if is_high else "⚪ NEUTRAL (कोई खास असर नहीं)।"
            
            block = f"""**📌 न्यूज़ हेडलाइन:** {str(item['title'])}

आसान शब्दों में मतलब: वैश्विक स्तर पर मैक्रो लिक्विडिटी और सेंट्रल बैंक की नीतियों से जुड़ा हुआ मुख्य अपडेट।

Forex (Gold/Dollar) पर असर: {gold_imp}

Other Major Pairs पर असर: {pairs_imp}

Indian Market (Nifty) पर असर: {nifty_imp}

असर का लेवल (Impact Level): {str(item['impact'])}

---"""
            fallback_blocks.append(block)
            
        fallback_interp = "### 🔍 AI News Interpreter & Market Impact Panel (Dynamic Flow)\n\n" + "\n\n".join(fallback_blocks)
        return fallback_main, fallback_interp

# =====================================================================
# 7. RESPONSIVE DUAL-COLUMN LAYOUT
# =====================================================================
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.header("📰 Live Alpha News Flow")
    
    @st.fragment(run_every=60)
    def show_live_news_stream():
        current_news = fetch_gold_news()
        st.caption(f"🔄 Auto-Refreshing: {time.strftime('%H:%M:%S')} (Every 60s)")
        
        for item in current_news:
            with st.container(border=True):
                st.markdown(f"**📢 {item['title']}**")
                st.caption(f"📅 {item['published']}")
                st.markdown(f"**Context:** {item['summary']}")
                st.markdown(f"**Impact:** {item['impact']} | **Gold:** `{item['reaction']}`")
                st.markdown(f"[Source Link]({item['link']})")
                
    show_live_news_stream()

with col2:
    st.header("🤖 Advanced AI Desk")
    
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
            
            st.markdown(f'<div class="ai-box-container">', unsafe_allow_html=True)
            st.markdown(ai_main_output)
            st.write("---")
            with st.container(border=True):
                st.markdown(ai_interpreter_output)
            st.markdown('</div>', unsafe_allow_html=True)
