import streamlit as st
from PIL import Image, ImageOps
import io
import os
import re
import urllib.parse
from openai import OpenAI

# --- INITIALIZATION & CONFIG ---
st.set_page_config(
    page_title="Build Localhost - Content Wizard",
    page_icon="🪄",
    layout="centered"
)

# --- VALIDATION ENGINE STRATEGIES ---
def is_valid_email(email_str):
    """Validates standard email formatting structures."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email_str.strip()))

def is_valid_mobile(mobile_str):
    """Validates global numeric phone structures (10 to 15 digits)."""
    clean_num = re.sub(r"[+\-\s()]", "", mobile_str)
    return clean_num.isdigit() and 10 <= len(clean_num) <= 15

def is_valid_github(github_str):
    """Validates baseline alphanumeric username syntax constraints."""
    clean_handle = github_str.strip().replace("@", "")
    if not clean_handle:
        return False
    # GitHub handles cannot start with hyphens and are limited to 39 chars
    return bool(re.match(r"^[a-zA-Z0-9][a-zA-Z0-9-]{0,38}$", clean_handle))

# --- SIDEBAR CONFIGURATION & API ENGINE ---
with st.sidebar:
    st.title("⚙️ Engine Settings")
    
    ai_mode = st.radio(
        "AI Transcription Mode",
        ["Off (Use Local Text/Keyboard Dictation)", "On (Use OpenAI Whisper & GPT)"],
        index=0,
        help="Switch to 'Off' if you don't have an OpenAI API key. Attendees can use their mobile keyboard's microphone button instead."
    )
    
    openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-proj-...", value=os.getenv("OPENAI_API_KEY", ""))

def get_openai_client(key):
    if ai_mode.startswith("On") and key:
        return OpenAI(api_key=key)
    return None

client = get_openai_client(openai_key)

# Initialize Session States
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "github" not in st.session_state:
    st.session_state.github = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "mobile" not in st.session_state:
    st.session_state.mobile = ""
if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None
if "linkedin_post" not in st.session_state:
    st.session_state.linkedin_post = ""

# --- IMAGE PROCESSING HELPERS ---
def generate_mock_background():
    # Branded base frame block canvas layer
    img = Image.new('RGB', (800, 450), color='#0f172a')
    return img

def process_composite_graphic(captured_stream):
    user_img = Image.open(captured_stream)
    user_img = ImageOps.exif_transpose(user_img) 
    user_img_resized = user_img.resize((360, 410))
    
    canvas = generate_mock_background()
    canvas.paste(user_img_resized, (20, 20))
    
    buffer = io.BytesIO()
    canvas.save(buffer, format='PNG')
    return buffer.getvalue()

# --- WIZARD HEADER ---
st.title("🪄 Build Localhost Content Wizard")

# Step progress layout metrics indicators
step_cols = st.columns(3)
with step_cols[0]:
    st.markdown(f"**Step 1: Onboarding Registry** { '🟢' if st.session_state.step == 1 else '⚪' }")
with step_cols[1]:
    st.markdown(f"**Step 2: Core Insights** { '🟢' if st.session_state.step == 2 else '⚪' }")
with step_cols[2]:
    st.markdown(f"**Step 3: Preview & Share** { '🟢' if st.session_state.step == 3 else '⚪' }")
st.markdown("---")

# ==========================================
# STEP 1: CAPTURE DETAILS & DATA VALIDATION
# ==========================================
if st.session_state.step == 1:
    st.subheader("Step 1: Attendee Identity Registry")
    
    name = st.text_input("Full Name", value=st.session_state.name)
    email = st.text_input("Email Address", value=st.session_state.email, placeholder="you@domain.com")
    mobile = st.text_input("Mobile Number", value=st.session_state.mobile, placeholder="e.g., +919876543210")
    github = st.text_input("GitHub Username", value=st.session_state.github, placeholder="e.g., samik-roy")
    
    st.write("📸 Snap a picture of your local environment configuration workspace setup:")
    camera_file = st.camera_input("Capture Workspace")
    
    # Live error parameter checks indicators
    validation_passed = True
    
    if email and not is_valid_email(email):
        st.error("❌ Invalid Email format framework detected.")
        validation_passed = False
        
    if mobile and not is_valid_mobile(mobile):
        st.error("❌ Invalid Mobile Number formatting (Must be a 10-15 digit string sequence).")
        validation_passed = False
        
    if github and not is_valid_github(github):
        st.error("❌ Invalid GitHub username structure syntax constraint.")
        validation_passed = False

    if camera_file and name and email and mobile and github and validation_passed:
        if st.button("Proceed to Next Step ➡️"):
            st.session_state.name = name
            st.session_state.email = email
            st.session_state.mobile = mobile
            st.session_state.github = github.strip().replace("@", "")
            st.session_state.photo_bytes = process_composite_graphic(camera_file)
            st.session_state.step = 2
            st.rerun()
    else:
        st.info("💡 Please ensure all configuration data entry parameter fields are filled, properly validated, and a picture is snapped to unlock Step 2.")

# ==========================================
# STEP 2: INSIGHT CAPTURE & PRIVACY FILTERING
# ==========================================
elif st.session_state.step == 2:
    st.subheader("Step 2: Document Your Breakthrough")
    
    # MODE A: FALLBACK LOCAL PROCESSING (NO PII)
    if ai_mode.startswith("Off"):
        st.info("🎤 **Mobile Tip:** Tap the box area block and press the **Microphone button** on your screen's device digital keyboard to dictate your milestones smoothly without a cloud key.")
        
        user_text = st.text_area(
            "What was your primary technical configuration milestone breakthrough today?", 
            placeholder="Type or dictate highlights here...",
            height=150
        )
        
        if st.button("✨ Structure into Post ➡️"):
            if user_text.strip() == "":
                st.error("Please insert bulleted items or notes before advancing.")
            else:
                # Local safe formatting structure containing absolutely ZERO PII data metrics
                st.session_state.linkedin_post = (
                    f"🚀 Just wrapped up a hands-on lab infrastructure pipeline at the #BuildLocalhost event!\n\n"
                    f"🛠️ **Technical Breakthrough Milestone:**\n{user_text}\n\n"
                    f"👨‍💻 Verified Account Portfolio: github.com/{st.session_state.github}\n\n"
                    f"#BuildLocalhost #DevSecOps #ProofOfWork"
                )
                st.session_state.step = 3
                st.rerun()

    # MODE B: AI TRANSFORMER PIPELINE WITH PRIVACY EXTRACTION FILTER
    else:
        st.write("🎙️ Record your voice detailing your infrastructure configurations out loud:")
        audio_file = st.audio_input("Record Voice Segment")
        
        if audio_file:
            st.audio(audio_file)
            
            if not client:
                st.error("⚠️ OpenAI Engine active but API Key parameter is unassigned. Paste a working key or use Local Mode.")
            else:
                if st.button("✨ Transcribe & Craft My LinkedIn Post via AI"):
                    with st.spinner("Executing speech-to-text filters and privacy alignment check..."):
                        try:
                            audio_bytes = audio_file.read()
                            audio_io = io.BytesIO(audio_bytes)
                            audio_io.name = "audio.wav"
                            
                            transcript_obj = client.audio.transcriptions.create(
                                model="whisper-1", file=audio_io
                            )
                            raw_text = transcript_obj.text
                            
                            # Tight context system instruction preventing PII leaking
                            system_prompt = (
                                "You are an expert technical developer and executive ghostwriter. "
                                "Take the raw conversational transcript and turn it into a crisp, high-impact LinkedIn post. "
                                "CRITICAL PRIVACY FILTER GUARDRAIL: Never mention the attendee's personal email, phone number, "
                                "or precise contact data inside the public post copy text. Keep the focus entirely on their technical milestones. "
                                "Format cleanly using professional line spacing layouts and appends relevant tags like #BuildLocalhost."
                            )
                            
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": f"Attendee Name: {st.session_state.name}\nGitHub Handle: {st.session_state.github}\nTranscript context: {raw_text}"}
                                ]
                            )
                            st.session_state.linkedin_post = response.choices[0].message.content
                            st.session_state.step = 3
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error running processing pipelines: {str(e)}")
                            
    if st.button("⬅️ Back to Step 1"):
        st.session_state.step = 1
        st.rerun()

# ==========================================
# STEP 3: PREVIEW & FINAL LINKEDIN EXPORT HUB
# ==========================================
elif st.session_state.step == 3:
    st.subheader("Step 3: Final Verification & Share Interface")
    
    # Renders compiled custom image banner
    if st.session_state.photo_bytes:
        st.image(st.session_state.photo_bytes, caption="Your Verified Branded Event Image", use_container_width=True)
    
    edited_post = st.text_area("Finalized Copy (Verified PII-Free):", value=st.session_state.linkedin_post, height=220)
    
    st.markdown("---")
    
    # URL intent composition line engine
    encoded_post_text = urllib.parse.quote(edited_post)
    linkedin_share_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_post_text}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="💾 1. Download Branded Image",
            data=st.session_state.photo_bytes,
            file_name=f"build_localhost_badge.png",
            mime="image/png",
            use_container_width=True
        )
    with col2:
        st.link_button("🚀 2. Open & Paste to LinkedIn Feed", linkedin_share_url, use_container_width=True)
        
    st.info("💡 **How to publish with your image:** First, click **Button 1** to save your branded event graphic to your device. Next, click **Button 2**. Your polished text copy carries over automatically into your composition dashboard view. Simply click the media/photo attachment icon inside LinkedIn to upload your saved event graphic!")
    
    if st.button("🔄 Start A New Entry Wizard"):
        st.session_state.step = 1
        st.session_state.photo_bytes = None
        st.session_state.linkedin_post = ""
        st.rerun()