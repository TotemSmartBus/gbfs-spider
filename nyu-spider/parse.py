import json
import os

import shapefile


cnt = 0


def parse_shapefile(dir, file) -> bool:
    global cnt
    print(file)
    file_name = os.path.basename(file).split('.')[0]
    try:
        sf = shapefile.Reader(file)
    except Exception as e:
        print(e)
        print('file' + file_name + ' decode fails')
        return False
    with open(dir + '/' + file_name + '_info.json', 'w+') as f:
        try:
            li = []
            for i in sf.bbox:
                li.append(i)
            dic = {'type': sf.shapeTypeName, 'count': len(sf.shapes()), 'bbox': li}
        # print(type(list))
            f.write(json.dumps(dic))
        except Exception as e:
            print(e)
            print('file ' + file_name + ' decode fails')
            return False
    with open(dir + '/' + file_name + '_data.json', 'w+') as f:
        try:
            f.write(json.dumps(sf.__geo_interface__))
        except Exception as e:
            print(e)
            print('file ' + file_name + ' decode fails')
            return False
    print('file ' + file_name + ' decode success')
    cnt += 1
    print(cnt)
    return True


def test():
    dir = './datasets/3/38/76/'
    # file = os.path.join(dir, 'nyu_2451_41639.zip/nycgwi_17b/nycgwi.shp')
    file = dir + 'nyu_2451_33876/nyu-NationalJewishPopulationMapbyCounty/nyu-NationalJewishPopulationMapbyCounty.shp'
    print(os.path.isfile(file))
    if os.path.exists(file):
        flag = parse_shapefile(dir, file)
        if flag:
            print('success')
    else:
        print('error')


def traverse_paths():
    n = 0
    for dir_path, dir_names, file_names in os.walk('./datasets'):
        # if os.path.exists(dir_path + '\\' + 'geoblacklight.json'):
        #     print(dir_path + '\\' + 'geoblacklight.json')
        #     n += 1
        for file in file_names:
            if file.endswith('.zip'):
                # print(dir_path + '\\' + file)
                n += 1
                traverse_datasets(dir_path, dir_path)
        # if dir_path.endswith('.zip'):
        #     new_path = dir_path[:-4]
        #     print(dir_path)
            # os.rename(dir_path, new_path)
            # traverse_datasets(dir_path)
    print(n)


def traverse_datasets(base_dir, dir):
    global cnt
    for child_dir in os.listdir(dir):
        dir_path = dir + '/' + child_dir
        if os.path.isfile(dir_path):
            if dir_path.endswith('_info.json'):
                print('file already exists')
                cnt += 1
                break
            if dir_path.endswith('.shp'):
                parse_shapefile(base_dir, dir_path)
        if os.path.isdir(dir_path):
            traverse_datasets(base_dir, dir_path)
    # for dir_path, dir_names, file_names in os.walk(dir):
    #     for file in file_names:
    #         if file.endswith('.shp'):
    #             print(dir)
    #             parse_shapefile(dir, file)


if __name__ == '__main__':
    traverse_paths()
    print(cnt)
    # test()
