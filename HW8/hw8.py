def getGaussianNoiseImage(originalImage, amplitude):
    from PIL import Image
    import random
    gaussianNoiseImage = originalImage.copy()

    for c in range(originalImage.size[0]):
        for r in range(originalImage.size[1]):
            noisePixel = int(originalImage.getpixel((c, r)) + amplitude * random.gauss(0, 1))
            if noisePixel > 255:
                noisePixel = 255
            gaussianNoiseImage.putpixel((c, r), noisePixel)
    return gaussianNoiseImage

def getSaltAndPepperImage(originalImage, probability):
    from PIL import Image
    import random
    saltAndPepperImage = originalImage.copy()
    for c in range(originalImage.size[0]):
        for r in range(originalImage.size[1]):
            randomValue = random.uniform(0, 1)
            if (randomValue <= probability):
                saltAndPepperImage.putpixel((c, r), 0)
            elif (randomValue >= 1 - probability):
                saltAndPepperImage.putpixel((c, r), 255)
            else:
                saltAndPepperImage.putpixel((c, r), originalImage.getpixel((c, r)))
    return saltAndPepperImage

def boxFilter(originalImage, boxWidth, boxHeight):
    centerKernel = (boxWidth // 2, boxHeight // 2)
    boxFilterImage = originalImage.copy()
    for c in range(originalImage.size[0]):
        for r in range(originalImage.size[1]):
            boxPixels = []
            for x in range(boxWidth):
                for y in range(boxHeight):
                    destX = c + (x - centerKernel[0])
                    destY = r + (y - centerKernel[1])
                    if ((0 <= destX < originalImage.size[0]) and \
                        (0 <= destY < originalImage.size[1])):
                        originalPixel = originalImage.getpixel((destX, destY))
                        boxPixels.append(originalPixel)
            boxFilterImage.putpixel((c, r), int(sum(boxPixels) / len(boxPixels)))
    return boxFilterImage

def medianFilter(originalImage, boxWidth, boxHeight):
    centerKernel = (boxWidth // 2, boxHeight // 2)
    medianFilterImage = originalImage.copy()
    for c in range(originalImage.size[0]):
        for r in range(originalImage.size[1]):
            boxPixels = []
            for x in range(boxWidth):
                for y in range(boxHeight):
                    destX = c + (x - centerKernel[0])
                    destY = r + (y - centerKernel[1])
                    if ((0 <= destX < originalImage.size[0]) and \
                        (0 <= destY < originalImage.size[1])):
                        originalPixel = originalImage.getpixel((destX, destY))
                        boxPixels.append(originalPixel)
            boxPixels.sort()
            medianPixel = boxPixels[len(boxPixels) // 2]
            medianFilterImage.putpixel((c, r), medianPixel)
    return medianFilterImage

def dilation(originalImage, kernel, centerKernel):
    from PIL import Image
    dilationImage = Image.new('L', originalImage.size)
    for c in range(originalImage.size[0]):
        for r in range(originalImage.size[1]):
            localMaxPixel = 0
            for x in range(kernel.shape[0]):
                for y in range(kernel.shape[1]):
                    if (kernel[x, y] == 1):
                        destX = c + (x - centerKernel[0])
                        destY = r + (y - centerKernel[1])
                        if ((0 <= destX < originalImage.size[0]) and \
                            (0 <= destY < originalImage.size[1])):
                            originalPixel = originalImage.getpixel((destX, destY))
                            localMaxPixel = max(localMaxPixel, originalPixel)
            dilationImage.putpixel((c, r), localMaxPixel)
    return dilationImage

def erosion(originalImage, kernel, centerKernel):
    from PIL import Image
    erosionImage = Image.new('L', originalImage.size)
    for c in range(originalImage.size[0]):
        for r in range(originalImage.size[1]):
            localMinPixel = 255
            for x in range(kernel.shape[0]):
                for y in range(kernel.shape[1]):
                    if (kernel[x, y] == 1):
                        destX = c + (x - centerKernel[0])
                        destY = r + (y - centerKernel[1])
                        if ((0 <= destX < originalImage.size[0]) and \
                            (0 <= destY < originalImage.size[1])):
                            originalPixel = originalImage.getpixel((destX, destY))
                            localMinPixel = min(localMinPixel, originalPixel)
            erosionImage.putpixel((c, r), localMinPixel)
    return erosionImage

def opening(originalImage, kernel, centerKernel):
    return dilation(erosion(originalImage, kernel, centerKernel), kernel, centerKernel)

def closing(originalImage, kernel, centerKernel):
    return erosion(dilation(originalImage, kernel, centerKernel), kernel, centerKernel)

def openingThenClosing(originalImage, kernel, centerKernel):
    return closing(opening(originalImage, kernel, centerKernel), kernel, centerKernel)

def closingThenOpening(originalImage, kernel, centerKernel):
    return opening(closing(originalImage, kernel, centerKernel), kernel, centerKernel)

def getSNR(signalImage, noiseImage):
    import math
    muSignal = 0
    powerSignal = 0
    muNoise = 0
    powerNoise = 0

    for c in range(signalImage.size[0]):
        for r in range(signalImage.size[1]):
            muSignal = muSignal + signalImage.getpixel((c, r))
    muSignal = muSignal / (signalImage.size[0] * signalImage.size[1])

    for c in range(noiseImage.size[0]):
        for r in range(noiseImage.size[1]):
            muNoise = muNoise + (noiseImage.getpixel((c, r)) - signalImage.getpixel((c, r)))
    muNoise = muNoise / (noiseImage.size[0] * noiseImage.size[1])

    for c in range(signalImage.size[0]):
        for r in range(signalImage.size[1]):
            powerSignal = powerSignal + math.pow(signalImage.getpixel((c, r)) - muSignal, 2)
    powerSignal = powerSignal / (signalImage.size[0] * signalImage.size[1])

    for c in range(noiseImage.size[0]):
        for r in range(noiseImage.size[1]):
            powerNoise = powerNoise +  math.pow((noiseImage.getpixel((c, r)) - signalImage.getpixel((c, r))) - muNoise, 2)
    powerNoise = powerNoise / (noiseImage.size[0] * noiseImage.size[1])

    return 20 * math.log(math.sqrt(powerSignal) / math.sqrt(powerNoise), 10)

if __name__ == '__main__':
    from PIL import Image
    import numpy as np
    seed = 888
    np.random.seed(seed)

    kernel = np.array([\
        [0, 1, 1, 1, 0], \
        [1, 1, 1, 1, 1], \
        [1, 1, 1, 1, 1], \
        [1, 1, 1, 1, 1], \
        [0, 1, 1, 1, 0]])
    centerKernel = (2, 2)

    originalImage = Image.open('lena.bmp')
    
    gaussianNoise_10_Image = getGaussianNoiseImage(originalImage, 10)
    gaussianNoise_30_Image = getGaussianNoiseImage(originalImage, 30)

    saltAndPepper_0_10_Image = getSaltAndPepperImage(originalImage, 0.10)
    saltAndPepper_0_05_Image = getSaltAndPepperImage(originalImage, 0.05)

    gaussianNoise_10_box_3x3_Image = boxFilter(gaussianNoise_10_Image, 3, 3)
    gaussianNoise_30_box_3x3_Image = boxFilter(gaussianNoise_30_Image, 3, 3)
    saltAndPepper_0_10_box_3x3_Image = boxFilter(saltAndPepper_0_10_Image, 3, 3)
    saltAndPepper_0_05_box_3x3_Image = boxFilter(saltAndPepper_0_05_Image, 3, 3)

    gaussianNoise_10_box_5x5_Image = boxFilter(gaussianNoise_10_Image, 5, 5)
    gaussianNoise_30_box_5x5_Image = boxFilter(gaussianNoise_30_Image, 5, 5)
    saltAndPepper_0_10_box_5x5_Image = boxFilter(saltAndPepper_0_10_Image, 5, 5)
    saltAndPepper_0_05_box_5x5_Image = boxFilter(saltAndPepper_0_05_Image, 5, 5)

    gaussianNoise_10_median_3x3_Image = medianFilter(gaussianNoise_10_Image, 3, 3)
    gaussianNoise_30_median_3x3_Image = medianFilter(gaussianNoise_30_Image, 3, 3)
    saltAndPepper_0_10_median_3x3_Image = medianFilter(saltAndPepper_0_10_Image, 3, 3)
    saltAndPepper_0_05_median_3x3_Image = medianFilter(saltAndPepper_0_05_Image, 3, 3)

    gaussianNoise_10_median_5x5_Image = medianFilter(gaussianNoise_10_Image, 5, 5)
    gaussianNoise_30_median_5x5_Image = medianFilter(gaussianNoise_30_Image, 5, 5)
    saltAndPepper_0_10_median_5x5_Image = medianFilter(saltAndPepper_0_10_Image, 5, 5)
    saltAndPepper_0_05_median_5x5_Image = medianFilter(saltAndPepper_0_05_Image, 5, 5)

    gaussianNoise_10_openingThenClosing_Image = openingThenClosing(gaussianNoise_10_Image, kernel, centerKernel)
    gaussianNoise_30_openingThenClosing_Image = openingThenClosing(gaussianNoise_30_Image, kernel, centerKernel)
    saltAndPepper_0_10_openingThenClosing_Image = openingThenClosing(saltAndPepper_0_10_Image, kernel, centerKernel)
    saltAndPepper_0_05_openingThenClosing_Image = openingThenClosing(saltAndPepper_0_05_Image, kernel, centerKernel)

    gaussianNoise_10_closingThenOpening_Image = closingThenOpening(gaussianNoise_10_Image, kernel, centerKernel)
    gaussianNoise_30_closingThenOpening_Image = closingThenOpening(gaussianNoise_30_Image, kernel, centerKernel)
    saltAndPepper_0_10_closingThenOpening_Image = closingThenOpening(saltAndPepper_0_10_Image, kernel, centerKernel)
    saltAndPepper_0_05_closingThenOpening_Image = closingThenOpening(saltAndPepper_0_05_Image, kernel, centerKernel)

    gaussianNoise_10_Image.save('gaussianNoise_10.bmp')
    gaussianNoise_30_Image.save('gaussianNoise_30.bmp')
    saltAndPepper_0_10_Image.save('saltAndPepper_0_10.bmp')
    saltAndPepper_0_05_Image.save('saltAndPepper_0_05.bmp')

    gaussianNoise_10_box_3x3_Image.save('gaussianNoise_10_box_3x3.bmp')
    gaussianNoise_30_box_3x3_Image.save('gaussianNoise_30_box_3x3.bmp')
    saltAndPepper_0_10_box_3x3_Image.save('saltAndPepper_0_10_box_3x3.bmp')
    saltAndPepper_0_05_box_3x3_Image.save('saltAndPepper_0_05_box_3x3.bmp')

    gaussianNoise_10_box_5x5_Image.save('gaussianNoise_10_box_5x5.bmp')
    gaussianNoise_30_box_5x5_Image.save('gaussianNoise_30_box_5x5.bmp')
    saltAndPepper_0_10_box_5x5_Image.save('saltAndPepper_0_10_box_5x5.bmp')
    saltAndPepper_0_05_box_5x5_Image.save('saltAndPepper_0_05_box_5x5.bmp')

    gaussianNoise_10_median_3x3_Image.save('gaussianNoise_10_median_3x3.bmp')
    gaussianNoise_30_median_3x3_Image.save('gaussianNoise_30_median_3x3.bmp')
    saltAndPepper_0_10_median_3x3_Image.save('saltAndPepper_0_10_median_3x3.bmp')
    saltAndPepper_0_05_median_3x3_Image.save('saltAndPepper_0_05_median_3x3.bmp')

    gaussianNoise_10_median_5x5_Image.save('gaussianNoise_10_median_5x5.bmp')
    gaussianNoise_30_median_5x5_Image.save('gaussianNoise_30_median_5x5.bmp')
    saltAndPepper_0_10_median_5x5_Image.save('saltAndPepper_0_10_median_5x5.bmp')
    saltAndPepper_0_05_median_5x5_Image.save('saltAndPepper_0_05_median_5x5.bmp')

    gaussianNoise_10_openingThenClosing_Image.save('gaussianNoise_10_openingThenClosing.bmp')
    gaussianNoise_30_openingThenClosing_Image.save('gaussianNoise_30_openingThenClosing.bmp')
    saltAndPepper_0_10_openingThenClosing_Image.save('saltAndPepper_0_10_openingThenClosing.bmp')
    saltAndPepper_0_05_openingThenClosing_Image.save('saltAndPepper_0_05_openingThenClosing.bmp')

    gaussianNoise_10_closingThenOpening_Image.save('gaussianNoise_10_closingThenOpening.bmp')
    gaussianNoise_30_closingThenOpening_Image.save('gaussianNoise_30_closingThenOpening.bmp')
    saltAndPepper_0_10_closingThenOpening_Image.save('saltAndPepper_0_10_closingThenOpening.bmp')
    saltAndPepper_0_05_closingThenOpening_Image.save('saltAndPepper_0_05_closingThenOpening.bmp')

    gaussianNoise_10_SNR = getSNR(originalImage, gaussianNoise_10_Image)
    gaussianNoise_30_SNR = getSNR(originalImage, gaussianNoise_30_Image)
    saltAndPepper_0_10_SNR = getSNR(originalImage, saltAndPepper_0_10_Image)
    saltAndPepper_0_05_SNR = getSNR(originalImage, saltAndPepper_0_05_Image)

    gaussianNoise_10_box_3x3_SNR = getSNR(originalImage, gaussianNoise_10_box_3x3_Image)
    gaussianNoise_30_box_3x3_SNR = getSNR(originalImage, gaussianNoise_30_box_3x3_Image)
    saltAndPepper_0_10_box_3x3_SNR = getSNR(originalImage, saltAndPepper_0_10_box_3x3_Image)
    saltAndPepper_0_05_box_3x3_SNR = getSNR(originalImage, saltAndPepper_0_05_box_3x3_Image)
    gaussianNoise_10_box_5x5_SNR = getSNR(originalImage, gaussianNoise_10_box_5x5_Image)
    gaussianNoise_30_box_5x5_SNR = getSNR(originalImage, gaussianNoise_30_box_5x5_Image)
    saltAndPepper_0_10_box_5x5_SNR = getSNR(originalImage, saltAndPepper_0_10_box_5x5_Image)
    saltAndPepper_0_05_box_5x5_SNR = getSNR(originalImage, saltAndPepper_0_05_box_5x5_Image)

    gaussianNoise_10_median_3x3_SNR = getSNR(originalImage, gaussianNoise_10_median_3x3_Image)
    gaussianNoise_30_median_3x3_SNR = getSNR(originalImage, gaussianNoise_30_median_3x3_Image)
    saltAndPepper_0_10_median_3x3_SNR = getSNR(originalImage, saltAndPepper_0_10_median_3x3_Image)
    saltAndPepper_0_05_median_3x3_SNR = getSNR(originalImage, saltAndPepper_0_05_median_3x3_Image)
    gaussianNoise_10_median_5x5_SNR = getSNR(originalImage, gaussianNoise_10_median_5x5_Image)
    gaussianNoise_30_median_5x5_SNR = getSNR(originalImage, gaussianNoise_30_median_5x5_Image)
    saltAndPepper_0_10_median_5x5_SNR = getSNR(originalImage, saltAndPepper_0_10_median_5x5_Image)
    saltAndPepper_0_05_median_5x5_SNR = getSNR(originalImage, saltAndPepper_0_05_median_5x5_Image)

    gaussianNoise_10_openingThenClosing_SNR = getSNR(originalImage, gaussianNoise_10_openingThenClosing_Image)
    gaussianNoise_30_openingThenClosing_SNR = getSNR(originalImage, gaussianNoise_30_openingThenClosing_Image)
    saltAndPepper_0_10_openingThenClosing_SNR = getSNR(originalImage, saltAndPepper_0_10_openingThenClosing_Image)
    saltAndPepper_0_05_openingThenClosing_SNR = getSNR(originalImage, saltAndPepper_0_05_openingThenClosing_Image)

    gaussianNoise_10_closingThenOpening_SNR = getSNR(originalImage, gaussianNoise_10_closingThenOpening_Image)
    gaussianNoise_30_closingThenOpening_SNR = getSNR(originalImage, gaussianNoise_30_closingThenOpening_Image)
    saltAndPepper_0_10_closingThenOpening_SNR = getSNR(originalImage, saltAndPepper_0_10_closingThenOpening_Image)
    saltAndPepper_0_05_closingThenOpening_SNR = getSNR(originalImage, saltAndPepper_0_05_closingThenOpening_Image)

    file = open("SNR.txt", "w")
    file.write("gaussianNoise_10_SNR: " + str(gaussianNoise_10_SNR) + '\n')
    file.write("gaussianNoise_30_SNR: " + str(gaussianNoise_30_SNR) + '\n')
    file.write("saltAndPepper_0_10_SNR: " + str(saltAndPepper_0_10_SNR) + '\n')
    file.write("saltAndPepper_0_05_SNR: " + str(saltAndPepper_0_05_SNR) + '\n')

    file.write("gaussianNoise_10_box_3x3_SNR: " + str(gaussianNoise_10_box_3x3_SNR) + '\n')
    file.write("gaussianNoise_30_box_3x3_SNR: " + str(gaussianNoise_30_box_3x3_SNR) + '\n')
    file.write("saltAndPepper_0_10_box_3x3_SNR: " + str(saltAndPepper_0_10_box_3x3_SNR) + '\n')
    file.write("saltAndPepper_0_05_box_3x3_SNR: " + str(saltAndPepper_0_05_box_3x3_SNR) + '\n')
    file.write("gaussianNoise_10_box_5x5_SNR: " + str(gaussianNoise_10_box_5x5_SNR) + '\n')
    file.write("gaussianNoise_30_box_5x5_SNR: " + str(gaussianNoise_30_box_5x5_SNR) + '\n')
    file.write("saltAndPepper_0_10_box_5x5_SNR: " + str(saltAndPepper_0_10_box_5x5_SNR) + '\n')
    file.write("saltAndPepper_0_05_box_5x5_SNR: " + str(saltAndPepper_0_05_box_5x5_SNR) + '\n')

    file.write("gaussianNoise_10_median_3x3_SNR: " + str(gaussianNoise_10_median_3x3_SNR) + '\n')
    file.write("gaussianNoise_30_median_3x3_SNR: " + str(gaussianNoise_30_median_3x3_SNR) + '\n')
    file.write("saltAndPepper_0_10_median_3x3_SNR: " + str(saltAndPepper_0_10_median_3x3_SNR) + '\n')
    file.write("saltAndPepper_0_05_median_3x3_SNR: " + str(saltAndPepper_0_05_median_3x3_SNR) + '\n')
    file.write("gaussianNoise_10_median_5x5_SNR: " + str(gaussianNoise_10_median_5x5_SNR) + '\n')
    file.write("gaussianNoise_30_median_5x5_SNR: " + str(gaussianNoise_30_median_5x5_SNR) + '\n')
    file.write("saltAndPepper_0_10_median_5x5_SNR: " + str(saltAndPepper_0_10_median_5x5_SNR) + '\n')
    file.write("saltAndPepper_0_05_median_5x5_SNR: " + str(saltAndPepper_0_05_median_5x5_SNR) + '\n')
    
    file.write("gaussianNoise_10_openingThenClosing_SNR: " + str(gaussianNoise_10_openingThenClosing_SNR) + '\n')
    file.write("gaussianNoise_30_openingThenClosing_SNR: " + str(gaussianNoise_30_openingThenClosing_SNR) + '\n')
    file.write("saltAndPepper_0_10_openingThenClosing_SNR: " + str(saltAndPepper_0_10_openingThenClosing_SNR) + '\n')
    file.write("saltAndPepper_0_05_openingThenClosing_SNR: " + str(saltAndPepper_0_05_openingThenClosing_SNR) + '\n')

    file.write("gaussianNoise_10_closingThenOpening_SNR: " + str(gaussianNoise_10_closingThenOpening_SNR) + '\n')
    file.write("gaussianNoise_30_closingThenOpening_SNR: " + str(gaussianNoise_30_closingThenOpening_SNR) + '\n')
    file.write("saltAndPepper_0_10_closingThenOpening_SNR: " + str(saltAndPepper_0_10_closingThenOpening_SNR) + '\n')
    file.write("saltAndPepper_0_05_closingThenOpening_SNR: " + str(saltAndPepper_0_05_closingThenOpening_SNR) + '\n')