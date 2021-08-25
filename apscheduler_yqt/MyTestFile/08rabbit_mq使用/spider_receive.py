#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/5 13:59
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : receive.py
 Description:
 Software   : PyCharm
"""
import pika

hostname='127.0.0.1'

creadentails=pika.PlainCredentials('admin','admin')
connection=pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=creadentails))
spider_datachannel=connection.channel()
spider_datachannel.queue_declare(queue="spider_data")



def clallback_spider(_,__,___,body):
    print("爬取到的数据：%r"%body.decode('utf-8'))
    spider_next_body="%r数据需要清洗正在传送"%body.decode('utf-8')
    print(spider_next_body)
    spider_datachannel.basic_publish(exchange='',routing_key='clear_data',body=body)

spider_datachannel.basic_consume('spider_data',clallback_spider,True)
spider_datachannel.start_consuming()






