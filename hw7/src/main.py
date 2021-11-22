import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys

def stage_A(img, x, y, sz, sz_max):
    if(sz%2 != 1):
        print('stage_A only accepts odd filter sizes. Exiting...')
        exit()

    h, w = img.shape[:2]
    nbhd = img[min(0,x-sz//2):max(h,x+sz//2), min(0,y-sz//2):max(w,y+sz//2)].flatten()
    zmed = nbhd[len(nbhd)//2]
    zmin, zmax = int(min(nbhd)), int(max(nbhd))
    a1 = int(zmed)-zmin
    a2 = int(zmed)-zmax
    if(a1 > 0 and a2 < 0):
        # 'Stage B'
        if(img[x,y]-zmin > 0 and img[x,y]-zmax < 0):
            return img[x,y]
        else:
            return zmed
    else:
        if(sz+2 <= sz_max):
            return stage_A(img, x, y, sz+2, 21)
        else:
            return zmed


def adaptive_median(img):
    h, w = img.shape[:2]
    filtered = np.zeros(shape=(h,w), dtype=np.ubyte)

    for x in range(h):
        for y in range(w):
            filtered[x,y] = stage_A(img, x, y, 3, 21)

    return filtered


if __name__ == '__main__':

    # argc check
    if(len(sys.argv) != 2):
        print('Usage: python3 src/main.py input.img')
        exit()

    img = cv.imread(str(sys.argv[1]), cv.IMREAD_GRAYSCALE)
    ext = str(sys.argv[1]).split('.')[-1]
    
    # sanity check
    print('shape:', img.shape)
    print('dtpye:', img.dtype)

    cv.imshow('AMF', adaptive_median(img))
    cv.waitKey(0)
