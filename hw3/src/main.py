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
    height, width = img.shape[:2]
    center = tuple(np.array(img.shape[1::-1])/2)
    R = cv.getRotationMatrix2D(center, deg, 1)
    return cv.warpAffine(img, R, (height, width))

def erase(img):
    height, width = img.shape[:2]
    # box 1
    p1_1 = (rand.randint(0,height),rand.randint(0,width))
    p2_1 = (rand.randint(0,height),rand.randint(0,width))
    # box 2
    p1_2 = (rand.randint(0,int(height/2)),rand.randint(0,int(width/2)))
    p2_2 = (rand.randint(0,int(height/2)),rand.randint(0,int(width/2)))
    # box 3
    p1_3 = (rand.randint(int(height/2),height),rand.randint(int(width/2),width))
    p2_3 = (rand.randint(int(height/2),height),rand.randint(int(width/2),width))
    erased1 = cv.rectangle(img, p1_1, p2_1, (0,0,0), -1)
    erased2 = cv.rectangle(erased1, p1_2, p2_2, (0,0,0), -1)
    erased3 = cv.rectangle(erased2, p1_3, p2_3, (0,0,0), -1)
    return erased3

def intensity(img, alpha, beta):
    return cv.convertScaleAbs(img, alpha=alpha, beta=beta)

def blur(img, filter_size):
    return cv.blur(img, (filter_size,filter_size))


if __name__ == '__main__':

    if(len(sys.argv) != 3):
        print('Usage: python3 main.py input.jpg output_dir')

    img = cv.imread(str(sys.argv[1]))
    height, width = img.shape[:2]

    # 5 transformations for each implemented function
    for i in range(5):
        cv.imwrite(sys.argv[2]+'/translate_'+str(i)+'.jpg', translate(img, rand.choice([-1,1])*(height/rand.randint(2,8)), rand.choice([-1,1])*(width/rand.randint(2,8))))
        cv.imwrite(sys.argv[2]+'/crop_'+str(i)+'.jpg', crop(img, rand.randint(1,2)*height/8, rand.randint(6,7)*height/8, rand.randint(1,2)*width/8, rand.randint(6,7)*width/8))
        cv.imwrite(sys.argv[2]+'/rotate_'+str(i)+'.jpg', rotate(img, rand.randint(-180, 180)))
        # cv.imwrite(sys.argv[2]+'/erase_'+str(i)+'.jpg', erase(img))
        cv.imwrite(sys.argv[2]+'/intensity_'+str(i)+'.jpg', intensity(img, rand.random()*2, rand.randint(-100,100)))
    
    # other transformations that don't fit above
    cv.imwrite(sys.argv[2]+'/xflip.jpg', xflip(img))
    cv.imwrite(sys.argv[2]+'/yflip.jpg', yflip(img))
    cv.imwrite(sys.argv[2]+'/blur3.jpg', blur(img, 3))
    cv.imwrite(sys.argv[2]+'/blur5.jpg', blur(img, 5))
    cv.imwrite(sys.argv[2]+'/blur7.jpg', blur(img, 7))