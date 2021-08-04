#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/30 12:00
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import  re
highpoints = re.compile(u'[\U00010000-\U0010ffff]')

try:
        # python UCS-4 build的处理方式
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
except re.error:
        # python UCS-2 build的处理方式
         highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
s1='🐴222'
print(type(s1))
print()
s2=highpoints.sub(u'', s1)
print(s2)
print(len(s2))