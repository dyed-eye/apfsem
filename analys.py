import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import statistics


normal_data_a = np.random.normal(size = 1000, loc = 100, scale = 10)
normal_data_b = np.random.normal(size = 1000, loc = 100, scale = 15)
array_of_size = []
for i in range(0,1000):
    array_of_size.append([normal_data_a[i],normal_data_b[i]])


def length_distribution(array_of_size):
    sns.set(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1)
    leight = []
    for i in range(0, len(array_of_size)):
        leight.append(max(array_of_size[i]))
    ax=sns.histplot(data=array_of_size, x=leight, color="darkred", alpha = 0.7, bins = 100, binwidth = 1)
    ax.set_xlabel("leight")
    ax.set_ylabel("count")
    plt.title(r"the number of crystals of a given length")
    plt.savefig(os.path.join('C:/git/проект/apfsem/res','диаграмма распределение длин кристаллов.png'), dpi=300)
    plt.show()


length_distribution(array_of_size)
