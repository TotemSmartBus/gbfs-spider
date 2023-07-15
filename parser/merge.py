import pandas as pd
import os

path = r"D:\Projects\Spadas\spadas_5-16\spadas_5-16\spadas\dataset\hz"  # csv_folder 为要处理的目录名

all_files = os.listdir(path)  # 获取目录下所有文件名
csv_files = [file for file in all_files if file.endswith('.csv')]  # 过滤出 CSV 文件

dfs = []  # 定义一个空列表，用于存放读取的数据
for file in csv_files:
    filepath = os.path.join(path, file)  # 获得文件的全路径
    df = pd.read_csv(filepath, encoding='gbk')  # 读取 csv 文件
    dfs.append(df)

merged_df = pd.concat(dfs)  # 合并所有的 DataFrame

new_filepath = r"D:\Projects\Spadas\spadas_5-16\spadas_5-16\spadas\dataset\hz\together.csv"
merged_df.to_csv(new_filepath, index=False, encoding='gbk')
