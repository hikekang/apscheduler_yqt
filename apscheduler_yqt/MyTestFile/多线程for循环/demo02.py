#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/20 11:52
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : demo02.py
 Description:
 Software   : PyCharm
"""

import multiprocessing.dummy as mp

def do_print(s):
    print(s)

if __name__=="__main__":
    p=mp.Pool(4)
    p.map(do_print,range(0,10)) # range(0,1000) if you want to replicate your example
    p.close()
    p.join()
