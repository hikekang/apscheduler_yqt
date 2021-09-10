#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/6 16:41
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : spider_producer.py
 Description:
 Software   : PyCharm
"""

import re
from lxml import etree
import time
import pika

# 1.连接mq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 2.可持久化队列
channel.queue_declare(queue='hello3', durable=True)
# 3.指定队列插入数据
channel.basic_publish(
    exchange='',
    routing_key='hello3',
    body='Hello World!',
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    )

)

