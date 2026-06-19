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

# Initialize OpenAI client (Ensure OPENAI_API_KEY is set in your environment variables)
# If running locally, set it via: export OPENAI_API_KEY="your-key"
# If deploying to Streamlit Community Cloud, add it to "Secrets"
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key)
    return None

client = get_openai_client()

# Initialize Multi-step Wizard Session States
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "github" not in st.session_state:
    st.session_state.github = ""
if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "linkedin_post" not in st.session_state:
    st.session_state.linkedin_post = ""

# --- HELPER FUNCTIONS ---
def generate_mock_background():
    """Creates a default dark-mode template frame canvas layer."""
    img = Image.new('RGB', (800, 450), color='#0f172a')
    return img

def process_composite_graphic(captured_stream):
    """Layers the captured user picture cleanly over the template block."""
    user_img = Image.open(captured_stream)
    user_img = ImageOps.exif_transpose(user_img) # Handle mobile rotation tags
    user_img_resized = user_img.resize((360, 410))
    
    canvas = generate_mock_background()
    canvas.paste(user_img_resized, (20, 20))
    
    # Save composite asset out to byte streams buffer
    buffer = io.BytesIO()
    canvas.save(buffer, format='PNG')
    return buffer.getvalue()

# --- WIZARD HEADER & NAVIGATION ---
st.title("🪄 Build Localhost Content Wizard")
st.write("Convert your live hackathon breakthroughs into polished LinkedIn proof-of-work.")

# Visual step progress bar indicators
step_cols = st.columns(3)
with step_cols[0]:
    st.markdown(f"**Step 1: Identity & Capture** {'🟢' if st.session_state.step == 1 else '⚪'}")
with step_cols[1]:
    st.markdown(f"**Step 2: Voice Dictation** {'🟢' if st.session_state.step == 2 else '⚪'}")
with step_cols[2]:
    st.markdown(f"**Step 3: Preview & Publish** {'🟢' if st.session_state.step == 3 else '⚪'}")
st.markdown("---")

# ==========================================
# STEP 1: CAPTURE PHOTO & PERSONAL DETAILS
# ==========================================
if st.session_state.step == 1:
    st.subheader("Step 1: Your Profile & Perspective")
    
    name = st.text_input("Full Name", value=st.session_state.name)
    github = st.text_input("GitHub Username", value=st.session_state.github, placeholder="e.g., samik-roy")
    
    st.write("📸 Snap a picture of your local environment configuration workspace:")
    camera_file = st.camera_input("Capture Workspace")
    
    if camera_file and name and github:
        if st.button("Proceed to Voice Dictation ➡️"):
            st.session_state.name = name
            st.session_state.github = github
            st.session_state.photo_bytes = process_composite_graphic(camera_file)
            st.session_state.step = 2
            st.rerun()
    else:
        st.info("💡 Fill out your personal details and capture a live workspace photo to advance.")

# ==========================================
# STEP 2: AUDIO RECORDING & AI TRANSLATION
# ==========================================
elif st.session_state.step == 2:
    st.subheader("Step 2: Speak Your Breakthrough")
    st.write(f"Hey **{st.session_state.name}**, don't bother typing out a long post. Click below to record your voice detailing your technical milestones or any bugs you successfully solved.")
    
    # Native Streamlit audio input recorder component (Mobile browser friendly)
    audio_file = st.audio_input("Record your thoughts out loud")
    
    if audio_file:
        st.audio(audio_file)
        
        if not client:
            st.error("⚠️ OpenAI API Key missing from environment. Cannot run automated voice transcription workflows.")
        else:
            if st.button("✨ Transcribe & Craft My LinkedIn Post"):
                with st.spinner("Processing speech-to-text telemetry and engineering post layouts..."):
                    try:
                        # 1. Transcribe the audio stream using Whisper API
                        # Convert Streamlit UploadedFile object into a named byte stream file object Whisper accepts
                        audio_bytes = audio_file.read()
                        audio_io = io.BytesIO(audio_bytes)
                        audio_io.name = "audio.wav"
                        
                        transcript_obj = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_io
                        )
                        raw_text = transcript_obj.text
                        st.session_state.transcript = raw_text
                        
                        # 2. Reshape raw spoken transcript into a high-converting LinkedIn post via GPT
                        system_prompt = (
                            "You are an expert technical developer and executive ghostwriter. "
                            "Take the raw, conversational, spoken transcript provided and turn it into a crisp, "
                            "compelling LinkedIn post. Maintain a professional, developer-first tone. Use strategic line breaks "
                            "for high mobile readability, clear formatting, and include a few relevant hashtags like #BuildLocalhost."
                        )
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": f"Attendee Name: {st.session_state.name}\nGitHub: {st.session_state.github}\nRaw spoken thoughts: {raw_text}"}
                            ]
                        )
                        
                        st.session_state.linkedin_post = response.choices[0].message.content
                        st.session_state.step = 3
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error during AI pipeline loop: {str(e)}")
                        
    if st.button("⬅️ Back to Step 1"):
        st.session_state.step = 1
        st.rerun()

# ==========================================
# STEP 3: PREVIEW LINKEDIN POST & PUBLISH
# ==========================================
elif st.session_state.step == 3:
    st.subheader("Step 3: Final Verification & Share Interface")
    
    # Display the composite photo created in Step 1
    if st.session_state.photo_bytes:
        st.image(st.session_state.photo_bytes, caption="Generated Event Graphic Banner", use_container_width=True)
    
    # Text area allowing the builder to do a final text polish before posting
    edited_post = st.text_area("Refine your finalized copy text:", value=st.session_state.linkedin_post, height=220)
    
    st.markdown("---")
    
    # Build URL intent string link vector to open up LinkedIn composing fields natively
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
        
    st.info("💡 **Next Step Instructions:** Click the Download button to save your event graphic, then hit the LinkedIn link button. Your custom post text will carry forward automatically into the text container field, where you can attach your image asset.")
    
    if st.button("🔄 Start A New Entry Wizard"):
        # Reset wizard configurations state parameters
        st.session_state.step = 1
        st.session_state.photo_bytes = None
        st.session_state.linkedin_post = ""
        st.session_state.transcript = ""
        st.rerun()