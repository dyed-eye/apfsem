import cv2 as cv
import numpy as np


def evaluate(grain_size):

    def algorithm(img):
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thr_img = cv.adaptiveThreshold(gray_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 19, 2)
        ret, thr_img = cv.threshold(thr_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        contours, hierarchy = cv.findContours(thr_img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    img = cv.imread('res/cached_image.png')

    contours, hierarchy = algorithm(img)
    print('I found ' + str(len(contours)) + ' contours')

    cv.drawContours(img, contours, -1, (50, 50, 255), 2, cv.LINE_AA, hierarchy, 1)
    # -1 is below zero so all the contours will be drawn
    # color is BGR tuple

    # cv.imwrite('res/cached_image.png', img)


def manual(median_blur_size=0, gaus_thresh=False, pixel_block=0, sens=0, contrast=False, clip_limit=0, tile_grid_size=0,
           line_thickness=10):
    img = cv.imread('res/cached_image.png')
    if median_blur_size > 0:
        img = cv.medianBlur(img, median_blur_size)
    if contrast:
        clahe = cv.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
        lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv.split(lab)  # split on 3 different channels
        l2 = clahe.apply(l)  # apply CLAHE to the L-channel
        lab = cv.merge((l2, a, b))  # merge channels
        img = cv.cvtColor(lab, cv.COLOR_LAB2BGR)  # convert from LAB to BGR
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if gaus_thresh:
        th = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, pixel_block, sens)
    else:
        th = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, pixel_block, sens)
    ret, th = cv.threshold(th, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    contours, hierarchy = cv.findContours(th, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, (20, 20, 255), line_thickness, cv.LINE_AA, hierarchy, 1)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    rows_rgb, cols_rgb, channels = img.shape
    rows_gray, cols_gray = img_gray.shape
    cols_comb = max(cols_rgb, cols_gray)
    rows_comb = rows_rgb + rows_gray
    comb = np.zeros(shape=(rows_comb, cols_comb, channels), dtype=np.uint8)
    comb[:rows_rgb, :cols_rgb] = img
    comb[rows_rgb:, :cols_gray] = img_gray[:, :, None]
    cv.imwrite('res/cached_cached_image.png', comb)

    return str(len(contours))
