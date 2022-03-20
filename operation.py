import cv2 as cv


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

    cv.imwrite('res/cached_image.png', img)
