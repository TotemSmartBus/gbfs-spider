# 基于OpenGeoMetadata/edu.umn仓库的爬虫
该爬虫程序针对OpenGeoMetadata/edu.umn仓库中的元数据(Metadata)来爬取下载对应的空间数据集，并对其中的Shapefile类型文件进行解析得到结构化、易读的数据文件。

## 运行方法
- 先下载<https://github.com/OpenGeoMetadata/edu.umn>仓库的源码，将`metadata-1.0/Datasets/`文件夹复制到项目目录下，命名为`umn-dataset`(需要自己修改代码中的路径)。

- 进入对应根目录，执行`python umn-spider\main.py`，下载并解析得到数据集文件，在`umn-dataset`目录下可以看到。