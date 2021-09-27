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

    # use threshold as mask to only focus on pixels that are on in thresh
    cropped_img = cv2.bitwise_and(img, img, mask = thresh) 

    return cropped_img


def display_and_crop(img_path = str, title = str, thresh = int, use_inv = bool):
    # CH.1 - load, display, save image
    image = cv2.imread(img_path)
    cv2.imshow(f'Original {title}', image)
    cv2.waitKey(0)
    cropped_img = crop_image(image, thresh, use_inv, False)
    cv2.imshow(f'Cropped {title}', cropped_img)
    cv2.waitKey(0)

    return cropped_img


def resize_image(target_w = int, img = np, title = str):
    i_width = img.shape[1]
    i_height = img.shape[0]
    print(f'Original {title} Width: {i_width}, Original {title} Height: {i_height}')

    r = target_w/i_width
    dim = (target_w, int(i_height * r))

    resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow(f'Resized {title}', resized_img)
    print(f'Resized {title} Width: {resized_img.shape[1]}, Resized {title} Height: {resized_img.shape[0]}')
    cv2.waitKey(0)

    return resized_img


def draw_stars(num = int, canvas = np, win_size = int):
    for i in range(num): # draws num stars
        # initializes random position and size for the star
        rand_x = np.random.randint(0, win_size)
        rand_y = np.random.randint(0, win_size)
        rand_r = np.random.randint(0, 4)

        star_center = (rand_x, rand_y)
        cv2.circle(canvas, star_center, rand_r, (255,255,255), -1)
    return


def draw_building(canvas, win_size):
    rand_bwidth = np.random.randint(win_size/15, high = win_size/8)
    rand_bheight = np.random.randint(win_size * 1/3, high = win_size * 3/4)
    rand_bpos = np.random.randint(0, win_size)
    rand_color = np.random.randint(20, 50)

    gray_color = (rand_color, rand_color, rand_color)
    bottom_left = (rand_bpos, win_size)
    top_right = (rand_bpos + rand_bwidth, win_size - rand_bheight)

    if top_right[0] < win_size and bottom_left[0] >= 0: # condition to make sure pixel index is not out of range
        cv2.rectangle(canvas, bottom_left, top_right, gray_color, -1) #draws building!
    return


def draw_telephone_line(canvas, win_size):
    black = (0,0,0)
    rand_y1 = np.random.randint(win_size*2/5, win_size*9/10)
    rand_y2 = np.random.randint(win_size*2/5, win_size*9/10)
    rand_thickness = np.random.randint(2, 4)

    cv2.line(canvas, (0, rand_y1), (win_size, rand_y2), black, rand_thickness)
    return


def draw_city(win_size = int):
    # CH. 5 Drawing - Rectangle buildings in canvas, line telephone wires, and circle stars
    canvas = np.full((win_size, win_size,3), [40, 5, 5], dtype = "uint8") # creates dark sky canvas for character to "move" in
    draw_stars(100, canvas, win_size)

    for i in range(30): # draws 30 buildings for the landscape
        # randomizes building's width, height, and color
        draw_building(canvas, win_size)

        # draws a telephone line layered between buildings
        if i % 4 == 0: # use mod so that only draws teleophone line after every 4 buildings
            draw_telephone_line(canvas, win_size)

    cv2.imshow("Landscape Background!", canvas)
    return canvas


def sobel_destroy(canvas, title = str):
    sobelX = cv2.Sobel(canvas, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(canvas, cv2.CV_64F, 0, 1)
    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    sobelCombined = cv2.bitwise_or(sobelX, sobelY)

    cv2.imshow(f'Destroyed {title}', sobelCombined)
    cv2.waitKey(0)

    (B,G,R) = cv2.split(sobelCombined)
    zeros = np.zeros(canvas.shape[:2], dtype = "uint8")
    cv2.imshow(f'{title} on FIRE!', cv2.merge([zeros, zeros, R]))

    return


def overlay_character(background1 = np, background2 = np, bgtitle1 = str, bgtitle2 = str, character = np):
    width = background1.shape[1]
    height = background1.shape[0]
    for x in range(width):
        for y in range(height):
            (cb, cg, cr) = character[y, x]
            if cb != 0 and cg != 0 and cr != 0: # if the pixel is on
                background1[y, x] = character[y, x] 
                background2[y, x] = character[y, x]       
    cv2.imshow(f'Character with {bgtitle1}', background1)
    cv2.imshow(f'Character with {bgtitle2}', background2)
    cv2.waitKey(0)

    return


def shake_city(canvas, num = int):
    for j in range(num):
        canvas = imutils.translate(canvas, np.random.randint(-10, 11), np.random.randint(-10, 11))
        cv2.imshow("Shaking City!", canvas)
        cv2.waitKey(100)
    return


def char_fly(canvas, char_sz, closed_wings, open_wings):
    for i in range(8): 
        new_canvas = imutils.translate(canvas, np.random.randint(-5, 6), np.random.randint(-5, 6))
        rand_shift = np.random.randint(-100, 101)
        for x in range(char_sz):
            for y in range(char_sz):
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
    f_width = fireball.shape[1]
    f_height = fireball.shape[0]
    for i in range(num): # num fireballs fall down on city
        x_pos = np.random.randint(f_width, win_size - f_width)
        y_pos = np.random.randint(f_height, win_size - f_height)
        
        for x in range(f_width):
            for y in range(f_height):
                (fb, fg, fr) = fireball[y, x]
                if fb != 0 and fg != 0 and fr != 0: # if the pixel is on
                    canvas[y_pos + y, x_pos + x] = fireball[y, x]   

        cv2.imshow("Falling Fireballs!", canvas)

        shake_city(canvas, 7)
        cv2.waitKey(500)
        
    return


def main():
    # CH.1 Parsing arguments
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

    # draws character with closed wings and character with open wings by overlaying character on top of image
    overlay_character(resized_cwings, resized_owings, "Closed Wings", "Open Wings", resized_char)

    # CH. 5 Drawing - Rectangle buildings in canvas, line telephone wires, and circle stars
    win_size = 1000
    canvas = draw_city(win_size)

    new_canvas = char_fly(canvas, width, resized_cwings, resized_owings)

    fireball_path = "images/fireball.jpeg"
    fireball = display_and_crop(fireball_path, "Fireball", 254, True)
    fireball = resize_image(int(win_size/5), fireball, "Fireball")

    falling_fireballs(new_canvas, 10, fireball, win_size)

    sobel_destroy(new_canvas, "City")

    cv2.waitKey(0)




main()