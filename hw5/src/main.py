import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys

def get_nbhd(img, x, y):
    arr = list()
    height, width = img.shape[:2]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if(x+i < 0 or x+i >= height or y+j < 0 or y+j >= width):
                arr.append(0)
            else:
                arr.append(img[x+i][y+j])
    return arr

def sobel_x_gray(img):
    Gx = [.25, 0, -.25, .5, 0, -.5, .25, 0, -.25]
    height, width = img.shape[:2]
    out_x = np.zeros(shape=(height, width), dtype=np.ubyte)
    for i in range(height-1):
        for j in range(width-1):
            out_x[i][j] = np.dot(get_nbhd(img,i,j), Gx)

    cv.imshow('Gx Out', out_x)
    cv.waitKey(0)

def sobel_y_gray(img):
    Gy = [.25, .5, .25, 0, 0, 0, -.25, -.5, -.25]
    height, width = img.shape[:2]
    out_y = np.zeros(shape=(height, width), dtype=np.ubyte)
    for i in range(height-1):
        for j in range(width-1):
            out_y[i][j] = np.dot(get_nbhd(img,i,j), Gy)

    cv.imshow('Gy Out', out_y)
    cv.waitKey(0)



if __name__ == '__main__':

    # argc check
    if(len(sys.argv) != 3):
        print('Usage: python3 src/main.py input.img output/dir')
        exit()

    img = cv.imread(str(sys.argv[1]))
    out_dir = str(sys.argv[2])
    # optionally uncomment to test grayscale features
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    print(img.shape) # sanity check

    # dealing with bgr img
    if(len(img.shape) == 3):
        pass
    # dealing with grayscale img
    else:
        sobel_x_gray(img)
        sobel_y_gray(img)


    # opencv ref
    cv.imshow('OpenCV Sobelx', cv.Sobel(img,cv.CV_64F,1,0,ksize=3))
    cv.waitKey(0)
    cv.imshow('OpenCV Sobely', cv.Sobel(img,cv.CV_64F,0,1,ksize=3))
    cv.waitKey(0)