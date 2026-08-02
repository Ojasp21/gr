import streamlit as st


def load_css():

    st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Lexend:wght@600;700;800&display=swap');

:root{
    --bg:            #0b0d12;
    --bg-elevated:   #12151d;
    --bg-card:       #161a24;
    --bg-hover:      #1c212e;
    --border:        #262c3a;
    --border-soft:   #1e2330;
    --text:          #eef1f7;
    --text-muted:    #8891a5;
    --text-faint:    #5b6478;
    --accent:        #4f7cff;
    --accent-soft:   #4f7cff22;
    --accent-strong: #6f8fff;
    --saffron:       #ff9838;
    --success:       #22c55e;
    --success-soft:  #22c55e1f;
    --warning:       #f5a524;
    --warning-soft:  #f5a5241f;
    --danger:        #f2495c;
    --danger-soft:   #f2495c1f;
    --radius-lg:     18px;
    --radius-md:     12px;
    --radius-sm:     8px;
}

*{
    font-family:'Inter',sans-serif;
}

#MainMenu, footer, header{
    visibility:hidden;
}

.stApp{
    background:
        radial-gradient(1200px 500px at 15% -10%, #4f7cff14, transparent 60%),
        radial-gradient(900px 400px at 100% 0%, #ff983814, transparent 55%),
        var(--bg);
}

.block-container{
    max-width:1360px;
    padding-top:1.6rem;
    padding-bottom:3rem;
}

hr{
    border-color:var(--border);
    margin:1.1rem 0;
}

::-webkit-scrollbar{ width:9px; height:9px; }
::-webkit-scrollbar-thumb{ background:#333a4a; border-radius:10px; }
::-webkit-scrollbar-thumb:hover{ background:#454e63; }
::-webkit-scrollbar-track{ background:transparent; }

.app-header{
    display:flex;
    align-items:center;
    gap:16px;
    padding:22px 26px;
    background:linear-gradient(135deg, var(--bg-card) 0%, var(--bg-elevated) 100%);
    border:1px solid var(--border);
    border-radius:var(--radius-lg);
    margin-bottom:22px;
    position:relative;
    overflow:hidden;
}

.app-header::before{
    content:"";
    position:absolute;
    top:0; left:0; right:0;
    height:3px;
    background:linear-gradient(90deg, var(--accent), var(--saffron));
}

.app-header .icon-badge{
    width:52px; height:52px;
    min-width:52px;
    border-radius:14px;
    background:linear-gradient(135deg, var(--accent), #7c5cff);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:26px;
    box-shadow:0 6px 18px #4f7cff33;
}

.app-header h1{
    font-family:'Lexend',sans-serif;
    font-size:1.5rem;
    font-weight:800;
    margin:0;
    color:var(--text);
    letter-spacing:-0.02em;
}

.app-header p{
    margin:2px 0 0 0;
    color:var(--text-muted);
    font-size:0.88rem;
}

.stat-pill{
    background:var(--bg-card);
    border:1px solid var(--border);
    border-radius:var(--radius-md);
    padding:14px 18px;
    display:flex;
    flex-direction:column;
    gap:2px;
}

.stat-pill .stat-label{
    font-size:0.72rem;
    text-transform:uppercase;
    letter-spacing:0.06em;
    color:var(--text-faint);
    font-weight:600;
}

.stat-pill .stat-value{
    font-family:'Lexend',sans-serif;
    font-size:1.35rem;
    font-weight:700;
    color:var(--text);
}

section[data-testid="stSidebar"]{
    background:var(--bg-elevated);
    border-right:1px solid var(--border);
    width:352px !important;
}

section[data-testid="stSidebar"] .block-container{
    padding-top:1.4rem;
}

.sidebar-brand{
    display:flex;
    align-items:center;
    gap:10px;
    padding-bottom:14px;
}

.sidebar-brand .dot{
    width:10px; height:10px;
    border-radius:50%;
    background:var(--success);
    box-shadow:0 0 0 3px var(--success-soft);
}

.sidebar-brand span{
    font-family:'Lexend',sans-serif;
    font-weight:700;
    font-size:1.05rem;
    color:var(--text);
}

.sidebar-section-label{
    font-size:0.72rem;
    text-transform:uppercase;
    letter-spacing:0.08em;
    font-weight:700;
    color:var(--text-faint);
    margin:6px 0 8px 0;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"],
section[data-testid="stSidebar"] [data-testid="stRadio"],
section[data-testid="stSidebar"] [data-baseweb="select"] > div{
    background:var(--bg-card);
    border:1px solid var(--border);
}

.stButton>button{
    width:100%;
    border-radius:var(--radius-sm);
    height:42px;
    font-weight:600;
    font-size:0.88rem;
    border:1px solid var(--border);
    background:var(--bg-card);
    color:var(--text);
    transition:all 0.15s ease;
}

.stButton>button:hover{
    border-color:var(--accent);
    color:var(--accent-strong);
    transform:translateY(-1px);
    background:var(--bg-hover);
}

.stButton>button:active{
    transform:translateY(0px);
}

.stButton>button[kind="primary"]{
    background:linear-gradient(135deg, var(--accent), #6f5cff);
    border:none;
    color:white;
    box-shadow:0 4px 14px #4f7cff33;
}

.stButton>button[kind="primary"]:hover{
    color:white;
    filter:brightness(1.08);
}

.stLinkButton a{
    border-radius:var(--radius-sm) !important;
    font-weight:600 !important;
    font-size:0.85rem !important;
}

[data-testid="stFileUploader"]{
    border:1.5px dashed #37415a;
    border-radius:var(--radius-md);
    background:var(--bg-card);
    padding:16px;
    transition:border-color 0.15s ease;
}

[data-testid="stFileUploader"]:hover{
    border-color:var(--accent);
}

[data-testid="stFileUploaderDropzone"]{
    background:transparent;
}

div[role="radiogroup"]{
    background:var(--bg-card);
    border:1px solid var(--border);
    border-radius:var(--radius-md);
    padding:6px;
    gap:2px;
}

div[role="radiogroup"] label{
    padding:8px 10px;
    border-radius:var(--radius-sm);
    margin:0 !important;
    transition:background 0.15s ease;
}

div[role="radiogroup"] label:hover{
    background:var(--bg-hover);
}

[data-baseweb="select"] > div{
    border-radius:var(--radius-sm) !important;
    border-color:var(--border) !important;
}

[data-testid="stMetric"]{
    background:var(--bg-card);
    border-radius:var(--radius-md);
    padding:14px 18px;
    border:1px solid var(--border);
}

[data-testid="stMetricValue"]{
    font-family:'Lexend',sans-serif;
    color:var(--accent-strong);
}

.stTabs [data-baseweb="tab-list"]{
    gap:6px;
    background:var(--bg-card);
    padding:6px;
    border-radius:var(--radius-md);
    border:1px solid var(--border);
}

.stTabs [data-baseweb="tab"]{
    border-radius:var(--radius-sm);
    padding:8px 18px;
    font-weight:600;
    color:var(--text-muted);
}

.stTabs [aria-selected="true"]{
    background:var(--accent-soft);
    color:var(--accent-strong) !important;
}

.stTabs [data-baseweb="tab-highlight"]{
    display:none;
}

.stChatMessage{
    border-radius:var(--radius-md);
    padding:6px 4px;
    background:transparent;
    border:none;
}

[data-testid="stChatMessageContent"]{
    background:var(--bg-card);
    border:1px solid var(--border-soft);
    border-radius:var(--radius-md);
    padding:12px 16px;
}

[data-testid="stChatInput"]{
    border-radius:var(--radius-lg);
    border:1px solid var(--border);
    background:var(--bg-card);
}

[data-testid="stChatInput"] textarea{
    color:var(--text);
}

.empty-state{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding:56px 24px;
    background:var(--bg-card);
    border:1px dashed var(--border);
    border-radius:var(--radius-lg);
    color:var(--text-muted);
}

.empty-state .icon{
    font-size:2.2rem;
    margin-bottom:8px;
    opacity:0.85;
}

.empty-state .title{
    font-weight:700;
    color:var(--text);
    font-size:1.02rem;
    margin-bottom:4px;
}

.empty-state .subtitle{
    font-size:0.85rem;
    max-width:380px;
}

.streamlit-expanderHeader{
    font-weight:600;
    background:var(--bg-card) !important;
    border-radius:var(--radius-sm) !important;
    border:1px solid var(--border) !important;
}

.streamlit-expanderContent{
    background:var(--bg-elevated) !important;
    border:1px solid var(--border-soft) !important;
    border-top:none !important;
    border-radius:0 0 var(--radius-sm) var(--radius-sm) !important;
}

.badge{
    display:inline-flex;
    align-items:center;
    gap:5px;
    padding:3px 10px;
    border-radius:999px;
    font-size:0.72rem;
    font-weight:700;
    letter-spacing:0.02em;
    text-transform:uppercase;
    white-space:nowrap;
}

.badge-dot{
    width:6px; height:6px;
    border-radius:50%;
}

.badge-success{ background:var(--success-soft); color:var(--success); }
.badge-success .badge-dot{ background:var(--success); }

.badge-warning{ background:var(--warning-soft); color:var(--warning); }
.badge-warning .badge-dot{ background:var(--warning); }

.badge-danger{ background:var(--danger-soft); color:var(--danger); }
.badge-danger .badge-dot{ background:var(--danger); }

.badge-info{ background:var(--accent-soft); color:var(--accent-strong); }
.badge-info .badge-dot{ background:var(--accent-strong); }

.doc-card{
    background:var(--bg-card);
    border:1px solid var(--border);
    border-radius:var(--radius-md);
    padding:16px 18px;
    margin-bottom:0;
    transition:border-color 0.15s ease, transform 0.15s ease;
    height:100%;
}

.doc-card:hover{
    border-color:#3a4256;
}

.doc-card .doc-title{
    font-weight:700;
    font-size:0.95rem;
    color:var(--text);
    margin-bottom:8px;
    display:flex;
    align-items:flex-start;
    gap:8px;
    line-height:1.3;
}

.doc-meta-row{
    display:flex;
    flex-wrap:wrap;
    gap:6px 14px;
    margin:10px 0 4px 0;
    font-size:0.8rem;
    color:var(--text-muted);
}

.doc-meta-row b{
    color:var(--text);
    font-weight:600;
}

.source-card{
    background:var(--bg-elevated);
    border:1px solid var(--border-soft);
    border-left:3px solid var(--accent);
    border-radius:var(--radius-sm);
    padding:12px 14px;
    margin-bottom:10px;
}

.source-card .source-title{
    font-weight:700;
    font-size:0.88rem;
    color:var(--text);
    margin-bottom:4px;
}

.source-card .source-meta{
    font-size:0.78rem;
    color:var(--text-muted);
    display:flex;
    gap:14px;
}

.section-heading{
    font-family:'Lexend',sans-serif;
    font-weight:700;
    font-size:1.05rem;
    color:var(--text);
    display:flex;
    align-items:center;
    gap:8px;
    margin-bottom:2px;
}

.section-subtext{
    color:var(--text-muted);
    font-size:0.84rem;
    margin-bottom:14px;
}

</style>
""", unsafe_allow_html=True)