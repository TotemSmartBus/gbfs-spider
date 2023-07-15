# 提取Shapefile文件中的点数据形成点集文件
import csv
import inspect
import os
import time
from pathlib import Path
import pandas as pd
import shapefile
import numpy as np

# root_dir_path = r'D:\Projects\GBFS_Spider\test\34698'
# root_dir_path = Path(r'D:\Projects\GBFS_Spider\btaa-dataset')
# root_dir_path = r'D:\Projects\GBFS_Spider\btaa-dataset'
# root_dir_path = r'D:\Projects\GBFS_Spider\nyu_tmp'
root_dir_path = r'D:\Projects\GBFS_Spider\umn-dataset\05d-03'
# root_dir_path = r'D:\Projects\GBFS_Spider\btaa-dataset\BC-GIS--climateactionplan-storm-drains-int-histstreams'
# dataset_cnt = 0
row_cnt = 0
one_root_path = Path(r'D:\Downloads')


def read(dir_name, my_set):
    global row_cnt
    dir_path = os.path.join(root_dir_path, dir_name)
    file_list = os.listdir(dir_path)
    zip_file_path = None
    for file_name in file_list:
        if str(file_name).endswith('.csv'):
            print('already parsed')
            return True
    for file_name in os.listdir(dir_path):
        print(file_name)
        # if file_name.endswith('.zip.zip'):
        #     file_path = os.path.join(dir_path, file_name)
        #     os.rename(file_path, file_path[0: -4])
        #     zip_file = file_path[0: -4]
        #     zip_file_path = os.path.join(dir_path, zip_file)
        #     break
        if str(file_name).endswith('.zip'):
            zip_file_path = os.path.join(dir_path, file_name)
            # print(zip_file_path)
            break
    try:
        sf = shapefile.Reader(zip_file_path)
        shape_list = sf.shapes()
    except Exception as e:
        print(e)
        # print('parse ' + dir_name + ' failed')
        return False

    # print(type(shape_list))
    # print(shape_list)
    # print(len(shape_list))
    # cnt = 0
    data = []

    # if len(shape_list) > 10000:
    #     print('file contains ' + str(len(shape_list)) + 'shapes')
    #     print('file too large')
    #     return False

    write_dir_path = r'D:\Projects\GBFS_Spider\umn-clean'
    first_data = shape_list[0].points[0][0]

    if first_data < -180 or first_data > 180:
        print('data not good')
        return False
    if first_data in my_set:
        print('duplicated data')
        return False
    my_set.add(first_data)

    for i in range(len(shape_list)):
        # data = []
        # if len(shape_list[i].points) > 50000:
        #     print('too much points')
        #     break
        for pt in shape_list[i].points:
            # if pt[0] < -180 or pt[0] > 180:
            #     print('data not good')
            #     return False
            a = []
            for val in pt:
                a.append(val)
            data.append(a)
        # if len(data) == 0:
        #     print('bad data')
        #     break
    partition_and_write(dir_name, write_dir_path, data)
    # if not flag:
    #     print('write fail')
    #     break
    row_cnt += len(data)
    # print(len(shape_list[i].points))
    # cnt += len(shape_list[i].points)
    # print()
    # print(shape_list[1].points)
    # print(cnt)
    # print(type(data[10000]))
    # write_dir_path = r'D:\Projects\GBFS_Spider\umn-clean'
    # flag = write(dir_name, write_dir_path, data)
    # if not flag:
    #     return False
    # print(len(data))
    # row_cnt += len(data)
    return True
    # print('parse ' + dir_name + ' done')


def partition_and_write(dir_name, dir_path, data):
    a = np.array(data)
    print(len(a))
    print(type(a))
    part_size = 10000
    part_cnt = int(len(a) / part_size)
    for i in range(part_cnt):
        b = a[part_size * i: part_size * (i + 1)]
        part_name = dir_name + '_' + str(i)
        write(part_name, dir_path, b)
    if len(a) / part_size > 0:
        b = a[part_cnt * part_size:]
        part_name = dir_name + '_' + str(part_cnt)
        write(part_name, dir_path, b)


def write(dir_name, dir_path, data):
    data_file_name = dir_name + '.csv'
    # a = np.array(data)
    data_file_path = os.path.join(dir_path, data_file_name)
    # print(type(df))
    try:
        with open(data_file_path, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(['lng', 'lat'])
            csv_writer.writerows(data)
    except Exception as e:
        print(e)
        return False
    return True


def parse_all():
    dataset_cnt = 0
    id = 0
    print(root_dir_path)
    dir_list = os.listdir(root_dir_path)
    my_set = set()
    for dir_item in dir_list:
        dir_path = os.path.join(root_dir_path, dir_item)
        print(dir_path)
        # time.sleep(1)
        flag = read(dir_item, my_set)
        if flag:
            dataset_cnt += 1
            print(str(id) + ': parse ' + str(dir_item) + ' done [' + str(dataset_cnt) + ']')
        else:
            print(str(id) + ': parse ' + str(dir_item) + ' failed [' + str(dataset_cnt) + ']')
        id += 1
    print('totally ' + str(dataset_cnt) + ' datasets and ' + str(row_cnt) + ' rows')


def test():
    path = Path(
        r'D:\Projects\GBFS_Spider\berkeley-dataset\567q\data.zip')
    sf = shapefile.Reader(path)
    shapes = sf.shapes()
    print(shapes)
    # print(len(sf.fields))
    # print(sf.records())
    shape = sf.shape(10)
    print(shape.points)


def rename():
    path = Path(r'D:\Projects\Spadas\spadas_5-16\spadas_5-16\spadas\dataset\Maryland')
    for file_name in os.listdir(path):
        if str(file_name).startswith('maryland--'):
            file = os.path.join(path, file_name)
            new_file_name = file_name[10:]
            new_file = os.path.join(path, new_file_name)
            print(new_file)
            os.rename(file, new_file)


# 帮师姐处理一个能做实验的bus lines数据集
def parse_one_dataset(zip_file_name):
    zip_file_path = os.path.join(one_root_path, zip_file_name)
    print(zip_file_path)
    print(os.path.exists(zip_file_path))
    path = Path(
        r'D:\app\wechat\data\WeChat Files\wxid_ocz68atk2uy722\FileStorage\File\2023-04\Metro_Lines_in_DC\Metro_Lines_in_DC.shp')
    sf = shapefile.Reader(path)
    shape_list = sf.shapes()
    # data = []
    for i in range(len(shape_list)):
        data = []
        for pt in shape_list[i].points:
            data.append(pt)
        file_name = 'data_' + str(i)
        file_path = Path(r'D:\Projects\Spadas\spadas_5-16\spadas_5-16\spadas\dataset\bus_lines')
        write(file_name, file_path, data)
        print(str(i) + 'finished')


if __name__ == '__main__':
    # read()
    parse_all()
    # test()
    # rename()
    # parse_one_dataset('Metro_Lines_in_DC.zip')
