#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/5/20 11:54
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : demo303.py
 Description:
 Software   : PyCharm
"""
# -*- coding: utf-8 -*-
import time
import math
from multiprocessing.dummy import Pool as ThreadPool
def process(item):
    math.sqrt(item)
items = ['apple', 'bananan', 'cake', 'dumpling']
strt_time=time.time()
pool = ThreadPool()
pool.map(process, range(10,100000))
pool.close()
pool.join()

# for i in range(10,10000000):
#     math.sqrt(i)
end_time=time.time()
print(end_time-strt_time)

st=time.time()
for i in range(100000):
    math.sqrt(i)

ed=time.time()
print(ed-st)
