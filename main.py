import numpy as np
import cv2 as cv
import pyzbar.pyzbar as pyzbar
import datetime
import os

current_time = f"[{datetime.datetime.now()}]"
print(current_time)
current_directory = os.getcwd()
directory = "images"
print(current_directory)
path = os.path.join(current_directory, directory)
try:
    os.mkdir(path)
except OSError as error:
    print(f"{current_time}  {error}")

color_of_qr_rectangle = (0, 0, 255)
color_of_text = (255, 255, 255)
thickness = 2
our_QR_text = "Take a screenshot now!"

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print(f"{current_time}  Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if the frame is read correctly, ret is True
    if not ret:
        print(f"{current_time}  Can't receive frame (stream end?). Exiting ...")
        break

    barcode = pyzbar.decode(frame)

    if barcode:
        print(f"{current_time}  Recognized a barcode!")
        bdata = barcode[0].data.decode('utf-8')
        print(f"{current_time}  QR decoded: \"{bdata}\"")

    for QR in barcode:
        x, y, w, h = QR.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), color_of_qr_rectangle, thickness)
        if QR.data.decode('utf-8') == our_QR_text:
            for i in range(3, -1, -1):
                cv.waitKey(200)
                cv.putText(frame, str(i), (150, 150), cv.FONT_HERSHEY_PLAIN, 10, color_of_text, 2)
                cv.imshow('frame', frame)
                frame = cap.read()[1]  # reading a new frame before updating the countdown
                cv.waitKey(1000)
                filename = f"QRPhoto_{i}.png"
                cv.imwrite(f"{path}/{filename}", frame)
                print(f"{current_time}  Image successfully saved as {filename}")
                if i == 0:
                    image = cv.imread(f'{path}/QRPhoto_2.png')
                    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                    blurred = cv.GaussianBlur(gray, (5, 5), 0)
                    edges = cv.Canny(blurred, 50, 150)
                    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                    largest_contour = max(contours, key=cv.contourArea)

                    epsilon = 0.02 * cv.arcLength(largest_contour, True)
                    approx = cv.approxPolyDP(largest_contour, epsilon, True)

                    x, y, w, h = cv.boundingRect(approx)
                    roi = image[y:y + h, x:x + w]

                    cv.imwrite('./images/ROI.png', roi)

                    cv.waitKey(1000)
                    break
        break

    # Display the resulting frame
    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        cv.imwrite(f"{path}/Last_frame.png", frame)
        break

# When everything is done, release the capture
cap.release()
cv.destroyAllWindows()
