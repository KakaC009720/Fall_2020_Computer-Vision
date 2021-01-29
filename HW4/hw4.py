import cv2 
import numpy as np


def main():
    img = cv2.imread('lena.bmp', 0)
    img_bin = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > 128:
                img_bin[i][j] = 255
            else:
                img_bin[i][j] = 0
    cv2.imwrite('bin.bmp', img_bin)

    img_bin2 = np.zeros(img_bin.shape, np.int)
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):
            if img_bin[i][j] == 255:
                img_bin2[i][j] = 0
            else:
                img_bin[i][j] == 0
                img_bin2[i][j] = 255
    cv2.imwrite('bin2.bmp', img_bin2)

    kernel = [[-2, -1], [-2, 0], [-2, 1],
        [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
        [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
        [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
        [2, -1], [2, 0], [2, 1]]
    
    J_kernel = [[0, -1], [0, 0], [1, 0]]
    K_kernel = [[-1, 0], [-1, 1], [0, 1]]

    img_dil = dilation(img_bin, kernel)
    cv2.imwrite('dilation.bmp', img_dil)
    img_ero = erosion(img_bin, kernel)
    cv2.imwrite('erosion.bmp', img_ero)
    img_open = opening(img_bin, kernel)
    cv2.imwrite('opening.bmp', img_open)
    img_close = closing(img_bin, kernel)
    cv2.imwrite('closing.bmp', img_close)

    img_eroj = erosion(img_bin, J_kernel)
    cv2.imwrite('erosionj.bmp', img_eroj)
    img_erok = erosion(img_bin2, K_kernel)
    cv2.imwrite('erosionk.bmp', img_erok)

    img_ham = hit_and_miss(img_bin, img_eroj, img_erok)
    cv2.imwrite('hit_and_miss.bmp', img_ham)


def dilation(img_bin, kernel):
    img_dil = np.zeros(img_bin.shape, np.int)
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):
            if img_bin[i][j] > 0:
                for element in kernel:
                    p, q = element
                    if (i + p) >= 0 and (i + p) <= (img_bin.shape[0]-1) and \
                    (j + q) >= 0 and (j + q) <= (img_bin.shape[1]-1):
                        img_dil[i+p][j+q] = 255
    return img_dil

def erosion(img_bin, kernel):
    img_ero = np.zeros(img_bin.shape, np.int)
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):

            exist = True
            for element in kernel:
                p, q = element
                if (i + p) < 0 or (i + p) > (img_bin.shape[0]-1) or \
                    (j + q) < 0 or (j + q) > (img_bin.shape[1]-1) or \
                    img_bin[i+p][j+q] == 0:                              #判斷kernel是否碰到黑點
                        exist = False
                        break
            if exist:
                img_ero[i][j] = 255
    return img_ero

def erosionj(img_bin, J_kernel):
    img_eroj = np.zeros(img_bin.shape, np.int)
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):
 
            exist = True
            for element in J_kernel:
                p, q = element
                if (i + p) < 0 or (i + p) > (img_bin.shape[0]-1) or \
                    (j + q) < 0 or (j + q) > (img_bin.shape[1]-1) or \
                    img_bin[i+p][j+q] == 0:                              #判斷kernel是否碰到黑點
                        exist = False
                        break
            if exist:
                img_eroj[i][j] = 255
    return img_eroj

def erosionk(img_bin2, K_kernel):
    img_erok = np.zeros(img_bin2.shape, np.int)
    for i in range(img_bin2.shape[0]):
        for j in range(img_bin2.shape[1]):
            exist = True
            for element in K_kernel:
                p, q = element
                if (i + p) < 0 or (i + p) > (img_bin2.shape[0]-1) or \
                   (j + q) < 0 or (j + q) > (img_bin2.shape[1]-1) or \
                   img_bin2[i+p][j+q] == 0:                              #判斷kernel是否碰到黑點
                        exist = False
                        break
            if exist:
                img_erok[i][j] = 255
    return img_erok

def opening(img_bin, kernel):
    img_open = dilation(erosion(img_bin, kernel), kernel)
    return img_open

def closing(img_bin, kernel):
    img_close = erosion(dilation(img_bin, kernel), kernel)
    return img_close

def hit_and_miss(img_bin, img_eroj, img_erok):
    img_ham = np.zeros(img_bin.shape, np.int)
    for i in range(img_bin.shape[0]):
        for j in range(img_bin.shape[1]):
            if img_eroj[i][j] == 255 and img_erok[i][j] == 255:
                img_ham[i][j] = 255
            else:
                img_ham[i][j] = 0
    return img_ham



if __name__ == '__main__':
    main()
