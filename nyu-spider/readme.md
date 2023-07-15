# 基于OpenGeoMetadata/edu.nyu仓库的爬虫
该爬虫程序针对OpenGeoMetadata/edu.nyu仓库中的元数据(Metadata)来爬取下载对应的空间数据集，并对其中的Shapefile类型文件进行解析得到结构化、易读的数据文件。

## 运行方法
- 先下载<https://github.com/OpenGeoMetadata/edu.nyu>仓库的源码，将`handle/2451`文件夹复制到`nyu-spider`目录下，命名为`datasets`。

- 进入对应根目录，执行`python nyu-spider\main.py`，下载数据集文件。

- 执行`python nyu-spider\parse.py`，解析Shapefile文件。

- 执行`python nyu-spider\wrap.py`，将解析出来的文件整理到统一的`data/`目录下。