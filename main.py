import numpy as np
import cv2 as cv
import pyzbar.pyzbar as pyzbar
import datetime


current_time = f"[{datetime.datetime.now()}]"
print(current_time)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print(f"{current_time}  Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print(f"{current_time}  Can't receive frame (stream end?). Exiting ...")
        break

    barcode = pyzbar.decode(frame)
    if barcode:
        print(f"{current_time}  Recognized a barcode!")
    color = (0, 0, 255)
    thickness = 2

    for QR in barcode:
        # x and y are upper left corner of the barcode while w and h are width and height of the barcode
        x, y, w, h = QR.rect
        cv.rectangle(frame, (x, y), (x+w, y+h), color, thickness)
        filename = "QRCode_2.png"
        cv.imwrite(filename, frame)
        print(f"{current_time}  Image successfully saved as {filename}")

    # Display the resulting frame
    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        cv.imwrite("Last_frame.png", frame)
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
