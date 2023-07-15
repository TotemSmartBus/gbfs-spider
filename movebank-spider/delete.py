import os

dir_path = r'/home/lyy/movebank-all/'  # 目录路径

for root, dirs, files in os.walk(dir_path):
    for filename in files:
        if filename != 'README.txt':
            file_path = os.path.join(root, filename)
            print(f'Deleting file: {file_path}')
            os.remove(file_path)