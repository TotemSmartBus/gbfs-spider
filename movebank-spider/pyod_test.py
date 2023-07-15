import os
import pandas as pd
from pyod.models.iforest import IForest
from pyod.models.suod import SUOD
from pyod.models.inne import INNE
import time

# 目录路径
directory = r'D:\Projects\GBFS_Spider\real-data'

# 开始计时
begin_time = time.time()
cost_time = 0

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # 构建完整文件路径
        file_path = os.path.join(directory, filename)

        # 读取 CSV 文件并将数据读取为数组
        data = pd.read_csv(file_path)
        # 假设数据在 CSV 文件中的列名为 'feature1' 和 'feature2'
        X = data[['lng', 'lat']].values

        start_time = time.time()

        # 创建模型
        model = SUOD()

        # 拟合模型并进行预测
        model.fit(X)

        # 预测离群值得分
        y_scores = model.decision_function(X)

        # 预测离群值标签
        y_pred = model.predict(X)

        end_time = time.time()

        # 输出结果
        print("文件名：", filename)
        print("预测得分：", y_scores)
        print("预测标签：", y_pred)
        print("该文件预测用时：", end_time - start_time)
        cost_time += end_time - start_time
        print("总预测用时：", cost_time)

# 结束计时并计算总时间
finish_time = time.time()
total_time = begin_time - finish_time
print("程序运行总时间：", total_time, "秒")
print("算法运行总时间: ", cost_time, "秒")
