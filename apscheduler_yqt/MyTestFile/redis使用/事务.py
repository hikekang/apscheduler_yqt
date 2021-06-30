# -*- coding: utf-8 -*-
"""
   File Name：     事务
   Description :
   Author :       hike
   time：          2021/4/14 11:45
"""
import redis
pool=redis.ConnectionPool(host='localhost', port=6379,decode_responses=True,db=0)
r=redis.Redis(connection_pool=pool)
