import numpy as np

# 原始数据集
data = np.array([1, 2, 3, 4, 5], dtype=np.float64)

# 添加椒盐噪声生成离群值
outliers = 2  # 离群值的数量
outlier_ratio = 0.1  # 离群值的比例
noise = np.random.choice([-1, 1], size=outliers, replace=True) * outlier_ratio
indices = np.random.choice(len(data), size=outliers, replace=False)
data[indices] += noise

print(data)
