#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/6 17:21
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : demo01.py
 Description:
 Software   : PyCharm
"""
# 自己的简单使用
from redisbloom.client import Client

# 因为我使用的是虚拟机中docker的redis, 填写虚拟机的ip地址和暴露的端口
rb = Client(host='127.0.0.1', port=6379)
rb.bfAdd('urls', 'baidu')
rb.bfAdd('urls', 'google')
print(rb.bfExists('urls', 'baidu'))  # out: 1
print(rb.bfExists('urls', 'tencent'))  # out: 0

rb.bfMAdd('urls', 'a', 'b')
print(rb.bfMExists('urls', 'google', 'baidu', 'tencent'))  # out: [1, 1, 0]