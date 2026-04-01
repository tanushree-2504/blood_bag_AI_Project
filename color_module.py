import cv2
import numpy as np

def detect_blood_type(image):

    img = cv2.resize(image, (200, 200))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue = np.mean(hsv[:, :, 0])
    saturation = np.mean(hsv[:, :, 1])
    value = np.mean(hsv[:, :, 2])

    if value > 120 and saturation > 100:
        return "Normal"

    elif value > 70:
        return "Hemolyzed"

    else:
        return "Severely Degraded"