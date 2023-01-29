import json
import requests
import os
import zipfile
base_dir = os.getcwd()

# 遇到已有的文件夹是否覆盖？
OVERWRITE = False

fails = []


def save_data(link, code, target_dir, progress):
    print(progress, code, ' downloading.')
    resp = requests.get(link, stream=True)
    if not resp.ok:
        print(progress, 'Error downloading')
        fails.append(code)
        return
    print(progress, code, ' saving.')
    zip_filename = os.path.join(target_dir, code + '.zip')
    with open(zip_filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(progress, code, ' unzipping.')
    zip_file = zipfile.ZipFile(zip_filename)
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件
    for f in zip_list:
        zip_file.extract(f, target_dir)  # 循环解压文件到指定目录
    zip_file.close()  # 关闭文件，必须有，释放内存
    print(progress, code, ' done.')


if __name__ == '__main__':
    join = os.path.join
    source_dir = join(join(join(join(join(base_dir, 'mobility-database-catalogs'), 'catalogs'), 'sources'), 'gtfs'), 'schedule')
    if not os.path.exists(source_dir):
        print('Source Directory not exist! Please Run at its own directory!')
        exit()

    dataset_dir = os.path.join(base_dir, 'datasets')
    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)

    size = len(os.listdir(source_dir))
    current = 0
    for filename in os.listdir(source_dir):
        current += 1
        progress = '[' + str(current) + '/' + str(size) + ']'
        if not filename.endswith('.json'):
            break
        code = filename.split('.')[0]
        target_dir = join(dataset_dir, code)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        elif OVERWRITE:
            os.rmdir(target_dir)
            os.mkdir(target_dir)

        with open(join(source_dir, filename), 'r') as f:
            json_data = json.load(f)
            if json_data['urls']['latest']:
                url = json_data['urls']['latest']
                save_data(url, code, target_dir, progress)

    if len(fails) > 0:
        with open(join(base_dir, 'fails.txt'), 'w') as f:
            for fail in fails:
                f.write(fail)
                f.write('\n')