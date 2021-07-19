#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/6 17:00
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : urlfillter.py
 Description:
 Software   : PyCharm
"""
from pybloom_live import ScalableBloomFilter, BloomFilter

# 可自动扩容的布隆过滤器
bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)

url1 = 'http://www.baidu.com'
url2 = 'http://qq.com'

bloom.add(url1)
print(url1 in bloom)
print(url2 in bloom)