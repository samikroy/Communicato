import streamlit as st
from streamlit_oauth import OAuth2Component
from PIL import Image, ImageOps
import io
import os
import re
import urllib.parse
from openai import OpenAI

# --- INITIALIZATION & PAGE CONFIG ---
st.set_page_config(
    page_title="Build Localhost - Auth Wizard",
    page_icon="🪄",
    layout="centered"
)

# Fetch secure environment keys from Streamlit Secrets Management
CLIENT_ID = st.secrets.get("GITHUB_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("GITHUB_CLIENT_SECRET")

AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
REFRESH_TOKEN_URL = "https://github.com/login/oauth/access_token"
REVOKE_TOKEN_URL = "https://api.github.com/applications/grant"

# Initialize OAuth Component Interface
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint=AUTHORIZE_URL,       # Changed from authorize_url
    token_endpoint=TOKEN_URL,               # Changed from token_url
    refresh_token_endpoint=REFRESH_TOKEN_URL, # Changed from refresh_token_url
    revoke_token_endpoint=REVOKE_TOKEN_URL   # Changed from revoke_token_url
)

# Initialize Wizard State Parameters Memory
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "mobile" not in st.session_state:
    st.session_state.mobile = ""
if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None
if "linkedin_post" not in st.session_state:
    st.session_state.linkedin_post = ""

# --- DATA FORMAT INTERACTION VALIDATORS ---
def is_valid_email(email_str):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_str.strip()))

def is_valid_mobile(mobile_str):
    clean_num = re.sub(r"[+\-\s()]", "", mobile_str)
    return clean_num.isdigit() and 10 <= len(clean_num) <= 15

# --- IMAGE GRAPHIC LAYER PROCESSING ---
def process_composite_graphic(captured_stream):
    user_img = Image.open(captured_stream)
    user_img = ImageOps.exif_transpose(user_img) 
    user_img_resized = user_img.resize((360, 410))
    canvas = Image.new('RGB', (800, 450), color='#0f172a')
    canvas.paste(user_img_resized, (20, 20))
    buffer = io.BytesIO()
    canvas.save(buffer, format='PNG')
    return buffer.getvalue()

# ==========================================
# PHASE 1: CORE AUTHENTICATION GATEWAY
# ==========================================
if "auth" not in st.session_state:
    st.title("🛠️ Build Localhost Verification Hub")
    st.write("Welcome! This system requires verification through GitHub to initialize your developer journey.")
    
    if not CLIENT_ID or not CLIENT_SECRET:
        st.error("⚠️ App Configuration Missing: Please register your GitHub Client ID and Secret within the secrets registry panel.")
    else:
        # Render the authentic GitHub Sign-In Button redirection pipeline
        # Requesting "read:user" scope to safely read their profile name and handle
        result = oauth2.authorize_button(
            name="Sign in with GitHub",
            redirect_uri=st.secrets.get("REDIRECT_URI", "http://localhost:8501"), 
            scope="read:user",
            key="github_auth_component"
        )
        
        if result and "token" in result:
            st.session_state.auth = result
            # Securely retrieve unique token access headers
            access_token = result["token"]["access_token"]
            
            # Request profile dataset metrics back from GitHub's Core API REST pipelines
            import requests
            headers = {"Authorization": f"token {access_token}"}
            user_profile = requests.get("https://api.github.com/user", headers=headers).json()
            
            # Persist authenticated details directly into Session State Memory
            st.session_state.github_handle = user_profile.get("login", "UnknownHandle")
            st.session_state.name = user_profile.get("name") if user_profile.get("name") else user_profile.get("login")
            st.rerun()
else:
    # User is Authenticated, Proceed to Core Application Layer Wizard
    st.title("🪄 Build Localhost Content Wizard")
    
    # Simple top layout indicator showing active login context tracking
    st.write(f"🔒 Signed in as: `{st.session_state.github_handle}` ({st.session_state.name})")
    
    step_cols = st.columns(3)
    with step_cols[0]:
        st.markdown(f"**Step 1: Onboarding Details** {'🟢' if st.session_state.step == 1 else '⚪'}")
    with step_cols[1]:
        st.markdown(f"**Step 2: Core Insights** {'🟢' if st.session_state.step == 2 else '⚪'}")
    with step_cols[2]:
        st.markdown(f"**Step 3: Export & Share** {'🟢' if st.session_state.step == 3 else '⚪'}")
    st.markdown("---")

    # ==========================================
    # WIZARD STEP 1: ONBOARDING DATA CAPTURE
    # ==========================================
    if st.session_state.step == 1:
        st.subheader("Step 1: Complementary Verification Details")
        
        # Name is pre-populated natively from their public profile payload data schema
        name_input = st.text_input("Full Name", value=st.session_state.name)
        email_input = st.text_input("Email Address", value=st.session_state.email, placeholder="you@domain.com")
        mobile_input = st.text_input("Mobile Number", value=st.session_state.mobile, placeholder="e.g., +919876543210")
        
        st.write("📸 Snap a picture of your environment setup configuration workspace:")
        camera_file = st.camera_input("Capture Workspace")
        
        valid = True
        if email_input and not is_valid_email(email_input):
            st.error("❌ Invalid Email formatting schema detected.")
            valid = False
        if mobile_input and not is_valid_mobile(mobile_input):
            st.error("❌ Invalid Mobile connection numeric formatting sequence (10-15 digits required).")
            valid = False
            
        if camera_file and name_input and email_input and mobile_input and valid:
            if st.button("Proceed to Next Step ➡️"):
                st.session_state.name = name_input
                st.session_state.email = email_input
                st.session_state.mobile = mobile_input
                st.session_state.photo_bytes = process_composite_graphic(camera_file)
                st.session_state.step = 2
                st.rerun()
        else:
            st.info("💡 Fill out registration fields and capture your workspace selfie to proceed forward to Step 2.")

    # ==========================================
    # WIZARD STEP 2: CAPTURING CONVERSATIONAL TEXT
    # ==========================================
    elif st.session_state.step == 2:
        st.subheader("Step 2: Document Your Breakthroughs")
        st.info("🎤 **Mobile Hack:** Click inside the text area container and hit the **Microphone option** on your phone's default spacebar keyboard to dictate text instantly without cloud audio keys!")
        
        user_text = st.text_area("What configuration milestones did you clear inside your Localhost environment today?", height=150)
        
        if st.button("Structure my LinkedIn Post ➡️"):
            if user_text.strip() == "":
                st.error("Please add a summary notes statement outlining your configuration results.")
            else:
                # Compile strict post layout removing all personal user PII parameters
                st.session_state.linkedin_post = (
                    f"🚀 Just wrapped up a hands-on lab infrastructure pipeline execution loop at #BuildLocalhost!\n\n"
                    f"🛠️ **Technical Breakthrough Milestone:**\n{user_text}\n\n"
                    f"👨‍💻 Verified Engineering Profile: github.com/{st.session_state.github_handle}\n\n"
                    f"#BuildLocalhost #DevSecOps #ProofOfWork"
                )
                st.session_state.step = 3
                st.rerun()
                
        if st.button("⬅️ Back to Step 1"):
            st.session_state.step = 1
            st.rerun()

    # ==========================================
    # WIZARD STEP 3: PREVIEW & DIRECT LINKEDIN INTENT
    # ==========================================
    elif st.session_state.step == 3:
        st.subheader("Step 3: Verification & Network Export Dashboard")
        
        if st.session_state.photo_bytes:
            st.image(st.session_state.photo_bytes, caption="Your Verified Branded Event Graphic Asset", use_container_width=True)
            
        edited_post = st.text_area("Finalized Post Text Copy (Verified PII-Free Frame Layout):", value=st.session_state.linkedin_post, height=220)
        st.markdown("---")
        
        encoded_text = urllib.parse.quote(edited_post)
        linkedin_share_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_text}"
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="💾 1. Download Branded Image",
                data=st.session_state.photo_bytes,
                file_name="build_localhost_badge.png",
                mime="image/png",
                use_container_width=True
            )
        with col2:
            st.link_button("🚀 2. Open & Paste to LinkedIn Feed", linkedin_share_url, use_container_width=True)
            
        st.info("💡 **Posting Protocol:** 1. Hit Button 1 to download your graphics asset. 2. Hit Button 2. Your custom text copies automatically directly into your LinkedIn feed creation drawer panel window. Simply click the photo upload option to append your saved canvas image!")