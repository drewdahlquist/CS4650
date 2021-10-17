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
    height, width = img.shape[:2]
    img_out = img.copy()
    for x in range(height):
        for y in range(width):
                # effectively makes log(0) = 0
                if(img[x][y] == 0):
                    img[x][y] = 1
                img_out[x][y] = np.log10(img[x][y])*100
            
    return gray_hist(img_out), img_out

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
    img_out = img.copy()
    for x in range(height):
        for y in range(width):
            for c in range(channels):
                # effectively makes log(0) = 0
                if(img[x][y][c] == 0):
                    img[x][y][c] = 1
                img_out[x][y][c] = np.log10(img[x][y][c])*100
            
    return bgr_hist(img_out), img_out

def bgr_hist_eq(img):

    # convert to proper color space
    img_ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)

    # use our grayscale hist eq on the y channel then merge & convert back to bgr
    (y, cr, cb) = cv.split(img_ycrcb)
    y_hist_eq, y_eq = gray_hist_eq(y)
    img_ycrcb_out = cv.merge((y_eq, cr, cb))
    img_out = cv.cvtColor(img_ycrcb_out, cv.COLOR_YCR_CB2BGR)

    # hist of bgr eq img
    hist_out = bgr_hist(img_out)

    return hist_out, img_out

if __name__ == '__main__':

    if(len(sys.argv) != 4):
        print('Usage: python3 src/main.py input.img bins output_dir')
        exit()

    img = cv.imread(str(sys.argv[1]))
    bins = int(sys.argv[2])
    out_dir = str(sys.argv[3])
    # optionally uncomment to test grayscale features
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    print(img.shape) # sanity check for bgr vs grayscale imgs
    
    # dealing with bgr img
    if(len(img.shape) == 3):

        hist = bgr_hist(img) # Part A a
        hist_bin = bgr_hist_bin(img, bins) # Part A b
        hist_log, img_log = bgr_log_transform(img) # Part A c
        hist_eq, img_eq = bgr_hist_eq(img) # Part B

        # normal hist
        plt.title('BGR Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist[0], 'b')
        plt.plot(hist[1], 'g')
        plt.plot(hist[2], 'r')
        plt.savefig(out_dir+'/bgr_hist.png')
        plt.show()

        # binned hist
        plt.title('BGR Binned Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_bin[0], 'b')
        plt.plot(hist_bin[1], 'g')
        plt.plot(hist_bin[2], 'r')
        plt.savefig(out_dir+'/bgr_hist_bin.png')
        plt.show()

        # log hist
        plt.title('BGR Log Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_log[0], 'b')
        plt.plot(hist_log[1], 'g')
        plt.plot(hist_log[2], 'r')
        plt.savefig(out_dir+'/bgr_hist_log.png')
        plt.show()
        # log img
        cv.imwrite(out_dir+'/bgr_img_log.png', img_log)
        cv.imshow('BGR Log', img_log)
        cv.waitKey(0)

        # equalized hist
        plt.title('BGR Histogram Equalized')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_eq[0], 'b')
        plt.plot(hist_eq[1], 'g')
        plt.plot(hist_eq[2], 'r')
        plt.savefig(out_dir+'/bgr_hist_eq.png')
        plt.show()
        # equalized img
        cv.imwrite(out_dir+'/bgr_img_eq.png', img_eq)
        cv.imshow('BGR Image Equalized', img_eq)
        cv.waitKey(0)

        # compare to opencv's hist eq
        ycrcb_img = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)
        ycrcb_img[:, :, 0] = cv.equalizeHist(ycrcb_img[:, :, 0])
        comp = cv.cvtColor(ycrcb_img, cv.COLOR_YCrCb2BGR)
        cv.imwrite(out_dir+'/cv_bgr_img_eq.png', comp)
        plt.title('OpenCV BGR Histogram Equalized')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv.calcHist([img],[i],None,[256],[0,256])
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.savefig(out_dir+'/cv_bgr_hist_eq.png')

    # grayscale img
    else:

        hist = gray_hist(img) # Part A a
        hist_bin = gray_hist_bin(img, bins) # Part A b
        hist_log, img_log = gray_log_transform(img) # Part A c
        hist_eq, img_eq = gray_hist_eq(img) # Part B

        # normal hist
        plt.title('Gray Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist, 'k')
        plt.savefig(out_dir+'/gray_hist.png')
        plt.show()

        # binned hist
        plt.title('Gray Binned Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_bin, 'k')
        plt.savefig(out_dir+'/gray_hist_bin.png')
        plt.show()

        # log hist
        plt.title('Gray Log Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_log, 'k')
        plt.savefig(out_dir+'/gray_hist_log.png')
        plt.show()
        # log img
        cv.imwrite(out_dir+'/gray_img_log.png', img_log)
        cv.imshow('Gray Log', img_log)
        cv.waitKey(0)

        # equalized hist
        plt.title('Gray Histogram Equalized')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(hist_eq, 'k')
        plt.savefig(out_dir+'/gray_hist_eq.png')
        plt.show()
        # equalized img
        cv.imwrite(out_dir+'/gray_img_eq.png', img_eq)
        cv.imshow('Gray Image Equalized', img_eq)
        cv.waitKey(0)

        # compare to opencv's hist eq
        comp = cv.equalizeHist(img)
        cv.imwrite(out_dir+'/cv_gray_img_eq.png', comp)
        plt.title('OpenCV Gray Histogram Equalized')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.plot(cv.calcHist([comp], [0], None, [256], [0, 256]), 'k')
        plt.savefig(out_dir+'/cv_gray_hist_eq.png')