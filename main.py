import numpy as np
import os
import cv2 as cv
import pyzbar.pyzbar as pyzbar
import logging
import compare_photos
import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s     %(levelname)s     %(message)s'
)

logging.info('Starting program')

# Create an image_directory for saving images
current_directory = os.getcwd()
image_directory = 'images'
logging.info(f'Current working directory: {current_directory}')

path = os.path.join(current_directory, image_directory)
try:
    os.mkdir(path)
except OSError as error:
    logging.warning(f'Error while creating directory: {error}')


# Open the camera and set resolution (you can check available cameras using 'camera_detect' script)
# DSHOW is an interface to the video I/O library provided by OS
cap = cv.VideoCapture(settings.camera_choice, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, settings.frame_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, settings.frame_height)

if not cap.isOpened():
    logging.error('Cannot open camera')
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if the frame is read correctly, ret is True
    if not ret:
        logging.error("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the frame
    cv.imshow('frame', frame)

    # Decode QR codes in the frame
    barcode = pyzbar.decode(frame)

    if barcode:
        logging.info('Recognized a barcode!')
        bdata = barcode[0].data.decode('utf-8')
        logging.info(f'QR decoded: \"{bdata}\"')

        for QR in barcode:
            x, y, w, h = QR.rect
            cv.rectangle(frame, (x, y), (x + w, y + h), settings.qr_rectangle_color, settings.thickness)

            if QR.data.decode('utf-8') == settings.our_QR_text:
                for i in range(3, -1, -1):
                    cv.putText(frame, str(i), settings.text_start_point, settings.text_font, settings.font_scale,
                               settings.text_color, settings.thickness, cv.LINE_AA)
                    cv.imshow('frame', frame)
                    frame = cap.read()[1]  # Read a new frame before updating the countdown
                    filename_capture = f'QRPhoto_{i}.png'
                    cv.imwrite(f'{path}/{filename_capture}', frame)
                    logging.info(f'Image successfully saved as {filename_capture}')
                    cv.waitKey(1000)

                    # Extracting the paper from the photo after the countdown
                    if i == 0:
                        for j in range(0, 4):
                            image_name = f'QRPhoto_{j}.png'
                            filename_cropped = f'Cropped_paper_{j}.png'
                            image = cv.imread(f'{path}/{image_name}')

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

                            # Contour approximation
                            epsilon = 0.01 * cv.arcLength(largest_contour, True)
                            approx = cv.approxPolyDP(largest_contour, epsilon, True)

                            # Apply Geometrical Transform The approxPolyDP's first output coordinate is of the lowest
                            # point, so either bottom left or bottom right and then the other coordinates are
                            # outputted clockwise. The if statement decides whether the first one is bottom left or
                            # bottom right
                            if approx[0][0][0] > (approx[1][0][0] + 200):

                                pts1 = np.float32([approx[0], approx[1], approx[2], approx[3]])
                                pts2 = np.float32([[1280, 0], [0, 0], [0, 720], [1280, 720]])

                                matrix = cv.getPerspectiveTransform(pts1, pts2)
                                transformed_frame = cv.warpPerspective(image, matrix, (1280, 720))

                            else:
                                pts1 = np.float32([approx[0], approx[1], approx[2], approx[3]])
                                pts2 = np.float32([[0, 0], [0, 720], [1280, 720], [1280, 0]])

                                matrix = cv.getPerspectiveTransform(pts1, pts2)
                                transformed_frame = cv.warpPerspective(image, matrix, (1280, 720))

                            cv.imwrite(f'{path}/{filename_cropped}', transformed_frame)
                            logging.info(f'Cropped image successfully saved as {filename_cropped}')

                cv.waitKey(1000)
                break

    # End the capture after pressing 'q'
    if cv.waitKey(1) == ord('q'):
        break


# Release the camera and close all windows
cap.release()
cv.destroyAllWindows()

# Using compare function from compare_photos file to check which photo is the best quality
logging.info('Comparing quality of Cropped Images')
compare_photos.compare()
logging.info('Ending program')
