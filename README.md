# OpenCV_Project
Author: Emma Hong
9/2021 Open CV Project to demonstrate understanding of OpenCV textbook

## Description
Creates semi-animation type thing of character with wings flying around city and city being destroyed by FIREBALLS
1. Displays cropped and resized images of character, open wings, closed wings
2. Overlays character on top of wings' images so that the character has wings
3. Creates a background of a city with rectangle buildings, circle stars, and line telephone wires
4. Overlays winged character in city multiple times so that it "flies"
5. Displays cropped and resized fireball
6. Overlays fireball on city so that they "fall" on the city
    Also translates background to give the impression of shaking
7. Uses Sobel and splits into red color channel to "destroy" the city


## Chapter Roadmap
3. Loading, Displaying, and Saving -- display_and_crop and parsing arguments in main
4. Image Basics (Accessing and Manipulating Pixels) -- overlay_character, falling_fireballs, char_fly
5. Drawing (Lines, Rectangles, Circles) -- draw_stars, draw_building, draw_telephone_line, draw_city
6. Image Processing (Transformations, Bitwise, Masking, Splitting Channels) -- shake_city, resize_image
7. NONE - Histograms
8. Smoothing & Blurring (Gaussian) -- crop_image
9. Thresholding (Simple, Adaptive) -- crop_image
10. Gradients & Edge Detection (Sobel) -- sobel_destroy
11. NONE - Countours


## Usage
    python city_animation.py --charactor $character_name$

character_name are any of the following strings: "groot", "hulk", "joseph", or "perry"

