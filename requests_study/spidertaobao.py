#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from selenium.webdriver.firefox.options import Options
from pyquery import PyQuery as pq


option = Options()
option.headless = True
brower = webdriver.Firefox(options=option)
wait = WebDriverWait(brower, 100)

KEYWORD = 'iPad'
MAX_PAGE = 100


def get_products():
    """
    提取商品数据
    :return:
    """
    html = brower.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    :return:
    """
    print('正在抓取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        print(url)
        brower.get(url)

        # 判断登录页面是否出现，如果出现，进行登录

        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            print(input)
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def main():
    """
    遍历每一页
    :return:
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    brower.close()


if __name__ == '__main__':
    main()
