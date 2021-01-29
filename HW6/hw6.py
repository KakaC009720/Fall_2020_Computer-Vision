import cv2
import numpy as np

def main():
    img = cv2.imread('lena.bmp', 0)

    img_bin = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] >= 128:
                img_bin[i][j] = 1

    img_d = np.zeros((64, 64), np.int)
    for i in range(img_d.shape[0]):
        for j in range(img_d.shape[1]):
            img_d[i][j] = img_bin[8*i][8*j]

    def h(b, c, d, e):
        if b == c and (d != b or e != b):
            return 'q'
        if b == c and (d == b and e == b):
            return 'r'
        return 's'

 
    for i in range(img_d.shape[0]):
        for j in range(img_d.shape[1]):
            if img_d[i][j] > 0:  
                if i == 0:
                    if j == 0:
                    # top-left
                        x7, x2, x6 = 0, 0, 0
                        x3, x0, x1 = 0, img_d[i][j], img_d[i][j + 1]
                        x8, x4, x5 = 0, img_d[i + 1][j], img_d[i + 1][j + 1]
                    elif j == img_d.shape[1] - 1:
                    # top-right
                        x7, x2, x6 = 0, 0, 0
                        x3, x0, x1 = img_d[i][j - 1], img_d[i][j], 0
                        x8, x4, x5 = img_d[i + 1][j - 1], img_d[i + 1][j], 0
                    else:
                    # top-row
                        x7, x2, x6 = 0, 0, 0
                        x3, x0, x1 = img_d[i][j - 1], img_d[i][j], img_d[i][j + 1]
                        x8, x4, x5 = img_d[i + 1][j - 1], img_d[i + 1][j], img_d[i + 1][j + 1]
                elif i == img_d.shape[0] - 1:
                    if j == 0:
                    # bottom-left
                        x7, x2, x6 = 0, img_d[i - 1][j], img_d[i - 1][j + 1]
                        x3, x0, x1 = 0, img_d[i][j], img_d[i][j + 1]
                        x8, x4, x5 = 0, 0, 0
                    elif j == img_d.shape[1] - 1:
                    # bottom-right
                        x7, x2, x6 = img_d[i - 1][j - 1], img_d[i - 1][j], 0
                        x3, x0, x1 = img_d[i][j - 1], img_d[i][j], 0
                        x8, x4, x5 = 0, 0, 0
                    else:
                    # bottom-row
                        x7, x2, x6 = img_d[i - 1][j - 1], img_d[i - 1][j], img_d[i - 1][j + 1]
                        x3, x0, x1 = img_d[i][j - 1], img_d[i][j], img_d[i][j + 1]
                        x8, x4, x5 = 0, 0, 0
                else:
                    if j == 0:
                        x7, x2, x6 = 0, img_d[i - 1][j], img_d[i - 1][j + 1]
                        x3, x0, x1 = 0, img_d[i][j], img_d[i][j + 1]
                        x8, x4, x5 = 0, img_d[i + 1][j], img_d[i + 1][j + 1]
                    elif j == img_d.shape[1] - 1:
                        x7, x2, x6 = img_d[i - 1][j - 1], img_d[i - 1][j], 0
                        x3, x0, x1 = img_d[i][j - 1], img_d[i][j], 0
                        x8, x4, x5 = img_d[i + 1][j - 1], img_d[i + 1][j], 0
                    else:
                        x7, x2, x6 = img_d[i - 1][j - 1], img_d[i - 1][j], img_d[i - 1][j + 1]
                        x3, x0, x1 = img_d[i][j - 1], img_d[i][j], img_d[i][j + 1]
                        x8, x4, x5 = img_d[i + 1][j - 1], img_d[i + 1][j], img_d[i + 1][j + 1]

                y1 = h(x0, x1, x6, x2)
                y2 = h(x0, x2, x7, x3)
                y3 = h(x0, x3, x8, x4)
                y4 = h(x0, x4, x5, x1)

                if y1 == 'r' and y2 == 'r' and y3 == 'r' and y4 == 'r':
                    ans = 5
                else:
                    ans = 0
                    for z in [y1, y2, y3, y4]:
                        if z == 'q':
                            ans += 1

                print(ans, end='')

            else:
                print(' ', end='')

            if j == img_d.shape[1] - 1:
                print('')

if __name__ == '__main__':
    main()

