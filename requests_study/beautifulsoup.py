#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup

soup = BeautifulSoup('<p>hello world</p>', 'lxml')
print(soup.p.string)
