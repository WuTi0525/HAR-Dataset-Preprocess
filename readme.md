## Human Activity Recogniton (HAR) 公开数据集预处理与网络搭建

### 包含数据集
* phyphox软件自采集excel数据
* Daily-and-Sports-Activities-dataset
* PAMAP2 dataset
* UCI-HAR dataset
* USC-HAD dataset
* UniMiB-SHAR dataset
* WISDM dataset
* OPPORTUNITY dataset (unfinished)


### 预处理代码运行样例
```
$ cd UniMiB-SHAR
$ python dataproc.py
```

### 预处理+模型训练代码运行样例
```
$ cd HAR-Dataset-Prerocess
$ python train.py --dataset uci --datadir ./UCI_HAR/UCI_HAR_Dataset --model resnet
```
