import numpy as np
import argparse
import cv2
import imutils

"""
Functionality: loads and displays image of Groot that is cropped to be just Groot's outline
Uses thresholding and mask on image 
"""

def crop_image(img, thresh_val = 150, use_inv = True):
    """
    Purpose: Loads passed in image and then returns the cropped image without the background
    using simple inverse threshold and mask for bitwise_and
    Parameters: original image, int threshold value, Boolean value for whether to use inverse threshold or not
    Return: cropped image
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5,5), 0)

    if use_inv: # inverse threshold
        (T, thresh) = cv2.threshold(blurred_img, thresh_val, 255, cv2.THRESH_BINARY_INV)
    else:
        # pixels above thresh_val are set to 255, pixels below are set to 0
        (T, thresh) = cv2.threshold(blurred_img, thresh_val, 255, cv2.THRESH_BINARY) 
    print(f'Threshold Value: {T}')

    # use threshold as mask to only focus on pixels that are on in thresh
    cropped_img = cv2.bitwise_and(img, img, mask = thresh) 

    return cropped_img


# CH.1 - load, display, save image
groot_path = "/Users/emma/Documents/GitHub/openCV_project/OpenCV_Project/images/groot.jpeg"
groot = cv2.imread(groot_path)
groot = crop_image(groot, 250, True)
cv2.imshow("Groot!", groot)

g_width = groot.shape[1]
g_height = groot.shape[0]
print(f'Groot Width: {g_width}, Groot Height: {g_height}')

wings_path = "/Users/emma/Documents/GitHub/openCV_project/OpenCV_Project/images/groot_wings.jpeg"
wings = cv2.imread(wings_path)
cv2.imshow("Original Wings!", wings)
wings = crop_image(wings, 254, True)
cv2.imshow("Wings!", wings)

w_width = wings.shape[1]
w_height = wings.shape[0]
print(f'Original Wings Width: {w_width}, Original Wings Height: {w_height}')

# CH. 6 Image Transformations - Resizing
r = g_width/w_width
dim = (g_width, int(w_height * r))
resized_wings = cv2.resize(wings, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("Resized Wings!", resized_wings)


# CH. 4 Image Basics - Accessing and manipulating pixels
for x in range(g_width):
   for y in range(g_height):
        (b, g, r) = groot[x, y]
        if b != 0 and g != 0 and r != 0: # if the pixel is on
            resized_wings[x, y] = groot[x, y] # overlays pixel in groot's image on pixel in wing's image 
cv2.imshow("Groot with Wings!", resized_wings)






cv2.waitKey(0)
