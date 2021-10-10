import cv2 as cv
import numpy as np
import sys
import random as rand

def translate(img, tx, ty):
    height, width = img.shape[:2]
    T = np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])
    new = cv.warpAffine(img, T, (height, width))
    return new

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

    if(len(sys.argv) != 3):
        print('Usage: python3 main.py input.jpg output_dir')

    img = cv.imread(str(sys.argv[1]))

    # 5 transformations for each implemented function
    for i in range(5):
        cv.imwrite(sys.argv[2]+'/translate_'+str(i)+'.jpg', translate(img, rand.choice([-1,1])*(img.shape[0]/rand.randint(2,8)), rand.choice([-1,1])*(img.shape[1]/rand.randint(2,8))))
