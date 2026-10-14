"""Main Application Dashboard: Cyberpunk Data Science Portfolio Interface."""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

from src import wikipedia_api, wikidata_api
from src.graph_builder import build_graph, graph_statistics, make_graph_html

st.set_page_config(page_title="Knowledge Graph Explorer", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# ADVANCED CSS STYLING
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700;800&display=swap');

html { zoom: 0.95; font-size: 14px; }
:root {
    --bg-color: #05060A; 
    --sidebar-bg: #090C15;
    --panel-bg: rgba(12, 16, 26, 0.7);
    --neon-cyan: #00F3FF; 
    --neon-magenta: #FF00EA;
    --text-primary: #F8FAFC; 
    --text-muted: #94A3B8; 
    --border-color: rgba(0, 243, 255, 0.18);
}

body, .stApp { 
    font-family: 'Inter', sans-serif !important; 
    background-color: var(--bg-color); 
    color: var(--text-primary); 
}

/* =========================================================
   1. TOP SPACING & HERO TITLE STYLING
   ========================================================= */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 1.5rem !important;
    z-index: 1;
}

.block-container {
    padding-top: 1.0rem !important;
    padding-bottom: 3rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 98% !important;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 54px !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    text-shadow: 0 0 20px rgba(255, 0, 234, 0.7), 0 0 45px rgba(0, 243, 255, 0.4) !important;
    line-height: 1.15 !important;
    letter-spacing: -1px !important;
    margin: 0 !important;
    padding: 0 !important;
    display: block !important;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #00F3FF !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin-top: 8px !important;
    margin-bottom: 22px !important;
    display: block !important;
}

/* =========================================================
   2. SEARCH & EXPLORE BOX (STYLING THE ST.FORM)
   ========================================================= */
[data-testid="stForm"] {
    background: linear-gradient(90deg, rgba(12,16,26,0.95), rgba(12,16,26,0.6)) !important;
    border-left: 6px solid var(--neon-magenta) !important; 
    border-bottom: 1px solid var(--border-color) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 10px !important; 
    padding: 20px 26px !important; 
    margin-bottom: 20px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stForm"] div[data-testid="stTextInput"] input {
    font-size: 1.05rem !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid var(--border-color) !important;
    color: #FFF !important;
}

[data-testid="stForm"] div[data-testid="stTextInput"] input:focus {
    border-color: var(--neon-cyan) !important; 
    box-shadow: 0 0 15px rgba(0,243,255,0.2) !important;
}

div[data-testid="stFormSubmitButton"] button {
    font-size: 1.05rem !important;
    padding: 8px 18px !important;
    border-radius: 8px !important;
    background: transparent !important; 
    color: var(--neon-cyan) !important; 
    border: 1px solid rgba(0, 243, 255, 0.4) !important; 
    width: 100%;
    margin-top: 1px;
}
div[data-testid="stFormSubmitButton"] button:hover { 
    background: rgba(0, 243, 255, 0.15) !important; 
    border-color: var(--neon-cyan) !important; 
}

/* =========================================================
   3. LEFT PANEL (SIDEBAR) STYLING
   ========================================================= */
section[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border-color) !important;
    min-height: 100vh !important;
    height: 100vh !important;
}

section[data-testid="stSidebar"] > div {
    background-color: var(--sidebar-bg) !important;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}

.sidebar-title {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--neon-cyan) !important;
    margin-bottom: 10px !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    font-size: 1.5rem !important;
    color: #CBD5E1 !important;
    line-height: 1.4 !important;
}

[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label {
    background: transparent !important;
    border: none !important;
    padding: 4px 6px !important;
    margin: 2px 0 !important;
    font-size: 1.5rem !important;
    color: #E2E8F0 !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label:hover {
    color: var(--neon-cyan) !important;
}

[data-testid="stSidebar"] div[data-testid="stSlider"] label {
    font-size: 1.5rem !important;
    color: #E2E8F0 !important;
}

/* =========================================================
   4. METRICS & MAIN AREA FONT PROPORTIONS
   ========================================================= */
.main p, 
.main span:not(.metric-value), 
.main label {
    font-size: 1.05rem !important;
}

.main h3 {
    font-size: 1.45rem !important;
}

.main h4 {
    font-size: 1.25rem !important;
}

.metric-box {
    background: var(--panel-bg); 
    border: 1px solid var(--border-color); 
    border-radius: 10px; 
    padding: 12px 14px !important; 
    text-align: center; 
    transition: 0.2s;
}

.metric-box:hover { 
    border-color: var(--neon-cyan); 
    box-shadow: 0 4px 16px rgba(0, 243, 255, 0.18); 
    transform: translateY(-2px); 
}

.metric-label { 
    font-size: 0.82rem !important; 
    color: var(--text-muted); 
    text-transform: uppercase; 
    font-weight: 600; 
    letter-spacing: 0.9px;
}

.metric-value { 
    font-size: 1.95rem !important; 
    font-family: 'Space Grotesk', sans-serif; 
    color: var(--text-primary); 
    margin: 4px 0 !important; 
    font-weight: 700; 
}

div[data-testid="stButton"] button {
    background: transparent !important; 
    color: var(--neon-cyan) !important; 
    border: 1px solid rgba(0, 243, 255, 0.4) !important; 
    font-size: 0.95rem !important;
    padding: 7px 18px !important;
    border-radius: 18px !important;
}

div[data-testid="stButton"] button:hover { 
    background: rgba(0, 243, 255, 0.15) !important; 
    border-color: var(--neon-cyan) !important; 
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION & PIPELINE LOGIC
# ==========================================
if "active_query" not in st.session_state:
    st.session_state["active_query"] = ""

@st.cache_data(ttl=3600, show_spinner=False)
def execute_pipeline(topic: str, max_nodes: int, source: str):
    """Executes the Data Science extraction, cleaning, and structuring pipeline."""
    api = wikidata_api if source == "Wikidata" else wikipedia_api
    
    root_info = api.search_article(topic)
    root = root_info["title"]
    
    if source == "Wikidata":
        related_raw = api.get_article_links(root_info["id"], max_nodes * 2)
        details = api.get_article_details(related_raw)
    else:
        related_raw = api.get_article_links(root, max_nodes * 2)
        details = api.get_article_details(tuple([root] + related_raw))

    root_key = root.casefold()
    unique_related = []
    
    for canonical_title in details.keys():
        if canonical_title.casefold() != root_key:
            unique_related.append(canonical_title)
            
    related = unique_related[:max_nodes - 1]

    details[root] = {"summary": root_info["summary"], "url": root_info["url"]}
    graph = build_graph(root, related, details, source)

    return {
        "root": root, 
        "root_info": root_info, 
        "source": source, 
        "details": details, 
        "graph": graph
    }

# ==========================================
# SIDEBAR (VIEW SELECTOR & CONTROLS)
# ==========================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Control Panel</div>', unsafe_allow_html=True)
    
    api_source = st.radio("Data Engine", ["Wikipedia", "Wikidata"])
    max_concepts = st.slider("Nodes Limit", min_value=5, max_value=60, value=25)
    
    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 15px 0;'>", unsafe_allow_html=True)
    
    if st.session_state["active_query"]:
        st.markdown('<div class="sidebar-title" style="color: var(--neon-magenta) !important;">View Options</div>', unsafe_allow_html=True)
        view_mode = st.radio(
            "Select View", 
            ["🕸️ Knowledge Graph", "📝 Concepts & Relations", "📊 Data Analysis"],
            label_visibility="collapsed"
        )
    else:
        view_mode = None

# ==========================================
# PROMINENT LARGE HEADING BANNER
# ==========================================
st.markdown(
    '<div style="padding-top: 5px; padding-bottom: 15px;">'
    '<div class="hero-title" style="font-family: \'Space Grotesk\', sans-serif !important; font-size: 54px !important; font-weight: 800 !important; color: #FFFFFF !important; line-height: 1.15 !important; text-shadow: 0 0 20px rgba(255,0,234,0.7), 0 0 45px rgba(0,243,255,0.4) !important;">Knowledge Graph Explorer</div>'
    '<div class="hero-subtitle" style="font-family: \'Inter\', sans-serif !important; font-size: 18px !important; font-weight: 600 !important; color: #00F3FF !important; letter-spacing: 2px !important; text-transform: uppercase !important; margin-top: 6px !important;">Interactive Knowledge Topology</div>'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# SEARCH & ANALYZE BOX (GROUPED TOGETHER)
# ==========================================
with st.form(key="search_form", clear_on_submit=False):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        search_val = st.text_input("Search:", value="", placeholder="Enter any topic to explore...", label_visibility="collapsed")
    with col_btn:
        search_clicked = st.form_submit_button("Explore")

if search_clicked and search_val.strip():
    st.session_state["active_query"] = search_val.strip()

# Suggested Topics (Below the box)
st.markdown("<div style='font-size: 0.95rem; color: var(--text-muted); margin-top: 4px; margin-bottom: 6px;'>Suggested Topics:</div>", unsafe_allow_html=True)
sug_cols = st.columns(6)
suggestions = ["Machine Learning", "Quantum Computing", "Black Hole", "Data Science", "String Theory", "Neuroscience"]

for i, sug in enumerate(suggestions):
    with sug_cols[i]:
        if st.button(sug, use_container_width=True):
            st.session_state["active_query"] = sug
            st.rerun()

# ==========================================
# DYNAMIC EXECUTION & UI RENDERING
# ==========================================
if st.session_state["active_query"]:
    query = st.session_state["active_query"]
    
    try:
        with st.spinner(f"Compiling topology for '{query}' via {api_source}..."):
            result = execute_pipeline(query, max_concepts, api_source)
    except Exception as exc:
        st.error(f"⚠️ Error: {str(exc)}")
        result = None

    if result and view_mode:
        root = result["root"]
        graph = result["graph"]
        stats = graph_statistics(graph)
        
        # Sub-header
        colA, colB = st.columns([4, 1])
        with colA:
            st.markdown(f"<h3 style='color:var(--text-primary); margin: 16px 0 12px 0;'>Target Entity: <span style='color:var(--neon-cyan);'>{root}</span></h3>", unsafe_allow_html=True)
        with colB:
            st.link_button("📄 Open Main Article ↗", result["root_info"]["url"], use_container_width=True)

        # 4-Column Metrics Board
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-box"><div class="metric-label">Unique Nodes</div><div class="metric-value">{stats["nodes"]}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-box"><div class="metric-label">Observed Edges</div><div class="metric-value">{stats["edges"]}</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-box"><div class="metric-label">Components</div><div class="metric-value">{stats["components"]}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-box"><div class="metric-label">Source Engine</div><div class="metric-value" style="font-size:1.55rem; padding-top:4px;">{result["source"]}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 0; border-top: 1px solid rgba(0, 243, 255, 0.12); margin: 18px 0;'>", unsafe_allow_html=True)

        # ==========================================
        # VIEW ROUTING
        # ==========================================
        if view_mode == "🕸️ Knowledge Graph":
            components.html(make_graph_html(graph, root), height=640, scrolling=False)

        elif view_mode == "📝 Concepts & Relations":
            st.markdown("<h4 style='color:var(--neon-magenta);'>Extracted Knowledge Database & Relationships</h4>", unsafe_allow_html=True)
            
            # Consolidated Single Clean Table (No Duplicate Tables or Links)
            table_rows = []
            for n, a in graph.nodes(data=True):
                is_root = (n == root)
                if is_root:
                    rel_type = "🎯 Target Entity"
                else:
                    rel_type = graph.edges[root, n].get("relation", "Linked Entity") if graph.has_edge(root, n) else "Connected Entity"

                summary_text = a.get("summary", "")
                formatted_summary = (summary_text[:240] + "...") if summary_text else "No summary available."
                
                table_rows.append({
                    "Concept": n,
                    "Relationship": rel_type,
                    "Summary": formatted_summary,
                    "URL": a.get("url", "")
                })
            
            st.dataframe(
                pd.DataFrame(table_rows), 
                use_container_width=True, 
                hide_index=True, 
                column_config={"URL": st.column_config.LinkColumn("Document Link", display_text="Open Resource ↗")}
            )

        elif view_mode == "📊 Data Analysis":
            st.markdown("<h3 style='color:var(--text-primary); margin-bottom:18px;'>Core Topological Analysis (EDA)</h3>", unsafe_allow_html=True)
            
            # Focused 2-Graph Analytical View
            col1, col2 = st.columns(2)
            
            with col1:
                # 1. Top Central Concepts (Bar Chart)
                degree_df = pd.DataFrame([{"Concept": n, "Connections": d} for n, d in sorted(stats["degrees"].items(), key=lambda x: x[1], reverse=True)[:10]])
                fig_bar = px.bar(
                    degree_df, 
                    x="Connections", 
                    y="Concept", 
                    orientation='h', 
                    title="1. Top Central Concepts (Hubs)", 
                    color="Connections", 
                    color_continuous_scale=["#00F3FF", "#FF00EA"]
                )
                fig_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font=dict(color='#94A3B8', size=12), 
                    yaxis={'categoryorder': 'total ascending'},
                    coloraxis_showscale=False,
                    margin=dict(t=40, b=25)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with col2:
                # 2. Node Degree Distribution (Histogram)
                degree_values = list(stats["degrees"].values())
                fig_hist = px.histogram(
                    x=degree_values, 
                    nbins=12, 
                    title="2. Connection Distribution Across Network", 
                    color_discrete_sequence=['#FF00EA']
                )
                fig_hist.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font=dict(color='#94A3B8', size=12),
                    margin=dict(t=40, b=25),
                    xaxis_title="Number of Connections",
                    yaxis_title="Node Count"
                )
                st.plotly_chart(fig_hist, use_container_width=True)