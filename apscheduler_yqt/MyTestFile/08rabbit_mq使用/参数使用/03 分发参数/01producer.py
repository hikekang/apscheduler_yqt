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
# 2.可持久化队列
channel.queue_declare(queue='hello4', durable=True)
# 3.指定队列插入数据
channel.basic_publish(
    exchange='',
    routing_key='hello4',
    body='Hello World!5689998',
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    )

)

print(" [x] Sent 'Hello World!'")
