# 1. 从handle-dspace-lookup.csv文件读取出所有dspace-id，作为后续爬虫的变量
# 2. 爬取zip文件
# 3. 处理zip文件（解压以及进一步提取数据）
# 先测试第二步，成功了再完成第一步
# 第二步可行，接下来完成第一步
# 第二步完成，接下来整合前两步，优化代码
# 修改
# 2. 爬取zip文件
#     2.1 通过1的网址爬取下页面
#     2.2 判断页面是否可读，可能存在需要登录无法访问的问题
#     2.3 通过元素选择器选择指定的文件URL
#     2.4 需要判断文件大小，太大的舍弃

# 改进
# 1. 下载GitHub上对应仓库的所有json文件，每个文件对应着一个dataset的metadata
# 2. 爬虫，把爬取到的文件解压到metadata所在的目录

import os.path
import urllib.request
import requests
from bs4 import BeautifulSoup
import zipfile
import csv
from fake_useragent import UserAgent
import shapefile

# 正式开始，上面的基础上添加辅助信息


# 1. 从handle-dspace-lookup.csv文件读取出所有dspace-id，作为后续爬虫的变量
lookup_dir = 'handle-dspace-lookup.csv'
dspace_id_list = []
log = 'LOG'
with open(lookup_dir) as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        dspace_id_list.append(row[0].split('/')[-1])
# print('Totally ' + len(dspace_id_list) + 'dataset files')
# log = log + 'Totally ' + len(dspace_id_list) + 'dataset files'
# t = 'Totally ' + len(dspace_id_list) + 'dataset files'
# log = logging(log, 'Totally ' + len(dspace_id_list) + 'dataset files')

# 创建datasets文件夹
base_dir = os.getcwd()
dataset_dir = os.path.join(base_dir, 'datasets')
if not os.path.exists(dataset_dir):
    os.mkdir(dataset_dir)


def logging(text) -> str:
    print(text)
    return log + '\n' + text


# 爬虫、下载、解压
def spider(file_id) -> bool:
    global log
    url = f'https://archive.nyu.edu/handle/2451/{file_id}'
    headers = {'User-Agent': UserAgent().Chrome}
    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        log = logging('NO URL EXISTS!!!')
        return False
    text = res.text
    soup = BeautifulSoup(text, 'lxml')
    # print(soup.prettify())
    # 测试代码
    tmp = soup.select('.panel-body > tr')
    # print(tmp)
    if not tmp:
        log = logging('ACCESS DENIED!!!')
        return False
    title = soup.select('.page-title')[0].text
    # print(title)
    tr = soup.select('.panel-body > tr')[1]
    href = tr.select('a')[0]['href']
    name = href.split('/')[-1]
    # print(href)
    size = tr.find(headers='t3').text
    # print(size)
    if size[-2:] == 'GB':
        log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: File too large')
        return False
    if size[-2:] == 'MB':
        num = float(size.split(' ')[0])
        if num > 100:
            log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: File too large')
            return False
    if href[-3:] != 'zip':
        log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: Not a zip file')
        return False
    base_url = 'https://archive.nyu.edu'
    file_url = f'{base_url}{href}'
    # file_dir = f'{dataset_dir}/{file_id}.zip'
    metadata_dir = f'{dataset_dir}/{file_id[0]}/{file_id[1:3]}/{file_id[3:5]}'
    if not os.path.exists(metadata_dir):
        log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: No metadata exists')
        return False
    # if not os.path.exists(unzip_dir):
    #     os.mkdir(unzip_dir)
    file_dir = f'{metadata_dir}/{name}.zip'
    unzip_dir = f'{metadata_dir}/{name}'
    if os.path.exists(unzip_dir):
        log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: File already exists')
        return True
    try:
        urllib.request.urlretrieve(file_url, file_dir)
    except Exception as e:
        print(e)
        log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: Download failed')
        return False
    # file_dir_new = f'{unzip_dir}/{name}'
    # 下面的判断冗余，但先不删
    if not zipfile.is_zipfile(file_dir):
        log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: Not a zip file')
        return False
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    zf = zipfile.ZipFile(file_dir, 'r')
    for f in zf.namelist():
        zf.extract(f, unzip_dir)
    zf.close()
    log = logging(f'<{file_id}> :: {title} :: {name} :: {size} :: Done')
    return True


# 2. 爬虫
valid_id_list = []
for i, file_id in enumerate(dspace_id_list):
    log = logging(f'[{i}/{len(dspace_id_list)}]')
    flag = spider(file_id)
    if flag:
        valid_id_list.append(file_id)
log = logging(f'Totally [{len(valid_id_list)}/{len(dspace_id_list)}] files valid')
log_dir = 'log.txt'
with open(log_dir, 'a+') as f:
    print(log, file=f)
