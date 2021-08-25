#!/usr/bin/python3.x
# -*- coding=utf-8 -*-
"""
 Time       : 2021/8/5 17:36
 Author     : hike
 Email      : hikehaidong@gmail.com
 File Name  : upload_data.py
 Description:
 Software   : PyCharm
"""
import pika

hostname='127.0.0.1'

creadentails=pika.PlainCredentials('admin','admin')
connection=pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=creadentails))

upload_data_channel=connection.channel()
upload_data_channel.queue_declare(queue="upload_data_channel")
def callback_upload(_,__,___,body):
    upload_next_body="%r数据接收，进行上传数据库"%body.decode('utf-8')
    print(upload_next_body)

upload_data_channel.basic_consume('upload_data_channel',callback_upload,True)
upload_data_channel.start_consuming()