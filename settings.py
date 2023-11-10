import cv2 as cv

# Settings
camera_choice = 1
frame_width = 1280
frame_height = 720
qr_rectangle_color = (0, 0, 255)
text_start_point = (frame_width // 2 - 20, frame_height // 2)
text_font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 5
text_color = (0, 0, 255)
thickness = 5
our_QR_text = "Take a screenshot now!"
