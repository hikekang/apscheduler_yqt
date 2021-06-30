# -*- coding: utf-8 -*-
"""
   File Name：     基本操作
   Description :
   Author :       hike
   time：          2021/4/10 15:42
"""
import redis
"""
redis 提供两个类 Redis 和 StrictRedis,
    StrictRedis 用于实现大部分官方的命令，
    Redis 是 StrictRedis 的子类，用于向后兼用旧版本。
    
redis 取出的结果默认是字节，我们可以设定 decode_responses=True 改成字符串。


"""

# r=redis.Redis(host="127.0.0.1",port=6379,db=0,decode_responses=True)

# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池，这样就可以实现多个 Redis 实例共享一个连接池
pool=redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
r=redis.Redis(connection_pool=pool)
# 增加
'''
set(name, value, ex=None, px=None, nx=False, xx=False)

在Redis中设置值，默认，不存在则创建，存在则修改
参数：
ex，过期时间（秒）
px，过期时间（毫秒）
nx，如果设置为True，则只有name不存在时，当前set操作才执行
xx，如果设置为True，则只有name存在时，当前set操作才执行

'''
r.set('hike','111')
print(r.get('hike'))
r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型

