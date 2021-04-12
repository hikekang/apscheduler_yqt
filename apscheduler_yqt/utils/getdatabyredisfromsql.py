# -*- coding: utf-8 -*-
"""
   File Name：     getdatabyredisfromsql
   Description :
   Author :       hike
   time：          2021/4/12 9:28
"""
import redis
pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True,db=1)
r=redis.Redis(connection_pool=pool)
from utils import ssql_helper
r.lpush(3,2)
datas=ssql_helper.get_month_data()
# 插入数据
for d in datas:
    r.sadd(d[0],d[1])

# 检查数据是否存在

# r.sismember(industry_id,url)

    # tutorial