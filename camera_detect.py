# A simple script to check which cameras are currently connected

import cv2


openCvVidCapIds = []

for i in range(10):
    try:
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            print(f"Camera {i} present")
            openCvVidCapIds.append(i)
            cap.release()
    except:
        pass

print(f"List of present cameras: {openCvVidCapIds}")