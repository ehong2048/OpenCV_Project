import numpy as np
import argparse
import cv2
import imutils


def get_char(char = str):
    """
    Purpose: Uses passed in character string and returns information relevant to image for thresholding later
    Parameters: string of character name
    Return: string to path of char's image, int threshold value, and Bool for whether to use inverse
    """
    if char == "groot":
        char_path = "images/groot.png"
        thresh_val = 250
        use_inv = True
    elif char == "hulk":
        char_path = "images/hulk.png"
        thresh_val = 240
        use_inv = True
    elif char == "perry":
        char_path = "images/perry.png"
        thresh_val = 40
        use_inv = False
    elif char == "joseph":
        char_path = "images/joseph.jpeg"
        thresh_val = 254
        use_inv = True
    else:
        print("Error: No character with that name. Use --help to see options.")
        quit()
    return char_path, thresh_val, use_inv


def crop_image(img, thresh_val = 150, use_inv = True, use_adaptive = False):
    # CH.8 Smoothing & Blurring (GuassianBlur)
    # CH.9 Simple thresholding and adaptive thresholding
    """
    Purpose: Takes passed in image and then returns the cropped image without the background
    using simple (or adaptive) thresholding and mask for bitwise_and
    Parameters: original image (np), int threshold value, Bool for whether to use inverse threshold, Bool for whether to use adaptive thresholding
    Return: np of cropped image
    """
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

    # use threshold as mask to only focus on pixels that we want, and turns off background pixels
    cropped_img = cv2.bitwise_and(img, img, mask = thresh) 

    return cropped_img


def display_and_crop(img_path = str, title = str, thresh = int, use_inv = bool):
    # CH.3 - load, display, save image
    """
    Purpose: Loads image based on passed in path and displays the original and cropped image
    Parameters: str img_path, string for title of image, int thresh value and Bool for whether to use inverse when cropping
    Return: np of cropped image
    """
    image = cv2.imread(img_path)
    cv2.imshow(f'Original {title}', image)
    cv2.waitKey(0)
    cropped_img = crop_image(image, thresh, use_inv, False)
    cv2.imshow(f'Cropped {title}', cropped_img)
    cv2.waitKey(0)

    return cropped_img


def resize_image(target_w = int, img = np, title = str):
    # CH.6 Image Transformations (Resizing)
    """
    Purpose: Resizes passed in image based on target width, and then displays it
    Parameters: int target width, image to resize (np), str title
    Return: np of resized image
    """
    i_width = img.shape[1]
    i_height = img.shape[0]
    print(f'Original {title} Width: {i_width}, Original {title} Height: {i_height}')

    r = target_w/i_width # ratio of target width to original image's width to scale the height proportionally
    dim = (target_w, int(i_height * r))

    resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow(f'Resized {title}', resized_img)
    print(f'Resized {title} Width: {resized_img.shape[1]}, Resized {title} Height: {resized_img.shape[0]}')
    cv2.waitKey(0)

    return resized_img


def draw_stars(num = int, canvas = np, win_size = int):
    # CH.5 Drawing (Circles)
    """
    Purpose: Draws num stars in passed in canvas at random positions and with random sizes
    Parameters: int number of stars to draw, canvas (np) to draw in, int window size
    """
    for i in range(num): # draws num stars
        # initializes random position and radius for the star
        rand_x = np.random.randint(0, win_size)
        rand_y = np.random.randint(0, win_size)
        rand_r = np.random.randint(0, 4)

        star_center = (rand_x, rand_y)
        cv2.circle(canvas, star_center, rand_r, (255,255,255), -1) # stars are white and filled in
    return


def draw_building(canvas, win_size):
    # CH.5 Drawing (Rectangle)
    """
    Purpose: Draws rectangle building in canvas at random position, with random width and height, and random gray color
    Parameters: canvas (np) to draw in, int window size
    """
    # initializes random width, height, lower x position, and gray color value
    rand_bwidth = np.random.randint(win_size/15, high = win_size/8)
    rand_bheight = np.random.randint(win_size * 1/3, high = win_size * 3/4)
    rand_lxpos = np.random.randint(0, win_size) # lower x position
    rand_color = np.random.randint(20, 50)

    gray_color = (rand_color, rand_color, rand_color)
    bottom_left = (rand_lxpos, win_size)
    top_right = (rand_lxpos + rand_bwidth, win_size - rand_bheight)

    if top_right[0] < win_size and bottom_left[0] >= 0: # condition to make sure pixel index is not out of range
        cv2.rectangle(canvas, bottom_left, top_right, gray_color, -1) #draws building!
    return


def draw_telephone_line(canvas, win_size):
    # CH.5 Drawing (line)
    """
    Purpose: Draws line for telephone wire in canvas at random position, with random thickness
    Parameters: canvas (np) to draw in, int window size
    """
    # initializes color, random y positions, and random thickness
    black = (0,0,0)
    rand_y1 = np.random.randint(win_size*2/5, win_size*9/10)
    rand_y2 = np.random.randint(win_size*2/5, win_size*9/10)
    rand_thickness = np.random.randint(2, 4)

    cv2.line(canvas, (0, rand_y1), (win_size, rand_y2), black, rand_thickness)
    return


def draw_city(win_size = int):
    # CH. 5 Drawing - Rectangle buildings, line telephone wires, and circle stars
    """
    Purpose: Draws city with rectangle buildings, line telephone wires, and circle stars, all with random positions and sizes
    Parameters: int window size
    Return: canvas (np) with created city
    """
    canvas = np.full((win_size, win_size, 3), [40, 5, 5], dtype = "uint8") # creates dark blue canvas as the "sky"
    
    draw_stars(100, canvas, win_size) # draws 100 stars in the sky randomly

    for i in range(30): # draws 30 buildings for the landscape
        draw_building(canvas, win_size)

        # draws a telephone line layered between buildings to make city have more depth
        if i % 4 == 0: # use mod so that only draws teleophone line after every 4 buildings
            draw_telephone_line(canvas, win_size)

    cv2.imshow("Landscape Background!", canvas)

    return canvas


def sobel_destroy(canvas, title = str):
    # CH.10 Gradients & Edge Detection (Sobel)
    """
    Purpose: "Destroys" city by using Sobel and splitting into red color channel so that city turns into red edges (and is thus on "fire")
    Parameters: np canvas, str for title of image
    """
    sobelX = cv2.Sobel(canvas, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(canvas, cv2.CV_64F, 0, 1)
    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    sobelCombined = cv2.bitwise_or(sobelX, sobelY) # combines gradient images in x and y direction

    cv2.imshow(f'Destroyed {title}', sobelCombined) # city made up of horizontal and vertical edges
    cv2.waitKey(0)

    (B,G,R) = cv2.split(sobelCombined) # splits edge city into color channels
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    cv2.imshow(f'{title} on FIRE!', cv2.merge([zeros, zeros, R])) # only uses red color channel so that city is red

    return


def overlay_character(background1 = np, background2 = np, bgtitle1 = str, bgtitle2 = str, character = np):
    # CH.4 Image Basics (Accessing and Manipulating Pixels)
    """
    Purpose: overlays character on the two backgrounds and displays the resulting image
    Parameters: np for 1st, 2nd background to overlay character on, str for 1st, 2nd bg title, np for character to overlay on bkgrds
    """
    width = background1.shape[1]
    height = background1.shape[0]

    # for every pixel
    for x in range(width):
        for y in range(height):
            (cb, cg, cr) = character[y, x] # gets the b, g, r values of pixel
            if cb != 0 and cg != 0 and cr != 0: # if the pixel is on
                background1[y, x] = character[y, x] # changes pixel in background to the value of the corresponding character pixel
                background2[y, x] = character[y, x]       
    cv2.imshow(f'Character with {bgtitle1}', background1)
    cv2.imshow(f'Character with {bgtitle2}', background2)
    cv2.waitKey(0)

    return


def shake_city(canvas, num = int):
    # CH.6 Image Processing (Translation)
    """
    Purpose: "Shakes" the canvas num times using random valued translations
    Parameters: np for canvas to shake, int num for how many times to shake it
    """
    for j in range(num):
        # makes shaking effect more random like an earthquake
        canvas = imutils.translate(canvas, np.random.randint(-10, 11), np.random.randint(-10, 11))
        cv2.imshow("Shaking City!", canvas)
        cv2.waitKey(100)
    return


def char_fly(canvas, char_sz, closed_wings, open_wings):
    # CH.4 Image Basics (Accessing and Manipulating Pixels)
    """
    Purpose: makes character "fly" by being overlayed in canvas in multiple places and opening and closing wings
    Parameters: np for canvas, int for size of character, np for closed_wings and open_wings
    """
    for i in range(8):
        new_canvas = imutils.translate(canvas, np.random.randint(-5, 6), np.random.randint(-5, 6)) # moves background for better flying effect
        rand_shift = np.random.randint(-100, 101) # initializes random shift for flying character
        # for every pixel in character image
        for x in range(char_sz):
            for y in range(char_sz):
                # use mod 2 so that character switches between opening and closing wings
                if i % 2 == 0:
                    (wb, wg, wr) = closed_wings[y, x]
                    if wb != 0 and wg != 0 and wr != 0: # if the pixel is on
                        new_canvas[600 + y - 60*i, 300 + x + rand_shift] = closed_wings[y, x] 
                else:
                    (wb, wg, wr) = open_wings[y, x]
                    if wb != 0 and wg != 0 and wr != 0: # if the pixel is on
                        new_canvas[600 + y - 60*i, 300 + x + rand_shift] = open_wings[y, x]

        cv2.imshow("Flying Character!", new_canvas)
        cv2.waitKey(1)
        
    cv2.waitKey(0)

    return new_canvas


def falling_fireballs(canvas, num = int, fireball = np, win_size = int):
    # CH.4 Image Basics (Accessing and Manipulating Pixels)
    """
    Purpose: num fireballs fall on the city and shake it
    Parameters: np for canvas, int num for how many fireballs, np for fireball, int win_size
    """
    f_width = fireball.shape[1]
    f_height = fireball.shape[0]

    for i in range(num): # num fireballs fall down on city
        # initializes random position for fireball
        x_pos = np.random.randint(f_width, win_size - f_width)
        y_pos = np.random.randint(f_height, win_size - f_height)
        
        # for every pixel of the fireball
        for x in range(f_width):
            for y in range(f_height):
                (fb, fg, fr) = fireball[y, x] # gets b, g, r value of fireball
                if fb != 0 and fg != 0 and fr != 0: # if the pixel is on
                    canvas[y_pos + y, x_pos + x] = fireball[y, x] 

        cv2.imshow("Falling Fireballs!", canvas)

        shake_city(canvas, 7) # shakes city 7 times for each fireball
        cv2.waitKey(500)
        
    return


def main():
    # CH.3 Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--character", required = True, help = "string with name of character: groot, hulk, perry, or joseph")
    args = vars(parser.parse_args())
    char = args["character"]

    char_path, c_thresh, use_inv = get_char(char)
    char = display_and_crop(char_path, "Character", c_thresh, use_inv)

    cw_path = "images/closed_wings.png"
    closed_wings = display_and_crop(cw_path, "Closed Wings", 60, False)

    ow_path = "images/open_wings.png"
    open_wings = display_and_crop(ow_path, "Open Wings", 120, False)

    # CH. 6 Image Transformations - Resizes wings and character to 400 by 400
    # This is so that overlaying char over wings is easier and fits better, and also fits in canvas later for every character
    width = 400 
    resized_char = resize_image(width, char, "Character")
    resized_cwings = resize_image(width, closed_wings, "Closed Wings")
    resized_owings = resize_image(width, open_wings, "Open Wings")

    # draws character with closed wings and character with open wings by overlaying character on top of images of wings
    overlay_character(resized_cwings, resized_owings, "Closed Wings", "Open Wings", resized_char)

    # CH. 5 Drawing - Rectangle buildings in canvas, line telephone wires, and circle stars
    win_size = 1000
    canvas = draw_city(win_size)

    new_canvas = char_fly(canvas, width, resized_cwings, resized_owings) # character flies around in city

    fireball_path = "images/fireball.jpeg"
    fireball = display_and_crop(fireball_path, "Fireball", 254, True)
    fireball = resize_image(int(win_size/5), fireball, "Fireball")

    falling_fireballs(new_canvas, 10, fireball, win_size) # 10 fireballs fall on the city and shake it

    sobel_destroy(new_canvas, "City") # city is "destroyed" by the fireballs

    cv2.waitKey(0)


main()