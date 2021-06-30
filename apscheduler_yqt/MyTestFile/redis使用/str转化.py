#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/3 17:09
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : str转化.py
 Description:
 Software   : PyCharm
"""
str="(2360, '百度搜索', '全网', 'baidu.com', None, None, None, 8, 1)"
str1=tuple(eval(str))
print(type(str1))