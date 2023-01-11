import json
import requests
import os

base_url = 'https://bikeshare-research.org/api/v1/categories/base'
url_prefix = 'https://bikeshare-research.org/api/v1/systems/'
bss_base = {}
bss_data = {}

base_dir = os.getcwd()
dataset_dir = 'datasets'


def get_bss_info() -> {}:
    resp = requests.get(base_url)
    data = resp.json()
    map = {}
    for item in data:
        map[item['bssid']] = item
    return map


def get_all_data(bssid):
    resp = requests.get(url_prefix + bssid)
    return resp.json()


def save(bss_id, bss_info, base_path):
    # basic info
    with open(os.path.join(base_path, bssid + '.json'), 'w') as f:
        f.write(json.dumps(bss_base[bss_id]))
    # all info
    with open(os.path.join(base_path, 'full.json'), 'w') as f:
        f.write(json.dumps(bss_info))
    # details
    for key, value in bss_info.items():
        with open(os.path.join(base_path, key + '.json'), 'w') as f:
            f.write(json.dumps(bss_info[key]))


if __name__ == '__main__':
    # collect data meta info
    print('getting bss system list')
    bss_base = get_bss_info()
    print('get ' + str(len(bss_base)) + ' bss system')

    data_root_dir = os.path.join(base_dir, dataset_dir)
    if not os.path.exists(data_root_dir):
        os.mkdir(data_root_dir)

    for bssid, bss_info in bss_base.items():
        # collect data
        print('getting data for ' + bssid)
        bss_data[bssid] = get_all_data(bssid)
        print('get data for ' + bssid + 'succeed')
        # save data
        print('saving data for ' + bssid)
        bss_dir = os.path.join(data_root_dir, bssid)
        if not os.path.exists(bss_dir):
            os.mkdir(bss_dir)
        save(bssid, bss_info, bss_dir)
        print('saved data for ' + bssid + ' succeed')
    print('done')
