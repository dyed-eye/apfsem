import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import scipy
from pandas.plotting import table
from matplotlib.pyplot import figure
import cv2 as cv
import numpy as np


def combine(img, img2):
    rows_rgb, cols_rgb, channels = img.shape
    rows_gray, cols_gray, chan = img2.shape
    cols_comb = max(cols_rgb, cols_gray)
    rows_comb = rows_rgb + rows_gray
    comb = np.zeros(shape=(rows_comb, cols_comb, channels), dtype=np.uint8)
    comb[:rows_rgb, :cols_rgb] = img
    comb[rows_rgb:, :cols_gray] = img2
    return comb


def length_distribution(array_of_size, grain_size, fplot=False, ftable=False, fnorm=False):
    length = array_of_size
    img = np.array([])
    if fplot:
        arr = []
        for i in range(1, len(length) + 1):
            arr.append([i, length[i - 1]])
        sns.set(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1)
        ax = sns.histplot(data=array_of_size, x=length, color="darkred", alpha=0.7, bins=100,
                          binwidth=1)  # график распределения
        ax.set_xlabel("length")
        ax.set_ylabel("count")
        plt.title(r"the number of crystals of a given length")
        plt.axvline(x=grain_size, color='b')
        plt.savefig('res/cached_cached_image.png')
        img = cv.imread('res/cached_cached_image.png')
    if ftable:
        figure(figsize=(3, 2), dpi=80)
        array_of_size1 = pd.DataFrame({'length': length})  # тупо анализ данных
        array_of_size2 = array_of_size1.describe().round(2)
        ax = plt.subplot(111, frame_on=False)  # no visible frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        colors = ['#56b5fd', '#56b5fd', '#56b5fd', '#56b5fd', '#56b5fd', '#56b5fd', '#56b5fd', '#56b5fd']
        widths = [0.3]
        table(ax, array_of_size2, loc='center', cellLoc='center', rowColours=colors, colColours=['#56b5fd'],
              colWidths=widths)
        plt.savefig('res/cached_cached_image.png')
        plot = cv.imread('res/cached_cached_image.png')
        #img = combine(img, plot)
        cv.imwrite('res/cached_cached_image.png', plot)
    if fnorm:
        stat, p = scipy.stats.normaltest(length)  # Критерий согласия Пирсона: проверка на нормальность данных
        print('Вычисленное значение статистики=%.3f, p-value=%.3f' % (stat, p))
        alpha = 0.05
        return p > alpha  # True stands for normal


