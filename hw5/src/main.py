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
    Gx = np.array([.25, 0, -.25, .5, 0, -.5, .25, 0, -.25])
    # Gx = [[.25, 0, -.25], [.5, 0, -.5], [.25, 0, -.25]]
    height, width = img.shape[:2]
    sob_x = np.zeros(shape=(height, width), dtype=np.ubyte)
    for i in range(height-1):
        for j in range(width-1):
            sob_x[i][j] = (np.dot(get_nbhd(img,i,j), Gx)+255)*255/510

    return sob_x

def sobel_y_gray(img):
    Gy = np.array([.25, .5, .25, 0, 0, 0, -.25, -.5, -.25])
    # Gy = [[.25, .5, .25], [0, 0, 0], [-.25, -.5, -.25]]
    height, width = img.shape[:2]
    sob_y = np.zeros(shape=(height, width), dtype=np.ubyte)
    for i in range(height-1):
        for j in range(width-1):
            sob_y[i][j] = (np.dot(get_nbhd(img,i,j), Gy)+255)*255/510

    return sob_y

def sobel_mag_gray(img):
    height, width = img.shape[:2]
    sob_mag = np.zeros(shape=(height, width), dtype=np.ubyte)
    sob_x, sob_y = sobel_x_gray(img), sobel_y_gray(img)
    for i in range(height):
        for j in range(width):
            sob_mag[i][j] = np.sqrt(sob_x[i][j]**2 + sob_y[i][j]**2)
    
    return sob_mag

def sobel_x_bgr(img):
    b, g, r = cv.split(img)
    b_sob_x = sobel_x_gray(b)
    g_sob_x = sobel_x_gray(g)
    r_sob_x = sobel_x_gray(r)
    return cv.merge((b_sob_x,g_sob_x,r_sob_x))

def sobel_y_bgr(img):
    b, g, r = cv.split(img)
    b_sob_y = sobel_y_gray(b)
    g_sob_y = sobel_y_gray(g)
    r_sob_y = sobel_y_gray(r)
    return cv.merge((b_sob_y,g_sob_y,r_sob_y))

def sobel_mag_bgr(img):
    b, g, r = cv.split(img)
    b_sob_mag = sobel_mag_gray(b)
    g_sob_mag = sobel_mag_gray(g)
    r_sob_mag = sobel_mag_gray(r)
    return cv.merge((b_sob_mag,g_sob_mag,r_sob_mag))

if __name__ == '__main__':

    # argc check
    if(len(sys.argv) != 3):
        print('Usage: python3 src/main.py input.img output/dir')
        exit()

    img = cv.imread(str(sys.argv[1]))
    out_dir = str(sys.argv[2])
    # optionally uncomment to test grayscale features
    # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    print(img.shape) # sanity check
    print(img.dtype)

    # dealing with bgr img
    if(len(img.shape) == 3):
        cv.imshow('My Sobel X', sobel_x_bgr(img))
        cv.waitKey(0)
        cv.imshow('My Sobel Y', sobel_y_bgr(img))
        cv.waitKey(0)
        cv.imshow('My Sobel Mag', sobel_mag_bgr(img))
        cv.waitKey(0)
    # dealing with grayscale img
    else:
        cv.imshow('My Sobel X', sobel_x_gray(img))
        cv.waitKey(0)
        cv.imshow('My Sobel Y', sobel_y_gray(img))
        cv.waitKey(0)
        cv.imshow('My Sobel Mag', sobel_mag_gray(img))
        cv.waitKey(0)
    