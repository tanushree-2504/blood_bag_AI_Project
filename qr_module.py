from pyzbar.pyzbar import decode

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

        if "BloodGroup" in parsed and "Expiry" in parsed:
            return "VALID_QR", parsed
        else:
            return "INVALID_QR", None

    except:
        return "INVALID_QR", None