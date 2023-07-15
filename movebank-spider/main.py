import os.path

import requests
from bs4 import BeautifulSoup
import csv


# 读保存有所有待爬网页url的csv文件，并进行爬虫
def read_csv(filename):
    # 读取CSV文件
    with open(filename, 'r', encoding='utf-8') as csvfile:
        # 创建CSV读取器
        csvreader = csv.reader(csvfile)

        # 跳过第一行
        next(csvreader)

        # 读取第二列并存储到列表中
        data_list = [row[1] for row in csvreader]

    print(data_list)
    print(len(data_list))

    for url in data_list:
        download_data(url)


# 下载某网页中满足条件的可用文件资源
def download_data(root_url):
    # 存放数据文件的根目录
    root_dir = r"/home/lyy/movebank-all/"
    # 发送请求，获取网页内容
    print(f"URL: {root_url}")
    response = requests.get(root_url)
    content = response.content
    # prefix = 'https://www.datarepository.movebank.org/'
    prefix = "https://datarepository.movebank.org/server/api/core"

    # 解析网页内容，获取所有后缀名为CSV的链接
    soup = BeautifulSoup(content, "html.parser")
    links = []
    # 旧方法，语法正确可用但需要修改逻辑
    # for link in soup.find_all('a', href=True):
    #     # print(link)
    #     if re.search(r'\.csv', link['href']) and re.search(r'^(?!.*metadata)(?!.*reference).*$', link['href']):
    #         links.append(prefix + link['href'])

    # 新方法
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "download" in href:
            new_href = href.split("download")[0] + "content"
            # absolute_url = urljoin(prefix, new_href)
            absolute_url = prefix + new_href
            # links.append(absolute_url)
            string = link.get_text()
            if ".txt" in string:
                text = string.split(".txt")[0] + ".txt"
            elif ".csv" in string:
                text = string.split(".csv")[0] + ".csv"
            else:
                print(f"Format error: {string}")
                continue
            # pattern = r"(.+)(\.csv\s|\.txt\s)"
            # match = re.match(pattern, string)
            # if match:
            #     text = match.group(1)[:-1]
            # else:
            #     print(f"Format error: {string}")
            #     continue
            # index = string.index("(")
            # text = string[:index - 1]
            # pattern = r"\("
            # match = re.search(pattern, string)
            # text = string[:match.start()]
            links.append((absolute_url, text))

    if not links:
        print("No valid resource")
        return
    print(f"Found resource: {len(links)}")

    # 输出所有链接
    # print()
    # print(len(links))

    # 保存的目录，旧方法是全存在一级
    # save_dir = r'/home/lyy/movebank-dataset/'
    # for link in links:
    #     # # 发送 HTTP 请求并获取响应头
    #     # response = requests.get(link, stream=True)
    #     # content_disposition = response.headers.get("Content-Disposition")
    #     #
    #     # # 如果响应头中有 Content-Disposition，从中获取文件名
    #     # if content_disposition:
    #     #     name = content_disposition.split("filename=")[-1].strip('"\'')
    #     #
    #     #     # 如果文件名是 URL 编码过的，则进行解码
    #     #     if "%20" in name:
    #     #         name = unquote(name)
    #     # else:
    #     #     # 如果响应头中没有 Content-Disposition，则使用 URL 中的最后一部分作为文件名
    #     #     name = os.path.basename(link)
    #
    #     name = os.path.basename(link)
    #     if '%20' in name:
    #         name = unquote(name)
    #     index = name.find('.csv')
    #     if index != -1:
    #         name = name[:index + 4]
    #         print(name)
    #     else:
    #         print('no csv found')
    #         continue
    #
    #     save_file = os.path.join(save_dir, name)
    #
    #     # 发送 HTTP 请求并下载文件
    #     # response = requests.get(link, stream=True)
    #     # with open(save_file, "wb") as f:
    #     #     for chunk in response.iter_content(chunk_size=1000000):
    #     #         if chunk:
    #     #             f.write(chunk)
    #     urllib.request.urlretrieve(link, save_file)
    #
    #     print(name + ' downloaded')

#     新方法需要将每个网页爬取的内容存放在不同的目录下
#         获取root_url的后缀，作为存放该网页内容的目录名
    dir_name = root_url.split("/")[-1]
    save_dir = os.path.join(root_dir, dir_name)
    os.mkdir(save_dir)

    for link, file_name in links:
        res = requests.get(link)
        # file_name = os.path.basename(link)
        # res_head = requests.head(link)
        # content_disposition = res.headers.get("Content-Disposition")
        # file_name = content_disposition.split("filename=")[-1].strip("\\")
        # file_name = re.findall("filename=(.+)", content_disposition)[0]
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(res.content)
        print(f"Downloaded: {file_name}")


if __name__ == '__main__':
    # filename = r'/home/lyy/movebank_download_pages.csv'
    file_name = r"/home/lyy/movebank_download_pages.csv"
    read_csv(file_name)
    print()
