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
import pickle
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=str({"name":"hike","age":"18","test":{"page":18}}))
                      # body="hello")

print(" [x] Sent 'Hello World!'")