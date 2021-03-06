#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/7/6 17:03
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : demo2.py
 Description:
 Software   : PyCharm
"""
import redis
from redisbloom.client import Client

# 创建一个连接池来进行使用
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=100)


def create_key(key, error, capacity):
    rb = Client(connection_pool=pool)
    rb.bfCreate(key, errorRate=error, capacity=capacity)


def get_item(key, item):
    """判断是否存在"""
    rb = Client(connection_pool=pool)
    return rb.bfExists(key, item)


def add_item(key, item):
    """添加值"""
    rb = Client(connection_pool=pool)
    return rb.bfAdd(key, item)


if __name__ == '__main__':
    # 添加黑名单, 误差为0.001， 大小为1000
    create_key('blacklist', 0.001, 1000)
    add_item('blacklist', 'user:1')
    add_item('blacklist', 'user:2')
    add_item('blacklist', 'user:3')
    add_item('blacklist', 'user:4')
    print('user:1是否在黑名单-> ', get_item('blacklist', 'user:1'))
    print('user:2是否在黑名单-> ', get_item('blacklist', 'user:2'))
    print('user:6是否在黑名单-> ', get_item('blacklist', 'user:6'))