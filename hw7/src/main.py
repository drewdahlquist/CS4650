import numpy as np
import cv2 as cv
import sys
import time
from multiprocessing import Process
from numba import njit, prange

@njit
def stage_A(img, x, y, sz=3, sz_max=21):
    pad = sz//2
    nbhd = img[x-pad:x+pad+1,y-pad:y+pad+1].flatten()
    zmed = int(np.median(nbhd))
    zmin = int(np.min(nbhd))
    zmax = int(np.max(nbhd))

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

@njit(parallel=True)
def adaptive_median(img,sz=3,sz_max=21):
    h, w = img.shape[:2]
    pad = sz_max//2

    # perform padding
    padded = np.zeros(shape=(h+2*pad,w+2*pad))
    padded[pad:-pad,pad:-pad] = img

    filtered = np.zeros(shape=padded.shape, dtype=np.ubyte)

    for x in prange(pad,h+pad+1):
        for y in range(pad,w+pad+1):
            filtered[x,y] = stage_A(padded, x, y, sz, sz_max)

    # only return non-padded slice of img
    return filtered[pad:-pad, pad:-pad]


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

    times = dict()

    # my median filter
    t1 = time.perf_counter()
    median = adaptive_median(img)
    t2 = time.perf_counter()
    times['amf'] = t2-t1
    cv.imwrite('median.'+ext, median)

    # time windows sizes 3x3 thru 21x21
    for sz in range(3, 22, 2):
        t1 = time.perf_counter()
        cv.medianBlur(img, sz)
        t2 = time.perf_counter()
        times[sz] = t2-t1

    print(times)