#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re
import time

base_url = "https://www.toutiao.com/api/search/content/?"

headers = {
    'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    'Host': 'www.toutiao.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Upgrade-Insecure-Requests': 1,
}


def get_page(offset):
    params = {
        # "aid": 24,
        "app_name": "web_search",
        "offset": offset,
        "format": "json",
        "autoload": "true",
        "keyword": "街拍",
        "count": 20,
        "en_qc": 1,
        "cur_tab": 1,
        "from": "search_tab",
        "pd": "synthesis",
        "timestamp": int(time.time() * 1000),
    }

    url = base_url + urlencode(params)
    print(url)

    try:
        resp = requests.get(url, headers=headers)
        if 200 == resp.status_code:
            return resp.json()
    except requests.ConnectionError:
        return None


def get_image(json):
    if json.get("data"):
        data = json.get("data")
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub("list/300x196", "origin", image.get('url'))
                yield {
                    "image": origin_image,
                    "title": title
                }


def save_image(item):
    image_path = 'img' + os.path.sep + item.get("title")
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    try:
        resp = requests.get(item.get("image"))
        print(resp.status_code)
        if codes.ok == resp.status_code:
            file_path = image_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg'
            )
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print("download image path is %s" % file_path)
            else:
                print("already download", file_path)
    except requests.ConnectionError:
        print("failed to save image, item %s" % item)


def main(offset):
    json = get_page(offset)
    for item in get_image(json):
        print(item)
        save_image(item)


GROUP_START = 0
GROUP_END = 7


if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
