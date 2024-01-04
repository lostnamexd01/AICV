import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import cv2

def divide_img_blocks(image):
    height, width = image.shape[:2]

    # Calculate the midpoint for height and width
    mid_height, mid_width = height // 2, width // 2

    # Split the image into four parts
    top_left = image[0:mid_height, 0:mid_width]
    top_right = image[0:mid_height, mid_width:width]
    bottom_left = image[mid_height:height, 0:mid_width]
    bottom_right = image[mid_height:height, mid_width:width]

    return [top_left, top_right, bottom_left, bottom_right]

image = cv2.imread("./images/Cropped_paper_0.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

result = divide_img_blocks(image)
fig = plt.figure(figsize=(8, 16))

model = tf.keras.models.load_model("./ai_model.keras")

for i in range(4):
    img = result[i]
    fig.add_subplot(2, 2, i + 1)
    plt.imshow(img)
    plt.axis("off")
    t = cv2.imread(img)
    t_input = cv2.resize(t, (256, 256))
    input = t_input.reshape((1, 256, 256, 3))
    prediction = model.predict(input)
    if prediction > 0.5:
        plt.title("Dog")
    else:
        plt.title("Cat")

plt.show()