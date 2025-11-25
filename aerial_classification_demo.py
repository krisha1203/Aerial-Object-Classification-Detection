import streamlit as st
from PIL import Image
import time
import random

# Page styling (mimic your React bg gradient with similar colors)
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0f172a 100%);
        color: white;
        min-height: 100vh;
        padding: 2rem 1rem;
    }
    .upload-area {
        border: 2px dashed #475569;
        border-radius: 1rem;
        height: 16rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        background-color: #334155cc;
        transition: background-color 0.3s;
    }
    .upload-area:hover {
        background-color: #334155ee;
    }
    .btn-primary {
        background-color: #2563eb;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        border: none;
        width: 100%;
        cursor: pointer;
        font-weight: 600;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        font-size: 1rem;
        transition: background-color 0.3s;
    }
    .btn-primary:disabled {
        background-color: #64748b;
        cursor: not-allowed;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; margin-bottom:3rem;">
        <h1 style="font-weight:bold; font-size:2.5rem;">Aerial Object Classification</h1>
        <p style="color:#7dd3fc; font-size:1.2rem;">AI-Powered Bird vs Drone Detection System</p>
        <p style="color:#94a3b8;">Upload an aerial image to classify whether it contains a bird or drone</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2>Upload Image</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png","jpg","jpeg"], label_visibility="collapsed")

    preview = None
    prediction = None
    loading = False

    if uploaded_file is not None:
        preview = Image.open(uploaded_file).convert("RGB")
        st.image(preview, use_container_width=True, caption="Preview")


    def simulate_prediction():
        time.sleep(1.5)
        preds = [
            {"class": "Bird", "confidence": 0.94, "color": "#16a34a"},
            {"class": "Drone", "confidence": 0.89, "color": "#2563eb"},
            {"class": "Bird", "confidence": 0.96, "color": "#16a34a"},
            {"class": "Drone", "confidence": 0.92, "color": "#2563eb"},
        ]
        return random.choice(preds)

    # Using session state to maintain prediction and loading state
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    if 'loading' not in st.session_state:
        st.session_state.loading = False

    def classify():
        st.session_state.loading = True
        st.session_state.prediction = None
        st.rerun()


    if uploaded_file:
        if st.button("Classify Image", key="classify_btn", disabled=st.session_state.loading):
            classify()

    # If loading simulate the delay and set prediction
    if st.session_state.loading:
        with st.spinner("Classifying..."):
            time.sleep(1.5)
            st.session_state.prediction = simulate_prediction()
        st.session_state.loading = False
        st.rerun()


with col2:
    st.markdown('<h2>Prediction Results</h2>', unsafe_allow_html=True)

    if (uploaded_file is None) and not st.session_state.loading:
        st.info("Upload an image and click classify to see results")
    elif st.session_state.loading:
        st.info("Analyzing image...")
    elif st.session_state.prediction and not st.session_state.loading:
        pred = st.session_state.prediction

        st.markdown(f"""
        <div style="background:#334155cc; border-radius:1rem; padding:1rem; border:1px solid #475569; margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
                <span style="color:#94a3b8;">Detected Class:</span>
                <span style="font-weight:bold; font-size:1.5rem; color:{pred['color']};">{pred['class']}</span>
            </div>
            <div style="margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#94a3b8;">
                    <span>Confidence Score:</span>
                    <span style="font-weight:bold; color:#fff;">{pred['confidence']*100:.1f}%</span>
                </div>
                <div style="background:#475569; height:0.7rem; border-radius:1rem; overflow:hidden;">
                    <div style="background: linear-gradient(90deg,#2563eb,#16a34a); height:0.7rem; width:{pred['confidence']*100}%; transition: width 1s;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#3341557a; padding:1rem; border-radius:1rem; border:1px solid #475569;">
            <h3 style="color:#fff; margin-bottom:0.5rem;">Model Information</h3>
            <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#94a3b8; margin-bottom:0.2rem;">
                <span>Architecture:</span><span>Transfer Learning (ResNet50)</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#94a3b8; margin-bottom:0.2rem;">
                <span>Input Size:</span><span>224 × 224 pixels</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#94a3b8;">
                <span>Classes:</span><span>Bird, Drone</span>
            </div>
        </div>
        """ , unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#1e40af4d; border-radius: 1rem; padding: 1rem; border: 1px solid #1e3a8a; margin-top:1rem;">
            <p style="color:#7dd3fc;"><strong>Use Case:</strong> This model helps in security surveillance, wildlife protection, and airspace safety by accurately distinguishing between birds and drones.</p>
        </div>
        """, unsafe_allow_html=True)

# Features section below main content
st.markdown('<div style="margin-top:3rem;"></div>', unsafe_allow_html=True)
features_col1, features_col2, features_col3 = st.columns(3)

features_col1.markdown("""
<div style="color:#4ade80; font-weight:600; margin-bottom:0.5rem;">✓ High Accuracy</div>
<p style="color:#94a3b8; font-size:0.9rem;">Trained on 2,662+ images with advanced deep learning techniques</p>
""", unsafe_allow_html=True)

features_col2.markdown("""
<div style="color:#38bdf8; font-weight:600; margin-bottom:0.5rem;">✓ Real-Time Detection</div>
<p style="color:#94a3b8; font-size:0.9rem;">Fast inference for immediate classification and threat assessment</p>
""", unsafe_allow_html=True)

features_col3.markdown("""
<div style="color:#a78bfa; font-weight:600; margin-bottom:0.5rem;">✓ Transfer Learning</div>
<p style="color:#94a3b8; font-size:0.9rem;">Leverages pre-trained models like ResNet50 and MobileNet</p>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
