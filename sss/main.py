import csv
import os


def split_csv(filename):
    data = {}
    directory = os.path.dirname(filename)
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # 读取表头
        for row in reader:
            key = row[1]  # 第二列作为分类依据
            if key not in data:
                data[key] = []
            data[key].append(row)

    # base_name = os.path.splitext(filename)[0]
    base_name = os.path.splitext(os.path.basename(filename))[0]
    for key, rows in data.items():
        # output_file = f"{base_name}_{key}.csv"
        output_file = os.path.join(directory, f"{base_name}_{key}.csv")
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # 写入表头
            writer.writerows(rows)  # 写入对应分类的行


# 示例调用
split_csv(r"C:\Users\12400\Desktop\水生所\水体理化指标.csv")
