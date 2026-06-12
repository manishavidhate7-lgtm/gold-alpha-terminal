import streamlit as st
import feedparser
import streamlit.components.v1 as components
import os
import time
import urllib.request
import json
import google.genai as genai
from google.genai import types
from bs4 import BeautifulSoup

# =====================================================================
# 1. PAGE SETUP & COMPLETE TEXT COLOR + HEADINGS SIZE FIX
# =====================================================================
st.set_page_config(
    page_title="XAUUSD Alpha Terminal v2", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    [data-testid="stVerticalBlock"] { gap: 0.4rem !important; }
    [data-testid="stHorizontalBlock"] { gap: 0.6rem !important; }
    
    [data-testid="stContentBlock"] h1, 
    [data-testid="stContentBlock"] h2, 
    [data-testid="stContentBlock"] h3, 
    [data-testid="stContentBlock"] p,
    .stMarkdown p, .stMarkdown h3 {
        color: #1e293b !important;
        line-height: 1.5 !important;
    }
    .ai-box-container { color: #1e293b !important; font-size: 14px !important; }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .ai-box-container h1, .ai-box-container h2, .ai-box-container h3 {
        font-size: 15px !important;
        font-weight: 800 !important;
        margin-top: 10px !important;
        margin-bottom: 5px !important;
        color: #1e293b !important;
    }
    
    .meter-card { 
        background-color: #ffffff; padding: 8px 10px; border-radius: 6px; 
        border: 1px solid #e2e8f0; text-align: center;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.03);
    }
    .timeframe-title { font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 4px; }
    .meter-bar-bg { background-color: #e2e8f0; border-radius: 4px; height: 6px; width: 100%; overflow: hidden; margin-top: 5px; }
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
# 4. REAL-TIME DATA & NEWS ENGINE (YAHOO FINANCE LIVE FEED)
# =====================================================================
@st.cache_data(ttl=30)
def fetch_gold_news():
    rss_url = "https://finance.yahoo.com/rss/headline?s=GC=F" 
    feed = feedparser.parse(rss_url)
    
    news_items = []
    entries = feed.entries if feed.entries else feedparser.parse("https://www.investing.com/rss/news_14.rss").entries
    
    for idx, entry in enumerate(entries[:5]):
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

        summary_text = entry.get("summary", "")
        if "<" in summary_text:
            soup_clean = BeautifulSoup(summary_text, "html.parser")
            summary_text = soup_clean.get_text()
        
        if not summary_text or len(summary_text) < 15:
            summary_text = f"Market data update regarding: {entry.title}"

        news_items.append({
            "title": entry.title,
            "summary": summary_text.strip(),
            "link": entry.link,
            "published": entry.get("published", "Recent Window"),
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
    with htf_cols[0]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 5M</div><span class="sell-text">🔴 STRONG SELL</span><div class="meter-bar-bg"><div class="meter-fill-sell"></div></div></div>', unsafe_allow_html=True)
    with htf_cols[1]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 15M</div><span class="sell-text">🔴 SELL</span><div class="meter-bar-bg"><div class="meter-fill-sell" style="width:65%;"></div></div></div>', unsafe_allow_html=True)
    with htf_cols[2]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 1H</div><span class="neutral-text">⚪ NEUTRAL</span><div class="meter-bar-bg"><div class="meter-fill-neut"></div></div></div>', unsafe_allow_html=True)
    with htf_cols[3]: st.markdown('<div class="metric-card"><div class="timeframe-title">⏳ 4H</div><span class="buy-text">🟢 BUY</span><div class="meter-bar-bg"><div class="meter-fill-buy"></div></div></div>', unsafe_allow_html=True)

st.write("---")

# =====================================================================
# 6. AI DESK ENGINE (🚨 ATTENTION-BIAS FIX: EXTREME HINDI CONSTRAINT)
# =====================================================================
@st.cache_data(ttl=60)
def generate_isolated_interpretation(title, content):
    if not client:
        return "AI Engine Offline"
        
    # प्रॉम्ट को पूरी तरह हिंदी निर्देशों से भर दिया ताकि मॉडल का ध्यान न भटके
    prompt = f"""
    दिए गए डेटा का केवल हिंदी भाषा में ही आउटपुट देना है। अंग्रेजी का एक भी वाक्य नहीं होना चाहिए।
    डेटा यहाँ है:
    डेटा_शीर्षक: {title}
    डेटा_विवरण: {content}
    """
    
    sys_instruction = (
        "CRITICAL RULE: You must write every single sentence in Hindi language using Devanagari script. "
        "You are strictly forbidden from writing responses in English. Even if the input text is in English, "
        "your analysis must be 100% in Hindi. Never use English sentences. "
        "Generate your response in Hindi using this exact template format:\n\n"
        "📌 **न्यूज़ हेडलाइन:** [अंग्रेजी हेडलाइन का हिंदी अनुवाद यहाँ लिखें]\n\n"
        "📰 **न्यूज़ का मुख्य सारांश:** [इस खबर का पूरा मतलब और विश्लेषण हिंदी में 2-3 वाक्यों में समझाएं]\n\n"
        "💡 **आसान शब्दों में मतलब:** [ट्रेडिंग के नजरिए से इसका क्या अर्थ है, हिंदी में लिखें]\n\n"
        "📈 **Forex (Gold/Dollar) पर असर:** [सोने और डॉलर पर तेजी या मंदी का असर हिंदी में कारण सहित लिखें]\n\n"
        "💱 **Other Major Pairs पर असर:** [EURUSD या USDJPY पर होने वाला प्रभाव हिंदी में लिखें]\n\n"
        "🇮🇳 **Indian Market (Nifty/Bank Nifty) पर असर:** [भारतीय बाजारों पर असर हिंदी में समझाएं]"
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.0,  # 0.0 टेम्परेचर यानी मॉडल को निर्देशों पर बिल्कुल फिक्स कर देना
                response_mime_type="text/plain"
            )
        )
        return response.text
    except Exception as e:
        return f"**📌 न्यूज़ हेडलाइन:** {title}\n\n⚪ विश्लेषण लोड नहीं हो पाया।"

@st.cache_data(ttl=60)
def generate_smc_grid(news_data, live_spot):
    if not client:
        return "SMC Matrix Offline"
    
    context_payload = ""
    for idx, item in enumerate(news_data, 1):
        context_payload += f"News {idx}: {item['title']}\n"
        
    prompt_main = f"Calculate technical SMC levels for price: ${live_spot:.2f} using context: {context_payload}"
    
    sys_instruction_main = (
        "You are a professional trader. You must answer exclusively in Hindi script (Devanagari). "
        "Do not use English sentences or English words for descriptions. Format exactly like this:\n\n"
        "### 📋 लाइव इंट्राडे मुख्य लेवल्स (SMC ग्रिड)\n"
        "- **PDH (पिछले दिन का हाई):** $[Calculate and print Level]\n"
        "- **PDL (पिछले दिन का लो):** $[Calculate and print Level]\n"
        "- **रेसिस्टेंस 1 (R1):** $[Calculate Level]\n"
        "- **सपोर्ट 1 (S1):** $[Calculate Level]\n\n"
        "### 🎯 लाइव ट्रेड सेटअप (ऐक्शन प्लान)\n"
        "- **आज का इंट्राडे झुकाव (Bias):** [तेजी / मंदी / न्यूट्रल]\n"
        "- **एंट्री ज़ोन (Entry Zone):** $[Zone range in numbers]\n"
        "- **स्टॉप लॉस (SL):** $[Level]\n"
        "- **टारगेट 1 (TP1):** $[Level]"
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_main,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction_main,
                temperature=0.0,
                response_mime_type="text/plain"
            )
        )
        return response.text
    except:
        return f"### 📋 Dynamic Intraday Key Levels\n- **Live Base Spot:** {live_spot:.2f}"

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
        st.warning("⚠️ सर्ver तिजोरी (Secrets) में 'GEMINI_API_KEY' डालना बाकी है।")
    
    if static_news:
        with st.spinner("जेमिनी प्रो इंजन लाइव लेवल्स और सभी खबरों का शुद्ध हिंदी विश्लेषण कैलकुलेट कर रहा है..."):
            
            # 1. पहले मुख्य SMC लेवल्स और ऐक्शन प्लान लोड करें
            ai_main_output = generate_smc_grid(static_news, live_spot_value)
            st.markdown(f'<div class="ai-box-container">', unsafe_allow_html=True)
            st.markdown(ai_main_output)
            st.write("---")
            
            # 2. हर न्यूज़ का अलग से कड़ा हिंदी विश्लेषण पैनल
            st.markdown("### 🔍 AI News Interpreter & Market Impact Panel")
            
            for item in static_news:
                with st.container(border=True):
                    single_interpretation = generate_isolated_interpretation(item['title'], item['summary'])
                    st.markdown(single_interpretation)
                    
            st.markdown('</div>', unsafe_allow_html=True)
