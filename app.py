import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Personalized Project Recommender",
    layout="wide",
)

st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    text-align: center;
    margin-bottom: 2.5rem;
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.35);
}
.hero h1 {
    color: white;
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0 0 0.6rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: rgba(255,255,255,0.85);
    font-size: 1.1rem;
    margin: 0;
    font-weight: 400;
}

/* ── Input card ── */
.input-card {
    background: #1e1e2e;
    border: 1px solid #2d2d3f;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}

/* ── Streamlit input overrides ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #13131f !important;
    border: 1.5px solid #3d3d55 !important;
    border-radius: 10px !important;
    color: #e2e2f0 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
label { color: #a0a0b8 !important; font-weight: 500 !important; font-size: 0.9rem !important; }

/* ── Generate button ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    color: white !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.55) !important;
}

/* ── Summary banner ── */
.summary-banner {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-left: 4px solid #6366f1;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 2rem;
    color: #c8c8e0;
    font-size: 0.97rem;
    line-height: 1.6;
}

/* ── Section header ── */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e2e2f0;
    margin: 0 0 1.5rem 0;
    letter-spacing: -0.3px;
}

/* ── Project card ── */
.project-card {
    background: #1a1a2e;
    border: 1px solid #2d2d4a;
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.project-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 36px rgba(0,0,0,0.4);
}

/* ── Rank badge ── */
.rank-1 { background: linear-gradient(135deg, #f59e0b, #f97316); }
.rank-2 { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.rank-3 { background: linear-gradient(135deg, #10b981, #059669); }
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px; height: 36px;
    border-radius: 50%;
    color: white;
    font-weight: 800;
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
}

/* ── Project title ── */
.project-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e2e2f0;
    margin: 0.2rem 0 0.4rem 0;
}
.project-one-liner {
    color: #8888aa;
    font-size: 0.97rem;
    margin-bottom: 1.4rem;
    line-height: 1.5;
}

/* ── Sub-section labels ── */
.label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.5rem;
}

/* ── Body text ── */
.body-text {
    color: #b0b0cc;
    font-size: 0.95rem;
    line-height: 1.65;
    margin-bottom: 1.2rem;
}

/* ── Tech pill ── */
.pill-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1.2rem; }
.pill {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ── Build time chip ── */
.build-time {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #6ee7b7;
    border-radius: 999px;
    padding: 0.25rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 500;
}

/* ── Feature list ── */
.feature-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    color: #b0b0cc;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
    line-height: 1.5;
}
.feature-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #6366f1;
    margin-top: 0.5rem;
    flex-shrink: 0;
}

/* ── Interview angle box ── */
.interview-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #c4c4e0;
    font-size: 0.93rem;
    line-height: 1.6;
    margin-top: 0.4rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #13131f !important;
    border-right: 1px solid #2d2d3f !important;
}
.sidebar-step {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    margin-bottom: 1rem;
}
.step-num {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 50%;
    width: 26px; height: 26px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 1px;
}
.step-text { color: #9090b0; font-size: 0.9rem; line-height: 1.4; }
.sidebar-title { color: #e2e2f0; font-weight: 700; font-size: 1rem; margin-bottom: 1rem; }

/* ── Divider ── */
hr { border-color: #2d2d4a !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero">
    <h1> Personalized Project Recommender</h1>
    <p>Research any company and get 3 tailored project ideas that make you stand out in interviews.</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">How it works</div>', unsafe_allow_html=True)
    steps = [
        "Searches latest company news & announcements",
        "Reads their engineering blog",
        "Scans job postings for tech stack signals",
        "GPT-4o synthesizes 3 tailored projects",
    ]
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div class="sidebar-step">
            <div class="step-num">{i}</div>
            <div class="step-text">{step}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Inputs ──
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Stripe, Notion, Linear, Vercel",
    )
with col2:
    user_skills = st.text_area(
        "Your Background & Skills (optional)",
        placeholder="e.g. 3 years React, Python backend, built fintech side projects...",
        height=104,
    )

generate_btn = st.button(" Generate Project Ideas", type="primary", use_container_width=True)

# ── Run ──
if generate_btn:
    if not company_name.strip():
        st.error("Please enter a company name.")
    else:
        from agent import run_agent

        TOOL_LABELS = {
            "search_company_news": "Searching latest news and announcements...",
            "scrape_company_tech_blog": "Reading their engineering blog...",
            "search_job_postings": "Scanning job postings for tech stack signals...",
        }
        TOOL_PROGRESS = {
            "search_company_news": 30,
            "scrape_company_tech_blog": 60,
            "search_job_postings": 85,
        }

        status = st.empty()
        progress = st.progress(0)

        def on_tool_call(fn_name: str, fn_args: dict):
            status.info(f" {TOOL_LABELS.get(fn_name, 'Thinking...')}")
            progress.progress(TOOL_PROGRESS.get(fn_name, 90))

        status.info(f" Starting research on **{company_name}**...")

        try:
            result = run_agent(
                company_name=company_name.strip(),
                user_skills=user_skills.strip(),
                progress_callback=on_tool_call,
            )
        except Exception as exc:
            status.empty()
            progress.empty()
            st.error(f"Something went wrong: {exc}")
            st.stop()

        progress.progress(100)
        status.success("Research complete!")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Results ──
        if "raw" in result:
            st.markdown(result["raw"])
        else:
            if summary := result.get("company_summary"):
                st.markdown(f'<div class="summary-banner"> <strong>About {company_name}:</strong> {summary}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="section-header">Top 3 Project Ideas for {company_name}</div>', unsafe_allow_html=True)

            rank_classes = {1: "rank-1", 2: "rank-2", 3: "rank-3"}

            for project in result.get("projects", []):
                rank = project.get("rank", "")
                title = project.get("title", "Untitled")
                one_liner = project.get("one_liner", "")
                why_it_fits = project.get("why_it_fits", "")
                tech_stack = project.get("tech_stack", [])
                build_time = project.get("estimated_build_time", "")
                features = project.get("key_features", [])
                interview_angle = project.get("interview_angle", "")

                rank_cls = rank_classes.get(rank, "rank-2")

                pills_html = "".join(f'<span class="pill">{t}</span>' for t in tech_stack)
                features_html = "".join(
                    f'<div class="feature-item"><div class="feature-dot"></div><span>{f}</span></div>'
                    for f in features
                )

                st.markdown(f"""
                <div class="project-card">
                    <div class="rank-badge {rank_cls}">#{rank}</div>
                    <div class="project-title">{title}</div>
                    <div class="project-one-liner">{one_liner}</div>
                    <div style="display:flex; gap:3rem; flex-wrap:wrap;">
                        <div style="flex:1; min-width:240px;">
                            <div class="label">Why it fits</div>
                            <div class="body-text">{why_it_fits}</div>
                            <div class="label">Tech Stack</div>
                            <div class="pill-row">{pills_html}</div>
                            <div class="label">Build Time</div>
                            <span class="build-time">⏱ {build_time}</span>
                        </div>
                        <div style="flex:1; min-width:240px;">
                            <div class="label">Key Features</div>
                            {features_html}
                            <div class="label" style="margin-top:1rem;">Interview Angle</div>
                            <div class="interview-box"> {interview_angle}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
