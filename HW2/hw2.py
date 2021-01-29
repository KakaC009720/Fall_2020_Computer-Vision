import copy
import numpy as np
import matplotlib.pyplot as plt
import cv2 


def main():
    img = cv2.imread('lena.bmp', 0)
    img_bin = np.zeros(img.shape, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] >= 128:
                img_bin[i][j] = 255

    cv2.imwrite('binarize.bmp', img_bin)
    
    dist = np.zeros(256, np.int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            dist[img[i][j]] += 1
    plt.bar(range(0,256), dist)
    plt.show()


    group = np.zeros(img.shape, np.int)
    k = 1
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img_bin[i][j] > 0:
                group[i][j] = k
                k += 1
    group_backup = copy.deepcopy(group)

    while True:
        # top-down pass ...
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if i == 0:
                    if j == 0:
                    # up-left corner
                        if group[i][j] > 0:
                            # check all of its neighbors for minimum id
                            min_id = group[i][j]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            # replace all of its neighbors with the minimum id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    elif j == img.shape[1] - 1:
                    # up-right corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    else:
                    # first row except the above two cases
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                elif i == img.shape[0] - 1:
                    if j == 0:
                    # bottom-left corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                    elif j == img.shape[1] - 1:
                    # bottom-right corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                    else:
                    # last row except the above two cases
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                else:
                    if j == 0:
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    elif j == img.shape[1] - 1:
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    else:
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
        # bottom-up pass ...
        for i in range(img.shape[0] - 1, -1, -1): # for lena.bmp: 511, 510, 509, ..., 2, 1, 0
            for j in range(img.shape[1]):
                if i == 0:
                    if j == 0:
                    # up-left corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    elif j == img.shape[1] - 1:
                    # up-right corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    else:
                    # first row except the above two cases
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                elif i == img.shape[0] - 1:
                    if j == 0:
                    # bottom-left corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                    elif j == img.shape[1] - 1:
                    # bottom-right corner
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                    else:
                    # last row except the above two cases
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                else:
                    if j == 0:
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    elif j == img.shape[1] - 1:
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
                    else:
                        if group[i][j] > 0:
                            min_id = group[i][j]
                            if group[i - 1][j] > 0 and group[i - 1][j] < min_id:
                                min_id = group[i - 1][j]
                            if group[i][j - 1] > 0 and group[i][j - 1] < min_id:
                                min_id = group[i][j - 1]
                            if group[i][j + 1] > 0 and group[i][j + 1] < min_id:
                                min_id = group[i][j + 1]
                            if group[i + 1][j] > 0 and group[i + 1][j] < min_id:
                                min_id = group[i + 1][j]
                            if group[i - 1][j] > 0:
                                group[i - 1][j] = min_id
                            if group[i][j - 1] > 0:
                                group[i][j - 1] = min_id
                            if group[i][j + 1] > 0:
                                group[i][j + 1] = min_id
                            if group[i + 1][j] > 0:
                                group[i + 1][j] = min_id
        # stop iterating if no change
        if False not in (group == group_backup):
            break
        # keep track of latest group
        group_backup = copy.deepcopy(group)


    count_pixel = np.zeros(np.max(group) + 1, np.int)
    for i in range(group.shape[0]):
        for j in range(group.shape[1]):
            if group[i][j] > 0:
                count_pixel[group[i][j]] += 1
                

    for i in range(group.shape[0]):
        for j in range(group.shape[1]):
            if count_pixel[group[i][j]] < 500:
                group[i][j] = 0

    n_regions = np.sum(count_pixel >= 500)
              
    cv2.imwrite('thre.bmp', img_bin)
    img_bin = cv2.imread('thre.bmp', 1)


    for k in range(count_pixel.shape[0]):
        if count_pixel[k] >= 500:
            # k is the region id

            (max_i, max_j, min_i, min_j) = (0, 0, 1000, 1000)
            (ii, jj) = (0, 0)
            count = 0

            for i in range(group.shape[0]):
                for j in range(group.shape[1]):
                    if group[i][j] == k:
                        if i > max_i:
                            max_i = i
                        if j > max_j:
                            max_j = j
                        if i < min_i:
                            min_i = i
                        if j < min_j:
                            min_j = j
                        ii += i
                        jj += j
                        count += 1
            ii = ii//count
            jj = jj//count
        
            cv2.rectangle(img_bin, (min_j,min_i), (max_j,max_i), (255,0,0), 2)
            cv2.circle(img_bin, (jj, ii), 0, (0, 0, 255), 20)

    cv2.imshow('centroid & bounding box', img_bin)
    cv2.waitKey(0)
    cv2.imwrite('connect_4.bmp', img_bin)
       

if __name__ == '__main__':
    main()
