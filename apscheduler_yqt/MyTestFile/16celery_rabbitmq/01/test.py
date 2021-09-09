#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/24 14:24
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : test.py
 Description:
 Software   : PyCharm
"""
from tasks import add
result=add.delay(4,4)
print(result)
print(result.get())