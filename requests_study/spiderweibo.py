#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2145291155',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'X-Requested-With': 'XMLHttpRequest',
}

max_page = 10


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2145291155',
        'containerid': '1076032145291155',
        'page': page
    }

    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json(), page
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json, page: int):
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog', {})
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_cont')
                yield weibo


if __name__ == '__main__':
    for page in range(1, max_page + 1):
        print(page)
        json_str = get_page(page)
        results = parse_page(*json_str)
        for result in results:
            print(result)
