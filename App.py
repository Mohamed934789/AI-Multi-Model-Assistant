import streamlit as st
from handlers.image_captioner import caption_image
from handlers.text_generator import generate_text
from handlers.summarizer import summarize_text
from handlers.sentiment import analyze_sentiment

# ---------------------------------------------------------
# إعدادات الصفحة العامة
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Multi-Model Assistant",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# ستايل فخم + أنيميشن (CSS مضمّن)
# ---------------------------------------------------------
st.markdown(
    """
    <style>

    /* Import a premium font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Hide Streamlit's default header/toolbar completely */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Hide the hamburger menu + "Deploy" button + footer for a clean, branded look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header [data-testid="stToolbar"] {visibility: hidden;}

    /* Remove default top padding since header is now invisible */
    .block-container {
        padding-top: 2rem;
    }

    /* خلفية متدرجة متحركة */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientMove 15s ease infinite;
    }

    @keyframes gradientMove {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* العنوان الرئيسي */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd700, #ff8c00, #ff00ff, #00e0ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s ease infinite;
        margin-bottom: 0px;
        padding-top: 10px;
    }

    @keyframes shine {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .sub-title {
        text-align: center;
        color: #d0d0d0;
        font-size: 1.1rem;
        margin-bottom: 30px;
        opacity: 0.85;
    }

    /* بطاقة زجاجية (Glassmorphism) تلف عناصر الإدخال */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        animation: fadeInUp 0.8s ease;
        margin-bottom: 20px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(25px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* حقول الإدخال */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.08) !important;
        color: #fff !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
    }

    /* File uploader — match the glass theme */
    [data-testid="stFileUploader"] section {
        background: rgba(255,255,255,0.06) !important;
        border: 1px dashed rgba(255,255,255,0.3) !important;
        border-radius: 14px !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #e0e0e0 !important;
    }

    [data-testid="stFileUploader"] button {
        background: linear-gradient(90deg, #00e0ff, #ff00ff) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
    }

    /* Uploaded file preview chip */
    [data-testid="stFileUploaderFile"] {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    /* زر رئيسي فخم */
    .stButton>button {
        background: linear-gradient(90deg, #ff8c00, #ff00ff);
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        border: none;
        border-radius: 14px;
        padding: 12px 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 255, 0.4);
    }

    .stButton>button:hover {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 140, 0, 0.6);
    }

    /* صندوق النتيجة */
    .result-box {
        background: rgba(255,255,255,0.07);
        border-left: 4px solid #ff8c00;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        color: #f5f5f5;
        animation: fadeInUp 0.6s ease;
    }

    /* رسائل التحذير تتماشى مع الثيم */
    .stAlert {
        border-radius: 12px !important;
    }

    /* تذييل بسيط */
    .footer-note {
        text-align: center;
        color: rgba(255,255,255,0.4);
        font-size: 0.8rem;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# الهيدر
# ---------------------------------------------------------
st.markdown('<div class="main-title">✨ AI Multi-Model Assistant ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your smart assistant for text generation, summarization, sentiment analysis, and image captioning</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# بطاقة الإدخال الرئيسية
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

options = st.selectbox(
    "🎯 Choose an action:",
    ["Generate Response", "Summarize Text", "Analyze Sentiment", "Image Captioning"],
)

handlers = {
    "Generate Response": generate_text,
    "Summarize Text": summarize_text,
    "Analyze Sentiment": analyze_sentiment,
}

if options == "Image Captioning":
    uploaded_file = st.file_uploader("📷 Choose an image...", type=["jpg", "jpeg", "png"])
else:
    user_input = st.text_input("💬 Write your prompt here:")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# منطق التنفيذ
# ---------------------------------------------------------
if options == "Image Captioning":
    if uploaded_file is None:
        st.warning("⚠️ Please upload an image first.")
    else:
        with st.spinner("🔮 Analyzing image..."):
            image_bytes = uploaded_file.read()
            caption = caption_image(image_bytes)
        st.image(image_bytes, caption="🖼️ Uploaded Image", use_container_width=True)
        st.markdown(f'<div class="result-box"><b>📝 Caption:</b><br>{caption}</div>', unsafe_allow_html=True)

else:
    if not user_input or user_input.strip() == "":
        st.warning("⚠️ Please enter a prompt before continuing.")
    else:
        if st.button(f"🚀 {options}"):
            selected_function = handlers[options]
            with st.spinner("✨ Processing..."):
                result = selected_function(user_input)
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown('<div class="footer-note">Powered by AI ⚡ Crafted with care</div>', unsafe_allow_html=True)