#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/22 10:16
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01eval解析.py
 Description:
 Software   : PyCharm
"""
import datetime
import time
str1="['2021-07-15 00:00:00','2021-07-20 00:00:00']"
test1=eval(str1)
print(type(test1))
print(test1)

start_time = datetime.datetime.strptime(test1[0], "%Y-%m-%d %H:%M:%S")
print(start_time)

xxx=time.mktime(time.strptime(test1[0],'%Y-%m-%d %H:%M:%S'))
print(xxx)
print(type(xxx))