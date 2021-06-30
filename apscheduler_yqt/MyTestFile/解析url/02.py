#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/3 15:31
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 02.py
 Description:
 Software   : PyCharm
"""
# !-*- coding:utf-8 -*-
from urllib.parse import urlparse


def get_domain_by_url(url):
    domain_config = ['com', 'top', 'xyz', 'cx', 'red', 'net', 'cn', 'org', 'edu']

    o = urlparse(url)
    host = o.netloc
    host = host.split('.')
    host.reverse()
    count = len(host)
    res = []
    for i in range(count):
        if host[i] in domain_config:
            res.append(host[i])
        else:
            res.append(host[i])
            break
    res.reverse()
    domain = '.'.join(res)

    return domain


url = "https://www.wx.qq.com.cn";

print(get_domain_by_url(url))


