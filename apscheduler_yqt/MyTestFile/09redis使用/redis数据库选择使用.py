#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/5 16:08
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : redis数据库选择使用.py
 Description:
 Software   : PyCharm
"""
import redis

r=redis.StrictRedis(host='localhost', port=6379, decode_responses=True,db=1)
print(r.randomkey)
