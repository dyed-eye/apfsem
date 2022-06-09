import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import statistics
import scipy
import dataframe_image as dfi
from pandas.plotting import table
from matplotlib.pyplot import figure

normal_data_a = np.random.normal(size = 50, loc = 100, scale = 10)
normal_data_b = np.random.normal(size = 50, loc = 100, scale = 15)
array_of_size = []
for i in range(0,50):
    array_of_size.append([normal_data_a[i],normal_data_b[i]])

def length_distribution(array_of_size, fplot = 'False', ftable = 'False', fnorm = 'False'):
    leight = []
    width = []
    for i in range(0, len(array_of_size)):
        leight.append(max(array_of_size[i]))
        width.append(min(array_of_size[i]))
    if fplot == 'True':
        sns.set(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1)
        ax=sns.histplot(data=array_of_size, x=leight, color="darkred", alpha = 0.7, bins = 100, binwidth = 1) #график распределения
        ax.set_xlabel("leight")
        ax.set_ylabel("count")
        plt.title(r"the number of crystals of a given length")
        plt.savefig(os.path.join('C:/git/проект/apfsem/res','диаграмма распределение длин кристаллов.png'), dpi=300)
        plt.show()
    if ftable == 'True':
        figure(figsize=(3, 2), dpi=80)
        array_of_size1 = pd.DataFrame({'leight': leight , 'width': width}) # тупо анализ данных
        array_of_size2 = array_of_size1.describe().round(2)
        ax = plt.subplot(111, frame_on=False)  # no visible frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        colors = ['#56b5fd','#56b5fd','#56b5fd','#56b5fd','#56b5fd','#56b5fd','#56b5fd','#56b5fd']
        widths = [0.3,0.3]
        table(ax, array_of_size2, loc='center', cellLoc = 'center', rowColours=colors, colColours=['#56b5fd','#56b5fd'], colWidths=widths)
        plt.savefig(os.path.join('C:/git/проект/apfsem/res', 'analys_table.png'), dpi=300)
        plt.show()
    if fnorm == 'True':
        stat, p = scipy.stats.normaltest(leight)  # Критерий согласия Пирсона: проверка на нормальность данных
        print('Вычисленное значение статистики=%.3f, p-value=%.3f' % (stat, p))
        alpha = 0.05
        if p > alpha:
            print('Распределение имеет нормальный характер')
        else:
            print('Распределение ненормальное')

length_distribution(array_of_size)

