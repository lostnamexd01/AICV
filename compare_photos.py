import cv2
import numpy as np


def calculate_sharpness(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    return sharpness


def calculate_noise(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noise = np.std(gray)
    return noise


def compare():
    # Initialize variables to keep track of the best image and its quality
    best_image = None
    best_quality = -1
    for i in range(0, 4):
        image_name = f'Cropped_paper_{i}.png'
        image = cv2.imread(f'./images/{image_name}')

        sharpness = calculate_sharpness(image)
        noise = calculate_noise(image)

        # Calculate an overall quality score (you can define your own metric)
        quality = sharpness - noise

        print(f'Current photo: {image_name}\n\tQuality: {quality:.2f}', flush=True)
        # Check if this image has higher quality than the current best
        if quality > best_quality:
            best_image = image
            best_quality = quality
            best_image_name = image_name

    # Display the best image
    if best_image is not None:
        print(f'Best Image Quality: {best_quality:.2f}', flush=True)
        print(f'Best Image Name: {best_image_name}', flush=True)

    else:
        print("No valid images found in the folder.")
