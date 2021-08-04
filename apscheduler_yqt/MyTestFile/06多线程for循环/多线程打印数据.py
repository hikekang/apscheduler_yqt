#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/29 17:51
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 多线程打印数据.py
 Description:
 Software   : PyCharm
"""
import threadpool

def pool_num(num,p_methond,num_list):
    pool=threadpool.ThreadPool(num) #声明线程池个数
    reqs=threadpool.makeRequests(p_methond,num_list) #生成线程池启动参数
    [pool.putRequest(req) for req in reqs] #循环执行启动线程
    pool.wait() #等待子线程
def p_methond(num):
    print(num)
num_list=[i for i in range(1,101)]
pool_num(3,p_methond,num_list)