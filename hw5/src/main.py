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
    sob_x = np.zeros(shape=(height, width))
    sob_x_norm = np.zeros(shape=(height, width), dtype=np.ubyte)
    for i in range(height-1):
        for j in range(width-1):
            sob_x[i][j] = np.dot(get_nbhd(img,i,j), Gx)
            sob_x_norm[i][j] = (np.dot(get_nbhd(img,i,j), Gx)+255)*255/510

    return sob_x, sob_x_norm

def sobel_y_gray(img):
    Gy = np.array([.25, .5, .25, 0, 0, 0, -.25, -.5, -.25])
    # Gy = [[.25, .5, .25], [0, 0, 0], [-.25, -.5, -.25]]
    height, width = img.shape[:2]
    sob_y = np.zeros(shape=(height, width))
    sob_y_norm = np.zeros(shape=(height, width), dtype=np.ubyte)
    for i in range(height-1):
        for j in range(width-1):
            sob_y[i][j] = np.dot(get_nbhd(img,i,j), Gy)
            sob_y_norm[i][j] = (np.dot(get_nbhd(img,i,j), Gy)+255)*255/510

    return sob_y, sob_y_norm

def sobel_mag_gray(img):
    height, width = img.shape[:2]
    sob_mag = np.zeros(shape=(height, width))
    sob_mag_norm = np.zeros(shape=(height, width), dtype=np.ubyte)
    sob_x = sobel_x_gray(img)[0]
    sob_y = sobel_y_gray(img)[0]
    rt2 = np.sqrt(2)
    for i in range(height):
        for j in range(width):
            sob_mag[i][j] = np.sqrt(sob_x[i][j]**2 + sob_y[i][j]**2)
            sob_mag_norm[i][j] = np.sqrt(sob_x[i][j]**2 + sob_y[i][j]**2)/rt2
    
    return sob_mag, sob_mag_norm

def sobel_ang_gray(img):
    assert img.shape != 3 # ensure we get grayscale
    height, width = img.shape[:2]
    sob_ang = cv.cvtColor(cv.cvtColor(img, cv.COLOR_GRAY2BGR), cv.COLOR_BGR2HSV)
    sob_x = sobel_x_gray(img)[0]
    sob_y = sobel_y_gray(img)[0]
    h, s, v = cv.split(sob_ang)
    for i in range(height):
        for j in range(width):
            h[i][j] = 180*np.arctan2(sob_y[i][j], sob_x[i][j])/np.pi if (sob_x[i][j] != 0 and sob_y[i][j] != 0) else 0 # H
    s[:] = 255
    v = sobel_mag_gray(img)[1] # normed magnitude values
    sob_ang = cv.cvtColor(cv.merge((h,s,v)), cv.COLOR_HSV2BGR) # return BGR img
    
    return sob_ang

def sobel_x_bgr(img):
    b, g, r = cv.split(img)
    b_sob_x, b_sob_x_norm = sobel_x_gray(b)
    g_sob_x, g_sob_x_norm = sobel_x_gray(g)
    r_sob_x, r_sob_x_norm = sobel_x_gray(r)
    return cv.merge((b_sob_x,g_sob_x,r_sob_x)), cv.merge((b_sob_x_norm,g_sob_x_norm,r_sob_x_norm))

def sobel_y_bgr(img):
    b, g, r = cv.split(img)
    b_sob_y, b_sob_y_norm = sobel_y_gray(b)
    g_sob_y, g_sob_y_norm = sobel_y_gray(g)
    r_sob_y, r_sob_y_norm = sobel_y_gray(r)
    return cv.merge((b_sob_y,g_sob_y,r_sob_y)), cv.merge((b_sob_y_norm,g_sob_y_norm,r_sob_y_norm))

def sobel_mag_bgr(img):
    b, g, r = cv.split(img)
    b_sob_mag, b_sob_mag_norm = sobel_mag_gray(b)
    g_sob_mag, g_sob_mag_norm = sobel_mag_gray(g)
    r_sob_mag, r_sob_mag_norm = sobel_mag_gray(r)
    return cv.merge((b_sob_mag,g_sob_mag,r_sob_mag)), cv.merge((b_sob_mag_norm,g_sob_mag_norm,r_sob_mag_norm))

if __name__ == '__main__':

    # argc check
    if(len(sys.argv) != 3):
        print('Usage: python3 src/main.py input.img output/dir')
        exit()

    img = cv.imread(str(sys.argv[1]))
    out_dir = str(sys.argv[2])
    ext = str(sys.argv[1]).split('.')[-1]

    # optionally uncomment to test grayscale features
    # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # sanity check
    print('shape:', img.shape)
    print('dtpye:', img.dtype)

    # dealing with bgr img
    if(len(img.shape) == 3):
        out_x_bgr = sobel_x_bgr(img)[1]
        out_y_bgr = sobel_y_bgr(img)[1]
        out_mag_bgr = sobel_mag_bgr(img)[1]
        out_ang_bgr = sobel_ang_gray(cv.cvtColor(img, cv.COLOR_BGR2GRAY))

        cv.imwrite(out_dir+'/sobel_x_rgb.'+ext, out_x_bgr)
        cv.imwrite(out_dir+'/sobel_y_bgr.'+ext, out_y_bgr)
        cv.imwrite(out_dir+'/sobel_mag_bgr.'+ext, out_mag_bgr)
        cv.imwrite(out_dir+'/sobel_ang_bgr.'+ext, out_ang_bgr)

        cv.imshow('My Sobel X', out_x_bgr)
        cv.waitKey(0)
        cv.imshow('My Sobel Y', out_y_bgr)
        cv.waitKey(0)
        cv.imshow('My Sobel Magnitude', out_mag_bgr)
        cv.waitKey(0)
        cv.imshow('My Sobel Angel', out_ang_bgr)
        cv.waitKey(0)
    # dealing with grayscale img
    else:
        out_x_gray = sobel_x_gray(img)[1]
        out_y_gray = sobel_y_gray(img)[1]
        out_mag_gray = sobel_mag_gray(img)[1]
        out_ang_gray = sobel_ang_gray(img)

        cv.imwrite(out_dir+'/sobel_x_gray.'+ext, out_x_gray)
        cv.imwrite(out_dir+'/sobel_y_gray.'+ext, out_y_gray)
        cv.imwrite(out_dir+'/sobel_mag_gray.'+ext, out_mag_gray)
        cv.imwrite(out_dir+'/sobel_ang_gray.'+ext, out_ang_gray)

        cv.imshow('My Sobel X', out_x_gray)
        cv.waitKey(0)
        cv.imshow('My Sobel Y', out_y_gray)
        cv.waitKey(0)
        cv.imshow('My Sobel Magnitude', out_mag_gray)
        cv.waitKey(0)
        cv.imshow('My Sobel Angel', out_ang_gray)
        cv.waitKey(0)