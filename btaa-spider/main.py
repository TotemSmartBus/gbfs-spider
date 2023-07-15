# 1 起始页的全部页上的共计21788个URL爬下来（修改page的值）
# 2 对每个URL对应的页面：
#     2.1 查看有没有Original Shapefile下载链接选项，若没有则放弃该页面
#     2.2 下载Full Details下的文本，转化为字典，转化为json格式，写成文件
#     2.3 下载Original Shapefile对应的文件链接，找到id，建立对应的目录，将2.2和2.3生成的文件放入目录下
#     2.4 解析2.3生成的zip文件
import json
import os.path
import shutil
import time
from datetime import datetime

import requests
# import wget
import wget
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# headers = {'User-Agent': UserAgent().random}
from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout
from requests_html import HTMLSession

ua = UserAgent()
root_dir_path = r'D:\Projects\GBFS_Spider\btaa-dataset'
valid_cnt = 0
cnt = 0
# start_i = 1237
start_i = 1275
end_i = 1500
session = HTMLSession()


def download_everything():
    first_url = 'https://geo.btaa.org/?f%5Bgbl_resourceClass_sm%5D%5B%5D=Datasets'
    headers = {'User-Agent': ua.random}
    res = requests.get(first_url, headers=headers)
    text = res.text
    soup = BeautifulSoup(text, 'lxml')
    page_cnt_str = soup.select('.page-item')[-1].select('a')[0].text
    page_cnt = int(page_cnt_str.replace(',', ''))
    dataset_cnt_str = soup.select('.page-entries')[0].select('strong')[-1].text
    dataset_cnt = int(dataset_cnt_str.replace(',', ''))
    print('Totally ' + dataset_cnt_str + ' datasets')
    for i in range(start_i, end_i):
        page_url = first_url + '&page=' + str(i)
        download_one_page(page_url)
        print('page ' + str(i) + ' finished')
    print('download finished')
    print('<' + str(valid_cnt) + '/' + str(cnt) + '>')


def download_one_page(page_url):
    global valid_cnt
    global cnt
    headers = {'User-Agent': ua.random}
    res = requests.get(page_url, headers=headers)
    text = res.text
    soup = BeautifulSoup(text, 'lxml')
    dataset_list = soup.select('#documents > article > div > h3 > a')
    for item in dataset_list:
        dataset_url = 'https://geo.btaa.org/' + item['href']
        time.sleep(3)
        flag, name = download_one_dataset(dataset_url)
        cnt += 1
        if flag:
            valid_cnt += 1
            print('no.' + str(cnt - 1) + ': ' + name + ' download DONE! <' + str(valid_cnt) + '/' + str(cnt) + '>')
        else:
            print('no.' + str(cnt - 1) + ': ' + name + ' download FAILED! <' + str(valid_cnt) + '/' + str(cnt) + '>')


def download_one_dataset(dataset_url):
    headers = {'User-Agent': ua.random}
    try:
        res = requests.get(dataset_url, headers=headers)
    except Exception as e:
        print(e)
        print('get dataset page failed')
        return False, 'unknown'
    text = res.text
    soup = BeautifulSoup(text, 'lxml')
    download_content = soup.select('div.card.card-body > a')
    # print(download_content)
    if len(download_content) != 1:
        print('download url not found')
        return False, 'unknown'
    url = download_content[0]['href']
    print('download url = ' + url)

    if url.endswith('.zip'):
        name = url.split('/')[-1][0: -4].replace(':', '-').replace('/', '-').replace('|', '-').replace('?', '-') \
            .replace('*', '-').replace('>', '-').replace('<', '-')
    else:
        name = url.split('/')[-1].replace(':', '-').replace('/', '-').replace('|', '-').replace('?', '-') \
            .replace('*', '-').replace('>', '-').replace('<', '-')

    download_dir_path = root_dir_path + '\\' + name
    if os.path.exists(download_dir_path):
        print('download already done')
        return True, name

    # headers = {'User-Agent': ua.random}
    # print('get res:')
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # res_headers = requests.get(url, headers=headers, verify=False).headers
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # max_bytes = 100000000
    # content_bytes = res_headers.get('Content-Length')
    # if content_bytes is None or int(content_bytes) > max_bytes:
    #     print('download file too large')
    #     return False, name
    #
    # os.mkdir(download_dir_path)
    # download_file_path = download_dir_path + r'\data.zip'
    # print('download file:')
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # wget.download(url, download_file_path)
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if url.endswith('.zip'):
        try:
            # response = requests.get(url, headers=headers, verify=False, stream=True)
            response = session.get(url, headers=headers, verify=False, stream=True)
        except Exception as e:
            print(e)
            print('download file out of time')
            return False, name
        flag = True
        os.mkdir(download_dir_path)
        download_file_path = download_dir_path + r'\data.zip'
        with open(download_file_path, 'wb') as f:
            chunk_size = 10000000
            i = 0
            for chunk in response.iter_content(chunk_size):
                print('i = ' + str(i))
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                if i >= 5:
                    print('download file too large')
                    flag = False
                    break
                f.write(chunk)
                i += 1
        if not flag:
            shutil.rmtree(download_dir_path)
            return False, name
        print('file downloaded')
    else:
        os.mkdir(download_dir_path)
        download_file_path = download_dir_path + r'\data.zip'
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            download_not_uri(url, download_file_path)
        except FunctionTimedOut as e:
            print(e)
            print('download file over time')
            shutil.rmtree(download_dir_path)
            return False, name
        except Exception as e:
            print(e)
            print('unknown error happened')
            shutil.rmtree(download_dir_path)
            return False, name
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('file downloaded')

    detail_key = soup.select('.document-metadata > dt')
    detail_val = soup.select('.document-metadata > dd')
    detail_dict = {}
    for i in range(len(detail_key)):
        key = detail_key[i].get_text().replace(':', '').strip()
        val = detail_val[i].get_text().strip()
        detail_dict[key] = val
    with open(download_dir_path + r'\metadata.json', 'w+') as f:
        f.write(json.dumps(detail_dict))
    return True, name


@func_set_timeout(60)
def download_not_uri(url, download_file_path):
    # headers = {'User-Agent': ua.random}
    # res = requests.get(url, headers=headers, verify=False)
    # return res
    wget.download(url, download_file_path)


def test_soup():
    # test_url = 'https://geo.btaa.org/catalog/26287ad9-7d76-4bce-b775-0bf192ac4f19'
    # headers = {'User-Agent': UserAgent().Chrome}
    # res = requests.get(test_url, headers=headers)
    # text = res.text
    # soup = BeautifulSoup(text, 'lxml')

    # page_cnt_str = soup.select('.page-item')[-1].select('a')[0].text
    # page_cnt = int(page_cnt_str.replace(',', ''))
    # print(page_cnt)
    # dataset_cnt_str = soup.select('.page-entries')[0].select('strong')[-1].text
    # dataset_cnt = int(dataset_cnt_str.replace(',', ''))
    # print(dataset_cnt)
    # download_content = soup.select('div.card.card-body > a')
    # url = download_content[0]['href']
    # print(url)
    # name = url.split('/')[-1][0: -4].replace(':', '-')
    # res_headers = requests.get(url, headers=headers).headers
    # max_bytes = 100000000
    # content_bytes = res_headers.get('Content-Length')
    # if int(content_bytes) > max_bytes:
    #     print('file size: ' + content_bytes)
    #     print('download file too large')
    #     return False
    # download_dir_path = root_dir_path + '\\' + name
    # if os.path.exists(download_dir_path):
    #     print('download already done')
    #     return True
    # os.mkdir(download_dir_path)
    # download_file_path = download_dir_path + r'\data.zip'
    # wget.download(url, download_file_path)
    # detail_key = soup.select('.document-metadata > dt')
    # detail_val = soup.select('.document-metadata > dd')
    # print(detail_key)
    # print(detail_val)
    # for i in range(len(detail_key)):
    #     key = detail_key[i].get_text().replace(':', '').strip()
    #     val = detail_val[i].get_text().strip()
    #     print(key)
    #     print(val)
    # dataset_list = 'https://geo.btaa.org/' + soup.select('#documents > article > div > h3 > a')[0]['href']
    # print(dataset_list)
    # download_content = soup.select('div.card.card-body > a')
    # url = download_content[0]['href']
    # res_headers = requests.get(url, headers=headers, verify=False).headers
    # print(res_headers)
    # res = requests.get(url, headers=headers, verify=False, stream=True)
    # flag = True
    # with open(r'D:\Projects\GBFS_Spider\data\xxx.zip', 'wb') as f:
    #     chunk_size = 10000000
    #     i = 0
    #     for chunk in res.iter_content(chunk_size):
    #         print('i = ' + str(i))
    #         print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #         if i >= 10:
    #             print('file too large')
    #             flag = False
    #             break
    #         f.write(chunk)
    #         i += 1
    #         # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # if not flag:
    #     shutil.rmtree(r'D:\Projects\GBFS_Spider\data')
    #     print('file download FAILED')
    # else:
    #     print('file download DONE')
    url = 'https://datacatalog.cookcountyil.gov/api/geospatial/6y64-fiuv?method=export&format=Shapefile'
    # url = 'https://public-iowadot.opendata.arcgis.com/datasets/IowaDOT::0-to-3-in-lower.zip'
    # wget.download(url, r'D:\Projects\GBFS_Spider\xxx.zip')
    # file_name = wget.detect_filename(url)
    # print(file_name)
    download_dir_path = r'D:\Projects\GBFS_Spider\data'
    download_file_path = r'D:\Projects\GBFS_Spider\data\xxx.zip'
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        # func_timeout(1, wget.download(url, download_dir_path))
        download_not_uri(url, download_file_path)
    except FunctionTimedOut as e:
        print(e)
        print('download file over time')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # shutil.rmtree(download_dir_path)
    # func_timeout(5, download_not_uri(url, download_dir_path))
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # download_not_uri(url, download_dir_path)
    # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    download_everything()
    # test_soup()
