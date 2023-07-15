import json
import os.path
from fake_useragent import UserAgent
import requests
import shapefile
import shutil

headers = {'User-Agent': UserAgent().Chrome}


def get_url(file_path):
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as f:
            content_dict = json.loads(f.read())
        try:
            ref_str = content_dict['dct_references_s']
            ref_dict = json.loads(ref_str)
            url = ref_dict['http://schema.org/downloadUrl']
        except Exception as e:
            print('get url failed')
            url = None
        if not isinstance(url, str):
            return None
        return url
    else:
        print('not a file')
        return None


def get_mapping_list(dir_path):
    id_list = os.listdir(dir_path)
    print(id_list)
    id_url_mapping_list = []
    for id in id_list:
        file_path = dir_path + '\\' + id
        name = id.split('.')[0]
        url = get_url(file_path)
        if url is not None:
            list_item = {'id': name, 'url': url}
            id_url_mapping_list.append(list_item)
    return id_url_mapping_list


def download_dataset(name, dir_path, download_path, url):
    is_downloaded = True
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        src_path = download_path + r'.json'
        dst_path = download_path
        shutil.copy(src_path, dst_path)
        is_downloaded = False
    # for file in os.listdir(download_path):
    #     if file.endswith('zip'):
    #         is_downloaded = True
    #         break
    if not is_downloaded:
        # res = requests.get(url, headers=headers)
        res_headers = requests.get(url, headers=headers, verify=False).headers
        max_bytes = 100000000
        content_bytes = res_headers.get('Content-Length')
        if content_bytes is not None and int(content_bytes) < max_bytes:
            res_content = requests.get(url, headers=headers, verify=False).content
            zip_file_path = download_path + '\\' + name + r'.zip'
            with open(zip_file_path, 'wb') as f:
                f.write(res_content)
            parse_flag = parse_shapefile(download_path, zip_file_path)
            return parse_flag
        print('download url failed')
        return False
    return True


def parse_shapefile(unzip_path, zip_file_path):
    try:
        sf = shapefile.Reader(zip_file_path)
    except Exception as e:
        print(e)
        print('read shapefile failed')
        return False
    info_path = unzip_path + r'\info.json'
    data_path = unzip_path + r'\data.json'
    with open(info_path, 'w+') as f:
        try:
            li = []
            for i in sf.bbox:
                li.append(i)
            dic = {'type': sf.shapeTypeName, 'count': len(sf.shapes()), 'bbox': li}
            f.write(json.dumps(dic))
        except Exception as e:
            print(e)
            print('get info failed')
            return False
    with open(data_path, 'w+') as f:
        try:
            f.write(json.dumps(sf.__geo_interface__))
        except Exception as e:
            print(e)
            print('get data failed')
            return False
    return True


if __name__ == '__main__':
    root_path = r'D:\Projects\GBFS_Spider\umn-dataset'
    total_cnt = 0
    success_cnt = 0
    for dir_name in os.listdir(root_path):
        dir_path = root_path + '\\' + dir_name
        id_url_mapping_list = get_mapping_list(dir_path)
        length = len(id_url_mapping_list)
        print(length)
        cnt = 0
        for item in id_url_mapping_list:
            flag = download_dataset(item['id'], dir_path, dir_path + '\\' + item['id'], item['url'])
            if flag:
                print('[' + str(cnt) + '/' + str(length) + '] dataset ' + item['id'] + ' DONE')
                success_cnt += 1
            else:
                print('[' + str(cnt) + '/' + str(length) + '] dataset ' + item['id'] + ' FAILED')
            cnt += 1
            total_cnt += 1
        print('directory ' + dir_name + ' DONE')
        print('< ' + str(success_cnt) + '/' + str(cnt) + ' >')
    print('DONE')
    print('<< ' + str(success_cnt) + '/' + str(total_cnt) + ' >>')
