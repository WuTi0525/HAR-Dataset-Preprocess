import os
import numpy as np
import pandas as pd
'''
PAMAP2 数据集下载地址
http://archive.ics.uci.edu/ml/machine-learning-databases/00231/
将PAMAP2_Dataset.zip中的Protocol文件夹放到该目录下即可运行

WINDOW_SIZE=171 # int
OVERLAP_RATE=0 # float in [0，1）
SPLIT_RATE=(7,3) # tuple or list  

'''

def PAMAP(WINDOW_SIZE=171, OVERLAP_RATE=0, SPLIT_RATE=(7,3), dataset_dir='Protocol'):
    if not os.path.exists(dataset_dir):
        print('OPAMAP2 数据集下载地址\nhttp://archive.ics.uci.edu/ml/machine-learning-databases/00231/\n将“PAMAP2_Dataset.zip”中的“Protocol”文件夹放入【HAR-Dataset-Preprocess/PAMAP2】目录下即可运行\nps:【或者通过 --datadir 自行指定“Protocol”文件夹路径】')
        quit()
    xtrain, xtest, ytrain, ytest = [], [], [], [] # train-test-data
    category_dict = dict(zip([*range(12)], [1, 2, 3, 4, 5, 6, 7, 12, 13, 16, 17, 24])) #12分类所对应的实际label，对应readme.pdf

    def slide_window(array, windowsize, overlaprate, label, split_rate=(7, 3)):
        '''
        array: 2d-numpy数组
        windowsize: 窗口尺寸
        overlaprate: 重叠率
        label: array对应的标签
        split_rate: train-test数据量比例
        '''
        nonlocal xtrain, xtest, ytrain, ytest
        stride = int(windowsize * (1 - overlaprate)) # 计算stride
        times = (array.shape[0]-windowsize)//stride + 1 # 滑窗次数，同时也是滑窗后数据长度
        tempx = []
        for i in range(times):
            x = array[i*stride : i*stride+windowsize]
            tempx.append(x)
        np.random.shuffle(tempx) # shuffle
        # 切分数据集
        trainleng = int(times*split_rate[0]/sum(split_rate))
        xtrain += tempx[: trainleng]
        xtest += tempx[trainleng: ]
        ytrain += [label]*trainleng
        ytest += [label]*(times-trainleng)

    dir = dataset_dir
    filelist = os.listdir(dir)
    os.chdir(dir)
    for file in filelist:
        content = pd.read_csv(file, sep=' ', usecols=[1]+[*range(4,16)]+[*range(21,33)]+[*range(38,50)]) # 取出有效数据列, 第2列为label，5-16，22-33，39-50都是可使用的传感数据
        content = content.dropna(axis=0).to_numpy() # 删除含有nan的行
        
        data = content[:, 1:] # 数据 （n, 36)
        label = content[:, 0] # 标签

        data = data[label!=0] # 去除0类
        label = label[label!=0]
        
        # data, label = data[::2], label[::2] # 降采样1/2

        print("==================================================================\n         【Loading File: “%s”】\nX-data shape: %s    Y-data shape: %s"%(file, data.shape, label.shape))
        for i in range(12):
            true_label = category_dict[i]
            slide_window(data[label==true_label], WINDOW_SIZE, OVERLAP_RATE, i, SPLIT_RATE)
    os.chdir('../')
    print('==================================================================')
    xtrain = np.array(xtrain, dtype=np.float32)
    xtest = np.array(xtest, dtype=np.float32)
    ytrain = np.array(ytrain, np.int64)
    ytest = np.array(ytest, np.int64)
    print('\n---------------------------------------------------------------------------------------------------------------------\n')
    print('xtrain shape: %s\nxtest shape: %s\nytrain shape: %s\nytest shape: %s'%(xtrain.shape, xtest.shape, ytrain.shape, ytest.shape))
    return xtrain, xtest, ytrain, ytest


if __name__ == '__main__':
    PAMAP()
