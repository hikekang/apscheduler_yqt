# -*- coding: utf-8 -*-
"""
   File Name：     redis_helper
   Description :
   Author :       hike
   time：          2021/5/9 18:16
"""
import redis

class my_redis():
    def __init__(self,host='localhost', port=6379, decode_responses=True,db=0):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True,db=db)
        self.redis = redis.Redis(connection_pool=self.pool)
    def close(self):
        self.redis.close()


if __name__ == '__main__':
    test_redis=my_redis(host='localhost', port=6379, decode_responses=True,db=1)
    print(test_redis.redis.randomkey())
    # print(test_redis.redis.sismember('12','http://weibo.com/1689123691/KeP2OnPDu'))
    test_redis.close()