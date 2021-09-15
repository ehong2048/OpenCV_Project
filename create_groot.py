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

    if use_inv:
        (T, thresh) = cv2.threshold(blurred_img, thresh_val, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow("Inverse Thresh", thresh)
    else:
        (T, thresh) = cv2.threshold(blurred_img, thresh_val, 255, cv2.THRESH_BINARY)
        # cv2.imshow("Thresh", thresh)
    print(T)

    cropped_img = cv2.bitwise_and(img, img, mask = thresh)
    return cropped_img



groot_path = "/Users/emma/Documents/GitHub/openCV_project/OpenCV_Project/images/groot.jpeg"
groot = cv2.imread(groot_path)
groot = crop_image(groot, 200, True)
cv2.imshow("Groot!", groot)

wings_path = "/Users/emma/Documents/GitHub/openCV_project/OpenCV_Project/images/wings.jpeg"
wings = cv2.imread(wings_path)[100:700,:] # take slice of image to avoid the vectorstock thing at bottom
cv2.imshow("Original Wings!", wings)
wings = crop_image(wings, 254, True)
cv2.imshow("Wings!", wings)


cv2.waitKey(0)
