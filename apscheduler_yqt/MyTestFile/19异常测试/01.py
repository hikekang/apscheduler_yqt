#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/28 13:32
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import traceback

def test():
    print(20/0)

def test2():
    test()
if __name__ == '__main__':
    try:
        test2()
    except:
        print(traceback.format_exc())