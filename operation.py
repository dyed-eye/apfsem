import cv2 as cv
import numpy as np
from colorama import Fore, Style

import analys as analys


def combine(img, img_gray):
    rows_rgb, cols_rgb, channels = img.shape
    rows_gray, cols_gray = img_gray.shape
    cols_comb = max(cols_rgb, cols_gray)
    rows_comb = rows_rgb + rows_gray
    comb = np.zeros(shape=(rows_comb, cols_comb, channels), dtype=np.uint8)
    comb[:rows_rgb, :cols_rgb] = img
    comb[rows_rgb:, :cols_gray] = img_gray[:, :, None]
    return comb


def limits(img, accuracy):
    img_temp = img.copy()
    pixels = np.array(img_temp.reshape(-1, 3))
    pixels = pixels[pixels[:, 2].argsort()]
    h, hc = np.unique(pixels[:, 0], axis=0, return_counts=True)
    m = max(hc)
    i = np.where(hc == m)[0]
    amount = accuracy/100 * m
    j = 1
    while i - j >= 0:
        if hc[i - j] > amount:
            j += 1
        elif hc[i - j] - amount <= 1e-4:
            beg = h[i - j]
            break
        else:
            beg = (h[i - j] + h[i - j + 1]) / 2
            break
    if i - j < 0:
        print(f"{Fore.RED}     (!)     Didn't reach the beginning!{Style.RESET_ALL}")
        beg = h[0]
    j = 1
    while i + j < len(h):
        if hc[i + j] > amount:
            j += 1
        elif hc[i + j] - amount <= 1e-4:
            end = h[i + j]
            break
        else:
            end = (h[i + j] + h[i + j - 1]) / 2
            break
    if i + j >= len(h):
        print(f"{Fore.RED}     (!)     Didn't reach the end!{Style.RESET_ALL}")
        end = h[-1]

    return int(beg), int(end)


def automised(grain_size, scale, accuracy):
    img = cv.imread('res/cached_image.png')
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    min_h, max_h = limits(img_hsv, accuracy)
    thresh = cv.inRange(img_hsv, (min_h, 0, 0), (max_h, 1e3, 1e3))
    thresh = cv.medianBlur(thresh, 3)
    thresh = cv.bitwise_not(thresh)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    perimeters = []
    boxes = []
    areas = []
    good = [] # at the moment we calculate only boxes which are easy to - straight rectangles
    for cnt in contours:
        if cv.contourArea(cnt) == 0:
            continue
        perimeters.append(cv.arcLength(cnt, True))
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        if cv.contourArea(box)/cv.contourArea(cnt) < 2:
            boxes.append(np.int0(box))
            areas.append(cv.contourArea(np.int0(box)))
            good.append(np.int0(box))
        else:
            epsilon = 0.005 * cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)
            boxes.append(approx)
            areas.append(cv.contourArea(approx))
    lengths = []
    for box in good:
        max_dim = 0
        for i in range(1, len(box)):
            if np.sqrt((int(box[i][0])-int(box[i-1][0])) ** 2 + (int(box[i][1])-int(box[i-1][1])) ** 2) > max_dim:
                max_dim = np.sqrt((int(box[i][0])-int(box[i-1][0])) ** 2 + (int(box[i][1])-int(box[i-1][1])) ** 2)
        lengths.append(max_dim * scale)

    # the possibility of choosing not all of the analytics functions will be available later
    return analys.length_distribution(lengths, grain_size, False, True, True)
