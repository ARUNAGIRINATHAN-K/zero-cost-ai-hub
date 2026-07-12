import streamlit as st
import requests
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Parallel Multi-Agent News Analyst",
    page_icon="●",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap');

/* ── Reset & Base ───────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Geist', sans-serif !important;
    background-color: #F5F5F3 !important;
    color: #1A1A1A;
}

.stApp { background-color: #F5F5F3 !important; }

:root {
    --st-top-header-offset: 3.8rem;
}

/* Keep Streamlit chrome above app content and offset custom sticky nav below it */
[data-testid="stHeader"],
[data-testid="stAppToolbar"] {
    z-index: 1000 !important;
}

.block-container {
    padding: 0 24px 28px !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* ── Navbar ─────────────────────────────────────────── */
.mn-nav {
    background: #ffffff;
    border: 1px solid #E8E8E4;
    border-radius: 12px;
    padding: 0 40px;
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: calc(var(--st-top-header-offset) + 10px);
    z-index: 900;
    max-width: 1320px;
    margin: 14px auto 0;
}

.mn-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.mn-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #1A1A1A;
}

.mn-name {
    font-size: 14px;
    font-weight: 500;
    color: #1A1A1A;
    letter-spacing: -0.01em;
}

.mn-live {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #3B6D11;
    background: #EAF3DE;
    padding: 4px 12px;
    border-radius: 99px;
    font-family: 'Geist Mono', monospace;
}

.mn-live-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #639922;
    animation: livepulse 1.6s infinite;
}

@keyframes livepulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}

/* ── Page Content Wrapper ───────────────────────────── */
.mn-page {
    padding: 34px 0 60px;
    max-width: 1320px;
    margin: 0 auto;
}

@media (max-width: 1024px) {
    :root {
        --st-top-header-offset: 4.1rem;
    }

    .block-container {
        padding: 0 14px 20px !important;
    }

    .mn-nav {
        padding: 0 16px;
        margin-top: 10px;
    }

    .mn-page {
        padding: 24px 0 44px;
    }
}

/* ── Page Header ────────────────────────────────────── */
.mn-page-header {
    margin-bottom: 32px;
}

.mn-page-title {
    font-size: 26px;
    font-weight: 500;
    color: #1A1A1A;
    letter-spacing: -0.02em;
    margin: 0 0 6px 0;
}

.mn-page-sub {
    font-size: 13px;
    color: #767672;
    display: flex;
    align-items: center;
    gap: 16px;
}

.mn-page-sub span {
    display: flex;
    align-items: center;
    gap: 5px;
}

/* ── Section Label ──────────────────────────────────── */
.mn-section {
    font-family: 'Geist Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #AAAAA6;
    margin-bottom: 10px;
}

/* ── Query Card ─────────────────────────────────────── */
.mn-query-card {
    background: #ffffff;
    border: 1px solid #E8E8E4;
    border-radius: 12px;
    padding: 22px 24px;
    margin-bottom: 28px;
}

.stTextArea textarea {
    background: #F5F5F3 !important;
    border: 1px solid #E8E8E4 !important;
    border-radius: 8px !important;
    color: #1A1A1A !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 12px 14px !important;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: #AAAAAA !important;
    box-shadow: none !important;
}

.stTextArea textarea::placeholder {
    color: #BBBBB8 !important;
}

.stTextArea label {
    font-family: 'Geist Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #AAAAA6 !important;
}

/* ── Run Button ─────────────────────────────────────── */
.stButton > button {
    background: #1A1A1A !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 22px !important;
    letter-spacing: -0.01em !important;
    transition: background 0.15s !important;
    height: auto !important;
}

.stButton > button:hover {
    background: #333333 !important;
}

.stButton > button:active {
    background: #555555 !important;
    transform: scale(0.99) !important;
}

/* ── Report Card ────────────────────────────────────── */
.mn-report-card {
    background: #ffffff;
    border: 1px solid #E8E8E4;
    border-radius: 12px;
    padding: 22px 24px;
    margin-bottom: 28px;
}

.mn-report-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #F5F5F3;
    color: #767672;
    font-size: 11px;
    font-family: 'Geist Mono', monospace;
    padding: 3px 10px;
    border-radius: 4px;
    border: 1px solid #E8E8E4;
    margin-bottom: 14px;
}

.mn-report-body {
    font-size: 14px;
    line-height: 1.75;
    color: #3A3A3A;
}

/* ── Agent Cards ────────────────────────────────────── */
.mn-agent-card {
    background: #ffffff;
    border: 1px solid #E8E8E4;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 0;
}

.mn-agent-head {
    padding: 14px 18px;
    border-bottom: 1px solid #F0F0EC;
    display: flex;
    align-items: center;
    gap: 12px;
}

.mn-agent-icon {
    width: 30px;
    height: 30px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
}

.icon-finance  { background: #EAF3DE; color: #3B6D11; }
.icon-ai       { background: #EEEDFE; color: #534AB7; }
.icon-cyber    { background: #FCEBEB; color: #A32D2D; }
.icon-startup  { background: #E6F1FB; color: #185FA5; }

.mn-agent-title {
    font-size: 13px;
    font-weight: 500;
    color: #1A1A1A;
}

.mn-agent-count {
    font-size: 11px;
    color: #AAAAA6;
    font-family: 'Geist Mono', monospace;
    margin-top: 1px;
}

.mn-agent-body {
    padding: 14px 18px;
}

/* ── News Items ─────────────────────────────────────── */
.mn-item {
    padding-bottom: 12px;
    margin-bottom: 12px;
    border-bottom: 1px solid #F0F0EC;
}

.mn-item:last-child {
    padding-bottom: 0;
    margin-bottom: 0;
    border-bottom: none;
}

.mn-item-tag {
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-family: 'Geist Mono', monospace;
}

.tag-finance  { color: #3B6D11; }
.tag-ai       { color: #534AB7; }
.tag-cyber    { color: #A32D2D; }
.tag-startup  { color: #185FA5; }

.mn-item-text {
    font-size: 12.5px;
    font-weight: 500;
    color: #1A1A1A;
    line-height: 1.5;
    margin-bottom: 4px;
}

.mn-item-meta {
    font-size: 11px;
    color: #AAAAA6;
    font-family: 'Geist Mono', monospace;
}

.mn-sources {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #F0F0EC;
}

.mn-sources-label {
    font-size: 9px;
    font-family: 'Geist Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #CCCCCA;
    margin-bottom: 5px;
}

.mn-source-link {
    display: block;
    font-size: 11px;
    color: #767672;
    text-decoration: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 3px;
    font-family: 'Geist Mono', monospace;
}

.mn-source-link:hover { color: #1A1A1A; }

/* ── Stat Cards ─────────────────────────────────────── */
.mn-stat-card {
    background: #ffffff;
    border: 1px solid #E8E8E4;
    border-radius: 10px;
    padding: 16px 18px;
}

.mn-stat-n {
    font-size: 28px;
    font-weight: 500;
    color: #1A1A1A;
    letter-spacing: -0.03em;
    line-height: 1;
}

.mn-stat-l {
    font-size: 11px;
    color: #AAAAA6;
    margin-top: 5px;
    font-family: 'Geist Mono', monospace;
}

.mn-stat-bar {
    height: 2px;
    border-radius: 1px;
    margin-top: 14px;
}

.bar-finance  { background: #639922; }
.bar-ai       { background: #7F77DD; }
.bar-cyber    { background: #E24B4A; }
.bar-startup  { background: #378ADD; }

/* ── Misc Overrides ─────────────────────────────────── */
.stSpinner > div { border-top-color: #1A1A1A !important; }

.stAlert {
    border-radius: 8px !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 13px !important;
}

.streamlit-expanderHeader {
    background: #ffffff !important;
    border: 1px solid #E8E8E4 !important;
    border-radius: 8px !important;
    font-family: 'Geist Mono', monospace !important;
    font-size: 11px !important;
    color: #767672 !important;
    letter-spacing: 0.08em !important;
}

hr {
    border: none !important;
    border-top: 1px solid #E8E8E4 !important;
    margin: 28px 0 !important;
}

</style>
""", unsafe_allow_html=True)


# API endpoint (sidebar removed)
api_url = "http://localhost:8000/analyze"


# =========================================================
# NAVBAR
# =========================================================

st.markdown(f"""
<div class="mn-nav">
  <div class="mn-brand">
    <div class="mn-dot"></div>
    <span class="mn-name">News Analyst</span>
  </div>
  <div class="mn-live">
    <div class="mn-live-dot"></div>
    4 agents ready &nbsp;·&nbsp; {datetime.now().strftime('%H:%M')}
  </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# PAGE WRAPPER OPEN
# =========================================================

st.markdown('<div class="mn-page">', unsafe_allow_html=True)

# ── Page Header ──────────────────────────────────────────

st.markdown("""
<div class="mn-page-header">
  <div class="mn-page-title">Parallel Multi-Agent News Analyst</div>
  <div class="mn-page-sub">
    <span>4 domain agents running simultaneously</span>
    <span>Finance · AI · Cybersecurity · Startup</span>
  </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# QUERY INPUT
# =========================================================

query = st.text_area(
    label="Analysis query",
    placeholder="e.g. Latest AI and startup ecosystem news · Global cybersecurity threats this week · AI impact on financial markets",
    height=90,
    label_visibility="visible"
)

col_btn, col_hint = st.columns([1, 4])
with col_btn:
    analyze_button = st.button("→ Run parallel analysis", use_container_width=True)
with col_hint:
    st.markdown(
        '<p style="font-size:12px;color:#BBBBB8;padding-top:10px;font-family:\'Geist Mono\',monospace;">LangGraph Send API · Groq · Tavily Search</p>',
        unsafe_allow_html=True
    )


# =========================================================
# HELPERS
# =========================================================

AGENT_CONFIG = {
    "finance":  {"label": "Finance",       "icon": "📈", "cls": "finance",  "tag_cls": "tag-finance"},
    "ai":       {"label": "AI",            "icon": "◈",  "cls": "ai",       "tag_cls": "tag-ai"},
    "cyber":    {"label": "Cybersecurity", "icon": "🛡",  "cls": "cyber",    "tag_cls": "tag-cyber"},
    "startup":  {"label": "Startup",       "icon": "🚀", "cls": "startup",   "tag_cls": "tag-startup"},
}

STAT_BARS = {
    "finance": "bar-finance",
    "ai":      "bar-ai",
    "cyber":   "bar-cyber",
    "startup": "bar-startup",
}


def render_agent_card(key, items):
    cfg = AGENT_CONFIG[key]
    count = len(items)

    items_html = ""
    for item in items:
        summary = item.get("summary", "")
        sources = item.get("sources") or []
        sources_html = ""
        if sources:
            links = "".join(
                f'<a class="mn-source-link" href="{s}" target="_blank">{s}</a>'
                for s in sources[:3]
            )
            sources_html = f'<div class="mn-sources"><div class="mn-sources-label">Sources</div>{links}</div>'

        items_html += f"""
        <div class="mn-item">
          <div class="mn-item-text">{summary}</div>
          {sources_html}
        </div>
        """

    if not items_html:
        items_html = '<div class="mn-item"><div class="mn-item-meta">No results</div></div>'

    st.markdown(f"""
    <div class="mn-agent-card">
      <div class="mn-agent-head">
        <div class="mn-agent-icon icon-{cfg['cls']}">{cfg['icon']}</div>
        <div>
          <div class="mn-agent-title">{cfg['label']} Agent</div>
          <div class="mn-agent-count">{count} article{"s" if count != 1 else ""}</div>
        </div>
      </div>
      <div class="mn-agent-body">{items_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_stat_card(key, count, sublabel):
    bar_cls = STAT_BARS[key]
    st.markdown(f"""
    <div class="mn-stat-card">
      <div class="mn-stat-n">{count}</div>
      <div class="mn-stat-l">{sublabel}</div>
      <div class="mn-stat-bar {bar_cls}"></div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# RUN ANALYSIS
# =========================================================

if analyze_button:

    if not query.strip():
        st.warning("Please enter a query to begin.")

    else:

        with st.spinner("Running parallel analysis across all agents…"):

            try:

                response = requests.post(
                    api_url,
                    json={"query": query},
                    timeout=120
                )
                data = response.json()

                if data.get("success"):

                    st.success("Analysis complete — all agents finished.")

                    # ── Final Report ───────────────────────────

                    st.markdown('<div class="mn-section">Intelligence report</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="mn-report-card">
                      <div class="mn-report-chip">✦ Synthesised from 4 agents</div>
                      <div class="mn-report-body">{data.get("final_report", "")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Agent Outputs ──────────────────────────

                    st.markdown('<div class="mn-section">Agent outputs</div>', unsafe_allow_html=True)

                    col1, col2, col3, col4 = st.columns(4)

                    finance_items = data.get("finance_results", [])
                    ai_items      = data.get("ai_results", [])
                    cyber_items   = data.get("cyber_results", [])
                    startup_items = data.get("startup_results", [])

                    with col1:
                        render_agent_card("finance", finance_items)
                    with col2:
                        render_agent_card("ai", ai_items)
                    with col3:
                        render_agent_card("cyber", cyber_items)
                    with col4:
                        render_agent_card("startup", startup_items)

                    # ── Summary Stats ──────────────────────────

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<div class="mn-section">Summary</div>', unsafe_allow_html=True)

                    s1, s2, s3, s4 = st.columns(4)
                    with s1:
                        render_stat_card("finance", len(finance_items), "Finance articles")
                    with s2:
                        render_stat_card("ai", len(ai_items), "AI articles")
                    with s3:
                        render_stat_card("cyber", len(cyber_items), "Cybersecurity articles")
                    with s4:
                        render_stat_card("startup", len(startup_items), "Startup articles")

                    # ── Raw JSON ───────────────────────────────

                    with st.expander("View raw API response"):
                        st.json(data)

                else:
                    st.error(f"API error: {data.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"Connection error: {str(e)}")


# =========================================================
# PAGE WRAPPER CLOSE + FOOTER
# =========================================================

st.markdown("""
<hr>
<p style="font-family:'Geist Mono',monospace;font-size:11px;color:#CCCCCA;">
  LangGraph &nbsp;·&nbsp; Groq &nbsp;·&nbsp; Tavily &nbsp;·&nbsp; FastAPI &nbsp;·&nbsp; Streamlit
</p>
</div>
""", unsafe_allow_html=True)