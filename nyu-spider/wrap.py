# 遍历目录，找到含有'_data.json'的目录并访问xxx_data.json文件
# 若文件不为空则访问该目录下的geoblacklight.json文件，找到"dc_identifier_s"字段的属性的后缀数值
# 找到geoblacklight.json文件中的"layer_geom_type_s"字段的属性，给对应属性+1
# 将整个目录移到./data/xxxxx下，sum+1
import json
import os
import shutil

data_dir = './data/'
types = {}
cnt = 0


def find_dataset(base_dir):
    for child_dir in os.listdir(base_dir):
        child_path = base_dir + '/' + child_dir
        if os.path.isfile(child_path):
            if child_path.endswith('_data.json'):
                if os.path.getsize(child_path) > 0:
                    move_dataset(base_dir)
        if os.path.isdir(child_path):
            find_dataset(child_path)


# 可能存在目标文件夹已经存在的情况
def move_dataset(base_dir):
    global cnt
    flag = True
    # if base_dir.endswith('87'):
    #     print('!')
    for child_dir in os.listdir(base_dir):
        child_path = base_dir + '/' + child_dir
        if child_path.endswith('geoblacklight.json'):
            with open(child_path, encoding='utf-8') as f:
                dic = json.load(f)
                dataset_id = dic['dc_identifier_s'].split('/')[-1]
                new_dir = data_dir + dataset_id
                dataset_type = dic['layer_geom_type_s']
            if dataset_type in types.keys():
                types[dataset_type] += 1
            else:
                types[dataset_type] = 1
            if os.path.exists(new_dir):
                print('already move')
                flag = False
            else:
                os.makedirs(new_dir)
            break
    if flag:
        # print(cnt)
        cnt += 1
        for c_dir in os.listdir(base_dir):
            c_path = base_dir + '/' + c_dir
            if os.path.isfile(c_path):
                shutil.copy(c_path, new_dir)
        print(dataset_id + ' move success')


if __name__ == '__main__':
    find_dataset('./datasets')
    print(types)
    print(cnt)
