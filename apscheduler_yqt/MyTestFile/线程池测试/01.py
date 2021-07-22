#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/20 14:11
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
from concurrent.futures.thread import ThreadPoolExecutor

import threading
cond=threading.Condition()
def producer():
    cond.acquire()
    print("生产")
    cond.wait()
    print("生产完毕")
    cond.notify()
    cond.release()

    pass
def customer():
    cond.acquire()
    print("消费")
    cond.notify()
    cond.wait()
    print("消费完毕")
    pass

with ThreadPoolExecutor(10) as pool:
    for i in range(10):
        pool.submit(producer)
        pool.submit(customer)