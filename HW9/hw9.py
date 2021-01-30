import numpy as np
import cv2
import math

def roberts(img, threshold):
    map = np.zeros(shape = (img.shape[0]+1, img.shape[1]+1), dtype=np.int)

    for i in range(map.shape[0]):                   #####kernel是2*2矩陣，會超出size，先把原本矩陣的擴增
        for j in range(map.shape[1]):
            if i < map.shape[0] - 1 and j < map.shape[1] - 1:
                map[i][j] = img[i][j]
            
            elif i == map.shape[0] - 1:
                map[i][j] = map[i-1][j]

            elif j == map.shape[1] - 1:
                map[i][j] = map[i][j-1]
            
            else:
                map[i][j] = map[i-1][j-1]
    
    result = np.zeros(img.shape, np.uint8)

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if i <= img.shape[0] - 1 and j <= img.shape[1] - 1:
                r1 = map[i+1][j+1] - map[i][j]
                r2 = map[i+1][j] - map[i][j+1]

                gradient = math.sqrt(r1 ** 2 + r2 ** 2)
                
                if gradient >= threshold:
                    result[i][j] = 0
                
                else:
                    result[i][j] = 255
    
    return result

def generate_map(img):           ##########kernel 3*3，需先生成上下左右都多一行的map
    map = np.zeros(shape = (img.shape[0]+2, img.shape[1]+2), dtype=np.int)
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
    return map

def prewitt(img, threshold):
    map = generate_map(img)

    result = np.zeros(img.shape, np.uint8)

    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            p1 = -map[i-1][j-1] -map[i-1][j] -map[i-1][j+1] +map[i+1][j-1] +map[i+1][j] +map[i+1][j+1]
            p2 = -map[i-1][j-1] -map[i][j-1] -map[i+1][j-1] +map[i-1][j+1] +map[i][j+1] +map[i+1][j+1]
            
            gradient = math.sqrt(p1 ** 2 + p2 ** 2)
            
            if gradient >= threshold:
                result[i-1][j-1] = 0
                
            else:
                result[i-1][j-1] = 255
    
    
    return result

def sobel(img, threshold):
    map = generate_map(img)

    result = np.zeros(img.shape, np.uint8)

    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            s1 = -map[i-1][j-1] -2*map[i-1][j] -map[i-1][j+1] +map[i+1][j-1] +2*map[i+1][j] +map[i+1][j+1]
            s2 = -map[i-1][j-1] -2*map[i][j-1] -map[i+1][j-1] +map[i-1][j+1] +2*map[i][j+1] +map[i+1][j+1]
            
            gradient = math.sqrt(s1 ** 2 + s2 ** 2)
            
            if gradient >= threshold:
                result[i-1][j-1] = 0
                
            else:
                result[i-1][j-1] = 255
    return result

def frei_and_chen(img, threshold):
    map = generate_map(img)

    result = np.zeros(img.shape, np.uint8)  #####開根號有小數

    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            f1 = -map[i-1][j-1] -(math.sqrt(2)*map[i-1][j]) -map[i-1][j+1] +map[i+1][j-1] +(math.sqrt(2)*map[i+1][j]) +map[i+1][j+1]
            f2 = -map[i-1][j-1] -(math.sqrt(2)*map[i][j-1]) -map[i+1][j-1] +map[i-1][j+1] +(math.sqrt(2)*map[i][j+1]) +map[i+1][j+1]
            

            gradient = math.sqrt(f1 ** 2 + f2 ** 2)
            
            if gradient >= threshold:
                result[i-1][j-1] = 0
                
            else:
                result[i-1][j-1] = 255
    return result

def kirsch_compass(img, threshold):
    map = generate_map(img)

    result = np.zeros(img.shape, np.uint8)

    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            
            k0 = -3*map[i-1][j-1] -3*map[i-1][j] +5*map[i-1][j+1] -3*map[i][j-1] +5*map[i][j+1] -3*map[i+1][j-1] -3*map[i+1][j] +5*map[i+1][j+1]
            k1 = -3*map[i-1][j-1] +5*map[i-1][j] +5*map[i-1][j+1] -3*map[i][j-1] +5*map[i][j+1] -3*map[i+1][j-1] -3*map[i+1][j] -3*map[i+1][j+1]
            k2 =  5*map[i-1][j-1] +5*map[i-1][j] +5*map[i-1][j+1] -3*map[i][j-1] -3*map[i][j+1] -3*map[i+1][j-1] -3*map[i+1][j] -3*map[i+1][j+1]
            k3 =  5*map[i-1][j-1] +5*map[i-1][j] -3*map[i-1][j+1] +5*map[i][j-1] -3*map[i][j+1] -3*map[i+1][j-1] -3*map[i+1][j] -3*map[i+1][j+1]
            k4 =  5*map[i-1][j-1] -3*map[i-1][j] -3*map[i-1][j+1] +5*map[i][j-1] -3*map[i][j+1] +5*map[i+1][j-1] -3*map[i+1][j] -3*map[i+1][j+1]      
            k5 = -3*map[i-1][j-1] -3*map[i-1][j] -3*map[i-1][j+1] +5*map[i][j-1] -3*map[i][j+1] +5*map[i+1][j-1] +5*map[i+1][j] -3*map[i+1][j+1]
            k6 = -3*map[i-1][j-1] -3*map[i-1][j] -3*map[i-1][j+1] -3*map[i][j-1] -3*map[i][j+1] +5*map[i+1][j-1] +5*map[i+1][j] +5*map[i+1][j+1]
            k7 = -3*map[i-1][j-1] -3*map[i-1][j] -3*map[i-1][j+1] -3*map[i][j-1] +5*map[i][j+1] -3*map[i+1][j-1] +5*map[i+1][j] +5*map[i+1][j+1]

            gradient = max(k0, k1, k2, k3, k4, k5, k6, k7)
            
            if gradient >= threshold:
                result[i-1][j-1] = 0
                
            else:
                result[i-1][j-1] = 255
    return result

def robinson_compass(img, threshold):
    map = generate_map(img)

    result = np.zeros(img.shape, np.uint8)

    for i in range(1, map.shape[0]-1):
        for j in range(1, map.shape[1]-1):
            
            r0 = -1*map[i-1][j-1] -0*map[i-1][j] +1*map[i-1][j+1] -2*map[i][j-1] +2*map[i][j+1] -1*map[i+1][j-1] -0*map[i+1][j] +1*map[i+1][j+1]
            r1 = -0*map[i-1][j-1] +1*map[i-1][j] +2*map[i-1][j+1] -1*map[i][j-1] +1*map[i][j+1] -2*map[i+1][j-1] -1*map[i+1][j] -0*map[i+1][j+1]
            r2 =  1*map[i-1][j-1] +2*map[i-1][j] +1*map[i-1][j+1] -0*map[i][j-1] -0*map[i][j+1] -1*map[i+1][j-1] -2*map[i+1][j] -1*map[i+1][j+1]
            r3 =  2*map[i-1][j-1] +1*map[i-1][j] -0*map[i-1][j+1] +1*map[i][j-1] -1*map[i][j+1] -0*map[i+1][j-1] -1*map[i+1][j] -2*map[i+1][j+1]
            r4 =  1*map[i-1][j-1] -0*map[i-1][j] -1*map[i-1][j+1] +2*map[i][j-1] -2*map[i][j+1] +1*map[i+1][j-1] -0*map[i+1][j] -1*map[i+1][j+1]      
            r5 = -0*map[i-1][j-1] -1*map[i-1][j] -2*map[i-1][j+1] +1*map[i][j-1] -1*map[i][j+1] +2*map[i+1][j-1] +1*map[i+1][j] -0*map[i+1][j+1]
            r6 = -1*map[i-1][j-1] -2*map[i-1][j] -1*map[i-1][j+1] -0*map[i][j-1] -0*map[i][j+1] +1*map[i+1][j-1] +2*map[i+1][j] +1*map[i+1][j+1]
            r7 = -2*map[i-1][j-1] -1*map[i-1][j] -0*map[i-1][j+1] -1*map[i][j-1] +1*map[i][j+1] -0*map[i+1][j-1] +1*map[i+1][j] +2*map[i+1][j+1]

            gradient = max(r0, r1, r2, r3, r4, r5, r6, r7)
            
            if gradient >= threshold:
                result[i-1][j-1] = 0
                
            else:
                result[i-1][j-1] = 255
    return result

def nevatia_babu(img, threshold):
    map = generate_map(generate_map(img))

    result = np.zeros(img.shape, np.uint8)

    for i in range(2, map.shape[0]-2):
        for j in range(2, map.shape[1]-2):

            n0 =  100*map[i-2][j-2] +100*map[i-2][j-1] +100*map[i-2][j] +100*map[i-2][j+1] +100*map[i-2][j+2]\
                  +100*map[i-1][j-2] +100*map[i-1][j-1] +100*map[i-1][j] +100*map[i-1][j+1] +100*map[i-1][j+2]\
                  -100*map[i+1][j-2] -100*map[i+1][j-1] -100*map[i+1][j] -100*map[i+1][j+1] -100*map[i+1][j+2]\
                  -100*map[i+2][j-2] -100*map[i+2][j-1] -100*map[i+2][j] -100*map[i+2][j+1] -100*map[i+2][j+2]
            
            n1 = 100*map[i-2][j-2] +100*map[i-2][j-1] +100*map[i-2][j] +100*map[i-2][j+1] +100*map[i-2][j+2]\
                 +100*map[i-1][j-2] +100*map[i-1][j-1] +100*map[i-1][j] +78*map[i-1][j+1] -32*map[i-1][j+2]\
                 +100*map[i][j-2]   +92*map[i][j-1]    +0*map[i][j]   -92*map[i][j+1]       -100*map[i][j+2]\
                 +32*map[i+1][j-2]  -78*map[i+1][j-1] -100*map[i+1][j] -100*map[i+1][j+1] -100*map[i+1][j+2]\
                 -100*map[i+2][j-2] -100*map[i+2][j-1] -100*map[i+2][j] -100*map[i+2][j+1] -100*map[i+2][j+2]
            
            n2 = 100*map[i-2][j-2] +100*map[i-2][j-1] +100*map[i-2][j] +32*map[i-2][j+1] -100*map[i-2][j+2]\
                 +100*map[i-1][j-2] +100*map[i-1][j-1] +92*map[i-1][j] -78*map[i-1][j+1] -100*map[i-1][j+2]\
                 +100*map[i][j-2]   +100*map[i][j-1]    +0*map[i][j]   -100*map[i][j+1]   -100*map[i][j+2]\
                 +100*map[i+1][j-2]  +78*map[i+1][j-1] -92*map[i+1][j] -100*map[i+1][j+1] -100*map[i+1][j+2]\
                 +100*map[i+2][j-2] -32*map[i+2][j-1] -100*map[i+2][j] -100*map[i+2][j+1] -100*map[i+2][j+2]
            
            n3 = -100*map[i-2][j-2] -100*map[i-2][j-1] +0*map[i-2][j] +100*map[i-2][j+1] +100*map[i-2][j+2]\
                 -100*map[i-1][j-2] -100*map[i-1][j-1] +0*map[i-1][j] +100*map[i-1][j+1] +100*map[i-1][j+2]\
                 -100*map[i][j-2]   -100*map[i][j-1]   +0*map[i][j]   +100*map[i][j+1]   +100*map[i][j+2]\
                 -100*map[i+1][j-2] -100*map[i+1][j-1] -0*map[i+1][j] +100*map[i+1][j+1] +100*map[i+1][j+2]\
                 -100*map[i+2][j-2] -100*map[i+2][j-1] -0*map[i+2][j] +100*map[i+2][j+1] +100*map[i+2][j+2]
            
            n4 = -100*map[i-2][j-2] +32*map[i-2][j-1] +100*map[i-2][j] +100*map[i-2][j+1] +100*map[i-2][j+2]\
                 -100*map[i-1][j-2] -78*map[i-1][j-1] +92*map[i-1][j] +100*map[i-1][j+1] +100*map[i-1][j+2]\
                 -100*map[i][j-2]   -100*map[i][j-1]   +0*map[i][j]   +100*map[i][j+1]   +100*map[i][j+2]\
                 -100*map[i+1][j-2] -100*map[i+1][j-1]-92*map[i+1][j] +78*map[i+1][j+1] +100*map[i+1][j+2]\
                 -100*map[i+2][j-2] -100*map[i+2][j-1]-100*map[i+2][j] -32*map[i+2][j+1] +100*map[i+2][j+2]
            
            n5 = 100*map[i-2][j-2] +100*map[i-2][j-1] +100*map[i-2][j] +100*map[i-2][j+1] +100*map[i-2][j+2]\
                 -32*map[i-1][j-2] +78*map[i-1][j-1]  +100*map[i-1][j] +100*map[i-1][j+1] +100*map[i-1][j+2]\
                 -100*map[i][j-2]   -92*map[i][j-1]      +0*map[i][j]   +92*map[i][j+1]   +100*map[i][j+2]\
                 -100*map[i+1][j-2] -100*map[i+1][j-1] -100*map[i+1][j] -78*map[i+1][j+1] +32*map[i+1][j+2]\
                 -100*map[i+2][j-2] -100*map[i+2][j-1] -100*map[i+2][j] -100*map[i+2][j+1] -100*map[i+2][j+2]

            N = max(n0, n1, n2, n3, n4, n5)
            
            if N >= threshold:
                result[i-2][j-2] = 0
                
            else:
                result[i-2][j-2] = 255
    return result


img = cv2.imread('lena.bmp', 0)

roberts_img = roberts(img, 12)
cv2.imwrite('roberts.bmp', roberts_img)

prewitt_img = prewitt(img, 24)
cv2.imwrite('prewitt.bmp', prewitt_img)

sobel_img = sobel(img, 38)
cv2.imwrite('sobel.bmp', sobel_img)

frei_and_chen_img = frei_and_chen(img, 30)
cv2.imwrite('frei_and_chen.bmp', frei_and_chen_img)

kirsch_compass_img = kirsch_compass(img, 135)
cv2.imwrite('kirsch_compass.bmp', kirsch_compass_img)

robinson_compass_img = robinson_compass(img, 43)
cv2.imwrite('robinson_compass.bmp', robinson_compass_img)

nevatia_babu_img = nevatia_babu(img, 12500)
cv2.imwrite('nevatia_babu.bmp', nevatia_babu_img)