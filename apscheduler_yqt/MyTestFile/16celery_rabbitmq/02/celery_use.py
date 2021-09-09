#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/23 15:38
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : celery.py
 Description:
 Software   : PyCharm
"""
from celery import Celery

# 中间件，这里使用RabbitMQ，pyamqp://Uername:Password@IP:Port//v_host
# broker_url = 'pyamqp://development:root@192.168.2.129:5672//development_host'
broker_url = 'amqp://guest:guest@localhost:5672//'

# 后端储存，这里使用RabbitMQ，rpc://Uername:Password@IP:Port//v_host
backend_url = 'rpc://development:root@192.168.2.129:5672//development_host'

# 实例化一个celery对象
app = Celery('tasks', broker=broker_url, backend=backend_url, include=['proj.tasks'])

app.conf.update(result_expires=3600, )

if __name__ == '__main__':
    app.start()