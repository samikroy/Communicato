import streamlit as str
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
str.set_page_config(
    page_title="Build Localhost - Hub",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE ---
# Track user onboarding, milestones, and feedback local state
if "attendee_name" not in str.session_state:
    str.session_state.attendee_name = ""
if "github_handle" not in str.session_state:
    str.session_state.github_handle = ""
if "milestones" not in str.session_state:
    str.session_state.milestones = {
        "1. Environment Provisioned": False,
        "2. Core Lab Completed": False,
        "3. Localhost Live Demo": False
    }
if "feedback_submitted" not in str.session_state:
    str.session_state.feedback_submitted = False

# --- FILE PATH FOR DATA COLLECTION ---
FEEDBACK_FILE = "event_feedback.csv"

def save_feedback(name, github, rating, comment):
    """Appends feedback metrics to a local CSV file dataset."""
    new_data = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "GitHub": github,
        "Rating": rating,
        "Comment": comment
    }])
    if not os.path.isfile(FEEDBACK_FILE):
        new_data.to_csv(FEEDBACK_FILE, index=False)
    else:
        new_data.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)

# --- SIDEBAR: ATTENDEE AUTHENTICATION & PROGRESS ---
with str.sidebar:
    str.title("🛠️ Event Identity")
    str.write("Register your developer handle to track your event milestone achievements.")
    
    # Capture Attendee Identity
    name_input = str.text_input("Full Name", value=str.session_state.attendee_name)
    github_input = str.text_input("GitHub Username", value=str.session_state.github_handle, placeholder="e.g., samik-roy")
    
    if name_input and github_input:
        str.session_state.attendee_name = name_input
        str.session_state.github_handle = github_input
        str.success(f"Linked: `{str.session_state.github_handle}`")
    else:
        str.warning("Please fill profile info to activate portfolio tracking.")

    str.markdown("---")
    str.subheader("🏆 Your Unlocked Badges")
    
    # Display dynamic visual gamification metrics based on milestones completed
    completed_count = sum(str.session_state.milestones.values())
    total_milestones = len(str.session_state.milestones)
    
    str.metric(label="Milestones Cleared", value=f"{completed_count} / {total_milestones}")
    str.progress(completed_count / total_milestones)
    
    if completed_count == total_milestones:
        str.balloons()
        str.success("🏅 Elite Localhost Builder Unlocked!")

# --- MAIN DASHBOARD INTERFACE ---
str.title("Build Localhost: Event Hub & Feedback Portal")
str.markdown(
    "Welcome to the interactive sandbox workstation. Track your lab deployments, "
    "view event metrics, and cast your performance feedback directly below."
)

if not str.session_state.attendee_name:
    str.info("👉 Enter your profile details in the left sidebar configuration panel to unlock the full workbench features.")
else:
    # Setup interactive responsive workspace tabs
    tab_journey, tab_feedback, tab_metrics = str.tabs([
        "🚀 My Learning Journey Checklist", 
        "📝 Submit Event Feedback", 
        "📊 Admin Analytics View"
    ])

    # --- TAB 1: GAMIFIED EVENT CHECKLIST ---
    with tab_journey:
        str.subheader("Complete Lab Objectives & Earn Contributions")
        str.write("Check off objectives as you complete them during the live hackathon session:")
        
        # Iteratively render dynamic interactive check-boxes bound to session state memory
        for milestone in str.session_state.milestones.keys():
            is_checked = str.checkbox(milestone, value=str.session_state.milestones[milestone])
            str.session_state.milestones[milestone] = is_checked
            
        str.markdown("---")
        str.markdown("### 🎁 Your Takeaway Package status")
        if completed_count > 0:
            str.info(f"Hey **{str.session_state.attendee_name}**, your checkpoint data is being staged. At the conclusion of Build Localhost, your verified markdown roadmap can be exported directly to your account profile repository.")
        else:
            str.write("Begin ticking off milestones above to populate your custom developer profile portfolio logs.")

    # --- TAB 2: DETAILED FEEDBACK CAPTURE ---
    with tab_feedback:
        str.subheader("Rate Your Build Localhost Experience")
        
        if str.session_state.feedback_submitted:
            str.success("🎉 Thank you! Your architectural experience feedback metrics have been captured successfully.")
        else:
            with str.form("feedback_form"):
                event_rating = str.slider("Rate the overall session utility (1 = Basic, 5 = Elite Architect)", 1, 5, 4)
                feedback_comments = str.text_area("What was your primary takeaway or configuration breakthrough today?")
                
                submit_button = str.form_submit_button("Submit Final Log Verification")
                
                if submit_button:
                    if feedback_comments.strip() == "":
                        str.error("Please add a short comment about your experience before submitting.")
                    else:
                        save_feedback(
                            str.session_state.attendee_name,
                            str.session_state.github_handle,
                            event_rating,
                            feedback_comments
                        )
                        str.session_state.feedback_submitted = True
                        str.experimental_rerun()

    # --- TAB 3: ADMIN METRICS / ANALYTICS ---
    with tab_metrics:
        str.subheader("Real-Time Event Data Stream")
        str.write("This metrics cluster displays live feedback responses received during the event execution loops.")
        
        if os.path.exists(FEEDBACK_FILE):
            df = pd.read_csv(FEEDBACK_FILE)
            
            # Show summarized KPIs
            col1, col2 = str.columns(2)
            with col1:
                str.metric("Total Logs Captured", len(df))
            with col2:
                str.metric("Average Experience Rating", f"{df['Rating'].mean():.2f} / 5")
            
            str.markdown("### Raw Submission Datatable View")
            str.dataframe(df, use_container_width=True)
        else:
            str.info("Waiting for first attendee log entry stream to populate telemetry databases.")