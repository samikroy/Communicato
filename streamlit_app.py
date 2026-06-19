import streamlit as st
import pandas as pd
from PIL import Image, ImageOps
import io
import urllib.parse

# --- PAGE SETUP & THEME ---
st.set_page_config(
    page_title="Build Localhost - Social Share Hub",
    page_icon="📸",
    layout="centered"
)

# Custom minimalistic styling matching your enterprise dark/indigo aesthetic
st.markdown("""
    <style>
    .reportview-container { background: #0b0f19; }
    div.stButton > button:first-child {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
    }
    .linkedin-card {
        background-color: #1d2226;
        border: 1px solid #38434f;
        border-radius: 10px;
        padding: 16px;
        color: #eef3f8;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📸 Build Localhost Post Creator")
st.write("Snap a live photo, add your core takeaway insights, and instantly export a tailored LinkedIn proof-of-work post.")

# --- STEP 1: INITIALIZE BACKGROUND TEMPLATE ---
# Creating a fallback blank indigo background banner if an external asset isn't present
@st.cache_data
def get_preset_background():
    # In production, replace this with your branded asset: Image.open("assets/event_banner.png")
    # For now, we dynamically generate a sleek dark indigo canvas block template
    img = Image.new('RGB', (800, 450), color='#1e1b4b')
    return img

preset_bg = get_preset_background()

# --- STEP 2: MOBILE CAMERA CAPTURE HUB ---
st.subheader("Step 1: Capture Your Workspace Photo")
captured_file = st.camera_input("Take a selfie or capture your local configuration setup")

processed_image = None

if captured_file:
    # Open captured file stream with PIL
    user_img = Image.open(captured_file)
    
    # Auto-rotate based on mobile EXIF data metadata protocols
    user_img = ImageOps.exif_transpose(user_img)
    
    # Process & Resize user photo to fit elegantly into a split frame format inside the asset banner
    user_img_resized = user_img.resize((360, 410))
    
    # Paste user image layer securely over the preset brand template base canvas
    final_canvas = preset_bg.copy()
    final_canvas.paste(user_img_resized, (20, 20))
    
    # Save composite output image to byte buffer layout
    img_byte_arr = io.BytesIO()
    final_canvas.save(img_byte_arr, format='PNG')
    processed_image = img_byte_arr.getvalue()
    
    st.success("🖼️ Branded event graphic compiled perfectly!")
    st.image(final_canvas, caption="Your Event Share Graphic Preview", use_container_width=True)

# --- STEP 3: CAPTION ENGINE ---
st.subheader("Step 2: Write Your Key Breakthrough Insight")
default_caption = "🚀 Just wrapped up a hands-on lab pipeline at the #BuildLocalhost event! Built an end-to-end framework locally from scratch. Real proof-of-work over theory."
user_caption = st.text_area("What was your primary technical milestone breakthrough today?", value=default_caption, height=100)

# --- STEP 4: REAL-TIME LINKEDIN SIMULATOR CARD ---
if processed_image:
    st.markdown("---")
    st.subheader("Step 3: LinkedIn Post Simulated Preview")
    
    # Construct a layout box block that accurately mimics modern desktop/mobile LinkedIn feeds
    st.markdown(f"""
    <div class="linkedin-card">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            <div style="background-color: #56687a; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; margin-right: 10px;">
                YO
            </div>
            <div>
                <div style="font-size: 14px; font-weight: 600; color: #f3f6f8;">You (Attendee Profile)</div>
                <div style="font-size: 11px; color: #939bb4;">Software Engineer & Builder • Just now</div>
            </div>
        </div>
        <div style="font-size: 13px; line-height: 1.4; margin-bottom: 12px; white-space: pre-wrap; color: #d0d7de;">{user_caption}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the compiled card image inside the custom css container box block framework
    st.image(processed_image, use_container_width=True)
    
    # --- STEP 5: REDIRECT DIRECT SHARE ACTION LAUNCHER ---
    st.markdown("### Step 4: Share with your professional network")
    
    # Prepare the URL encoded text share parameter vector
    encoded_text = urllib.parse.quote(user_caption)
    linkedin_intent_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_text}"
    
    col1, col2 = st.columns(2)
    with col1:
        # Prompt user to download image file locally first
        st.download_button(
            label="💾 1. Download Branded Image",
            data=processed_image,
            file_name="build_localhost_moment.png",
            mime="image/png",
            use_container_width=True
        )
    with col2:
        # Open LinkedIn Share box dialog endpoint path natively
        st.link_button("🌐 2. Open & Paste to LinkedIn", linkedin_intent_url, use_container_width=True)
        
    st.info("💡 **How to publish:** Click Button 1 to save the premium generated image asset, then click Button 2. Your custom text will copy forward instantly into the composition dashboard screen, where you can attach your picture asset.")
else:
    st.info("📸 Snap a photo above using your device camera interface to activate the live LinkedIn post renderer engine.")