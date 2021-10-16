import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys

def gray_hist(img):
    hist = np.zeros(256)
    for row in img:
        for pix in row:
            hist[pix] += 1
    
    plt.plot(hist, 'k')
    plt.show()

def bgr_hist(img):
    hist = np.zeros((3,256))
    for row in img:
        for pix in row:
            hist[0][pix[0]] += 1
            hist[1][pix[1]] += 1
            hist[2][pix[2]] += 1
    
    plt.plot(hist[0], 'b')
    plt.plot(hist[1], 'g')
    plt.plot(hist[2], 'r')
    plt.show()


if __name__ == '__main__':

    if(len(sys.argv) != 3):
        print('Usage: python3 src/main.py input.jpg output_dir')
        exit()

    img = cv.imread(str(sys.argv[1]))
    print(img.shape) # sanity check for bgr vs grayscale imgs

    # check if img is bgr or grayscale
    if(len(img.shape) == 3):
        gray = False
    
    # dealing with bgr img
    if(gray == False):
        bgr_hist(img)
    # grayscale img
    else:
        pass