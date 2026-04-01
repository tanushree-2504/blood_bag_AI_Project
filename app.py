import streamlit as st
import time
import numpy as np
from PIL import Image

from modules.qr_module import read_qr_safe
from modules.color_module import detect_blood_type
from modules.risk_module import calculate_risk

st.set_page_config(page_title="HemoTrack", layout="centered")

# ---------------- SESSION STATE ---------------- #
if "page" not in st.session_state:
    st.session_state.page = "splash"

# ---------------- SPLASH SCREEN ---------------- #
if st.session_state.page == "splash":
    st.markdown("<h1 style='text-align:center;'>🩸 HemoTrack</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>AI Blood Monitoring System</p>", unsafe_allow_html=True)
    
    time.sleep(3)  # 3–5 seconds
    st.session_state.page = "start"
    st.rerun()

# ---------------- START PAGE ---------------- #
elif st.session_state.page == "start":
    st.markdown("<h2 style='text-align:center;'>Welcome to HemoTrack</h2>", unsafe_allow_html=True)

    if st.button("🚀 Start System"):
        st.session_state.page = "menu"
        st.rerun()

# ---------------- MENU PAGE ---------------- #
elif st.session_state.page == "menu":
    st.markdown("## Select Mode")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧑‍🔬 Technician"):
            st.session_state.page = "technician"
            st.rerun()

    with col2:
        if st.button("📷 Scan Blood Bag"):
            st.session_state.page = "scan"
            st.rerun()

# ---------------- TECHNICIAN PAGE ---------------- #
elif st.session_state.page == "technician":

    st.markdown("## 🧑‍🔬 Technician Panel")

    # BACK BUTTON
    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("### Enter Blood Details")

    blood_group = st.text_input("Blood Group (e.g., B+)")
    expiry = st.date_input("Expiry Date")
    donor_id = st.text_input("Donor ID")

    if st.button("Generate QR"):
        import qrcode

        data = f"BloodGroup:{blood_group}|Expiry:{expiry}|DonorID:{donor_id}|Status:Valid"

        qr = qrcode.make(data)
        st.image(qr, caption="Generated QR")

# ---------------- SCANNING PAGE ---------------- #
elif st.session_state.page == "scan":

    st.markdown("## 📷 Blood Bag Scanning")

    # BACK BUTTON
    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        img = np.array(image)

        st.image(image, caption="Uploaded Image")

        # QR Detection
        qr_status, qr_data = read_qr_safe(img)

        st.subheader("QR Status")

        if qr_status == "NO_QR":
            st.warning("QR Not Visible")

        elif qr_status == "INVALID_QR":
            st.info("QR Detected but Unreadable")

        else:
            st.success("QR Detected")

        # Blood Condition
        condition = detect_blood_type(img)

        st.subheader("Blood Condition")
        st.write(condition)

        # Risk
        risk = calculate_risk(condition)

        st.subheader("Risk Score")
        st.progress(risk)
        st.write(f"{risk}%")

        # Final Result
        if risk < 40:
            st.success("SAFE")
        elif risk < 60:
            st.warning("NEEDS ATTENTION")
        else:
            st.error("HIGH RISK")