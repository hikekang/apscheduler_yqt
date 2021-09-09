#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/26 9:56
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
def test(**kwargs):
    print(kwargs)
    print(kwargs['name'])
def test2(kwargs):
    print(kwargs)
    print(kwargs['name'])
data={
    'name':'hike',
    'age':'18'
}
test(**data)
test2(data)