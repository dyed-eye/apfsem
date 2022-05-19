import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def limits(img, accuracy):
    img_temp = img.copy()

    pixels = np.array(img_temp.reshape(-1, 3))
    '''v, vc = np.unique(pixels[:, 2], axis=0, return_counts=True)
    s, sc = np.unique(pixels[:, 1], axis=0, return_counts=True)'''
    h, hc = np.unique(pixels[:, 0], axis=0, return_counts=True)

    new_h = []
    amount = accuracy/100 * len(pixels)
    for i in range(len(h)):
        if hc[i] > amount:
            new_h.append(h[i])

    '''plt.plot(v, vc, 'r', label='Value', linewidth=1)
    plt.plot(s, sc, 'g', label='Saturation', linewidth=1)
    plt.plot(h, hc, 'b', label='Hue', linewidth=1)
    plt.legend()
    plt.savefig('res/cached_cached_image')'''

    return int(min(new_h)), int(max(new_h))

def automised(grain_size, accuracy):
    img = cv.imread('res/cached_image.png')
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    min_h, max_h = limits(img_hsv, accuracy)
    thresh = cv.inRange(img_hsv, (min_h, 0, 0), (max_h, 1e3, 1e3))

    cv.imwrite('res/cached_cached_image.png', thresh)

    return grain_size
