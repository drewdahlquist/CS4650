import cv2 as cv
import sys

def translate(img, tx, ty):
    pass

def crop(img):
    pass

def verticalflip(img):
    pass

def horizontalflip(img):
    pass

def rotate(img, deg):
    pass

def erase(img):
    pass

def intensity(img):
    pass

def blur(img, filter_size):
    pass


if __name__ == '__main__':
    
    if(len(sys.argv) != 2):
        print('Usage: python3 main.py input.png')

    img = cv.imread(str(sys.argv[1]))
