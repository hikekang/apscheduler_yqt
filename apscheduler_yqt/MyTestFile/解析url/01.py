#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/3 15:17
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from urllib.parse import urlparse

import tldextract
url="http://hike.baidu.com/index.html;user?id=5#comment"
# print(urlparse(url))
# print(tldextract.extract(url).domain)
# print(tldextract.extract(url).subdomain)
netloc=urlparse(url).netloc
print(netloc)
