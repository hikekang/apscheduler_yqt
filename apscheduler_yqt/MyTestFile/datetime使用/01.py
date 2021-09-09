#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/30 16:15
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import datetime

# print(datetime)
print()

def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1
if __name__ == '__main__':
    print(_cmp(1,1))