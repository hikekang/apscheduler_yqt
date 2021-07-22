#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/21 11:27
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 连接失败.py
 Description:
 Software   : PyCharm
"""
from urllib import parse
import redis
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
domain_sub = parse.urlparse('http://www.mp.weixin.qq.com').netloc.replace("www.", "")
rx = domain_sub.split(".")
domain_search = '.'.join(rx)
# print(domain_search)
flag = 0
for i in range(0, len(rx) - 1):
    print(r.hexists("url", '.'.join(rx[i:])))
    print('.'.join(rx[i:]))