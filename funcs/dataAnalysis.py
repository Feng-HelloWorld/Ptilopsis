import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def drawHistogram(data:list):
    try:
        sns.set()                                   #设置seaborn默认格式
        from matplotlib.font_manager import FontProperties   #显示中文，并指定字体
        myfont=FontProperties(fname=r'./data/fonts/pf-light.ttf',size=14)
        sns.set(font=myfont.get_name())
        plt.rcParams['axes.unicode_minus']=False      #显示负号
        plt.rcParams['figure.figsize'] = (7, 5)    #设定图片大小
        f = plt.figure()                            #确定画布
        f.add_subplot(1,1,1)
        sns.distplot(data, kde=False)                 #绘制频数直方图
        plt.xticks(fontsize=16)                    #设置x轴刻度值的字体大小
        plt.yticks(fontsize=16)                   #设置y轴刻度值的字体大小
        file_path = './data/temp/histogram.jpg'
        plt.savefig(file_path)
        return file_path
    except:
        raise RuntimeError