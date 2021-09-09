#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/23 15:39
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : task.py
 Description:
 Software   : PyCharm
"""
# -*- coding: utf-8 -*-

import time
from celery import Celery
# 消息中间件
broker = 'redis://127.0.0.1:6379'
# 存储
backend = 'redis://127.0.0.1:6379/0'

# 创建一个名为app的celery
app = Celery('my_task', broker=broker, backend=backend)

# celery 可调度的任务
@app.task
def add(x, y):
    time.sleep(5)     # 模拟耗时操作
    return x + y