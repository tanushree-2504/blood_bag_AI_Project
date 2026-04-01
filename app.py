import streamlit as st
import time
import streamlit as st
import numpy as np
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import qrcode
import time

st.set_page_config(page_title="HemoTrack", layout="centered")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "splash"

# ---------------- QR FUNCTION ----------------
def read_qr_safe(image):
    try:
        decoded = decode(image)
        if not decoded:
            return "NO_QR", None

        data = decoded[0].data.decode("utf-8")

        parsed = {}
        for item in data.split("|"):
            if ":" in item:
                key, value = item.split(":")
                parsed[key.strip()] = value.strip()

        return "VALID_QR", parsed

    except:
        return "INVALID_QR", None

# ---------------- COLOR DETECTION ----------------
def detect_blood_type(image):
    img = cv2.resize(image, (200, 200))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    saturation = np.mean(hsv[:,:,1])
    value = np.mean(hsv[:,:,2])

    if value > 120 and saturation > 100:
        return "Normal Blood 🟢"
    elif value > 70:
        return "Hemolyzed Blood 🟡"
    else:
        return "Severely Degraded Blood 🔴"

# ---------------- RISK CALCULATION ----------------
def calculate_risk(condition):
    if "Normal" in condition:
        return 15
    elif "Hemolyzed" in condition:
        return 45
    else:
        return 75

# ---------------- SPLASH SCREEN ----------------
if st.session_state.page == "splash":
    st.markdown("<h1 style='text-align:center;'>🩸 HemoTrack</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>AI Blood Monitoring System</p>", unsafe_allow_html=True)

    time.sleep(3)
    st.session_state.page = "start"
    st.rerun()

# ---------------- START PAGE ----------------
elif st.session_state.page == "start":
    st.markdown("## Welcome to HemoTrack")

    if st.button("🚀 Start System"):
        st.session_state.page = "menu"
        st.rerun()

# ---------------- MENU PAGE ----------------
elif st.session_state.page == "menu":
    st.markdown("## Select Mode")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧑‍🔬 Technician"):
            st.session_state.page = "tech"
            st.rerun()

    with col2:
        if st.button("📷 Scan Blood Bag"):
            st.session_state.page = "scan"
            st.rerun()

# ---------------- TECHNICIAN PAGE ----------------
elif st.session_state.page == "tech":

    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("## 🧑‍🔬 Technician Panel")

    blood_group = st.text_input("Blood Group (e.g., B+)")
    expiry = st.text_input("Expiry Date (YYYY-MM-DD)")
    donor_id = st.text_input("Donor ID")

    if st.button("Generate QR"):

        if blood_group and expiry and donor_id:
            data = f"BloodGroup:{blood_group}|Expiry:{expiry}|DonorID:{donor_id}|Status:Valid"

            qr = qrcode.make(data)
            st.image(qr, caption="Generated QR Code")

            st.success("QR Generated Successfully")
        else:
            st.warning("Please fill all fields")

# ---------------- SCANNING PAGE ----------------
elif st.session_state.page == "scan":

    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("## 📷 Blood Bag Analysis")

    uploaded_file = st.file_uploader("Upload Blood Bag Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        img = np.array(image)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.markdown("---")

        # ---------------- QR RESULT ----------------
        qr_status, qr_data = read_qr_safe(img)

        st.subheader("🔳 QR Detection")

        if qr_status == "NO_QR":
            st.warning("QR Code Not Visible")

        elif qr_status == "INVALID_QR":
            st.info("QR Detected but Unreadable")

        else:
            st.success("QR Code Detected")
            st.write(qr_data)

        # ---------------- BLOOD CONDITION ----------------
        condition = detect_blood_type(img)

        st.subheader("🩸 Blood Condition")
        st.write(condition)

        # ---------------- RISK ----------------
        risk = calculate_risk(condition)

        st.subheader("📊 Health Risk Score")
        st.progress(risk)
        st.write(f"Risk Level: {risk}%")

        # ---------------- FINAL RESULT ----------------
        st.subheader("🚨 Final Diagnosis")

        if risk < 40:
            st.success("🟢 SAFE BLOOD")
        elif risk < 60:
            st.warning("🟡 NEEDS ATTENTION")
        else:
            st.error("🔴 HIGH RISK DETECTED")

        st.markdown("---")
        st.info("Analysis Complete")