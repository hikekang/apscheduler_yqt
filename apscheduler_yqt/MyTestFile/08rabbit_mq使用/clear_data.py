#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/5 17:35
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : clear_data.py
 Description:
 Software   : PyCharm
"""
import pika

hostname='127.0.0.1'
# 1。连接
creadentails=pika.PlainCredentials('admin','admin')
connection=pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=creadentails))
clear_data_channel=connection.channel()
# 2.创建队列
clear_data_channel.queue_declare(queue="clear_data")
#3。确定回调函数
def callback_clear(_,__,___,body):
    print("清洗数据:%r"%body)
    clear_back="%r数据清洗完毕,正在进行上传"%body.decode('utf-8')
    print(clear_back)
    clear_data_channel.basic_publish(exchange='',# 简单模式
                                     routing_key='upload_data_channel',#
                                     body=body)

#4.确定监听队列
clear_data_channel.basic_consume('clear_data',callback_clear,True)
clear_data_channel.start_consuming()