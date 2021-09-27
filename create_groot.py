import numpy as np
import argparse
import cv2
import imutils

"""
Functionality: loads and displays image of Groot that is cropped to be just Groot's outline
Uses thresholding and mask on image 
"""

def crop_image(img, thresh_val = 150, use_inv = True, use_adaptive = False):
    """
    Purpose: Loads passed in image and then returns the cropped image without the background
    using simple inverse threshold and mask for bitwise_and
    Parameters: original image, int threshold value, Boolean value for whether to use inverse threshold or not
    Return: cropped image
    """
    # CH.9 Simple thresholding and adaptive thresholding
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (5,5), 0)

    if use_inv: # inverse threshold
        if use_adaptive:
            thresh = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 0)
        else:
            (T, thresh) = cv2.threshold(blurred_img, thresh_val, 255, cv2.THRESH_BINARY_INV)
    else:
        if use_adaptive:
            thresh = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 0)
        else:
            # pixels above thresh_val are set to 255, pixels below are set to 0
            (T, thresh) = cv2.threshold(blurred_img, thresh_val, 255, cv2.THRESH_BINARY) 
            print(f'Threshold Value: {T}')

    # use threshold as mask to only focus on pixels that are on in thresh
    cropped_img = cv2.bitwise_and(img, img, mask = thresh) 

    return cropped_img

# CH.1 Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("--character", required = True, help = "string with name of character: groot, hulk, perry, or joseph")
args = vars(parser.parse_args())

if args["character"] == "groot":
    char_path = "images/groot.jpeg"
    thresh_val = 250
    use_inv = True
elif args["character"] == "hulk":
    char_path = "images/hulk.jpeg"
    thresh_val = 250
    use_inv = True
elif args["character"] == "perry":
    char_path = "images/perry.png"
    thresh_val = 40
    use_inv = False
elif args["character"] == "joseph":
    char_path = "images/joseph.jpeg"
    thresh_val = 254
    use_inv = True
else:
    print("Error: No character with that name. Use --help to see options.")
    quit()

# CH.1 - load, display, save image
char = cv2.imread(char_path)
cv2.imshow("Original Character!", char)
cv2.waitKey(0)
char = crop_image(char, thresh_val, use_inv, False)
cv2.imshow("Cropped Character!", char)
cv2.waitKey(0)


char_width = char.shape[1]
char_height = char.shape[0]
print(f'Character Width: {char_width}, Character Height: {char_height}')

wings_path = "/Users/emma/Documents/GitHub/openCV_project/OpenCV_Project/images/groot_wings.jpeg"
wings = cv2.imread(wings_path)
cv2.imshow("Original Wings!", wings)
wings = crop_image(wings, 254, True)
cv2.imshow("Cropped Wings!", wings)
cv2.waitKey(0)

w_width = wings.shape[1]
w_height = wings.shape[0]
print(f'Original Wings Width: {w_width}, Original Wings Height: {w_height}')

# CH. 6 Image Transformations - Resizes wings and character to 400 by 400
# This is so that overlaying char over wings is easier and fits better, and also fits in canvas later for every character
width = 400

r = width/w_width
dim = (width, int(w_height * r))
resized_wings = cv2.resize(wings, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("Resized Wings!", resized_wings)

r = width/char_width
dim = (width, int(char_height * r))
resized_char = cv2.resize(char, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("Resized Char!", resized_char)

cv2.waitKey(0)


# CH. 5 Drawing - Rectangle buildings in canvas, line telephone wires, and circle stars
win_size = 1000
canvas = np.full((win_size, win_size,3), [40, 5, 5], dtype = "uint8") # creates dark sky canvas for character to "move" in

for i in range(100): # draws 100 stars
    # initializes random position and size for the star
    rand_x = np.random.randint(0, win_size)
    rand_y = np.random.randint(0, win_size)
    rand_r = np.random.randint(0, 4)
    
    star_center = (rand_x, rand_y)
    cv2.circle(canvas, star_center, rand_r, (255,255,255), -1)


for i in range(30): # draws 30 buildings for the landscape
    # randomizes building's width, height, and color
    rand_bwidth = np.random.randint(win_size/15, high = win_size/8)
    rand_bheight = np.random.randint(win_size * 1/3, high = win_size * 3/4)
    rand_bpos = np.random.randint(0, win_size)
    rand_color = np.random.randint(20, 50)

    gray_color = (rand_color, rand_color, rand_color)
    bottom_left = (rand_bpos, win_size)
    top_right = (rand_bpos + rand_bwidth, win_size - rand_bheight)

    if top_right[0] < win_size and bottom_left[0] >= 0: # condition to make sure pixel index is not out of range
        cv2.rectangle(canvas, bottom_left, top_right, gray_color, -1) #draws building!

     # draws a telephone line layered between buildings
    if i % 4 == 0: # use mod so that only draws teleophone line after every 4 buildings
        black = (0,0,0)
        rand_y1 = np.random.randint(win_size*2/5, win_size*9/10)
        rand_y2 = np.random.randint(win_size*2/5, win_size*9/10)
        rand_thickness = np.random.randint(2, 4)

        line = cv2.line(canvas, (0, rand_y1), (win_size, rand_y2), black, rand_thickness)


cv2.imshow("Landscape Background!", canvas)



"""
for x in range(width):
   for y in range(width):
        (wb, wg, wr) = resized_wings[y, x]
        if wb != 0 and wg != 0 and wr != 0: # if the pixel is on
            canvas[500 + y, 300 + x] = resized_wings[y, x] 
        
        (cb, cg, cr) = resized_char[y, x]
        if cb != 0 and cg != 0 and cr != 0: # if the pixel is on
            canvas[500 + y, 300 + x] = resized_char[y, x] # overlays pixel in groot's image on pixel in wing's image 
cv2.imshow("Character with Wings!", canvas)
cv2.waitKey(0)


for i in range(80): 
    canvas = imutils.translate(canvas, np.random.random_integers(-2, 2), np.random.random_integers(2, 10))
    cv2.imshow("Shifted Character", canvas)
    cv2.waitKey(1)


    for x in range(width):
        for y in range(width):
                (wb, wg, wr) = resized_wings[y, x]
                if wb != 0 and wg != 0 and wr != 0: # if the pixel is on
                    canvas[500 + y, 300 + x] = resized_wings[y, x] 
                
                (cb, cg, cr) = resized_char[y, x]
                if cb != 0 and cg != 0 and cr != 0: # if the pixel is on
                    canvas[500 + y, 300 + x] = resized_char[y, x] # overlays pixel in groot's image on pixel in wing's image 
    cv2.imshow("Shifted Character!", canvas)
    cv2.waitKey(1)
"""



# have background move down
# can also switch between closed and open wings


cv2.waitKey(0)
