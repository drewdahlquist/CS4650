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

def erase(img, r1, r2, r3):
    cpy = img.copy()
    return cv.rectangle(cv.rectangle(cv.rectangle(cpy, r1[0], r1[1], (0,0,0), -1), r2[0], r2[1], (0,0,0), -1), r3[0], r3[1], (0,0,0), -1)

def intensity(img, alpha_b, beta_b, alpha_g, beta_g, alpha_r, beta_r):
    height,width=img.shape[:2]
    b,g,r=cv.split(img)
    for x in range(height):
        for y in range(width):
            b_val = b[x,y]*alpha_b+beta_b
            g_val = g[x,y]*alpha_g+beta_g
            r_val = r[x,y]*alpha_r+beta_r
            if(b_val < 0):
                b[x,y] = 0
            elif(b_val > 255):
                b[x,y] = 255
            else:
                b[x,y] = b_val
            if(g_val < 0):
                g[x,y] = 0
            elif(g_val > 255):
                g[x,y] = 255
            else:
                g[x,y] = g_val
            if(r_val < 0):
                r[x,y] = 0
            elif(r_val > 255):
                r[x,y] = 255
            else:
                r[x,y] = r_val
    return cv.merge((b,g,r))

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
        cv.imwrite(sys.argv[2]+'/xflip_'+str(i)+'.jpg', xflip(img))
        cv.imwrite(sys.argv[2]+'/yflip_'+str(i)+'.jpg', yflip(img))
        cv.imwrite(sys.argv[2]+'/rotate_'+str(i)+'.jpg', rotate(img, rand.randint(-180, 180)))
        # corner points of 3 rectangles for random erasing
        p1 = (rand.randint(0,int(height/2)), rand.randint(0,width))
        p2 = (p1[0]+rand.randint(20,40), p1[1]+rand.randint(20,40))
        p3 = (rand.randint(int(height/2), height),rand.randint(0, int(width/2)))
        p4 = (p3[0]+rand.randint(20,40), p3[1]+rand.randint(20,40))
        p5 = (rand.randint(int(height/2),height), rand.randint(int(width/2),width))
        p6 = (p5[0]+rand.randint(20,40), p5[1]+rand.randint(20,40))
        cv.imwrite(sys.argv[2]+'/erase_'+str(i)+'.jpg', erase(img, (p1, p2), (p3, p4), (p5, p6)))
        cv.imwrite(sys.argv[2]+'/intensity_'+str(i)+'.jpg', intensity(img, rand.random()*2, rand.randint(-64,64), rand.random()*2, rand.randint(-64,64), rand.random()*2, rand.randint(-64,64)))
        cv.imwrite(sys.argv[2]+'/blur3_'+str(i)+'.jpg', blur(img, 3))
        cv.imwrite(sys.argv[2]+'/blur5_'+str(i)+'.jpg', blur(img, 5))
        cv.imwrite(sys.argv[2]+'/blur7_'+str(i)+'.jpg', blur(img, 7))