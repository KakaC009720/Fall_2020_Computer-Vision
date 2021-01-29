import numpy as np
import cv2 as cv
from pylab import *

img = cv.imread('lena.bmp',0) #以灰階讀入
row = img.shape[0]
col = img.shape[1]
result = np.zeros([row,col],np.uint8)

#part1_a
def upside_down(img):
    for i in range(0, row, 1):
        result[i,:] = img[row-1-i,:]
    return result

p1_a = upside_down(img)
cv.imshow('upside_down', p1_a)

#part1_b
def right_side_left(img):
    for i in range(0, col, 1):
        result[:,i] = img[:,col-1-i]
    return result

p1_b = right_side_left(img)
cv.imshow('right_side_left', p1_b)

#part1_c
def diagonally_flip(img):
    for i in range(0,row,1):
        for j in range(0,col,1):    
            result[row-i-1, j] = img[i, col-j-1]
    return result

p1_c = diagonally_flip(img)
cv.imshow('diagonally_flip', p1_c)

#part2_d
def rotate(image, angle, center = None, scale=1.0):
    (h, w) = img.shape[:2]
    if center is None:
        center = (w/2, h/2)
    
    M = cv.getRotationMatrix2D(center, angle, scale)
    rotated = cv.warpAffine(image, M, (w, h))
    return rotated

p2_d = rotate(img, -45)
cv.imshow('rotate', p2_d)

#part2_e
def shrink(img):
    scale_percent = 50 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    return resized

p2_e = shrink(img)
cv.imshow('shrink', p2_e)


#part2_f
def binarize(img):
    ret,binary = cv.threshold(img,127,255,cv.THRESH_BINARY)
    return binary

p2_f = binarize(img)
cv.imshow('binarize', p2_f)

cv.waitKey(0)
cv.destroyAllWindows()