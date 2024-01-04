import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import cv2

def divide_img_blocks(img, n_blocks=(2,2)):
   horizontal = np.array_split(img, n_blocks[0])
   splitted_img = [np.array_split(block, n_blocks[1], axis=1) for block in horizontal]
   return np.asarray(splitted_img, dtype=np.ndarray).reshape(n_blocks)


def predict(img):
    result = divide_img_blocks(img)
    model = tf.keras.models.load_model("./ai_model.keras")

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            t = cv2.imread(result[i,j])
            plt.imshow(t)
            t_input = cv2.resize(t,(256,256))
            input = t_input.reshape((1,256,256,3))
            z = model.predict(input)
            if(z > 0.5):
                print("dog")
            else:
                print("cat")
    
    
    