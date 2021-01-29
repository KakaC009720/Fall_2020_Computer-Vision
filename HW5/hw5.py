import cv2
import numpy as np

def main():
    img = cv2.imread('lena.bmp', 0)
    kernel = [[-2, -1], [-2, 0], [-2, 1],
        [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
        [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
        [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
        [2, -1], [2, 0], [2, 1]]
    
    img_dil = dilation(img, kernel)
    cv2.imwrite('dilation.bmp', img_dil)
    img_ero = erosion(img, kernel)
    cv2.imwrite('erosion.bmp', img_ero)
    img_open = opening(img, kernel)
    cv2.imwrite('opening.bmp', img_open)
    img_close = closing(img, kernel)
    cv2.imwrite('closing.bmp', img_close)
    
def dilation(img, kernel):
    img_dil = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > 0:
                maximum = 0
                for element in kernel:
                    p, q = element
                    if (i + p) >= 0 and (i + p) <= (img.shape[0] - 1) and \
                       (j + q) >= 0 and (j + q) <= (img.shape[1] - 1):
                       if img[i + p][j + q] > maximum:
                           maximum = img[i + p][j + q]
                for element in kernel:
                    p, q = element
                    if (i + p) >= 0 and (i + p) <= (img.shape[0] - 1) and \
                       (j + q) >= 0 and (j + q) <= (img.shape[1] - 1):
                       img_dil[i + p][j + q] = maximum
    return img_dil

def erosion(img, kernel):
    img_ero = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            exist = True
            minimum = np.inf
            for element in kernel:
                p, q = element
                if (i + p) >= 0 and (i + p) <= (img.shape[0] - 1) and \
                   (j + q) >= 0 and (j + q) <= (img.shape[1] - 1):
                    if img[i + p][j + q] == 0:
                        exist = False
                        break
                    if img[i + p][j + q] < minimum:
                        minimum = img[i + p][j + q]
            exist = True
            for element in kernel:
                p, q = element
                if (i + p) >= 0 and (i + p) <= (img.shape[0] - 1) and \
                   (j + q) >= 0 and (j + q) <= (img.shape[1] - 1):
                    if img[i + p][j + q] == 0:
                        exist = False
                        break
                if (i + p) >= 0 and (i + p) <= (img.shape[0] - 1) and \
                   (j + q) >= 0 and (j + q) <= (img.shape[1] - 1) and \
                   exist:
                    img_ero[i + p][j + q] = minimum
    return img_ero

def opening(img, kernel):
    return dilation(erosion(img, kernel), kernel)

def closing(img, kernel):
    return erosion(dilation(img, kernel), kernel)

if __name__ == '__main__':
    main()