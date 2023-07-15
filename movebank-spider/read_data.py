import os
import csv
import pandas as pd

# 定义源目录和目标目录
src_dir = r'D:\Projects\GBFS_Spider\movebank-dataset'
dest_dir = r'D:\Projects\GBFS_Spider\movebank-clean'


def read_all():
    for file_name in os.listdir(src_dir):
        print('read file ' + file_name)
        read_one(file_name)


def read_one(file_name):
    if not file_name.endswith(".csv"):
        print("not a csv format file")
        return
    file_path = os.path.join(src_dir, file_name)
    # df = pd.read_csv(file_path)
    # if "location-long" not in df.columns or "location-lat" not in df.columns:
    #     print("don't have lat or lng")
    #     return
    longs = []
    lats = []

    try:
        with open(file_path, 'r', newline='') as f:
            reader_pre = csv.reader(f)
            headers = next(reader_pre, None)
            col_name = 'location-long'
            f.seek(0)
            if col_name not in headers:
                print("don't have lat or lng")
                return
            reader = csv.DictReader(f)
            longs = [row['location-long'] for row in reader]
            f.seek(0)
            reader = csv.DictReader(f)
            lats = [row['location-lat'] for row in reader]
    except Exception as e:
        print(type(e))
        return

    num_rows = len(longs)
    if num_rows <= 10000:
        dest_path = os.path.join(dest_dir, file_name)
        write(dest_path, lats, longs)
    else:
        for i in range(1, num_rows // 10000 + 2):
            start_row = (i - 1) * 10000
            end_row = min(i * 10000, num_rows)
            lats_subset = lats[start_row: end_row]
            lngs_subset = longs[start_row: end_row]
            dest_path = os.path.join(dest_dir, f"{file_name[:-4]}_{i}.csv")
            write(dest_path, lats_subset, lngs_subset)


def write(dest_file, lats, lngs):
    if os.path.isfile(dest_file):
        print('file already written')
    with open(dest_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['lng', 'lat'])
        writer.writerows(zip(lngs, lats))
    print('file ' + dest_file + ' written')


if __name__ == '__main__':
    read_all()
    print()
