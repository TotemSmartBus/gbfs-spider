import csv
import json
import os
import shutil
from pathlib import Path

# 1. 遍历所有的最小一级目录
# 2. 对每个最小一级目录，查询其下的metadata文件，确定所属地区，再查询其下的data文件，过滤掉文件数据量过大或数值不规范的
# 3. 建立所属地区的目录，将过滤出来的文件夹复制到该目录下

base_dir_path = Path(r'D:\Projects\GBFS_Spider\btaa-dataset-pure-data')
cnt = 0
copy_dir_path = Path(r'D:\Projects\GBFS_Spider\btaa-clean')


# place_dir_dict = dict


def scan_each_min_dir(root_dir_path):
    # 只遍历，业务封装起来，不写在这个函数里
    for dir_path_name in os.listdir(root_dir_path):
        dir_path = os.path.join(root_dir_path, dir_path_name)
        if os.path.isfile(dir_path):
            if dir_path_name.endswith('.csv'):
                move_data(dir_path)
            # scan_min_dir(os.path.dirname(dir_path))
            # break
        else:
            scan_each_min_dir(dir_path)


def scan_min_dir(root_dir_path):
    global cnt
    # global place_dir_dict
    print(root_dir_path)
    # cnt += 1
    #     1. 判断是否有一个data文件，一个metadata文件
    data_file = None
    metadata_file = None
    for file_name in os.listdir(root_dir_path):
        if str(file_name).endswith('.csv'):
            data_file = os.path.join(root_dir_path, file_name)
        elif str(file_name).endswith('.json'):
            metadata_file = os.path.join(root_dir_path, file_name)

    if os.path.basename(data_file)[0].upper() < 'M':
        print('already scan')
        return

    with open(data_file, 'r') as f:
        f_csv = list(csv.reader(f))
        if len(f_csv) > 1:
            first_row = f_csv[1]
            print(first_row)
        else:
            return
    if float(first_row[0]) < 180 and float(first_row[1]) < 90 and len(f_csv) < 50000:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            if 'Place' in content:
                place_content = content['Place']
                print(place_content)
            else:
                return
        place = str(place_content).split('--')[0]
        place_dir = os.path.join(r'D:\Projects\GBFS_Spider\btaa-dataset-clean', place)
        if not os.path.exists(place_dir):
            os.mkdir(place_dir)
            # place_dir_dict[place] = str(place_dir)
        new_dir_path = os.path.join(place_dir, os.path.basename(data_file)[0: -4])
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            try:
                shutil.copy(data_file, new_dir_path)
                shutil.copy(metadata_file, new_dir_path)
            except Exception as e:
                print(e)
        cnt += 1
    else:
        return


def move_data(file_path):
    global cnt
    print(file_path)
    with open(file_path, 'r') as f:
        f_csv = list(csv.reader(f))
    if len(f_csv) > 1:
        first_row = f_csv[1]
        print(first_row)
    else:
        return
    if len(f_csv) < 5 or len(f_csv) > 300000 or float(first_row[0]) < -180 or float(first_row[0]) > 180 or float(
            first_row[1]) < -180 or float(first_row[1]) > 180:
        return
    try:
        shutil.copy(file_path, copy_dir_path)
    except Exception as e:
        print(e)
    print(cnt)
    cnt += 1


if __name__ == '__main__':
    scan_each_min_dir(base_dir_path)
    print(cnt)
    # s = 'aaa-bbb'
    # print(s.split('--'))
    # fake_path = Path(r'D:\Projects\GBFS_Spider\btaa-dataset\111')
    # print(os.path.exists(fake_path))
    # print('2aAA'.lower() > '100Bbb'.lower())
    # print('a2AA'.lower())
    # print('2'.lower())
