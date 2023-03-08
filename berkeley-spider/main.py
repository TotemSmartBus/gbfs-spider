# 1. GitHub上下载metadata目录
# 2. 读取每个metadata文件，解析出下载URL
# 3. 建立字典列表：[{id: "0c7w", url: "xxx"}, {id: "0d5g", url: "xxxx"}]
# 4. 下载URL并（解压）解析得到便于阅读的数据文件
import json
import os.path
from fake_useragent import UserAgent
import requests
from urllib3 import PoolManager
import shapefile


def get_url(file_path):
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as f:
            content_dict = json.loads(f.read())
        ref_str = content_dict['dct_references_s']
        ref_dict = json.loads(ref_str)
        # print(type(ref_dict))
        url = ref_dict['http://schema.org/downloadUrl']
        # print(url)
        return url
    else:
        print('not a file!')
        return ''


def get_mapping_list(root_dir_path):
    id_list = os.listdir(root_dir_path)
    print(id_list)
    id_url_mapping_list = []
    for id in id_list:
        file_path = os.path.join(root_dir_path, id)
        url = get_url(file_path + r'\geoblacklight.json')
        if url is not None:
            list_item = {'id': id, 'url': url}
            id_url_mapping_list.append(list_item)
    return id_url_mapping_list


def download_dataset(download_path, url, headers):
    if os.path.exists(download_path + r'\info.json'):
        return True
    # pool = PoolManager()
    try:
        # res = pool.request("GET", url, headers=headers)
        res = requests.get(url, headers=headers).headers
    except Exception as e:
        print(e)
        return False
    max_bytes = 50000000
    content_bytes = res.get('Content-Length')
    # print(content_bytes)
    if content_bytes is not None and int(content_bytes) < max_bytes:
        data = requests.get(url, headers=headers).content
        # print(type(data))
        # print(len(data))
        with open(download_path + r'\data.zip', 'wb') as f:
            f.write(data)
        parse_flag = parse_shapefile(download_path)
        return parse_flag
    return False


def parse_shapefile(unzip_path):
    zip_file_path = unzip_path + r'\data.zip'
    if os.path.isfile(zip_file_path) and os.path.isdir(unzip_path):
        try:
            sf = shapefile.Reader(zip_file_path)
        except Exception as e:
            print(e)
            return False
        with open(unzip_path + r'\info.json', 'w+') as f:
            try:
                li = []
                for i in sf.bbox:
                    li.append(i)
                dic = {'type': sf.shapeTypeName, 'count': len(sf.shapes()), 'bbox': li}
                f.write(json.dumps(dic))
            except Exception as e:
                print(e)
                return False
        with open(unzip_path + r'\data.json', 'w+') as f:
            try:
                f.write(json.dumps(sf.__geo_interface__))
            except Exception as e:
                print(e)
                return False
        return True
    return False


if __name__ == '__main__':
    # file_path = os.path.join(os.path.dirname(r"D:\Projects\GBFS_Spider\berkeley-dataset\0c7w"), 'geoblacklight.json')
    # file_path = r'D:\Projects\GBFS_Spider\berkeley-dataset\0c7w\geoblacklight.json'
    # get_url(file_path)
    # root_dir_path = r'D:\Projects\GBFS_Spider\berkeley-dataset'
    # get_mapping_list(root_dir_path)
    headers = {'User-Agent': UserAgent().Chrome}
    # download_dataset(r'D:\Projects\GBFS_Spider\berkeley-dataset\0c7w',
    #                  'https://spatial.lib.berkeley.edu/public/ark28722-s70c7w/data.zip', headers)
    root_dir_path = r'D:\Projects\GBFS_Spider\berkeley-dataset'
    id_url_mapping_list = get_mapping_list(root_dir_path)
    print(len(id_url_mapping_list))
    cnt = 0
    for item in id_url_mapping_list:
        download_flag = download_dataset(root_dir_path + '\\' + item['id'], item['url'], headers)
        if download_flag:
            print('dataset ' + item['id'] + ' downloaded and parsed success')
            cnt += 1
        else:
            print('dataset ' + item['id'] + ' downloaded and parsed failed')
    print('download and parse finished')
    print(cnt)
