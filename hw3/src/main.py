import cv2 as cv
import numpy as np
import sys
import random as rand

def translate(img, tx, ty):
    height, width = img.shape[:2]
    # transformation matrix
    T = np.float32([
        [1, 0, tx],
        [0, 1, ty]
    ])
    return cv.warpAffine(img, T, (height, width))

def crop(img, x_i, x_j, y_i, y_j):
    return img[int(x_i):int(x_j), int(y_i):int(y_j)]

def xflip(img):
    return cv.flip(img, 0)

def yflip(img):
    return cv.flip(img, 1)

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
    height, width = img.shape[:2]

    # 5 transformations for each implemented function
    for i in range(5):
        cv.imwrite(sys.argv[2]+'/translate_'+str(i)+'.jpg', translate(img, rand.choice([-1,1])*(height/rand.randint(2,8)), rand.choice([-1,1])*(width/rand.randint(2,8))))
        cv.imwrite(sys.argv[2]+'/crop_'+str(i)+'.jpg', crop(img, rand.randint(1,2)*height/8, rand.randint(6,7)*height/8, rand.randint(1,2)*width/8, rand.randint(6,7)*width/8))
        cv.imwrite(sys.argv[2]+'/vflip_'+str(i)+'.jpg', xflip(img))
        cv.imwrite(sys.argv[2]+'/hflip_'+str(i)+'.jpg', yflip(img))
