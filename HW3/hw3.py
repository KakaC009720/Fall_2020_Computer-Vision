import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread('lena.bmp', 0)
cv2.imshow("aaa", img)

img_bin = np.zeros(img.shape, np.int)
dist = np.zeros(256, np.int)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        dist[img[i][j]] += 1
plt.bar(range(0,256), dist)
plt.show()


for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i][j] = img[i][j] / 3
cv2.imshow('bbb', img)
cv2.imwrite('bbb.bmp', img)

img_bin2 = np.zeros(img.shape, np.int)
dist2 = np.zeros(256, np.int)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        dist2[img[i][j]] += 1
plt.bar(range(0,256), dist2)
plt.show()



def histequ(img, nlevels=256):
    histogram = np.bincount(img.flatten(), minlength=nlevels)

    uniform_hist = (nlevels - 1) * (np.cumsum(histogram)/(img.size * 1.0))
    uniform_hist = uniform_hist.astype('uint8')

    height, width = img.shape
    uniform_img = np.zeros(img.shape, dtype='uint8') 
    for i in range(height):
        for j in range(width):
            uniform_img[i,j] = uniform_hist[img[i,j]]

    return uniform_img


if __name__ == '__main__':
    img = cv2.imread('bbb.bmp', 0)
    uniform_img = histequ(img)

    img_bin3 = np.zeros(uniform_img.shape, np.int)
    dist3 = np.zeros(256, np.int)
    for i in range(uniform_img.shape[0]):
        for j in range(uniform_img.shape[1]):
            dist3[uniform_img[i][j]] += 1
    plt.bar(range(0,256), dist3)
    plt.show()
    cv2.imshow('ccc', uniform_img)
    cv2.waitKey(0)
