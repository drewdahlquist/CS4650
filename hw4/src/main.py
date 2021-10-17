import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys

# calc historgram for single-channel grayscale img
def gray_hist(img):
    hist = np.zeros(256)
    for row in img:
        for pix in row:
            hist[pix] += 1
    
    return hist

# calc binned historgram for single-channel grayscale img
def gray_hist_bin(img, bins):
    hist = np.zeros(bins)
    for row in img:
        for pix in row:
            hist[int(pix*bins/256)] += 1
    
    return hist

# calc log_10-transformed output for single-channel grayscale img
def gray_log_transform(img):
    pass

def gray_hist_eq(img):
    
    hist = gray_hist(img)

    # calc cdf
    cdf = np.zeros(256)
    cdf[0] = hist[0]
    for i in range(1,256):
        cdf[i] = hist[i] + cdf[i-1]
    cdf /= img.shape[0]*img.shape[1]

    # new histograms
    hist_eq = np.around(255*cdf)
    hist_out = np.zeros(hist.shape)
    for i in range(256):
        hist_out[int(hist_eq[i])] += hist[i]
    
    # new img
    img_out = img.copy()
    height, width = img.shape[:2]
    for x in range(height):
        for y in range(width):
            img_out[x][y] = hist_eq[img[x][y]]

    return hist_out, img_out

# calc historgram for 3-channel bgr img
def bgr_hist(img):
    hist = np.zeros((3,256))
    for row in img:
        for pix in row:
            hist[0][pix[0]] += 1
            hist[1][pix[1]] += 1
            hist[2][pix[2]] += 1
    
    return hist

# calc binned historgram for 3-channel bgr img
def bgr_hist_bin(img, bins):
    hist = np.zeros((3,bins))
    for row in img:
        for pix in row:
            hist[0][int(pix[0]*bins/256)] += 1
            hist[1][int(pix[1]*bins/256)] += 1
            hist[2][int(pix[2]*bins/256)] += 1
    
    return hist

# calc log_10-transformed output for 3-channel bgr img
def bgr_log_transform(img):
    height, width, channels = img.shape[:3]
    new = np.zeros(img.shape[:3])
    for x in range(height):
        for y in range(width):
            for c in range(channels):
                # effectively makes log(0) = 0
                # if(img[x][y][c] == 0):
                #     img[x][y][c] = 1
                # new[x][y][c] = np.log10(img[x][y][c])*255/np.log10(255)
                new[x][y][c] = img[x][y][c]
            
    cv.imshow('bgr_log', new)
    cv.waitKey(0)

def bgr_hist_eq(img):

    hist = bgr_hist(img)

    # calc cdf
    cdf = np.zeros((3,256))
    cdf[0][0] = hist[0][0]
    cdf[1][0] = hist[1][0]
    cdf[2][0] = hist[2][0]
    for i in range(3):
        for j in range(1,256):
            cdf[i][j] = hist[i][j] + cdf[i][j-1]
    cdf /= img.shape[0]*img.shape[1]
    
    # new histograms
    hist_eq = np.around(255*cdf)
    hist_out = np.zeros(hist.shape)
    for i in range(3):
        for j in range(256):
            hist_out[i][int(hist_eq[i][j])] += hist[i][j]
    
    # new img
    img_out = img.copy()
    height, width, channels = img.shape[:3]
    for x in range(height):
        for y in range(width):
            for c in range(channels):
                img_out[x][y][c] = hist_eq[c][img[x][y][c]]

    return hist_out, img_out


if __name__ == '__main__':

    if(len(sys.argv) != 4):
        print('Usage: python3 src/main.py input.jpg bins output_dir')
        exit()

    img = cv.imread(str(sys.argv[1]))
    bins = int(sys.argv[2])
    print(img.shape) # sanity check for bgr vs grayscale imgs
    
    # dealing with bgr img
    if(len(img.shape) == 3):

        hist = bgr_hist(img) # Part A a
        hist_bin = bgr_hist_bin(img, bins) # Part A b
        # bgr_log_transform(img) # Part A c
        hist_eq, img_eq = bgr_hist_eq(img) # Part B

        # normal hist
        plt.title('BGR Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist[0], 'b')
        plt.plot(hist[1], 'g')
        plt.plot(hist[2], 'r')
        plt.show()

        # binned hist
        plt.title('BGR Binned Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_bin[0], 'b')
        plt.plot(hist_bin[1], 'g')
        plt.plot(hist_bin[2], 'r')
        plt.show()

        # log transform

        # equalized hist
        plt.title('BGR Histogram Equalized')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_eq[0], 'b')
        plt.plot(hist_eq[1], 'g')
        plt.plot(hist_eq[2], 'r')
        plt.show()
        # equalized img
        cv.imshow('BGR Image Equalized', img_eq)
        cv.waitKey(0)


    # grayscale img
    else:

        hist = gray_hist(img) # Part A a
        hist_bin = gray_hist_bin(img, bins) # Part A b
        gray_log_transform(img) # Part A c
        gray_hist_eq(img) # Part B

        # normal hist
        plt.title('Grayscale Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist, 'k')
        plt.show()

        # binned hist
        plt.title('Grayscale Binned Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist, 'k')
        plt.show()

        # log transform

        # equalized hist
        # equalized img