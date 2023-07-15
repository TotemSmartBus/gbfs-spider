import os
from pathlib import Path
import shutil

root_dir_path = Path(r'D:\Projects\GBFS_Spider\btaa-dataset')


def delete_all():
    for dir_item in os.listdir(root_dir_path):
        dir_path = os.path.join(root_dir_path, dir_item)
        cnt = len(os.listdir(dir_path))
        # 没有解压后的数据文件，删除整个目录
        if cnt < 3:
            shutil.rmtree(dir_path)
        # 有解压后的数据文件，删除压缩文件
        else:
            for file in os.listdir(dir_path):
                if str(file).endswith('.zip'):
                    file_path = os.path.join(dir_path, file)
                    os.remove(file_path)
                    break
    print('done')


if __name__ == '__main__':
    delete_all()
