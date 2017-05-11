from PIL import Image
from pytesseract import image_to_string
import sys

def main():
    image_name = sys.argv[1]

    im = Image.open(image_name)
    im1, im2, im3, im4, im5 = split_image(im)

    # Convert each split character to a string
    char1 = image_to_string(im1, config='-psm 10')
    char2 = image_to_string(im2, config='-psm 10')
    char3 = image_to_string(im3, config='-psm 10')
    char4 = image_to_string(im4, config='-psm 10')
    char5 = image_to_string(im5, config='-psm 10')

    # Print the concatenated characters
    res = char1 + char2 + char3 + char4 + char5
    print res

# Split image into 5 chunks
def split_image(im):
    im1, rest = split_char(im)
    im2, rest = split_char(rest)
    im3, rest = split_char(rest)
    im4, im5 = split_char(rest)

    return im1, im2, im3, im4, im5

# Split off the next character by finding the next chunk of continuous white lines
def split_char(im):
    pixels = im.getdata()
    width, height = im.size

    crop_width = 0
    # Look past the first white vertical lines
    while not has_colored_pixels(im, crop_width):
        crop_width += 1

    # Look past the non-white vertical lines
    while has_colored_pixels(im, crop_width):
        crop_width += 1
    # Crop at the next white vertical line
    left = im.crop((0, 0, crop_width, height))
    right = im.crop((crop_width, 0, width, height))

    return left, right

# Does the given width value have any non-white pixels?
def has_colored_pixels(im, cur_width):
    pixels = im.getdata()
    width, height = im.size
 
    for cur_height in range(height):
        r,g,b = pixels[cur_height * width + cur_width]
        # If they're not super close to white
        if r + g + b < 600:
            return True
    return False

if __name__ == "__main__":
    main()
