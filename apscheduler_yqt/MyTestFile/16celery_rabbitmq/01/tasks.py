#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/23 15:37
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : tasks.py
 Description:
 Software   : PyCharm
"""
from celery import Celery

# 中间件，这里使用RabbitMQ，pyamqp://Uername:Password@IP:Port//v_host
broker_url = 'amqp://guest:guest@127.0.0.1:5672//'

# 后端储存，这里使用RabbitMQ，rpc://Uername:Password@IP:Port//v_host
backend_url = 'rpc://guest:guest@192.168.2.129:5672//'

# 实例化一个celery对象
# app = Celery('tasks', broker=broker_url, backend=backend_url)
app = Celery('tasks', broker=broker_url,backend=backend_url)

# 设置配置参数的文件，创建文件celeryconfig.py来配置参数
# app.config_from_object('celeryconfig')


@app.task
def add(x, y):
    """
        求和的函数
    :param x:
    :param y:
    :return:
    """
    return x + y
