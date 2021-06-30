#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/6/29 17:56
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 多线程实现斐波那契数列.py
 Description:
 Software   : PyCharm
"""
import threadpool
def fib(x):
    if x < 2 : return 1
    return (fib(x-2) + fib(x-1))
def pool_num(num,p_methond,num_list):
    pool=threadpool.ThreadPool(num) #声明线程池个数
    reqs=threadpool.makeRequests(p_methond,num_list) #生成线程池启动参数
    [pool.putRequest(req) for req in reqs] #循环执行启动线程
    pool.wait() #等待子线程
if __name__ == '__main__':
    pool_num(10,)

