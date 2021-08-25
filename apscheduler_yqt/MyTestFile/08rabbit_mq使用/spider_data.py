#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/5 13:59
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : 01.py
 Description:
 Software   : PyCharm
"""
import pika
import random
hostname='127.0.0.1'
# 1。新建链接
parameters=pika.ConnectionParameters(hostname,credentials=pika.PlainCredentials('admin','admin'))
connection=pika.BlockingConnection(parameters)

# 2.创建通道
channel=connection.channel()

# 3.创建声明一个队列
channel.queue_declare(queue='spider_data')
import time
number=random.randint(1,100000000)

def spider_data():
    for i in range(100):
        time.sleep(0.1)
        body = str(int(time.time() * 1000))
        print(body)
        # 4.发消息
        channel.basic_publish(exchange='',#没有指定就是简单模式
                              routing_key='spider_data',#插入指定队列
                              body=body
                              )

connection.close()