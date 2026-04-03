def read_qr_safe(image):
    """
    Cloud-safe simulated QR reader
    Prevents zbar dependency crash on Streamlit Cloud
    """

    # Simulated QR output for demo/project presentation
    parsed = {
        "BloodGroup": "O+",
        "Expiry": "42 Days",
        "DonorID": "DNR1024",
        "BagID": "BB2026"
    }

    return "VALID_QR", parsed