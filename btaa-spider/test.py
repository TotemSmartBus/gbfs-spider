import shutil
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

print('hello linux server')
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

test_url = 'https://geo.btaa.org/catalog/26287ad9-7d76-4bce-b775-0bf192ac4f19'
headers = {'User-Agent': UserAgent().Chrome}
res = requests.get(test_url, headers=headers)
text = res.text
soup = BeautifulSoup(text, 'lxml')
download_content = soup.select('div.card.card-body > a')
url = download_content[0]['href']
new_url = 'https://datacatalog.cookcountyil.gov/api/geospatial/uhv8-ar4p?method=export&format=Shapefile'
# res_headers = requests.get(url, headers=headers, verify=False).headers
# print(res_headers)
res = requests.get(new_url, headers=headers, verify=False, stream=True)
flag = True
print(new_url)
with open(r'D:\Projects\GBFS_Spider\data\xxx.zip', 'wb') as f:
    chunk_size = 10000000
    i = 0
    for chunk in res.iter_content(chunk_size):
        print('i = ' + str(i))
        print(len(chunk))
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if i >= 50:
            print('file too large')
            flag = False
            break
        f.write(chunk)
        i += 1
        # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
if not flag:
    shutil.rmtree(r'D:\Projects\GBFS_Spider\data')
    print('file download FAILED')
else:
    print('file download DONE')
