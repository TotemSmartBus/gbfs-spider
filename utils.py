import os

base_url = 'https://bikeshare-research.org/api/v1/systems/'


def get_url(id):
    return base_url + id

def mkdir(name):
    pwd = os.getcwd()
    exist = os.path.exists(path)