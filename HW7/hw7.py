import cv2
import numpy as np
import copy

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

    img_thin = img_d

    for k in range(7):       #迭代7次
        yokoi_map = yokoi(img_thin)
        img_pair = pair_relationship(yokoi_map)
        img_thin = shrink(img_pair)
        img_thin = (img_thin > 0)*255

    cv2.imwrite('thinning.bmp', img_thin)

def yokoi(img_d):
    yokoi_map = np.zeros(img_d.shape, np.int)
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
                elif y1 == 's' and y2 == 's' and y3 == 's' and y4 == 's':  #4個s 表示在yokoi是isolated
                    ans = 6            #為了在pair relationship與shrink不與背景pixel搞混，此處標記為6
                else:
                    ans = 0
                    for z in [y1, y2, y3, y4]:
                        if z == 'q':
                            ans += 1
                
                yokoi_map[i][j] = ans
    return yokoi_map

def pair_relationship(yokoi_map):
    def h(a, m):
        if a == m:
            return 1
        return 0
    img_pair = np.zeros(yokoi_map.shape, np.int)
    for i in range(yokoi_map.shape[0]):
        for j in range(yokoi_map.shape[1]):
            if yokoi_map[i][j] > 0:
                x1, x2, x3, x4 = 0, 0, 0, 0
                if i == 0:
                    if j == 0:
                        x1, x4 = yokoi_map[i][j + 1], yokoi_map[i + 1][j]
                    elif j == yokoi_map.shape[1] - 1:
                        x3, x4 = yokoi_map[i][j - 1], yokoi_map[i + 1][j]
                    else:
                        x1, x3, x4 = yokoi_map[i][j + 1], yokoi_map[i][j - 1], yokoi_map[i + 1][j]
                elif i == yokoi_map.shape[0] - 1:
                    if j == 0:
                        x1, x2 = yokoi_map[i][j + 1], yokoi_map[i - 1][j]
                    elif j == yokoi_map.shape[1] - 1:
                        x2, x3 = yokoi_map[i - 1][j], yokoi_map[i][j - 1]
                    else:
                        x1, x2, x3 = yokoi_map[i][j + 1], yokoi_map[i - 1][j], yokoi_map[i][j - 1]
                else:
                    if j == 0:
                        x1, x2, x4 = yokoi_map[i][j + 1], yokoi_map[i - 1][j], yokoi_map[i + 1][j]
                    elif j == yokoi_map.shape[1] - 1:
                        x2, x3, x4 = yokoi_map[i - 1][j], yokoi_map[i][j - 1], yokoi_map[i + 1][j]
                    else:
                        x1, x2, x3, x4 = yokoi_map[i][j + 1], yokoi_map[i - 1][j], yokoi_map[i][j - 1], yokoi_map[i + 1][j]
                if h(x1, 1) + h(x2, 1) + h(x3, 1) + h(x4, 1) >= 1 and yokoi_map[i][j] == 1:
                    img_pair[i][j] = 1   #p = 1
                else:
                    img_pair[i][j] = 2   #q = 2
    return img_pair

def shrink(img_pair):

    def h(b, c, d, e):
        if b == c and (d != b or e != b):
            return 1
        else:
            return 0
    
    def f(a1, a2, a3, a4, x0):
        if a1 + a2 + a3 + a4 == 1 and img_thin[i][j] == 1:
            return 0
        else:
            return x0

    img_thin = copy.deepcopy(img_pair)
    img_pair = (img_pair > 0)*1

    for i in range(img_pair.shape[0]):
        for j in range(img_pair.shape[1]):
            if img_thin[i][j] == 1:  
                if i == 0:
                    if j == 0:
                    # top-left
                        x7, x2, x6 = 0, 0, 0
                        x3, x0, x1 = 0, img_pair[i][j], img_pair[i][j + 1]
                        x8, x4, x5 = 0, img_pair[i + 1][j], img_pair[i + 1][j + 1]
                    elif j == img_pair.shape[1] - 1:
                    # top-right
                        x7, x2, x6 = 0, 0, 0
                        x3, x0, x1 = img_pair[i][j - 1], img_pair[i][j], 0
                        x8, x4, x5 = img_pair[i + 1][j - 1], img_pair[i + 1][j], 0
                    else:
                    # top-row
                        x7, x2, x6 = 0, 0, 0
                        x3, x0, x1 = img_pair[i][j - 1], img_pair[i][j], img_pair[i][j + 1]
                        x8, x4, x5 = img_pair[i + 1][j - 1], img_pair[i + 1][j], img_pair[i + 1][j + 1]
                elif i == img_pair.shape[0] - 1:
                    if j == 0:
                    # bottom-left
                        x7, x2, x6 = 0, img_pair[i - 1][j], img_pair[i - 1][j + 1]
                        x3, x0, x1 = 0, img_pair[i][j], img_pair[i][j + 1]
                        x8, x4, x5 = 0, 0, 0
                    elif j == img_pair.shape[1] - 1:
                    # bottom-right
                        x7, x2, x6 = img_pair[i - 1][j - 1], img_pair[i - 1][j], 0
                        x3, x0, x1 = img_pair[i][j - 1], img_pair[i][j], 0
                        x8, x4, x5 = 0, 0, 0
                    else:
                    # bottom-row
                        x7, x2, x6 = img_pair[i - 1][j - 1], img_pair[i - 1][j], img_pair[i - 1][j + 1]
                        x3, x0, x1 = img_pair[i][j - 1], img_pair[i][j], img_pair[i][j + 1]
                        x8, x4, x5 = 0, 0, 0
                else:
                    if j == 0:
                        x7, x2, x6 = 0, img_pair[i - 1][j], img_pair[i - 1][j + 1]
                        x3, x0, x1 = 0, img_pair[i][j], img_pair[i][j + 1]
                        x8, x4, x5 = 0, img_pair[i + 1][j], img_pair[i + 1][j + 1]
                    elif j == img_pair.shape[1] - 1:
                        x7, x2, x6 = img_pair[i - 1][j - 1], img_pair[i - 1][j], 0
                        x3, x0, x1 = img_pair[i][j - 1], img_pair[i][j], 0
                        x8, x4, x5 = img_pair[i + 1][j - 1], img_pair[i + 1][j], 0
                    else:
                        x7, x2, x6 = img_pair[i - 1][j - 1], img_pair[i - 1][j], img_pair[i - 1][j + 1]
                        x3, x0, x1 = img_pair[i][j - 1], img_pair[i][j], img_pair[i][j + 1]
                        x8, x4, x5 = img_pair[i + 1][j - 1], img_pair[i + 1][j], img_pair[i + 1][j + 1]

                a1 = h(x0, x1, x6, x2)
                a2 = h(x0, x2, x7, x3)
                a3 = h(x0, x3, x8, x4)
                a4 = h(x0, x4, x5, x1)
                img_pair[i][j] = f(a1, a2, a3, a4, x0)

    return img_pair

if __name__ == '__main__':
    main()
