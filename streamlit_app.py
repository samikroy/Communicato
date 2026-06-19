import streamlit as st
from PIL import Image, ImageOps
import io
import os
import urllib.parse
from openai import OpenAI

# --- INITIALIZATION & CONFIG ---
st.set_page_config(
    page_title="Build Localhost - Content Wizard",
    page_icon="🪄",
    layout="centered"
)

# --- SIDEBAR CONFIGURATION & API ENGINE ---
with st.sidebar:
    st.title("⚙️ Engine Settings")
    
    # Allow switching to a keyless fallback mode directly from the UI
    ai_mode = st.radio(
        "AI Transcription Mode",
        ["Off (Use Local Text/Keyboard Dictation)", "On (Use OpenAI Whisper & GPT)"],
        index=0,
        help="Switch to 'Off' if you do not have an OpenAI API key. Attendees can use their mobile keyboard's native voice button instead."
    )
    
    openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-proj-...", value=os.getenv("OPENAI_API_KEY", ""))

# Initialize OpenAI client if enabled and key is present
def get_openai_client(key):
    if ai_mode.startswith("On") and key:
        return OpenAI(api_key=key)
    return None

client = get_openai_client(openai_key)

# Initialize Multi-step Wizard Session States
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "github" not in st.session_state:
    st.session_state.github = ""
if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None
if "linkedin_post" not in st.session_state:
    st.session_state.linkedin_post = ""

# --- IMAGE PROCESSING HELPERS ---
def generate_mock_background():
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

# Visual progress tracking indicator
step_cols = st.columns(3)
with step_cols[0]:
    st.markdown(f"**Step 1: Identity & Capture** {'🟢' if st.session_state.step == 1 else '⚪'}")
with step_cols[1]:
    st.markdown(f"**Step 2: Core Insights** {'🟢' if st.session_state.step == 2 else '⚪'}")
with step_cols[2]:
    st.markdown(f"**Step 3: Preview & Publish** {'🟢' if st.session_state.step == 3 else '⚪'}")
st.markdown("---")

# ==========================================
# STEP 1: CAPTURE PHOTO & DETAILS
# ==========================================
if st.session_state.step == 1:
    st.subheader("Step 1: Your Profile & Perspective")
    
    name = st.text_input("Full Name", value=st.session_state.name)
    github = st.text_input("GitHub Username", value=st.session_state.github, placeholder="e.g., samik-roy")
    
    st.write("📸 Snap a picture of your local environment setup:")
    camera_file = st.camera_input("Capture Workspace")
    
    if camera_file and name and github:
        if st.button("Proceed to Next Step ➡️"):
            st.session_state.name = name
            st.session_state.github = github
            st.session_state.photo_bytes = process_composite_graphic(camera_file)
            st.session_state.step = 2
            st.rerun()
    else:
        st.info("💡 Complete your personal details and capture a live workspace photo to advance the wizard.")

# ==========================================
# STEP 2: INSIGHT CAPTURE (DYNAMIC MODE)
# ==========================================
elif st.session_state.step == 2:
    st.subheader("Step 2: Document Your Breakthrough")
    
    # MODE A: NO OPENAI KEY (KEYBOARD VOICE FALLBACK)
    if ai_mode.startswith("Off"):
        st.info("🎤 **Mobile Tip:** Tap the text block below and press the **Microphone icon** on your phone's digital keyboard to dictate your thoughts seamlessly without an API key!")
        
        user_text = st.text_area(
            "What was your primary technical milestone breakthrough today?", 
            placeholder="Type or dictate your core technical accomplishments here...",
            height=150
        )
        
        if st.button("✨ Structure into Post ➡️"):
            if user_text.strip() == "":
                st.error("Please add some insights or notes before advancing.")
            else:
                # Local baseline formatting without calling cloud models
                st.session_state.linkedin_post = (
                    f"🚀 Just wrapped up a hands-on lab pipeline at #BuildLocalhost!\n\n"
                    f"🛠️ **Milestone Breakthrough:**\n{user_text}\n\n"
                    f"👨‍💻 Connected on GitHub: github.com/{st.session_state.github}\n\n"
                    f"#BuildLocalhost #CloudSecurity #DevSecOps #ProofOfWork"
                )
                st.session_state.step = 3
                st.rerun()

    # MODE B: AUTOMATED OPENAI PIPELINE
    else:
        st.write("🎙️ Record your voice detailing your configurations out loud:")
        audio_file = st.audio_input("Record Voice Segment")
        
        if audio_file:
            st.audio(audio_file)
            
            if not client:
                st.error("⚠️ OpenAI Engine active but API Key is missing. Please provide a valid key in the sidebar configuration drawer or switch to Local Text mode.")
            else:
                if st.button("✨ Transcribe & Craft My LinkedIn Post via AI"):
                    with st.spinner("Processing speech-to-text transcription algorithms..."):
                        try:
                            audio_bytes = audio_file.read()
                            audio_io = io.BytesIO(audio_bytes)
                            audio_io.name = "audio.wav"
                            
                            transcript_obj = client.audio.transcriptions.create(
                                model="whisper-1", file=audio_io
                            )
                            raw_text = transcript_obj.text
                            
                            system_prompt = (
                                "You are an expert technical developer and ghostwriter. Turn the conversational spoken transcript "
                                "into a crisp, high-impact LinkedIn post. Maintain a professional tone, use clean line breaks for mobile formatting, "
                                "and include structural hashtags."
                            )
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": f"Name: {st.session_state.name}\nGitHub: {st.session_state.github}\nTranscript: {raw_text}"}
                                ]
                            )
                            st.session_state.linkedin_post = response.choices[0].message.content
                            st.session_state.step = 3
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error executing AI generation loop: {str(e)}")
                            
    if st.button("⬅️ Back to Step 1"):
        st.session_state.step = 1
        st.rerun()

# ==========================================
# STEP 3: PREVIEW LINKEDIN POST & PUBLISH
# ==========================================
elif st.session_state.step == 3:
    st.subheader("Step 3: Final Verification & Share Interface")
    
    if st.session_state.photo_bytes:
        st.image(st.session_state.photo_bytes, caption="Generated Event Graphic Banner", use_container_width=True)
    
    edited_post = st.text_area("Refine your finalized copy text layout:", value=st.session_state.linkedin_post, height=220)
    
    st.markdown("---")
    
    encoded_post_text = urllib.parse.quote(edited_post)
    linkedin_share_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_post_text}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="💾 Download Event Image Asset",
            data=st.session_state.photo_bytes,
            file_name=f"build_localhost_{st.session_state.github}.png",
            mime="image/png",
            use_container_width=True
        )
    with col2:
        st.link_button("🚀 Open & Paste onto LinkedIn Feed", linkedin_share_url, use_container_width=True)
        
    if st.button("🔄 Start A New Entry Wizard"):
        st.session_state.step = 1
        st.session_state.photo_bytes = None
        st.session_state.linkedin_post = ""
        st.rerun()