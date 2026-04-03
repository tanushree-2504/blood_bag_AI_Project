def detect_blood_type(image):
    import numpy as np

    img = np.array(image)

    # Resize manually (without cv2)
    img = img[:200, :200]

    # Average RGB values
    avg_color = np.mean(img, axis=(0, 1))

    r, g, b = avg_color

    # Detection logic
    if r > 150 and g < 80:
        return "Normal Blood 🟢"
    elif r > 100:
        return "Hemolyzed Blood 🟡"
    else:
        return "Severely Degraded Blood 🔴"