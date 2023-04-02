# coding:utf-8
#!/usr/bin/python

import json
import os
import requests


def save_json_data(file_path, datas):
    # fl = open('json/'+title.decode('utf-8') + '.json', 'w')
    with open(file_path, 'w', encoding='utf8') as fl:
        fl.write(json.dumps(datas, sort_keys=True, indent=4, separators=(
            ',', ': '), ensure_ascii=False))
        fl.close()

    print(file_path + ' save success')


def UpdateToJson(file_path, datas):
    with open(file_path, 'a', encoding='utf8') as fl:
        fl.write(json.dumps(datas, sort_keys=True, indent=4, separators=(
            ',', ': '), ensure_ascii=False))
        fl.close()
    print(file_path + 'save success')


def load_json_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def check_file_exists(file_path):
    return os.path.isfile(file_path)

def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print(path)
        return
