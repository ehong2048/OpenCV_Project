import numpy as np
import cv2

def translate(img, x, y):
    mat = np.float32([[1,0,x],[0,1,y]])
    shifted_img = cv2.warpAffine(img, mat, (img.shape[1], img.shape[0]))
    return shifted_img

def rotate(img, angle, center = None, scale=1.0):
    (height, width) = img.shape[:2]

    if center is None:
        center = (width//2, height//2)

    mat = cv2.getRotationMatrix2D(center, angle, scale)
    rotated_img = cv2.warpAffine(img, mat, (width, height))

    return rotated_img

def resize(img, width = None, height = None, inter = cv2.INTER_AREA):
    (h, w) = img.shape[:2]
    
    if width is None and height is None:
        return img
    
    if width is not None:
        r = width/float(w) #new width divided by old width of image
        dim = (width, int(h * r)) #new image dimensions is 150 by corresponding new resized height

    else:
        r = height/float(h) #new height divided by old height of image
        dim = (int(w * r), height) #new image dimensions is 150 by corresponding new resized width
    
    resized_img = cv2.resize(img, dim, interpolation = inter)

    return resized_img