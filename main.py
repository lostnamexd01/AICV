import numpy as np
import os
import cv2 as cv
import pyzbar.pyzbar as pyzbar
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s     %(levelname)s     %(message)s"
)

logging.info("Starting program")

# Create a directory for saving images
current_directory = os.getcwd()
directory = "images"
logging.info(f"Current working directory: {current_directory}")

path = os.path.join(current_directory, directory)
try:
    os.mkdir(path)
except OSError as error:
    logging.warning(f"{error}")

# Some settings
frame_width = 1280
frame_height = 720
qr_rectangle_color = (0, 0, 255)
text_start_point = (frame_width//2, frame_height//2)
text_font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 5
text_color = (0, 0, 255)
thickness = 5
our_QR_text = "Take a screenshot now!"


# Open the default camera and set resolution (you can check available cameras using 'camera_detect' script)
# DSHOW is an interface to the video I/O library provided by OS
cap = cv.VideoCapture(1, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, frame_height)


if not cap.isOpened():
    logging.error("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if the frame is read correctly, ret is True
    if not ret:
        logging.error("Can't receive frame (stream end?). Exiting ...")
        break

    # Get frame dimensions
    (frame_height, frame_width) = frame.shape[:2]

    # Display the frame
    cv.imshow('frame', frame)

    # Decode QR codes in the frame
    barcode = pyzbar.decode(frame)

    if barcode:
        logging.info("Recognized a barcode!")
        bdata = barcode[0].data.decode('utf-8')
        logging.info(f"QR decoded: \"{bdata}\"")

    for QR in barcode:
        x, y, w, h = QR.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), qr_rectangle_color, thickness)

        if QR.data.decode('utf-8') == our_QR_text:
            for i in range(3, -1, -1):
                cv.waitKey(200)
                cv.putText(frame, str(i), text_start_point, text_font, font_scale, text_color, thickness, cv.LINE_AA)
                cv.imshow('frame', frame)
                frame = cap.read()[1]  # Read a new frame before updating the countdown
                cv.waitKey(1000)
                filename_capture = f"QRPhoto_{i}.png"
                cv.imwrite(f"{path}/{filename_capture}", frame)
                logging.info(f"Image successfully saved as {filename_capture}")

                # Extracting the paper from the photo after the countdown
                if i == 0:
                    image = cv.imread(f'{path}/QRPhoto_2.png')

                    # Convert the image to grayscale for easier processing
                    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                    # Apply Gaussian blur to reduce noise
                    blurred = cv.GaussianBlur(gray, (5, 5), 0)
                    # Apply Canny edge detection for finding edges in the image
                    edges = cv.Canny(blurred, 50, 150)
                    # Find contours in the edge-detected image
                    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                    # Get the largest contour (the paper with photos printed)
                    largest_contour = max(contours, key=cv.contourArea)

                    # Extract the region of interest using the largest contour
                    x, y, w, h = cv.boundingRect(largest_contour)
                    roi = image[y:y + h, x:x + w]

                    filename_cropped = "ROI.png"
                    cv.imwrite(f"{path}/{filename_cropped}", roi)
                    logging.info(f"Cropped image successfully saved as {filename_cropped}")

                    cv.waitKey(1000)

            break

    # End the capture after pressing 'q'
    if cv.waitKey(1) == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv.destroyAllWindows()

logging.info("Ending program")
