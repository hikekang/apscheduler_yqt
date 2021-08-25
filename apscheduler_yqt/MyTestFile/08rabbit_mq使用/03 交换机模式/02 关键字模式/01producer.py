#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/6 10:58
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : producer.py
 Description:
 Software   : PyCharm
"""
import pika

# 1.连接mq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明名为logs交换机
channel.exchange_declare(exchange='logs1',exchange_type='direct')

channel.basic_publish(exchange='logs1',
                      routing_key='hike',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")
connection.close()