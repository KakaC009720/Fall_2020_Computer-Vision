import cv2 
import numpy as np
np.set_printoptions(threshold=10000000000)

def generate_map(img, size):           #生成map
    map = np.zeros(shape = (img.shape[0], img.shape[1]), dtype=np.int)
    count = size // 2
    for k in range(count):
        if k == 0:
            map = np.zeros(shape = (map.shape[0]+2, map.shape[1]+2), dtype=np.int)
            for i in range(map.shape[0]):
                for j in range(map.shape[1]):
                    if i == 0:
                        if j == 0:
                            map[i][j] = img[0][0]
                        elif j == map.shape[1]-1:
                            map[i][j] = img[0][img.shape[1]-1]
                        else:
                            map[i][j] = img[0][j-1]
                    elif i == map.shape[0]-1:
                        if j == 0:
                            map[i][j] = img[img.shape[0]-1][0]
                        elif j == map.shape[1]-1:
                            map[i][j] = img[img.shape[0]-1][img.shape[1]-1]
                        else:
                            map[i][j] = img[img.shape[0]-1][j-1]
                    else:
                        if j == 0:
                            map[i][j] = img[i-1][0]
                        elif j == map.shape[1]-1:
                            map[i][j] = img[i-1][img.shape[1]-1]
                        else:
                            map[i][j] = img[i-1][j-1]
            map_old = map
        elif k > 0:
            map_new = np.zeros(shape = (map_old.shape[0]+2, map_old.shape[1]+2), dtype=np.int)
            for i in range(map_new.shape[0]):
                for j in range(map_new.shape[1]):
                    if i == 0:
                        if j == 0:
                            map_new[i][j] = map_old[0][0]
                        elif j == map_new.shape[1]-1:
                            map_new[i][j] = map_old[0][map_old.shape[1]-1]
                        else:
                            map_new[i][j] = map_old[0][j-1]
                    elif i == map_new.shape[0]-1:
                        if j == 0:
                            map_new[i][j] = map_old[map_old.shape[0]-1][0]
                        elif j == map_new.shape[1]-1:
                            map_new[i][j] = map_old[map_old.shape[0]-1][map_old.shape[1]-1]
                        else:
                            map_new[i][j] = map_old[map_old.shape[0]-1][j-1]
                    else:
                        if j == 0:
                            map_new[i][j] = map_old[i-1][0]
                        elif j == map_new.shape[1]-1:
                            map_new[i][j] = map_old[i-1][map_old.shape[1]-1]
                        else:
                            map_new[i][j] = map_old[i-1][j-1]
            map_old = map_new
    if count == 1:
        return map
    else:
        return map_new

def laplacian_mask_1(img, threshold):
    map = generate_map(img, 3)
    result = np.zeros(img.shape, np.float64)
    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            gradient = map[i-1][j] + map[i][j-1] - 4*map[i][j] + map[i][j+1] + map[i+1][j]
            if gradient >= threshold:
                result[i-1][j-1] = 1
                #print(result[i-1][j-1], end = ' ')
            elif gradient <= (-threshold):
                result[i-1][j-1] = -1
                #print(result[i-1][j-1], end = ' ')
            else:
                result[i-1][j-1] = 0
                #print(result[i-1][j-1], end = ' ')
    #print(result)
    return result

def zero_crossing(result):
    zero_output = np.zeros(img.shape, np.uint8)
    laplacian_output = generate_map(result, 3)
    for i in range(1, laplacian_output.shape[0]-1):
        for j in range(1, laplacian_output.shape[1]-1):
            
            if laplacian_output[i][j] == 1:
                if laplacian_output[i-1][j-1] == -1 or laplacian_output[i-1][j] == -1 or laplacian_output[i-1][j+1] == -1 \
                    or laplacian_output[i][j-1] == -1 or laplacian_output[i][j+1] == -1 \
                    or laplacian_output[i+1][j-1] == -1 or laplacian_output[i+1][j] == -1 or laplacian_output[i+1][j+1] == -1:
                    zero_output[i-1][j-1] = 0
                else:
                    zero_output[i-1][j-1] = 255
            else:
                zero_output[i-1][j-1] = 255
    #print(zero_output)
    return zero_output

def laplacian_mask_2(img, threshold):
    map = generate_map(img, 3)
    result = np.zeros(img.shape, np.float64)
    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            gradient = (map[i-1][j-1] + map[i-1][j] + map[i-1][j+1] \
                        + map[i][j-1]- 8*map[i][j] + map[i][j+1] \
                        + map[i+1][j-1] + map[i+1][j] + map[i+1][j+1]) / 3
            if gradient >= threshold:
                result[i-1][j-1] = 1
            elif gradient <= (-threshold):
                result[i-1][j-1] = -1
            else:
                result[i-1][j-1] = 0
    return result

def minimum_variance(img, threshold):
    map = generate_map(img, 3)
    result = np.zeros(img.shape, np.float64)
    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            gradient = (2*map[i-1][j-1] - map[i-1][j] + 2*map[i-1][j+1] \
                        - map[i][j-1] - 4*map[i][j] - map[i][j+1] \
                        + 2*map[i+1][j-1] - map[i+1][j] + 2*map[i+1][j+1]) / 3
            if gradient >= threshold:
                result[i-1][j-1] = 1
            elif gradient <= (-threshold):
                result[i-1][j-1] = -1
            else:
                result[i-1][j-1] = 0
    return result

def laplacian_of_gaussian(img, threshold):
    map = generate_map(img, 11)
    result = np.zeros(img.shape, np.float64)
    for i in range(5, map.shape[0]-5):
        for j in range(5, map.shape[1]-5):
            gradient =    0*map[i-5][j-5] + 0*map[i-5][j-4] + 0*map[i-5][j-3] - map[i-5][j-2] - map[i-5][j-1] - 2*map[i-5][j] - map[i-5][j+1] - map[i-5][j+2] + 0*map[i-5][j+3] + 0*map[i-5][j+4] + 0*map[i-5][j+5] \
                        + 0*map[i-4][j-5] + 0*map[i-4][j-4] - 2*map[i-4][j-3] - 4*map[i-4][j-2] - 8*map[i-4][j-1] - 9*map[i-4][j] - 8*map[i-4][j+1] - 4*map[i-4][j+2] - 2*map[i-4][j+3] + 0*map[i-4][j+4] + 0*map[i-4][j+5] \
                        + 0*map[i-3][j-5] - 2*map[i-3][j-4] - 7*map[i-3][j-3] - 15*map[i-3][j-2] - 22*map[i-3][j-1] - 23*map[i-3][j] - 22*map[i-3][j+1] - 15*map[i-3][j+2] - 7*map[i-3][j+3] - 2*map[i-3][j+4] + 0*map[i-3][j+5] \
                        - map[i-2][j-5] - 4*map[i-2][j-4] - 15*map[i-2][j-3] - 24*map[i-2][j-2] - 14*map[i-2][j-1] - map[i-2][j] - 14*map[i-2][j+1] - 24*map[i-2][j+2] - 15*map[i-2][j+3] - 4*map[i-2][j+4] - map[i-2][j+5] \
                        - map[i-1][j-5] - 8*map[i-1][j-4] - 22*map[i-1][j-3] - 14*map[i-1][j-2] + 52*map[i-1][j-1] + 103*map[i-1][j] + 52*map[i-1][j+1] - 14*map[i-1][j+2] - 22*map[i-1][j+3] - 8*map[i-1][j+4] - map[i-1][j+5] \
                        - 2*map[i][j-5] - 9*map[i][j-4] - 23*map[i][j-3] - map[i][j-2] + 103*map[i][j-1] + 178*map[i][j] + 103*map[i][j+1] - map[i][j+2] - 23*map[i][j+3] - 9*map[i][j+4] - 2*map[i][j+5] \
                        - map[i+1][j-5] - 8*map[i+1][j-4] - 22*map[i+1][j-3] - 14*map[i+1][j-2] + 52*map[i+1][j-1] + 103*map[i+1][j] + 52*map[i+1][j+1] - 14*map[i+1][j+2] - 22*map[i+1][j+3] - 8*map[i+1][j+4] - map[i+1][j+5] \
                        - map[i+2][j-5] - 4*map[i+2][j-4] - 15*map[i+2][j-3] - 24*map[i+2][j-2] - 14*map[i+2][j-1] - map[i+2][j] - 14*map[i+2][j+1] - 24*map[i+2][j+2] - 15*map[i+2][j+3] - 4*map[i+2][j+4] - map[i+2][j+5] \
                        + 0*map[i+3][j-5] - 2*map[i+3][j-4] - 7*map[i+3][j-3] - 15*map[i+3][j-2] - 22*map[i+3][j-1] - 23*map[i+3][j] - 22*map[i+3][j+1] - 15*map[i+3][j+2] - 7*map[i+3][j+3] - 2*map[i+3][j+4] + 0*map[i+3][j+5] \
                        + 0*map[i+4][j-5] + 0*map[i+4][j-4] - 2*map[i+4][j-3] - 4*map[i+4][j-2] - 8*map[i+4][j-1] - 9*map[i+4][j] - 8*map[i+4][j+1] - 4*map[i+4][j+2] - 2*map[i+4][j+3] + 0*map[i+4][j+4] + 0*map[i+4][j+5] \
                        + 0*map[i+5][j-5] + 0*map[i+5][j-4] + 0*map[i+5][j-3] - map[i+5][j-2] - map[i+5][j-1] - 2*map[i+5][j] - map[i+5][j+1] - map[i+5][j+2] + 0*map[i+5][j+3] + 0*map[i+5][j+4] + 0*map[i+5][j+5]     
            if gradient >= threshold:
                result[i-5][j-5] = 1
            elif gradient <= (-threshold):
                result[i-5][j-5] = -1
            else:
                result[i-5][j-5] = 0
    return result

def difference_of_gaussian(img, threshold):
    map = generate_map(img, 11)
    result = np.zeros(img.shape, np.float64)
    for i in range(5, map.shape[0]-5):
        for j in range(5, map.shape[1]-5):
            gradient =   -map[i-5][j-5] - 3*map[i-5][j-4] - 4*map[i-5][j-3] - 6*map[i-5][j-2] - 7*map[i-5][j-1] - 8*map[i-5][j] - 7*map[i-5][j+1] - 6*map[i-5][j+2] - 4*map[i-5][j+3] - 3*map[i-5][j+4] - map[i-5][j+5] \
                        - 3*map[i-4][j-5] - 5*map[i-4][j-4] - 8*map[i-4][j-3] - 11*map[i-4][j-2] - 13*map[i-4][j-1] - 13*map[i-4][j] - 13*map[i-4][j+1] - 11*map[i-4][j+2] - 8*map[i-4][j+3] - 5*map[i-4][j+4] - 3*map[i-4][j+5] \
                        - 4*map[i-3][j-5] - 8*map[i-3][j-4] - 12*map[i-3][j-3] - 16*map[i-3][j-2] - 17*map[i-3][j-1] - 17*map[i-3][j] - 17*map[i-3][j+1] - 16*map[i-3][j+2] - 12*map[i-3][j+3] - 8*map[i-3][j+4] - 4*map[i-3][j+5] \
                        - 6*map[i-2][j-5] - 11*map[i-2][j-4] - 16*map[i-2][j-3] - 16*map[i-2][j-2] + 0*map[i-2][j-1] + 15*map[i-2][j] + 0*map[i-2][j+1] - 16*map[i-2][j+2] - 16*map[i-2][j+3] - 11*map[i-2][j+4] - 6*map[i-2][j+5] \
                        - 7*map[i-1][j-5] - 13*map[i-1][j-4] - 17*map[i-1][j-3] + 0*map[i-1][j-2] + 85*map[i-1][j-1] + 160*map[i-1][j] + 85*map[i-1][j+1] + 0*map[i-1][j+2] - 17*map[i-1][j+3] - 13*map[i-1][j+4] - 7*map[i-1][j+5] \
                        - 8*map[i][j-5] - 13*map[i][j-4] - 17*map[i][j-3] + 15*map[i][j-2] + 160*map[i][j-1] + 283*map[i][j] + 160*map[i][j+1] + 15*map[i][j+2] - 17*map[i][j+3] - 13*map[i][j+4] - 8*map[i][j+5] \
                        - 7*map[i+1][j-5] - 13*map[i+1][j-4] - 17*map[i+1][j-3] + 0*map[i+1][j-2] + 85*map[i+1][j-1] + 160*map[i+1][j] + 85*map[i+1][j+1] + 0*map[i+1][j+2] - 17*map[i+1][j+3] - 13*map[i+1][j+4] - 7*map[i+1][j+5] \
                        - 6*map[i+2][j-5] - 11*map[i+2][j-4] - 16*map[i+2][j-3] - 16*map[i+2][j-2] + 0*map[i+2][j-1] + 15*map[i+2][j] + 0*map[i+2][j+1] - 16*map[i+2][j+2] - 16*map[i+2][j+3] - 11*map[i+2][j+4] - 6*map[i+2][j+5] \
                        - 4*map[i+3][j-5] - 8*map[i+3][j-4] - 12*map[i+3][j-3] - 16*map[i+3][j-2] - 17*map[i+3][j-1] - 17*map[i+3][j] - 17*map[i+3][j+1] - 16*map[i+3][j+2] - 12*map[i+3][j+3] - 8*map[i+3][j+4] - 4*map[i+3][j+5] \
                        - 3*map[i+4][j-5] - 5*map[i+4][j-4] - 8*map[i+4][j-3] - 11*map[i+4][j-2] - 13*map[i+4][j-1] - 13*map[i+4][j] - 13*map[i+4][j+1] - 11*map[i+4][j+2] - 8*map[i+4][j+3] - 5*map[i+4][j+4] - 3*map[i+4][j+5] \
                        - map[i+5][j-5] - 3*map[i+5][j-4] - 4*map[i+5][j-3] - 6*map[i+5][j-2] - 7*map[i+5][j-1] - 8*map[i+5][j] - 7*map[i+5][j+1] - 6*map[i+5][j+2] - 4*map[i+5][j+3] - 3*map[i+5][j+4] - map[i+5][j+5]     
            if gradient >= threshold:
                result[i-5][j-5] = 1
            elif gradient <= (-threshold):
                result[i-5][j-5] = -1
            else:
                result[i-5][j-5] = 0
    #print(result)
    return result


img = cv2.imread('lena.bmp', 0)

result = laplacian_mask_1(img, 15)
laplacian1 = zero_crossing(result)
cv2.imwrite('laplacian_mask1.bmp', laplacian1)

result = laplacian_mask_2(img, 15)
laplacian2 = zero_crossing(result)
cv2.imwrite('laplacian_mask2.bmp', laplacian2)

result = minimum_variance(img, 20)
mini = zero_crossing(result)
cv2.imwrite('minimum_variance_laplacian.bmp', mini)

result = laplacian_of_gaussian(img, 3000)
log = zero_crossing(result)
cv2.imwrite('laplacian_of_gaussian.bmp', log)

result = difference_of_gaussian(img, 1)
dog = zero_crossing(result)
cv2.imwrite('difference_of_gaussian.bmp', dog)
