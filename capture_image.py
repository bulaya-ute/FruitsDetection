import cv2
import numpy as np
import os
from datetime import datetime


def adjust_brightness_contrast(image, brightness=0, contrast=0):
    brightness = int((brightness - 50) * 2.55)  # Convert scale from 0-100 to -255 to 255
    contrast = int((contrast - 50) * 2.55)  # Convert scale from 0-100 to -255 to 255

    B = np.clip(brightness, -255, 255)
    C = np.clip(contrast, -255, 255)

    if B != 0:
        if B > 0:
            shadow = B
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + B
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

    if C != 0:
        f = 131 * (C + 127) / (127 * (131 - C))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)

    return image


def save_image(frame, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = os.path.join(folder, f"{timestamp}.png")
    cv2.imwrite(filename, frame)
    print(f"Saved: {filename}")


cap = cv2.VideoCapture(1)
brightness = 50
contrast = 50

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = adjust_brightness_contrast(frame, brightness, contrast)

    # Draw the "+" in the center
    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2
    cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), (0, 255, 0), 2)
    cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), (0, 255, 0), 2)

    # Display brightness and contrast values
    text = f"Brightness: {brightness}  Contrast: {contrast}"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        brightness = min(brightness + 1, 100)
    elif key == ord('s'):
        brightness = max(brightness - 1, 0)
    elif key == ord('d'):
        contrast = min(contrast + 1, 100)
    elif key == ord('a'):
        contrast = max(contrast - 1, 0)
    elif key == ord('c'):
        save_image(frame, 'captures/instances')
    elif key == ord('b'):
        save_image(frame, 'captures/background')

cap.release()
cv2.destroyAllWindows()
