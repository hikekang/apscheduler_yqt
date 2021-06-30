#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/20 10:48
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : demo01.py
 Description:
 Software   : PyCharm
"""
import threading

def ThFun(start, stop):
    for item in range(start, stop):
        print (item)

for n in range(0, 1000, 100):
    stop = n + 100 if n + 100 <= 1000 else 1000
    threading.Thread(target = ThFun, args = (n, stop)).start()