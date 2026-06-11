import streamlit as st
import json
import os
from datetime import datetime

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="90-Day Engineering Excellence Radar",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "team_progress.json"

# --- DATA PERSISTENCE LAYER ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_data()

# --- APP UI CUSTOMIZATION ---
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    .card { background-color: #F3F4F6; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #3B82F6; margin-bottom: 1rem; }
    .framework-box { background-color: #EFF6FF; padding: 1.2rem; border-radius: 0.5rem; border: 1px solid #BFDBFE; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">🚀 90-Day Engineering Excellence Radar</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A structured framework to scale communication, architecture patterns, and technical agility.</div>', unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.header("📋 Team Navigation")
    
    team_members = ["Select Member...", "Lead Architect", "Senior Engineer", "Cloud Security Engineer", "DevOps Specialist"]
    selected_user = st.selectbox("Team Member Profile", team_members)
    
    if selected_user == "Select Member...":
        st.warning("Please select a team member to view or track progress.")
        st.stop()
        
    # User data initialization
    if selected_user not in db:
        db[selected_user] = {
            "current_day": 1,
            "tasks": {}
        }
        
    user_data = db[selected_user]
    
    # Day Slider
    current_day = st.slider("Current Program Day", 1, 90, int(user_data.get("current_day", 1)))
    db[selected_user]["current_day"] = current_day
    save_data(db)

    # Dynamic Phase Calculation
    if current_day <= 30:
        phase_title = "Phase 1: Foundations & Habits"
        phase_desc = "Focusing on dependency mapping, daily recordings, and structural communication."
        progress_val = (current_day / 30) * 0.33
    elif current_day <= 60:
        phase_title = "Phase 2: Deep Architecture"
        phase_desc = "Writing explicit trade-off matrixes, ADRs, and abstracting business intent."
        progress_val = 0.33 + ((current_day - 30) / 30) * 0.33
    else:
        phase_title = "Phase 3: Organizational Agility"
        phase_desc = "Driving sandbox environments, evaluating tool deprecation, and peer mentorship."
        progress_val = 0.66 + ((current_day - 60) / 30) * 0.34

    st.markdown("---")
    st.metric(label="Program Velocity", value=f"Day {current_day}", delta=phase_title)
    st.progress(min(progress_val, 1.0))
    st.caption(f"*{phase_desc}*")

# --- GLOBAL UTILITY FUNCTION FOR CHECKBOXES ---
def persistent_checkbox(label, task_id):
    """Tracks checkbox state uniquely per user and saves automatically."""
    full_key = f"{selected_user}_{task_id}"
    default_val = db[selected_user]["tasks"].get(task_id, False)
    
    # Store state directly in user DB on change
    val = st.checkbox(label, value=default_val, key=full_key)
    if val != default_val:
        db[selected_user]["tasks"][task_id] = val
        save_data(db)
    return val

# --- MAIN WORKSPACE TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🗣️ 1. Communication Mastery", 
    "🏗️ 2. Architectural Thinking", 
    "🧠 3. Critical Analysis", 
    "⚡ 4. Technical Agility"
])

# --- TAB 1: ENGLISH & COMMUNICATION ---
with tab1:
    st.markdown("### Objective: Transition technical complexity into clear business value stories.")
    
    col1, col2 = st.columns([5, 4])
    with col1:
        st.markdown(f"#### 📅 Current Commitments (Day {current_day})")
        if current_day <= 30:
            persistent_checkbox("Daily: Record a 2-minute updates summary (Focus on eliminating filler text/words).", "c_d1")
            persistent_checkbox("Weekly: Strip out internal jargon from a client/stakeholder email update.", "c_w1")
        elif current_day <= 60:
            persistent_checkbox("Daily: Explain design decisions verbally without leaning on UI diagrams or slides.", "c_d2")
            persistent_checkbox("Weekly: Author a 1-page business abstract for a complex engineering sprint.", "c_w2")
        else:
            persistent_checkbox("Daily: Lead a live context-setting run for project delivery modules.", "c_d3")
            persistent_checkbox("Weekly: Host a 15-minute training deep-dive for technical junior peers.", "c_w3")

    with col2:
        st.markdown('<div class="framework-box">', unsafe_allow_html=True)
        st.markdown("#### 💡 Structural Framework: The PREP Model")
        st.markdown("""
        When communicating engineering bottlenecks to senior stakeholders, always structure responses using:
        * **P**oint: *State the clear, bottom-line upfront statement.*
        * **R**eason: *Provide the technical or operational why.*
        * **E**xample: *Back it up with concrete application performance metrics or data.*
        * **P**oint: *Reiterate the core takeaway or next decision node.*
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: ARCHITECTURAL THINKING ---
with tab2:
    st.markdown("### Objective: Move from 'how to code features' to 'system trade-off evaluation'.")
    
    col1, col2 = st.columns([5, 4])
    with col1:
        st.markdown("#### 🛠️ Core Phase Milestones")
        if current_day <= 30:
            st.info("**Milestone 1:** Trace and map out your system data pipelines. Identify every potential single point of failure (SPOF) and latency constraint.")
            persistent_checkbox("Component dependency map complete", "a_m1")
        elif current_day <= 60:
            st.info("**Milestone 2:** For every architectural pivot, outline three distinct paths: Cost-optimized, Scale-optimized, and Time-to-Market-optimized.")
            persistent_checkbox("Trade-off matrix submitted to repo", "a_m2")
        else:
            st.info("**Milestone 3:** Draft, finalize, and get team approval on a formal Architecture Decision Record (ADR).")
            persistent_checkbox("Formal ADR merged into main line", "a_m3")
            
    with col2:
        st.markdown("#### 📑 Standard ADR Framework")
        with st.expander("Show Lightweight ADR Blueprint"):
            st.code("""
# ADR-00X: [Descriptive Project Title]

## Context
What engineering problem are we trying to solve?
What are our technical/financial limitations?

## Decision
What path or tool are we selecting? 

## Consequences
What is the explicit trade-off? 
(What did we trade off in complexity, cost, or debt?)
            """, language="markdown")

# --- TAB 3: CRITICAL THINKING ---
with tab3:
    st.markdown("### Objective: Question foundational assertions to systematically clear root causes.")
    st.markdown("#### 🕵️‍♂️ The Five Whys Workbench")
    st.markdown("Use this workspace during engineering post-mortems or sprint retrospectives to uncover root causes:")
    
    w1 = st.text_input("1. Define the high-level operational failure:", placeholder="e.g., The pipeline broke during the Friday night deploy.")
    w2 = st.text_input("2. Why did that specific event occur?", placeholder="e.g., A configuration variable was missing in production environments.")
    w3 = st.text_input("3. Why was that variable or key missing?", placeholder="e.g., It was manually injected in staging but not added to the code repository.")
    w4 = st.text_input("4. Why was it manually injected instead of automated?", placeholder="e.g., The deployment pipeline framework lacks multi-environment parameter inheritance.")
    w5 = st.text_input("5. Why does it lack that baseline framework feature? (Root Cause)", placeholder="e.g., We prioritized pipeline speed over environment parity guardrails.")
    
    if w5:
        st.success("🎯 **Root Cause Isolated:** Focus your engineering remediation tickets around Step 5 rather than patching Step 1.")

# --- TAB 4: TECHNICAL AGILITY ---
with tab4:
    st.markdown("### Objective: Accelerate software adoption through time-boxed sandboxes.")
    
    st.markdown("#### ⏱️ The 3-Step Technology Evaluation Loop")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><b>1. Read & Scope (Day 1)</b><br>Determine exactly what architectural problem the library or service targets. Evaluate code health and ecosystem patterns.</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><b>2. Stress & Break (Day 2)</b><br>Build an isolated environment spike. Intentionally break error handling pipelines to see how the system logs exceptions.</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><b>3. Antipattern Matrix (Day 3)</b><br>Explicitly document situations where this tool should NOT be used before showing team members.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚡ Active Lab Verification")
    persistent_checkbox("The team dedicated at least 2 hours this week to structured sandbox exploration and prototyping.", "agility_weekly")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 0.85rem;'>Engineered for Team Growth Operations & Framework Tracking</p>", unsafe_allow_html=True)