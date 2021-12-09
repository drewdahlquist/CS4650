import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import sys
import time
import random

# will vary by user/system
PATH_TO_OPENCV_HAARCASCADES = '/Users/drew/opencv/opencv-master/data/haarcascades/haarcascade_frontalface_alt.xml'

def integral_image(img):
    height, width = img.shape[:2]
    integral = np.zeros(shape=img.shape, dtype=np.int32)

    # initial pixel
    integral[0, 0] = img[0, 0]

    # fill left-most col
    for x in range(1, height):
        integral[x, 0] = integral[x-1, 0] + img[x, 0]

    # fill top-most row
    for y in range(1, width):
        integral[0, y] = integral[0, y-1] + img[0, y]

    # do rest of img
    for x in range(1, height):
        for y in range(1, width):
            integral[x, y] = integral[x, y-1] + \
                integral[x-1, y] - integral[x-1, y-1] + img[x, y]

    # padded for 0's on bottom & right side
    padded = np.zeros(shape=(height+1, width+1), dtype=np.int32)
    padded[0:height, :width] = integral

    return padded


if __name__ == '__main__':

    # argc check
    if(len(sys.argv) != 2):
        print('Usage: python3 src/main.py input.img')
        exit()

    # read img in graysacle & get its extension type
    original_img = cv.imread(str(sys.argv[1]))
    grayscale_img = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
    ext = str(sys.argv[1]).split('.')[-1]

    # sanity check
    print('shape:', original_img.shape)
    print('dtpye:', original_img.dtype)

    # for future reference
    h, w = original_img.shape[:2]

    """begin: Integral Image computations"""

    # compute & save integral image
    integral_img = integral_image(grayscale_img)
    plt.imsave('integral_img.'+ext, integral_img[0:h,0:w])

    # timing
    int_time = 0
    reg_time = 0
    int_sum = 0
    reg_sum = 0
    for i in range(1000):
        
        # pick 2 points 'at random' to form rectangle region
        pt1 = (random.randint(0,50), random.randint(0,50))
        pt2 = (random.randint(h-50,h), random.randint(w-50,w))
        
        # rectangle sum w integral image
        t1 = time.perf_counter()
        sum1 = integral_img[pt2[0]-1, pt2[1]-1] \
            - integral_img[pt2[0]-1, pt1[1] - 1] \
            - integral_img[pt1[0]-1, pt2[1]-1] \
            + integral_img[pt1[0]-1, pt1[1]-1]
        t2 = time.perf_counter()

        # rectangle sum w for loops
        t3 = time.perf_counter()
        sum2 = 0
        for x in range(pt1[0], pt2[0]):
            for y in range(pt1[1], pt2[1]):
                sum2 += grayscale_img[x, y]
        t4 = time.perf_counter()

        int_time += t2 - t1
        reg_time += t4 - t3
        int_sum += sum1
        reg_sum += sum2

    print('Difference between each sum: ', sum1 - sum2)
    print('Integral Image Time', int_time)
    print('Regular Image Time', reg_time)

    """end: Integral Image computations"""

    """begin: Face detection"""

    face_cascade = cv.CascadeClassifier(PATH_TO_OPENCV_HAARCASCADES)

    face = face_cascade.detectMultiScale(grayscale_img)

    for (column, row, width, height) in face:
        cv.rectangle(
            original_img,
            (column, row),
            (column + width, row + height),
            (0, 255, 0),
            2
        )

    cv.imwrite('Face.'+ext, original_img)

    """end: Face detection"""
