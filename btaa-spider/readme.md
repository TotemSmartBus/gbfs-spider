# 基于https://geo.btaa.org/网址的爬虫
该爬虫程序针对<https://geo.btaa.org/>中的datasets类型文件进行爬取，并生成对应的元数据(metadata)方便管理。

## 运行方法
- 修改`root_dir_path`变量为本地某目录，用来存放爬取下来的数据集文件。
- 进入项目根目录，执行`python btaa-spider\main.py`，进行爬取。